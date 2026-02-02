# Use Case: Software Architect

## Who Needs This

**Persona:** Alex Kim, senior software architect at mid-sized tech company
- Documenting microservice architecture (80 services)
- Creating technical documentation for new engineers
- Maintaining system design docs in Git (Markdown/Sphinx)
- Needs automated diagram generation (code → diagrams)
- CI/CD integration for up-to-date documentation

**Context:** Managing transition from monolith to microservices. Documentation must stay synchronized with codebase, generate automatically, and be version-controlled.

## Why They Need Graph Visualization

**Problem:**
- Manual diagram updates fall out of sync with reality
- New engineers need visual overview of service dependencies
- Architecture review meetings require clear dependency graphs
- Debugging production issues needs call graph visualization

**Success Criteria:**
- ✅ Automated diagram generation from code/config
- ✅ Version-controlled diagrams (Git-friendly formats)
- ✅ CI/CD pipeline integration (diagrams auto-update)
- ✅ Hierarchical layouts (services grouped by domain)
- ✅ Static output (embedded in Markdown/Sphinx docs)

## Requirements

### Technical
- **Scale:** 50-200 services, 200-500 dependencies
- **Layout:** Hierarchical (top-down), clear direction of dependencies
- **Output:** SVG (web docs), PNG (presentations), PDF (design docs)
- **Automation:** Script-driven, no manual positioning
- **Reproducibility:** Same input → same output (deterministic)

### Workflow
- Parse service registry or Kubernetes configs
- Extract dependencies (service A calls service B)
- Generate dependency graph
- Render diagram
- Commit to docs/ directory
- CI rebuilds on code changes

### Constraints
- Must run in Docker containers (CI/CD environment)
- No GUI dependencies (headless rendering)
- Fast rendering (<10 seconds for CI)
- Lightweight (docs repo stays small)

## Recommended Solution

### Primary: Graphviz (DOT language)

**Why this choice:**
1. **Best hierarchical layouts:** dot engine excels at directed graphs
2. **Deterministic:** Same DOT input → same output (Git-friendly)
3. **Automation-friendly:** Pure text input, scriptable rendering
4. **CI/CD ready:** Available in Docker images, fast rendering
5. **Industry standard:** Used by Doxygen, Sphinx, PlantUML

**Workflow:**
```python
from graphviz import Digraph

# Generate from service registry
g = Digraph('Architecture', format='svg')
g.attr(rankdir='LR')  # Left-to-right

# Group by domain
with g.subgraph(name='cluster_payment') as c:
    c.attr(label='Payment Domain', style='filled', color='lightgrey')
    c.node('payment-api')
    c.node('payment-processor')

with g.subgraph(name='cluster_user') as c:
    c.attr(label='User Domain', style='filled', color='lightblue')
    c.node('user-api')
    c.node('auth-service')

# Dependencies
g.edge('user-api', 'payment-api', label='REST')
g.edge('payment-api', 'payment-processor', label='async')

# Render
g.render('docs/architecture', cleanup=True)
```

**Output:** SVG embedded in Markdown, version-controlled.

### Alternative: NetworkX → Graphviz (for complex parsing)

**When to use:**
- Complex dependency extraction (parse Kubernetes YAML, Terraform configs)
- Need graph algorithms (find circular dependencies, critical paths)
- Already using NetworkX for analysis

**Pattern:**
```python
import networkx as nx
from networkx.drawing.nx_agraph import write_dot

# Parse and analyze
G = nx.DiGraph()
# ... build graph from configs ...

# Find cycles (circular dependencies)
cycles = list(nx.simple_cycles(G))
if cycles:
    print(f"WARNING: Circular dependencies: {cycles}")

# Export to Graphviz
write_dot(G, 'arch.dot')
# Render with Graphviz CLI or Python bindings
```

### Avoid: Plotly, PyVis, Cytoscape, Gephi

**Why not interactive (Plotly/PyVis):**
- Documentation needs static embeds (Markdown, Sphinx)
- Interactive HTML is overkill for architecture diagrams
- Git diffs on HTML files are messy (large JSON blobs)

