# Use Case: Python + JavaScript Monorepo

## Scenario Overview

Managing a monorepo containing both Python backend services and JavaScript/TypeScript frontend applications, requiring coordinated formatting across language boundaries.

## Primary Requirements

### Multi-Language Support
- Python formatting (backend services)
- JavaScript/TypeScript formatting (frontend)
- Shared configuration files (JSON, YAML, TOML)
- Documentation formatting (Markdown)

### Monorepo Coordination
- Single command for all formatting
- Workspace-aware configuration
- Selective formatting by path
- Consistent style philosophy

### Performance
- Fast formatting for large codebases
- Parallel execution per language
- Efficient CI caching
- Incremental formatting support

### Developer Experience
- Single pre-commit hook for all languages
- Clear separation of concerns
- No tool conflicts
- Simple onboarding

## Recommended Toolchain

### Python: Ruff Format
Fast, modern Python formatter

### JavaScript/TypeScript: Prettier
Industry standard for JS ecosystem

### Orchestration: pre-commit
Language-agnostic hook framework

**Why This Combination:**
- Best-in-class tools per language
- No overlap or conflicts
- Single hook framework
- Excellent performance

## Repository Structure

```
monorepo/
├── .pre-commit-config.yaml     # Unified hook configuration
├── pyproject.toml              # Python formatting config
├── .prettierrc                 # JS/TS formatting config
├── backend/
│   ├── services/
│   │   ├── api/                # Python FastAPI
│   │   └── workers/            # Python background jobs
│   └── shared/                 # Python packages
├── frontend/
│   ├── web/                    # React application
│   ├── mobile/                 # React Native
│   └── shared/                 # TypeScript packages
└── docs/                       # Markdown documentation
```

## Configuration Approach

### Python Configuration

`pyproject.toml`:
```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ruff.lint]
select = ["E", "F", "I", "N"]
extend-exclude = ["frontend/**"]  # Exclude JS/TS areas
```

### JavaScript/TypeScript Configuration

`.prettierrc`:
```json
{
  "printWidth": 100,
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "tabWidth": 2
}
```

`.prettierignore`:
```
backend/**
*.py
node_modules/
dist/
build/
```

### Unified Pre-commit Configuration

`.pre-commit-config.yaml`:
```yaml
repos:
  # Python formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff
        args: [--fix]
        files: ^backend/
      - id: ruff-format
        files: ^backend/

  # JavaScript/TypeScript formatting
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx]
        files: ^frontend/

  # Shared file formatting
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        name: prettier-shared
        types_or: [json, yaml, markdown]
        exclude: ^(backend/|frontend/)

  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
```

## Pre-commit Hook Setup

### Installation
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files (initial setup)
pre-commit run --all-files
```

### Selective Execution
```bash
# Format only Python
pre-commit run ruff-format --all-files

# Format only JavaScript/TypeScript
pre-commit run prettier --all-files

# Format specific path
pre-commit run --files backend/services/api/**
```

## CI/CD Integration

### GitHub Actions (Optimized for Monorepo)

```yaml
name: Format Check
on: [pull_request]

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      python: ${{ steps.filter.outputs.python }}
      javascript: ${{ steps.filter.outputs.javascript }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            python:
              - 'backend/**/*.py'
            javascript:
              - 'frontend/**/*.{js,jsx,ts,tsx}'

  format-python:
    needs: changes
    if: needs.changes.outputs.python == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - name: Check Python formatting
        run: uvx ruff format --check backend/

  format-javascript:
    needs: changes
    if: needs.changes.outputs.javascript == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Check JS formatting
        run: npx prettier --check "frontend/**/*.{js,jsx,ts,tsx}"
```

### Performance Optimization
- Use path filtering to skip unnecessary checks
- Run language checks in parallel
- Cache tool installations
- Use `--check` mode to avoid writes

## Common Pitfalls

### Pitfall 1: Overlapping File Patterns
**Problem:** Both Python and JS formatters try to process JSON/YAML files differently

**Solution:** Use explicit `files:` patterns in `.pre-commit-config.yaml` to separate concerns

### Pitfall 2: Conflicting Line Lengths
**Problem:** Python code at 88 chars, JS at 80 chars creates inconsistent style philosophy

**Solution:** Align line lengths across languages (recommend 100 for both)

### Pitfall 3: Shared Config File Formatting
**Problem:** `package.json` formatted by Prettier, `pyproject.toml` left unformatted

**Solution:** Use Prettier for JSON formatting, Taplo for TOML formatting:
```yaml
- repo: https://github.com/ComPWA/taplo-pre-commit
  rev: v0.9.3
  hooks:
    - id: taplo-format
```

### Pitfall 4: Slow Pre-commit on Large Changes
**Problem:** Formatting 1000+ files in single commit takes minutes

**Solution:**
- Run formatters in parallel (pre-commit does this by default)
- Use `pre-commit run --files $(git diff --name-only)` for faster iteration
- Consider `lint-staged` for JS-specific workflows

### Pitfall 5: Documentation Drift
**Problem:** Code examples in docs aren't validated or formatted

**Solution:** Add documentation formatting hooks:
```yaml
- repo: https://github.com/asottile/blacken-docs
  rev: v1.16.0
  hooks:
    - id: blacken-docs
      additional_dependencies: [black]
```

## Alternative Approaches

### Approach 1: Language-Specific Hooks
Use Husky (JS) for frontend, pre-commit (Python) for backend

**Pros:** Native tooling per ecosystem
**Cons:** Duplicated configuration, harder to maintain

### Approach 2: Unified Tooling (Mega-Linters)
Use MegaLinter or Super-Linter for all formatting

**Pros:** Single configuration file
**Cons:** Slower, less flexible, heavier dependencies

### Approach 3: CI-Only Formatting
Skip pre-commit hooks, enforce only in CI

**Pros:** No local development friction
**Cons:** Slower feedback, more failed CI runs

## Workspace-Specific Commands

### Root-Level Scripts

`Makefile`:
```makefile
.PHONY: format format-check

format:
	@echo "Formatting Python..."
	uvx ruff format backend/
	@echo "Formatting JavaScript/TypeScript..."
	cd frontend && npm run format

format-check:
	@echo "Checking Python formatting..."
	uvx ruff format --check backend/
	@echo "Checking JavaScript/TypeScript formatting..."
	cd frontend && npm run format:check
```

### NPM Scripts for Frontend

`frontend/package.json`:
```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

## Success Metrics

- Single command formats entire monorepo
- CI checks complete in < 60 seconds
- No cross-language formatting conflicts
- Onboarding developers in < 30 minutes
- Zero manual formatting discussions

## Date Compiled
December 4, 2025
