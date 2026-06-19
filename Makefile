.PHONY: build check lint test

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

lint build: check

test:
	@cd "$(ROOT)" && python3 -m unittest discover -s tests

check:
	@cd "$(ROOT)" && ./scripts/check-baseline.py
	@cd "$(ROOT)" && python3 -m unittest discover -s tests
