# Code Formatter Feature Comparison Matrix

## Overview

Comprehensive comparison of code formatting and linting tools across Python and JavaScript/TypeScript ecosystems. This matrix evaluates tools across performance, configuration, integration, and capability dimensions.

## Quick Reference

| Tool | Language | Type | Speed | Config | Primary Use |
|------|----------|------|-------|--------|-------------|
| **Black** | Python | Formatter | Baseline | Minimal | Python formatting standard |
| **Ruff** | Python | Unified | 30-100x | Moderate | Fast Python format+lint |
| **Prettier** | JS/TS/Multi | Formatter | Baseline | Minimal | JS/TS formatting standard |
| **Biome** | JS/TS | Unified | 25x | Moderate | Fast JS/TS format+lint |
| **ESLint** | JS/TS | Linter | Slow | Extensive | Comprehensive linting |

## Performance Comparison

### Formatting Speed

**Python Formatters (250k lines codebase):**

| Tool | Time | Lines/Second | Speedup vs Black | Implementation |
|------|------|--------------|------------------|----------------|
| **Ruff** | <100ms | 2,500,000+ | 30-100x faster | Rust |
| **Black** | 1-3s | ~100,000 | Baseline | Python |
| **YAPF** | 10-15s | ~20,000 | 10x slower | Python |
| **autopep8** | 5-8s | ~40,000 | 3-5x slower | Python |
| **Blue** | ~1-3s | ~100,000 | Similar | Python (Black fork) |

**JavaScript Formatters (large codebase):**

| Tool | Time (312 files) | Speedup | Implementation |
|------|------------------|---------|----------------|
| **dprint** | <100ms | 100x faster | Rust |
| **Biome** | 1.3s | 20x faster | Rust |
| **Prettier** | 28s | Baseline | JavaScript |

### Linting Speed

**Python Linters:**

| Tool | Speed | Comparison |
|------|-------|------------|
| **Ruff check** | 10-100x faster | vs Flake8 |
| **Flake8** | Baseline | Traditional |
| **Pylint** | 2-5x slower | Comprehensive but slow |

**JavaScript Linters:**

| Tool | Speed | Comparison |
|------|-------|------------|
| **Biome lint** | 15x faster | vs ESLint |
| **ESLint** | Baseline | Traditional |

### Startup Time Impact

| Tool | Startup Overhead | Impact on Small Files |
|------|------------------|----------------------|
| **Ruff** | <10ms | Negligible |
| **Biome** | <10ms | Negligible |
| **Black** | ~100-200ms | Noticeable in pre-commit |
| **Prettier** | ~50-100ms | Moderate |
| **ESLint** | ~100-300ms | Noticeable with plugins |

## Configuration Flexibility

### Philosophy Spectrum

| Tool | Philosophy | Line Length | String Quotes | Import Sorting | Total Options |
|------|------------|-------------|---------------|----------------|---------------|
| **Black** | Uncompromising | ✓ (88 default) | ✗ (double only) | ✗ (separate tool) | ~5 |
| **Ruff format** | Black-compatible | ✓ (88 default) | ✓ | ✓ (via lint) | ~10 |
| **Blue** | Less uncompromising | ✓ (79 default) | ✓ (single default) | ✗ | ~8 |
| **autopep8** | PEP 8 compliant | ✓ | ✗ | ✗ | ~20 |
| **YAPF** | Highly configurable | ✓ | ✓ | ✗ | ~50 |
| **Prettier** | Opinionated | ✓ (80 default) | ✓ | ✗ | ~15 |
| **Biome** | Moderately opinionated | ✓ (80 default) | ✓ | ✓ | ~20 |
| **dprint** | Configurable | ✓ | ✓ | ✗ | ~30 |
| **ESLint** | Highly configurable | ✓ | ✓ | Via plugin | 400+ rules |

### Configuration File Format

| Tool | Config File | Format | Multiple Files |
|------|-------------|--------|----------------|
| **Black** | pyproject.toml | TOML | No |
| **Ruff** | pyproject.toml, ruff.toml | TOML | Yes |
| **Prettier** | .prettierrc | JSON/YAML/JS | Yes |
| **Biome** | biome.json | JSON/JSONC | Yes |
| **ESLint** | eslint.config.js, .eslintrc | JS/JSON/YAML | Yes |

### Per-File Configuration

