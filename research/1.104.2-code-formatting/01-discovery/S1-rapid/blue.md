# Blue - The Slightly Less Uncompromising Python Formatter

**Ecosystem:** Python
**Category:** Code Formatter
**Repository:** https://github.com/grantjenks/blue
**PyPI:** https://pypi.org/project/blue/

## Popularity Metrics (Dec 2025)

- **GitHub Stars:** ~300-400 (estimated, niche tool)
- **Current Version:** 0.9.1
- **Origin:** LinkedIn engineers
- **Ecosystem Position:** Niche Black alternative

## Key Differentiator

Blue is a Black fork with two opinionated changes: single-quoted strings (instead of double) and 79-character line lengths (instead of 88). Otherwise maintains Black's philosophy.

## Philosophy: Minimal Black Modifications

Blue agrees with Black's automatic formatting but disagrees with specific style choices:
- **Single quotes** for strings (except docstrings)
- **79-character line length** (PEP 8 standard)
- Everything else stays Black-like

The team monkeypatches Black rather than forking the codebase, hoping to eventually merge configuration options back into Black.

## Configuration Support

Supports multiple config files:
- `pyproject.toml`
- `setup.cfg`
- `tox.ini`
- `.blue`

## Why "Blue"?

Named after LinkedIn's brand color. The tool was created by LinkedIn engineers and socialized internally.

## Use Cases

**Good for:**
- Teams strongly preferring single quotes
- Projects strictly adhering to 79-character PEP 8 limit
- Organizations (like LinkedIn) with existing style preferences

**Not ideal for:**
- Ecosystem compatibility (Black is the standard)
- Projects wanting zero configuration debates
- Teams seeking maximum tool adoption

## Quick Verdict

**Status:** Niche tool, minimal adoption outside LinkedIn
**Best for:** Teams with strong single-quote preference
**Trade-off:** Customization vs ecosystem standardization

Blue demonstrates the tension between Black's "uncompromising" philosophy and team preferences. While the modifications are minimal, they fragment the ecosystem. Black's dominance (and Ruff's Black compatibility) makes Blue's use case increasingly narrow.

**Recommendation:** Avoid unless single quotes are non-negotiable. Use Black or Ruff for ecosystem alignment.