**Why not desktop tools (Cytoscape/Gephi):**
- Require GUI (incompatible with CI/CD headless environments)
- Manual operation doesn't scale (80+ services)
- Heavyweight for this use case

## Detailed Implementation

### Parsing Kubernetes Service Mesh
```python
import yaml
from graphviz import Digraph

g = Digraph('ServiceMesh', format='svg')
g.attr(rankdir='TB')  # Top-to-bottom

# Parse all Kubernetes manifests
for yaml_file in Path('k8s/').glob('*.yaml'):
    with open(yaml_file) as f:
        manifest = yaml.safe_load(f)
        if manifest['kind'] == 'Service':
            service_name = manifest['metadata']['name']
            namespace = manifest['metadata']['namespace']
            g.node(service_name, label=service_name,
                   color='blue' if namespace == 'production' else 'gray')

# Parse dependencies from service annotations
# (assumes custom annotations: dependencies.io/calls)
for yaml_file in Path('k8s/').glob('*.yaml'):
    # ... extract edges from annotations ...
    g.edge(caller, callee, label=protocol)

g.render('docs/images/service-mesh', cleanup=True)
```

### CI/CD Integration (GitHub Actions)
```yaml
# .github/workflows/docs.yml
name: Update Architecture Diagrams

on:
  push:
    paths:
      - 'k8s/**'
      - 'services/**'

jobs:
  diagrams:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Graphviz
        run: sudo apt-get install -y graphviz
      - name: Generate diagrams
        run: python scripts/generate_arch_diagrams.py
      - name: Commit updates
        run: |
          git config user.name "Architecture Bot"
          git add docs/images/*.svg
          git commit -m "docs: update architecture diagrams" || true
          git push
```

**Result:** Diagrams auto-update on service changes.

### Sphinx Integration
```restructuredtext
Architecture Overview
=====================

Our microservice architecture:

.. image:: images/service-mesh.svg
   :width: 100%
   :alt: Service dependency graph

Dependencies are automatically generated from Kubernetes manifests.
Last updated: |today|
```

**Benefit:** Documentation always reflects current architecture.

## Alternative Scenarios

### If Need Interactive Exploration
**Add:** Plotly for internal dashboard
- Keep Graphviz for static docs
- Build Plotly dashboard for "live" service graph
- Link to Grafana/Datadog for runtime dependencies

### If Architecture is Massive (>500 services)
**Switch to:** Multi-level documentation
- Domain-level overview (Graphviz)
- Per-domain detailed graphs (Graphviz)
- Interactive drill-down (custom D3.js or Plotly)

### If Need Real-Time Dependency Mapping
**Add:** Distributed tracing
- Use Jaeger/Zipkin for runtime call graphs
- Graphviz for static design-time dependencies
- Combine: design vs. reality comparison

## Tools Comparison for This Use Case

| Library | Fit Score | Reasoning |
|---------|-----------|-----------|
| Graphviz | ⭐⭐⭐⭐⭐ | Perfect - hierarchical, scriptable, CI-friendly |
| NetworkX + Graphviz | ⭐⭐⭐⭐ | Good for complex analysis + rendering |
| PlantUML | ⭐⭐⭐⭐ | Alternative, similar benefits |
| Plotly | ⭐⭐ | Overkill for static docs |
| PyVis | ⭐ | Not suitable for documentation |
| Gephi/Cytoscape | ⭐ | Manual, not automatable |

## Success Indicators

**This recommendation works if:**
- ✅ Architecture is relatively stable (not changing hourly)
- ✅ CI/CD pipeline exists
- ✅ Team uses version control for docs
- ✅ Hierarchical layout is appropriate (directed dependencies)

**Reconsider if:**
- ❌ Need real-time updates (use distributed tracing dashboards)
- ❌ Non-hierarchical architecture (microservices mesh) - may need force-directed
- ❌ Team prefers manual diagram tools (draw.io, Lucidchart) - cultural fit matters

## Long-Term Benefits

1. **Always up-to-date:** Diagrams auto-regenerate on changes
2. **Onboarding:** New engineers see current architecture
3. **Debugging:** Dependency graphs aid incident response
4. **Architecture governance:** Detect circular dependencies automatically
5. **Historical view:** Git history shows architecture evolution
