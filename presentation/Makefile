# Build the CH5103 beamer deck (LuaLaTeX, Noir theme).
#   make           build build/main.pdf and copy it to ch5103-presentation.pdf
#   make handout   one page per frame (overlays collapsed) -> ch5103-handout.pdf
#   make presenter the narration of every slide, plain text -> ch5103-presenter-script.pdf
#   make script    the same with each slide's picture and video times -> ch5103-script-handout.pdf
#   make script-body  regenerate script/*-body.tex from the video's scenes and render subtitles first
#   make assets    regenerate screenshots, plot data and JS/SVG diagrams first
#   make check     list every warning / bad box in the last build (expects "CLEAN")
#   make clean     remove build/
UV      ?= uv
THREADS ?= $(shell nproc)
PY       = OMP_NUM_THREADS=$(THREADS) $(UV) run --project $(CURDIR)/.. python -I

.PHONY: all pdf handout presenter script script-body assets screenshots data diagrams check clean

all: pdf

pdf:
	latexmk main.tex
	cp build/main.pdf ch5103-presentation.pdf
	@python3 -I scripts/check_log.py

handout:
	latexmk handout.tex
	cp build/handout.pdf ch5103-handout.pdf

presenter:
	latexmk script/presenter.tex
	cp build/presenter.pdf ch5103-presenter-script.pdf

script:
	latexmk script/script.tex
	cp build/script.pdf ch5103-script-handout.pdf

script-body:
	cd .. && video/scenes/.venv/bin/python -I video/tools/script_handout.py

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
