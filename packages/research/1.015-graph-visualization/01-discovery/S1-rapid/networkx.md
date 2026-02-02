# NetworkX + matplotlib (Python)

**GitHub:** ~15K stars | **Ecosystem:** Python | **License:** BSD-3-Clause

## Positioning

The de facto standard for graph algorithms in Python. Primarily an algorithmic library (shortest paths, centrality, communities) with basic matplotlib visualization as a secondary feature.

## Key Metrics

- **Performance:** Pure Python, slower than compiled libraries but sufficient for <10K nodes
- **Download stats:** ~45M downloads/month on PyPI (Jan 2025)
- **Maintenance:** Mature project (2002), active NumFOCUS-sponsored development
- **Python versions:** 3.9+ supported

## Visualization Capabilities

- Spring layout (Fruchterman-Reingold)
- Circular, shell, spectral layouts
- Static PNG/SVG output via matplotlib
- Basic node/edge styling (colors, sizes, labels)

## Community Signals

**Stack Overflow sentiment:**
- "NetworkX for algorithms, not visualization - use it with Plotly/PyVis for display"
- "Great for quick exploratory graphs, switch to Gephi for publication-quality"
- "The NumPy of graph theory - everyone uses it for computation"

**Common use cases:**
- Social network analysis (academic research)
- Graph algorithm prototyping
- Network topology analysis
- Citation network mapping

## Trade-offs

**Strengths:**
- Comprehensive algorithm library (400+ functions)
- SciPy/NumPy integration (scientific Python stack)
- Excellent documentation and tutorials
- Industry standard for graph computation

**Limitations:**
- Matplotlib visualization is basic (not interactive, limited styling)
- Slow on large graphs (>50K nodes)
- Layouts don't scale well visually
- Static output only (no web interactivity)

## Decision Context

**Choose NetworkX when:**
- You need graph algorithms first, visualization second
- Working in the scientific Python ecosystem
- Building computational pipelines (centrality, clustering, pathfinding)
- Prototyping graph analysis with familiar matplotlib plots

**Skip if:**
- Primary goal is beautiful/interactive visualization
- Need real-time graph updates
- Analyzing massive graphs (>100K nodes)
- Require web-based interactive exploration
