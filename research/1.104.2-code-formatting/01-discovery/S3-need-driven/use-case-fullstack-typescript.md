# Use Case: Full-Stack TypeScript Application

## Scenario Overview

Developing a full-stack TypeScript application with React/Vue/Svelte frontend and Node.js backend, requiring unified formatting across all code and configuration files.

## Primary Requirements

### Code Consistency
- Unified style across frontend and backend
- Framework-specific formatting support
- JSX/TSX handling
- JSON/YAML configuration formatting

### Developer Experience
- Editor integration (VSCode, WebStorm, Vim)
- Fast format-on-save (< 200ms)
- Clear error messages
- Minimal configuration debates

### Build Integration
- Pre-commit formatting
- CI verification
- Build tool integration (Vite, Next.js, etc.)
- Monorepo support if needed

### Team Collaboration
- Onboarding simplicity
- Consistent PR formatting
- Automated fixes
- Clear style guide

## Recommended Toolchain

### Primary: Prettier
Industry standard for JavaScript/TypeScript ecosystem

**Why Prettier:**
- Zero-config opinionated defaults
- Comprehensive language support (JS, TS, JSX, CSS, JSON, YAML, Markdown)
- Excellent framework integration
- Universal editor support
- Massive ecosystem adoption

### Complementary: ESLint
For code quality rules beyond formatting

**Why ESLint + Prettier:**
- ESLint handles logic/quality rules
- Prettier handles formatting
- `eslint-config-prettier` disables conflicting rules
- Best-of-both-worlds approach

## Configuration Approach

### Prettier Configuration

`.prettierrc`:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "avoid"
}
```

Or use zero-config (recommended):
```json
{}
```

### ESLint Integration

`.eslintrc.json`:
```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "prettier"
  ],
  "plugins": ["@typescript-eslint", "react"],
  "rules": {
    "no-console": "warn"
  }
}
```

### File Ignore Patterns

`.prettierignore`:
```
dist/
build/
coverage/
node_modules/
*.min.js
package-lock.json
pnpm-lock.yaml
```

## Pre-commit Hook Setup

### Using Husky + lint-staged

`package.json`:
```json
{
  "scripts": {
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "prettier --write",
      "eslint --fix"
    ],
    "*.{json,css,md,yaml,yml}": [
      "prettier --write"
    ]
  }
}
```

`.husky/pre-commit`:
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
```

### Using pre-commit (Python-based)

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, yaml, markdown]
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Format & Lint
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Check formatting
        run: npm run format:check

      - name: Lint code
        run: npm run lint
```

### NPM Scripts

`package.json`:
```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint . --ext .js,.jsx,.ts,.tsx --fix"
  }
}
```

## Common Pitfalls

### Pitfall 1: ESLint Formatting Rules Conflict
**Problem:** Running ESLint and Prettier creates conflicting formatting requirements

**Solution:** Install `eslint-config-prettier` to disable ESLint formatting rules:
```bash
npm install --save-dev eslint-config-prettier
```
Add `"prettier"` as last item in `.eslintrc.json` extends array

### Pitfall 2: Slow Format-on-Save
**Problem:** Formatting large files or many files blocks editor

**Solution:**
- Configure editor to format only changed files
- Use Prettier's cache: `prettier --write --cache .`
- Consider Biome for 10x faster formatting

### Pitfall 3: Inconsistent Configuration
**Problem:** Different developers use different Prettier versions with subtle differences

**Solution:**
- Pin exact Prettier version in `package.json`
- Use `engines` field to enforce Node version
- Document editor setup in README

### Pitfall 4: Build Output Formatting
**Problem:** Prettier tries to format generated bundles in `dist/` or `build/`

**Solution:** Always maintain comprehensive `.prettierignore` file

### Pitfall 5: Markdown Code Block Formatting
**Problem:** Code examples in markdown get formatted differently than actual code

**Solution:** Use `prettier-plugin-embed` or ensure markdown processor respects language tags

## Alternative: Biome (Modern Performance)

For performance-critical workflows, consider Biome:

**Biome Advantages:**
- 10-35x faster than Prettier
- Single tool for linting + formatting
- Zero dependencies (Rust binary)
- Near-Prettier output compatibility

**Biome Configuration (`biome.json`):**
```json
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
  }
}
```

**When to Choose Biome:**
- Very large codebases (100k+ lines)
- Monorepo with many packages
- CI speed is critical
- Willing to adopt newer tooling

## Success Metrics

- Format-on-save completes in < 200ms
- CI formatting check completes in < 30 seconds
- Zero formatting PR comments after onboarding
- 100% of team uses consistent editor configuration

## Date Compiled
December 4, 2025
