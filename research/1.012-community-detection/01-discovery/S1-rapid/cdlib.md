# CDlib (Community Detection Library)

## Overview

CDlib is a meta-library that aggregates 39+ community detection algorithms into a single unified API. Instead of implementing one algorithm, it provides a standardized interface for comparing multiple methods.

**Key Stats:**
- **Ecosystem:** ~405 GitHub stars, Python-only
- **Maintenance:** Active, published in Applied Network Science (2019)
- **Algorithms:** 39+ implementations (Louvain, Leiden, Infomap, Label Propagation, etc.)
- **Output:** Standardized clustering representations, overlapping/fuzzy/edge clusterings

## When to Use

**Best for:**
- Comparing multiple algorithms on the same dataset
- Research requiring systematic evaluation
- Projects where the "right" algorithm is unknown
- Integration testing across community detection methods

**Avoid when:**
- You need a single, production-optimized implementation
- Minimizing dependencies is critical
- Performance is paramount (wrapper overhead exists)
- You've already chosen a specific algorithm

## Strengths

1. **Comprehensive:** Largest collection of community detection algorithms in one package
2. **Standardization:** Consistent input/output across all algorithms
3. **Evaluation:** Built-in quality metrics (modularity, NMI, ARI, etc.)
4. **Comparison tools:** Efficiently compare methods and parameter variations
5. **Visualization:** Tools to analyze and visualize clusterings

## Limitations

1. **Overhead:** Wrapper layer adds complexity and potential performance cost
2. **Dependencies:** Inherits dependencies from all wrapped libraries
3. **Version lag:** May not have latest algorithm improvements immediately
4. **Indirection:** Debugging issues requires understanding underlying libraries

## What It Wraps

CDlib **inherits** implementations from original projects when possible:
- Louvain → python-louvain
- Leiden → leidenalg
- Infomap → infomap (mapequation.org)
- NetworkX algorithms → native NetworkX
- igraph algorithms → python-igraph

**Automatic conversion:** Handles NetworkX ↔ igraph conversion transparently

## Performance Context (2024 Study)

A comprehensive 2024 comparison of Python community detection libraries found:
- **igraph:** Fastest execution, efficient memory, user-friendly
- **CDlib:** Most comprehensive due to extensive features and evaluation capabilities
- **NetworkX:** Slower but widely adopted
- **Scikit-Network:** Specialized use cases

**Verdict:** CDlib trades raw speed for breadth and evaluation power.

## Ecosystem Maturity

**Production-ready for research.** Excellent for exploration and systematic comparison. For production, use the underlying library directly (e.g., Leiden via leidenalg).

**Recommendation tier:** **Best for algorithm selection and benchmarking**, not for optimized production deployment.

## Sources

- [CDLIB: a python library to extract, compare and evaluate communities (Applied Network Science)](https://link.springer.com/article/10.1007/s41109-019-0165-9)
- [CDlib Documentation](https://cdlib.readthedocs.io/)
- [GitHub: GiulioRossetti/cdlib](https://github.com/GiulioRossetti/cdlib)
- [Performance Evaluation of Python Libraries for Community Detection (2024)](https://www.researchgate.net/publication/382750317_Performance_Evaluation_of_Python_Libraries_for_Community_Detection_on_Large_Social_Network_Graphs)
