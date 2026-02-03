# Prettier: Opinionated Code Formatter for JavaScript and More

## Overview

Prettier is the most popular code formatter for JavaScript, TypeScript, and web technologies. Released in 2017, it pioneered the "opinionated formatter" concept in the JavaScript ecosystem, eliminating style debates through deliberate lack of configuration.

**Current Status:** Mature, industry standard
**Written In:** JavaScript
**License:** MIT
**First Release:** 2017
**Latest Version:** 3.x (as of December 2025)
**Monthly Downloads:** ~50 million (npm)

## Core Philosophy

Prettier follows the principle: "You press save and code is formatted. No discussion needed."

**Design Principles:**
- Opinionated with minimal configuration
- Multi-language support (JS, TS, CSS, HTML, JSON, Markdown, YAML, etc.)
- Focus on consistent output over customization
- Print width optimization (line length management)
- AST-based formatting (safe, semantic-preserving)

**The Prettier Style:**
- Single quotes (configurable)
- Semicolons (configurable)
- 2-space indentation (configurable)
- 80 character print width (configurable)
- Trailing commas in multi-line structures

## Language Support

**First-Class Support:**
- JavaScript (ES5-ES2024+)
- TypeScript
- JSX/TSX (React)
- CSS, SCSS, Less
- JSON
- HTML
- Markdown
- YAML
- GraphQL

**Plugin Support:**
- PHP (via plugin)
- Ruby (via plugin)
- Java (via plugin)
- Python (via plugin - limited)
- XML (via plugin)
- Many others

## Performance Characteristics

**Speed Benchmarks:**
- ~1,000-2,000 files: 2-3 seconds (single-threaded)
- Baseline for JavaScript formatter comparisons
- Adequate for most projects, but not optimized for large monorepos

**Performance Limitations:**
- Single-threaded (no parallel processing)
- JavaScript-based (V8 performance ceiling)
- Startup overhead on small files
- No incremental formatting (formats entire files)

**Caching:**
- `--cache` flag available (v2.0+)
- Caches formatting results
- Significantly speeds up repeated runs
- Useful in CI pipelines

## Configuration

Prettier deliberately limits configuration options to prevent style debates:

**Available Options:**
- `printWidth` (default 80)
- `tabWidth` (default 2)
- `useTabs` (default false)
- `semi` (default true)
- `singleQuote` (default false)
- `quoteProps` (as-needed, consistent, preserve)
- `trailingComma` (es5, none, all)
- `bracketSpacing` (default true)
- `arrowParens` (always, avoid)
- `endOfLine` (lf, crlf, cr, auto)

**Configuration Files:**
- `.prettierrc` (JSON, YAML, or JS)
- `.prettierrc.json`, `.prettierrc.yml`, `.prettierrc.js`
- `prettier.config.js`
- `package.json` (`"prettier"` key)

**Example Configuration:**
```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
```

## IDE and Ecosystem Integration

**IDE Support (Excellent):**
- VS Code: Official extension (10M+ installs)
- WebStorm/IntelliJ: Built-in support
- Vim/Neovim: Multiple plugins (vim-prettier, coc-prettier)
- Emacs: prettier-emacs
- Sublime Text: JsPrettier plugin

**Build Tool Integration:**
- webpack: prettier-webpack-plugin
- ESLint: eslint-plugin-prettier
- lint-staged: Direct integration
- Husky: Pre-commit hook support

**CI/CD Integration:**
- GitHub Actions: Multiple community actions
- Pre-commit: prettier hook
- GitLab CI, CircleCI: Simple command execution

**Editor Plugins:**
- Format on save
- Format selection
- Format on paste
- Real-time feedback

## Compatibility and Integration

**ESLint Integration:**

Two approaches:

1. **eslint-plugin-prettier** (Run Prettier as ESLint rule)
   ```json
   {
     "extends": ["plugin:prettier/recommended"]
   }
   ```
   Pros: Single command
   Cons: Slower, conflates formatting and linting

2. **Separate tools** (Recommended)
   ```bash
   prettier --write . && eslint --fix .
   ```
   Pros: Clear separation, faster
   Cons: Two commands

**eslint-config-prettier:**
Disables ESLint rules that conflict with Prettier:
```json
{
  "extends": ["eslint:recommended", "prettier"]
}
```

## Strengths

