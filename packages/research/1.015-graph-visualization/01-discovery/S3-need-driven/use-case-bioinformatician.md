# Use Case: Bioinformatician

## Who Needs This

**Persona:** Dr. Priya Patel, bioinformatics researcher at cancer research institute
- Analyzing protein-protein interaction networks (50K proteins, 200K interactions)
- Publishing in high-impact journals (Cell, Nature Genetics)
- Integrating pathway databases (KEGG, Reactome, STRING)
- Needs reproducible pipelines for genomic data analysis
- Collaborates with wet-lab biologists (non-programmers)

**Context:** Identifying disease-associated protein modules in cancer. Must integrate multi-omics data, visualize pathways, and generate publication-quality figures that meet biology journal standards.

## Why They Need Graph Visualization

**Problem:**
- Protein interaction networks reveal disease mechanisms (which proteins work together)
- Must overlay experimental data (gene expression, mutations) on network structure
- Reviewers expect specific layout conventions (biological pathways have standard layouts)
- Wet-lab collaborators need interpretable visualizations (not raw data)
- Findings must compare to published pathways (Reactome, KEGG standards)

**Success Criteria:**
- ✅ Publication-quality figures (Nature/Cell journal standards)
- ✅ Standard biological layouts (pathway conventions, not arbitrary)
- ✅ Multi-omics data integration (expression, mutations, phosphorylation overlaid)
- ✅ Reproducible analysis pipeline (R/Python code sharing)
- ✅ Pathway enrichment analysis (automated annotations)

## Requirements

### Technical
- **Scale:** 10K-100K nodes (protein networks), 50K-500K edges
- **Algorithms:** Pathway enrichment, module detection, centrality
- **Layout:** Biological conventions (hierarchical for signaling, clustered for complexes)
- **Data integration:** Overlay gene expression, mutations, phosphorylation states
- **Output:** High-resolution PNG/PDF (300+ DPI), vector formats for figures

### Workflow
- Query protein interaction databases (STRING, BioGRID)
- Integrate omics data (RNA-seq, proteomics, mutations)
- Detect disease-associated modules
- Visualize pathways with experimental data overlaid
- Export publication figures
- Share analysis code with reviewers

### Constraints
- Must use domain-standard tools (reviewers expect Cytoscape)
- Reproducible (same data → same network layout)
- Scripted (no manual positioning for 50K+ nodes)
- Open-source (grant-funded research)

## Recommended Solution

### Primary: py4cytoscape (Cytoscape desktop + Python)

**Why this choice:**
1. **Domain standard:** Cytoscape is THE tool for biological networks (reviewers expect it)
2. **Biological layouts:** Optimized for pathways, protein complexes, signaling cascades
3. **Omics integration:** Built-in tools for expression overlays, mutation mapping
4. **Pathway databases:** Direct import from KEGG, Reactome, WikiPathways
5. **App ecosystem:** 1000+ Cytoscape apps for specialized analyses (ClueGO, stringApp, ReactomeFI)
6. **Publication quality:** Meets Nature/Cell figure standards

**Workflow:**
```python
import py4cytoscape as p4c
import pandas as pd

# Import protein interaction network from STRING
p4c.commands_post('string protein query query="BRCA1"')  # STRING app

# Or build from custom data
proteins_df = pd.read_csv('proteins.csv')  # id, name, type
interactions_df = pd.read_csv('interactions.csv')  # source, target, score

suid = p4c.create_network_from_data_frames(
    nodes=proteins_df,
    edges=interactions_df,
    title='BRCA1 Interaction Network'
)

# Overlay gene expression data
expression_df = pd.read_csv('rnaseq_results.csv')  # protein_id, log2fc, padj
p4c.load_table_data(expression_df, data_key_column='protein_id')

# Visual mapping (expression → color)
p4c.set_node_color_mapping(
    table_column='log2fc',
    mapping_type='c',  # Continuous
    colors=['blue', 'white', 'red'],
    points=[-2, 0, 2]
)

# Apply biological layout
p4c.layout_network('force-directed')  # Or: 'hierarchical', 'organic'

# Export high-resolution figure
p4c.export_image('figure_2a.png', type='PNG', resolution=300)
p4c.export_image('figure_2a.pdf', type='PDF')
```

**Output:** Publication-ready figure with expression data overlaid on network.

### Advanced: Pathway Enrichment
```python
# Install ClueGO app (Gene Ontology enrichment)
# Via Cytoscape app manager

# Run enrichment on selected nodes
p4c.select_nodes(['TP53', 'BRCA1', 'ATM', 'CHEK2'])  # DNA damage response
# Use ClueGO via Cytoscape GUI or commands API

# Result: Annotated pathway clusters colored by function
```

### Alternative: NetworkX + py4cytoscape (for complex analysis)

**When to use:**
- Need graph algorithms not in Cytoscape (custom centrality, specialized clustering)
- Computational analysis in Python, visualization in Cytoscape

**Pattern:**
```python
import networkx as nx
import py4cytoscape as p4c

# Complex analysis in NetworkX
G = nx.read_edgelist('interactions.txt')
betweenness = nx.betweenness_centrality(G)
communities = nx.community.louvain_communities(G)

# Add results as node attributes
nx.set_node_attributes(G, betweenness, 'betweenness')
nx.set_node_attributes(G, {n: i for i, comm in enumerate(communities)
                            for n in comm}, 'community')

# Transfer to Cytoscape for visualization
p4c.create_network_from_networkx(G, title='Analyzed Network')
p4c.set_node_size_mapping('betweenness', [10, 100])
p4c.set_node_color_mapping('community', style_name='default')
```

