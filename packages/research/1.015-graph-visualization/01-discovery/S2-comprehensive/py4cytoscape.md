# py4cytoscape - Technical Deep Dive

## Architecture

### Client-Server Model
- **Cytoscape Desktop:** Java application with REST API (CyREST plugin)
- **py4cytoscape:** Python HTTP client calling Cytoscape REST endpoints
- **Data flow:** Python → HTTP → Cytoscape → Rendering/Analysis
- **State:** Cytoscape maintains network state, Python sends commands

### Communication Protocol
```python
# Example HTTP call (abstracted by py4cytoscape)
POST http://localhost:1234/v1/networks
{
  "collection": "My Network",
  "nodes": [...],
  "edges": [...]
}
```

**Key insight:** py4cytoscape is a remote control, not a standalone library.

## Performance Characteristics

### Scaling Limits
- **Practical limit:** 100K nodes (Cytoscape desktop performance)
- **Tested maximum:** 1M+ nodes (requires 16GB+ RAM)
- **Edge limit:** 500K edges (rendering slows beyond this)

### Layout Performance

| Algorithm | 10K Nodes | 100K Nodes | Notes |
|-----------|-----------|------------|-------|
| Prefuse Force Directed | 5s | 60s | General purpose |
| Organic (yFiles) | 3s | 30s | Fast, good quality |
| Hierarchical | 2s | 20s | For DAGs |
| Circular | 1s | 10s | Simple layouts |

**Memory:** Cytoscape desktop uses 2-8GB for large networks.

### Network Transfer
- **Overhead:** JSON serialization + HTTP
- **Large networks:** 10-30 seconds to transfer 50K node graph
- **Optimization:** Batch operations, minimize round-trips

## API Design

### Network Creation
```python
import py4cytoscape as p4c

# Create network from node/edge lists
nodes = [{'id': 'A'}, {'id': 'B'}]
edges = [{'source': 'A', 'target': 'B'}]
suid = p4c.create_network_from_data_frames(nodes_df, edges_df)
```

### Styling Pipeline
```python
# Set visual properties
p4c.set_node_color_default('#AAAAAA')
p4c.set_node_size_mapping('degree', [10, 50])
p4c.set_edge_width_mapping('weight', [1, 10])
```

**Pattern:** Imperative commands modifying remote state.

### NetworkX Integration
```python
# Import from NetworkX
p4c.create_network_from_networkx(G, title='My Graph')
```

**Convenience:** Direct import without manual data extraction.

## Layout Algorithms

### Cytoscape Core Layouts
- **Prefuse Force Directed:** Spring embedder, general purpose
- **Attribute Circle:** Group by attribute values
- **Grid:** Rows and columns layout
- **Hierarchical:** Directed graphs with levels

### yFiles Layouts (Commercial Plugin)
- **Organic:** High-quality force-directed
- **Hierarchical:** Sugiyama with edge bundling
- **Circular:** Circular with hierarchy
- **Orthogonal:** Right-angle edges (circuit diagrams)

**Note:** yFiles requires separate license for commercial use.

### Layout Tuning
```python
p4c.layout_network('force-directed',
                   defaultSpringLength=100,
                   defaultNodeMass=10)
```

**Flexibility:** Fine-grained control over algorithm parameters.

## Styling Capabilities

### Visual Mapping
- **Passthrough:** Direct attribute values (e.g., `color` → node color)
- **Continuous:** Numeric attributes → color gradients, sizes
- **Discrete:** Categorical attributes → distinct colors/shapes

### Node Styles
- **Shapes:** 20+ built-in (ellipse, rectangle, triangle, hexagon, etc.)
- **Colors:** Border, fill, label colors
- **Transparency:** Alpha channel for overlapping nodes
- **Images:** URL-based images as node backgrounds

### Edge Styles
- **Types:** Solid, dashed, dotted
- **Arrows:** 10+ arrowhead types (normal, delta, circle, T)
- **Routing:** Straight, curved, orthogonal, arc
- **Bundling:** Edge bundling for reducing visual clutter

