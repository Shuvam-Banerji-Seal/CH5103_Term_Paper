# Working memory

## Decisions
| ID | decision | rationale | alternatives rejected |
|---|---|---|---|
| V-D1 | Rigor state for this task in plans/video/ (not overwriting plans/*) | plans/ already holds the finished term-paper log; rule: never delete from plans/ | reuse plans/*.md (would destroy the old log) |
| V-D2 | Code lives in video/ of this repo: video/script (narration), video/tts (Breeze uv project), video/scenes (ManimGX uv project, Python 3.14), video/editor (JS compositor adapted from pdoom-video-sbs), video/tools (inventory, coverage, checks), video/build (outputs, gitignored) | one repo, pushed with the rest; separate envs (torch 2.9 vs Python 3.14 manimgx) keep the main uv project light | putting torch into the main pyproject; editing the pdoom music-video repo in place |
| V-D3 | Frame-exact integration: the JS engine is the final compositor. render.ts decodes the ManimGX section videos with ffmpeg and streams frame k to the page before rendering t = k/fps; the engine draws it as a texture plus the editorial layer (chapter cards, progress HUD, word-synced captions, transitions) and streams the result to ffmpeg with the master narration track | every output frame is a deterministic function of t and of exactly one source frame: "frame by frame integration" | `<video>` seeking in headless Chrome (inexact); plain ffmpeg concat (no JS editing) |
| V-D4 | Video content = all 136 slide frames (coverage-tested) + an extended verification chapter: every test script (T1–T15, T1b, T11a–c, T16) and every Lean theorem (17) explained; plus any derivation in derivations/ that the slides skip | the goal says "maths and python and lean without missing anything"; the slides only excerpt T4, T11a, T17 | slides only |
| V-D5 | Sound = Breeze-TTS-2 narration only (no music/SFX) | goal: "all sound must be generated using proper natural TTS" | background music |
| V-D6 | Narration text must avoid parentheses (Breeze reads "(laugh)" etc. as vocal events) and is written for the ear (symbols spoken: "S squared", "K sub a b") | model card | raw slide text |

| V-D7 | Output 1080p at 30 fps (resolves V-Q1) | ~3.5 h of programme: a GitHub release asset must stay under 2 GB, and the final encode time halves | 60 fps |
| V-D8 | One narrator: a voice designed from a text prompt (3 rounds, 18 candidates, chosen by ASR WER = 0 and 2.7 words/s), then voice-clone mode (cfg 1) from that recording for every line (resolves V-Q2) | identical timbre for 786 lines; clone mode needs no CFG pass | voice design per line (timbre drifts) |
| V-D9 | CPU synthesis (video/tts/fastcpu.py): int8 weight-only backbone + text encoder (dequantised GEMM for prefill), bf16 depth decoder copied to private memory, depth CFG loop stacked + KV-cached (bit-identical logits, selftest), prompt audio encoded once, 24 lines per batch | measured: memory-bandwidth bound; 8 threads beat 16 (contention with the user's jobs) | 16 threads; int8 depth decoder at batch 24; one line at a time |
| V-D10 | Pronunciation lexicon applied to the spoken text only; captions and alignment keep the written words (pairs written→spoken) | Whisper round trip found mispronunciations (wavefunction, antisymmetric, aufbau, xylylene, …) | editing the narration text |
| V-D11 | Plots use noir.Plot: box axes on the bottom/left edges with numbered ticks (pgfplots style), log axes supported | ManimGX axes cross at zero, which put the x axis across negative-energy plots | ManimGX Axes |
| V-D12 | Code and recorded output shown in the video are read from the repository at render time (noir.excerpt), never retyped; ranges may not start/end on a blank line | what is shown is what was run | retyped snippets (chapter 3 had one; replaced) |

| V-D13 | A 4K version (3840x2160, HEVC via VAAPI, QP 20) is built after the 1080p one and kept local only; the GitHub release carries the 1080p file | the user asked for 4K "after the 1080p is done" and said "4k video is local only" | uploading 4K (2 GB asset limit) |

## Discoveries
| ID | discovery | impact | status |
|---|---|---|---|
| V-X1 | Breeze code runs eagerly on CPU when CUDA is absent | TTS possible here without code changes; speed unknown (D2) | open |
| V-X2 | ManimGX typesets with Typst; MathTex = LaTeX-math subset, no \def/packages | all slide macros must be expanded; every formula test-rendered (D3) | open |
| V-X3 | ManimGX voice = any function text → Speech; voice/ cache; .srt captions | Breeze can be the scene voice; bracket sync needs word timings (D4) | open |
| V-X4 | pdoom-video-sbs is a three.js music-video engine (deterministic f(t)), offline render via headless Chrome → ffmpeg; hard-wired to Chrome/macOS (channel 'chrome', angle metal) | must adapt to /usr/bin/chromium on Linux | open |
| V-X6 | Memory is the binding constraint: the laptop (15 GB) also runs the user's browser and experiment jobs; Breeze bf16 (7.7 GB) was OOM-killed; private copies of mmap'd weights also OOM | int8 parts + one heavy job at a time; user said swap is fine | handled |
| V-X7 | manimgx.timed lives in manimgx.audio (not the top level); m.Code keeps inner blank lines as empty entries but drops blank lines at the ends | fixed voice.py; excerpt() guards ranges | done |
| V-X8 | Typst markup clashes: leading +/-/= start lists; literal * (6-31G*) opens emphasis once **bold**/*italic* are supported | escapes; basis names use ∗ (U+2217) | done |
| V-X5 | Deck = 136 frames, 1382 maths blocks, 29 figures, 577 overlay steps (video/build/inventory.json) | sizing: ~1.5–2.5 h narration | done |

## Reversals
| ID | was | now | why |
|---|---|---|---|
| V-R1 | V-D3: every source frame streamed through the browser | the JS editor (pdoom-derived: f(t), headless Chromium, WebSocket → ffmpeg) renders the editorial layer — chapter cards and a per-scene HUD (progress bar with chapter ticks, part label); assemble.ts overlays it on each scene in one encode per segment, joins segments without re-encoding, and builds one narration track sample-exactly (1600 samples per frame at 48 kHz/30 fps) | a 16 MB round trip per frame for ~380k frames would take ~15 h; the per-segment overlay is still frame-exact (each output frame = one scene frame + one overlay frame) |

## Open questions
| ID | question | priority | status |
|---|---|---|---|
| V-Q1 | Output frame rate: 60 vs 30 | medium | resolved: 30 (V-D7) |
| V-Q2 | One voice: design once, then clone? | high | resolved: yes (V-D8) |
