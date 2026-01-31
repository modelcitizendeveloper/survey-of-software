# Use Case: Bioinformatics Researchers

## Who Needs This

**Persona:** Dr. Chen, Computational Biology Postdoc

**Role:** Analyzes protein-protein interaction (PPI) networks to identify functional modules

**Organization:** University research lab (systems biology)

**Technical background:** PhD in biology + bioinformatics training, proficient Python/R

**Team size:** Solo researcher with occasional undergrad help

## Why Community Detection Matters

### Problem 1: Protein Complex Identification

**Challenge:** Identify multi-protein complexes from interaction data
- PPI network: 5K proteins, 20K interactions (from yeast two-hybrid screens)
- Known complexes: RNA polymerase II (12 proteins), ribosome (80 proteins)
- Goal: Find novel complexes for experimental validation

**Why it matters:**
- Protein complexes = functional units (like molecular machines)
- Discovering novel complex = potential publication
- Experimental validation costs $10K-50K per complex (must prioritize)

**Without community detection:**
- Literature review (misses novel complexes)
- Manual network browsing (biased, not exhaustive)
- Simple clique finding (too restrictive, misses loose complexes)

**With community detection:**
- Automated discovery of 200-500 candidate complexes
- Rank by biological plausibility (GO term enrichment)
- Prioritize top 10 for experimental validation

### Problem 2: Pathway Module Discovery

**Challenge:** Find functional modules in metabolic pathways
- Metabolic network: 1K enzymes, 3K reactions
- Goal: Identify pathways that work together
- Example: glycolysis, TCA cycle, oxidative phosphorylation

**Value:**
- Understanding disease mechanisms (cancer rewires metabolism)
- Drug target identification (inhibit entire pathway module)
- Synthetic biology (transplant entire module to bacteria)

### Problem 3: Gene Regulatory Network Analysis

**Challenge:** Identify co-regulated gene modules from expression data
- Gene co-expression network: 10K genes, 50K edges
- Edges: high correlation in expression across conditions
- Goal: Find transcriptional programs

**Insight:**
- Genes in same community = likely co-regulated
- Community = candidate transcription factor target set
- Validates ChIP-seq data (TF binding experiments)

## Requirements

### Graph Characteristics

- **Size:** 1K-20K nodes (proteins, genes, metabolites)
- **Type:** Undirected (PPI, co-expression)
- **Weighted:** Yes (interaction confidence, correlation strength)
- **Noisy:** YES (false positives from experiments)

### Quality Needs

**Biological validity:** CRITICAL
- Must match known complexes/pathways (ground truth)
- Evaluated by GO term enrichment (Gene Ontology)
- Goal: p-value < 0.001 for biological process enrichment

**Resolution:** FLEXIBLE
- Some proteins in multiple complexes (ribosome assembly + ribosome)
- Hierarchical structure common (sub-complexes within complexes)

**Robustness:** HIGH
- Networks noisy (false positives from experiments)
- Algorithm should be stable to edge noise

### Constraints

**Technical:**
- Cluster environment (HPC available but prefers laptop)
- Python + Jupyter notebooks (standard in bioinformatics)
- Integration with NetworkX, Cytoscape, or igraph

**Validation:**
- Must compare to databases (STRING, KEGG, Reactome)
- Enrichment analysis (GO terms, pathways)
- Literature validation (can take weeks)

**Publication:**
- Need to cite algorithm (methodologically rigorous)
- Prefer methods with strong theoretical foundation
- Reproducibility critical (same data = same result)

## Success Criteria

**Good communities = biologically meaningful**
1. **GO enrichment:** p < 0.001 for shared biological process
2. **Literature support:** >50% of proteins co-occur in reviews
3. **Experimental validation:** Top complex confirmed in wet lab
4. **Interpretability:** Can explain to biologist collaborators

**Bad communities = noise**
- Random protein groupings (no GO enrichment)
- Single giant community (no insights)
- Unstable to parameter changes (not robust)

## Algorithm Selection for This Persona

**Best fit: Leiden or Infomap**

**Leiden:**
- Guaranteed connected communities (proteins should interact)
- Hierarchical output (complexes within super-complexes)
- Well-cited (Nature Scientific Reports paper, citable)
- Reproducible with seed

**Infomap:**
- Information theory foundation (appeals to quantitative biologists)
- Handles weighted edges well (interaction confidence)
- Multi-scale hierarchy (pathways within super-pathways)
- Flow-based = captures functional relationships

**Why NOT others:**
- ❌ Louvain: Disconnected communities (proteins not interacting = bad complex)
- ❌ Label Propagation: Low quality, hard to justify in Methods section
- ❌ Spectral: Requires knowing K (number of complexes unknown)

**Typical workflow:**
1. Construct PPI network from STRING database
2. Weight edges by interaction confidence
3. Run Leiden with resolution sweep (0.5, 1.0, 1.5)
4. For each partition, compute GO enrichment
5. Pick resolution with best enrichment
6. Validate top 10 complexes in literature
7. Propose top 3 for experimental validation

## Real-World Example

**Case study:** Identifying novel mRNA processing complex in yeast

**Network:** 3,500 proteins, 15,000 interactions (from BioGRID database)

**Method:** Leiden community detection, resolution=1.2, validated against GO terms

**Result:**
- Found 180 communities, 85% with significant GO enrichment
- Novel 8-protein complex in mRNA splicing pathway
- Experimental validation: 7/8 proteins confirmed to interact
- Publication: Cell Reports (high-impact journal)

**Why it worked:**
- Leiden found connected communities (all proteins interact)
- Hierarchical output revealed sub-complexes (early vs late spliceosome)
- High-confidence interactions (weighted edges) improved quality
- Reproducibility (same seed = same result) enabled peer review

## Domain-Specific Considerations

### False Positives in PPI Networks

**Problem:** Yeast two-hybrid has ~30% false positive rate

**Impact:** Spurious edges can create artifactual communities

**Mitigation:**
- Weight edges by experimental evidence (multiple studies = higher weight)
- Filter edges below confidence threshold before community detection
- Validate communities with orthogonal data (co-expression, co-localization)

### Hierarchical Biological Organization

**Reality:** Proteins organized in nested hierarchy
- Protein → Sub-complex → Complex → Pathway → System

**Requirement:** Algorithm should support multi-level communities

**Leiden advantage:** Multi-level output maps naturally to biology

### Overlapping Function

**Reality:** Some proteins belong to multiple complexes
- Example: Transcription factor in multiple regulatory complexes

**Standard algorithms:** Non-overlapping communities (limitation)

**Workaround:** Run detection multiple times, analyze overlap

**Better solution:** Infomap with overlapping communities enabled

## Validation Pipeline

1. **Computational validation:**
   - GO enrichment (biological process, molecular function)
   - Pathway enrichment (KEGG, Reactome)
   - Protein domain enrichment (Pfam)

2. **Literature validation:**
   - PubMed co-occurrence (proteins mentioned together)
   - Text mining (MeSH term co-occurrence)

3. **Orthogonal data:**
   - Co-expression (RNA-seq)
   - Co-localization (microscopy)
   - Co-evolution (phylogenetic profiles)

4. **Experimental validation:**
   - Co-immunoprecipitation (pull down complex)
   - Mass spectrometry (identify complex members)
   - Functional assays (does complex have activity?)

**Cost:** Computational ($0), Literature (days), Orthogonal (varies), Experimental ($10K-50K)

**Timeline:** Computational (hours), Literature (weeks), Experimental (months)
