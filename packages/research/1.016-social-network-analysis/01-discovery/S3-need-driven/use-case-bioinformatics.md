# Use Case: Bioinformatics Researchers

## Who Needs This

**Persona**: Computational biologists, bioinformatics researchers analyzing molecular interaction networks, systems biology labs.

**Context**:
- Protein-protein interactions, gene regulatory networks, metabolic pathways
- Graph sizes: 10K-100M nodes (depends on omics data scale)
- Publication-driven (peer review standards for methods)
- Complex statistical analyses required
- Often integrating multiple data types

## Why They Need Social Network Analysis

**Primary objectives**:
1. **Pathway discovery**: Identify functional modules in biological networks
2. **Disease mechanisms**: Find dysregulated subnetworks in disease vs healthy
3. **Drug targets**: Detect key proteins in disease pathways
4. **Evolutionary analysis**: Compare networks across species
5. **Multi-omics integration**: Combine protein, gene, metabolite networks

**Key requirements**:
- **Advanced community detection**: Biological modules = communities
- **Statistical rigor**: Methods must be publishable
- **Scalability**: Some analyses involve millions of interactions
- **Reproducibility**: Peer review requires exact method replication
- **Integration**: Works with bioinformatics data (Pandas DataFrames, BioPython)

## Specific Constraints

**Scale**: Highly variable
- Small: Single pathway (100s of nodes)
- Medium: Proteome (10K-100K nodes)
- Large: Multi-omics (1M-100M interactions)

**Statistical requirements**: Publication standards
- Methods must be well-established or rigorously validated
- Need citations to published algorithms
- Reviewers scrutinize methodology

**Computational resources**: Variable
- Some labs: Powerful HPC clusters
- Others: Modest workstations
- Often need both (explore on laptop, scale on cluster)

## Best-Fit Library: graph-tool

**Why graph-tool wins for advanced analyses**:

1. **Stochastic Block Models**: State-of-the-art community detection for biological modules
2. **Statistical inference**: Bayesian methods for network structure
3. **Scalability**: Handles multi-omics scale (millions of interactions)
4. **Performance**: Fast enough for iterative analyses
5. **Academic rigor**: Methods published in top venues

**Trade-offs accepted**:
- Installation complexity: HPC admins can handle, worth it for capabilities
- Learning curve: Research teams can invest time
- LGPL license: Acceptable for academic research

## Alternative: NetworkX (for exploration)

**When to use**:
- Initial exploration of small networks (<10K nodes)
- Teaching/learning network analysis concepts
- Simple analyses (degree distribution, basic centrality)

**Why not primary**:
- Lacks advanced community detection (no SBM, Infomap)
- Too slow for large omics datasets
- Missing statistical inference methods

## Alternative: igraph (for standard analyses)

**When to use**:
- Standard community detection (Louvain, label propagation)
- Medium-scale networks (10K-1M nodes)
- Team prefers easier API than graph-tool

**Why not primary for cutting-edge research**:
- Missing SBM-based methods
- Fewer statistical inference tools
- Less suitable for reviewers expecting state-of-the-art

## Anti-fit Libraries

**snap.py**: Too limited for biology
- Missing biological network algorithms
- Narrow focus on web-scale social networks

**NetworKit**: Parallelism not the bottleneck
- Biological analyses often algorithm-limited, not compute-limited
- graph-tool's algorithms > NetworKit's parallelism for this domain

**CDlib**: Useful addition but not standalone
- Good for comparing community detection methods
- Should be used WITH graph-tool/igraph backend, not instead

## Example Requirements Mapping

**Protein interaction network**:
- 20K proteins, 200K interactions
- Find functional modules (communities), identify disease-related subnetworks
- **Library**: graph-tool (SBM for modules, statistical rigor)

**Gene regulatory network**:
- 5K genes, 15K regulatory edges
- Identify master regulators (centrality), detect regulatory modules
- **Library**: igraph (fast, established methods, easier API)

**Multi-omics integration**:
- 50M interactions (genes, proteins, metabolites)
- Large-scale module detection, integration across data types
- **Library**: graph-tool (only library handling this scale with advanced methods)

## Success Criteria

**Library is right fit if**:
✅ Provides algorithms reviewers will accept (published, validated)
✅ Handles data scale (from small pathways to full omics)
✅ Enables statistical rigor required for publication
✅ Integrates with bioinformatics workflow (Python data stack)
✅ Reproducible (others can install and run)

**Library is wrong fit if**:
❌ Missing critical algorithms (e.g., SBM for module detection)
❌ Too slow for iterative analysis
❌ Methods not academically rigorous enough for publication
❌ Can't handle multi-omics scale
