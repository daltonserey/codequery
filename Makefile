.PHONY: help venv dist test install
.DEFAULT: help

VENV?=venv
SYS_PYTHON=python3
PYTHON=$(VENV)/bin/python3
PIP=$(PYTHON) -m pip

help:
	@echo "uso: make [ venv | test | dist | upload | install ]"

venv: $(VENV)/bin/activate
$(VENV)/bin/activate: setup.py requirements.txt
	test -d $(VENV) || $(SYS_PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install wheel
	$(PIP) install --requirement requirements.txt
	touch $(VENV)/bin/activate

test:
	pytest


install: venv $(INSTALLED)
$(INSTALLED): $(shell find $(MODULE))
	$(PIP) install -e .
	touch $(INSTALLED)

dist: venv requirements.txt
	$(PYTHON) setup.py sdist bdist_wheel
	$(PYTHON) setup.py build -e"/usr/bin/env python3"

clean:
	python3 setup.py clean --all
	find . -type f -name "*.pyc" -exec rm '{}' +
	find . -type d -name "__pycache__" -exec rmdir '{}' +
	find . -type d -name ".pytest_cache" -exec rmdir '{}' +
	rm -rf dist build venv *.egg-info .coverage

$(VENV)/bin/twine:
	$(PIP) install twine

upload: dist $(VENV)/bin/twine
	$(PYTHON) -m twine upload dist/*
