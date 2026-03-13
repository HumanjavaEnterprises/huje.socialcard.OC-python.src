# socialcard — CLAUDE.md

## What is this?
An OpenClaw skill / Python package for generating social card images (OG, Twitter, GitHub).
Builder pattern API. Single dependency: Pillow.

## Commands
- `pytest -v` — run all tests
- `python -m build` — build wheel
- `twine upload dist/*` — publish to PyPI

## Structure
- `src/socialcard/` — package source
- `clawhub/` — ClawHub skill metadata
- `tests/` — pytest tests
- `examples/` — usage examples

## Conventions
- Vanilla Python, no async
- Kebab-case for file names (except Python modules)
- All source files have the huje.tools tagline comment
