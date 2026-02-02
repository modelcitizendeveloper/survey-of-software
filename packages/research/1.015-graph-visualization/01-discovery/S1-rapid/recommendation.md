# S1 Recommendation: Quick Decision Guide

## TL;DR

| Priority | Library | Best For | Avoid If |
|----------|---------|----------|----------|
| 1st | NetworkX + matplotlib | Graph algorithms + basic viz | Need interactivity |
| 2nd | Plotly | Interactive dashboards | Static output only |
| 3rd | PyVis | Quick HTML demos | Production apps |
| 4th | Graphviz | Hierarchical diagrams, docs | Need interactivity |
| 5th | py4cytoscape | Biological networks | No desktop install |
| 6th | gephi-toolkit | Massive graphs (>500K) | Need Python-native |

## Decision Tree

### Start Here: What's your primary goal?

**"I need to compute graph metrics (shortest paths, centrality, communities)"**
→ **NetworkX** - It's the NumPy of graph theory. Visualization is secondary.

**"I need interactive exploration in a web browser or Jupyter"**
→ **Plotly** if building dashboards or polished apps
→ **PyVis** if prototyping with minimal code (but note vis.js maintenance risk)

**"I need publication-quality static diagrams"**
→ **Graphviz** for hierarchical/directed graphs (flowcharts, dependency trees)
→ **py4cytoscape** for biological networks (requires Cytoscape desktop)

**"I'm working with massive graphs (100K+ nodes)"**
→ **Graphviz** (best scaling for static output)
→ **Gephi desktop** (manually, Python integration is poor)

## Common Combinations

Real-world workflows often combine libraries:

- **NetworkX + Plotly:** Compute with NetworkX, visualize interactively with Plotly
- **NetworkX + PyVis:** Quick prototype - `PyVis.from_nx(G)` and you're done
- **NetworkX + Graphviz:** Algorithm analysis in Python, documentation diagrams with DOT
- **Pandas → NetworkX → PyVis:** Data pipeline to interactive network

## Red Flags

**Avoid these mistakes:**

❌ Using NetworkX/matplotlib for final deliverables (unless target is scientific papers)
❌ PyVis in production (vis.js is unmaintained, security risk)
❌ Attempting gephi-toolkit automation (better to export GEXF and use desktop)
❌ Installing Cytoscape just for simple graphs (massive overkill)

## Quick Wins

**Fast paths to success:**

✅ NetworkX for computation + any visualization library for display
✅ Plotly if already using it for other charts
✅ Graphviz if generating documentation programmatically
✅ PyVis for internal demos (not production)

## When to Go to S2

Move to comprehensive analysis if:

- Performance is critical (need benchmarks)
- Choosing between 2-3 finalists (need feature comparison)
- Building long-term architecture (need strategic insights)
- None of these libraries "obviously" fit your use case
