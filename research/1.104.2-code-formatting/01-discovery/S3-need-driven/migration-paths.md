# Migration Paths Between Code Formatters

## Overview

Strategic guidance for migrating between code formatting tools, including compatibility considerations, automation strategies, and rollback procedures.

## Migration Scenarios

### Python Formatters

#### Black → Ruff Format

**Compatibility:** 99.9% output compatible

**Rationale:**
- 10-100x performance improvement
- Unified linting + formatting
- Drop-in Black replacement
- Active development and ecosystem growth

**Migration Steps:**

1. **Verify Compatibility**
```bash
# Format with Black
black --check .

# Format with Ruff (should be identical)
ruff format --check .
```

2. **Update Configuration**

Before (`pyproject.toml`):
```toml
[tool.black]
line-length = 88
target-version = ['py38']
```

After:
```toml
[tool.ruff]
line-length = 88
target-version = "py38"

[tool.ruff.format]
# Additional options if needed
quote-style = "double"
```

3. **Update Pre-commit**

Before:
```yaml
- repo: https://github.com/psf/black
  rev: 24.10.0
  hooks:
    - id: black
```

After:
```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.7.4
  hooks:
    - id: ruff-format
```

4. **Update CI**
```yaml
# Before
- run: pip install black && black --check .

# After
- run: pip install ruff && ruff format --check .
```

5. **Update Dependencies**
```bash
# Remove Black
pip uninstall black

# Install Ruff
pip install ruff
```

**Timeline:** 1-2 hours
**Risk:** Very low (output compatible)

#### YAPF/autopep8 → Black or Ruff

**Compatibility:** Output will differ significantly

**Rationale:**
- Black/Ruff are opinionated (fewer debates)
- Better community adoption
- Superior performance
- Modern tooling ecosystem

**Migration Steps:**

1. **Document Current Style**
```bash
# Capture current YAPF configuration
cat .style.yapf > yapf-legacy-config.txt
```

2. **Trial Run**
```bash
# Test Black on sample files
black --diff src/sample_module/ > black-preview.diff
```

3. **Full Reformatting**
```bash
# Remove YAPF
pip uninstall yapf

# Install and run Black
pip install black
black .
```

4. **Git Blame Protection**
```bash
# Commit and add to .git-blame-ignore-revs
git add .
git commit -m "Migrate from YAPF to Black"
git rev-parse HEAD >> .git-blame-ignore-revs
```

5. **Update Tooling**
- Remove `.style.yapf` or `setup.cfg` YAPF config
- Add `pyproject.toml` with Black/Ruff config
- Update pre-commit hooks
- Update CI pipelines

**Timeline:** 1-2 days
**Risk:** Medium (requires full reformatting)

### JavaScript/TypeScript Formatters

#### Prettier → Biome

**Compatibility:** 95%+ compatible with careful configuration

**Rationale:**
- 10-35x performance improvement
- Unified linting + formatting
- Modern tooling architecture
- Growing ecosystem

**Migration Steps:**

1. **Install Biome**
```bash
npm install --save-dev @biomejs/biome
```

2. **Migrate Configuration**

Before (`.prettierrc`):
```json
{
  "printWidth": 100,
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5"
}
```

After (`biome.json`):
```json
{
  "formatter": {
    "enabled": true,
    "lineWidth": 100,
    "indentStyle": "space"
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "always",
      "trailingCommas": "es5"
    }
  }
}
```

3. **Test Compatibility**
```bash
# Compare outputs
prettier --write test.js
cp test.js test-prettier.js

git checkout test.js
biome format --write test.js
diff test-prettier.js test.js
```

4. **Gradual Rollout**
```json
// package.json
{
  "scripts": {
    "format:prettier": "prettier --write .",
    "format:biome": "biome format --write .",
    "format": "npm run format:biome"
  }
}
```

5. **Update CI**
```yaml
# Before
- run: npm run format:check

# After
- run: biome ci .
```

**Timeline:** 2-3 days
**Risk:** Low-medium (minor formatting differences possible)

#### ESLint (formatting rules) → Prettier

**Compatibility:** Complementary (not replacement)

**Rationale:**
- Separate concerns (linting vs formatting)
- Avoid rule conflicts
- Better performance
- Industry standard

**Migration Steps:**

1. **Install Prettier and ESLint Config**
```bash
npm install --save-dev prettier eslint-config-prettier
```

2. **Disable ESLint Formatting Rules**

`.eslintrc.json`:
```json
{
  "extends": [
    "eslint:recommended",
    "prettier"  // Must be last
  ]
}
```

3. **Add Prettier Configuration**

`.prettierrc`:
```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5"
}
```

4. **Update Scripts**
```json
{
  "scripts": {
    "lint": "eslint .",
    "format": "prettier --write .",
    "check": "npm run lint && npm run format:check",
    "format:check": "prettier --check ."
  }
}
```

