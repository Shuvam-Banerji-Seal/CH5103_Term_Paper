"""Breeze-TTS-2 narration for the explainer video (CPU, bfloat16, eager), loading the model once.

usage (from the repo root):
  uv run --project video/tts python -E -s video/tts/synth.py smoke [--threads 8] [--cfg 4]
  uv run --project video/tts python -E -s video/tts/synth.py design            # candidate narrator voices
  uv run --project video/tts python -E -s video/tts/synth.py batch [--limit N] # every line in requests.jsonl

The model code is vendored in video/tts/breeze (breeze-tts commit 6eba901). `python -E -s` ignores a global
PYTHONPATH while keeping this script's directory importable (`-I` would drop it).
"""
from __future__ import annotations

import argparse
import json
import resource
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE / "breeze"))

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
import torch  # noqa: E402

CKPT = HERE / "checkpoints" / "breeze-tts-2"
BUILD = ROOT / "video" / "build" / "tts"
STORE = BUILD / "store"
REQUESTS = BUILD / "requests.jsonl"
VOICE_DIR = HERE / "voice"  # the narrator's reference recording (committed): reference.wav + reference.txt

NARRATOR = ("A clear, warm and calm male lecturer with a neutral international English accent, speaking at a steady, "
            "unhurried pace with precise articulation, like a patient university teacher explaining mathematics.")
# The voice-design prompt for the narrator's reference recording. NARRATOR spoke at ~1.8 words per second (too
# slow for three hours of narration); "moderately brisk" gave 3.5-3.8 (too fast for mathematics); "calm, measured
# and even" gave 1.9-2.3.
NARRATOR_V2 = ("A clear, warm male lecturer with a neutral international English accent, speaking at a natural "
               "conversational pace, neither rushed nor slow, with crisp articulation and an engaged, friendly tone, "
               "like a good university teacher explaining mathematics.")
REFERENCE_TEXT = ("Today we will follow the whole argument, one step at a time. Every equation is derived on screen, "
                  "and every claim is checked against the original paper.")


class Breeze:
    """The model on the CPU in bfloat16, generating with the eager (non-streaming) Hugging Face path: the
    streaming runtime needs CUDA, while BreezeForConditionalGeneration.generate falls back to eager modules,
    including its own classifier-free-guidance depth decoder."""

    def __init__(self, threads: int = 8, quantize: bool = True, depth: str = "bf16") -> None:
        from breeze_infer.runtime import load_runtime, update_generation_config_for_breeze

        torch.set_num_threads(threads)
        t0 = time.time()
        self.tok, self.model, self.atok = load_runtime(CKPT, device="cpu", attn_implementation="eager")
        update_generation_config_for_breeze(self.model)
        # The weights arrive memory-mapped from the checkpoint. On this 15 GB laptop (shared with a browser and
        # other jobs) the bfloat16 model does not stay resident: the kernel evicts its file pages and every
        # decoding step re-reads them from disk, and private copies get the process OOM-killed. Int8 copies of
        # the transformer layers (2.5 GB) stay resident; the large embedding tables stay mapped, touched only at
        # the rows a line uses. See fastcpu.py.
        from fastcpu import patch_depth_cfg, quantize_linears

        parts = ("backbone_model", "text_encoder") + (("depth_decoder",) if depth == "int8" else ())
        self.quantized = {name: quantize_linears(getattr(self.model, name)) if quantize else 0 for name in parts}
        # The depth decoder runs 15 times per audio frame, so it sets the speed. The int8 kernel costs the same for
        # 1-8 rows and then grows linearly, while a bfloat16 GEMM costs ~2x more at 1 row but stays flat up to ~32
        # rows (research.md): int8 suits batches of up to ~8 lines, bfloat16 larger ones. bfloat16 weights are
        # copied into private memory (0.8 GB) so that they cannot be evicted.
        with torch.no_grad():
            for t in list(self.model.depth_decoder.parameters()) + list(self.model.depth_decoder.buffers()):
                t.data = t.data.clone()
        patch_depth_cfg(self.model)
        _cache_prompt_audio()
        self.load_seconds = time.time() - t0

    @property
    def rate(self) -> int:
        return int(self.model.config.codec_config.sampling_rate)

    def say(self, text: str, **kw) -> np.ndarray:
        return self.say_batch([text], **kw)[0]

    def say_batch(self, texts: list[str], *, instruction: str | None = None, ref_audio: Path | None = None,
                  ref_text: str | None = None, cfg_scale: float = 1.0, seed: int = 42,
                  max_new_tokens: int = 1500) -> list[np.ndarray]:
        """One generate() call for several lines (same voice settings). The CPU cost of a decoding step is mostly
        reading the weights, which a batch shares, so throughput grows almost linearly with the batch size."""
        from transformers.generation.logits_process import LogitsProcessorList

        from breeze_infer.batch import eager_batch_modules
        from breeze_infer.runtime import set_all_seeds
        from breeze_infer.templates import get_template, prepare_inputs, select_template_name
        from models.logits_process import GeneratedTokenRepetitionPenaltyLogitsProcessor

        requests = []
        for i, text in enumerate(texts):
            request: dict = {"id": f"line{i}", "text": text, "speaker": "S0"}
            if instruction:
                request["instruction"] = instruction
            if ref_audio is not None:
                request["ref_audio_path"] = str(ref_audio)
                request["ref_text"] = ref_text
            requests.append(request)
        set_all_seeds(seed)
        inputs = prepare_inputs(self.tok, self.atok, self.model, requests,
                                get_template(select_template_name(requests[0])), guidance_scale=cfg_scale,
                                guidance_scale_ref=None, guidance_scale_ins=None)
        lp = LogitsProcessorList([GeneratedTokenRepetitionPenaltyLogitsProcessor(1.1)])
        with eager_batch_modules(self.model), torch.inference_mode():
            audio = self.model.generate(**inputs, output_audio=True, audio_tokenizer=self.atok,
                                        logits_processor=lp, max_new_tokens=max_new_tokens)
        return [a.detach().float().cpu().numpy().reshape(-1) for a in audio]


