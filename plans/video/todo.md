# Master TODO (cycle 1)

## Research / validation
- [x] R1 Breeze-TTS-2 model + code + licence (research.md R1)
- [x] R2 ManimGX docs: maths (Typst), voice/say, render/inspect (research.md R2)
- [x] R3 pdoom-video-sbs engine + render pipeline (research.md R3)
- [x] R4 slide inventory (video/tools/inventory.py → 136 frames)
- [ ] R5 derivations/ vs slides: list derivation content missing from the slides
- [x] R6 verification code + Lean inventory: every script and all 17 theorems read line by line (chapters 18, 19)
- [x] D2 TTS on this laptop: CPU only; RTF 8.5 single line → 1.5–1.9 effective in batches of 24 (int8 backbone + text encoder, bf16 depth decoder, cached prompt audio, stacked/cached CFG depth loop); peak RSS 6–6.5 GB (research.md R5)
- [x] D3 MathTex compatibility — 1498/1499 typeset (sole failure is a TikZ variable, not maths); texmacros 8/8 tests
- [x] D4 Speech API resolved (doubts D4); pilot scene runs with say() spans (inspect timeline shows synced plays)
- [ ] D5 compositor (re-planned, working-memory V-R1): editor renders cards + HUD; assemble.ts overlays per segment and checks every segment's frame count; test: frame count of output == programme, audio/video durations equal within one frame, overlay-free pixels unchanged (to verify on the real render)
- [x] D6 12.5 frames/s → 120 s per request max
- [x] D7 ~200 fps at 1080p (GPU); --crf 0 for intermediates
- [x] D8 pronunciation: Whisper round trip on 24 probe sentences → lexicon (video/tts/lexicon.py); every synthesised line gets the same check (asr.py)

## Production
- [x] P1 narration for all 136 frames + appendices A (every test) and B (every Lean theorem): 164 scenes, 786 lines, 24.3k words; video/tools/coverage.py: 136/136
- [ ] P2 TTS synthesis of every line (cached), durations + word alignment — in progress (batch 3 running; align.py + asr.py after)
- [x] P3 ManimGX scenes for every chapter; inspect clean after fixes (box-style Plot, code excerpts read from the repo, table_rows reveal)
- [ ] P4 render every section at 1080p
- [ ] P5 JS compositor timeline + editorial layer; final render with narration
- [ ] P6 QA: coverage, maths audit, A/V sync audit, visual spot checks, audio QA, file checks
- [ ] P7 commit + push all code (no AI trailer); docs (video/README.md, main README)
- [ ] P8 gh release with the final 1080p MP4 (+ .srt captions)
