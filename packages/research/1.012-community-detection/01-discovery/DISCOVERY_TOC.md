# Community Detection Libraries: Discovery Table of Contents

## Overview

This research analyzes community detection libraries through four complementary perspectives (4PS methodology), enabling selection based on your specific context.

**Total research time:** ~2 weeks (S1: 2-4 hours, S2: 1-2 days, S3: 4-6 hours, S4: 1-2 days)

---

## S1: Rapid Discovery (Quick Decision)

**Read time:** 15-30 minutes
**Use when:** Need answer NOW, limited time for research

**Files:**
- [`approach.md`](S1-rapid/approach.md) - Methodology and decision criteria
- [`louvain.md`](S1-rapid/louvain.md) - Most popular algorithm, fast prototyping
- [`label-propagation.md`](S1-rapid/label-propagation.md) - Extreme speed for massive graphs
- [`spectral-clustering.md`](S1-rapid/spectral-clustering.md) - Mathematical rigor, small graphs only
- [`infomap.md`](S1-rapid/infomap.md) - Flow-based, best for directed networks
- [`cdlib.md`](S1-rapid/cdlib.md) - Meta-library with 39+ algorithms
- [`recommendation.md`](S1-rapid/recommendation.md) - **START HERE** - Quick decision guide

**Key takeaway:** **Use Leiden for 80% of use cases** (fixes Louvain's defects, faster, better quality)

---

## S2: Comprehensive Analysis (Technical Deep-Dive)

**Read time:** 2-4 hours
**Use when:** Production deployment, need to understand internals

**Files:**
- [`approach.md`](S2-comprehensive/approach.md) - Deep analysis methodology
- [`louvain.md`](S2-comprehensive/louvain.md) - Algorithm phases, disconnection problem
- [`leiden.md`](S2-comprehensive/leiden.md) - Refinement phase, quality guarantees
- [`label-propagation.md`](S2-comprehensive/label-propagation.md) - Update strategies, convergence issues
- [`spectral-clustering.md`](S2-comprehensive/spectral-clustering.md) - Eigendecomposition, O(n³) complexity
- [`infomap.md`](S2-comprehensive/infomap.md) - Map equation, random walks, code length
- [`cdlib.md`](S2-comprehensive/cdlib.md) - Architecture, evaluation framework
- [`feature-comparison.md`](S2-comprehensive/feature-comparison.md) - **Comparative tables** - Complexity, quality, scalability
- [`recommendation.md`](S2-comprehensive/recommendation.md) - **Technical decision guide** - Algorithm selection flowchart

**Key takeaway:** **Leiden guarantees connected communities** (Louvain doesn't), 20x faster on large graphs

---

## S3: Need-Driven Discovery (Use Case Matching)

**Read time:** 1-2 hours
**Use when:** Know your specific problem, want to see similar use cases

**Files:**
- [`approach.md`](S3-need-driven/approach.md) - Persona-driven methodology
- [`use-case-social-media-analysts.md`](S3-need-driven/use-case-social-media-analysts.md) - Influencer identification, bot detection
- [`use-case-bioinformatics-researchers.md`](S3-need-driven/use-case-bioinformatics-researchers.md) - Protein complexes, pathway analysis
- [`use-case-cybersecurity-teams.md`](S3-need-driven/use-case-cybersecurity-teams.md) - Botnet detection, threat attribution
- [`use-case-urban-planners.md`](S3-need-driven/use-case-urban-planners.md) - Neighborhood discovery from mobility
- [`use-case-academic-researchers.md`](S3-need-driven/use-case-academic-researchers.md) - Citation network analysis, field mapping
- [`recommendation.md`](S3-need-driven/recommendation.md) - **Persona-to-algorithm mapping** - Match your role to best library

**Key takeaway:** **Different personas need different algorithms** (explainability vs speed vs quality trade-offs)

---

## S4: Strategic Selection (Long-Term Planning)

**Read time:** 1-2 hours
**Use when:** Multi-year architectural decision, need to assess project viability

**Files:**
- [`approach.md`](S4-strategic/approach.md) - Strategic risk evaluation methodology
- [`networkx-viability.md`](S4-strategic/networkx-viability.md) - Infrastructure project, zero risk
- [`leiden-viability.md`](S4-strategic/leiden-viability.md) - Single maintainer risk, institutional backing
- [`infomap-viability.md`](S4-strategic/infomap-viability.md) - Academic project, grant-dependent
- [`scikit-learn-viability.md`](S4-strategic/scikit-learn-viability.md) - ML ecosystem, limited use case
- [`recommendation.md`](S4-strategic/recommendation.md) - **Risk-adjusted portfolio** - Safe bets vs calculated risks

**Key takeaway:** **NetworkX + Leiden is safe for 5+ years** (NetworkX = infrastructure, Leiden has fallback to cuGraph)

---

## Domain Explainer (Universal Context)

**Read time:** 10-15 minutes
**Use when:** New to community detection, need accessible explanation

**File:** [`DOMAIN_EXPLAINER.md`](../DOMAIN_EXPLAINER.md)

**Covers:**
- What community detection solves (without jargon)
- Analogies: cafeteria groups, language families, water flow
- When you need it (vs when you don't)
- Trade-offs: speed vs quality, explainability vs sophistication
- Implementation reality: timelines, pitfalls, first 90 days

**Key takeaway:** **Community detection finds groups that connect more internally than externally**

---

## Quick Navigation

### By Time Available

| Time | Start Here |
|------|-----------|
| 5 minutes | [S1 Recommendation](S1-rapid/recommendation.md) |
| 30 minutes | S1 (all files) |
| 2 hours | [S2 Feature Comparison](S2-comprehensive/feature-comparison.md) + [S2 Recommendation](S2-comprehensive/recommendation.md) |
| 4 hours | S2 (all files) |
| Full day | All passes (S1-S4) |

### By Question Type

| Question | Read This |
|----------|-----------|
| "Which library should I use?" | [S1 Recommendation](S1-rapid/recommendation.md) |
| "How does Leiden work internally?" | [S2 Leiden](S2-comprehensive/leiden.md) |
| "What do social media analysts use?" | [S3 Social Media Use Case](S3-need-driven/use-case-social-media-analysts.md) |
| "Is leidenalg safe long-term?" | [S4 Leiden Viability](S4-strategic/leiden-viability.md) |
| "I'm new to this, explain simply" | [Domain Explainer](../DOMAIN_EXPLAINER.md) |

### By Network Size

| Graph Size | Best Algorithm | Read This |
|------------|----------------|-----------|
| <10K nodes | Leiden or Spectral | [S1 Spectral](S1-rapid/spectral-clustering.md), [S1 Louvain](S1-rapid/louvain.md) |
| 10K-100K nodes | Leiden | [S2 Leiden](S2-comprehensive/leiden.md) |
| 100K-1M nodes | Leiden or Label Prop | [S2 Leiden](S2-comprehensive/leiden.md), [S2 Label Prop](S2-comprehensive/label-propagation.md) |
| >1M nodes | Label Prop or GPU Leiden | [S2 Label Prop](S2-comprehensive/label-propagation.md) |

### By Use Case

| Domain | Recommended Algorithm | Read This |
|--------|----------------------|-----------|
| Social media | Leiden | [S3 Social Media](S3-need-driven/use-case-social-media-analysts.md) |
| Biology | Leiden or Infomap | [S3 Bioinformatics](S3-need-driven/use-case-bioinformatics-researchers.md) |
| Cybersecurity | Label Prop → Leiden | [S3 Cybersecurity](S3-need-driven/use-case-cybersecurity-teams.md) |
| Urban planning | Leiden + spatial | [S3 Urban Planning](S3-need-driven/use-case-urban-planners.md) |
| Academic research | Leiden or Infomap | [S3 Academic](S3-need-driven/use-case-academic-researchers.md) |

---

## Methodology: The Four-Pass Survey (4PS)

This research uses **4PS** - a multi-perspective approach that reveals different optimal solutions:

**S1 (Rapid):** "Popular libraries exist for a reason" - Speed-focused, ecosystem-driven
**S2 (Comprehensive):** "Understand everything before choosing" - Feature matrices, deep comparisons
**S3 (Need-Driven):** "Start with requirements, find exact-fit solutions" - Scenario-based selection
**S4 (Strategic):** "Think long-term and broader context" - Maintenance, team expertise, ecosystem fit

**Why four perspectives?** Different discovery approaches reveal different optimal solutions. A library "best" for prototyping might be wrong for production. Strategic constraints might override technical superiority. **Single-methodology discovery misses better paths.**

---

## Validation Checklist

Before deploying community detection in production:

- [ ] **Read S1 recommendation** - Understand the 80/20 rule (Leiden for most use cases)
- [ ] **Validate approach** - Run on toy data (karate club graph), verify results make sense
- [ ] **Check requirements** - Match your use case to S3 personas, pick appropriate algorithm
- [ ] **Assess risk** - Read S4 viability for chosen library, understand maintenance status
- [ ] **Validate quality** - Modularity > 0.3, communities connected, domain expert review
- [ ] **Document methodology** - Justify algorithm choice, parameters, validation approach
- [ ] **Plan for scale** - Budget for migration if graph grows (NetworkX → Leiden → cuGraph)

---

## Updates and Maintenance

**Research snapshot:** January 2026

**Key version info:**
- NetworkX: 3.6.1
- leidenalg: 0.10.3+
- scikit-learn: 1.8.0
- CDlib: 0.4.0

**Major changes since last update:**
- Leiden Nature Scientific Reports paper (2019): 2K+ citations
- nx-cugraph GPU backend (2024): 315x speedup
- scikit-learn cluster_qr (1.8.0): Deterministic spectral clustering
- Infomap ACM tutorial (2024): Comprehensive methodology guide

**Next review recommended:** January 2027 (annual check)
