.PHONY: build check lint test

override empty :=
override space := $(empty) $(empty)
override makefile_space := __GARETHPAUL_MAKEFILE_SPACE__
override encoded_makefile_list := $(patsubst $(makefile_space)%,%,$(subst $(space),$(makefile_space),$(MAKEFILE_LIST)))
override ROOT := $(subst $(makefile_space),$(space),$(abspath $(dir $(lastword $(encoded_makefile_list)))))
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
