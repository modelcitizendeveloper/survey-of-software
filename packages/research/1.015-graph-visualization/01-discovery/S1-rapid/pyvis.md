# PyVis (Python)

**GitHub:** ~1K stars | **Ecosystem:** Python | **License:** BSD-3-Clause

## Positioning

Purpose-built for network graph visualization with minimal code. Wraps vis.js JavaScript library to produce interactive HTML network diagrams. Optimized for simplicity over customization.

## Key Metrics

- **Performance:** vis.js rendering, ~5K-10K nodes practical limit
- **Download stats:** ~1.5M downloads/month on PyPI (Jan 2025)
- **Maintenance:** Moderate activity (updates every 3-6 months)
- **Python versions:** 3.6+ supported

## Visualization Capabilities

- Physics-based layout (nodes repel, edges attract)
- Interactive node dragging
- Click events for node details
- Hierarchical and custom layouts
- Export to standalone HTML

## Community Signals

**Stack Overflow sentiment:**
- "PyVis is the easiest way to get an interactive network graph - 5 lines of code"
- "Works great with NetworkX - just pass the graph object"
- "Limited customization but perfect for quick demos"

**Common use cases:**
- Knowledge graphs for documentation
- Organizational network visualization
- Dependency graph exploration
- Social network prototypes

## Trade-offs

**Strengths:**
- Extremely simple API (add nodes/edges, show graph)
- Direct NetworkX integration (from_nx method)
- Physics simulation creates natural layouts
- No JavaScript knowledge required
- Self-contained HTML output (share via email/Slack)

**Limitations:**
- Less control than Plotly/Cytoscape for advanced styling
- vis.js is no longer actively maintained (security risk for production)
- Poor performance on dense graphs (>10K nodes)
- Limited layout algorithms compared to Gephi

## Decision Context

**Choose PyVis when:**
- Need interactive HTML output with minimal code
- Working with NetworkX graphs already
- Prototyping or internal documentation
- Audience needs drag-and-drop exploration

**Skip if:**
- Production application (vis.js maintenance concerns)
- Need publication-quality layouts
- Working with massive graphs
- Require extensive customization control
