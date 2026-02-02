# 1.016 Social Network Analysis Libraries - Discovery Table of Contents

## Research Overview

**Topic**: Social Network Analysis Libraries for Python
**Coverage**: NetworkX, igraph, graph-tool, snap.py, NetworKit, CDlib
**Completed**: 2026-01-30
**Status**: Full 4PS cycle complete

## Four-Pass Survey Structure

This research used the **4PS methodology** - four complementary perspectives that reveal different optimal solutions for different contexts.

### S1: Rapid Discovery (WHICH library?)
**Focus**: Quick comparison for immediate decision-making
**Philosophy**: Popular libraries exist for a reason
**Read time**: 5-10 minutes

- [Approach](S1-rapid/approach.md) - Research methodology
- [NetworkX](S1-rapid/networkx.md) - Pure Python, educational, comprehensive
- [igraph](S1-rapid/igraph.md) - C core, production balance
- [graph-tool](S1-rapid/graph-tool.md) - C++ Boost, maximum performance
- [snap.py](S1-rapid/snap-py.md) - Stanford, billion-node focus
- [CDlib](S1-rapid/cdlib.md) - Community detection specialist
- [NetworKit](S1-rapid/networkit.md) - OpenMP parallelism
- [**Recommendation**](S1-rapid/recommendation.md) - Decision matrices and guidance

**Key finding**: NetworkX for learning/prototyping, igraph for production, graph-tool for massive graphs, NetworKit for parallelism.

### S2: Comprehensive Analysis (HOW do they work?)
**Focus**: Technical deep-dive for architectural understanding
**Philosophy**: Understand the entire solution space
**Read time**: 30-60 minutes

- [Approach](S2-comprehensive/approach.md) - Technical analysis methodology
- [NetworkX](S2-comprehensive/networkx.md) - Architecture, algorithms, API
- [igraph](S2-comprehensive/igraph.md) - C implementation details
- [graph-tool](S2-comprehensive/graph-tool.md) - Boost Graph Library internals
- [snap.py](S2-comprehensive/snap-py.md) - SWIG bindings, scale focus
- [CDlib](S2-comprehensive/cdlib.md) - Wrapper pattern analysis
- [NetworKit](S2-comprehensive/networkit.md) - Parallel algorithm engineering
- [Feature Comparison](S2-comprehensive/feature-comparison.md) - Side-by-side technical comparison
- [**Recommendation**](S2-comprehensive/recommendation.md) - Architecture-driven selection

**Key finding**: Library choice is fundamentally an architectural trade-off - no library dominates all dimensions. Ease vs performance, single-core vs multi-core, general vs specialized.

### S3: Need-Driven Discovery (WHO needs this + WHY?)
**Focus**: Requirements-first selection
**Philosophy**: Map use cases to exact-fit solutions
**Read time**: 20-40 minutes

- [Approach](S3-need-driven/approach.md) - Persona-based methodology
- [Data Science Researchers](S3-need-driven/use-case-data-science-research.md) - Academic research, 10K-1M nodes → NetworkX
- [Network Infrastructure Engineers](S3-need-driven/use-case-network-infrastructure.md) - Production monitoring, 100K-10M nodes → igraph
- [Bioinformatics Researchers](S3-need-driven/use-case-bioinformatics.md) - Omics networks, advanced methods → graph-tool
- [Fraud/Security Analysts](S3-need-driven/use-case-fraud-security.md) - Real-time detection, scalability → igraph or graph-tool
- [Product Analysts](S3-need-driven/use-case-product-analytics.md) - Fast iteration, visualization → NetworkX
- [**Recommendation**](S3-need-driven/recommendation.md) - Requirement-driven mapping

**Key finding**: The "best" library depends entirely on persona - team skills, scale, priorities, and constraints drive selection more than raw performance.

### S4: Strategic Selection (Long-term viability)
**Focus**: Multi-year architectural decisions
**Philosophy**: Think long-term - maintenance, ecosystem, vendor risk
**Read time**: 15-30 minutes

