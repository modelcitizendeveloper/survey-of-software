# Code Formatting Tool Recommendations: Evidence-Based Selection Guide

## Overview

This guide provides evidence-based recommendations for selecting code formatting and linting tools based on project characteristics, team priorities, and ecosystem constraints. Recommendations synthesize performance benchmarks, feature comparisons, and real-world migration experiences.

## Quick Decision Matrix

### Python Projects

| Project Type | Recommended | Alternative | Rationale |
|-------------|-------------|-------------|-----------|
| **New project** | Ruff (format + lint) | Black + Ruff lint | Unified, fastest, modern |
| **Existing (Black)** | Migrate to Ruff | Keep Black + Ruff lint | >99.9% compatible, huge speedup |
| **Large monorepo** | Ruff (format + lint) | Ruff only | Performance critical |
| **Conservative org** | Black + Ruff lint | Black + Flake8 | Battle-tested stability |
| **Custom style guide** | YAPF + Ruff lint | autopep8 | Configurability needed |
| **Small script** | Black | Ruff | Simplicity over speed |

### JavaScript/TypeScript Projects

| Project Type | Recommended | Alternative | Rationale |
|-------------|-------------|-------------|-----------|
| **New project** | Biome (format + lint) | Prettier + ESLint | Unified, 25x faster |
| **Existing (Prettier)** | Keep Prettier + ESLint | Migrate to Biome | Stability vs. performance |
| **Large monorepo** | Biome (format + lint) | Prettier + ESLint | 26x faster quality checks |
| **Multi-language** | Prettier + ESLint | Biome + Prettier | Prettier for HTML/YAML/Markdown |
| **JS/TS only** | Biome | Prettier + ESLint | Simplicity + speed |
| **Custom ESLint plugins** | Prettier + ESLint | Biome + ESLint | Plugin ecosystem needed |

## Detailed Recommendations

### Python: The Ruff vs. Black Decision

#### Choose Ruff Format + Ruff Check (Unified) If:

**Performance is a priority:**
- Large codebase (>100k lines)
- Frequent commits (>50/day/team)
- Slow CI pipelines (quality checks >30s)
- Pre-commit hooks feel sluggish

**Simplicity is valued:**
- New project without legacy constraints
- Desire to reduce tool count (5 tools → 1)
- Team wants unified configuration
- Simplified dependency management

**Modern tooling preferred:**
- Team comfortable with newer tools
- Willing to adopt actively developed projects
- Value Rust-based performance

**Migration effort acceptable:**
- Expected impact: <0.1% line changes from Black
- Compatible with >99.9% of Black output
- Easy rollback if needed

**Practical Example:**
```toml
# pyproject.toml - Single unified config
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "C4"]
ignore = ["E501"]  # Line length handled by formatter

[tool.ruff.format]
quote-style = "double"
```

**Commands:**
```bash
# Format and lint in one go
ruff check --fix . && ruff format .

# Or use pre-commit
ruff check --fix . ; ruff format .
```

#### Choose Black + Ruff Check (Hybrid) If:

**Stability is paramount:**
- Conservative organization
- Risk-averse team culture
- Prefer 7+ year battle-tested tools
- Existing Black formatting satisfactory

**100% Black compatibility required:**
- Zero tolerance for formatting differences
- Large existing codebase reviewed and approved
- Legal/compliance requirements for minimal changes

**Gradual migration preferred:**
- Phase 1: Keep Black, add Ruff linter
- Phase 2: Evaluate Ruff formatter on branches
- Phase 3: Switch after team approval

**Practical Example:**
```toml
# pyproject.toml - Hybrid approach
[tool.black]
line-length = 88
target-version = ['py311']

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
# Exclude formatting rules (Black handles those)
ignore = ["E501"]
```

**Commands:**
```bash
# Format with Black
black .

# Lint with Ruff
ruff check --fix .
```

#### Avoid Black + Flake8 + isort (Traditional Stack) Unless:

**Specific plugins required:**
- Custom Flake8 plugins not in Ruff
- Company-specific linting rules

**Team resistance to change:**
- Team familiar with existing tools
- No performance pain points
- "If it ain't broke, don't fix it" culture

**Note:** This stack is 53x slower than unified Ruff. Strongly consider migration.

### JavaScript/TypeScript: The Biome vs. Prettier Decision

#### Choose Biome (Format + Lint) If:

**Performance is critical:**
- Large monorepo (>100k lines)
- Slow pre-commit hooks (>2s)
- CI pipelines taking minutes for quality checks
- Many developers committing frequently

