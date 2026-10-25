# Master TODO (cycle 1)

## Research / validation
- [x] R1 Breeze-TTS-2 model + code + licence (research.md R1)
- [x] R2 ManimGX docs: maths (Typst), voice/say, render/inspect (research.md R2)
- [x] R3 pdoom-video-sbs engine + render pipeline (research.md R3)
- [x] R4 slide inventory (video/tools/inventory.py → 136 frames)
- [x] R5 derivations/ vs slides: every derivation subsection maps to a scene except §17's sources-and-access table (added as Appendix A's last scene) and §7's remark that the Hubbard model cannot be held to the virial theorem (added as a spoken note at the end of S66TwoViews)
- [x] R6 verification code + Lean inventory: every script and all 17 theorems read line by line (chapters 18, 19)
- [x] D2 TTS on this laptop: CPU only; RTF 8.5 single line → 1.5–1.9 effective in batches of 24 (int8 backbone + text encoder, bf16 depth decoder, cached prompt audio, stacked/cached CFG depth loop); peak RSS 6–6.5 GB (research.md R5)
- [x] D3 MathTex compatibility — 1498/1499 typeset (sole failure is a TikZ variable, not maths); texmacros 8/8 tests
- [x] D4 Speech API resolved (doubts D4); pilot scene runs with say() spans (inspect timeline shows synced plays)
- [x] D5 compositor (re-planned, working-memory V-R1): editor renders cards + HUD; assemble.ts overlays per segment and checks every segment's frame count; test: frame count of output == programme, audio/video durations equal within one frame, overlay-free pixels unchanged (to verify on the real render)
- [x] D6 12.5 frames/s → 120 s per request max
- [x] D7 ~200 fps at 1080p (GPU); --crf 0 for intermediates
- [x] D8 pronunciation: Whisper round trip on 24 probe sentences → lexicon (video/tts/lexicon.py); every synthesised line gets the same check (asr.py)

## Production
- [x] P1 narration for all 136 frames + appendices A (every test) and B (every Lean theorem): 164 scenes, 786 lines, 24.3k words; video/tools/coverage.py: 136/136
- [x] P2 TTS synthesis of every line (cached), durations + word alignment: 791 lines, 174.4 min; 123 newest aligned with 0 failures; Whisper round trip (sentence-by-sentence re-hearing of cut-short transcripts), 4 lines re-synthesised, 2 kept after round 2 (Whisper cannot spell xylylene)
- [x] P3 ManimGX scenes for every chapter; inspect clean after fixes (box-style Plot, code excerpts read from the repo, table_rows reveal)
- [x] P4 render every section at 1080p: 165 scenes (renders are VFR: frames = duration x 30)
- [x] P5 JS compositor timeline + editorial layer; final render with narration: 322637 frames, 2:59:14.6, 0.97 GiB, x264 slow CRF 12
- [x] P6 QA: coverage, maths audit, A/V sync audit, visual spot checks, audio QA, file checks (qa.py all ok; tests video-12..16)
- [x] P7 commit + push all code (no AI trailer); docs (video/README.md, main README)
- [x] P8 gh release video-v1.0 with the final 1080p MP4, .srt captions, chapter list, qa.txt
- [ ] P9 4K version (local only): render4k, probe4k, editor4k, assemble4k (HEVC VAAPI QP 20), qa4k
- [x] AUD1 slide 08-hund frame 7 subtitle says "within 10^-4 Eh of exact": the singlet is 1.1e-4 off (T4 output; derivations sec05 already says 1.7e-5 and 1.1e-4). Fixed; both PDFs rebuilt (log clean: no warnings or bad boxes).
- [x] AUD2 slide 17-bs frame 1 said "(Part III)" for "a single determinant cannot be the open-shell singlet"; the deck's Part III is Spin & antisymmetry, the result is in Part IV (Two electrons, two orbitals). Slide and video fixed; rebuild PDFs with AUD1.
