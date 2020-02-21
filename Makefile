CLANG ?= clang
LLC ?= llc
OPT ?= opt
PYTHON ?= python

.PHONY: all
all: fib

.PHONY: clean
clean:
	$(RM) fib

fib: fth.py core.fth fib.fth
	cat core.fth fib.fth | \
	$(PYTHON) fth.py | \
	$(OPT) --Os -S | \
	$(LLC) | \
	$(CLANG) -Wl,--gc-sections -x assembler -o $@ -
