# CH5103 explainer video

A complete narrated video of the term paper on Gryn'ova, Coote & Corminboeuf, "Theory and practice of uncommon
molecular electronic configurations", *WIREs Comput. Mol. Sci.* 5, 440 (2015).

* **What it covers.** All 136 frames of the slide deck as animated scenes, in 18 parts, every derivation step shown
  and spoken; then Appendix A walks through every verification script (T1–T16) and its recorded output, and Appendix B
  reads all 17 Lean theorems line by line, tactic by tactic.
* **Format.** {LENGTH}, 1920×1080 at 30 fps, H.264 + AAC; English captions (`.srt`); a chapter list.
* **Sound.** Narration by a synthetic voice made with Breeze-TTS-2 (one designed voice, cloned for all {LINES}
  lines), synthesised on a laptop CPU, over an original ambient score generated in code and ducked whenever the
  narrator speaks ({MUSIC}). No sound effects.
* **Checks.** Slide coverage 136/136; every narration line transcribed back by Whisper; word-level alignment for the
  animation cues; the final file was checked for its exact frame count, audio/video sync (cross-correlation of each
  sampled scene's narration against the soundtrack: worst lag {LAG}), picture placement and loudness
  ({LOUDNESS}). See `qa.txt`.

Assets: `ch5103-explainer.mp4`, `ch5103-explainer.srt`, `ch5103-explainer.chapters.txt`, `qa.txt`, `music-check.txt`
(how far the music sits under the voice, and Whisper with and without it). The narration-only cut is release
`video-v1.0`.

Everything needed to rebuild the video is in [`video/`](https://github.com/Shuvam-Banerji-Seal/CH5103_Term_Paper/tree/main/video).
The narration was generated with Breeze-TTS-2, whose licence permits research and non-commercial use.
