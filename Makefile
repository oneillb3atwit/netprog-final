.POSIX:

all: run-client

run-client:
	python src/airhockey.py

run-server:
	python src/airhockey.py -s

debug-client:
	python src/airhockey.py -d

debug-server:
	python src/airhockey.py -s -d

dist:
	tar -czfv pygame-multiplayer-$(git rev-parse --short HEAD).tar.gz img src/ Makefile README.md LICENSE

distclean:
	rm -fv pygame-multiplayer-*.tar.gz

.PHONY: all run-client run-server dist distclean
