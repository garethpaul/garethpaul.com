.PHONY: build check lint test

lint build: check

test:
	python3 -m unittest discover -s tests

check:
	./scripts/check-baseline.py
	python3 -m unittest discover -s tests
