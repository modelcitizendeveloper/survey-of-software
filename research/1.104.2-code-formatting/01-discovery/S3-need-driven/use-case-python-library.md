# Use Case: Python Library/Package Development

## Scenario Overview

Developing a Python library or package for distribution via PyPI, requiring consistent formatting that aligns with Python ecosystem standards.

## Primary Requirements

### Code Quality
- PEP 8 compliance for broad compatibility
- Consistent style across all modules
- Readable diffs in version control
- Professional appearance for OSS consumers

### Distribution
- No runtime dependencies on formatters
- Clean source distribution formatting
- Documentation code example formatting
- Compatibility with multiple Python versions

### Development Workflow
- Fast local formatting
- Pre-commit integration
- CI verification without duplication
- Editor-agnostic consistency

### Collaboration
- Zero-config onboarding for contributors
- Minimal PR style debates
- Clear formatting enforcement
- Automated style fixes

## Recommended Toolchain

### Primary: Ruff Format
Modern, fast Python formatter with excellent library compatibility

**Why Ruff Format:**
- 10-100x faster than Black for CI/CD
- Drop-in Black compatibility for easy migration
- Single tool for linting + formatting
- Zero external dependencies
- Excellent Python 3.8+ support

### Alternative: Black
Industry standard with maximum ecosystem adoption

**Why Black:**
- Largest community and plugin ecosystem
- Proven stability over 5+ years
- Maximum tool integration
- "Opinionated" means zero configuration debates

## Configuration Approach

### Ruff Format Configuration

`pyproject.toml`:
```toml
[tool.ruff]
line-length = 88
target-version = "py38"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.ruff.lint]
select = ["E", "F", "I"]  # pycodestyle, pyflakes, isort
```

### Black Configuration

`pyproject.toml`:
```toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\.pyi?$'
```

## Pre-commit Hook Setup

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

Or for Black:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Format Check
on: [pull_request]
jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - name: Check formatting
        run: uvx ruff format --check .
```

### Performance Optimization
- Use `ruff format --check` for verification (no file writes)
- Cache pip/uv packages between runs
- Run formatting before test suite (fail fast)
- Consider `ruff format --diff` for PR comments

## Common Pitfalls

### Pitfall 1: Over-Customization
**Problem:** Customizing line length or quote styles reduces ecosystem compatibility

**Solution:** Use defaults (88 char, double quotes) unless strong requirement exists

### Pitfall 2: Formatting + Linting Conflicts
**Problem:** Running Black + Flake8 can create conflicting style requirements

**Solution:** Use Ruff which unifies formatting and linting, or configure Flake8 to ignore Black-formatted rules

### Pitfall 3: Documentation Example Drift
**Problem:** Code examples in docs aren't formatted consistently

**Solution:** Include `docs/**/*.py` in formatting paths, use `blacken-docs` for markdown

### Pitfall 4: Generated Code Formatting
**Problem:** Protobuf, GraphQL, or other generated code gets reformatted

**Solution:** Add generated paths to `.gitignore` and exclude from formatting

## Migration Strategy

### From Manual Style to Automated
1. Run `ruff format .` on entire codebase
2. Commit formatting changes separately
3. Add pre-commit hooks
4. Update CONTRIBUTING.md
5. Enable CI checks

### From Black to Ruff Format
1. Keep existing `pyproject.toml` configuration
2. Replace Black with Ruff in pre-commit
3. Update CI to use `uvx ruff format`
4. No code changes needed (compatible output)

## Success Metrics

- CI formatting check completes in < 10 seconds
- Zero formatting-related PR comments after adoption
- New contributors submit formatted code without prompting
- No configuration changes for 12+ months

## Date Compiled
December 4, 2025
