.PHONY: build check lint test

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3
override PYTHONDONTWRITEBYTECODE := 1
export PYTHONDONTWRITEBYTECODE

lint build: check

test:
	@PYTHON="$(PYTHON)" "$(ROOT)/scripts/check-python3.sh"
	@cd "$(ROOT)" && "$(PYTHON)" -m unittest discover -s tests

check:
	@PYTHON="$(PYTHON)" "$(ROOT)/scripts/check-python3.sh"
	@cd "$(ROOT)" && "$(PYTHON)" scripts/check-baseline.py
	@cd "$(ROOT)" && "$(PYTHON)" -m unittest discover -s tests
