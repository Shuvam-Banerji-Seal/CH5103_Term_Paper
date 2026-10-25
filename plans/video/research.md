# Research archive (append-only)

## R1 Breeze-TTS-2 (cycle 1, 2026-10-25)
- HF API (huggingface.co/api/models/BreezeBlue/Breeze-TTS-2): exists, created 2026-08-25, sha 3e28c51…, 3.47 B params
  (BF16), ~7.7 GB, library transformers, arch BreezeForConditionalGeneration, languages en/zh. [VERIFIED: HF API]
- License: code Apache-2.0; weights and *self-hosted outputs* under "BreezeBlue Research and Non-Commercial License"
  (LICENSE in the repo). A course explainer published on GitHub is non-commercial use. [VERIFIED: model card]
- Inference code: github.com/breezeblue-ai/breeze-tts (commit 6eba901). requirements: torch==2.9.1, torchaudio==2.9.1,
  qwen-tts==0.1.1, transformers==4.57.3, soundfile, numpy>=2. [VERIFIED: requirements.txt]
- Model card requirements: Linux, Python ≥3.10, CUDA NVIDIA GPU, ~7.7 GiB GPU memory eager. [VERIFIED: README]
- Code: `resolve_device()` returns "cuda:N" if torch.cuda.is_available() else "cpu"; model loaded in bfloat16 with
  attn_implementation="eager"; fast paths (CUDA graphs) are opt-in, default eager. So CPU (and ROCm/HIP, which
  reports as cuda) are possible without code changes. [VERIFIED: breeze_infer/runtime.py, infer.py]
- Limits per request: MAX_NEW_TOKENS=1500, MAX_SEQ_LEN=2048 → narration must be chunked (frames/sec of the codec
  to be checked). Sampling: temperature 0.9, top_k 50, repetition penalty 1.1, seed settable. [VERIFIED: infer.py]
- Modes: voice design (text instruction, cfg 4), voice clone (ref audio + exact transcript), voice direction (both).
  Output mono 24 kHz PCM16. Vocal events "(laugh)" etc. — avoid accidental parentheses in narration text!
  [VERIFIED: README] → script text must not contain parentheses unless an event is wanted [DERIVED].

## R2 ManimGX (cycle 1)
- PyPI manimgx 0.1.1, requires Python ≥3.13; deps numpy, pillow, skia-pathops, svgelements, typer, fonts. Rust GPU
  core (Vulkan on Linux; falls back to Mesa lavapipe CPU). [VERIFIED: PyPI JSON, llms.txt]
- Maths is typeset with **Typst**, not LaTeX: `MathTex` accepts a LaTeX-math subset (fractions, roots, sums,
  integrals, matrices, cases, Greek, \mathbb, \text); **no LaTeX packages, no \def**; unknown commands raise an error
  naming the command. `m.MathTypst` takes Typst math directly. [VERIFIED: user-guide/text-and-math]
  → the slides' macros (noir-macros.sty: \eri, \Hop, \OSS, \pa, \pb, \ket, \bra, \braket, \mel, \ev, \Eh, \hl, \canc…)
  must be expanded to supported commands, and every formula must be test-rendered.
- Narration: `self.say("text with [bracketed spans]", anim1, anim2)`; each animation starts at its span's first
  word; scene waits for the line to end. Voice = any function text → `m.Speech`. Audio cached in `voice/` next to the
  scene file; own recordings can replace a line's file (same name). Captions (.srt) written automatically.
  `m.Sound(path)`, `self.add_sound`, `.gain()`, `.fade_in()`. [VERIFIED: user-guide/sound-and-voice]
- Render: `manimgx render file.py Scene -r WxH --fps N -o out.mp4`; default 1920×1080@60; encodes video+audio to MP4
  itself. `inspect` = storyboard + timeline + 2D layout checks (overlap, clipping, tiny text), exit 1 on problems.
  [VERIFIED: user-guide/rendering]

## R3 pdoom-video-sbs (cycle 1)
- The user's repo (MIT): a code-rendered music video. TypeScript + three.js app (bun + Vite), engine ~2.5k lines:
  deterministic frame = f(t); timeline entries (scene windows) anchored to word timings; post-processing (bloom,
  grain…); typography (Archivo, IBM Plex Mono, Cormorant Garamond, stroke fonts); offline render = headless Chrome
  (playwright-core) → raw frames over WebSocket → ffmpeg (x264 CRF 16, AAC); stills/contact-sheet modes.
  [VERIFIED: README.md, docs/ENGINE.md]
- analysis/: Python (uv) forced alignment (CTC + Whisper cross-check) producing word-level timings JSON.
  [VERIFIED: README] → reusable to get word timings of the TTS narration.
- Engine supports image textures (THREE.TextureLoader); no video layer yet. [VERIFIED: grep]
- Local toolchain: bun, node, chromium (no google-chrome), ffmpeg with libx264/libx265/prores/vp9/svt-av1. [VERIFIED]

## R0 Hardware (cycle 1)
- AMD Ryzen 7 250 (Zen 4, 8C/16T), Radeon 780M iGPU (gfx1103, ROCm in /opt/rocm), 14 GiB RAM (2.2 GiB available at
  check time; browser tabs hold ~4 GiB), no NVIDIA GPU, 132 GB free disk. [VERIFIED: lscpu, free, rocminfo, df]

## R5 — CPU synthesis measurements (2026-10-25, Ryzen 7 250, 8C/16T, 15 GB, other jobs running)
- bf16 model mmap'd: page-cache eviction (RssFile 3.5 of 7.6 GB) → 5 min for a 12 s line; private copies → OOM kill.
- int8 weight-only `_weight_int8pack_mm`: 2–7× faster than bf16 at 1–8 rows, but linear in rows beyond 8 (it is a GEMV kernel); bf16 GEMM is flat up to ~32 rows (≈900 µs for 1024→8192), so batches use a bf16 depth decoder.
- Prefill through int8pack was the batch bottleneck (4.5 s → 16.9 s from 1 to 8 rows): Int8Linear dequantises to a bf16 GEMM for ≥64 rows.
- Codec: encode of an 18 s reference 0.8 s; decode RTF 0.3–0.37.
- Threads: one TTS process at 16 threads RTF 3.38 vs 1.69 at 8 (matmul 3200 vs 907 µs) — bandwidth-bound and preempted by other jobs.
- Effective RTF: 8.9 (1 line) → 2.65 (8, int8) → 2.03 (8, prefill fix) → 1.69 (24, bf16 depth) → 1.45–2.1 in production batches.
- Depth-decoder CFG loop: original reruns the whole prefix twice per codebook (30 uncached passes per frame); stacked + KV-cached version gives bit-identical guided logits (synth.py selftest: max difference 0.0).
- Voice design rounds: "steady, unhurried" 1.9 w/s; "moderately brisk" 3.5–3.8; "calm, measured" 1.85–2.27; "natural conversational" 2.46–3.10 → candidate 5 (2.74 w/s, WER 0) is the reference (video/tts/voice/).
- Whisper small.en round trip on 24 probes: mispronounced → lexicon: wavefunction, antisymmetric, zwitterionic, aufbau, xylylene, cyclobutadiene, Laplacian, psi, chi, Mathlib, SymPy, Mott.
- Lean re-check for the video: #print axioms of all 17 theorems → only propext, Classical.choice, Quot.sound (sum_is_triplet, diff_is_singlet: propext, Quot.sound only); evidence/lean_axioms_2026-10-25.txt.
