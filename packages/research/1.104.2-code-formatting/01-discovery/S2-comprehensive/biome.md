# Biome: Fast, Unified Formatter and Linter for JavaScript/TypeScript

## Overview

Biome is a performant, all-in-one toolchain for JavaScript, TypeScript, JSX, JSON, and CSS. Designed as a unified replacement for Prettier (formatting) and ESLint (linting), Biome delivers 25x faster formatting and 15x faster linting through its Rust-based architecture and multi-threading capabilities.

**Current Status:** Production-ready, rapidly maturing
**Written In:** Rust
**License:** MIT
**First Release:** 2023 (forked from Rome project)
**Latest Version:** 2.x (as of December 2025)
**Company:** Community-driven (originally Rome, now independent)

## Core Philosophy

Biome's philosophy: **unified, fast, and practical tooling** that replaces multiple JavaScript tools with a single, performant solution.

**Design Principles:**
- Unified toolchain (formatter + linter in one tool)
- Extreme performance (Rust + multi-threading)
- Prettier compatibility (~97%)
- Single configuration file (biome.json)
- Modern architecture for modern JavaScript

**Goals:**
- Replace Prettier + ESLint with one tool
- Provide consistent, fast developer experience
- Minimize configuration complexity
- Support plugin system (Biome 2.0+)

## Architecture

**Two Primary Functions:**

1. **`biome format`** - Code formatting
   - ~97% compatible with Prettier
   - Multi-threaded (25x faster on multi-core systems)
   - Supports JS, TS, JSX, TSX, JSON, CSS

2. **`biome lint`** - Linting and auto-fixing
   - Covers many ESLint rules
   - Includes TypeScript ESLint equivalents
   - Accessibility rules (JSX A11y)
   - React-specific rules
   - Auto-fix capabilities

3. **`biome check`** - Combined format + lint
   - Single command for both operations
   - Optimal performance (shared AST)

## Performance Characteristics

**Formatter Benchmarks:**
- 25x faster than Prettier (multi-threaded)
- 100x faster on M1 Max with 10 cores
- 7x faster single-threaded
- Real-world: 1.3s vs. 28s for 312 files (20x speedup)

**Linter Benchmarks:**
- 15x faster than ESLint (without plugins)
- 4x faster even single-threaded
- Faster than ESLint with extensive caching

**Why So Fast:**
- Written in Rust (memory safety, no GC pauses)
- Multi-threaded by default
- Optimized parser (shared across format/lint)
- Incremental processing (planned)
- Zero npm dependencies

**Performance Impact:**
- Pre-commit hooks: instant instead of seconds
- CI pipelines: seconds instead of minutes
- Watch mode: near-instantaneous feedback

## Language Support

**First-Class Support:**
- JavaScript (ES5-ES2024+)
- TypeScript
- JSX/TSX (React)
- JSON/JSONC
- CSS (experimental)

**Limited/Experimental:**
- GraphQL (in progress)
- Vue (limited support)
- Markdown (limited)
- YAML (not supported)

**Not Supported:**
- HTML (use Prettier)
- PHP, Ruby, Python (use language-specific tools)

## Prettier Compatibility

**Compatibility Level:**
- ~97% compatible with Prettier output
- Biome won the "Prettier Challenge" (official recognition)
- Most projects can migrate with minimal diff

**Known Differences:**
- Default quote style (configurable)
- Some edge cases in JSX formatting
- Comment placement subtleties
- Line break decisions in complex expressions

**Migration Command:**
```bash
npx biome migrate prettier --write
```
Automatically converts `.prettierrc` to `biome.json`

## ESLint Compatibility

**Covered Rule Categories:**
- ESLint core rules (many implemented)
- TypeScript ESLint (@typescript-eslint)
- JSX A11y (accessibility)
- React rules (react-hooks, etc.)
- Unicorn plugin (flake8-like checks)

**Not Covered:**
- 1000+ community ESLint plugins
- Framework-specific plugins (Vue, Angular specific)
- Custom company/team plugins

**Migration Tool:**
```bash
npx biome migrate eslint --write
```
Converts compatible ESLint rules to Biome configuration

## Configuration

**Single Configuration File:**
- `biome.json` or `biome.jsonc`
- Consolidates formatting, linting, and file patterns
- Simpler than separate ESLint + Prettier configs

**Example Configuration:**
```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noExtraBooleanCast": "error"
      },
      "style": {
        "useConst": "warn"
      }
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
      "semicolons": "asNeeded",
      "trailingCommas": "es5"
    }
  }
}
```

**Configuration Options:**

