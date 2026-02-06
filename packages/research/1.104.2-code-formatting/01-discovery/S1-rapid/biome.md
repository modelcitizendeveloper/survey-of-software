# Biome - Unified Toolchain for Web Projects

**Ecosystem:** JavaScript/TypeScript (multi-language)
**Category:** Linter + Formatter (unified)
**Repository:** https://github.com/biomejs/biome
**npm:** https://www.npmjs.com/package/@biomejs/biome

## Popularity Metrics (Dec 2025)

- **GitHub Stars:** 20,000+ (estimated)
- **Current Version:** 2.3.8 (released 6 days ago)
- **Dependent Projects:** 223
- **Written in:** Rust

## Key Differentiator

Biome is a unified linter + formatter + import sorter written in Rust, aiming to replace the ESLint + Prettier + import sorting tool chain with a single, fast CLI tool.

## Performance

Biome is significantly faster than Node-based tools:
- **Formatting:** Faster than Prettier on 171,127 lines across 2,104 files
- **Linting:** 6s vs ESLint's 15s (with type-aware rules)
- **Type inference:** 85% coverage of typescript-eslint at fraction of performance cost
- Rust-based execution eliminates Node.js overhead

## Compatibility

- **Prettier:** 97% compatibility
- **ESLint rules:** 391 rules from ESLint, TypeScript ESLint, and other sources
- **Language support:** JavaScript, TypeScript, JSX, TSX, JSON, HTML, CSS, GraphQL

## Biome v2.0 (June 2025)

Major milestone adding type inference:
- Catches type-related issues without TypeScript compiler
- Scans `.d.ts` files in `node_modules`
- ~85% coverage of typescript-eslint type checking
- Transitive dependency analysis

## What Biome Replaces

**All-in-one toolchain:**
- ESLint → Biome linter
- Prettier → Biome formatter
- Import sorters → Biome import sorting
- JSON/CSS formatting → Built-in support

## Limitations

**Plugin Ecosystem:**
- ESLint has 10+ years of plugin maturity
- Biome's plugin ecosystem is growing but not comprehensive
- Missing some framework-specific linting (Vue SFCs, Angular templates)
- CSS, SCSS, YAML, Markdown support improving but not complete

**Coverage Gaps:**
- 85% type inference vs 100% with typescript-eslint
- Fewer rules than ESLint's full ecosystem
- Less mature configuration patterns

## Use Cases

**Good for:**
- New projects (especially with Vite)
- Performance-critical tooling
- Simple linting requirements
- Teams wanting unified toolchain
- Monorepos needing speed

**Not ideal for:**
- Projects requiring advanced ESLint plugins
- Complex framework-specific linting
- Teams with heavily customized ESLint configs
- Vue/Angular projects needing template linting

## Quick Verdict

**Status:** Fast-growing alternative, not yet replacement
**Best for:** New projects prioritizing performance and simplicity
**Trade-off:** Speed + simplicity vs plugin ecosystem maturity

Biome represents the Rust-based future of JavaScript tooling - fast, unified, and simple. While it can't fully replace ESLint + Prettier today (plugin gap), it's a strong choice for new projects with straightforward needs.

**Recommendation:**
- **New projects with Vite/simple needs:** Consider Biome
- **Existing projects:** Stick with ESLint + Prettier unless performance is critical
- **Complex linting requirements:** Wait for Biome's ecosystem to mature
