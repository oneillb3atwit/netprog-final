.POSIX:

all: run-client

run-client:
	python src/client.py

run-server:
	python src/server.py


.PHONY: all run-client run-server