5. **Reformat Codebase**
```bash
prettier --write .
git add .
git commit -m "Apply Prettier formatting"
```

**Timeline:** 1 day
**Risk:** Low (both tools can coexist)

### Multi-Language Migrations

#### Mixed Tools → Unified pre-commit

**Scenario:** Currently using Black, Prettier, and various linters independently

**Target:** Single pre-commit framework orchestrating all tools

**Migration Steps:**

1. **Create Pre-commit Configuration**

`.pre-commit-config.yaml`:
```yaml
repos:
  # Python
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # JavaScript/TypeScript
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx]

  # General
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

2. **Install Pre-commit**
```bash
pip install pre-commit
pre-commit install
```

3. **Test Hooks**
```bash
# Run on all files
pre-commit run --all-files
```

4. **Update CI**
```yaml
- name: Install pre-commit
  run: pip install pre-commit

- name: Run hooks
  run: pre-commit run --all-files
```

5. **Remove Old Tooling**
```bash
# Remove old git hooks
rm .git/hooks/pre-commit.old

# Update package.json to remove redundant scripts
# Update CI to use pre-commit instead of individual tools
```

**Timeline:** 2-3 days
**Risk:** Low (hooks are additive)

## Rollback Procedures

### Immediate Rollback (Same Day)

**If formatting causes critical issues:**

1. **Revert Formatting Commit**
```bash
git revert HEAD
git push
```

2. **Restore Old Configuration**
```bash
git checkout HEAD~1 -- .pre-commit-config.yaml pyproject.toml
```

3. **Notify Team**
- Announce rollback in team chat
- Document issues encountered
- Plan remediation

### Gradual Rollback (After Adoption)

**If team decides tool isn't working:**

1. **Document Pain Points**
- Collect specific issues
- Measure impact on productivity
- Identify alternative solutions

2. **Plan Alternative**
- Research replacement formatter
- Test on subset of code
- Prepare migration guide

3. **Execute Migration**
- Follow migration path to new tool
- Preserve git history
- Update all integration points

## Compatibility Matrix

### Python Formatters

| From/To | Black | Ruff | YAPF | autopep8 |
|---------|-------|------|------|----------|
| Black | - | Easy | Hard | Hard |
| Ruff | Easy | - | Hard | Hard |
| YAPF | Medium | Medium | - | Medium |
| autopep8 | Medium | Medium | Medium | - |

**Easy:** Drop-in replacement, minimal changes
**Medium:** Requires reformatting, configuration migration
**Hard:** Significant output differences, team adaptation needed

### JavaScript/TypeScript Formatters

| From/To | Prettier | Biome | ESLint |
|---------|----------|-------|--------|
| Prettier | - | Easy | N/A |
| Biome | Easy | - | N/A |
| ESLint | Medium | Medium | - |

## Common Migration Challenges

### Challenge 1: Team Resistance
**Symptom:** Developers prefer old formatter

**Solution:**
- Demonstrate performance improvements with metrics
- Run pilot on single module first
- Address specific concerns individually
- Provide comprehensive training

### Challenge 2: Output Incompatibility
**Symptom:** New formatter changes formatting significantly

**Solution:**
- Plan full reformatting during quiet period
- Use `.git-blame-ignore-revs`
- Create comparison reports showing changes
- Allow time for team adjustment

### Challenge 3: Tool Integration Breakage
**Symptom:** IDE, CI, or pre-commit breaks after migration

**Solution:**
- Test all integration points before rollout
- Update documentation proactively
- Provide troubleshooting guide
- Monitor support channels closely

### Challenge 4: Configuration Complexity
**Symptom:** Can't replicate old formatting rules in new tool

**Solution:**
- Accept opinionated defaults when possible
- Document intentional style changes
- Focus on consistency over perfect replication
- Gradually adjust team preferences

## Migration Checklist

### Pre-Migration
- [ ] Document current formatting configuration
- [ ] Test new formatter on sample files
- [ ] Review output differences
- [ ] Get team consensus
- [ ] Schedule migration window

### Migration
- [ ] Update configuration files
- [ ] Install new tools
- [ ] Run formatter on codebase
- [ ] Commit with clear message
- [ ] Update `.git-blame-ignore-revs`

### Post-Migration
- [ ] Update pre-commit hooks
- [ ] Update CI/CD pipelines
- [ ] Update developer documentation
- [ ] Remove old formatter dependencies
- [ ] Monitor for issues

### Validation
- [ ] CI passes on all branches
- [ ] Pre-commit hooks work locally
- [ ] Editor integration functional
- [ ] Team can format successfully
- [ ] Git blame still useful

## Date Compiled
December 4, 2025
