# ESLint - Pluggable JavaScript Linter

**Ecosystem:** JavaScript/TypeScript
**Category:** Linter
**Repository:** https://github.com/eslint/eslint
**npm:** https://www.npmjs.com/package/eslint

## Popularity Metrics (Dec 2025)

- **GitHub Stars:** 26,279
- **Weekly Downloads:** 63,348,123 (63M+)
- **Current Version:** 9.36.0
- **Annual Donations:** $128,688 from 144 sponsors
- **Repositories:** 34 official ESLint repos

## Key Differentiator

ESLint is the #1 JavaScript linter by downloads, providing pluggable linting with extensive rule customization. While Prettier handles formatting, ESLint catches code quality issues, bugs, and anti-patterns.

## Major Users

- Microsoft
- Airbnb
- Netflix
- Facebook
- Countless open-source projects

## ESLint vs Prettier: Division of Labor

**ESLint:** Code quality and best practices
- Unused variables
- Missing dependencies
- Potential bugs
- Anti-patterns
- TypeScript-specific issues (via typescript-eslint)

**Prettier:** Code formatting
- Whitespace
- Line breaks
- Quotes
- Semicolons

These tools are complementary, not competitive.

## TypeScript Support

`typescript-eslint` provides comprehensive TypeScript linting:
- Type-aware rules
- TypeScript-specific checks
- Integration with TSC
- Growing ecosystem

## Plugin Ecosystem

ESLint's killer feature is its mature plugin ecosystem:
- Framework-specific rules (React, Vue, Angular)
- Library-specific linting (Jest, Testing Library)
- Custom organizational rules
- Accessibility (jsx-a11y)
- Security scanning

**Maturity:** 10+ years of plugin development

## 2025 Status

ESLint remains the standard for JavaScript/TypeScript linting. While Biome is emerging as an alternative, ESLint's plugin ecosystem and decade of maturity make it the safe default.

## Performance Considerations

ESLint can be slow on large codebases, especially with type-aware rules:
- Type checking adds overhead
- Plugin chains compound execution time
- Biome offers 6s vs ESLint's 15s on some codebases

## Quick Verdict

**Status:** Dominant standard, irreplaceable plugin ecosystem
**Best for:** Any JavaScript/TypeScript project needing linting
**Pair with:** Prettier for formatting
**Consider Biome:** If performance is critical and you don't need advanced plugins

ESLint's combination of maturity, flexibility, and ecosystem support makes it the de facto linting standard. While newer tools offer performance improvements, none match ESLint's breadth.

**Recommendation:** Default choice. Pair with Prettier for formatting. Consider Biome only for new projects with simple linting needs and performance requirements.