| Tool | Inline Disable | Per-Directory | Per-File Overrides |
|------|----------------|---------------|--------------------|
| **Black** | ✓ (# fmt: off) | ✗ | ✗ |
| **Ruff** | ✓ (# noqa) | ✓ | ✓ |
| **Prettier** | ✓ (<!-- prettier-ignore -->) | ✗ | ✓ (via overrides) |
| **Biome** | ✓ (// biome-ignore) | ✓ | ✓ |
| **ESLint** | ✓ (/* eslint-disable */) | ✓ | ✓ |

## IDE Integration

### VS Code Support

| Tool | Extension | Downloads | LSP | Format on Save | Auto-fix | Quality |
|------|-----------|-----------|-----|----------------|----------|---------|
| **Black** | Official + Python ext | 10M+ (Python ext) | ✓ | ✓ | N/A | Excellent |
| **Ruff** | Official | 1M+ | ✓ | ✓ | ✓ | Excellent |
| **Prettier** | Official | 30M+ | ✗ | ✓ | N/A | Excellent |
| **Biome** | Official | 500K+ | ✓ | ✓ | ✓ | Excellent |
| **ESLint** | Official | 25M+ | ✓ | ✓ | ✓ | Excellent |

### PyCharm/WebStorm Support

| Tool | Integration | Quality | Native Support |
|------|-------------|---------|----------------|
| **Black** | Built-in | Excellent | ✓ |
| **Ruff** | Plugin | Good | ✗ |
| **Prettier** | Built-in | Excellent | ✓ |
| **Biome** | Plugin | Good | ✗ |
| **ESLint** | Built-in | Excellent | ✓ |

### Vim/Neovim Support

| Tool | Plugin Availability | LSP Support | Quality |
|------|---------------------|-------------|---------|
| **Black** | vim-black | ✗ | Good |
| **Ruff** | nvim-lspconfig | ✓ | Excellent |
| **Prettier** | Multiple | ✗ | Good |
| **Biome** | nvim-lspconfig | ✓ | Good |
| **ESLint** | coc-eslint, ALE | ✓ | Excellent |

## CI/CD Integration

### Pre-commit Hook Support

| Tool | Official Hook | Speed | Startup Time | Cache Support |
|------|---------------|-------|--------------|---------------|
| **Black** | ✓ | Moderate | ~200ms | ✓ |
| **Ruff** | ✓ | Very Fast | <10ms | ✓ |
| **Prettier** | ✓ | Moderate | ~100ms | ✓ |
| **Biome** | Community | Very Fast | <10ms | ✗ |
| **ESLint** | ✓ | Slow | ~300ms | ✓ |

### GitHub Actions

| Tool | Official Action | Community Actions | Ease of Use |
|------|----------------|-------------------|-------------|
| **Black** | ✓ (psf/black) | Many | Excellent |
| **Ruff** | ✓ (astral-sh/ruff-action) | Growing | Excellent |
| **Prettier** | ✗ | Many | Good |
| **Biome** | ✗ | Few | Moderate |
| **ESLint** | ✗ | Many | Good |

### Docker/Container Friendliness

| Tool | Binary Size | Dependencies | Install Time |
|------|-------------|--------------|--------------|
| **Ruff** | ~10MB | Single binary | <1s |
| **Biome** | ~15MB | Single binary | <1s |
| **Black** | ~50MB+ | Python + deps | 5-10s |
| **Prettier** | ~30MB+ | Node + deps | 10-20s |
| **ESLint** | ~50MB+ | Node + plugins | 20-60s |

## Language and Feature Support

### Python Tools

| Feature | Black | Ruff | autopep8 | YAPF | Blue |
|---------|-------|------|----------|------|------|
| **Formatting** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Linting** | ✗ | ✓ | ✗ | ✗ | ✗ |
| **Import Sorting** | ✗ | ✓ | ✗ | ✗ | ✗ |
| **Auto-fix** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Type Stubs (.pyi)** | ✓ | ✓ | ✗ | ✓ | ✓ |
| **Jupyter Notebooks** | ✓ (via plugin) | ✓ | ✗ | ✗ | ✓ |
| **Python 2 Support** | ✗ | ✗ | ✓ | ✓ | ✗ |
| **Python 3.7+** | ✓ | ✓ | ✓ | ✓ | ✓ |

### JavaScript/TypeScript Tools

| Feature | Prettier | Biome | dprint | ESLint |
|---------|----------|-------|--------|--------|
| **JavaScript** | ✓ | ✓ | ✓ | ✓ |
| **TypeScript** | ✓ | ✓ | ✓ | ✓ |
| **JSX/TSX** | ✓ | ✓ | ✓ | ✓ |
| **JSON** | ✓ | ✓ | ✓ | ✓ |
| **CSS/SCSS** | ✓ | ✓ (exp) | ✓ | ✗ |
| **HTML** | ✓ | ✗ | ✓ | ✗ |
| **Markdown** | ✓ | ✗ | ✓ | ✗ |
| **YAML** | ✓ | ✗ | ✓ | ✗ |
| **GraphQL** | ✓ | 🚧 | ✓ | Via plugin |
| **Vue** | ✓ | Limited | ✓ | ✓ |
| **Import Sorting** | ✗ | ✓ | ✗ | Via plugin |
| **Linting** | ✗ | ✓ | ✗ | ✓ |

✓ = Full support, 🚧 = In progress, ✗ = Not supported

## Compatibility and Migration

### Drop-in Replacement Compatibility

| Original Tool | Replacement | Compatibility | Migration Effort |
|---------------|-------------|---------------|------------------|
| Black → Ruff | Ruff format | >99.9% | Low (minimal diffs) |
| isort → Ruff | Ruff check -I | ~95% | Low |
| Flake8 → Ruff | Ruff check | ~90% | Moderate (config mapping) |
| Prettier → Biome | Biome format | ~97% | Low (migration tool) |
| ESLint → Biome | Biome lint | ~30% | High (limited rules) |

### Breaking Change Frequency

| Tool | Major Releases | Breaking Changes | Stability |
|------|----------------|------------------|-----------|
| **Black** | Yearly | Minimal | Very Stable |
| **Ruff** | Frequent | Low (semantic versioning) | Stable |
| **Prettier** | ~Yearly | Minimal | Very Stable |
| **Biome** | Frequent | Moderate | Maturing |
| **ESLint** | ~2 years | Moderate | Stable |

### Cross-Platform Consistency

| Tool | Windows | macOS | Linux | Deterministic Output |
|------|---------|-------|-------|---------------------|
| **Black** | ✓ | ✓ | ✓ | ✓ |
| **Ruff** | ✓ | ✓ | ✓ | ✓ |
| **Prettier** | ✓ | ✓ | ✓ | ✓ |
| **Biome** | ✓ | ✓ | ✓ | ✓ |
| **ESLint** | ✓ | ✓ | ✓ | ✓ |

## Advanced Features

### Incremental Formatting

| Tool | Incremental Support | Cache Strategy | Performance Gain |
|------|---------------------|----------------|------------------|
| **Ruff** | ✓ | File-level | Moderate |
| **Black** | ✓ | File-level (.black cache) | Moderate |
| **Prettier** | ✓ | File-level (--cache) | Significant |
| **Biome** | ✗ | None | N/A |
| **dprint** | ✓ | File-level | Significant |

### Multi-threading

| Tool | Multi-threaded | Performance Impact |
|------|----------------|-------------------|
| **Ruff** | ✓ (Rust) | High |
| **Biome** | ✓ (Rust, default) | Very High (25-100x) |
| **dprint** | ✓ (Rust) | Very High |
| **Black** | Limited (--fast) | Moderate |
| **Prettier** | ✗ | N/A |
| **ESLint** | ✗ | N/A |

### Plugin/Extension System

| Tool | Plugin System | Plugin Count | Extensibility |
|------|---------------|--------------|---------------|
| **Ruff** | 🚧 (coming) | N/A | Limited (built-in rules) |
| **ESLint** | ✓ | 1000+ | Excellent |
| **Prettier** | ✓ | 100+ | Good |
| **Biome** | 🚧 (Biome 2.0) | N/A | Limited |
| **Black** | ✗ | N/A | Minimal |

## Ecosystem Maturity

### Community Metrics (December 2025)

| Tool | GitHub Stars | npm/PyPI Downloads/month | Age | Activity |
|------|--------------|--------------------------|-----|----------|
| **Black** | ~38,000 | ~15M PyPI | 7 years | Active |
| **Ruff** | ~50,000 | ~10M PyPI | 3 years | Very Active |
| **Prettier** | ~49,000 | ~50M npm | 8 years | Active |
| **Biome** | ~15,000 | ~5M npm | 2 years | Very Active |
| **ESLint** | ~25,000 | ~60M npm | 12 years | Active |

### Documentation Quality

| Tool | Docs Quality | Examples | Migration Guides | Community Resources |
|------|--------------|----------|------------------|---------------------|
| **Black** | Excellent | Good | Good | Extensive |
| **Ruff** | Excellent | Excellent | Excellent | Growing |
| **Prettier** | Excellent | Excellent | Good | Extensive |
| **Biome** | Good | Good | Excellent | Growing |
| **ESLint** | Excellent | Excellent | Good | Extensive |

## Decision Matrix

### Choose Based on Priority

**Priority: Speed (Large Codebase, CI Performance)**
1. Ruff (Python)
2. Biome (JS/TS)
3. dprint (JS/TS multi-language)

**Priority: Stability (Battle-tested, Mature)**
1. Black (Python)
2. Prettier (JS/TS)
3. ESLint (JS/TS linting)

**Priority: Unified Toolchain (Format + Lint)**
1. Ruff (Python)
2. Biome (JS/TS)

**Priority: Configuration Flexibility**
1. ESLint (JS/TS linting)
2. YAPF (Python formatting)

**Priority: Language Coverage (Multi-language projects)**
1. Prettier (JS/TS/CSS/HTML/Markdown/YAML)
2. dprint (similar coverage, faster)

**Priority: Linting Depth (Comprehensive checks)**
1. ESLint (JS/TS)
2. Ruff (Python)

## Summary Recommendations

### Python Projects
- **New project:** Ruff (format + lint)
- **Established project:** Black + Ruff (lint)
- **Maximum stability:** Black + Flake8/isort
- **Performance critical:** Ruff

### JavaScript/TypeScript Projects
- **New project:** Biome (format + lint)
- **Established project:** Prettier + ESLint
- **Large monorepo:** Biome (performance)
- **Multi-language:** Prettier (coverage)
- **Maximum linting:** Prettier + ESLint

### Hybrid Approach
- Biome/Ruff for speed on JS/TS or Python
- Prettier for additional languages (HTML, Markdown, YAML)
- ESLint for comprehensive JS/TS linting if Biome insufficient
