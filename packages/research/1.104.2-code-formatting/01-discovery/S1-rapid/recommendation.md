# Code Formatting Recommendations by Ecosystem

**Research Date:** December 4, 2025
**Methodology:** S1 Rapid Library Search
**Research Domain:** 1.104.2 Code Formatting

## Executive Summary

The code formatting landscape has consolidated around opinionated, zero-configuration tools. Two major trends define late 2025:

1. **Rust-based unified toolchains** are displacing single-purpose tools (Ruff, Biome)
2. **Performance matters** - 10-100x speedups are driving adoption

**Key Finding:** Ruff is replacing Black + isort + Flake8 in Python. Prettier + ESLint remain dominant in JavaScript/TypeScript, but Biome is emerging for new projects.

---

## Python Ecosystem

### Default Recommendation: **Ruff**

**Why Ruff?**
- 30x faster than Black with >99.9% compatibility
- Unified linting + formatting + import sorting
- Replaces Black, isort, Flake8, pyupgrade, autoflake
- 800+ built-in rules
- Backed by Astral (creators of uv)
- Major adoption: FastAPI, pandas, Apache Airflow, pydantic

**Migration Path:**
```bash
# Replace Black + isort + Flake8
ruff format .  # Black-compatible formatting
ruff check .   # Comprehensive linting
```

**Configuration:** Black-compatible by default. Minimal config needed.

### Alternative: **Black**

**Use Black if:**
- Maximum ecosystem compatibility is critical
- Team is risk-averse about new tools
- Ruff's 0.1% formatting differences matter
- You want the most battle-tested formatter

Black remains a safe choice with 38,000+ stars and adoption across pytest, Django, pandas, and SQLAlchemy. It's mature, stable, and well-understood.

### Legacy Tools to Avoid

**autopep8:** Only fixes PEP 8 violations without enforcing consistency. Use Ruff or Black instead.

**YAPF:** Configurable but slower and less adopted. Black's "uncompromising" philosophy won.

**blue:** Niche Black fork for single quotes. Fragments ecosystem without meaningful benefit.

**isort:** Standalone import sorting is obsolete - use Ruff's integrated import sorting.

---

## JavaScript/TypeScript Ecosystem

### Default Recommendation: **Prettier + ESLint**

**Why Prettier?**
- 55M weekly downloads (dominant standard)
- 97% of projects expect Prettier formatting
- Multi-language: JS/TS/JSX, CSS, HTML, JSON, Markdown, YAML
- Opinionated, zero-config consistency
- Mature IDE integration

**Why ESLint?**
- 63M weekly downloads (linting standard)
- 10+ years of plugin ecosystem maturity
- Type-aware rules via typescript-eslint
- Framework-specific linting (React, Vue, Angular)
- Security and accessibility rules

**Configuration:**
```json
// .eslintrc - Disable formatting rules (let Prettier handle)
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"  // Disables ESLint formatting rules
  ]
}
```

**Division of Labor:**
- **Prettier:** Formatting (whitespace, quotes, semicolons)
- **ESLint:** Code quality (unused vars, bugs, best practices)

### Emerging Alternative: **Biome**

