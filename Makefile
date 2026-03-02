MAIN_TEX := main.tex
LATEXMK := latexmk

.PHONY: all build pdf watch clean

all: pdf

build: pdf

pdf:
	$(LATEXMK) -g -pdf -interaction=nonstopmode -halt-on-error $(MAIN_TEX) -f

watch:
	$(LATEXMK) -pvc -view=none -pdf -interaction=nonstopmode -halt-on-error $(MAIN_TEX)

clean:
	$(LATEXMK) -C $(MAIN_TEX)
