# Plan (cycle 1, Phase 3: step-locked)

## Architecture (decisions V-D2..V-D6 in working-memory.md)
```
presentation/sections/*.tex ──► video/tools/inventory.py ──► build/inventory.json ──► coverage test
                                                                                         ▲
video/scenes/chNN_*.py  (ManimGX; one Scene per slide frame + verification chapter)      │
   noir.py      theme: palette, fonts (font_paths), title bar, boxes, pills, symbol strip,
                derivation rows (lhs | = rhs | why), figure helper, code helper
   texmacros.py slide macros → MathTex-safe LaTeX (tested)
   voice.py     BreezeVoice(text) → m.Speech(wav, words=timed(...)) from the TTS store;
                COLLECT mode records every line instead (for batch synthesis)
        │ collect lines (video/tools/collect_lines.py)                                    │
        ▼                                                                                  │
video/tts/ (uv, Python 3.12, torch 2.9.1 CPU, Breeze code vendored by commit)             │
   synth.py   batch: line text → (pronunciation lexicon) → Breeze voice-clone of one
              designed reference voice → build/tts/<key>.wav (24 kHz mono)                 │
   align.py   CTC forced alignment (torchaudio MMS_FA + Viterbi) → word times JSON         │
   qa.py      ASR round trip (pronunciation), loudness normalisation, clipping check       │
        │                                                                                  │
        ▼                                                                                  │
manimgx render (per scene, 1920×1080) ──► build/scenes/*.mp4 (+ .srt) ─────────────────────┘
        ▼
video/editor/ (bun + three.js engine adapted from pdoom-video-sbs, MIT)
   timeline.json  = scene order, durations (ffprobe), chapter boundaries, captions (word times)
   render.ts      ffmpeg decodes scene k frame-by-frame → page texture; engine adds chapter cards,
                  progress HUD, captions, transitions; frames → ffmpeg + master narration (concat
                  of the scenes' audio) → build/ch5103-explainer-1080p.mp4
```

## Steps (step N+1 blocked until N's test passes)
1. Tooling: ManimGX installed (scenes env); Breeze env installed; model downloaded. Test: `import manimgx`; Breeze imports.
2. D3 MathTex compatibility sweep over all slide maths (macros expanded). Test: list of failing commands → mapping table; 0 failures after mapping.
3. D7 ManimGX speed test (1080p, 60 & 30 fps). Decide fps (V-Q1).
4. D2 Breeze CPU smoke test: one 10–15 s line; RTF, peak RSS. If RTF > ~6, try ROCm torch. Test: wav exists, RTF logged.
5. Voice design → pick reference → voice-clone consistency test (3 lines, same timbre by ear + speaker-embedding cosine if available) [V-Q2].
6. Alignment: align.py on test lines; test: word count = text words, monotone times, within audio duration; ManimGX `timed()` accepts them.
7. noir.py components + one pilot scene (slide 05 "sign error" frame) with narration end-to-end: collect → synth → align → render. Test: inspect = no layout problems; video plays with synced audio; spot frames.
8. JS editor prototype with the pilot clip: frame-exact compositing. Test: frame k of output vs clip (PSNR in overlay-free area high), audio offset = 0.
9. Write all chapters (19 + verification): narration + scenes, chapter by chapter; coverage test after each chapter.
10. Batch TTS + alignment for all lines; QA (ASR round trip WER, loudness).
11. Render all scenes; inspect each (no layout problems), storyboard review.
12. Final edit render 1080p; QA: duration = sum, A/V sync checks at chapter boundaries, black-frame/silence detection, captions.
13. Docs, commit, push; gh release with the MP4 (+ .srt). Final report.
