# S3 Recommendation: Requirement-Driven Selection

## Use Case Summary

S3 analyzed five distinct personas with different needs, constraints, and success criteria:

| Persona | Scale | Priority | Best Fit | Why |
|---------|-------|----------|----------|-----|
| **Data Science Researchers** | 10K-1M | Ease + comprehensive | NetworkX | Prototyping speed, algorithm breadth, reproducibility |
| **Network Infrastructure** | 100K-10M | Speed + reliability | igraph | Production-grade, fast enough, memory-efficient |
| **Bioinformatics** | 10K-100M | Advanced methods | graph-tool | SBM, statistical rigor, handles omics scale |
| **Fraud/Security** | 1M-100M | Speed + scale | igraph/graph-tool | Real-time detection, production reliability |
| **Product Analytics** | 100K-10M | Fast iteration | NetworkX | Team collaboration, integration, visualization |

## Pattern: Requirements Drive Selection

**Key insight**: The "best" library depends entirely on context. No single library dominates across all use cases.

### When Team Factors Dominate

**NetworkX wins when**:
- Team has mixed skill levels
- Iteration speed > execution speed
- Collaboration and code readability critical
- **Examples**: Research labs, product teams, students

**Requires performance library when**:
- Specialized team can handle complexity
- Execution speed critical (SLAs, real-time)
- Single expert can build and maintain
- **Examples**: Infrastructure teams, security engineers, HPC labs

### When Scale Factors Dominate

**Graph size thresholds**:

| Size | NetworkX | igraph | graph-tool | NetworKit/snap.py |
|------|----------|--------|------------|-------------------|
| <10K | ✅ Best | Overkill | Overkill | Overkill |
| 10K-100K | ✅ Good | ✅ Better if speed matters | Overkill | Overkill |
| 100K-1M | ⚠️ Slow | ✅ Best | ✅ If need advanced methods | Overkill |
| 1M-10M | ❌ Too slow | ✅ Good | ✅ Better | ✅ If have cores |
| 10M-100M | ❌ No | ⚠️ Struggles | ✅ Best | ✅ Best (parallel) |
| >100M | ❌ No | ❌ No | ✅ Possible | ✅ Best |

**Reality check**: Most teams overestimate their scale
- "We have millions of users" often means hundreds of thousands in practice
- Sample before processing full graph
- 100K node graph sufficient for most analyses

### When Algorithm Requirements Dominate

**Must use specific library for**:
- **SBM community detection** → graph-tool (only option)
- **Overlapping communities** → CDlib (most comprehensive)
- **Cascades/diffusion at scale** → snap.py (best support)
- **General algorithms** → NetworkX (most comprehensive)

**Can substitute**:
- Louvain: igraph, graph-tool, NetworKit, or CDlib
- Betweenness: All libraries (choose by speed needs)
- PageRank: All libraries (choose by speed needs)

## Requirement → Library Mapping

### Map Your Constraints

**Step 1: Identify critical constraint**

```
What constraint is NON-NEGOTIABLE?

A. Graph size >10M nodes AND need comprehensive algorithms
   → graph-tool or NetworKit

B. Team skill = mixed, collaboration critical
   → NetworkX

C. Production SLAs, reliability critical
   → igraph (or graph-tool if have expertise)

D. Need specific algorithm (SBM, overlapping communities)
   → Check algorithm availability (may force choice)

E. Budget/time = tight, must use what team knows
   → Stick with current tools, optimize later
```

**Step 2: Validate with secondary constraints**

```
Does primary choice satisfy all MUST-HAVE requirements?

✅ Scale: Library handles your graph size comfortably
✅ Speed: Analysis completes within timeframe
✅ Team: Team can learn/use within project timeline
✅ Algorithms: Critical algorithms available
✅ Integration: Works with existing stack

❌ Any NO → Re-evaluate or mitigate (e.g., sample data)
```

**Step 3: Optimize for NICE-TO-HAVE**

```
Among viable options, prefer:
- Easier API (if team skill varies)
- Faster (if iteration speed matters)
- More permissive license (if commercial)
- Better docs (if learning curve steep)
```

## Common Requirement Patterns

### Pattern: Research Project

**Constraints**:
- Team: Mixed skill (grad students to professors)
- Scale: <1M nodes typically
- Time: Semester or grant cycle
- Priority: Reproducibility, comprehensiveness

**Library**: NetworkX → (igraph if hitting limits)

**Rationale**:
- Easy for team to learn and collaborate
- Comprehensive algorithms for thorough research
- Reproducible (pip-installable, version-stable)
- Can switch to igraph later if needed

### Pattern: Production Service

**Constraints**:
- Team: Experienced engineers
- Scale: 100K-10M nodes
- Time: SLA-driven (seconds to minutes)
- Priority: Reliability, speed

**Library**: igraph → (graph-tool for >10M)

**Rationale**:
- Production-proven stability
- Fast enough for SLAs
- Team can handle API complexity
- Memory-efficient for large graphs

### Pattern: Cutting-Edge Research

**Constraints**:
- Team: PhD-level expertise
- Scale: Variable (sometimes massive)
- Time: Publication-driven
- Priority: State-of-the-art methods

**Library**: graph-tool

**Rationale**:
- SBM and advanced methods required for top-tier publications
- Team has expertise for complex API
- Performance handles large-scale analyses
- Academic rigor expected by reviewers

### Pattern: Billion-Scale Analysis

**Constraints**:
- Team: Specialists (systems + algorithms)
- Scale: >100M nodes
- Time: Batch processing acceptable
- Priority: Scale above all

**Library**: snap.py or NetworKit (32+ cores)

**Rationale**:
- Only libraries proven at billion-node scale
- NetworKit if have HPC resources
- snap.py if need specific algorithms (cascades)

## Anti-Patterns: Wrong Library Choice

### Don't Do This

❌ **Use graph-tool for small team prototype**
- Installation friction blocks progress
- API complexity slows iteration
- NetworkX 100x easier, fast enough for small graphs

❌ **Use NetworkX for production >1M nodes**
- Too slow, will hit wall
- Memory usage excessive
- Migrate to igraph before deploying

❌ **Choose on benchmark alone, ignore team**
- Fastest library useless if team can't use it
- Development time often exceeds execution time
- Factor in learning curve and maintenance

❌ **Over-engineer for hypothetical future scale**
- "We might have millions of users someday"
- Start with NetworkX, migrate when actually needed
- Premature optimization wastes time

## Validation Checklist

**Before committing to library**:

```
[ ] Confirmed graph size (measured, not estimated)
[ ] Validated library handles scale (tested on sample)
[ ] Team can install and run basic examples
[ ] Critical algorithms available or implementable
[ ] Integration with existing stack tested
[ ] Performance acceptable for workflow (measured)
[ ] License compatible with project (checked with legal if needed)
[ ] Maintenance/support acceptable (project active, community responsive)
```

**If any checkbox unchecked** → Reassess choice

## Final Recommendation by Persona

**Default for most teams**: Start with **NetworkX**
- Covers 60-70% of use cases
- Migrate to igraph when hitting limits (clear signal: analysis taking >10 minutes)

**Production-first teams**: Start with **igraph**
- If you know you need production-grade from start
- Team has engineering expertise
- Scale >100K nodes certain

**Specialist teams**: Choose by specialization
- **Bioinformatics** → graph-tool (SBM)
- **HPC** → NetworKit (parallelism)
- **Web-scale** → snap.py (billions)
- **Community detection research** → CDlib

**The pragmatic path**: NetworkX → igraph → graph-tool
- Start easy, migrate when needed
- Each step 10-100x performance gain
- Pay complexity cost only when justified