**Unified tooling desired:**
- Prefer single tool over Prettier + ESLint
- Simplified configuration
- Faster onboarding for new developers

**Primary languages are JS/TS:**
- Project is >90% JavaScript/TypeScript/JSON/CSS
- Don't need HTML/YAML/Markdown formatting
- Can use Prettier for auxiliary files if needed

**ESLint rule coverage sufficient:**
- Biome's ~200 rules cover your needs
- No custom ESLint plugins required
- Standard React/TypeScript project

**Migration acceptable:**
- ~97% Prettier compatibility
- Migration tools available
- Team willing to review differences

**Practical Example:**
```json
// biome.json - Unified config
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "es5"
    }
  }
}
```

**Commands:**
```bash
# Format and lint together
biome check --write .

# CI check (no modifications)
biome ci .
```

#### Choose Prettier + ESLint (Separate) If:

**Multi-language project:**
- Need HTML, YAML, Markdown formatting
- Using Vue, Svelte with templates
- GraphQL queries need formatting

**Maximum ESLint ecosystem needed:**
- Custom company/team ESLint plugins
- Framework-specific rules (Angular, Ember)
- Specific third-party plugins essential

**Stability over speed:**
- Team prefers 8-year battle-tested tools
- Performance adequate for project size
- Risk-averse organization

**Complex ESLint configurations:**
- Dynamic JavaScript configs (environment-based)
- Per-file overrides extensively used
- Cannot convert to JSON-based config

**Practical Example:**
```json
// .prettierrc
{
  "printWidth": 100,
  "singleQuote": true,
  "trailingComma": "es5"
}

// eslint.config.js (ESLint 9 flat config)
import js from '@eslint/js';
import typescript from '@typescript-eslint/eslint-plugin';
import prettier from 'eslint-config-prettier';

export default [
  js.configs.recommended,
  {
    files: ['**/*.ts', '**/*.tsx'],
    plugins: { '@typescript-eslint': typescript },
    rules: {
      '@typescript-eslint/no-unused-vars': 'error'
    }
  },
  prettier // Disable conflicting rules
];
```

**Commands:**
```bash
# Format first, then lint
prettier --write . && eslint --fix .
```

#### Hybrid Approach: Biome + Prettier If:

**Best of both worlds:**
- Use Biome for JS/TS formatting + linting (fast)
- Use Prettier for HTML/Markdown/YAML (coverage)
- Separate concerns cleanly

**Practical Example:**
```json
// package.json scripts
{
  "scripts": {
    "format:js": "biome format --write .",
    "format:other": "prettier --write '**/*.{html,md,yml}'",
    "format": "npm run format:js && npm run format:other",
    "lint": "biome lint --write ."
  }
}
```

## Migration Strategies

### Python: Black → Ruff Format

**Phase 1: Assessment (1-2 hours)**
1. Run Ruff on codebase to see differences:
   ```bash
   ruff format --diff . | wc -l
   ```
2. Review changes (expect <0.1% lines affected)
3. Identify any problematic differences

