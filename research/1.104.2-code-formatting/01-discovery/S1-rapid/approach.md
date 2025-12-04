# S1 RAPID Library Search: Code Formatting

**Research Domain:** 1.104.2 Code Formatting
**Methodology:** S1 - Rapid Library Search
**Date Compiled:** December 4, 2025
**Time Investment:** ~2-3 hours

## Objective

Speed-focused discovery of code formatting and linting libraries across Python and JavaScript/TypeScript ecosystems to determine current best practices and identify the dominant tools in each space.

## Scope

**Python Ecosystem:**
- Black (established formatter)
- Ruff (Rust-based formatter/linter)
- autopep8 (PEP 8 compliance)
- yapf (Google's formatter)
- isort (import sorting)
- blue (Black alternative)

**JavaScript/TypeScript Ecosystem:**
- Prettier (dominant formatter)
- ESLint (linting standard)
- Biome (unified toolchain)
- dprint (Rust-based alternative)

## Methodology: S1 Rapid Library Search

The S1 approach prioritizes speed and ecosystem awareness over deep technical analysis:

### 1. Popularity Metrics (30 minutes)
- GitHub stars (community adoption)
- Weekly downloads (npm/PyPI)
- Dependent packages
- Major project adoption

### 2. Quick Feature Assessment (45 minutes)
- Primary purpose (formatting vs linting vs both)
- Performance claims (benchmarks if available)
- Key differentiator in 1-2 sentences
- Language/ecosystem support

### 3. Community Signals (30 minutes)
- Recent release activity
- Backing organization (Astral, Google, Meta, etc.)
- Migration trends (what's replacing what)
- Integration with modern tooling

### 4. Decision Framework (30 minutes)
- When to use each tool
- Compatibility considerations
- Migration paths
- Future trajectory

## Key Research Questions

1. **Is Ruff replacing Black?** What's the current state of Python formatting in late 2025?
2. **Prettier dominance:** Is Prettier still the default for JavaScript/TypeScript, or are alternatives gaining ground?
3. **All-in-one tools:** Are unified toolchains (Ruff, Biome) winning over single-purpose tools?
4. **Performance matters:** How much do speed improvements influence adoption?

## Success Criteria

- Quick verdict on each tool (50-100 words)
- Clear recommendation by ecosystem
- Understanding of migration trends
- Confidence in "safe default" choices

## Limitations

S1 research does NOT provide:
- Detailed configuration analysis
- Edge case behavior testing
- Plugin ecosystem deep-dives
- Custom rule implementation guides

For those needs, escalate to S2 (Comprehensive) or S3 (Need-Driven) methodologies.

## Output Structure

Each tool gets a dedicated markdown file with:
- Stars/downloads snapshot
- Key differentiator
- Performance notes
- Quick verdict

Final `recommendation.md` synthesizes findings into actionable guidance.
