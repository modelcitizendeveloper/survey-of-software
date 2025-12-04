# 1.104.2 Code Formatting Libraries - Discovery Table of Contents

**Research Code**: 1.104.2
**Domain**: Code Formatting & Linting (Python + JavaScript/TypeScript)
**Methodology**: MPSE v3.0 (S1-S4 Parallel Discovery)
**Date Compiled**: December 4, 2025

---

## Executive Summary

### Strategic Winners (December 2025)

| Ecosystem | Winner | Viability | Key Rationale |
|-----------|--------|-----------|---------------|
| **Python** | ruff | 92% | 30-100x faster than Black, unified format+lint, VC-backed |
| **JS/TS (performance)** | Biome | 88% | 25x faster than Prettier, format+lint unified |
| **JS/TS (stability)** | Prettier | 85% | Mature, best language coverage, OpenJS Foundation |

**Key Insight**: The "Rust rewrite everything" trend is real. Ruff is eating Black's lunch. Biome is challenging Prettier but hasn't won yet.

---

## Critical Question Answered: Is Ruff Replacing Black?

**Yes, increasingly.**

| Metric | Black | Ruff |
|--------|-------|------|
| Speed | Baseline | 30-100x faster |
| Compatibility | N/A | >99.9% Black-compatible |
| Features | Format only | Format + lint + import sort |
| Funding | Volunteer | VC-backed ($4M+ Astral) |
| Adoption | Established | FastAPI, pandas, pydantic migrated |
| 3-Year Outlook | Survives (75%) | Dominates (92%) |

**Recommendation**: Use ruff for all new Python projects. Migrate existing Black projects when convenient.

---

## Methodology Convergence

| Method | Python Recommendation | JS/TS Recommendation | Confidence |
|--------|----------------------|---------------------|------------|
| S1 Rapid | ruff | Prettier (safe) / Biome (fast) | High |
| S2 Comprehensive | ruff | Prettier or Biome by need | High |
| S3 Need-Driven | ruff (all use cases) | Prettier (multi-lang) / Biome (JS-only) | High |
| S4 Strategic | ruff (92% viability) | Biome (88%) challenging Prettier (85%) | High |

**Convergence Level**: HIGH (4/4 methodologies align on ruff; JS/TS split by use case)

---

## S1: Rapid Library Search

**Location**: `S1-rapid/`

### Files
- `approach.md` - S1 methodology (88 lines)
- `black.md` - Python formatter (45 lines)
- `ruff.md` - Unified Python tool (64 lines)
- `autopep8.md` - Legacy PEP 8 fixer (52 lines)
- `prettier.md` - JS/TS formatter (64 lines)
- `eslint.md` - JS linter (84 lines)
- `biome.md` - Unified JS/TS tool (88 lines)
- `isort.md` - Import sorting (65 lines)
- `recommendation.md` - Final recommendations (373 lines)

### Key Findings
- **Ruff**: 35K+ stars, 18M+ weekly downloads, 30x faster than Black
- **Prettier**: 49K stars, 45M+ weekly downloads, dominant JS formatter
- **Biome**: 16K+ stars, 97% Prettier compatible, 25x faster
- **Black**: 39K stars, mature but slower, volunteer-maintained

---

## S2: Comprehensive Solution Analysis

**Location**: `S2-comprehensive/`

### Files
- `approach.md` - S2 methodology (141 lines)
- `black.md` - Deep analysis (234 lines)
- `ruff.md` - Deep analysis (328 lines)
- `prettier.md` - Deep analysis (357 lines)
- `biome.md` - Deep analysis (447 lines)
- `eslint.md` - Deep analysis (475 lines)
- `feature-comparison.md` - Matrix comparison (335 lines)
- `performance-benchmarks.md` - Speed data (410 lines)
- `recommendation.md` - Evidence-based guidance (657 lines)

### Performance Benchmarks

| Tool | Speed vs Baseline | Memory | Notes |
|------|------------------|--------|-------|
| **ruff** | 30-100x vs Black | Lower | Rust-based |
| **Biome** | 25x vs Prettier | Lower | Rust-based |
| **Black** | Baseline | Moderate | Python-based |
| **Prettier** | Baseline | Moderate | JavaScript-based |

### Feature Comparison Highlights

| Feature | ruff | Black | Biome | Prettier |
|---------|------|-------|-------|----------|
| Formatting | ✅ | ✅ | ✅ | ✅ |
| Linting | ✅ | ❌ | ✅ | ❌ |
| Import sorting | ✅ | ❌ | ✅ | ❌ |
| pyproject.toml | ✅ | ✅ | N/A | N/A |
| package.json | N/A | N/A | ✅ | ✅ |
| IDE integration | ✅ | ✅ | ✅ | ✅ |

