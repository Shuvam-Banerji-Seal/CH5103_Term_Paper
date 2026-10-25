# The explainer video

A narrated video of the whole term paper: every one of the 136 slide frames as an animated scene, every derivation
step shown and spoken, and two appendices that walk through every verification script (T1–T16) and every Lean
theorem (17), line by line. Narration is synthesised with [Breeze-TTS-2](https://huggingface.co/BreezeBlue/Breeze-TTS-2);
animation with [ManimGX](https://pypi.org/project/manimgx/); editing with a JavaScript editor adapted from
[pdoom-video-sbs](https://github.com/Shuvam-Banerji-Seal/pdoom-video-sbs). Under the narration runs an original
ambient score, generated in code (`tools/bgm.py`: additive synthesis, no samples or recordings) and ducked whenever
the narrator speaks; there are no sound effects.

The finished video (1080p, 30 fps, with captions) is attached to the GitHub release.

## Layout

| path | what |
|---|---|
| `scenes/` | ManimGX scenes, one file per chapter (`ch00_intro.py` … `ch19_lean.py`), one class per slide frame (165 scenes); `noir.py` is the slides' theme (palette, fonts, boxes, derivations, plots, code excerpts); `voice.py` serves the synthesised narration to ManimGX; `texmacros.py` expands the slide macros; `fonts/` are the slide fonts (OFL / GUST licences inside) |
| `tts/` | Breeze-TTS-2 on the CPU: `synth.py` (batch synthesis, voice design, benchmarks, self-test), `fastcpu.py` (int8 linears, cached CFG depth loop), `lexicon.py` (pronunciation respellings), `align.py` (word timings by CTC forced alignment), `asr.py` (Whisper round-trip check), `voice/` (the narrator's reference recording), `breeze/` (vendored model code, its licence) |
| `editor/` | the editorial layer: chapter title cards and the progress HUD (`src/engine.ts`, a deterministic function of the programme position), rendered in headless Chromium (`scripts/render.ts`) and assembled with ffmpeg (`scripts/assemble.ts`) |
| `tools/` | `bgm.py` (the background score: compose, mix under the voice, check), `inventory.py` (parse the deck), `coverage.py` (every frame has its scene), `collect_lines.py` (every narration line, linted), `program.py` (chapters, scenes, exact frame counts), `inspect_all.py` (layout checks and storyboards), `mathtex_sweep.py` |
| `build/` | everything generated (git-ignored) |

## Rebuilding

Three environments, each locked with `uv` (or `bun`): `video/scenes` (Python 3.14, ManimGX), `video/tts`
(Python 3.12, PyTorch CPU), `video/editor` (Bun, Vite, Playwright with the system Chromium).

```sh
# 0. the model (7.7 GB) and the forced-alignment / ASR models (downloaded on first use)
uv run --project video/tts hf download BreezeBlue/Breeze-TTS-2 --local-dir video/tts/checkpoints/breeze-tts-2
uv run --project video/tts hf download openai/whisper-small.en --local-dir video/tts/checkpoints/whisper-small.en

# 1. narration: collect every line, synthesise (resumable), check, align
uv run --project video/scenes python -I video/tools/collect_lines.py --write
OMP_NUM_THREADS=8 uv run --project video/tts python -E -s video/tts/synth.py batch --threads 8 --cfg 1 --batch 24
uv run --project video/tts python -E -s video/tts/asr.py
uv run --project video/tts python -E -s video/tts/align.py

# 2. scenes: layout checks, then the final renders with the narration
cd video/scenes
uv run --project . python -I ../tools/inspect_all.py ch03_two_electrons.py --end      # storyboards in video/build/inspect
VIDEO_VOICE=final uv run --project . manimgx render ch03_two_electrons.py S23Sum -r 1920x1080 --fps 30 -o ../build/scenes/ch03_two_electrons/S23Sum.mp4
cd ../..
python3 video/tools/program.py --probe                                              # exact frame counts -> program.json

# 3. editing and assembly
cd video/editor && bun install
bun scripts/render.ts cards && bun scripts/render.ts hud
bun scripts/assemble.ts                                                              # -> video/build/final/
```

`python3 video/tools/coverage.py` must report 136/136; `collect_lines.py` must report no lint problems.

All of this runs unattended with `python3 video/tools/pipeline.py [--from STAGE]` (stages wait, tts, align, asr, render,
probe, editor, start4k, assemble, qa, then the 4K ones): every stage is resumable, logs go to `video/build/logs/`, and
`pipeline.status` has one line per event. What was measured on the build laptop (Ryzen 7 with a Radeon 780M, 15 GB):

* **Scenes render one at a time.** ManimGX rasterises on the GPU (Vulkan) and one render already keeps the GPU 65–85 %
  busy and about six CPU threads working: three renders at once took as long as three in a row. 1080p runs at about
  seven times real time.
* **Renders are variable frame rate.** A still stretch is stored as one long frame, so a scene's length is its stream
  duration (frames on screen = duration × 30, which `program.py --probe` records) and the assembler expands every scene
  to constant 30 fps before overlaying the HUD.
* **The final encode** is x264 `slow`, CRF 12, `-tune animation`: the slides are mostly still, so this costs about
  270 kb/s, and x264 runs at the same speed as at CRF 22. Three segments encode at once (each ffmpeg peaks at about
  1.7 GB); the joined file is checked frame by frame count, for sync and for loudness (`tools/qa.py`).

## How the narration is made

* **One voice.** The narrator's voice was designed once from a text description (18 candidates in three rounds, chosen
  by a perfect Whisper transcript and a speaking rate of 2.7 words per second) and every line is then synthesised in
  voice-clone mode from that recording, so the timbre never changes.
* **On a laptop CPU.** The 3.5-billion-parameter model runs in PyTorch on the CPU: int8 weights for the backbone and the
  text encoder, a bfloat16 depth decoder, 24 lines per batch, and a rewritten classifier-free-guidance loop whose logits
  are bit-identical to the original's (`synth.py selftest`). About 1.5–2 seconds of compute per second of speech.
* **Written for the ear.** Lines spell out numbers and symbols ("S squared", "two K a b"); a lexicon fixes words the model
  mispronounced in a Whisper round trip (for example *wavefunction*, *aufbau*, *xylylene*); every line is transcribed by
  Whisper and compared with its text. Whisper hears 30 s at a time and tends to stop at the pause after a colon, so a
  line whose transcript comes back cut short is heard again sentence by sentence (cut at its aligned word times); a
  line still over 50 % word error is synthesised again with another seed, for at most two rounds.
* **In sync.** Each line's words are timed by CTC forced alignment, and ManimGX starts each animation on the word in
  square brackets of the `say()` text. In the final assembly a frame is exactly 1600 audio samples, so the narration
  cannot drift from the picture.

## The background music

`tools/bgm.py compose` writes an original score as long as the programme: one chord every 8 s, all in D major /
B minor (so chapters cannot clash where their notes overlap), each chapter opening a fresh phrase on its title card
with its own pair of progressions and its own sparse felt-piano line; warm pads (four soft partials, slow swells, each
voice panned to its own place), a centred sine bass and a synthetic hall reverb (the only decorrelated part, so the
music survives a mono phone speaker). `bgm.py mix` sets the score to -26 LUFS, ducks it with
a sidechain compressor keyed on the narration (about 11 dB down while someone speaks, back up in pauses and on the
cards), adds it to the voice, normalises to -16 LUFS and muxes it with the video stream copied. `bgm.py check`
measures how far the music sits under the voice and transcribes the same excerpts with and without it.

## Credits and licences

* Breeze-TTS-2 by BreezeBlue — model weights and code under their licence (`tts/breeze/LICENSE`; research and
  non-commercial use). The narration in this video was generated with it.
* ManimGX (pinned to 0.1.1 in `scenes/uv.lock`).
* The editor's renderer is adapted from pdoom-video-sbs (MIT).
* Fonts: TeX Gyre Chorus (GUST licence), Libertinus, EB Garamond, JetBrains Mono (SIL OFL).
* Figures from the reviewed paper (Gryn'ova, Coote & Corminboeuf, *WIREs Comput. Mol. Sci.* **5**, 440, 2015) are
  shown for commentary, as on the slides.
