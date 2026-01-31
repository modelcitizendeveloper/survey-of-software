# Use Case: Academic Researchers (Citation Network Analysis)

## Who Needs This

**Persona:** Dr. Patel, Assistant Professor in Information Science

**Role:** Studies evolution of scientific fields through citation analysis

**Organization:** R1 research university (doctoral-granting, high research activity)

**Technical background:** PhD in information science, strong programming (Python, R)

**Team size:** Solo PI + 2 grad students

## Why Community Detection Matters

### Problem 1: Research Field Mapping

**Challenge:** Identify emerging subfields in machine learning
- Citation network: 100K papers, 500K citations (last 10 years)
- Goal: Map landscape of research topics
- Question: "What are the major research clusters?"

**Why it matters:**
- Curriculum design (what topics to teach?)
- Hiring decisions (which expertise gaps to fill?)
- Funding allocation (which areas growing?)

**Without community detection:**
- Manual literature review (subjective, incomplete)
- Keyword analysis (misses conceptual clusters)
- Citation count (popularity ≠ community structure)

**With community detection:**
- Papers cluster by citation patterns (who cites whom)
- Each community = research subfield
- Identify: deep learning, NLP, computer vision, reinforcement learning, etc.

**Value:**
- Objective field delineation (data-driven taxonomy)
- Discover novel clusters (emerging fields)
- Track evolution (fields splitting, merging over time)

### Problem 2: Interdisciplinary Collaboration Mapping

**Challenge:** Find boundary-spanning research areas
- Author collaboration network: 50K researchers, 200K co-authorship edges
- Goal: Identify interdisciplinary clusters
- Example: bio-informatics (biology + computer science)

**Why it matters:**
- Funding agencies prioritize interdisciplinary work (NSF, NIH)
- Innovation often happens at boundaries
- Identify collaboration opportunities

**Community detection use:**
- Tight clusters = disciplinary silos
- Bridge papers = interdisciplinary work (high betweenness centrality)
- Communities spanning departments = successful interdisciplinary areas

**Insight:**
- Some fields naturally collaborative (computational biology)
- Others siloed (pure mathematics, theoretical physics)
- Policy: target funding to bridge silos

### Problem 3: Scientific Influence Analysis

**Challenge:** Track influence of seminal papers
- Paper citation network: 1M papers (last 20 years)
- Goal: Identify foundational papers that spawned research communities
- Example: "Attention is All You Need" (Transformer paper) → NLP revolution

**Method:**
- Run community detection on citation network
- Identify papers cited by entire community (community anchors)
- Track community growth over time (from seed paper → thousands)

**Value:**
- Science of science (how do fields emerge?)
- Predict future trends (which seeds growing fastest?)
- Evaluate impact (beyond simple citation count)

## Requirements

### Graph Characteristics

- **Size:** 10K-10M nodes (papers, authors)
- **Type:** Directed (citations are directional: A cites B)
- **Temporal:** Yes (track field evolution over decades)
- **Edge attributes:** Publication year, journal prestige

### Quality Needs

**Interpretability:** CRITICAL
- Communities must map to recognizable research topics
- Publishable (paper submission requires clear explanation)
- Peer review (reviewers must find clustering plausible)

**Ground truth validation:** HIGH
- Compare to existing taxonomies (ACM Computing Classification, arXiv categories)
- Survey domain experts ("is this a real subfield?")
- Literature validation (do reviews describe this cluster?)

**Reproducibility:** CRITICAL
- Academic requirement: same data → same result
- Code availability (GitHub repository)
- Parameter documentation (justify all choices)

### Constraints

**Technical:**
- Cluster computing available (HPC cluster, AWS)
- Python + NetworkX ecosystem (academic standard)
- Large datasets (10M papers from Web of Science, Scopus)

