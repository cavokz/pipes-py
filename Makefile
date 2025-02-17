SHELL := bash
TEE_STDERR := tee >(cat 1>&2)

ifneq ($(VENV),)
	PYTHON ?= $(VENV)/bin/python3
else
	PYTHON ?= python3
endif

all: lint

prereq:
	$(PYTHON) -m pip install -r requirements.txt

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m black -q --check . || ($(PYTHON) -m black .; false)
	$(PYTHON) -m isort -q --check . || ($(PYTHON) -m isort .; false)

test: FORCE
	$(PYTHON) -m venv test/venv
	source test/venv/bin/activate; $(MAKE) test-ci

test-ci:
	pip install .
	elastic-pipes version
	elastic-pipes new-pipe -f test/test-pipe.py
	echo "test-result: ok" | $(PYTHON) test/test-pipe.py | [ "`$(TEE_STDERR)`" = "test-result: ok" ]
	echo "test-result: ok" | elastic-pipes run --log-level=debug test/test.yaml | [ "`$(TEE_STDERR)`" = "test-result: ok" ]
	cat test/test.yaml | elastic-pipes run --log-level=debug - | [ "`$(TEE_STDERR)`" = "{}" ]

clean:
	rm -rf test/venv test/test-pipe.py

.PHONY: FORCE
