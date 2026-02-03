# ESLint: Pluggable JavaScript and TypeScript Linter

## Overview

ESLint is the most popular and comprehensive linting tool for JavaScript and TypeScript. Unlike formatters (Prettier, Biome), ESLint focuses on code quality, bug detection, and best practices enforcement. It provides a highly configurable, plugin-based architecture with 1000+ rules and extensive community ecosystem.

**Current Status:** Mature, industry standard
**Written In:** JavaScript
**License:** MIT
**First Release:** 2013
**Latest Version:** 9.x (as of December 2025)
**Monthly Downloads:** ~60 million (npm)

## Core Philosophy

ESLint's philosophy: **Pluggable linting** that allows teams to enforce code quality standards, detect bugs, and maintain best practices through configurable rules.

**Design Principles:**
- Pluggable architecture (custom rules, plugins)
- Highly configurable (per-project, per-file)
- AST-based analysis (safe, semantic-aware)
- Auto-fix capabilities where possible
- Language agnostic (via parsers)

**Focus Areas:**
- Code quality (complexity, patterns)
- Bug detection (potential errors)
- Best practices (modern JS/TS patterns)
- Style consistency (though Prettier preferred for formatting)

## ESLint vs. Formatters

**Key Distinction:**

**ESLint (Linter):**
- Finds problematic code patterns
- Enforces best practices
- Detects potential bugs
- Can fix some issues automatically
- Configurable style rules (discouraged)

**Prettier/Biome (Formatters):**
- Formats code appearance
- Enforces consistent style
- Opinionated formatting
- No bug detection
- Minimal configuration

**Recommended Approach:**
- Use Prettier/Biome for formatting
- Use ESLint for linting/quality
- Disable ESLint formatting rules (eslint-config-prettier)

## Architecture

**Core Components:**

1. **Parser:** Converts code to AST
   - Default: espree (JavaScript)
   - @typescript-eslint/parser (TypeScript)
   - @babel/eslint-parser (Babel features)

2. **Rules:** Individual checks (400+ built-in)
   - Errors, warnings, suggestions
   - Auto-fixable vs. manual

3. **Plugins:** Rule collections and extensions
   - Community plugins (1000+)
   - Framework-specific (React, Vue, Angular)
   - Tool-specific (Jest, Testing Library)

4. **Configs:** Shareable rule configurations
   - eslint:recommended
   - Airbnb, Google, Standard
   - Company/team configs

## Performance Characteristics

**Speed Benchmarks:**
- Single-threaded execution
- Moderate speed (JavaScript-based)
- Can be slow with many plugins
- Caching helps significantly

**Performance Issues:**
- Large codebases: 10s-60s+ linting time
- Multiple plugins compound slowness
- TypeScript rules particularly slow
- No built-in parallelization

**Optimization Strategies:**
- Enable caching (`--cache`)
- Limit plugin count
- Use flat config (ESLint 9+)
- Consider Biome for speed-critical projects

**Comparison:**
- Biome: 15x faster than ESLint
- ESLint with cache: Moderate improvement
- ESLint without cache: Baseline

## Rule Coverage

**Built-in Categories:**

**Possible Errors:**
- `no-console`: Disallow console statements
- `no-debugger`: Disallow debugger statements
- `no-dupe-keys`: Disallow duplicate object keys
- `no-unreachable`: Disallow unreachable code

**Best Practices:**
- `eqeqeq`: Require === and !==
- `no-eval`: Disallow eval()
- `no-implied-eval`: Disallow implied eval
- `no-var`: Require let/const instead of var

**ES6+:**
- `prefer-const`: Prefer const over let
- `prefer-arrow-callback`: Prefer arrow functions
- `prefer-template`: Prefer template literals
- `no-useless-constructor`: Disallow unnecessary constructors

**Style (Discouraged - Use Prettier):**
- `indent`, `quotes`, `semi`, etc.
- Better handled by formatters

