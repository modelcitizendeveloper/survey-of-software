# NetworkX + matplotlib - Technical Deep Dive

## Architecture

### Core Design
- **Graph storage:** Dictionary-of-dictionaries (node → neighbors → edge data)
- **Algorithm library:** Pure Python implementations of 400+ graph algorithms
- **Visualization:** Thin wrapper around matplotlib with layout algorithms
- **Data model:** Flexible attribute storage on nodes/edges

### Rendering Pipeline
1. Layout algorithm computes node positions (dict: node → (x, y))
2. matplotlib draws nodes as scatter plot
3. Edges drawn as line collections
4. Labels rendered as text annotations

## Performance Characteristics

### Scaling Limits
- **Practical limit:** 10K nodes (layout computation dominates)
- **Theoretical limit:** Millions of nodes (for algorithms only, not visualization)
- **Dense graph penalty:** O(n²) for force-directed layouts

### Benchmarks
- **Spring layout (5K nodes):** ~3 seconds on modern CPU
- **Spectral layout (5K nodes):** ~1 second (uses eigendecomposition)
- **Memory:** ~100MB for 10K node graph with attributes

### Layout Algorithm Complexity
- Spring/Fruchterman-Reingold: O(n² × iterations)
- Spectral: O(n³) due to eigenvalue computation
- Circular: O(n) - deterministic placement

## API Design

### Graph Construction
```python
# Flexible attribute model
G.add_node(1, label="Alice", age=30)
G.add_edge(1, 2, weight=0.5, relationship="friend")
```

### Visualization Pattern
```python
pos = nx.spring_layout(G)  # Layout separated from drawing
nx.draw(G, pos, with_labels=True)
```

**Key insight:** Layout and drawing are decoupled. Compute layout once, reuse positions for multiple renderings.

### Integration Strengths
- Direct conversion from Pandas adjacency matrices
- Export to standard formats (GEXF, GraphML, adjacency lists)
- Compatibility with SciPy sparse matrices

## Layout Algorithms

| Algorithm | Best For | Complexity | Notes |
|-----------|----------|------------|-------|
| spring_layout | General purpose | O(n²) | Fruchterman-Reingold |
| spectral_layout | Symmetric graphs | O(n³) | Uses Laplacian eigenvalues |
| circular_layout | Equal-importance nodes | O(n) | Simple, fast |
| shell_layout | Hierarchical clusters | O(n) | Manual shell assignment |
| kamada_kawai | Small graphs (<100) | O(n³) | High-quality but slow |

## Visualization Limitations

### What matplotlib Can't Do Well
- **Interactivity:** No hover tooltips, click events, or zoom
- **Large graphs:** Overlapping labels, illegible tangles
- **Aesthetics:** Basic styling, no anti-aliasing control
- **Web deployment:** Static images only

### Workarounds
- Export positions, visualize with Plotly: `plotly.graph_objs.Scatter(x=x, y=y)`
- Use Gephi/Cytoscape for final rendering
- Combine with PyVis: `pyvis.from_nx(G)`

## Advanced Features

### Subgraph Visualization
- Ego networks: `nx.ego_graph(G, node, radius=2)`
- Community coloring: Map partition to node colors
- Edge bundling: Not natively supported (manual implementation needed)

### Temporal Graphs
- No built-in animation
- Manual approach: Generate frames, combine with imageio/ffmpeg

## Memory Optimization

For large graphs (>50K nodes):
- Use `nx.to_scipy_sparse_array()` for adjacency operations
- Store node positions separately (dict → numpy array)
- Disable labels (`with_labels=False`)

## Ecosystem Position

**Core dependency for:**
- scikit-network (graph ML)
- graph-tool (if unavailable, falls back to NetworkX)
- PyVis, Plotly (use NetworkX as input format)

**Often combined with:**
- Pandas (node/edge dataframes)
- NumPy (matrix operations)
- matplotlib/seaborn (statistical graph plots)

## When NetworkX Shines

✅ **Ideal scenarios:**
- Exploratory data analysis (Jupyter notebooks)
- Algorithm prototyping (centrality, clustering)
- Scientific computing pipelines
- Teaching graph theory concepts

❌ **Poor fit:**
- Production dashboards (no interactivity)
- Large-scale visualization (performance cliff)
- Marketing/presentation materials (basic aesthetics)
