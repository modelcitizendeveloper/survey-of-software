# S3 Need-Driven Recommendations: Code Formatting Tools

## Executive Summary

This document provides best-fit code formatting solutions matched to specific development workflow requirements, based on comprehensive need-driven analysis.

## Quick Decision Matrix

| Use Case | Primary Tool | Rationale | Setup Time |
|----------|-------------|-----------|------------|
| Python Library | Ruff Format | Speed, ecosystem compatibility | 30 min |
| TypeScript Full-Stack | Prettier | Universal adoption, zero-config | 20 min |
| Python + JS Monorepo | Ruff + Prettier | Best-in-class per language | 45 min |
| Legacy Migration | Ruff/Prettier | Incremental adoption support | 2-4 weeks |
| CI Optimization | Ruff + Biome | Maximum performance | 1 hour |

## Detailed Recommendations by Use Case

### 1. Python Library/Package Development

**Recommended Solution: Ruff Format**

**Primary Requirements Met:**
- Fast local formatting (10-100x faster than Black)
- PEP 8 compliance and ecosystem standards
- Zero-config opinionated defaults
- Excellent CI/CD performance

**Configuration:**
```toml
[tool.ruff]
line-length = 88
target-version = "py38"

[tool.ruff.format]
quote-style = "double"
```

**Pre-commit:**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff-format
```

**CI Example:**
```yaml
- run: uvx ruff format --check .
```

**Alternative: Black**
- Choose if maximum ecosystem compatibility is critical
- 5+ years of stability and proven adoption
- Slightly slower but battle-tested

**When to Choose Alternative:**
- Team strongly prefers established tooling
- Existing Black configuration works well
- No performance concerns in current workflow

**Success Metrics:**
- CI formatting check < 10 seconds
- Zero formatting PR debates
- Onboarding new contributors < 15 minutes

---

### 2. Full-Stack TypeScript Application

**Recommended Solution: Prettier**

**Primary Requirements Met:**
- Comprehensive language support (JS, TS, JSX, JSON, CSS, Markdown)
- Zero-config opinionated formatting
- Universal editor integration
- Massive ecosystem and plugin support

**Configuration:**
```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "es5"
}
```

**Pre-commit:**
```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
```

**CI Example:**
```yaml
- run: npm ci && npm run format:check
```

**Complementary: ESLint with eslint-config-prettier**
- ESLint handles code quality and logic rules
- Prettier handles formatting
- `eslint-config-prettier` prevents conflicts

**Alternative: Biome**
- Choose for performance-critical scenarios
- 10-35x faster than Prettier
- 95%+ output compatible
- Growing but smaller ecosystem

**When to Choose Alternative:**
- Large codebase (100k+ lines)
- CI performance is bottleneck
- Willing to adopt newer tooling
- Monorepo with many packages

**Success Metrics:**
- Format-on-save < 200ms
- CI check < 30 seconds
- 100% team uses consistent editor config

---

### 3. Python + JavaScript Monorepo

**Recommended Solution: Ruff Format + Prettier + pre-commit**

**Primary Requirements Met:**
- Best-in-class per-language formatting
- Unified orchestration via pre-commit
- No tool overlap or conflicts
- Excellent performance across languages

**Configuration:**

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff-format
        files: ^backend/

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx]
        files: ^frontend/
```

**CI Example:**
```yaml
jobs:
  format-python:
    runs-on: ubuntu-latest
    steps:
      - run: uvx ruff format --check backend/

  format-js:
    runs-on: ubuntu-latest
    steps:
      - run: npx prettier --check "frontend/**/*.{js,jsx,ts,tsx}"
```

**Key Benefits:**
- Single pre-commit command formats all languages
- Parallel execution in CI
- Clear separation of concerns
- No cross-language conflicts

**Alternative: Biome + Ruff (Performance-First)**
- Replace Prettier with Biome for JavaScript
- 10x+ overall speedup
- Smaller ecosystem for Biome

**When to Choose Alternative:**
- CI performance is critical
- Very large codebase
- Team comfortable with newer tools

**Success Metrics:**
- Single command formats entire monorepo
- CI checks < 60 seconds
- No cross-language conflicts
- Onboarding < 30 minutes

---

### 4. Legacy Codebase Migration

**Recommended Solution: Ruff Format or Prettier with Incremental Adoption**