## Popular Plugins

**TypeScript:**
- `@typescript-eslint/eslint-plugin`
- 100+ TypeScript-specific rules
- Type-aware rules (requires tsconfig.json)

**React:**
- `eslint-plugin-react`
- `eslint-plugin-react-hooks`
- JSX best practices, hook rules

**Testing:**
- `eslint-plugin-jest`
- `eslint-plugin-testing-library`
- Test-specific best practices

**Accessibility:**
- `eslint-plugin-jsx-a11y`
- ARIA rules, accessibility checks

**Import/Module:**
- `eslint-plugin-import`
- Import order, resolution, circular dependencies

**Unicorn:**
- `eslint-plugin-unicorn`
- Additional best practices

## Configuration

**Configuration Files:**
- `eslint.config.js` (ESLint 9+ flat config)
- `.eslintrc.js` / `.eslintrc.json` (legacy)
- `.eslintrc.yml`
- `package.json` (`"eslintConfig"` key)

**Flat Config Example (ESLint 9+):**
```javascript
import js from '@eslint/js';
import typescript from '@typescript-eslint/eslint-plugin';
import react from 'eslint-plugin-react';
import prettier from 'eslint-config-prettier';

export default [
  js.configs.recommended,
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: '@typescript-eslint/parser',
      parserOptions: {
        project: './tsconfig.json'
      }
    },
    plugins: {
      '@typescript-eslint': typescript,
      'react': react
    },
    rules: {
      '@typescript-eslint/no-unused-vars': 'error',
      'react/jsx-uses-react': 'off',
      'react/react-in-jsx-scope': 'off'
    }
  },
  prettier
];
```

**Legacy Config Example:**
```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2024,
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "plugins": ["@typescript-eslint", "react"],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "eqeqeq": ["error", "always"],
    "no-console": "warn"
  }
}
```

## Prettier Integration

**Recommended Approach:**

1. **Install eslint-config-prettier:**
   ```bash
   npm install --save-dev eslint-config-prettier
   ```

2. **Add to config (must be last):**
   ```json
   {
     "extends": [
       "eslint:recommended",
       "prettier"
     ]
   }
   ```

3. **Run separately:**
   ```bash
   prettier --write . && eslint --fix .
   ```

**Alternative (Not Recommended):**
- `eslint-plugin-prettier`: Runs Prettier as ESLint rule
- Cons: Slower, conflates concerns
- Use only if you must have single command

## IDE and Ecosystem Integration

**IDE Support (Excellent):**
- VS Code: Official ESLint extension (10M+ installs)
- WebStorm/IntelliJ: Built-in support
- Vim/Neovim: coc-eslint, ALE
- Emacs: flycheck with eslint
- Sublime Text: SublimeLinter-eslint

**VS Code Settings:**
```json
{
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

**CI/CD Integration:**
- GitHub Actions: Multiple community actions
- Pre-commit: eslint hook
- Simple CLI for any CI system

**Commands:**
```bash
# Lint files
eslint .

# Auto-fix issues
eslint --fix .

# Check specific files
eslint src/**/*.ts

