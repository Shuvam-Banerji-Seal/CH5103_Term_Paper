"""CPU speed-ups for Breeze-TTS-2's eager generation path, without changing what the model computes.

1. `quantize_linears`: int8 weight-only linear layers (symmetric, one scale per output channel) through
   `torch.ops.aten._weight_int8pack_mm`. Half the memory of bfloat16 and 2-7x faster at 1-8 rows on this Zen 4
   CPU; the matmul error is ~0.8 % relative (measured in plans/video/research.md). Many rows (a prompt's
   prefill) use a dequantised bfloat16 GEMM, same weights.
2. `patch_depth_cfg`: the vendored eager classifier-free-guidance depth loop runs the depth decoder twice per
   codebook (cond, then uncond) and recomputes the whole codebook prefix each time (`use_cache=False`), so 30
   uncached passes per audio frame. The replacement stacks cond and uncond rows into one batch and keeps a KV
   cache, so 15 single-token passes. Causal attention makes the cached logits equal to the recomputed ones up to
   rounding; test_fastcpu.py checks this against the original loop's own forward passes.
"""
from __future__ import annotations

import types

import torch
from torch import nn


class Int8Linear(nn.Module):
    """y = x W^T (+ b) with W stored as int8 rows and one bfloat16 scale per output channel."""

    def __init__(self, linear: nn.Linear) -> None:
        super().__init__()
        w = linear.weight.detach().float()
        scale = (w.abs().amax(dim=1) / 127.0).clamp(min=1e-12)
        self.in_features, self.out_features = linear.in_features, linear.out_features
        self.register_buffer("weight_int8", torch.round(w / scale[:, None]).clamp(-127, 127).to(torch.int8).contiguous())
        self.register_buffer("scale", scale.to(torch.bfloat16))
        self.bias = None if linear.bias is None else nn.Parameter(linear.bias.detach().clone(), requires_grad=False)

    # _weight_int8pack_mm is a matrix-vector kernel: its cost is flat up to ~8 rows and then linear in the rows,
    # so a prompt's prefill (hundreds of rows) goes through a dequantised bfloat16 GEMM instead.
    GEMM_ROWS = 64

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        shape = x.shape
        x2 = x.reshape(-1, self.in_features).to(torch.bfloat16)
        if x2.shape[0] >= self.GEMM_ROWS:
            w = self.weight_int8.to(torch.bfloat16) * self.scale[:, None]
            y = nn.functional.linear(x2, w)
        else:
            y = torch.ops.aten._weight_int8pack_mm(x2.contiguous(), self.weight_int8, self.scale)
        y = y.reshape(*shape[:-1], self.out_features).to(x.dtype)
        return y if self.bias is None else y + self.bias.to(y.dtype)

    def extra_repr(self) -> str:
        return f"in_features={self.in_features}, out_features={self.out_features}, int8 weight-only"


def quantize_linears(root: nn.Module, *, min_features: int = 256) -> int:
    """Replace every nn.Linear under `root` whose sides are both >= min_features. Returns how many."""
    targets = [(name, mod) for name, mod in root.named_modules()
               if isinstance(mod, nn.Linear) and min(mod.in_features, mod.out_features) >= min_features]
    for name, mod in targets:
        parent_name, _, child = name.rpartition(".")
        parent = root.get_submodule(parent_name) if parent_name else root
        setattr(parent, child, Int8Linear(mod))
        del mod
    return len(targets)


def _sample_next(logits: torch.Tensor, generation_config) -> torch.Tensor:
    """The vendored loop's sampling rule (temperature, top-k, top-p, multinomial), unchanged."""
    temperature, top_p, top_k = generation_config.temperature, generation_config.top_p, generation_config.top_k
    if temperature is not None and temperature != 1.0:
        logits = logits / temperature
    if not generation_config.do_sample:
        return torch.argmax(logits, dim=-1, keepdim=True)
    probs = nn.functional.softmax(logits, dim=-1)
    if top_k is not None and top_k > 0:
        top_k_probs, top_k_indices = torch.topk(probs, min(top_k, probs.size(-1)))
        probs = torch.zeros_like(probs).scatter_(-1, top_k_indices, top_k_probs)
        probs = probs / probs.sum(dim=-1, keepdim=True)
    if top_p is not None and top_p < 1.0:
        sorted_probs, sorted_indices = torch.sort(probs, descending=True)
        remove = torch.cumsum(sorted_probs, dim=-1) > top_p
        remove[..., 1:] = remove[..., :-1].clone()
        remove[..., 0] = 0
        probs = probs.masked_fill(remove.scatter(-1, sorted_indices, remove), 0.0)
        probs = probs / probs.sum(dim=-1, keepdim=True)
    return torch.multinomial(probs, num_samples=1)


def depth_cfg_cached(self, depth_decoder_input_ids: torch.LongTensor, cond_backbone_hidden_state: torch.FloatTensor,
                     uncond_backbone_hidden_state: torch.FloatTensor, cfg_scale: float,
                     *, trace: list | None = None) -> torch.LongTensor:
    """Drop-in for BreezeGenerationMixin._depth_decoder_generate_with_cfg (same arguments and result).

    `depth_decoder_input_ids` is [B, 2] = (placeholder, codebook-0 token); position 0 of the depth decoder takes
    the projected backbone state instead of the placeholder's embedding. Rows 0..B-1 are cond, B..2B-1 uncond.
    `trace`, if given, collects each step's guided logits (for the equivalence test)."""
    depth = self.depth_decoder
    b = depth_decoder_input_ids.shape[0]
    sequences = depth_decoder_input_ids
    out = depth(input_ids=torch.cat([sequences, sequences]),
                backbone_last_hidden_state=torch.cat([cond_backbone_hidden_state, uncond_backbone_hidden_state]),
                use_cache=True, logits_to_keep=1, return_dict=True)
    cache = out.past_key_values
    for step in range(self.config.num_codebooks - 1):
        logits = out.logits[:, -1, :].float()
        cond, uncond = logits[:b], logits[b:]
        guided = uncond + cfg_scale * (cond - uncond)
        self._mask_reserved_codec_logits(guided)
        if trace is not None:
            trace.append(guided.clone())
        nxt = _sample_next(guided, depth.generation_config)
        sequences = torch.cat([sequences, nxt], dim=-1)
        if step == self.config.num_codebooks - 2:
            break
        pos = sequences.shape[1] - 1  # the new token's position in the depth sequence
        out = depth(input_ids=torch.cat([nxt, nxt]), past_key_values=cache, use_cache=True, logits_to_keep=1,
                    cache_position=torch.tensor([pos], device=sequences.device), return_dict=True)
        cache = out.past_key_values
    return sequences


def patch_depth_cfg(model) -> None:
    model._depth_decoder_generate_with_cfg = types.MethodType(depth_cfg_cached, model)
