# Plotly - Technical Deep Dive

## Architecture

### Rendering Model
- **Backend:** plotly.js (D3.js-based JavaScript library)
- **Python layer:** Generates JSON specification, delegates to browser
- **Data model:** Graph objects (dict-like structures) serialized to JSON
- **Output:** HTML file with embedded plotly.js or iframe in Jupyter

### Network Graph Implementation
- Nodes: `Scatter` trace with mode='markers'
- Edges: `Scatter` trace with mode='lines' or line shapes
- Layout: External (use NetworkX, igraph, or manual positions)

## Performance Characteristics

### Scaling Limits
- **Practical limit:** 10K-20K nodes (browser rendering bottleneck)
- **Edge limit:** ~50K edges (WebGL mode extends this)
- **File size:** 2-10MB HTML for typical networks (includes plotly.js bundle)

### Rendering Performance
- **Initial load:** 1-3 seconds for 10K node graph
- **Interactivity:** Smooth pan/zoom up to 20K nodes
- **Hover tooltips:** Real-time up to 5K nodes, laggy beyond

### WebGL Acceleration
- Enable with `go.Scattergl()` instead of `go.Scatter()`
- Extends practical limit to 100K points
- Trade-off: Some styling features unavailable

## API Design

### Graph Construction Pattern
```python
# Manual edge/node specification
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    mode='lines',
    line=dict(width=0.5, color='#888')
)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    marker=dict(size=10, color='blue')
)
```

**Key insight:** Plotly has no native "graph" object. You build networks from scatter plots and line segments.

### Integration with NetworkX
```python
pos = nx.spring_layout(G)
# Extract x, y coordinates from pos dict
# Build edge_trace and node_trace manually
```

**Pain point:** No `from_networkx()` helper - requires manual data extraction.

### Customization Depth

**Node styling:**
- Size, color, opacity, symbol shape
- Hover text (HTML formatting supported)
- Click events (via Dash callbacks)

**Edge styling:**
- Width, color, dash patterns
- Curved edges (via Bezier splines)
- Directed arrows (with `arrowhead` parameter)

**Layout control:**
- Custom drag modes (pan, zoom, select)
- Annotations and shapes overlay
- 3D network graphs (`go.Scatter3d`)

## Advanced Features

### 3D Network Visualization
```python
node_trace_3d = go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(size=5, color=colors)
)
```

**Use case:** Temporal networks (time as Z-axis), high-dimensional embeddings

### Animation
- Frame-based animation for temporal graphs
- Slider controls for time-series networks
- Example: Network evolution over time

### Dash Integration
- Embed graphs in full-stack web apps
- Interactive callbacks (click node → update sidebar)
- Real-time updates (WebSocket data streams)

## Styling Capabilities

### Professional Theming
- Built-in templates: `plotly`, `plotly_white`, `plotly_dark`
- Custom color scales (continuous and discrete)
- Consistent styling across chart types

### Publication Quality
- Export to static images (PNG, SVG) via `pio.write_image()`
- Vector output preserves interactivity metadata
- LaTeX support in labels (via MathJax)

## File Size Optimization

### Reducing HTML Output
- Use CDN-hosted plotly.js: `include_plotlyjs='cdn'`
- Reduce precision: Round coordinates to 2 decimals
- Simplify large graphs: Sample nodes/edges

**Example savings:**
- Default: 3.5MB (plotly.js bundled)
- CDN mode: 150KB (loads plotly.js from CDN)

## Ecosystem Position

**Core component of:**
- Dash (Plotly's web framework)
- Jupyter ecosystem (nbformat support)
- Streamlit (via `st.plotly_chart()`)

**Alternatives within Plotly:**
- Graph objects (imperative): Full control, verbose
- Plotly Express (declarative): Simple API, limited graph support

## Interactivity Features

### Hover Tooltips
- Custom HTML templates
- Multi-line text with metadata
- Performance: Smooth up to 5K nodes

### Selection and Filtering
- Box select, lasso select
- Linked selections across multiple plots
- Callback-driven filtering (via Dash)

### Zoom and Pan
- Scroll zoom, double-click reset
- Axis range constraints
- Persistent zoom state in HTML exports

## When Plotly Shines

✅ **Ideal scenarios:**
- Web dashboards with multiple chart types
- Jupyter-based exploratory analysis
- Dash applications (full interactivity)
- Temporal network animation

❌ **Poor fit:**
- Specialized graph layouts (Gephi/Cytoscape quality)
- Massive graphs (>50K nodes)
- Offline static reports (large file sizes)
- Pure command-line workflows (requires browser)

## Performance Tuning

### For large graphs (>10K nodes):
1. Use `Scattergl` instead of `Scatter`
2. Reduce marker sizes (smaller = faster)
3. Disable hover text on edges
4. Simplify edge rendering (straight lines only)

### Memory optimization:
- Generate HTML without plotly.js bundle
- Use numpy arrays instead of Python lists
- Pre-compute layouts offline, save positions
