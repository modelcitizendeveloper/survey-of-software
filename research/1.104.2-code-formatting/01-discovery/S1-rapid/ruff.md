# Ruff - Extremely Fast Python Linter and Formatter

**Ecosystem:** Python
**Category:** Linter + Formatter (unified)
**Repository:** https://github.com/astral-sh/ruff
**PyPI:** https://pypi.org/project/ruff/
**Maintainer:** Astral (creators of uv)

## Popularity Metrics (Dec 2025)

- **GitHub Stars:** 25,000+
- **Current Version:** 0.14.7
- **Major Adopters:** Apache Airflow, FastAPI, pandas, pydantic, Pylint itself
- **Built-in Rules:** 800+ rules
- **Written in:** Rust

## Key Differentiator

Ruff is a unified linter and formatter written in Rust that replaces Black, isort, Flake8, pyupgrade, autoflake, and dozens of plugins - all while running 10-100x faster than any individual tool.

## Performance Benchmarks

- **vs Black:** 30x faster (even faster than Black with caching)
- **vs Flake8:** 10-100x faster
- **vs YAPF:** 100x faster
- **Real-world:** 0.2s for entire codebase vs 20s with Flake8
- **dagster (250k LOC):** 0.4s vs pylint's 2.5 minutes

## Black Compatibility

Ruff's formatter achieves **>99.9% compatibility** with Black. When formatting Django codebase, Ruff and Black differ on only 34 out of 2,772 files.

**Known differences:**
- Ruff formats f-string expressions inside `{...}`
- Ruff handles end-of-line comments differently to preserve intent
- Default config mimics Black (double quotes, spaces, magic trailing commas)

## Features

- **Unified toolchain:** Linting + formatting + import sorting in one tool
- **Native re-implementations:** Popular Flake8 plugins built-in
- **Replaces:** Black, isort, Flake8, pyupgrade, autoflake, pydocstyle, yesqa, eradicate
- **Jupyter support:** Formats and lints `.ipynb` files
- **Python 3.14 support:** Updated for latest Python releases

## 2025 Status: Is Ruff Replacing Black?

**Yes, increasingly.** Major projects (FastAPI, pandas, Apache Airflow) have migrated to Ruff. The combination of:
- Black-compatible formatting
- Unified linting/formatting
- Extreme performance
- Active development by Astral

...makes Ruff the modern default for new Python projects.

## Quick Verdict

**Status:** Rapidly becoming the ecosystem default
**Best for:** Any Python project wanting speed, unified tooling, and Black compatibility
**Migration:** Drop-in Black replacement via `ruff format`

Ruff represents the new generation of Python tooling - Rust-based, unified, and extremely fast. While Black pioneered opinionated formatting, Ruff delivers the same philosophy with better performance and integrated linting.

**Recommendation:** Default choice for new projects. Strong candidate for migrating existing Black + Flake8 + isort setups.
