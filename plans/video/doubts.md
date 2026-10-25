# Doubts (each needs a Resolution)

| ID | time | doubt | how it will be resolved | Resolution |
|---|---|---|---|---|
| D1 | 2026-10-25 | Does BreezeBlue/Breeze-TTS-2 exist and how is it run? | HF API + model card + code | **RESOLVED**: exists; code at breezeblue-ai/breeze-tts; CPU fallback in code (research R1) |
| D2 | 2026-10-25 | User: "you can run the tts on this laptop efficiently" — no NVIDIA GPU; card says CUDA GPU required. CPU or ROCm iGPU fast enough? RAM 14 GiB vs ~7.7 GiB model | download weights, run a timed test on CPU (bf16), measure real-time factor and peak RSS; try ROCm torch on gfx1103 if CPU is too slow | open |
| D3 | 2026-10-25 | Which LaTeX commands in the slides does ManimGX's MathTex (Typst) accept? | extract every formula from presentation/sections, expand macros, test-render each with manimgx; list failures | **RESOLVED**: MathTex uses mitex (LaTeX→Typst). Sweep (video/tools/mathtex_sweep.py) over 1499 pieces: first run 32 failures, all from our side (unexpanded \\stepno; expander glued \\rangle to a following letter; overlay stripping created `{{`, which ManimGX reads as a part marker). After fixing texmacros.py: 1498/1499 typeset; the remaining one is a TikZ loop variable (\\ms), not maths [VERIFIED: sweep run] |
| D4 | 2026-10-25 | How does a custom ManimGX voice return word timings (`m.Speech` fields) for `say` bracket sync? | introspect the installed package (signature, docstring, source) | **RESOLVED** (docs reference 'Voice', source quoted): `Voice = Callable[[str], Speech]`; `m.Speech(source, *, text, words=(), rate=None)`, source = path/bytes/samples; `words` = `m.Word(text,start,end)`, built by `m.timed(text, pieces)` from timed pieces that spell the text's letters; without words they are estimated from loudness. `Scene.speech` → `cached(voice, text, voice/)`: key = digest(identity(voice), text); stores audio + words JSON. say(): each animation starts at its span's first word, run_time = max(own, span length) [VERIFIED: llms-full.txt 'Voice' page, src quoted] |
| D5 | 2026-10-25 | How to integrate ManimGX clips with the JS (pdoom) engine frame-exactly? | read app/scripts/render.ts + engine; prototype | open |
| D6 | 2026-10-25 | Codec frame rate of the Breeze audio tokenizer (frames/s) → max seconds per request (1500 tokens) | read audio_tokenizer/config.json | **RESOLVED**: encoder `_frame_rate` 12.5, 24 kHz, downsample 1920 (24000/1920 = 12.5 frames/s), 16 codebooks/frame → 1500 frames = 120 s max per request [VERIFIED: config.json]. Lines kept ≤ ~40 s |
| D7 | 2026-10-25 | Does ManimGX render on this iGPU (Vulkan RADV) and how fast at 1080p? | timed render of a test scene | **RESOLVED**: 10 s 1080p clip in 2.9 s at 30 and at 60 fps (bench.py) [VERIFIED: run] |
| D8 | 2026-10-25 | TTS pronunciation of technical terms (Hund, aufbau, Janak, Koopmans, Ovchinnikov, ROHF, NBMO, ⟨S²⟩ …) | listen-test via ASR round trip (transcribe the TTS output and compare) | open |

## Resolved 2026-10-25
- D2 (TTS speed on CPU): resolved — RTF ~1.5–2 effective with batching (research.md R5); ~4–5 h for all narration.
- D5 (compositor): resolved by V-R1 — editorial layer from the JS editor, frame-exact overlay per segment in ffmpeg.
- D8 (pronunciation): resolved — lexicon from a Whisper round trip; asr.py checks every line (WER ≤ 0.12, else listen/regenerate).
