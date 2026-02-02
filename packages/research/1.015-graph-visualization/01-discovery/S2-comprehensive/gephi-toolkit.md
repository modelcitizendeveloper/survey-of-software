# gephi-toolkit - Technical Deep Dive

## Architecture

### Gephi Overview
- **Core:** Java desktop application for network visualization and analysis
- **Toolkit:** JAR library for programmatic access (headless Gephi)
- **Python integration:** Unofficial wrappers (subprocess calls, file intermediaries)
- **Data flow:** Python → GEXF/GraphML → Gephi Toolkit → Layout/Export

### Integration Approaches

**Method 1: File-based workflow**
```python
# NetworkX → GEXF → Gephi Desktop (manual)
nx.write_gexf(G, 'network.gexf')
# Open in Gephi desktop, apply layouts manually
```

**Method 2: Gephi Toolkit (Java)**
- Programmatic control via Java API
- Python wrappers use Jython or subprocess calls
- Complex setup, fragile integration

**Method 3: GephiStreamer (deprecated)**
- Stream data to running Gephi instance
- No longer maintained

## Performance Characteristics

### Scaling Limits (Gephi Desktop)
- **Practical limit:** 1M+ nodes (tested on social networks)
- **Edge limit:** 10M+ edges
- **Memory:** 8-32GB recommended for large graphs
- **Performance:** Force Atlas 2 is highly optimized (multi-threaded)

### Layout Performance

| Algorithm | 100K Nodes | 1M Nodes | Notes |
|-----------|------------|----------|-------|
| Force Atlas 2 | 30s | 5min | GPU acceleration available |
| OpenOrd | 60s | 10min | Multilevel approach |
| Yifan Hu | 45s | 8min | Fast force-directed |
| Fruchterman-Reingold | 120s | Impractical | Not optimized for scale |

**Key advantage:** Force Atlas 2 is the fastest high-quality layout for large networks.

### Memory Optimization
- Graph database backend (Gephi 0.9+)
- Disk-based storage for massive graphs
- Streaming API for incremental loading

## Gephi Toolkit API (Java)

### Headless Graph Processing
```java
// Example Gephi Toolkit code (not Python)
GraphModel graphModel = Lookup.getDefault()
    .lookup(GraphController.class)
    .getGraphModel();

Graph graph = graphModel.getGraph();
// Add nodes, apply layouts, export
```

**Python problem:** Requires JVM bridge (Jython, Py4J, subprocess) - all fragile.

## Layout Algorithms

### Force Atlas 2
- **Algorithm:** Modified Barnes-Hut simulation with scaling
- **Best for:** Large networks with communities
- **Parameters:**
  - `linLogMode`: Linear vs logarithmic attraction
  - `gravity`: Pull nodes to center
  - `scalingRatio`: Edge length tuning

**Unique feature:** LinLog mode reveals hierarchical structures.

### OpenOrd
- **Algorithm:** Multilevel force-directed (coarsening + refinement)
- **Best for:** Very large graphs (>100K nodes)
- **Output:** Clear community separation
- **Speed:** Comparable to Force Atlas 2 on massive graphs

### Yifan Hu
- **Algorithm:** Adaptive cooling schedule force-directed
- **Best for:** Medium graphs (10K-100K nodes)
- **Output:** Balanced layouts with good node spacing

## Python Integration Strategies

### Strategy 1: NetworkX → GEXF → Gephi Desktop (Recommended)
```python
import networkx as nx
nx.write_gexf(G, 'network.gexf')
# Open in Gephi, apply Force Atlas 2, export PNG
```

**Pros:** Reliable, no Python-Java bridge
**Cons:** Manual intervention required

### Strategy 2: Subprocess with Gephi Toolkit
```python
# Create GEXF, call Java with Gephi Toolkit JAR
subprocess.run(['java', '-jar', 'gephi-toolkit.jar',
                'input.gexf', 'output.png'])
```

**Pros:** Automated pipeline
**Cons:** Complex setup, brittle, not officially supported

### Strategy 3: Jython (Python running on JVM)
```python
# Use Jython to directly call Gephi Toolkit
from org.gephi.project.api import ProjectController
# Full Gephi API access
```

