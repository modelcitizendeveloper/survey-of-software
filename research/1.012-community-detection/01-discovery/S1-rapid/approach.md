# S1 Rapid Discovery: Approach

**Goal:** Identify the key community detection libraries for rapid decision-making.

**Time Budget:** 2-4 hours

**Methodology:**
1. Identify ecosystem leaders via GitHub stars, PyPI downloads, and citation counts
2. Focus on actively maintained libraries (commits within last 12 months)
3. Prioritize libraries with strong Python integration
4. Evaluate based on speed, ease of use, and community support

**Libraries Selected:**
- **Louvain** (NetworkX/python-louvain): Most popular modularity-based algorithm
- **Label Propagation** (NetworkX/NetworKit): Fast, simple consensus-based approach
- **Spectral Clustering** (scikit-learn): Matrix-based mathematical method
- **Infomap** (mapequation.org): Information theory-based approach
- **cdlib**: Meta-library aggregating 39+ algorithms

**Decision Criteria:**
- Algorithm speed for networks with 10K-1M nodes
- Ease of integration with existing NetworkX workflows
- Quality of community detection (modularity scores)
- Maintenance status and ecosystem maturity
