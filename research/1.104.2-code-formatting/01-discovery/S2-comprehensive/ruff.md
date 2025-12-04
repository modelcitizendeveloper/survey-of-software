# Ruff: Unified Python Linting and Formatting

## Overview

Ruff is an extremely fast Python linter and code formatter written in Rust. It provides a unified toolchain combining linting (Flake8, pylint, pyupgrade, etc.) and formatting (Black-compatible) in a single tool, delivering 10-100x performance improvements over traditional Python tools.

**Current Status:** Rapidly maturing, production-ready
**Written In:** Rust
**License:** MIT
**First Release:** 2022
**Latest Version:** 0.8.x (as of December 2025)
**Company:** Astral (formerly maintained by Charlie Marsh)

## Core Philosophy

Ruff's philosophy centers on **unified toolchain performance**: consolidate multiple Python quality tools (formatter, linter, import sorter) into a single, blazingly fast executable.

**Design Principles:**
- Extreme performance through Rust implementation
- Black-compatible formatting (>99.9% compatibility)
- isort-compatible import sorting
- Replace Flake8, Black, isort, pyupgrade, autoflake, and more
- Single configuration file
- Zero-downtime migration from existing tools

## Architecture

**Two Primary Modes:**

1. **`ruff check`** - Linting and auto-fixing
   - 800+ rules covering Flake8, pylint, pyupgrade, etc.
   - Import sorting (isort replacement)
   - Code quality checks
   - Auto-fixes for many rules

2. **`ruff format`** - Code formatting
   - Black-compatible formatter
   - AST-based, safe transformations
   - Does NOT currently sort imports (use `ruff check --select I --fix`)

## Performance Characteristics

**Speed Benchmarks:**