def _cache_prompt_audio() -> None:
    """Encode each reference recording once, not once per line of a batch."""
    import functools

    import breeze_infer.templates as templates

    if not getattr(templates._encode_prompt_audio, "cached", False):
        once = functools.lru_cache(maxsize=8)(templates._encode_prompt_audio)
        templates._encode_prompt_audio = lambda atok, path: once(atok, path).clone()
        templates._encode_prompt_audio.cached = True


def peak_rss_gb() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024


def cmd_smoke(args) -> None:
    text = ("Now add the two determinants, keeping track of every term. Write A for phi a of electron one times phi b "
            "of electron two, and B for the same product with the two electrons swapped.")
    tts = Breeze(args.threads)
    print(f"model loaded in {tts.load_seconds:.1f} s, int8 linears {tts.quantized}, peak RSS {peak_rss_gb():.2f} GB, "
          f"sample rate {tts.rate}", flush=True)
    t0 = time.time()
    audio = tts.say(text, instruction=NARRATOR, cfg_scale=args.cfg, seed=args.seed)
    dt = time.time() - t0
    dur = len(audio) / tts.rate
    out = BUILD / "smoke.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(out, audio, tts.rate, subtype="PCM_16")
    print(f"synth {dt:.1f} s for {dur:.2f} s of audio: real-time factor {dt / max(dur, 1e-9):.2f} "
          f"(threads {args.threads}, cfg {args.cfg}); peak RSS {peak_rss_gb():.2f} GB -> {out}")


BENCH_LINES = [
    "Step one. In an ionic configuration both electrons sit in one orbital.",
    "That spatial part is symmetric: swapping the electrons changes nothing.",
    "Since the total must be antisymmetric, its spin part must be the antisymmetric singlet.",
    "So only the singlet can borrow energy from ionic configurations.",
    "Their energies are U plus k and U minus k.",
    "Write each orbital energy as alpha plus x beta.",
    "They share no atom: the orbitals of this molecule are disjoint.",
    "Meta xylylene is also nondisjoint.",
    "Atom three has a single neighbour, atom one, so its rule forces c one to be zero.",
    "A rank can never exceed the smaller side of the matrix.",
    "The zero blocks say that no bond joins two starred atoms or two unstarred atoms.",
    "Every entry is one we derived before, with the new names.",
    "Two contributions compete, and the larger one decides the ground state.",
    "That mapping is qualitative: the review gives no numbers to test.",
    "It is the same state with different bookkeeping.",
    "Applied bond by bond, this coupling will build the topology rules later on.",
]


def cmd_bench(args) -> None:
    """Throughput of voice-clone synthesis (reference = smoke.wav) against the batch size."""
    ref_text = ("Now add the two determinants, keeping track of every term. Write A for phi a of electron one times phi "
                "b of electron two, and B for the same product with the two electrons swapped.")
    tts = Breeze(args.threads, depth=args.depth)
    for bsz in [int(x) for x in args.sizes.split(",")]:
        lines = [BENCH_LINES[i % len(BENCH_LINES)] for i in range(bsz)]
        t0 = time.time()
        audio = tts.say_batch(lines, ref_audio=BUILD / "smoke.wav", ref_text=ref_text, cfg_scale=args.cfg, seed=args.seed)
        dt = time.time() - t0
        dur = sum(len(a) for a in audio) / tts.rate
        for i, a in enumerate(audio):
            sf.write(BUILD / f"bench_b{bsz}_{i}.wav", a, tts.rate, subtype="PCM_16")
        print(f"batch {bsz}: {dt:.1f} s for {dur:.1f} s of audio ({[round(len(a) / tts.rate, 1) for a in audio]}): "
              f"effective real-time factor {dt / dur:.2f}; peak RSS {peak_rss_gb():.2f} GB", flush=True)