### Advanced Styling
- **Bypass:** Override style for specific nodes/edges
- **Conditional:** Rules based on multiple attributes
- **Templates:** Save/load style configurations

## Analysis Integration

### Network Statistics
```python
# Compute centrality
degree = p4c.analyze_network('degree')
betweenness = p4c.analyze_network('betweenness')

# Apply to visual properties
p4c.set_node_size_mapping('degree', [10, 100])
```

**Workflow:** Analyze → Map results to visual properties.

### Community Detection
- **Algorithms:** GLay, MCODE, clusterMaker2
- **Output:** Node clusters, modularity scores
- **Visualization:** Color nodes by cluster

### Enrichment Analysis
- **Pathway enrichment:** BiNGO, ClueGO (bioinformatics)
- **Gene Ontology:** Automated annotation
- **Integration:** Results displayed as network annotations

## Export Options

### Image Formats
- **PNG:** Raster export at custom DPI
- **SVG:** Vector graphics (editable in Inkscape/Illustrator)
- **PDF:** Publication-quality output
- **PostScript:** Legacy print workflows

### Data Formats
- **CYS:** Cytoscape session (all networks + styles)
- **XGMML:** XML graph format
- **GraphML:** Standard interchange format
- **JSON:** Cytoscape.js compatible

### Programmatic Export
```python
# Export current network
p4c.export_image('network.png', type='PNG', resolution=300)
p4c.export_network('network.graphml', type='GraphML')
```

## Ecosystem Position

### Cytoscape App Ecosystem
- **1000+ apps:** Specialized analysis, import/export, styling
- **Accessible from Python:** Launch apps via py4cytoscape
- **Examples:** stringApp (protein networks), ReactomeFI (pathways)

### Integration Points
- **NetworkX:** Bidirectional conversion
- **Pandas:** Node/edge dataframes
- **igraph:** Via GraphML export/import
- **R (RCy3):** R equivalent of py4cytoscape

## Advanced Features

### Subnetwork Creation
```python
# Extract ego network
p4c.select_first_neighbors()
p4c.create_subnetwork_from_selection()
```

**Use case:** Focus on local neighborhoods.

### Temporal Networks
- **Manual:** Create networks per timestep, link with app
- **TS-Tools app:** Specialized temporal analysis

### Batch Processing
```python
# Process multiple networks
for file in network_files:
    suid = p4c.import_network_from_file(file)
    p4c.layout_network('hierarchical')
    p4c.export_image(f'{file}.png')
```

## Production Considerations

### Desktop Dependency
- **Requirement:** Cytoscape desktop must be running
- **Automation:** Start Cytoscape programmatically (platform-specific)
- **Headless:** Possible with Xvfb (Linux) or hidden windows (Windows)

### CI/CD Challenges
- **Docker:** Requires X11 server or Xvfb
- **Cloud:** Not suitable for serverless architectures
- **Alternative:** Export positions, render with Plotly/matplotlib

### Version Compatibility
- **Cytoscape versions:** 3.7+ supported
- **py4cytoscape:** Tied to CyREST API versions
- **Breaking changes:** Rare but possible with major Cytoscape updates

## When py4cytoscape Shines

✅ **Ideal scenarios:**
- Biological pathway visualization (protein interactions, gene networks)
- Publication-quality figures (Nature/Science standards)
- Large network analysis (>50K nodes)
- Reproducible research pipelines (computational biology)

❌ **Poor fit:**
- Web applications (requires desktop install)
- Lightweight scripts (heavy dependency)
- Real-time visualization (desktop app overhead)
- Non-biological domains (overkill for general graphs)

## Typical Workflow

1. **Data preparation:** Build NetworkX graph or Pandas dataframes
2. **Import:** `p4c.create_network_from_networkx(G)`
3. **Analysis:** Run centrality, clustering algorithms
4. **Styling:** Map analysis results to visual properties
5. **Layout:** Apply specialized layout algorithm
6. **Export:** Generate high-resolution images for publication

**Time investment:** 30-60 minutes for complex network (vs. hours in Gephi desktop).