**Primary Requirements Met:**
- Gradual migration without disruption
- Git blame history preservation
- Minimal merge conflicts
- Flexible enforcement timeline

**Migration Strategy:**

**Phase 1: Setup (Week 1)**
```yaml
# Pre-commit with manual stage
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff-format
        stages: [manual]
```

**Phase 2: New Code Only (Week 2)**
```yaml
# Auto-format on commit
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff-format
        stages: [commit]
```

**Phase 3: Module-by-Module (Week 3-4)**
```bash
# Format specific modules
ruff format backend/auth/
git add backend/auth/
git commit -m "Format auth module with Ruff"
git rev-parse HEAD >> .git-blame-ignore-revs
```

**Phase 4: Full Enforcement**
```yaml
# Check mode prevents unformatted commits
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff-format
        args: [--check]
```

**Git Blame Protection:**
```bash
# .git-blame-ignore-revs
a1b2c3d4  # Format auth module - 2025-01-15
b2c3d4e5  # Format api module - 2025-01-22

# Configure git
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

**Alternative: Big Bang Migration**
- Choose only for small codebases (< 10k lines)
- Or single developer projects
- Or when clean history not critical

**Success Metrics:**
- Migration completed without major conflicts
- Git blame remains useful
- < 5% team needs formatting help after Week 2
- Development velocity maintained

---

### 5. CI/CD Pipeline Optimization

**Recommended Solution: Ruff + Biome with Aggressive Caching**

**Primary Requirements Met:**
- Sub-30 second formatting checks
- Efficient caching and incremental checks
- Minimal resource usage
- Fast feedback on PRs

**Configuration:**

**Ruff with Caching:**
```yaml
- name: Set up Ruff cache
  uses: actions/cache@v4
  with:
    path: .ruff_cache
    key: ruff-${{ runner.os }}-${{ hashFiles('pyproject.toml') }}

- name: Check formatting
  run: ruff format --check .
```

**Changed Files Only:**
```yaml
- uses: tj-actions/changed-files@v44
  id: changed
  with:
    files: "**/*.py"

- if: steps.changed.outputs.any_changed == 'true'
  run: |
    echo "${{ steps.changed.outputs.all_changed_files }}" | \
      xargs ruff format --check
```

**Parallel Language Checks:**
```yaml
jobs:
  format-python:
    runs-on: ubuntu-latest
    steps:
      - run: ruff format --check backend/

  format-js:
    runs-on: ubuntu-latest
    steps:
      - run: biome format --check frontend/
