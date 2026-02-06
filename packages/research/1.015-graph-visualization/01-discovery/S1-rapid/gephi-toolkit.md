# gephi-toolkit (Python)

**GitHub:** N/A (unofficial bindings) | **Ecosystem:** Python + Gephi (Java) | **License:** Varies

## Positioning

Python wrappers for Gephi's programmatic toolkit. Gephi is a desktop application famous for large-scale network visualization and exploration. Toolkit enables headless automation but has fragmented Python support.

## Key Metrics

- **Performance:** Java-based, handles 1M+ nodes (Gephi's strength)
- **Download stats:** Limited (no official PyPI package, multiple unofficial wrappers)
- **Maintenance:** Gephi core is active, Python bindings are community-maintained (variable quality)
- **Python versions:** Varies by wrapper implementation

## Visualization Capabilities

- Force Atlas 2 layout (Gephi's signature algorithm)
- OpenOrd, Fruchterman-Reingold layouts
- Modularity-based community detection
- Export to GEXF, GraphML, PNG, SVG, PDF
- Timeline and dynamic graph support

## Community Signals

**Stack Overflow sentiment:**
- "Gephi is amazing for exploration, terrible for programmatic access"
- "Use Gephi desktop manually, Python automation isn't mature"
- "Force Atlas 2 is the best large-graph layout - worth the Java dependency"

**Common use cases:**
- Social network exploration (Twitter, Facebook networks)
- Large-scale graph analysis (million+ node networks)
- Investigative journalism (leaked data network analysis)
- Academic research with manual refinement needs

## Trade-offs

**Strengths:**
- Force Atlas 2 is industry-leading for large networks
- Gephi handles massive datasets (1M+ nodes tested)
- Rich plugin ecosystem for specialized analysis
- Beautiful visual output for presentations

**Limitations:**
- No official Python API (community wrappers are fragmented)
- Requires Gephi desktop or toolkit JAR files
- Heavyweight Java dependency
- Python integration is hacky (subprocess calls, file intermediaries)
- Better suited for interactive desktop use than automation

## Decision Context

**Choose gephi-toolkit when:**
- Need Force Atlas 2 layout specifically
- Working with massive networks (>500K nodes)
- Willing to manage Java dependencies
- Python is for preprocessing, Gephi desktop for final visualization

**Skip if:**
- Need clean Python-native workflow
- Prefer maintained, official libraries
- Building automated pipelines (fragile integration)
- Want simple deployment (avoid Java dependencies)

## Implementation Reality

Most practitioners use Gephi as a desktop tool and export data from Python (NetworkX → GEXF → Gephi) rather than attempting programmatic control via Python.