**Consider Biome if:**
- Starting a new project (especially with Vite)
- Performance is critical (6s vs ESLint's 15s)
- Simple linting needs (391 rules sufficient)
- Want unified toolchain (no Prettier + ESLint coordination)

**Don't use Biome if:**
- Need advanced ESLint plugins
- Vue/Angular template linting required
- Complex framework-specific rules
- Team has heavily customized ESLint configs

**Biome Status (Dec 2025):**
- 97% Prettier compatibility
- 391 ESLint-compatible rules
- Type inference (85% of typescript-eslint)
- Growing but not mature plugin ecosystem

### Niche Performance Tool: **dprint**

**Consider dprint only if:**
- Prettier takes 10+ seconds on your codebase
- Pre-commit hooks are painfully slow
- You're building Rust-based toolchain

**Reality check:** Prettier's 2-3 seconds is adequate for 95% of projects. dprint's 20-60x speedup rarely justifies adoption friction.

---

## Decision Matrix

### Python Projects

| Scenario | Recommendation | Rationale |
|----------|---------------|-----------|
| New project | **Ruff** | Unified tooling, speed, modern default |
| Existing Black setup | **Ruff** | Drop-in replacement, massive speedup |
| Risk-averse team | **Black** | Maximum stability and compatibility |
| Legacy codebase | **Black** → **Ruff** | Migrate incrementally |
| Single quote preference | **Blue** (reluctantly) | Use Ruff/Black unless non-negotiable |

### JavaScript/TypeScript Projects

| Scenario | Recommendation | Rationale |
|----------|---------------|-----------|
| New project (standard) | **Prettier + ESLint** | Ecosystem standard, mature plugins |
| New project (Vite) | **Biome** (consider) | Performance, simplicity, growing fast |
| Existing project | **Prettier + ESLint** | Don't fix what works |
| Large monorepo (slow) | **Biome** (evaluate) | Performance matters at scale |
| Complex linting | **Prettier + ESLint** | Plugin ecosystem irreplaceable |
| Performance crisis | **dprint** (last resort) | Only if Prettier is genuine bottleneck |

---

## Cross-Language Considerations

### Monorepo with Python + JavaScript/TypeScript

**Recommended Stack:**
```
Python: Ruff (format + lint)
JS/TS:  Prettier (format) + ESLint (lint)
```

**Alternative (performance-focused):**
```
Python: Ruff (format + lint)
JS/TS:  Biome (format + lint)
```

### CI/CD Pipeline Optimization

**Speed matters in CI:**
- Use Ruff for Python (0.4s vs Black's ~3s)
- Consider Biome for JS/TS (6s vs 15s with ESLint)
- Pre-commit hooks benefit from incremental formatting

**Caching Strategy:**
```yaml
# GitHub Actions - Cache formatter dependencies
- uses: actions/cache@v3
  with:
    path: ~/.cache/ruff
    key: ruff-${{ hashFiles('**/pyproject.toml') }}
```

---

## The "Is Ruff Replacing Black?" Question

**Answer: Yes, increasingly.**

**Evidence:**
- Major projects migrated: FastAPI, pandas, Apache Airflow, pydantic
- Pylint uses Ruff as pre-commit hook
- Astral backing (uv creators) ensures long-term support
- >99.9% Black compatibility eliminates risk
- 30x speed improvement is compelling

**Timeline:**
- **2024:** Ruff gains formatter capability
- **2025:** Rapid adoption across major projects
- **2026 (projected):** Ruff becomes default for new Python projects

**Black's Future:**
Black isn't going away - it remains maintained and widely used. But Ruff represents the next generation: Rust-based, unified, and dramatically faster.

**Recommendation:** Use Ruff for new projects. Migrate existing Black setups when convenient.

---

## The "Is Biome Replacing Prettier + ESLint?" Question

**Answer: Not yet, but momentum building.**

**Evidence for Biome:**
- 97% Prettier compatibility
- 391 ESLint-compatible rules
- Significant performance improvements
- Strong with modern tooling (Vite)
- Type inference without TSC overhead

**Evidence against Biome:**
- Prettier + ESLint have 10+ years of maturity
- Plugin ecosystem gap remains significant
- Framework support (Vue, Angular) incomplete
- Most projects "good enough" with current tools

**Timeline:**
- **2024:** Biome v2.0 adds type inference
- **2025:** Growing adoption in new projects
- **2026+ (projected):** Biome matures, plugin gap narrows

**Recommendation:** Watch Biome closely. Consider for new projects with simple needs. Stick with Prettier + ESLint for complex requirements.

---

## Configuration Examples

### Python with Ruff

```toml
# pyproject.toml
[tool.ruff]
line-length = 88  # Black default
target-version = "py311"

[tool.ruff.format]
quote-style = "double"  # Black-compatible
indent-style = "space"

[tool.ruff.lint]
select = ["E", "F", "I"]  # pycodestyle, Pyflakes, isort
ignore = ["E501"]  # Line too long (formatter handles)

# Pre-commit
[tool.ruff]
extend-exclude = ["migrations", "snapshots"]
```

### JavaScript/TypeScript with Prettier + ESLint

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2,
  "trailingComma": "es5"
}

// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "plugins": ["@typescript-eslint"],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "project": "./tsconfig.json"
  }
}
```

### JavaScript/TypeScript with Biome

```json
// biome.json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "semicolons": "always"
    }
  }
}
```

---

## Final Recommendations by Team Size

### Solo Developer / Small Team (1-5 people)

**Python:** Ruff (simplicity + speed)
**JS/TS:** Prettier + ESLint (or Biome for simple projects)

**Rationale:** Minimize tool complexity, maximize consistency.

### Medium Team (5-20 people)

**Python:** Ruff (eliminate debate, enforce consistency)
**JS/TS:** Prettier + ESLint (mature ecosystem, predictable)

**Rationale:** Team coordination benefits from opinionated defaults.

### Large Team / Enterprise (20+ people)

**Python:** Ruff (speed critical in CI/CD at scale)
**JS/TS:** Prettier + ESLint (unless performance is bottleneck)

**Rationale:** Established tools reduce onboarding friction. Performance matters in large repos.

---

## Migration Strategies

### Black → Ruff

1. Install Ruff: `uv add --dev ruff`
2. Format codebase: `ruff format .`
3. Compare diff with Black: `black . --check`
4. Review differences (<0.1% of lines)
5. Update CI/CD configs
6. Remove Black, isort, Flake8

**Risk:** Minimal. >99.9% compatibility.

### Prettier + ESLint → Biome

1. Install Biome: `npm install --save-dev @biomejs/biome`
2. Initialize config: `npx @biomejs/biome init`
3. Migrate rules from ESLint (manual review)
4. Test on subset of files
5. Compare output with Prettier
6. Full codebase migration
7. Update CI/CD configs

**Risk:** Moderate. Plugin gaps may require keeping ESLint.

---

## Conclusion

**Python (2025):** Ruff is the modern default, replacing Black + isort + Flake8 with unified, blazing-fast tooling.

**JavaScript/TypeScript (2025):** Prettier + ESLint remain standard, but Biome is viable for new projects prioritizing simplicity and speed.

**The Pattern:** Rust-based unified toolchains are winning. Performance + simplicity + zero-config = developer joy.

**Safe Defaults:**
- Python: **Ruff**
- JavaScript/TypeScript: **Prettier + ESLint**
- Performance-critical JS/TS: **Biome**
