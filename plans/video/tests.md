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
