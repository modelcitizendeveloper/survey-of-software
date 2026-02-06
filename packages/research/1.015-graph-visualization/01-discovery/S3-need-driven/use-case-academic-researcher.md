# Use Case: Academic Researcher

## Who Needs This

**Persona:** Dr. Maria Chen, sociology PhD candidate
- Analyzing Twitter follower networks (15K nodes)
- Publishing in peer-reviewed journals (Nature, PNAS)
- Familiar with Python basics, uses Pandas for data analysis
- Works in Jupyter notebooks on university servers
- Needs reproducible research pipeline

**Context:** Studying information diffusion in online communities. Must generate publication-quality figures, document methodology, and share code with reviewers.

## Why They Need Graph Visualization

**Problem:**
- Network structure reveals community patterns (who influences whom)
- Must demonstrate findings visually for peer review
- Editors require high-resolution figures (300+ DPI)
- Reviewers expect reproducible analysis code

**Success Criteria:**
- ✅ Publication-quality static images (vector format preferred)
- ✅ Reproducible layout (same graph → same visualization)
- ✅ Statistical rigor (centrality, modularity metrics integrated)
- ✅ Code sharing (GitHub repo for peer verification)

## Requirements

### Technical
- **Scale:** 10K-50K nodes (Twitter follower networks)
- **Algorithms:** Community detection, centrality measures
- **Output:** PNG/SVG at 300 DPI, PDF for LaTeX integration
- **Reproducibility:** Deterministic layouts (fixed random seed)

### Workflow
- Data cleaning in Pandas
- Network analysis (degree distribution, clustering coefficient)
- Visualization for paper figures
- Export for LaTeX document

### Constraints
- No commercial licenses (grant-funded research)
- Must work on university cluster (Linux, no GUI)
- Code must be shareable (open-source license)

## Recommended Solution

### Primary: NetworkX + matplotlib

**Why this choice:**
1. **Scientific Python ecosystem:** Integrates with Pandas, NumPy, SciPy (already in use)
2. **Algorithm library:** 400+ functions for network analysis (no secondary tools needed)
3. **Matplotlib integration:** Publication-quality output matching other paper figures
4. **Reproducibility:** Deterministic layouts with random seeds
5. **Open source:** BSD license, acceptable for journal code sharing

**Workflow:**
```python
import networkx as nx
import matplotlib.pyplot as plt

# Analysis
G = nx.from_pandas_edgelist(df, 'follower', 'followed')
communities = nx.community.louvain_communities(G)
centrality = nx.betweenness_centrality(G)

# Visualization
pos = nx.spring_layout(G, seed=42)  # Reproducible
nx.draw_networkx(G, pos, node_color=community_colors,
                 node_size=[centrality[n]*1000 for n in G.nodes()])
plt.savefig('network.pdf', dpi=300, bbox_inches='tight')
```

**Output:** Vector graphics matching journal requirements.

### Secondary: Graphviz (for specific layouts)

**When to use:**
- Need hierarchical layout (information cascades, retweet trees)
- Directed acyclic graphs (diffusion pathways)
- Deterministic positioning required (not force-directed)

**Example:** Visualizing retweet propagation from seed tweet.

### Avoid: Plotly, PyVis

**Why not Plotly:**
- Interactive HTML doesn't fit paper format (journals want static figures)
- Overkill for static output (adds dependency complexity)
- Export quality is good but matplotlib is better integrated

**Why not PyVis:**
- No value-add for static publication figures
- vis.js dependency irrelevant for academic use case

## Alternative Scenarios

### If Working with Biological Networks
**Switch to:** py4cytoscape
- Cytoscape is domain standard in biology/bioinformatics
- Reviewers expect Cytoscape-generated figures
- Pathway enrichment analysis integrated

### If Network is Massive (>100K nodes)
**Switch to:** Graphviz sfdp or Gephi desktop
- NetworkX spring layout becomes impractical (hours to compute)
- Graphviz sfdp handles large graphs efficiently
- Gephi for exploratory analysis, export positions, render with NetworkX

### If Need Interactive Supplementary Material
**Add:** Plotly for journal supplementary files
- Some journals accept interactive HTML supplements
- Export NetworkX positions, build Plotly visualization
- Readers can explore full network in browser

## Implementation Path

### Phase 1: Analysis (NetworkX)
- Load data from CSV/database
- Compute network metrics
- Detect communities
- Calculate centrality measures

### Phase 2: Visualization (matplotlib)
- Layout with spring_layout (or spectral for symmetric graphs)
- Map analysis results to visual properties (size, color)
- Export publication-quality figures

### Phase 3: Documentation (Jupyter)
- Document methodology in notebook
- Share code on GitHub
- Include requirements.txt for reproducibility

### Phase 4: Submission
- Embed figures in LaTeX manuscript
- Upload code to journal-specific repository (if required)
- Prepare response to reviewers with regenerated figures

## Tools Comparison for This Use Case

| Library | Fit Score | Reasoning |
|---------|-----------|-----------|
| NetworkX + matplotlib | ⭐⭐⭐⭐⭐ | Perfect fit - algorithms + publication output |
| Graphviz | ⭐⭐⭐⭐ | Good for hierarchical, but less flexible |
| py4cytoscape | ⭐⭐ | Only if biological data |
| Plotly | ⭐⭐ | Overengineered for static papers |
| PyVis | ⭐ | No benefit for this use case |
| Gephi | ⭐⭐⭐ | Good for exploration, but desktop-only |

## Success Indicators

**This recommendation works if:**
- ✅ Graphs fit in memory (<100K nodes)
- ✅ Static figures are acceptable
- ✅ Researcher comfortable with Python
- ✅ Integration with scientific Python stack needed

**Reconsider if:**
- ❌ Need interactive figures (add Plotly for supplements)
- ❌ Network is massive (use Gephi for exploration)
- ❌ Biological domain (switch to py4cytoscape)
