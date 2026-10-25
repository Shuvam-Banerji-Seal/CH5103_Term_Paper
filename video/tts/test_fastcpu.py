"""Int8Linear against nn.Linear (no model needed): python -E -s -m pytest -q test_fastcpu.py"""
import torch
from torch import nn

from fastcpu import Int8Linear, quantize_linears


def test_int8_linear_close_to_bf16():
    torch.manual_seed(0)
    lin = nn.Linear(512, 768, bias=True).to(torch.bfloat16)
    q = Int8Linear(lin)
    x = torch.randn(4, 7, 512, dtype=torch.bfloat16)
    ref, got = lin(x).float(), q(x).float()
    assert got.shape == ref.shape
    assert ((got - ref).norm() / ref.norm()).item() < 0.02


def test_int8_weights_reconstruct_rows():
    torch.manual_seed(1)
    lin = nn.Linear(300, 260, bias=False)
    q = Int8Linear(lin)
    back = q.weight_int8.float() * q.scale.float()[:, None]
    row_err = (back - lin.weight).abs().amax(1) / lin.weight.abs().amax(1)
    assert row_err.max().item() < 0.01  # half a quantisation step is 1/254 of the row maximum, plus bf16 scale rounding


def test_quantize_linears_skips_small_layers():
    net = nn.Sequential(nn.Linear(512, 512), nn.ReLU(), nn.Linear(512, 8))
    assert quantize_linears(net) == 1
    assert isinstance(net[0], Int8Linear) and isinstance(net[2], nn.Linear)


def test_float32_input_keeps_dtype():
    lin = nn.Linear(256, 256)
    q = Int8Linear(lin)
    x = torch.randn(3, 256)
    y = q(x)
    assert y.dtype == torch.float32
    assert ((y - lin(x)).norm() / lin(x).norm()).item() < 0.02


def test_gemm_path_matches_int8pack_path():
    torch.manual_seed(2)
    q = Int8Linear(nn.Linear(256, 320, bias=True).to(torch.bfloat16))
    x = torch.randn(Int8Linear.GEMM_ROWS + 5, 256, dtype=torch.bfloat16)
    big = q(x).float()                                   # one call: dequantised GEMM
    small = torch.cat([q(x[i:i + 8]) for i in range(0, len(x), 8)]).float()  # int8pack in chunks of 8 rows
    assert ((big - small).norm() / small.norm()).item() < 1e-2
