# Rigor task index: explainer video

**Task (user, 2026-10-25, verbatim intent):** make a complete explainer video of the CH5103 term paper.
- Voice: TTS with https://huggingface.co/BreezeBlue/Breeze-TTS-2.
- Visuals: ManimGX ("manim-gx api") scripts, reusing the LaTeX from the slides (presentation/sections).
- Editing / assembly: the user's JS editor git@github.com:Shuvam-Banerji-Seal/pdoom-video-sbs.git.
- "Do not worry about length but be sure to make it complete without missing any details. Be rigorous."
- Mid-task user note: "you can run the tts on this laptop efficiently" (to be validated; see doubts D2).
- **Goal set by the user (2026-10-25, verbatim):** "complete the whole video covering all slides, explaining everything
  and deriving every concept with every steps and maths and python and lean without missing anything, push all the code
  to the repo, do a gh release of the final complete video at 1080p. all sound must be generated using proper natural
  TTS with proper frame by frame integration and editing."
  -> acceptance: (a) every one of the 136 slide frames is covered; (b) every derivation step shown and narrated;
  (c) the Python checks and Lean proofs are explained too; (d) all audio = Breeze-TTS-2 narration; (e) audio/visual
  sync at frame level; (f) all code pushed; (g) GitHub release with the final 1080p MP4.

**Standing constraints (from earlier in the project):** no AI co-author trailers in commits; uv-based Python;
use all cores (OMP_NUM_THREADS=16); sub-agents use model haiku; GPU (Radeon 780M, gfx1103) was unusable for PySCF.

| field | value |
|---|---|
| Cycle | 1 |
| Phase | 1 RESEARCH |
| Open TODOs | see todo.md |
