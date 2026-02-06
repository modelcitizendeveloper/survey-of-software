# PyVis - Technical Deep Dive

## Architecture

### Core Design
- **Backend:** vis.js (JavaScript network visualization library)
- **Python layer:** HTML template generator with vis.js configuration
- **Data model:** Nodes/edges list → JSON → vis.js Network object
- **Output:** Standalone HTML file with embedded vis.js library

### Rendering Pipeline
1. Python builds node/edge dictionaries
2. JSON serialization with vis.js options
3. HTML template generation (Jinja2)
4. Browser loads and renders vis.js physics simulation

## Performance Characteristics

### Scaling Limits
- **Practical limit:** 5K-10K nodes (physics simulation bottleneck)
- **Edge limit:** ~20K edges (rendering performance degrades)
- **File size:** 1-3MB typical (includes vis.js bundle)

### Physics Simulation
- **Real-time layout:** Barnes-Hut approximation (O(n log n))
- **Stabilization time:** 2-5 seconds for 5K nodes
- **Disable physics:** `net.toggle_physics(False)` for static layouts

### Browser Rendering
- **Initial render:** 1-2 seconds for 5K nodes
- **Interactivity:** Smooth drag/zoom up to 10K nodes
- **Canvas-based:** No WebGL, pure 2D canvas rendering

## API Design

### Simplified Interface
```python
net = Network(height='750px', width='100%')
net.add_node(1, label='Alice', color='blue')
net.add_edge(1, 2, weight=5)
net.show('network.html')
```

**Key strength:** Minimal API surface - add nodes/edges, configure physics, export.

### NetworkX Integration
```python
net.from_nx(G)
# Automatically converts NetworkX graph
# Preserves node/edge attributes as vis.js properties
```

**Convenience win:** No manual data extraction needed (unlike Plotly).

### Physics Configuration
```python
net.set_options("""
{
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -30000,
      "springLength": 200
    }
  }
}
""")
```

**Flexibility:** Direct access to vis.js options via JSON strings.

## Layout Algorithms

### Physics-Based (Default)
- **Barnes-Hut:** General-purpose force simulation
- **Repulsion:** Nodes repel, edges attract
- **Stabilization:** Iterative convergence to equilibrium

### Hierarchical Layout
```python
net.set_options("""
{
  "layout": {
    "hierarchical": {
      "direction": "UD",  # Up-Down
      "sortMethod": "directed"
    }
  }
}
""")
```

**Use case:** Directed acyclic graphs (DAGs), org charts, dependency trees.

## Styling Capabilities

### Node Customization
- **Shapes:** dot, square, triangle, star, box, ellipse
- **Colors:** Hex codes, gradients (border, background, highlight)
- **Sizes:** Pixel-based or scaled by attribute
- **Images:** Use image URLs as node shapes

### Edge Customization
- **Types:** Solid, dashed, dotted
- **Arrows:** Directional arrows (from, to, middle)
- **Curvature:** Smooth curves for multiple edges between same nodes
- **Dynamic width:** Scale by weight attribute

### Interactivity
- **Hover:** Node/edge highlighting
- **Click:** Custom JavaScript callbacks (requires manual editing)
- **Drag:** Physics simulation responds to dragged nodes
- **Zoom:** Mouse wheel zoom, panning

## Limitations

### vis.js Maintenance Status
- **Last release:** 2021 (v9.1.2)
- **Status:** Community-maintained, no active core development
- **Security:** No recent security patches
- **Future:** Uncertain long-term viability

**Implication:** Acceptable for internal tools, risky for production applications.

### Performance Bottlenecks
- **Dense graphs:** Poor performance on highly connected networks
- **Large graphs:** Physics simulation becomes unresponsive
- **No clustering:** Cannot collapse/expand subgraphs natively

### Browser Compatibility
- Modern browsers only (no IE support)
- Mobile performance is poor (touch events lag)
- Export requires headless browser (pyppeteer, selenium)

## Advanced Features

### Clustering
```python
# Manual clustering API
net.add_node(1, label='Cluster 1', shape='database')
net.add_node(2, group='cluster1')  # Group nodes visually
```

**Limitation:** No automatic community detection integration.

### Temporal Networks
- No built-in animation support
- Manual approach: Generate HTML files per timestep, link with navigation

### Export Options
- **HTML:** Default output (standalone file)
- **PNG/SVG:** Requires headless browser (not native)
- **JSON:** Export graph data for re-import

## Ecosystem Position

**Often paired with:**
- NetworkX (graph construction)
- Pandas (node/edge data from dataframes)
- Jupyter notebooks (inline rendering)

**Alternatives:**
- Plotly (more flexible, larger ecosystem)
- Cytoscape.js (modern JavaScript alternative to vis.js)

## When PyVis Shines

✅ **Ideal scenarios:**
- Quick prototypes with NetworkX graphs
- Internal documentation (knowledge graphs)
- Educational demos (physics simulation is engaging)
- Small-to-medium networks (<5K nodes)

❌ **Poor fit:**
- Production web applications (vis.js maintenance risk)
- Large-scale networks (>10K nodes)
- Mobile-responsive visualizations
- Advanced analytics (limited integration with graph libraries)

## Code Maintenance Considerations

### vis.js Alternatives
If vis.js risks are unacceptable:
- **Migrate to:** Plotly, Cytoscape.js, D3.js
- **Static fallback:** Export layout positions, render with matplotlib/Graphviz
- **Hybrid approach:** Use PyVis for prototyping, migrate to Plotly for production

### Long-term Strategy
PyVis is best viewed as a **rapid prototyping tool**, not a production framework. Plan migration paths if the project scales beyond demos.