**Pros:** Direct API access
**Cons:** Jython is Python 2.7, incompatible with modern libraries

## Gephi Desktop Features

### Interactive Exploration
- **Overview:** Graph-level layouts and filtering
- **Data Laboratory:** Spreadsheet view of nodes/edges
- **Preview:** Export configuration with anti-aliasing, fonts

### Statistical Analysis
- **Centrality:** Degree, betweenness, closeness, eigenvector
- **Communities:** Modularity (Louvain algorithm)
- **Paths:** Shortest paths, diameter, average path length
- **Clustering:** Clustering coefficient

### Filtering
- **Topology filters:** Degree range, giant component extraction
- **Attribute filters:** Numeric/categorical value ranges
- **Partition filters:** Color by community, group by attribute

### Timeline
- **Dynamic networks:** Temporal graph animation
- **Timeline control:** Scrub through time steps
- **Export:** Animated GIF, video export (via ffmpeg)

## Export Options

### Image Formats
- **PNG:** High-resolution raster (up to 8K resolution)
- **SVG:** Vector graphics (editable in Illustrator)
- **PDF:** Publication-quality output

### Export Settings
- **Anti-aliasing:** Smooth edges and text
- **Background:** Transparent or colored
- **Margins:** Padding around graph
- **Show labels:** Node labels, edge labels, customizable fonts

### Data Formats
- **GEXF:** Gephi native format (preserves all metadata)
- **GraphML:** Standard interchange
- **CSV:** Node/edge lists with attributes
- **Pajek:** Legacy format for social network analysis

## Ecosystem Position

### Desktop Alternative to
- **Cytoscape:** Gephi is faster, Cytoscape has better bioinformatics integration
- **NodeXL:** Gephi is cross-platform, NodeXL is Excel-based (Windows only)
- **Pajek:** Gephi has modern UI, Pajek has more algorithms

### Complementary Tools
- **NetworkX:** Analysis in Python, visualization in Gephi
- **igraph:** R/Python analysis, Gephi for final layouts
- **D3.js:** Gephi for static, D3 for web interactivity

## Community and Plugins

### Popular Plugins
- **GeoLayout:** Geographic network layouts
- **Sigma.js Exporter:** Interactive web exports
- **Multimode Networks Projection:** Bipartite graph analysis
- **Circular Layout:** Enhanced circular layouts

### Data Sources
- **Twitter Streaming Importer:** Live social network capture
- **Graph Database Connector:** Neo4j integration
- **Spreadsheet Import:** Excel/CSV import wizards

## When Gephi (via Python) Makes Sense

### Viable Use Case
```python
# Analysis pipeline
import networkx as nx

# 1. Build graph in Python
G = build_large_network()  # 500K nodes

# 2. Export to GEXF
nx.write_gexf(G, 'network.gexf')

# 3. Manual step: Open in Gephi
#    - Apply Force Atlas 2
#    - Set node sizes by degree
#    - Export publication-quality PNG

# 4. Continue Python analysis
```

**When this works:** You're willing to accept manual intervention for visualization.

### When to Avoid
- Fully automated pipelines (no manual steps allowed)
- Web application backends (desktop dependency)
- Lightweight scripts (multi-GB installation)
- Non-technical users (steep learning curve)

## Force Atlas 2 Comparison

**Why Gephi's Force Atlas 2 is unique:**
- Multi-threaded (uses all CPU cores)
- GPU-accelerated version available (OpenCL plugin)
- Optimized for massive graphs (tested on 1M+ nodes)
- LinLog mode reveals hierarchical patterns (not in standard force-directed)

**Alternatives:**
- NetworkX spring_layout: Python, but slow (O(n²))
- Plotly/PyVis: Interactive, but can't handle >20K nodes
- Graphviz sfdp: Fast, but static output only

**Verdict:** For large graph visualization quality, Force Atlas 2 is unmatched. But Python integration is painful.

## Practical Recommendation

**Use Gephi as a desktop tool, not via Python:**
1. Build and analyze graphs in Python (NetworkX, igraph)
2. Export to GEXF or GraphML
3. Open in Gephi desktop for visualization
4. Export high-resolution images
5. Import results (if needed) back to Python

**Avoid:** Attempting to script Gephi Toolkit from Python. The integration layer is not mature.
