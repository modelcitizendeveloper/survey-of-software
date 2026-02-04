# S3 Recommendation: Requirement-Driven Selection

## Persona-to-Algorithm Mapping

| Persona | Primary Need | Best Algorithm | Key Constraint |
|---------|--------------|----------------|----------------|
| Social Media Analyst | Explainability | Leiden | Must explain to clients |
| Bioinformatician | Biological validity | Leiden or Infomap | Must match GO terms |
| Cybersecurity Analyst | Speed + Precision | Label Prop → Leiden | Real-time detection |
| Urban Planner | Spatial coherence | Leiden + post-processing | Political defensibility |
| Academic Researcher | Reproducibility | Leiden or Infomap | Peer review requirements |

## Decision Criteria by Persona

### Social Media Analysts

**Primary criteria:**
1. **Explainability:** Can you explain to non-technical client?
2. **Speed:** Can you iterate in meeting (minutes)?
3. **Stability:** Do communities make sense week-over-week?

**Algorithm selection:**
→ **Leiden**
- Modularity easy to explain ("groups that talk to each other more")
- Fast enough for interactive analysis
- Stable with seed (show same results in follow-up meeting)

**Red flags:**
- Infomap: Information theory too abstract for clients
- Label Propagation: Unstable results confuse stakeholders

### Bioinformatics Researchers

**Primary criteria:**
1. **Biological plausibility:** Do communities match known biology?
2. **Publication quality:** Can you justify in Methods section?
3. **Robustness:** Stable to noisy interaction data?

**Algorithm selection:**
→ **Leiden** (standard choice) or **Infomap** (advanced)

**Leiden when:**
- First pass analysis (standard, well-cited)
- Need connected communities (proteins must interact)
- Modularity matches biological intuition

**Infomap when:**
- Directed networks (e.g., signaling pathways)
- Want flow-based interpretation (information flow = signal propagation)
- Studying novel organism (less ground truth to validate against)

**Red flags:**
- Label Propagation: Hard to justify low quality in peer review
- Spectral: Requires knowing number of protein complexes (unknown)

### Cybersecurity Analysts

**Primary criteria:**
1. **Speed:** Real-time detection (minutes, not hours)
2. **Precision:** False positives waste limited analyst time
3. **Legal defensibility:** Can you explain method in court?

**Algorithm selection:**
→ **Two-stage:** Label Propagation → Leiden

**Stage 1 (Triage): Label Propagation**
- Speed critical (scan 1M nodes in minutes)
- High recall (catch everything suspicious)
- Accept false positives (refined in Stage 2)

**Stage 2 (Confirmation): Leiden**
- Higher precision (reduce false positives)
- Reproducible (legal requirement)
- Explainable (modularity clear to non-technical judges)

**Red flags:**
- Pure Leiden: Too slow for real-time (use for daily batch only)
- Pure Label Prop: Too many false positives (alert fatigue)

### Urban Planners

**Primary criteria:**
1. **Spatial coherence:** Communities must be contiguous on map
2. **Political defensibility:** Elected officials must accept results
3. **Resident validation:** "Yes, that's my neighborhood"

**Algorithm selection:**
→ **Leiden + spatial post-processing**

**Why Leiden:**
- Guaranteed connected communities (baseline for spatial contiguity)
- Hierarchical (neighborhoods within districts)
- Modularity interpretable to non-technical council

**Post-processing:**
- Enforce spatial contiguity (split disconnected components)
- Balance population (legal requirement for voting districts)
- Respect natural boundaries (rivers, highways)

**Why NOT Infomap:**
- Flow-based interpretation less intuitive to politicians
- Harder to explain in public meetings

**Red flags:**
- Raw algorithmic output: Requires manual spatial cleanup
- Spectral: Requires knowing K (how many neighborhoods? political question)

### Academic Researchers

**Primary criteria:**
1. **Reproducibility:** Same data → same result (peer review requirement)
2. **Theoretical rigor:** Strong mathematical foundation
3. **Novelty:** Must justify why not just using standard Louvain

**Algorithm selection:**
→ **Leiden** (safe choice) or **Infomap** (novelty)

**Leiden when:**
- Undirected networks (co-authorship, undirected citations)
- Need to compare to prior work (Louvain/Leiden standard)
- Reviewers expect modularity-based methods

**Infomap when:**
- Directed networks (citations, knowledge flow)
- Novel contribution: flow-based interpretation
- Studying information diffusion (natural fit)

