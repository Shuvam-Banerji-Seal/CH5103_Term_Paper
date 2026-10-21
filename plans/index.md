# Rigor task index
Task: step-by-step derivations of all mathematics in Gryn'ova, Coote & Corminboeuf,
WIREs Comput Mol Sci 2015, 5:440 (doi 10.1002/wcms.1233); consult cited originals; verify
algebra symbolically/numerically; output compilable LaTeX in assets/derivations.tex.
Sub-agents: model haiku (user instruction).
Cycle: 1 | Phase: 4-5 IMPLEMENT/TEST | Open: T11b(running), T11c(new), T17 Lean(mathlib fetching), final compile+audit
Python: uv project (pyproject.toml + uv.lock, .venv); run `uv run --project . python -I <script>` (global UV_PROJECT and PYTHONPATH leak otherwise). Old verification/.venv used by T11/T11c runs.