def cmd_profile(args) -> None:
    """Where the time of one short voice-clone line goes (cProfile: cumulative, then own time)."""
    import cProfile
    import pstats

    ref_text = ("Now add the two determinants, keeping track of every term. Write A for phi a of electron one times phi "
                "b of electron two, and B for the same product with the two electrons swapped.")
    tts = Breeze(args.threads)
    lines = BENCH_LINES[:int(args.sizes.split(",")[0])]
    tts.say_batch(lines, ref_audio=BUILD / "smoke.wav", ref_text=ref_text, cfg_scale=args.cfg, max_new_tokens=10)
    prof = cProfile.Profile()
    t0 = time.time()
    prof.enable()
    audio = tts.say_batch(lines, ref_audio=BUILD / "smoke.wav", ref_text=ref_text, cfg_scale=args.cfg,
                          max_new_tokens=40)
    prof.disable()
    dt = time.time() - t0
    print(f"batch {len(lines)}: {dt:.1f} s for 40 frames", flush=True)
    prof.dump_stats(str(BUILD / f"profile_b{len(lines)}.pstats"))
    st = pstats.Stats(prof)
    st.sort_stats("cumulative").print_stats(r"(generation_breeze|breeze|modeling_qwen3|t5gemma|fastcpu|tokenizer|"
                                            r"generation/utils|torch/nn/modules/module)", 45)
    st.sort_stats("tottime").print_stats(30)


def cmd_design(args) -> None:
    """Candidate reference recordings for the narrator: one guided batch, each row its own sample."""
    tts = Breeze(args.threads, depth=args.depth)
    t0 = time.time()
    audio = tts.say_batch([REFERENCE_TEXT] * args.n, instruction=NARRATOR_V2, cfg_scale=args.cfg, seed=args.seed)
    for i, a in enumerate(audio):
        out = BUILD / "design" / f"candidate_{i}.wav"
        out.parent.mkdir(parents=True, exist_ok=True)
        sf.write(out, a, tts.rate, subtype="PCM_16")
        print(f"{out.name}: {len(a) / tts.rate:.2f} s, {len(REFERENCE_TEXT.split()) / (len(a) / tts.rate):.2f} words/s")
    print(f"{time.time() - t0:.0f} s for {args.n} candidates")


REFERENCE = VOICE_DIR / "reference.wav"


def reference_text() -> str:
    return (VOICE_DIR / "reference.txt").read_text(encoding="utf-8").strip()


def cmd_lines(args) -> None:
    """Synthesise the lines of a text file in the narrator's voice (one batch per --batch lines) into --out."""
    lines = [l.strip() for l in Path(args.file).read_text(encoding="utf-8").splitlines() if l.strip()]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tts = Breeze(args.threads, depth=args.depth)
    t0 = time.time()
    for start in range(0, len(lines), args.batch):
        chunk = lines[start:start + args.batch]
        audio = tts.say_batch(chunk, ref_audio=REFERENCE, ref_text=reference_text(), cfg_scale=args.cfg, seed=args.seed)
        for i, a in enumerate(audio, start):
            sf.write(out / f"line_{i:03d}.wav", a, tts.rate, subtype="PCM_16")
    print(f"{len(lines)} lines in {time.time() - t0:.0f} s -> {out}")


def _record_ok(meta: Path, wav: Path, text: str, speaker: str) -> bool:
    from lexicon import spoken

    if not (meta.exists() and wav.exists()):
        return False
    record = json.loads(meta.read_text(encoding="utf-8"))
    return record.get("text") == text and record.get("speaker") == speaker and record.get("spoken") == spoken(text)