**Publication:**
- Methodologically rigorous (prefer algorithms with strong theory)
- Novelty (can't just use off-the-shelf Louvain without justification)
- Comparison required (benchmark multiple algorithms)

**Time:**
- Grants run 3-5 years (analysis can take months)
- PhD timelines (grad students need results for dissertation)

## Success Criteria

**Good communities = publishable findings**
1. **Face validity:** Domain experts recognize communities as real subfields
2. **Quantitative validation:** High modularity, match ground truth taxonomies
3. **Novelty:** Reveal insights not obvious from manual analysis
4. **Reproducibility:** Published code + data enables replication

**Bad communities = desk rejection**
- Trivial results (everyone already knows these clusters)
- Garbage clusters (no coherent topic)
- Non-reproducible (reviewers can't replicate)

## Algorithm Selection for This Persona

**Best fit: Leiden or Infomap (depending on research question)**

**Leiden:**
- Well-cited (Nature Scientific Reports = citable in Methods section)
- Reproducible (set seed)
- Hierarchical (subfields within fields)
- Guaranteed connectedness (all papers in cluster must cite each other)

**Infomap:**
- Information-theoretic foundation (appeals to quantitative researchers)
- Flow-based = captures idea propagation
- Handles directed citations naturally
- Multi-scale hierarchy (micro → meso → macro fields)

**Why NOT others:**
- ❌ Louvain: Disconnected communities (papers not citing each other = bad cluster)
- ❌ Label Propagation: Low quality, hard to justify in peer review
- ❌ Spectral: Requires knowing K (number of subfields unknown)

**Typical research workflow:**
1. Data collection (Web of Science API, MAG, arXiv)
2. Graph construction (papers = nodes, citations = edges)
3. Pre-processing (filter: recent papers, minimum citations)
4. Algorithm comparison (run Louvain, Leiden, Infomap, spectral)
5. Validation (modularity, NMI vs ground truth, expert survey)
6. Analysis (temporal evolution, interdisciplinarity, impact)
7. Visualization (Gephi, Cytoscape)
8. Paper writing (JASIS&T, Scientometrics, arXiv)

## Real-World Example

**Case study:** Mapping the evolution of Deep Learning research (2010-2020)

**Data:**
- 50K papers from arXiv cs.LG, cs.CV, cs.CL
- 300K citations
- 80K authors

**Method:**
- Leiden community detection, resolution sweep (0.5-2.0)
- Temporal analysis (yearly snapshots)
- Validation: compare to arXiv sub-categories

**Results:**
1. **7 major communities identified:**
   - Deep learning theory (optimization, generalization)
   - Computer vision (CNNs, object detection)
   - NLP (RNNs, Transformers)
   - Reinforcement learning
   - Generative models (GANs, VAEs)
   - Graph neural networks (emerging 2017+)
   - Applications (healthcare, robotics)

2. **Temporal evolution:**
   - 2010-2015: CNNs dominate (vision community largest)
   - 2015-2017: RNNs grow (NLP community expands)
   - 2017-2020: Transformers explode (NLP overtakes vision)
   - 2018-2020: GNN emerges as new cluster

3. **Key findings:**
   - Transformer paper (2017) spawned entire sub-community
   - Cross-citation between vision + NLP increased 5x (multimodal)
   - Theory community remained small but highly cited

**Publication:** Published in Journal of Informetrics, 500+ citations

**Why it worked:**
- Leiden guaranteed connected communities (papers citing each other)
- Hierarchical output revealed sub-communities (e.g., object detection within vision)
- Reproducible (code + data on GitHub)
- Validated (matched expert understanding + arXiv categories)

## Domain-Specific Considerations

### Citation Dynamics

**Problem:** Older papers have more citations (time bias)

**Impact:** Communities might cluster by age, not topic

**Solutions:**
- Normalize by paper age (citations per year)
- Time-windowed analysis (only citations within 5 years)
- Vintaging (compare papers from same year)

### Self-Citation and Citation Cartels

**Problem:** Authors cite their own work excessively

**Impact:** Artificially inflates community structure

**Solutions:**
- Filter self-citations (remove edges A→B if authors overlap)
- Detect citation cartels (cliques with excessive internal citations)
- Weight edges by citation context (is it substantive or superficial?)

### Preprints vs Published Papers

**Problem:** arXiv preprints may differ from published versions

**Impact:** Same paper appears twice (preprint + published)

**Solutions:**
- Deduplication (DOI matching, title similarity)
- Prefer published version (more stable)

### Incomplete Data

**Problem:** Proprietary databases (WoS, Scopus) have gaps

**Impact:** Missing citations create disconnected components

**Solutions:**
- Multi-source fusion (combine WoS + Scopus + arXiv + Microsoft Academic Graph)
- Imputation (predict missing citations from co-authorship)

## Validation Strategies

### Quantitative Validation

1. **Modularity:** Q > 0.3 (standard threshold)
2. **NMI vs ground truth:** Compare to arXiv categories, ACM CCS
3. **Stability:** Bootstrap resampling, check partition similarity
4. **Coverage:** What % of papers assigned to communities?

### Qualitative Validation

1. **Expert survey:** Show clusters to domain experts, ask "is this real?"
2. **Labeling task:** Can experts consistently label community topics?
3. **Literature review:** Do review papers describe these clusters?

### Novel Discovery Validation

1. **Predictive validity:** Do emerging clusters grow in subsequent years?
2. **Funding validation:** Do funding agencies recognize these topics?
3. **Job market:** Do faculty positions advertise these specializations?

## Comparison to Ground Truth

**Existing taxonomies:**
- ACM Computing Classification System (hierarchical)
- arXiv categories (flat)
- Microsoft Academic Graph fields (broad)

**Validation approach:**
- Normalized Mutual Information (NMI) with ground truth
- Adjusted Rand Index (ARI)
- Contingency table (how do algorithmic clusters map to taxonomy?)

**Expected result:**
- NMI ~ 0.4-0.6 (moderate agreement, capturing finer structure than taxonomy)
- Some novel clusters (emerging fields not in taxonomy yet)

## Publication Requirements

**Methods section must include:**
1. Algorithm selection rationale (why Leiden/Infomap?)
2. Parameter justification (resolution, iterations, seed)
3. Pre-processing steps (filtering, normalization)
4. Validation methodology (quantitative + qualitative)
5. Code availability (GitHub, Zenodo)

**Results section must include:**
1. Quantitative metrics (modularity, NMI, coverage)
2. Community descriptions (topic labels, sample papers)
3. Visualizations (network diagrams, hierarchical dendrograms)
4. Temporal evolution (if applicable)

**Discussion section must include:**
1. Interpretation (what do clusters mean?)
2. Limitations (data gaps, algorithmic choices)
3. Comparison to prior work (how does this advance field?)

## Computational Considerations

**Scalability:**
- Citation networks can be huge (10M papers)
- Need efficient implementation (C++ core, Python bindings)
- Parallel processing (multi-core, HPC cluster)

**Typical runtime:**
- 10K papers: minutes (laptop)
- 100K papers: hours (laptop)
- 1M papers: hours (HPC cluster)
- 10M papers: days (HPC cluster)

**Storage:**
- Raw data: gigabytes (paper metadata, citations)
- Graph: hundreds of MB (edge list)
- Results: megabytes (partition, modularity scores)

**Tools:**
- Data wrangling: pandas, dask
- Graph: NetworkX (small), igraph (large), graph-tool (very large)
- HPC: Slurm, PBS
- Visualization: Gephi, Cytoscape, VOSviewer
