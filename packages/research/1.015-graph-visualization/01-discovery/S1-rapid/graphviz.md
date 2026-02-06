# Graphviz (Python bindings)

**GitHub:** ~1.7K stars (python library) | **Ecosystem:** Python/C | **License:** MIT

## Positioning

Python wrapper for the venerable Graphviz DOT language compiler. Industry standard for hierarchical and directed graph layouts. Used by documentation generators (Sphinx, Doxygen) and UML tools.

## Key Metrics

- **Performance:** C-based rendering, handles 100K+ nodes efficiently
- **Download stats:** ~25M downloads/month on PyPI (Jan 2025)
- **Maintenance:** Graphviz core (1991) is stable; Python bindings actively maintained
- **Python versions:** 3.7+ supported

## Visualization Capabilities

- Hierarchical layouts (dot - top-down trees)
- Force-directed layouts (neato, fdp)
- Circular layouts (circo, twopi)
- Export to PNG, SVG, PDF, PostScript
- Subgraph clustering

## Community Signals

**Stack Overflow sentiment:**
- "Graphviz for flowcharts and dependency graphs - nothing better for hierarchical layouts"
- "The gold standard for DOT diagrams, but learning curve is steep"
- "Use it for static documentation, not interactive exploration"

**Common use cases:**
- Software architecture diagrams (dependency trees, call graphs)
- State machine visualization (compiler design)
- Documentation generation (autodoc tools)
- Organizational charts and process flows

## Trade-offs

**Strengths:**
- Best hierarchical layout algorithms (dot engine)
- Production-proven (30+ years in use)
- High-quality static output (PDF, SVG for papers/docs)
- Scales to massive graphs (100K+ nodes)
- Deterministic layouts (reproducible diagrams)

**Limitations:**
- No interactivity (static images only)
- DOT language learning curve (declarative syntax)
- Python bindings are thin wrappers (limited Pythonic API)
- Requires separate Graphviz installation (system dependency)

## Decision Context

**Choose Graphviz when:**
- Need hierarchical or directed graph layouts
- Generating documentation diagrams programmatically
- Require publication-quality static output
- Working with very large graphs (>50K nodes)

**Skip if:**
- Need interactive web-based exploration
- Prefer pure Python (no system dependencies)
- Want drag-and-drop node positioning
- Audience needs to explore graph dynamically
