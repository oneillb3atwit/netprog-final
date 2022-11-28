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


.PHONY: all run-client run-server
