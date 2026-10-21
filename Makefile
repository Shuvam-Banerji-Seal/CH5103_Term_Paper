# Reproduce everything in this repository (uv-managed Python project).
#   make sync          create/refresh .venv from uv.lock
#   make figures       re-extract figures + captions from the paper PDF into assets/
#   make formulae      build assets/formulae.pdf
#   make derivations   build derivations/derivations.pdf
#   make verify        run the fast verification suite (T1-T10, T12-T15, T9b)
#   make verify-dft    run the DFT tests T11/T11c (slow: geometry optimisations)
#   make lean          fetch the Mathlib cache and check the Lean proofs
#   make all           sync figures formulae derivations verify lean
#
# `--project .` makes uv use this repository even if UV_PROJECT is set globally.
# `python -I` (isolated mode) ignores a global PYTHONPATH that may point at another Python.

UV      ?= uv
THREADS ?= $(shell nproc)
PY       = OMP_NUM_THREADS=$(THREADS) $(UV) run --project $(CURDIR) python -I

.PHONY: all sync figures formulae derivations verify verify-dft lean clean

all: sync figures formulae derivations verify lean

sync:
	$(UV) sync --project .

figures:
	$(PY) scripts/extract_figures.py

formulae:
	cd assets && latexmk -pdf -interaction=nonstopmode -outdir=../build/formulae formulae.tex \
	  && cp ../build/formulae/formulae.pdf formulae.pdf

derivations:
	cd derivations && latexmk -pdf -interaction=nonstopmode -jobname=derivations \
	  -outdir=../build/derivations main.tex && cp ../build/derivations/derivations.pdf derivations.pdf

verify:
	@cd verification && for t in t01_spin_and_determinants t02_two_orbital_hamiltonian \
	  t03_t05_hund_virial_h2 t06_t09_models t09b_t15_correlation t10_t12_t13_symbolic; do \
	  echo "== $$t"; $(PY) $$t.py | tail -1; done

verify-dft:
	cd verification && $(PY) -u t11_rohf_and_distonic.py > logs/t11.log 2>&1
	cd verification && $(PY) -u t11c_distonic_functionals.py > logs/t11c.log 2>&1

lean:
	cd verification/lean_proofs && lake exe cache get && lake build

clean:
	rm -rf build