**Phase 2: Parallel Testing (1 week)**
1. Add Ruff to CI alongside Black (don't block)
2. Monitor differences on new PRs
3. Gather team feedback

**Phase 3: Migration (1 day)**
1. Create migration branch
2. Run Ruff format:
   ```bash
   ruff format .
   ```
3. Commit with message: "Migrate to Ruff formatter (Black-compatible)"
4. Update CI/pre-commit configs
5. Remove Black dependency

**Phase 4: Rollback Plan**
Keep Black config for 1-2 sprints:
```bash
# If issues arise, revert:
git revert <ruff-commit>
black .
```

**Expected Impact:**
- Time: 2-4 hours total effort
- Code changes: <0.1% of lines
- Performance gain: 30-100x faster formatting

### JavaScript: Prettier + ESLint → Biome

**Phase 1: Assessment (2-3 hours)**
1. Use Biome migration tools:
   ```bash
   npx @biomejs/biome migrate prettier --write
   npx @biomejs/biome migrate eslint --write
   ```
2. Review generated `biome.json`
3. Test formatting differences:
   ```bash
   biome format --write .
   git diff --stat
   ```
4. Identify ESLint rules not covered by Biome

**Phase 2: Gradual Adoption (2-4 weeks)**
1. Use Biome on new modules/features
2. Keep Prettier + ESLint on existing code
3. Compare performance and ergonomics

**Phase 3: Full Migration (1-2 days)**
1. Run Biome across entire codebase
2. Address unmapped ESLint rules:
   - Accept Biome equivalents
   - Or keep ESLint for specific rules
3. Update CI/pre-commit configs
4. Remove Prettier, potentially keep ESLint

**Phase 4: Hybrid (if needed)**
If some ESLint rules essential:
```json
{
  "scripts": {
    "format": "biome format --write .",
    "lint": "biome lint --write . && eslint --fix ."
  }
}
```

**Expected Impact:**
- Time: 1-2 days total effort
- Code changes: ~3% of lines (mostly minor)
- Performance gain: 25x faster formatting, 15x faster linting

## Team Size Considerations

### Small Team (1-5 developers)

**Python:**
- Recommended: Ruff (format + lint)
- Rationale: Simplicity, minimal config, fast

**JavaScript:**
- Recommended: Biome or Prettier + ESLint
- Rationale: Either works, choose based on multi-language needs

**Priority:** Developer experience, simplicity

### Medium Team (5-20 developers)

**Python:**
- Recommended: Ruff (format + lint) or Black + Ruff lint
- Rationale: Performance starts mattering, unified tooling helps onboarding

**JavaScript:**
- Recommended: Biome (fast) or Prettier + ESLint (stable)
- Rationale: Pre-commit hooks noticeable, choose based on stability vs. speed

**Priority:** Balance performance and stability

### Large Team (20+ developers)

**Python:**
- Strongly recommended: Ruff (format + lint)
- Rationale: Performance critical, CI costs add up, unified reduces confusion

**JavaScript:**
- Strongly recommended: Biome
- Rationale: 25x speedup × many developers = major productivity gain

**Priority:** Performance, CI cost reduction, consistency

## Codebase Size Considerations

### Small (<10k lines)

**Python:** Black or Ruff (either fine)
**JavaScript:** Prettier or Biome (either fine)
**Rationale:** Performance differences imperceptible

### Medium (10k-100k lines)

**Python:** Ruff preferred (noticeable speed gain)
**JavaScript:** Biome preferred (pre-commit hooks faster)
**Rationale:** Performance improvements felt by developers

### Large (100k-500k lines)

**Python:** Ruff strongly recommended (30x faster)
**JavaScript:** Biome strongly recommended (25x faster)
**Rationale:** Traditional tools become painfully slow

### Extra Large (>500k lines)

**Python:** Ruff essential (traditional tools impractical)
**JavaScript:** Biome essential (Prettier takes minutes)
**Rationale:** Performance differences are transformative

## Industry and Domain Considerations

### Startups and Fast-Moving Teams

**Recommendation:** Modern, fast tools (Ruff, Biome)
**Rationale:**
- Speed to market prioritized
- Less legacy constraint
- Developer productivity critical
- Willing to adopt new tools

### Enterprise and Regulated Industries

**Recommendation:** Stable, battle-tested tools (Black, Prettier + ESLint)
**Rationale:**
- Risk aversion
- Compliance requirements
- Change management overhead
- Extensive existing codebases

**Alternative:** Ruff/Biome with extended evaluation period

### Open Source Projects

**Python:**
- Recommendation: Ruff (if started recently) or Black (established standard)
- Rationale: Community familiarity, easy contributor setup

**JavaScript:**
- Recommendation: Prettier + ESLint (universal recognition)
- Rationale: Maximum contributor compatibility

### Consulting/Agencies (Multi-Client)

**Recommendation:** Flexible, client-matching tools
**Python:** Maintain both Black and Ruff capabilities
**JavaScript:** Maintain both Prettier+ESLint and Biome
**Rationale:** Adapt to client preferences, demonstrate modern options

## Continuous Integration Considerations

### CI Performance Critical (High Commit Frequency)

**Python:** Ruff (53x faster than traditional stack)
**JavaScript:** Biome (26x faster than Prettier + ESLint)
**Rationale:** Multiply per-check time × commits/day × cost/minute

### CI Performance Acceptable

**Python:** Black + Ruff lint or Ruff
**JavaScript:** Prettier + ESLint or Biome
**Rationale:** Flexibility to choose based on other factors

### Cost-Optimized CI

**Python:** Ruff (fewer dependencies, faster setup)
**JavaScript:** Biome (fewer dependencies, faster setup)
**Rationale:** Reduce runner time, dependency installation time

## Special Scenarios

### Jupyter Notebook Formatting

**Recommendation:** Ruff or Black (both support notebooks)
**Tools:**
- Ruff: Built-in support via `ruff format`
- Black: Via `black-jupyter` or `nbqa`

### Monorepos with Multiple Languages

**Recommendation:** Language-specific tools
**Python + JavaScript:**
- Use Ruff for Python
- Use Biome for JavaScript
- Use Prettier for shared formats (Markdown, YAML)

**Alternative:** Single tool where overlap
- Prettier for JS + JSON + Markdown + YAML
- Ruff for Python only

### CI/CD Pipelines (Quality Gates)

**Recommendation:**
- Use `--check` modes (no modifications)
- Fail builds on formatting violations
- Separate formatting check from linting

**Python:**
```bash
ruff format --check .
ruff check .
```

**JavaScript:**
```bash
biome ci .
# or
prettier --check . && eslint .
```

### Pre-commit Hooks (Developer Experience)

**Priority:** Speed above all
**Python:** Ruff (instant feedback)
**JavaScript:** Biome or dprint (instant feedback)

**Avoid:** Slow tools in pre-commit (frustrates developers)

## Technology Stack Integration

### Django Projects

**Recommendation:** Ruff (format + lint)
**Specific Config:**
```toml
[tool.ruff.lint]
select = ["E", "F", "I", "DJ"]  # DJ = Django-specific rules
```

### FastAPI Projects

**Recommendation:** Ruff (format + lint)
**Rationale:** FastAPI itself uses Ruff

### React Projects

**Recommendation:** Biome (format + lint)
**Specific Config:**
```json
{
  "linter": {
    "rules": {
      "recommended": true,
      "a11y": {
        "recommended": true
      }
    }
  }
}
```

### Next.js Projects

**Recommendation:** Prettier + ESLint (Next.js bundles ESLint config)
**Alternative:** Biome (faster, but requires manual Next.js rule mapping)

### TypeScript Strict Projects

**Recommendation:** Prettier + @typescript-eslint (comprehensive rules)
**Alternative:** Biome (faster, growing type-aware rules)

## Decision Tree Summary

### Python Decision Tree

```
Start
├─ New project?
│  └─ YES → Ruff (format + lint)
├─ Large codebase (>100k lines)?
│  └─ YES → Ruff (performance critical)
├─ Conservative organization?
│  └─ YES → Black + Ruff lint
├─ Custom style guide needed?
│  └─ YES → YAPF + Ruff lint
└─ Default → Ruff (format + lint)
```

### JavaScript Decision Tree

```
Start
├─ New project AND JS/TS only?
│  └─ YES → Biome
├─ Multi-language (HTML/YAML/Markdown)?
│  └─ YES → Prettier + ESLint
├─ Large monorepo (>100k lines)?
│  └─ YES → Biome (performance)
├─ Custom ESLint plugins required?
│  └─ YES → Prettier + ESLint
└─ Default → Biome OR Prettier + ESLint
```

## Final Recommendations

### 2025 Default Stack

**Python:**
- **Formatting:** Ruff
- **Linting:** Ruff
- **Import Sorting:** Ruff
- **Why:** Unified, 30-100x faster, battle-tested by major projects

**JavaScript/TypeScript:**
- **Formatting:** Biome OR Prettier
- **Linting:** Biome OR ESLint
- **Why:** Biome for speed (new projects), Prettier + ESLint for stability

### Conservative Stack (Maximum Stability)

**Python:**
- **Formatting:** Black
- **Linting:** Ruff (or Flake8 if needed)
- **Import Sorting:** Ruff (or isort)

**JavaScript/TypeScript:**
- **Formatting:** Prettier
- **Linting:** ESLint

### Performance-Optimized Stack (Large Codebases)

**Python:** Ruff (everything)
**JavaScript:** Biome (everything)

## Conclusion

The code formatting landscape in 2025 is defined by a clear trend: **Rust-based, unified toolchains** (Ruff, Biome) offer transformative performance improvements (30-100x) while maintaining compatibility with established standards (Black, Prettier).

**Key Takeaway:**
- **New projects:** Use modern tools (Ruff, Biome)
- **Existing projects:** Migrate if performance matters
- **Conservative teams:** Hybrid approaches work well (Black + Ruff lint)
- **No wrong choice:** All tools in this analysis are production-ready

**The shift is clear:** By 2025, Ruff has become the default for Python, and Biome is rapidly becoming the default for JavaScript/TypeScript. However, Black and Prettier remain excellent choices for stability-focused teams.

Choose based on your priorities: **speed vs. stability, unified vs. specialized, modern vs. proven.**
