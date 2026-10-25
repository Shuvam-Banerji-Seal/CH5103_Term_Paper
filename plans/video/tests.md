# Test log (explainer video)
| time | test | command | result | notes |
|---|---|---|---|---|
| c1 | texmacros unit tests (8) | uvx pytest video/scenes/test_texmacros.py | PASS | 3 tests added test-first after the D3 sweep; failed before the fix, pass after |
| c1 | D3 MathTex sweep | uv run --project video/scenes python -I video/tools/mathtex_sweep.py | PASS (1498/1499) | sole failure: TikZ variable \ms (not maths) |
| c1 | CTC aligner unit tests (5) | uvx --with numpy pytest video/tts/test_ctc.py | PASS | mutation test (illegal skip between repeated labels) SURVIVED the first suite → added test_repeat_forces_blank_even_when_unlikely; re-check: mutant FAILS (1 failed), real PASSES 6/6 |
| c1 | D7 ManimGX speed | manimgx render bench.py -r 1920x1080 --fps 30/60 | PASS | 10 s clip rendered in 2.9 s at both 30 and 60 fps (~200 fps, GPU); default x264 CRF 23 → use --crf 0 for intermediates |

| video-1 | texmacros: 8 | uvx pytest | PASS | |
| video-2 | ctc Viterbi: 6 (incl. a mutation test) | pytest | PASS | |
| video-3 | fastcpu Int8Linear: 5 (accuracy, row reconstruction, GEMM path = int8pack path) | pytest | PASS | |
| video-4 | depth CFG loop cached vs original: guided logits per step | synth.py selftest | PASS | max |Δ| / max |logit| = 0.0 |
| video-5 | ASR normalisation + WER: 2 | pytest | PASS | |
| video-6 | pronunciation lexicon: 4 | pytest | PASS | |
| video-7 | noir rich→Typst: 6 (escapes, emphasis, code spans) | pytest | PASS | |
| video-8 | slide coverage: 136 frames ↔ scenes | video/tools/coverage.py | PASS | 136/136, 0 missing/duplicated |
| video-9 | narration lint: digits, parentheses, LaTeX, non-Latin letters | video/tools/collect_lines.py | PASS | 786 lines, 0 problems |
| video-10 | every code excerpt range valid, indices in range (chapters 16, 18, 19) | inline check | PASS | 40 + 10 excerpts |
| video-11 | independent narration audit vs slides (two read-only reviewers, ch00–ch17), every finding re-checked | review + manual check | PASS after fixes | fixed: He basis accuracy (singlet 1.1e-4, slide also off → AUD1), "matches" SCS-MP2 → "compare", 2³S read as "two cubed S" (twice), spin-polarisation mechanism stated backwards (ch10), T3 "positive" → "never negative"; kept 3 consistent elaborations |
| video-12 | ASR spans: sentence cuts at aligned word times, pieces <= 24 s, contiguous | pytest video/tts/test_asr.py | PASS (3) | written with the sentence-by-sentence re-check |
| video-13 | scene renders VFR → CFR: S00Title 543 stored frames for 35.333 s → fps=30 gives exactly 1060; frames at 2.5/5/12/20/30/35.2 s match the source | ffmpeg + PSNR | PASS | 57–61 dB = the test encode's own loss; frame n shows time n/30 |
| video-14 | HUD as one repeated image (eof_action=repeat) vs looped image: frame count, HUD present on the last frames, peak memory | ffmpeg on S00Title | PASS | 1060 frames, HUD on frame 1000; 1.7 GB vs 3.6 GB |
| video-15 | x264 settings on two scenes: preset/CRF vs speed, size, SSIM to the render | bench.sh | PASS | speed independent of CRF; CRF 12 slow: ~270 kb/s, SSIM 0.99994 → chosen |
| video-16 | final 1080p file: format, size, frames, durations, sync (24 scenes), picture (PSNR below HUD), loudness, silences | video/tools/qa.py | PASS | all [ok]: 322637 = programme; lag 0.0 ms; worst PSNR 50.3 dB; −16.0 LUFS, TP −1.2 dBTP; no silence ≥ 8 s |
| video-17 | score: no clicks at the 30 s chunk joins; mono compatibility; spectrum | inline (soundfile, numpy) | PASS after a fix | first render: L/R correlation 0.008 (independent phases per channel, bass could cancel in mono) → voices made coherent and panned: correlation 0.55, mono downmix −1.2 dB; largest step at a join 0.017 < 99.9th pct nearby 0.025; no energy below 40 Hz, 0.01 % above 2 kHz |
| video-18 | music version: format, frames, sync, picture, loudness, silences | qa.py --final final-music/… | PASS | all [ok]; −16.0 LUFS, TP −1.3 dBTP; lag 0.0 ms |
| video-19 | music under the voice; Whisper with and without it | bgm.py check | PASS | voice over music median 25.2 dB (5th pct 13.0 dB); first version of the check cut 20 s windows through words (5.9 % vs 1.0 %: boundary artefacts); pause-to-pause excerpts: 1.7 % with music vs 1.4 % with −60 dB noise |