---

## S3: Need-Driven Discovery

**Location**: `S3-need-driven/`

### Files
- `approach.md` - S3 methodology (90 lines)
- `use-case-python-library.md` - Python package dev (120 lines)
- `use-case-fullstack-typescript.md` - Full-stack TS (118 lines)
- `use-case-python-js-monorepo.md` - Mixed monorepo (120 lines)
- `use-case-legacy-migration.md` - Adopting formatters (117 lines)
- `use-case-ci-optimization.md` - Fast CI pipelines (120 lines)
- `migration-paths.md` - Switching tools (112 lines)
- `recommendation.md` - Best-fit solutions (150 lines)

### Use Case Recommendations

| Use Case | Primary Tool | Alternative |
|----------|-------------|-------------|
| Python library | ruff | Black (conservative) |
| Full-stack TypeScript | Prettier + ESLint | Biome |
| Python + JS monorepo | ruff + Prettier | ruff + Biome |
| Legacy migration | Incremental ruff | Incremental Black |
| CI optimization | ruff + Biome | Fastest possible |

### CI Performance Impact

| Stack | Traditional Time | Optimized Time | Savings |
|-------|-----------------|----------------|---------|
| Python (Black + Flake8 + isort) | 60s | 2s (ruff) | 97% |
| JS/TS (Prettier + ESLint) | 45s | 5s (Biome) | 89% |

---

## S4: Strategic Solution Selection

**Location**: `S4-strategic/`

### Files
- `approach.md` - S4 methodology (98 lines)
- `black-viability.md` - 75% survival (146 lines)
- `ruff-viability.md` - 92% survival (170 lines)
- `prettier-viability.md` - 85% survival (172 lines)
- `biome-viability.md` - 88% survival (197 lines)
- `ecosystem-trajectory.md` - 2025-2028 trends (408 lines)
- `recommendation.md` - Strategic guidance (389 lines)

### 3-Year Viability Scores

| Tool | Survival | Trend | Risk Factor |
|------|----------|-------|-------------|
| **ruff** | 92% | 📈 Rising | Young tool, commercial pressure |
| **Biome** | 88% | 📈 Rising | Funding uncertainty |
| **Prettier** | 85% | ➡️ Stable | Speed disadvantage |
| **Black** | 75% | 📉 Declining | No funding, speed disadvantage |

### Ecosystem Trajectory (2025-2028)

1. **Rust rewrites continue** - Performance advantages too significant to ignore
2. **Tool consolidation** - format + lint → single tool (ruff, Biome)
3. **Ruff dominates Python** - 70%+ market share by 2028
4. **Biome challenges Prettier** - Gains share but doesn't replace
5. **Black survives** - PSF backing ensures longevity, but loses share

---

## Decision Framework

### Python Projects

```
All Python Projects → ruff

Why?
- 30-100x faster
- >99.9% Black compatible
- Format + lint + import sort unified
- VC-backed (Astral $4M+)
- Already adopted by FastAPI, pandas, pydantic
```

### JavaScript/TypeScript Projects

```
Performance-critical OR JS/TS-only?
├─ Yes → Biome (25x faster, unified)
└─ No → Prettier + ESLint (mature, best coverage)

Need HTML, YAML, Markdown formatting?
├─ Yes → Prettier (Biome doesn't support these)
└─ No → Either works
```

---

## Total Research Volume

| Phase | Files | Lines |
|-------|-------|-------|
| S1 Rapid | 13 | ~1,100 |
| S2 Comprehensive | 9 | ~3,400 |
| S3 Need-Driven | 8 | ~950 |
| S4 Strategic | 7 | ~1,600 |
| **Total** | **37** | **~7,050** |

---

## Quick Reference: Tool Selection

### New Project Starting Today

| Language | Use This |
|----------|----------|
| Python | `ruff format` + `ruff check` |
| JavaScript/TypeScript | Biome (performance) or Prettier + ESLint (stability) |
| Python + JS monorepo | ruff + Prettier |

### Existing Project Migration

| From | To | Difficulty |
|------|-----|-----------|
| Black → ruff | ruff | Easy (drop-in) |
| Flake8 → ruff | ruff | Easy (config migration) |
| Prettier → Biome | Biome | Medium (97% compatible) |
| ESLint → Biome | Biome | Medium (subset of rules) |

---

## Research Disclaimer

This research is provided for informational purposes only and should not be considered professional advice. Tool capabilities, performance characteristics, and ecosystem dynamics change frequently. No warranty is provided regarding accuracy, completeness, or fitness for a particular purpose.

**Methodology Transparency**: See metadata.yaml for data sources and attribution.

---

**Date compiled**: December 4, 2025