# Output JSON (for tooling)
eslint --format json .
```

## Strengths

**Comprehensive Rule Coverage:**
- 400+ built-in rules
- 1000+ community plugin rules
- Covers virtually all JS/TS patterns

**Pluggable Architecture:**
- Custom rules for company standards
- Framework-specific plugins
- Tool-specific plugins

**Configurability:**
- Per-project, per-directory, per-file configs
- Inline rule overrides (`/* eslint-disable */`)
- Granular severity levels (error, warn, off)

**Maturity:**
- 12+ years of development
- Battle-tested on millions of projects
- Extensive documentation
- Large community

**TypeScript Support:**
- Full TypeScript integration
- Type-aware rules
- Modern TS pattern enforcement

## Limitations

**Performance:**
- Single-threaded (slow on large codebases)
- Plugin overhead compounds
- 15x slower than Biome
- Caching helps but not enough for huge monorepos

**Complexity:**
- Configuration can be overwhelming
- Many overlapping rules
- Plugin conflicts possible
- Steep learning curve for custom rules

**Formatting Rules:**
- Style rules conflict with Prettier
- Formatting should be handled by Prettier/Biome
- eslint-config-prettier required

**Breaking Changes:**
- Major versions can have significant changes
- Plugin compatibility issues
- Migration effort (especially ESLint 9 flat config)

## Use Cases

**Ideal For:**
- Any JavaScript/TypeScript project (quality checks)
- Teams enforcing best practices
- Custom rule requirements
- Framework-specific linting (React, Vue, Angular)
- Large codebases with established ESLint configs

**Less Ideal For:**
- Projects needing only formatting (use Prettier/Biome)
- Performance-critical CI (consider Biome)
- Small scripts (overkill)

## ESLint 9 Flat Config

**Major Change (2024-2025):**
- New flat config format (`.js` based)
- Simpler, more explicit configuration
- Better TypeScript support
- Improved performance

**Migration:**
- Legacy configs still supported (for now)
- Migration tools available
- Documentation comprehensive

## Recommended Workflows

**With Prettier (Separate):**
```bash
# Format first
prettier --write .

# Then lint
eslint --fix .
```

**Package.json Scripts:**
```json
{
  "scripts": {
    "format": "prettier --write .",
    "lint": "eslint --fix .",
    "quality": "npm run format && npm run lint"
  }
}
```

**Pre-commit Hook:**
```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0
    hooks:
      - id: prettier
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.0.0
    hooks:
      - id: eslint
        args: [--fix]
```

## Comparison Summary

**vs. Biome Linter:**
- ESLint: 1000+ rules, slow, mature
- Biome: 200+ rules, 15x faster, growing

**vs. Prettier:**
- ESLint: Linting/quality focus
- Prettier: Formatting focus only

**vs. TSLint (Deprecated):**
- ESLint: Active, with @typescript-eslint
- TSLint: Deprecated (migrated to ESLint)

## Popular Shareable Configs

**Airbnb:**
- `eslint-config-airbnb`
- Comprehensive, opinionated
- Most popular shareable config

**Standard:**
- `eslint-config-standard`
- Zero-config, JavaScript Standard Style

**Google:**
- `eslint-config-google`
- Google's JavaScript style guide

**XO:**
- `eslint-config-xo`
- Opinionated, strict

## Community and Maintenance

**Maturity:** Very mature (12+ years)
**Activity:** Active development
**GitHub Stars:** ~25,000+
**npm Downloads:** ~60 million/month
**Maintainers:** OpenJS Foundation

**Ecosystem:**
- 1000+ plugins
- Extensive Stack Overflow presence
- Active Discord/discussions
- Comprehensive documentation

## Verdict

ESLint remains the industry standard for JavaScript/TypeScript linting in 2025. Its comprehensive rule coverage, pluggable architecture, and mature ecosystem make it indispensable for code quality enforcement. While newer alternatives like Biome offer speed improvements, ESLint's depth and breadth are unmatched.

**Use ESLint if:**
- You need comprehensive linting (quality, bugs, best practices)
- You have custom rule requirements
- You're using framework-specific rules (React, Vue)
- Performance is acceptable for your codebase size

**Consider alternatives if:**
- You only need formatting (use Prettier/Biome instead)
- Performance is critical and rule coverage of Biome suffices
- You're starting fresh and want unified tooling (Biome)

**Recommended combination for 2025:**
- **Formatting:** Prettier or Biome
- **Linting:** ESLint (with eslint-config-prettier)
- **Best of both:** Comprehensive checks + consistent formatting

ESLint's role is clear: focus on what it does best (linting/quality), and let formatters handle style.
