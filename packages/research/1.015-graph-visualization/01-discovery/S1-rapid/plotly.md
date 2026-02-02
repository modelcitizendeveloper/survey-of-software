# Plotly (Python)

**GitHub:** ~16K stars | **Ecosystem:** Python/JavaScript | **License:** MIT

## Positioning

Enterprise-grade interactive visualization platform. Graph visualization is one feature among many (charts, 3D plots, maps). Browser-based rendering with extensive customization.

## Key Metrics

- **Performance:** JavaScript rendering, handles ~10K-20K nodes smoothly
- **Download stats:** ~35M downloads/month on PyPI (Jan 2025)
- **Maintenance:** Active commercial backing (Plotly Technologies Inc.)
- **Python versions:** 3.6+ supported

## Visualization Capabilities

- Interactive pan/zoom in browser
- Hover tooltips with node metadata
- 2D and 3D network layouts
- Animation support (temporal graphs)
- Export to PNG, SVG, HTML

## Community Signals

**Stack Overflow sentiment:**
- "Plotly for interactive dashboards, NetworkX for algorithms - use both together"
- "Great for web apps, overkill for static reports"
- "Beautiful output but verbose API compared to matplotlib"

**Common use cases:**
- Dashboards with embedded network graphs
- Interactive exploratory analysis (Jupyter notebooks)
- Web applications requiring client-side interaction
- Temporal network animation

## Trade-offs

**Strengths:**
- Rich interactivity (hover, click, zoom) without JavaScript coding
- Integrates with Dash for full web applications
- Professional styling out-of-the-box
- Works seamlessly in Jupyter notebooks
- Both open-source and enterprise support options

**Limitations:**
- Heavier dependency (includes full chart library)
- Layout algorithms less sophisticated than specialized tools
- Requires building graph data structure manually (no NetworkX integration)
- Large HTML files for complex graphs (2-10MB typical)

## Decision Context

**Choose Plotly when:**
- Building web dashboards or Jupyter-based analysis
- Interactivity is essential (tooltips, filtering, zoom)
- Already using Plotly for other charts
- Need temporal graph animations

**Skip if:**
- Need specialized graph layouts (Gephi/Cytoscape quality)
- Working with massive graphs (>50K nodes)
- Prefer lightweight dependencies
- Only generating static images
