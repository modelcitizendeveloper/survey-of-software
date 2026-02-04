# S1 Rapid Library Search: Code Formatting

**Research Domain:** 1.104.2 Code Formatting
**Date Compiled:** December 4, 2025
**Methodology:** S1 - Rapid Library Search (2-3 hours)

## Quick Start

Read `recommendation.md` first for actionable guidance.

## Files

### Methodology
- `approach.md` - S1 methodology explanation (88 lines)

### Python Ecosystem
- `black.md` - Established formatter standard (45 lines)
- `ruff.md` - Modern unified linter/formatter (64 lines) ⭐ **RECOMMENDED**
- `autopep8.md` - Legacy PEP 8 fixer (52 lines)
- `yapf.md` - Google's configurable formatter (55 lines)
- `isort.md` - Import sorting tool (65 lines)
- `blue.md` - Black alternative with single quotes (60 lines)

### JavaScript/TypeScript Ecosystem
- `prettier.md` - Dominant formatter (64 lines) ⭐ **RECOMMENDED**
- `eslint.md` - Standard linter (84 lines) ⭐ **RECOMMENDED**
- `biome.md` - Unified Rust-based toolchain (88 lines) 🚀 **EMERGING**
- `dprint.md` - Rust-based performance formatter (86 lines)

### Recommendations
- `recommendation.md` - Comprehensive guidance by ecosystem (373 lines) ⭐ **START HERE**

## Key Findings

### Python (Dec 2025)
**Ruff is replacing Black + isort + Flake8**
- 30x faster than Black
- >99.9% Black compatibility
- Unified linting + formatting
- Major adoption: FastAPI, pandas, Apache Airflow

**Safe Default:** Ruff

### JavaScript/TypeScript (Dec 2025)
**Prettier + ESLint remain dominant**
- 55M weekly Prettier downloads
- 63M weekly ESLint downloads
- Mature ecosystem, predictable behavior

**Emerging:** Biome (97% Prettier compatibility, 391 ESLint rules, much faster)

**Safe Default:** Prettier + ESLint

## Decision Tree

```
Python Project?
├─ New → Use Ruff
├─ Existing Black → Migrate to Ruff
└─ Risk-averse → Keep Black

JavaScript/TypeScript Project?
├─ New + Simple → Consider Biome
├─ New + Complex → Prettier + ESLint
└─ Existing → Keep Prettier + ESLint
```

## Research Scope

Total lines: 1,124 across 12 files
Time investment: ~2-3 hours (S1 Rapid methodology)

## Next Steps

- S2 (Comprehensive): Deep configuration analysis
- S3 (Need-Driven): Specific use case implementation
- S4 (Strategic): Long-term tooling strategy