**Benefit:** Python's analytical power + Cytoscape's visualization quality.

### Avoid: General-purpose tools (NetworkX, Plotly, PyVis)

**Why not NetworkX matplotlib:**
- Layouts don't follow biological conventions
- No pathway database integration
- Reviewers expect Cytoscape-quality figures
- Missing domain-specific features (GO enrichment, pathway import)

**Why not Plotly:**
- Not standard in biology (reviewers unfamiliar)
- No direct pathway database integration
- Biological apps (stringApp, ReactomeFI) only work with Cytoscape

**Why not Gephi:**
- Less biological tooling than Cytoscape
- Bioinformatics community centered on Cytoscape
- Python integration is worse than py4cytoscape

## Real-World Example: Cancer Pathway Analysis

### Step 1: Query Disease-Associated Genes
```python
# Get genes from TCGA cancer genomics
cancer_genes = ['TP53', 'KRAS', 'EGFR', 'PIK3CA', 'PTEN']  # Example

# Import STRING network
p4c.commands_post(f'string protein query query="{",".join(cancer_genes)}" species="Homo sapiens"')
```

### Step 2: Integrate Multi-Omics Data
```python
# RNA-seq expression
rnaseq = pd.read_csv('tumor_vs_normal_expression.csv')
p4c.load_table_data(rnaseq, data_key_column='gene')

# Somatic mutations
mutations = pd.read_csv('mutation_frequencies.csv')
p4c.load_table_data(mutations, data_key_column='gene')

# Visual mapping
p4c.set_node_color_mapping('log2fc', colors=['blue', 'white', 'red'])
p4c.set_node_border_width_mapping('mutation_freq', [1, 10])
```

### Step 3: Module Detection
```python
# Cytoscape's MCODE app for protein complexes
p4c.commands_post('mcode cluster degreeCutoff=2')

# Result: Disease-associated protein modules highlighted
```

### Step 4: Pathway Enrichment
```python
# ReactomeFI app
p4c.commands_post('reactomefi analyze')

# Output: Modules annotated with Reactome pathways
# Example: "DNA Damage Response", "EGFR Signaling", "Apoptosis"
```

### Step 5: Export for Publication
```python
p4c.export_image('figure_3_cancer_network.png', resolution=300)
p4c.export_image('figure_3_cancer_network.pdf')  # For journal submission
p4c.save_session('analysis.cys')  # For reviewers/supplementary materials
```

## Alternative Scenarios

### If Need Web-Based Collaboration
**Add:** Cytoscape.js export
- Export to Cytoscape.js JSON
- Build web viewer for collaborators (no Cytoscape install needed)
- Useful for sharing with wet-lab biologists

### If Cytoscape is Unavailable (HPC Cluster)
**Switch to:** NetworkX + Graphviz
- Analysis with NetworkX
- Hierarchical layouts with Graphviz
- Accept lower figure quality (fallback solution)

### If Building Automated Pipeline (No Desktop)
**Challenge:** py4cytoscape requires desktop
**Solution:**
- Headless Cytoscape (Xvfb on Linux)
- CI/CD with Xvfb wrapper: `xvfb-run -a python analysis.py`
- Docker with Xvfb for reproducibility

## Tools Comparison for This Use Case

| Library | Fit Score | Reasoning |
|---------|-----------|-----------|
| py4cytoscape | ⭐⭐⭐⭐⭐ | Perfect - domain standard, pathway tools, publication quality |
| NetworkX + Cytoscape | ⭐⭐⭐⭐ | Good - analysis in Python, viz in Cytoscape |
| Graphviz | ⭐⭐ | Hierarchical layouts decent, but no omics integration |
| NetworkX + matplotlib | ⭐⭐ | Analysis OK, visualization not publication-ready |
| Plotly | ⭐ | Not domain-standard, missing biological tooling |
| Gephi | ⭐⭐ | Good layouts, but less biological support |

## Success Indicators

**This recommendation works if:**
- ✅ Working with biological networks (pathways, protein interactions, gene regulation)
- ✅ Publishing in biology journals (need domain-standard tools)
- ✅ Need omics data integration (expression, mutations, PTMs)
- ✅ Acceptable to install Cytoscape desktop
- ✅ Reproducibility is critical (save sessions, export code)

**Reconsider if:**
- ❌ Pure graph algorithms (non-biological) - use NetworkX
- ❌ Web-only deployment (Cytoscape is desktop) - use Cytoscape.js export
- ❌ Minimal dependencies (can't install desktop) - fallback to NetworkX + Graphviz
- ❌ Non-biological domain - Cytoscape is overkill

## Reproducibility Best Practices

### Session Management
```python
# Save full analysis session
p4c.save_session('analysis_v1.cys')

# Version control key files (not CYS - it's binary)
# - Python analysis scripts
# - Input data files
# - Exported images/tables

# Document Cytoscape version
cytoscape_version = p4c.cytoscape_version_info()
print(f"Cytoscape {cytoscape_version['cytoscapeVersion']}")
```

### Sharing with Reviewers
- Upload CYS file to journal supplementary materials
- Share Python scripts on GitHub
- Document Cytoscape app versions (stringApp 1.7, MCODE 2.0, etc.)
- Export to XGMML (text format, easier to diff)

**Result:** Reviewers can reproduce visualizations exactly.