def cmd_batch(args) -> None:
    """Synthesise every collected narration line (requests.jsonl) that the store lacks, shortest first, in batches;
    each batch is written as soon as it is done, so an interrupted run resumes where it stopped."""
    import hashlib

    from lexicon import spoken

    requests = [json.loads(l) for l in REQUESTS.read_text(encoding="utf-8").splitlines() if l.strip()]
    todo = [r for r in requests if not _record_ok(STORE / f"{r['key']}.json", STORE / f"{r['key']}.wav",
                                                  r["text"], r["speaker"])]
    todo.sort(key=lambda r: len(spoken(r["text"])))
    if args.limit:
        todo = todo[:args.limit]
    print(f"{len(requests)} requests, {len(todo)} to synthesise", flush=True)
    if not todo:
        return
    STORE.mkdir(parents=True, exist_ok=True)
    ref_sha = hashlib.sha256(REFERENCE.read_bytes()).hexdigest()[:16]
    tts = Breeze(args.threads, depth=args.depth)
    t_all, audio_all = time.time(), 0.0
    for n, start in enumerate(range(0, len(todo), args.batch)):
        chunk = todo[start:start + args.batch]
        seed = args.seed + start
        t0 = time.time()
        audio = tts.say_batch([spoken(r["text"]) for r in chunk], ref_audio=REFERENCE, ref_text=reference_text(),
                              cfg_scale=args.cfg, seed=seed)
        for r, a in zip(chunk, audio):
            sf.write(STORE / f"{r['key']}.wav", a, tts.rate, subtype="PCM_16")
            record = {"key": r["key"], "speaker": r["speaker"], "text": r["text"], "spoken": spoken(r["text"]),
                      "seconds": round(len(a) / tts.rate, 3), "seed": seed, "cfg": args.cfg,
                      "reference": ref_sha, "words": []}
            (STORE / f"{r['key']}.json").write_text(json.dumps(record, ensure_ascii=False, indent=1) + "\n",
                                                   encoding="utf-8")
        secs = sum(len(a) for a in audio) / tts.rate
        audio_all += secs
        print(f"batch {n}: {len(chunk)} lines, {secs:.0f} s audio in {time.time() - t0:.0f} s "
              f"(rtf {(time.time() - t0) / secs:.2f}); done {start + len(chunk)}/{len(todo)}, "
              f"{audio_all / 60:.1f} min audio in {(time.time() - t_all) / 60:.1f} min", flush=True)


def cmd_selftest(args) -> None:
    """The cached, stacked depth loop against the original uncached cond/uncond passes, teacher-forced on the
    cached loop's own output: per-step guided logits must agree to rounding."""
    from fastcpu import depth_cfg_cached

    tts = Breeze(args.threads)
    model = tts.model
    torch.manual_seed(0)
    b, h = 3, model.config.hidden_size
    dtype = next(model.depth_decoder.parameters()).dtype
    cond = torch.randn(b, h, dtype=dtype) * 2
    uncond = torch.randn(b, h, dtype=dtype) * 2
    ids = torch.stack([torch.zeros(b, dtype=torch.long), torch.randint(0, 2048, (b,))], dim=1)
    trace: list = []
    with torch.inference_mode():
        seq = depth_cfg_cached(model, ids, cond, uncond, args.cfg, trace=trace)
        worst = 0.0
        for step, guided in enumerate(trace):
            prefix = seq[:, :step + 2]
            c = model.depth_decoder(input_ids=prefix, backbone_last_hidden_state=cond, use_cache=False,
                                    return_dict=True).logits[:, -1, :].float()
            u = model.depth_decoder(input_ids=prefix, backbone_last_hidden_state=uncond, use_cache=False,
                                    return_dict=True).logits[:, -1, :].float()
            ref = u + args.cfg * (c - u)
            model._mask_reserved_codec_logits(ref)
            fin = torch.isfinite(ref)
            assert torch.equal(fin, torch.isfinite(guided)), f"step {step}: masks differ"
            err = ((guided - ref)[fin].abs().max() / ref[fin].abs().max()).item()
            worst = max(worst, err)
            print(f"step {step:2d}: max |cached - uncached| / max |logit| = {err:.2e}")
    print(f"sequence shape {tuple(seq.shape)}; worst relative logit difference {worst:.2e}")
    assert seq.shape == (b, model.config.num_codebooks + 1)
    assert worst < 2e-2, "cached depth loop disagrees with the original"
    print("SELFTEST PASS")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["smoke", "selftest", "bench", "profile", "design", "lines", "batch"])
    p.add_argument("--threads", type=int, default=8)
    p.add_argument("--cfg", type=float, default=4.0)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--sizes", default="1,4,8")
    p.add_argument("--depth", choices=["bf16", "int8"], default="bf16")
    p.add_argument("--n", type=int, default=6)
    p.add_argument("--file")
    p.add_argument("--out")
    p.add_argument("--batch", type=int, default=24)
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args()
    {"smoke": cmd_smoke, "selftest": cmd_selftest, "bench": cmd_bench, "profile": cmd_profile, "design": cmd_design, "lines": cmd_lines, "batch": cmd_batch}[args.cmd](args)


if __name__ == "__main__":
    main()