**Consistency:**
- Eliminates style debates
- Same output across team members
- Stable output across versions

**Multi-Language:**
- Single tool for JS, TS, CSS, HTML, JSON, Markdown
- Consistent formatting across entire project
- Reduces tool complexity

**Adoption:**
- Industry standard (highest npm downloads)
- Universal IDE support
- Extensive documentation
- Large community

**Ease of Use:**
- Zero-config getting started
- Intuitive options
- Easy to understand output

**Safety:**
- AST-based (never breaks code)
- Extensive test suite
- Semantic preservation guarantees

## Limitations

**Performance:**
- 7-25x slower than Biome
- 10-100x slower than dprint
- Single-threaded (no parallelization)
- Noticeable in large monorepos

**Configurability:**
- Limited options (by design)
- Cannot adapt to many existing style guides
- No per-file overrides (only ignore files)

**Linting:**
- Only formats, doesn't lint
- Requires separate ESLint setup
- Two tools = two configs, two runs

**ESLint Conflicts:**
- Requires eslint-config-prettier to avoid conflicts
- Plugin approach (eslint-plugin-prettier) slower
- Integration complexity

## Use Cases

**Ideal For:**
- Web development projects (JS/TS/React/Vue)
- Teams wanting zero-config formatting
- Multi-language codebases (JS + CSS + HTML + Markdown)
- Projects prioritizing consistency over customization
- Organizations standardizing across multiple projects

**Less Ideal For:**
- Large monorepos (performance issues)
- Teams with strict existing style guides
- Projects requiring deep customization
- Performance-critical CI pipelines

## Comparison Context

**vs. Biome:**
- Prettier: Mature, multi-language, slower
- Biome: 25x faster, JS/TS/JSON only, 97% compatible

**vs. dprint:**
- Prettier: More languages, slower, larger ecosystem
- dprint: 10-100x faster, plugin-based, less adoption

**vs. ESLint:**
- Prettier: Formatting only, opinionated
- ESLint: Linting focus, highly configurable

## Recommended Workflows

**Standard Setup:**
```bash
# Install
npm install --save-dev prettier

# Create config
echo '{"singleQuote": true, "printWidth": 100}' > .prettierrc.json

# Format
npx prettier --write .
```

**With ESLint (Separate):**
```bash
# Format first
npx prettier --write .

# Then lint
npx eslint --fix .
```

**Pre-commit Hook:**
```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{js,ts,jsx,tsx,css,md,json}": ["prettier --write"]
  }
}
```

**VS Code Settings:**
```json
{
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

**package.json scripts:**
```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "lint": "eslint --fix .",
    "quality": "npm run format && npm run lint"
  }
}
```

## Community and Maintenance

**Maturity:** Very mature (8+ years)
**Activity:** Active development, stable
**GitHub Stars:** ~49,000+
**npm Downloads:** ~50 million/month
**Maintainers:** Community-driven (Prettier organization)

**Ecosystem:**
- 100+ editor plugins
- Extensive Stack Overflow presence
- Active Discord community
- Comprehensive documentation

## Migration Considerations

**From Manual Formatting:**
- Expect significant initial diff
- Recommend separate "format all" commit
- Use `.prettierignore` for legacy code

**From ESLint Formatting Rules:**
- Disable conflicting ESLint rules (eslint-config-prettier)
- Run Prettier first, then ESLint
- Update CI pipelines

**To Biome:**
- Biome provides ~97% compatibility
- Migration command: `npx biome migrate prettier --write`
- Review differences before committing

## Prettier 3.x Updates

**Major Changes (v3.0+):**
- Improved TypeScript support
- Better JSX formatting
- Enhanced performance (still slower than Biome/dprint)
- Simplified plugin API

## Verdict

Prettier remains the gold standard for JavaScript/TypeScript formatting in 2025. Its opinionated approach and multi-language support have made it indispensable for web development. While newer alternatives like Biome offer significant speed improvements, Prettier's maturity, ecosystem, and language coverage make it a reliable default choice.

**Choose Prettier if:** You want the battle-tested industry standard with maximum language coverage and ecosystem support.

**Consider alternatives if:** Performance is critical (large monorepo) or you want unified formatting + linting (Biome).

**Recommended combination:** Prettier (formatting) + ESLint (linting) remains a proven, robust setup for most JavaScript/TypeScript projects in 2025.