```

**Performance Benchmarks:**

| Approach | Typical Time | Cache Hit Rate |
|----------|-------------|----------------|
| Ruff (all files, cached) | 3s | 95% |
| Ruff (changed only) | 0.5s | 98% |
| Black (all files, cached) | 35s | 80% |
| Prettier (all files) | 15s | 85% |
| Biome (all files) | 2s | 90% |

**Key Optimizations:**
1. Tool selection (Ruff, Biome)
2. Intelligent caching
3. Changed files only
4. Parallel execution
5. Fail-fast configuration

**Alternative: Prettier (JavaScript)**
- Use if Biome ecosystem not mature enough
- Add `--cache` flag for performance
- Still significantly faster than other JS formatters

**Success Metrics:**
- CI formatting check < 10 seconds for typical PRs
- 95%+ cache hit rate
- Developer feedback time < 2 minutes total
- 90%+ reduction in CI time vs. legacy approach

---

## Comparison Matrix

### Performance

| Tool | Speed (relative) | Cache Support | Binary Size | Language |
|------|-----------------|---------------|-------------|----------|
| Ruff | 100x | Excellent | 5MB | Python |
| Black | 1x | Good | 1MB + deps | Python |
| Biome | 35x | Excellent | 30MB | JS/TS |
| Prettier | 1x | Good | varies | JS/TS/etc |

### Features

| Tool | Opinionated | Config Depth | Ecosystem | Maturity |
|------|------------|--------------|-----------|----------|
| Ruff | Yes | Low | Growing | 2+ years |
| Black | Yes | Very Low | Mature | 5+ years |
| Biome | Yes | Medium | Growing | 2+ years |
| Prettier | Yes | Low | Mature | 7+ years |

### Integration

| Tool | Pre-commit | CI/CD | Editor | Git Hooks |
|------|-----------|-------|--------|-----------|
| Ruff | Excellent | Excellent | Excellent | Excellent |
| Black | Excellent | Excellent | Excellent | Excellent |
| Biome | Good | Excellent | Good | Good |
| Prettier | Excellent | Excellent | Excellent | Excellent |

## Anti-Recommendations

### What NOT to Do

**1. Multiple Formatters on Same Files**
- Don't run Black and YAPF on same Python files
- Don't run Prettier and Biome on same JavaScript files
- Causes conflicts and confusion

**2. Over-Configuration**
- Don't customize every formatting rule
- Defeats purpose of opinionated formatters
- Creates maintenance burden

**3. Optional Formatting**
- Don't make formatting optional in CI
- Creates style debates and PR friction
- Enforcement must be mandatory

**4. Ignoring Performance**
- Don't use slow formatters in CI without caching
- Wastes developer time and CI resources
- Modern tools (Ruff, Biome) are 10-100x faster

**5. No Migration Plan**
- Don't introduce formatters without strategy
- Causes merge conflicts and resistance
- Plan incremental adoption for legacy code

## Decision Framework

### Step 1: Identify Primary Language(s)
- Python only → Ruff Format
- JavaScript/TypeScript only → Prettier (or Biome for performance)
- Multi-language → Per-language tools + pre-commit

### Step 2: Evaluate Performance Needs
- CI time critical → Ruff, Biome
- CI time acceptable → Black, Prettier
- Large codebase → Prioritize speed

### Step 3: Assess Team Readiness
- New team → Opinionated defaults (Black, Prettier)
- Experienced team → Modern tools (Ruff, Biome)
- Legacy codebase → Incremental migration strategy

### Step 4: Consider Ecosystem Maturity
- Need maximum stability → Black, Prettier
- Want modern performance → Ruff, Biome
- Require specific plugins → Check ecosystem

### Step 5: Validate Requirements
- Run pilot on sample code
- Measure performance metrics
- Gather team feedback
- Iterate configuration

### Step 6: Execute Rollout
- Document decisions
- Prepare migration guide
- Enable enforcement
- Monitor and adjust

## Tooling Combinations

### Recommended Combinations

**Python Project:**
- Formatter: Ruff Format
- Linter: Ruff
- Pre-commit: ruff-pre-commit
- CI: GitHub Actions + Ruff

**JavaScript Project:**
- Formatter: Prettier
- Linter: ESLint + eslint-config-prettier
- Pre-commit: pre-commit or husky + lint-staged
- CI: GitHub Actions + Prettier

**Python + JavaScript Monorepo:**
- Formatter: Ruff + Prettier
- Orchestration: pre-commit
- CI: Parallel jobs per language

**Performance-Critical:**
- Formatter: Ruff + Biome
- Cache: Aggressive caching strategy
- CI: Changed files only + parallel execution

## Future Considerations

### Emerging Tools (Watch List)

**Biome (JavaScript/TypeScript):**
- Rapid development and adoption
- Potential Prettier replacement
- Monitor for production readiness

**Ruff (Python):**
- Already production-ready
- Continuing to add features
- Strong momentum toward becoming standard

**dprint (Multi-language):**
- Performance-focused formatter
- Growing language support
- Consider for specific use cases

### Stability Expectations

**Mature (5+ years):**
- Black: Stable, minimal changes expected
- Prettier: Stable, incremental improvements

**Growing (2-3 years):**
- Ruff: Rapid feature additions, stabilizing
- Biome: Active development, API changes possible

**Emerging (< 2 years):**
- Evaluate carefully before production adoption
- Monitor issue trackers and release notes
- Plan for potential breaking changes

## Summary Recommendations

### Choose Ruff Format if:
- Python codebase
- Performance matters
- Want unified linting + formatting
- Comfortable with modern tooling

### Choose Black if:
- Python codebase
- Maximum stability critical
- Need proven track record
- Performance acceptable

### Choose Prettier if:
- JavaScript/TypeScript codebase
- Need comprehensive language support
- Want universal ecosystem adoption
- Value zero-config experience

### Choose Biome if:
- JavaScript/TypeScript codebase
- Performance critical
- Want unified linting + formatting
- Comfortable with newer tooling

### Choose pre-commit if:
- Multi-language project
- Need unified hook framework
- Want flexible orchestration
- Standardized across team

## Date Compiled
December 4, 2025