**Justification template:**
```
We chose Leiden because:
1. Addresses Louvain's disconnected communities defect [cite: Traag 2019]
2. Subset optimality guarantees [cite: Traag 2019]
3. Reproducible with fixed random seed
4. Standard in field (enables comparison to prior work)
```

**Red flags:**
- Label Propagation: Hard to justify low quality
- No comparison: Must benchmark multiple algorithms

## Requirement-Driven Decision Trees

### Tree 1: Speed vs Quality

```
Speed requirement?
├─ Real-time (seconds) → Label Propagation
├─ Interactive (minutes) → Leiden
├─ Batch (hours) → Leiden or Infomap
└─ Research (days OK) → Try all, pick best

Quality requirement?
├─ Approximate (rough clustering) → Label Propagation
├─ High (production) → Leiden
├─ Rigorous (academic) → Leiden + validation
└─ Exploratory (visual ization) → Any fast method
```

### Tree 2: Explainability vs Complexity

```
Audience?
├─ Non-technical stakeholders → Leiden (modularity intuitive)
├─ Technical team → Leiden or Infomap
├─ Academic peer review → Leiden or Infomap (strong theory)
└─ Legal/regulatory → Leiden (reproducible, explainable)

Explainability need?
├─ Critical (client-facing) → Leiden ("groups that connect more internally")
├─ Important (team decision) → Leiden or Infomap
└─ Low (internal analysis) → Any method
```

### Tree 3: Network Type

```
Network characteristics?
├─ Directed + flow matters → Infomap
├─ Undirected → Leiden
├─ Temporal → Label Propagation (streaming) or Infomap
├─ Weighted → Any (all handle weights)
└─ Known K → Spectral (if <10K nodes)

Domain?
├─ Social media → Leiden (explainability)
├─ Biology → Leiden or Infomap (validation critical)
├─ Security → Label Prop + Leiden (speed + precision)
├─ Urban → Leiden + spatial (contiguity)
└─ Academic → Leiden or Infomap (reproducibility)
```

## Common Requirement Patterns

### Pattern 1: "I need to explain this to my boss"

**Requirements:**
- Non-technical audience
- Quick turnaround (days, not weeks)
- Defensible methodology

**Recommendation:** Leiden
- Modularity = "how tightly connected groups are"
- Well-cited paper (credibility)
- Fast results

**Implementation:**
```python
from cdlib import algorithms

communities = algorithms.leiden(G, seed=42)
modularity = communities.newman_girvan_modularity().score

# Explain: "We found {len(communities.communities)} communities
# with modularity {modularity:.2f}, meaning groups are {modularity*100:.0f}%
# more internally connected than random expectation."
```

### Pattern 2: "I have a huge graph (millions of nodes)"

**Requirements:**
- Scale: 1M+ nodes
- Speed: results in hours, not days
- Quality: approximate OK

**Recommendation:** Label Propagation or GPU Leiden

**CPU option:**
```python
import networkit as nk

G_nk = nk.nxadapter.nx2nk(G)
lp = nk.community.PLP(G_nk)
lp.run()
# Runtime: 1M nodes in minutes
```

**GPU option (if NVIDIA GPU available):**
```python
import cugraph

communities = cugraph.leiden(G_cudf)
# Runtime: 1M nodes in seconds, 47x faster than CPU
```

### Pattern 3: "I need this for a paper"

**Requirements:**
- Peer review standards
- Reproducibility
- Strong theoretical foundation

**Recommendation:** Leiden + comprehensive validation

**Methodology:**
1. **Algorithm comparison:** Benchmark Louvain, Leiden, Infomap
2. **Validation:** Modularity, NMI vs ground truth (if available)
3. **Sensitivity analysis:** Parameter sweep, bootstrap stability
4. **Reproducibility:** Publish code + data

**Methods section template:**
```
Community detection via Leiden algorithm [1], which addresses
the Louvain algorithm's disconnected communities defect. We ran
Leiden with resolution parameter γ=1.0, n_iterations=2, and
random seed=42 for reproducibility. Modularity Q=0.42 (95% CI:
0.40-0.44 via bootstrap). Code and data available at [URL].

[1] Traag et al., From Louvain to Leiden: guaranteeing
well-connected communities, Sci Rep 2019.
```

### Pattern 4: "I don't know which algorithm to use"

**Requirements:**
- Algorithm selection uncertainty
- Budget for experimentation (time)
- Need to justify choice

