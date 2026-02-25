.PHONY: help demo validate test lint format typecheck clean

PY ?= python3

help:
	@echo "Targets:"
	@echo "  make demo       Run end-to-end demo (fixtures -> artifacts)"
	@echo "  make validate   Lint + format-check + typecheck + tests + demo"
	@echo "  make test       Run pytest"
	@echo "  make lint       Run ruff check"
	@echo "  make format     Run ruff format (write)"
	@echo "  make typecheck  Run mypy"
	@echo "  make clean      Remove generated artifacts (careful)"

demo:
	$(PY) -m msb demo

test:
	$(PY) -m pytest

lint:
	$(PY) -m ruff check .

format:
	$(PY) -m ruff format .

typecheck:
	$(PY) -m mypy src tests

validate:
	$(PY) -m ruff format --check .
	$(PY) -m ruff check .
	$(PY) -m mypy src tests
	$(PY) -m pytest -m "not slow"
	$(PY) -m msb demo

clean:
	rm -rf artifacts/before artifacts/after artifacts/compare artifacts/report