**Formatter (`ruff format`):**
- 30x faster than Black
- 100x faster than YAPF
- ~250,000 lines: <100ms (vs. Black's 1-3 seconds)
- Even without caching, faster than Black with caching

**Linter (`ruff check`):**
- 10-100x faster than Flake8
- 98% faster in real-world cases (120ms vs 7s)
- Pre-commit hooks: 10s → 80ms in monorepo examples

**Example Benchmarks (250k line codebase):**
| Tool | Time | Speedup |
|------|------|---------|
| Ruff format | <100ms | - |
| Black (cached) | 1-2s | 10-20x slower |
| Black (no cache) | 2-3s | 20-30x slower |
| YAPF | 10-15s | 100x slower |

**Why So Fast:**
- Written in Rust (no GIL, true parallelization)
- Single binary (no Python startup time)
- Optimized parser and AST representation
- Minimal file I/O through shared infrastructure

## Formatter: Black Compatibility

**Compatibility Level:**
- >99.9% compatible with Black on Black-formatted code
- Django codebase: differ on 34 out of 2,772 files
- Zulip codebase: >99.9% identical output

**Known Differences:**
- Rare edge cases in string concatenation
- Subtle differences in comment placement
- Minimal impact on most codebases

**Configuration Parity:**
- Supports Black's main options: `line-length`, `target-version`
- `format.quote-style` for string quotes
- `format.indent-style` (spaces/tabs)
- `format.skip-magic-trailing-comma`

## Linter: Rule Coverage

**Built-in Rule Categories (800+ rules):**

- **Pyflakes (F):** Logical errors
- **pycodestyle (E, W):** PEP 8 violations
- **isort (I):** Import sorting
- **pydocstyle (D):** Docstring conventions
- **pyupgrade (UP):** Modern Python syntax
- **flake8-bugbear (B):** Bug detection
- **flake8-comprehensions (C4):** List/dict comprehension improvements
- **pylint (PL):** Code quality checks
- **Many more:** 50+ Flake8 plugins implemented

**Import Sorting (isort replacement):**
- Near-equivalent to `isort` with `profile = "black"`
- Enable with: `ruff check --select I --fix`
- Configurable import sections
- Supports `__all__` sorting with RUF022

## Configuration

**Single Configuration File:**
- `pyproject.toml` (preferred)
- `ruff.toml`
- `.ruff.toml`

**Example Configuration:**
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

# Linter configuration
[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "F",  # pyflakes
    "I",  # isort
    "UP", # pyupgrade
    "B",  # flake8-bugbear
]
ignore = ["E501"]  # Line too long (handled by formatter)

[tool.ruff.lint.isort]
known-first-party = ["mypackage"]

# Formatter configuration
[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## IDE and Ecosystem Integration

**IDE Support:**
- VS Code: Official Ruff extension (excellent performance)
- PyCharm: Ruff plugin available
- Vim/Neovim: nvim-lspconfig support
- Emacs: ruff.el package
- Language Server Protocol: Built-in support

**CI/CD Integration:**
- Pre-commit: `ruff` and `ruff-format` hooks
- GitHub Actions: `astral-sh/ruff-action`
- Extremely fast in CI (seconds vs. minutes)

**Migration Tools:**
```bash
# Check compatibility with existing code
ruff check --diff .

# Format and show what would change
ruff format --diff .

# Auto-fix and format
ruff check --fix . && ruff format .
```

## Migration Strategy

**From Black + Flake8 + isort:**

1. **Phase 1: Add Ruff linter**
   ```toml
   [tool.ruff.lint]
   select = ["E", "F", "I"]
   ```
   Continue using Black for formatting

2. **Phase 2: Enable Ruff formatter**
   ```bash
   ruff format .  # Should produce near-identical output
   ```
   Compare diffs, commit separately

3. **Phase 3: Remove old tools**
   ```bash
   pip uninstall black isort flake8
   ```
   Update pre-commit config, CI scripts

**Expected Impact:**
- Django: 34 changed files out of 2,772 (1.2%)
- Most projects: <0.1% line changes
- Primarily comment placement and edge cases

## Strengths

**Performance:**
- 30-100x faster than equivalent Python tools
- Transforms slow pre-commit hooks into instant feedback
- Critical for large monorepos and AI/ML codebases

**Unified Toolchain:**
- Single tool replaces 5-10 separate tools
- One configuration file vs. multiple
- Consistent behavior across linting and formatting
- Shared AST infrastructure (faster, more consistent)

**Black Compatibility:**
- Drop-in replacement for most projects
- Minimal migration effort
- Preserves existing code style

**Active Development:**
- Rapidly improving (multiple releases per month)
- Responsive maintainers
- Strong community adoption

**Major Adopters:**
- Apache Airflow
- FastAPI
- pandas
- pydantic
- Pylint (uses Ruff as pre-commit hook)

## Limitations

**Formatter Maturity:**
- Newer than Black (2023 vs. 2018)
- Edge cases still being discovered
- Some teams prefer Black's battle-tested stability

**Import Sorting Separation:**
- `ruff format` does NOT sort imports
- Must run `ruff check --select I --fix` separately
- Less ergonomic than isort integration

**Rule Coverage:**
- 800+ rules, but not every Flake8 plugin covered
- Some custom pylint plugins not available
- Gap shrinking rapidly

**Configuration Migration:**
- Not 1:1 mapping from all Flake8 plugins
- Requires manual config translation
- May need to adjust ignored rules

## Use Cases

**Ideal For:**
- New Python projects (modern, fast, unified)
- Large codebases with slow CI pipelines
- Monorepos requiring fast pre-commit hooks
- Teams consolidating toolchains
- Projects already using Black (easy migration)

**Consider Carefully:**
- Teams requiring 100% Black compatibility
- Projects with complex custom Flake8 plugins
- Conservative organizations (Black more mature)

## Recommended Workflow

**Standard Commands:**
```bash
# Check code (lint + import sort)
ruff check --fix .

# Format code
ruff format .

# Combined (recommended in CI)
ruff check . && ruff format --check .
```

**Pre-commit Hook:**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

**VS Code Settings:**
```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    }
  }
}
```

## Future Direction

**Roadmap:**
- Plugin system for custom rules
- Enhanced import sorting (integrated with formatter)
- Additional language support (type stubs)
- Performance optimizations
- Deeper IDE integration

## Unified vs. Separate Tools Decision

**Ruff Format + Check (Unified):**
- Pros: Single tool, 30x faster, simpler config
- Cons: Newer, slight compatibility differences

**Black + Ruff Check (Hybrid):**
- Pros: Battle-tested Black, still fast linting
- Cons: Two tools, two configs, slightly slower

**Recommendation:** Use unified Ruff for new projects or if CI performance is critical. Use Black + Ruff check if maximum stability is required.

## Verdict

Ruff represents the future of Python tooling: fast, unified, and practical. Its Black-compatible formatter achieves >99.9% compatibility while delivering 30x speed improvements. Combined with its comprehensive linting capabilities, Ruff consolidates 5-10 tools into one.

**Choose Ruff if:** You want maximum performance and a unified toolchain, or you're starting a new project.
**Stick with Black + Ruff linter if:** You need 100% Black compatibility or prefer maximum stability.

The Python community is rapidly adopting Ruff, with major projects like FastAPI, pandas, and pydantic already migrated. By 2025, Ruff has become the default recommendation for new Python projects.