**Recommendation:** CDlib for systematic comparison

**Approach:**
```python
from cdlib import algorithms, evaluation

# Try multiple algorithms
results = {}
for name, algo in [('louvain', algorithms.louvain),
                    ('leiden', algorithms.leiden),
                    ('infomap', algorithms.infomap)]:
    comm = algo(G)
    results[name] = {
        'communities': comm,
        'modularity': evaluation.newman_girvan_modularity(G, comm).score,
        'num_communities': len(comm.communities),
        'coverage': evaluation.node_coverage(G, comm).score
    }

# Pick best by modularity
best = max(results.items(), key=lambda x: x[1]['modularity'])
print(f"Best algorithm: {best[0]} with Q={best[1]['modularity']:.3f}")
```

**Justification:**
"We compared 3 algorithms (Louvain, Leiden, Infomap) and selected
Leiden based on highest modularity (Q=0.42) and guaranteed
connected communities."

### Pattern 5: "Results must be reproducible for compliance"

**Requirements:**
- Regulatory compliance (GDPR, SOX)
- Audit trail
- Deterministic results

**Recommendation:** Leiden with fixed seed OR Spectral (cluster_qr)

**Leiden (reproducible with seed):**
```python
communities = algorithms.leiden(G, seed=42)
# Same graph + same seed = same result
```

**Spectral (fully deterministic):**
```python
from sklearn.cluster import SpectralClustering

sc = SpectralClustering(
    n_clusters=K,
    assign_labels='cluster_qr',  # Deterministic
    random_state=42
)
labels = sc.fit_predict(adjacency_matrix)
# Same graph = same result (no randomness)
```

**Compliance documentation:**
```
Algorithm: Leiden (Traag et al. 2019)
Parameters: resolution=1.0, n_iterations=2, seed=42
Reproducibility: Fixed seed ensures identical results
Validation: Modularity Q=0.42, {N} communities detected
Audit trail: Logged to compliance database [timestamp]
```

## Anti-Patterns: What NOT to Do

### Anti-Pattern 1: Using Louvain in Production

**Problem:** Up to 16% disconnected communities

**Impact:** Confusing results, wasted analyst time investigating disconnects

**Solution:** Switch to Leiden (trivial migration via CDlib)

### Anti-Pattern 2: Expecting Determinism from Modularity Methods

**Problem:** Louvain/Leiden have randomness → different results each run

**Mistake:** Not setting seed, presenting unstable results to stakeholders

**Solution:** Always set seed for presentation results
```python
# Wrong: unstable
communities = algorithms.leiden(G)

# Right: reproducible
communities = algorithms.leiden(G, seed=42)
```

### Anti-Pattern 3: Using Spectral for Large Graphs

**Problem:** O(n³) complexity → hours for 10K nodes, impractical for 50K+

**Mistake:** "I need deterministic results" → uses spectral on 100K nodes

**Solution:** Use Leiden with seed (reproducible enough for most use cases)

### Anti-Pattern 4: Choosing Algorithm by Speed Alone

**Problem:** "Label Propagation is fastest" → uses it everywhere

**Impact:** Low quality results, stakeholder confusion, rework

**Solution:** Match algorithm to requirements (speed AND quality AND explainability)

### Anti-Pattern 5: No Validation

**Problem:** Run algorithm, accept results blindly

**Impact:** Garbage clusters accepted as real

**Solution:** Always validate
- Quantitative: modularity, coverage, size distribution
- Qualitative: domain expert review, sample inspection
- Ground truth: compare to known structure (if available)

## Validation Checklist

Before presenting community detection results:

**Quantitative validation:**
- [ ] Modularity Q > 0.3 (baseline threshold)
- [ ] No singleton communities (size > 1)
- [ ] No giant community (largest < 50% of nodes)
- [ ] Connected communities (check with `nx.is_connected`)

**Qualitative validation:**
- [ ] Communities make domain sense (ask expert)
- [ ] Visualization confirms structure (Gephi, Cytoscape)
- [ ] Stable across parameter variations (resolution sweep)

**Stakeholder validation:**
- [ ] Can explain algorithm choice (why Leiden?)
- [ ] Can explain results (what do communities mean?)
- [ ] Can defend parameters (why resolution=1.0?)

**Reproducibility:**
- [ ] Random seed documented (if applicable)
- [ ] Code available (GitHub, Zenodo)
- [ ] Data accessible (or synthetic example for proprietary data)
