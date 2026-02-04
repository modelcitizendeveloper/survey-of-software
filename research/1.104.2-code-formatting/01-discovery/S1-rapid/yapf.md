# YAPF - Yet Another Python Formatter

**Ecosystem:** Python
**Category:** Code Formatter
**Maintainer:** Google
**Repository:** https://github.com/google/yapf

## Popularity Metrics (Dec 2025)

- **GitHub Stars:** 13,000+ (estimated)
- **Ecosystem Position:** Niche tool for teams wanting configurability
- **Origin:** Google

## Key Differentiator

YAPF is a "strict formatter" like Black but with significant configurability. It comes with three built-in styles (pep8, google, chromium) and extensive customization options.

## Philosophy: Configurable Formatting

Unlike Black's "uncompromising" approach:
- Highly configurable base styles
- Does not fix PEP 8 violations (just formats)
- Can beautify already-compliant code
- Balances consistency with team preferences

## Readability Focus

October 2025 analysis comparing Ruff, autopep8, and YAPF found:
- **Best readability out of the box** (only 1 tweak needed)
- Strange handling of long dictionaries (main complaint)
- Most readable code output among alternatives

## Performance Concerns

**Weaknesses:**
- Slower than Black (significantly slower than Ruff)
- Clunky CLI: `yapf --inplace --recursive .` vs Black's `black .`
- Not Rust-based, so limited speed improvements

## Built-in Styles

- **pep8:** PEP 8 guidelines
- **google:** Google's Python style guide
- **chromium:** Chromium project style
- **facebook:** Facebook's internal style

## Quick Verdict

**Status:** Mature but niche
**Best for:** Teams needing style customization beyond Black's opinionated defaults
**Trade-off:** Configuration complexity vs consistency guarantees

YAPF's configurability is both strength and weakness. While it produces highly readable code and respects team preferences, the Python ecosystem has largely moved toward Black's "no configuration" philosophy. Speed and simplicity win over customization.

**Recommendation:** Consider only if your team has strong, specific formatting requirements that Black/Ruff cannot accommodate. Otherwise, use Black or Ruff for simplicity and ecosystem alignment.