- [Approach](S4-strategic/approach.md) - Strategic analysis framework
- [NetworkX Viability](S4-strategic/networkx-viability.md) - NumFOCUS backing, 20-year track record → Excellent
- [igraph Viability](S4-strategic/igraph-viability.md) - Multi-language, stable → Good
- [graph-tool Viability](S4-strategic/graph-tool-viability.md) - Single maintainer → Moderate risk
- [snap.py Viability](S4-strategic/snap-viability.md) - Declining momentum → Moderate concern
- [NetworKit Viability](S4-strategic/networkit-viability.md) - Rising momentum, HPC trend → Good
- [CDlib Viability](S4-strategic/cdlib-viability.md) - Niche but low-risk addition → Moderate
- [**Recommendation**](S4-strategic/recommendation.md) - Strategic playbook

**Key finding**: NetworkX has best long-term sustainability (NumFOCUS, 20 years). graph-tool has bus factor risk (single maintainer). NetworKit rising momentum favors parallelism. Choose libraries that keep future options open.

## Supplementary: Domain Explainer

**For**: Non-specialists, technical decision-makers
**Purpose**: Understand the domain through universal analogies
**Read time**: 5-10 minutes

- [**Domain Explainer**](../DOMAIN_EXPLAINER.md) - What social network analysis solves, accessible analogies, when you need it, trade-offs

## Quick Navigation

### By Goal

**Want quick answer?** → [S1 Recommendation](S1-rapid/recommendation.md)
**Want technical depth?** → [S2 Feature Comparison](S2-comprehensive/feature-comparison.md)
**Want use-case fit?** → [S3 Recommendation](S3-need-driven/recommendation.md)
**Want long-term view?** → [S4 Recommendation](S4-strategic/recommendation.md)
**Want to understand domain?** → [Domain Explainer](../DOMAIN_EXPLAINER.md)

### By Library

**NetworkX**: [S1](S1-rapid/networkx.md) | [S2](S2-comprehensive/networkx.md) | [S4](S4-strategic/networkx-viability.md)
**igraph**: [S1](S1-rapid/igraph.md) | [S2](S2-comprehensive/igraph.md) | [S4](S4-strategic/igraph-viability.md)
**graph-tool**: [S1](S1-rapid/graph-tool.md) | [S2](S2-comprehensive/graph-tool.md) | [S4](S4-strategic/graph-tool-viability.md)
**snap.py**: [S1](S1-rapid/snap-py.md) | [S2](S2-comprehensive/snap-py.md) | [S4](S4-strategic/snap-viability.md)
**NetworKit**: [S1](S1-rapid/networkit.md) | [S2](S2-comprehensive/networkit.md) | [S4](S4-strategic/networkit-viability.md)
**CDlib**: [S1](S1-rapid/cdlib.md) | [S2](S2-comprehensive/cdlib.md) | [S4](S4-strategic/cdlib-viability.md)

### By Question

**"Which library should I use?"** → [S1 Recommendation](S1-rapid/recommendation.md)
**"How do they compare technically?"** → [S2 Feature Comparison](S2-comprehensive/feature-comparison.md)
**"What fits my use case?"** → [S3 Recommendation](S3-need-driven/recommendation.md)
**"Will this choice last 5 years?"** → [S4 Recommendation](S4-strategic/recommendation.md)
**"What even is network analysis?"** → [Domain Explainer](../DOMAIN_EXPLAINER.md)

## Summary Decision Tree

```
1. Graph size?
   <10K → NetworkX
   10K-1M → igraph
   1M-100M → graph-tool or NetworKit
   >100M → NetworKit or snap.py

2. Team skills?
   Mixed/learning → NetworkX
   Engineers → igraph
   Specialists → graph-tool

3. Special needs?
   SBM → graph-tool (only option)
   Multi-core server → NetworKit
   Community detection focus → CDlib
   Billion nodes → snap.py

4. Strategic risk tolerance?
   Low risk → NetworkX or igraph
   Moderate → NetworKit
   High → graph-tool
```

## The One-Line Summary

**NetworkX to learn, igraph for production, graph-tool for scale, NetworKit for parallelism, snap.py for billions, CDlib for communities.**

## Research Completeness

✅ S1-rapid: Complete (approach, 6 libraries, recommendation)
✅ S2-comprehensive: Complete (approach, 6 libraries, feature comparison, recommendation)
✅ S3-need-driven: Complete (approach, 5 use cases, recommendation)
✅ S4-strategic: Complete (approach, 6 viability assessments, recommendation)
✅ Domain Explainer: Complete (all required sections)
✅ Discovery TOC: Complete

**Research quality**: All 4 passes independently valuable, cumulative insights across passes.