Formatter:
- `lineWidth` (like Prettier's printWidth)
- `indentStyle`, `indentWidth`
- `quoteStyle` (single, double)
- `semicolons` (always, asNeeded)
- `trailingCommas`

Linter:
- Rule-by-rule configuration
- Severity levels (error, warn, off)
- Ignore patterns per rule

## IDE and Ecosystem Integration

**IDE Support:**
- VS Code: Official Biome extension (fast LSP-based)
- WebStorm: Plugin available (community)
- Neovim: nvim-lspconfig support
- Vim: Basic support
- Emacs: Limited support

**VS Code Integration:**
```json
{
  "[javascript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  }
}
```

**CI/CD Integration:**
- GitHub Actions: Community actions available
- Pre-commit: biome hook
- Simple CLI for any CI system

**Commands:**
```bash
# Check and fix everything
biome check --write .

# Format only
biome format --write .

# Lint only
biome lint --write .

# CI check (no fixes)
biome ci .
```

## Strengths

**Performance:**
- 25x faster formatting (multi-threaded)
- 15x faster linting
- Transforms slow CI into instant feedback
- Critical for large monorepos

**Unified Toolchain:**
- One tool replaces Prettier + ESLint
- Single configuration file
- Shared AST (faster, consistent)
- Reduced npm dependencies

**Prettier Compatibility:**
- 97% compatible output
- Easy migration path
- Official migration tools
- Recognized by Prettier maintainers

**Developer Experience:**
- Fast LSP-based editor integration
- Clear error messages
- Auto-fix capabilities
- Modern CLI design

**Modern Architecture:**
- Rust-based (safe, fast)
- Multi-threaded by default
- Plugin system (Biome 2.0+)
- Active development

## Limitations

**Language Coverage:**
- JS/TS/JSON/CSS only (no HTML, YAML, Markdown formatting)
- Need Prettier for additional languages
- Vue, Svelte support limited

**Rule Coverage:**
- Not all ESLint plugins covered (~200 rules vs. ESLint's 1000+)
- Custom company plugins not available
- Gap shrinking but not complete

**Maturity:**
- Newer than Prettier/ESLint (less battle-tested)
- Some edge cases still being discovered
- Smaller community and ecosystem

**Configuration Format:**
- JSON/JSONC only (no JS config files)
- Less flexible for dynamic configuration
- Cannot use environment variables easily

**Incremental Formatting:**
- No incremental formatting (formats full files)
- Prettier supports this, Biome does not yet

## Use Cases

**Ideal For:**
- New JavaScript/TypeScript projects
- Large monorepos with slow CI
- Teams wanting to simplify toolchain
- Projects primarily using JS/TS (not multi-language)
- Performance-critical development workflows

**Less Ideal For:**
- Projects requiring HTML/YAML/Markdown formatting
- Teams with extensive custom ESLint plugins
- Conservative organizations (Prettier/ESLint more mature)
- Multi-language projects (JS + Python + Ruby, etc.)

## Migration Strategy

**From Prettier + ESLint:**

**Phase 1: Assessment**
```bash
# Test Biome on codebase
npx @biomejs/biome check --write .

# Review differences
git diff
```

**Phase 2: Migration**
```bash
# Migrate configs
npx @biomejs/biome migrate prettier --write
npx @biomejs/biome migrate eslint --write

# Install Biome
npm install --save-dev @biomejs/biome

# Remove old tools
npm uninstall prettier eslint eslint-plugin-*
```

**Phase 3: Integration**
- Update VS Code settings
- Update pre-commit hooks
- Update CI scripts
- Document for team

**Expected Impact:**
- ~3% line changes from Prettier differences
- Some ESLint rules may not have equivalents
- Significant CI speed improvement

## Biome 2.0 Features

**Plugin System:**
- Allow custom rules (like ESLint plugins)
- Community-developed plugins
- Framework-specific extensions

**Enhanced Language Support:**
- Improved CSS support
- GraphQL formatting
- Potential HTML support

**Performance:**
- Incremental formatting/linting
- Even faster multi-threading
- Caching improvements

## Recommended Workflows

**Standard Commands:**
```bash
# Format and lint everything
biome check --write .

# CI check (no modifications)
biome ci .

# Format only
biome format --write .

# Lint only
biome lint --write .
```

**Package.json Scripts:**
```json
{
  "scripts": {
    "format": "biome format --write .",
    "lint": "biome lint --write .",
    "check": "biome check --write .",
    "ci": "biome ci ."
  }
}
```

**Pre-commit Hook:**
```yaml
repos:
  - repo: local
    hooks:
      - id: biome
        name: Biome
        entry: npx @biomejs/biome check --write --no-errors-on-unmatched --files-ignore-unknown=true
        language: system
        types: [javascript, typescript, jsx, tsx, json]
        pass_filenames: true
```

## Comparison Summary

**vs. Prettier:**
- Biome: 25x faster, JS/TS only, 97% compatible, includes linting
- Prettier: Multi-language, mature, slower

**vs. ESLint:**
- Biome: 15x faster, fewer rules, unified with formatter
- ESLint: 1000+ rules, highly configurable, slower

**vs. Ruff (Python):**
- Similar philosophy: Rust-based, unified, fast
- Different ecosystems (JS vs. Python)

## Community and Maintenance

**Maturity:** Young but rapidly maturing (2 years)
**Activity:** Very active development
**GitHub Stars:** ~15,000+
**Maintainers:** Community-driven, multiple core contributors
**Release Cadence:** Frequent releases (weekly/bi-weekly)

## Verdict

Biome represents the future of JavaScript tooling: fast, unified, and practical. Its 25x formatting speed and 15x linting speed make it ideal for large projects and performance-conscious teams. With 97% Prettier compatibility and growing ESLint rule coverage, Biome is ready for production use.

**Choose Biome if:**
- You want maximum performance (large monorepo, slow CI)
- You're starting a new JS/TS project
- You want to simplify toolchain (one tool vs. two)
- Your project is primarily JS/TS (not multi-language)

**Stick with Prettier + ESLint if:**
- You need multi-language formatting (HTML, YAML, Markdown)
- You rely on specific ESLint plugins not in Biome
- You prefer maximum maturity and stability
- You have complex dynamic ESLint configurations

**Hybrid Approach:**
- Biome for JS/TS formatting + linting
- Prettier for HTML/Markdown/YAML
- Best of both worlds

By 2025, Biome has gained significant traction, with many teams migrating for performance gains. The upcoming plugin system (Biome 2.0) will likely accelerate adoption further.
