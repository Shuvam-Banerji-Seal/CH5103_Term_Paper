# Build the CH5103 beamer deck (LuaLaTeX, Noir theme).
#   make           build build/main.pdf and copy it to ch5103-presentation.pdf
#   make assets    regenerate screenshots, plot data and JS/SVG diagrams first
#   make check     list every warning / bad box in the last build (expects "CLEAN")
#   make clean     remove build/
UV      ?= uv
THREADS ?= $(shell nproc)
PY       = OMP_NUM_THREADS=$(THREADS) $(UV) run --project $(CURDIR)/.. python -I

.PHONY: all pdf assets screenshots data diagrams check clean

all: pdf

pdf:
	latexmk main.tex
	cp build/main.pdf ch5103-presentation.pdf
	@python3 -I scripts/check_log.py

assets: screenshots data diagrams

screenshots:
	$(PY) scripts/make_screenshots.py

data:
	$(PY) scripts/make_data.py

diagrams:
	diagrams-src/build.sh

check:
	@python3 -I scripts/check_log.py

clean:
	rm -rf build
