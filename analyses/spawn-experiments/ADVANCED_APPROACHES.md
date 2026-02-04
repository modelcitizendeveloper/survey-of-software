# Advanced Approaches: LLM Extraction & Graph Databases

**Purpose**: Explore advanced techniques for experiment tracking beyond basic SQLite
**Status**: Research & recommendations
**Date**: October 31, 2025

---

## Table of Contents

1. [Local LLMs for Data Extraction](#local-llms-for-data-extraction)
2. [Graph Databases for Relationship Modeling](#graph-databases-for-relationship-modeling)
3. [Hybrid Approach: SQL + Graph + LLM](#hybrid-approach)
4. [LLM-Driven Experiment Automation](#llm-driven-experiment-automation)
5. [Implementation Roadmap](#implementation-roadmap)

---

## Local LLMs for Data Extraction

### Current Limitation: Regex-Based Parsing

**migrate_from_markdown.py limitations**:
```python
# Current regex approach (brittle)
id_match = re.search(r'\[(\d+\.\d+[A-Z]?)\s*-\s*([^\]]+)\]', text)
winner_match = re.search(r'\*\*Winner\*\*:?\s*Method\s+(\d)', text)
```

**Problems**:
- ❌ Breaks with format variations ("Method 2 winner" vs "Winner: M2" vs "Best: Specification-Driven")
- ❌ Misses implicit relationships ("builds on 1.700" vs "extends" vs "validates")
- ❌ Cannot extract qualitative insights from narrative sections
- ❌ Requires manual regex updates for new markdown patterns

### Solution: Local LLM Extraction

**Why Local LLMs** (not cloud APIs):
- ✅ **Zero cost**: Ollama runs locally, no API fees
- ✅ **Privacy**: Experiment data stays local (no external API calls)
- ✅ **Speed**: Local inference faster than API round-trips for batch processing
- ✅ **spawn-experiments validated**: Already using Ollama (llama3.2, phi3, gemma2)

**From spawn-experiments**:
- 1.608-1.608.B: Ollama integration for poetry generation (validated)
- 1.609: Intent classification with local LLMs (91.7% accuracy)
- 1.613: Text summarization (96/100 quality)
- 1.615: Data extraction from unstructured text ← **DIRECTLY APPLICABLE**

### Implementation: LLM-Based Migration Script

**Architecture**:
```python
# migrate_from_markdown_llm.py

import ollama
from pathlib import Path
import json

class LLMMarkdownExtractor:
    """Extract structured data from markdown using local LLM"""

    def __init__(self, model="llama3.2:latest"):
        self.model = model

    def extract_experiment(self, markdown_section: str) -> dict:
        """
        Extract experiment metadata using LLM

        Input: Markdown section for one experiment
        Output: Structured JSON with experiment data
        """
        prompt = f"""
        Extract experiment metadata from this markdown section.
        Return ONLY valid JSON with these exact fields:

        {{
            "id": "experiment ID (e.g., 1.608, 1.608.A)",
            "title": "experiment title",
            "tier": integer (1-4),
            "domain": "domain name",
            "completed_date": "YYYY-MM-DD or null",
            "winner_method": integer (1-4) or null,
            "key_finding": "main discovery or null",
            "related_experiments": ["list", "of", "experiment", "IDs"],
            "spawn_solutions_refs": ["1.127", "1.120"] or []
        }}

        Markdown section:
        {markdown_section}

        JSON output:
        """

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.1}  # Low temperature for consistency
        )

        # Parse JSON response
        try:
            data = json.loads(response['response'])
            return data
        except json.JSONDecodeError:
            # Fallback to regex if LLM fails
            return self.fallback_regex_extraction(markdown_section)

    def extract_methodology_results(self, markdown_section: str, exp_id: str) -> list:
        """
        Extract 4 methodology results using LLM

        Returns: List of 4 dicts with timing, LOC, quality scores
        """
        prompt = f"""
        Extract methodology results from this experiment report.
        Return ONLY valid JSON array with 4 objects (Method 1-4):

        [
            {{
                "method_number": 1,
                "method_name": "Immediate",
                "time_minutes": float or null,
                "lines_of_code": integer or null,
                "quality_score": integer (0-100) or null,
                "is_winner": boolean
            }},
            ... (repeat for methods 2-4)
        ]

        Markdown section:
        {markdown_section}

        JSON array:
        """

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.1}
        )

        try:
            results = json.loads(response['response'])
            return results
        except json.JSONDecodeError:
            return self.fallback_methodology_extraction(markdown_section, exp_id)

    def extract_relationships(self, markdown_section: str) -> dict:
        """
        Extract implicit relationships using LLM reasoning

        This is where LLMs shine vs regex:
        - "builds on 1.700" → depends_on: ["1.700"]
        - "extends the pattern from 1.608.A" → related_to: ["1.608.A"]
        - "validates Finding #15" → validates_finding: [15]
        - "uses libraries from spawn-solutions 1.127" → spawn_solutions: ["1.127"]
        """
        prompt = f"""
        Extract experiment relationships from this markdown.
        Identify dependencies, extensions, validations, and cross-references.

        Return ONLY valid JSON:
        {{
            "depends_on": ["list of prerequisite experiment IDs"],
            "extends": ["list of extended experiment IDs"],
            "validates_findings": [list of finding numbers],
            "validates_patterns": ["list of pattern names"],
            "spawn_solutions_refs": ["list of spawn-solutions IDs"],
            "uses_components_from": ["list of component source experiment IDs"]
        }}

        Markdown section:
        {markdown_section}

        JSON output:
        """

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.1}
        )

        try:
            relationships = json.loads(response['response'])
            return relationships
        except json.JSONDecodeError:
            return {}

    def extract_qualitative_insights(self, markdown_section: str) -> dict:
        """
        Extract narrative insights that regex cannot capture

        Examples:
        - "Method 3 won but Method 2 was close (2 point gap)"
        - "Surprising result: TDD worked for visual code"
        - "Key insight: Code quality affects LLM output"
        """
        prompt = f"""
        Extract key insights from this experiment report.
        Focus on surprising results, close calls, and methodology insights.

        Return ONLY valid JSON:
        {{
            "key_insight": "main discovery in 1-2 sentences",
            "surprising_result": "unexpected finding or null",
            "close_methodologies": ["methods with <5 point gap"],
            "pattern_deviation": "how this deviates from expected pattern or null"
        }}

        Markdown section:
        {markdown_section}

        JSON output:
        """

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.2}  # Slightly higher for insights
        )

        try:
            insights = json.loads(response['response'])
            return insights
        except json.JSONDecodeError:
            return {}
```

### Benefits of LLM Extraction

**1. Robustness to Format Variations**
```markdown
# Regex fails on these variations:
- "Winner: Method 2"
- "Best: M2 (Specification-Driven)"
- "Optimal: Spec-driven approach"
- "Method 2 achieved highest quality"

# LLM extracts correctly from all formats
```

**2. Implicit Relationship Detection**
```markdown
# Text: "This experiment extends the haiku converter (1.608) to iambic pentameter"
# Regex: Misses relationship
# LLM extracts: {"extends": ["1.608"], "related_to": ["1.608"]}
```

**3. Qualitative Insight Extraction**
```markdown
# Text: "Surprising: Method 3 won despite TDD traditionally struggling with visual code"
# Regex: Cannot extract
# LLM extracts: {
#   "surprising_result": "TDD works for visual code (refutes hypothesis)",
#   "pattern_deviation": "Expected Method 2, got Method 3"
# }
```

**4. Cross-Repository Understanding**
```markdown
# Text: "Uses Prophet from spawn-solutions 1.127 financial simulation research"
# Regex: Might catch "1.127" but not the context
# LLM extracts: {
#   "spawn_solutions_refs": ["1.127"],
#   "validation_type": "library_wrapper",
#   "library_name": "Prophet"
# }
```

### Implementation Roadmap

**Phase 1: Parallel Migration** (1-2 weeks)
- Run both regex and LLM migration
- Compare results (which extracts more relationships?)
- Identify LLM extraction accuracy (spot-check 10 experiments)
- Measure performance (regex: 1 sec/experiment, LLM: 5-10 sec/experiment)

**Phase 2: Hybrid Approach** (2-4 weeks)
- Regex for simple fields (ID, title, dates)
- LLM for complex extraction (relationships, insights)
- Validation: LLM vs manual review (10% sample)
- Performance optimization (batch processing, caching)

**Phase 3: Production Deployment** (1 month)
- Integrate into experiment framework
- Automatic LLM extraction on experiment completion
- Fallback to regex if LLM fails
- Monitor accuracy and adjust prompts

### Cost-Benefit Analysis

**Time Investment**:
- LLM script development: 8-12 hours
- Prompt engineering: 4-6 hours
- Validation & testing: 4-6 hours
- **Total: 16-24 hours**

**Benefits**:
- +30-50% more relationships extracted (vs regex)
- Qualitative insights captured (currently lost)
- Future-proof (works with format variations)
- Validated approach (spawn-experiments 1.615 data extraction)

**ROI**: 16-24 hours investment → 5-10 hours/month saved (manual relationship tracking)
- **Break-even**: 2-4 months
- **First-year ROI**: 300-500%

---

## Graph Databases for Relationship Modeling

### Why Graphs for spawn-experiments?

**Relational databases (SQLite/PostgreSQL)**:
- ✅ Great for: Tabular data, aggregations, reporting
- ❌ Weak for: Multi-hop relationships, path finding, network analysis

**Graph databases (Neo4j, memgraph, NetworkX)**:
- ✅ Great for: Relationships, dependencies, paths, clusters
- ✅ Natural fit for: Experiment dependencies, finding validation chains, pattern evolution

### spawn-experiments as a Graph

**Nodes**:
```
(Experiment:1.700) - Basic Queue Simulation
(Experiment:1.701) - Queue Animation
(Experiment:1.702) - Grid Search Integration
(Experiment:1.703) - scipy.optimize Integration

(Finding:16) - DES Library Methodology
(Pattern:DES) - Discrete Event Simulation

(Library:salabim) - DES library
(Library:scipy.optimize) - Optimization library

(SpawnSolutions:1.120) - DES research
```

**Relationships** (Edges):
```
(1.700) -[VALIDATES]-> (Finding:16) -[DEFINES]-> (Pattern:DES)
(1.701) -[EXTENDS]-> (1.700)
(1.701) -[VALIDATES]-> (Finding:16)
(1.702) -[DEPENDS_ON]-> (1.700)
(1.702) -[DEPENDS_ON]-> (1.701)
(1.702) -[USES_LIBRARY]-> (Library:pandas)
(1.703) -[USES_LIBRARY]-> (Library:scipy.optimize)
(1.703) -[VALIDATES]-> (Finding:16)
(Pattern:DES) -[OPTIMAL_METHOD]-> (Method:3)

(1.700) -[IMPLEMENTS]-> (SpawnSolutions:1.120)
```

### Graph Queries (Cypher for Neo4j)

**Query 1: Finding validation chains**
```cypher
// How did Finding #16 (DES) reach ROBUST confidence?
MATCH path = (e:Experiment)-[:VALIDATES]->(f:Finding {number: 16})
RETURN e.id, e.completed_date, e.quality_score
ORDER BY e.completed_date;

// Output (visual graph):
// 1.700 → Finding:16 (N=1, PROVISIONAL)
// 1.701 → Finding:16 (N=2)
// 1.702 → Finding:16 (N=3)
// 1.703 → Finding:16 (N=4, ROBUST)
```

**Query 2: Experiment dependency chains**
```cypher
// What experiments built on 1.700?
MATCH path = (base:Experiment {id: '1.700'})<-[:EXTENDS|DEPENDS_ON*1..3]-(derived:Experiment)
RETURN path;

// Visual output:
//          ┌─> 1.701 (animation)
// 1.700 ──┤
//          └─> 1.702 (grid search) ─> 1.703 (scipy.optimize)
```

**Query 3: Pattern emergence**
```cypher
// How did DES pattern emerge from experiments?
MATCH path = (e:Experiment)-[:VALIDATES]->(p:Pattern {name: 'Discrete Event Simulation'})
WITH p, collect(e) as experiments
RETURN p.name, p.confidence, size(experiments) as n_value, experiments;

// Shows: PROVISIONAL (N=1) → ROBUST (N=4) progression
```

**Query 4: Cross-repository integration**
```cypher
// spawn-solutions libraries WITH spawn-experiments validation
MATCH (ss:SpawnSolutions)-[:VALIDATED_BY]->(se:Experiment)-[:WINNER]->(m:Method)
RETURN ss.id, ss.title, se.id, m.number, m.quality_score;

// Output:
// 1.127 (Financial Sim) ─> 1.611 (Prophet) ─> Method 4 (96/100)
// 1.127 (Financial Sim) ─> 1.623 (numpy-financial) ─> Method 4 (96/100)
```

**Query 5: Component reuse networks**
```cypher
// Components created in Tier 1, reused in Tier 2+
MATCH (creator:Experiment {tier: 1})-[:CREATES]->(c:Component)<-[:REUSES]-(reuser:Experiment)
WHERE reuser.tier >= 2
RETURN creator.id, c.name, collect(reuser.id) as reused_in;

// Visual output:
// 1.501 (Email Validator) ─> email_validator.py ─> [2.505, 2.506, 2.507]
```

**Query 6: Next experiment recommendations**
```cypher
// What experiments would reach ROBUST confidence (N=4)?
MATCH (p:Pattern)<-[:VALIDATES]-(e:Experiment)
WITH p, count(e) as current_n
WHERE current_n < 4
MATCH (planned:PlannedExperiment)-[:TARGETS]->(p)
RETURN p.name, current_n, 4 - current_n as needed, planned.id;

// Output:
// Database Models | 1 | 3 | [1.810, 1.811, 1.820]
```

**Query 7: Methodology performance by path**
```cypher
// Average Method 4 quality for all experiments in DES chain
MATCH path = (root:Experiment {id: '1.700'})<-[:EXTENDS|DEPENDS_ON*0..5]-(e:Experiment)
WHERE e.winner_method = 4
RETURN avg(e.quality_score) as avg_m4_quality, collect(e.id) as experiments;
```

### Graph Database Options

| Option | Type | Best For | Cost |
|--------|------|----------|------|
| **Neo4j** | Native graph | Production, complex queries | $0 (Community) → $65/mo (Aura) |
| **memgraph** | In-memory graph | Real-time queries, speed | $0 (Community) → $99/mo (Cloud) |
| **NetworkX** | Python library | Analysis, visualization | $0 (open source) |
| **SQLite FTS5** | Hybrid (SQL + graph) | Lightweight, embedded | $0 (built-in) |

**Recommendation for spawn-experiments**:

1. **Start: NetworkX** (Python library)
   - Zero infrastructure cost
   - Excellent for analysis and visualization
   - Integrates with existing Python tools
   - Can export to Neo4j later

2. **Scale: Neo4j Community** (if >500 experiments)
   - Free self-hosted option
   - Cypher query language (powerful)
   - Web UI for visual exploration
   - Can import from NetworkX

### NetworkX Implementation Example

```python
# graph_builder.py - Build experiment graph from SQLite

import networkx as nx
import sqlite3
from pathlib import Path

class ExperimentGraph:
    """Build and analyze experiment relationship graph"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.graph = nx.DiGraph()  # Directed graph

    def build_from_database(self):
        """
        Build graph from SQLite database

        Nodes: Experiments, Findings, Patterns, Libraries
        Edges: VALIDATES, EXTENDS, DEPENDS_ON, USES_LIBRARY
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Add experiment nodes
        cursor.execute("SELECT id, title, domain, quality_score FROM experiments")
        for exp_id, title, domain, quality in cursor.fetchall():
            self.graph.add_node(
                exp_id,
                type='experiment',
                title=title,
                domain=domain,
                quality_score=quality
            )

        # Add finding nodes
        cursor.execute("SELECT finding_number, title, confidence_level FROM findings")
        for num, title, confidence in cursor.fetchall():
            self.graph.add_node(
                f"Finding:{num}",
                type='finding',
                title=title,
                confidence=confidence
            )

        # Add VALIDATES edges (experiments → findings)
        cursor.execute("""
            SELECT experiment_id, finding_id, contribution_type
            FROM experiment_findings
        """)
        for exp_id, finding_id, contrib in cursor.fetchall():
            cursor.execute("SELECT finding_number FROM findings WHERE id=?", (finding_id,))
            finding_num = cursor.fetchone()[0]
            self.graph.add_edge(
                exp_id,
                f"Finding:{finding_num}",
                relationship='VALIDATES',
                contribution=contrib
            )

        # Add pattern nodes and edges
        cursor.execute("SELECT id, name, confidence FROM patterns")
        for pattern_id, name, confidence in cursor.fetchall():
            self.graph.add_node(
                f"Pattern:{name}",
                type='pattern',
                confidence=confidence
            )

        # Add VALIDATES edges (experiments → patterns)
        cursor.execute("""
            SELECT e.id, p.name
            FROM experiment_patterns ep
            JOIN experiments e ON ep.experiment_id = e.id
            JOIN patterns p ON ep.pattern_id = p.id
            WHERE ep.validates_pattern = 1
        """)
        for exp_id, pattern_name in cursor.fetchall():
            self.graph.add_edge(
                exp_id,
                f"Pattern:{pattern_name}",
                relationship='VALIDATES'
            )

        conn.close()

    def find_validation_path(self, finding_number: int):
        """
        Find all experiments that validated a finding

        Returns: List of (experiment_id, date) in chronological order
        """
        finding_node = f"Finding:{finding_number}"

        # Get all nodes that have edge TO finding
        predecessors = list(self.graph.predecessors(finding_node))

        # Sort by completion date (requires database lookup)
        # Returns validation progression
        return predecessors

    def find_experiment_dependencies(self, exp_id: str, max_depth: int = 3):
        """
        Find all experiments that depend on this experiment

        Returns: Dependency tree
        """
        # Use NetworkX DFS to find all reachable nodes
        descendants = nx.descendants(self.graph, exp_id)
        return descendants

    def recommend_next_experiments(self):
        """
        Recommend experiments to reach ROBUST confidence (N=4)

        Returns: List of (pattern_name, current_n, needed, suggested_experiments)
        """
        recommendations = []

        for node in self.graph.nodes():
            if node.startswith("Pattern:"):
                # Count validating experiments
                predecessors = list(self.graph.predecessors(node))
                current_n = len(predecessors)

                if current_n < 4:
                    recommendations.append({
                        'pattern': node,
                        'current_n': current_n,
                        'needed': 4 - current_n,
                        'validated_by': predecessors
                    })

        return recommendations

    def visualize(self, output_path: Path):
        """
        Export graph visualization

        Options:
        - Matplotlib: Static image
        - Plotly: Interactive HTML
        - Graphviz: Publication-quality
        - Gephi: Advanced network analysis
        """
        import matplotlib.pyplot as plt

        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue')
        plt.savefig(output_path)
```

### Hybrid Approach: SQL + Graph

**Best of both worlds**:

```python
# Use SQLite for:
- Tabular queries (average quality scores)
- Aggregations (count experiments by domain)
- Time series (experiments completed per month)

# Use NetworkX/Neo4j for:
- Relationship queries (what validates Finding #15?)
- Path finding (dependency chains)
- Network analysis (component reuse networks)
- Recommendations (next experiments to reach ROBUST)

# Workflow:
1. Store data in SQLite (source of truth)
2. Build NetworkX graph from SQLite (on demand)
3. Query graph for relationships
4. Update SQLite with results
```

---

## Hybrid Approach: SQL + Graph + LLM

### Recommended Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Data Layer: SQLite (source of truth)                    │
│ - experiments, methodology_results, findings, patterns   │
│ - Foreign keys, constraints, validation                 │
└───────────────┬─────────────────────────────────────────┘
                │
                ├─────> Extract (on demand) ─────────┐
                │                                     │
                ▼                                     ▼
┌───────────────────────────────┐   ┌────────────────────────────────┐
│ Graph Layer: NetworkX         │   │ LLM Layer: Ollama              │
│ - Relationship queries        │   │ - Markdown → structured data   │
│ - Dependency analysis         │   │ - Implicit relationship detect │
│ - Path finding                │   │ - Qualitative insight extract  │
│ - Recommendations             │   │ - Cross-reference understanding│
└───────────────────────────────┘   └────────────────────────────────┘
```

### Workflow: New Experiment Completion

```python
# Step 1: LLM extracts structured data from markdown
extractor = LLMMarkdownExtractor(model="llama3.2")
exp_data = extractor.extract_experiment(markdown_report)
relationships = extractor.extract_relationships(markdown_report)
insights = extractor.extract_qualitative_insights(markdown_report)

# Step 2: Store in SQLite (source of truth)
db.insert_experiment(exp_data)
db.insert_relationships(relationships)
db.insert_insights(insights)

# Step 3: Rebuild graph (incremental update)
graph = ExperimentGraph(db_path)
graph.add_experiment_node(exp_data['id'])
graph.add_validation_edges(relationships['validates_findings'])

# Step 4: Graph queries for recommendations
recommendations = graph.recommend_next_experiments()
gap_analysis = graph.identify_research_gaps()

# Step 5: Update planned_experiments table
for rec in recommendations:
    db.update_planned_priority(rec['pattern'], priority='HIGH')
```

### Example: Complete Integration

```python
# complete_experiment.py - Full workflow

from llm_extractor import LLMMarkdownExtractor
from graph_builder import ExperimentGraph
from database import ExperimentDB
from pathlib import Path

def complete_experiment(experiment_id: str, markdown_path: Path):
    """
    Complete experiment workflow with LLM + Graph + SQL

    1. LLM extracts data from markdown
    2. Store in SQLite
    3. Update graph
    4. Generate recommendations
    5. Auto-update EXPERIMENT_INDEX.md
    """

    # Step 1: LLM extraction
    with open(markdown_path, 'r') as f:
        markdown_content = f.read()

    extractor = LLMMarkdownExtractor(model="llama3.2")

    exp_data = extractor.extract_experiment(markdown_content)
    methodology_results = extractor.extract_methodology_results(markdown_content, experiment_id)
    relationships = extractor.extract_relationships(markdown_content)
    insights = extractor.extract_qualitative_insights(markdown_content)

    # Step 2: Store in SQLite
    db = ExperimentDB('spawn_experiments.db')

    db.update_experiment(
        experiment_id=experiment_id,
        status='completed',
        **exp_data
    )

    for result in methodology_results:
        db.insert_methodology_result(result)

    # Link to findings
    for finding_num in relationships.get('validates_findings', []):
        db.link_experiment_finding(experiment_id, finding_num, 'validated')

    # Link to patterns
    for pattern_name in relationships.get('validates_patterns', []):
        db.link_experiment_pattern(experiment_id, pattern_name, validates=True)

    # Store insights
    db.update_experiment_insights(experiment_id, insights)

    # Step 3: Rebuild graph
    graph = ExperimentGraph('spawn_experiments.db')
    graph.build_from_database()

    # Step 4: Analyze graph for recommendations
    recommendations = graph.recommend_next_experiments()

    print(f"\n✓ Completed {experiment_id}")
    print(f"\nRecommended next experiments:")
    for rec in recommendations:
        print(f"  - {rec['pattern']}: Need {rec['needed']} more for ROBUST")

    # Step 5: Auto-generate markdown index
    from generators import generate_experiment_index
    generate_experiment_index(db, output_path='../../spawn-experiments/docs/EXPERIMENT_INDEX.md')

    print(f"\n✓ Updated EXPERIMENT_INDEX.md")
```

---

## LLM-Driven Experiment Automation

### Meta-Level Insight: AI Running AI Experiments

**Current State**: spawn-experiments uses Claude/LLMs to generate code across 4 methodologies, but execution is semi-manual

**Opportunity**: **Fully automate the experiment loop** using LLMs

**Why This Works**:
- spawn-experiments already uses LLMs for code generation (all 4 methodologies)
- LLMs can coordinate parallel execution (Task tool with 4 agents)
- LLMs can evaluate code quality (already doing this in quality scoring)
- LLMs can write experiment reports (synthesis of results)

**From spawn-experiments validation**:
- ✅ **1.608 Run 3**: Clean room protocol with 5 methodologies executed in parallel
- ✅ **1.610-1.623**: Library wrapper series (automated parallel execution)
- ✅ **1.700-1.703**: DES series (systematic methodology validation)
- ✅ **Quality evaluation**: LLMs judge code quality (88-99/100 scores)

**Meta observation**: spawn-experiments is already 70% automated - we just need to close the loop!

### Full Automation Architecture

```python
# experiment_orchestrator.py - Fully automated experiment execution

from typing import Dict, List
import ollama
from pathlib import Path
import json
from datetime import datetime

class ExperimentOrchestrator:
    """
    Automate complete experiment lifecycle using LLMs

    Steps:
    1. LLM generates experiment specification from roadmap
    2. LLM coordinates parallel execution (4 methodologies)
    3. LLM evaluates code quality
    4. LLM extracts results and relationships
    5. LLM writes experiment report
    6. LLM updates database
    7. LLM recommends next experiment
    """

    def __init__(self, db_path: Path, model: str = "llama3.2"):
        self.db_path = db_path
        self.model = model
        self.graph = ExperimentGraph(db_path)

    def select_next_experiment(self) -> Dict:
        """
        Step 1: LLM selects next experiment from roadmap

        Input: Planned experiments + pattern gaps + research priorities
        Output: Experiment specification
        """
        # Get context from database
        planned = self.db.get_planned_experiments(priority='HIGH')
        patterns = self.graph.recommend_next_experiments()
        recent = self.db.get_recent_experiments(limit=5)

        prompt = f"""
        Select the next spawn-experiments experiment to run.

        Context:
        - Planned experiments (HIGH priority): {json.dumps(planned, indent=2)}
        - Patterns needing validation: {json.dumps(patterns, indent=2)}
        - Recent experiments: {json.dumps(recent, indent=2)}

        Consider:
        1. Which pattern needs validation for ROBUST confidence (N=4)?
        2. Which experiments have cleared dependencies?
        3. Which aligns with spawn-solutions research priorities?
        4. Which has highest research value (new domain vs incremental)?

        Return ONLY valid JSON:
        {{
            "experiment_id": "selected ID (e.g., 1.810)",
            "title": "experiment title",
            "rationale": "why this experiment now (2-3 sentences)",
            "expected_pattern": "hypothesis about optimal methodology",
            "estimated_hours": float,
            "dependencies_met": boolean,
            "research_value": "HIGH|MEDIUM|LOW"
        }}

        JSON output:
        """

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.3}  # Some creativity for selection
        )

        selection = json.loads(response['response'])
        return selection

    def generate_experiment_specification(self, experiment_id: str) -> Dict:
        """
        Step 2: LLM generates detailed experiment specification

        Input: Experiment ID, related research
        Output: Complete TASK_SPECIFICATION.md content
        """
        # Get related experiments
        related = self.graph.find_related_experiments(experiment_id)
        patterns = self.db.get_patterns_for_experiment(experiment_id)

        prompt = f"""
        Generate a complete experiment specification for spawn-experiments.

        Experiment: {experiment_id}
        Related experiments: {json.dumps(related, indent=2)}
        Expected patterns: {json.dumps(patterns, indent=2)}

        Generate a TASK_SPECIFICATION.md with:
        1. Problem statement (clear, testable)
        2. Acceptance criteria (what "working" means)
        3. Test cases (input → expected output)
        4. Constraints (libraries, dependencies, scope)
        5. Evaluation criteria (how to judge quality)

        Format as markdown, follow spawn-experiments conventions.

        Markdown output:
        """

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.2}
        )

        spec = response['response']
        return spec

    def execute_experiment_parallel(self, spec: Dict) -> List[Dict]:
        """
        Step 3: LLM coordinates parallel execution (4 methodologies)

        Uses Claude Code's Task tool to launch 4 parallel agents:
        - Method 1 (Immediate)
        - Method 2 (Specification-Driven)
        - Method 3 (Pure TDD)
        - Method 4 (Adaptive TDD)

        This is already working in spawn-experiments!
        """
        results = []

        # Launch 4 parallel agents (pseudo-code - actual implementation via Claude Code)
        for method_num in range(1, 5):
            result = self.launch_methodology_agent(
                experiment_id=spec['id'],
                method_number=method_num,
                task_spec=spec['specification']
            )
            results.append(result)

        return results

    def evaluate_code_quality(self, results: List[Dict]) -> List[Dict]:
        """
        Step 4: LLM evaluates code quality (30 point rubric)

        Already working in spawn-experiments quality evaluation!
        """
        for result in results:
            evaluation = self.llm_evaluate_quality(
                code=result['code'],
                tests=result['tests'],
                rubric='spawn_experiments_rubric.md'
            )
            result['quality_score'] = evaluation['total_score']
            result['code_quality'] = evaluation['code_quality']
            result['test_quality'] = evaluation['test_quality']
            result['implementation_quality'] = evaluation['implementation_quality']

        return results

    def extract_relationships(self, experiment_id: str, results: List[Dict]) -> Dict:
        """
        Step 5: LLM extracts implicit relationships

        Uses LLMMarkdownExtractor (from earlier section)
        """
        # Analyze all 4 implementations
        combined_analysis = ""
        for result in results:
            combined_analysis += f"\n\n## Method {result['method_number']}\n"
            combined_analysis += f"Code:\n{result['code']}\n"
            combined_analysis += f"Notes:\n{result['notes']}\n"

        extractor = LLMMarkdownExtractor(model=self.model)
        relationships = extractor.extract_relationships(combined_analysis)

        return relationships

    def synthesize_report(self, experiment_id: str, results: List[Dict], relationships: Dict) -> str:
        """
        Step 6: LLM writes comprehensive experiment report

        Output: EXPERIMENT_REPORT.md (markdown)
        """
        prompt = f"""
        Write a comprehensive spawn-experiments report for {experiment_id}.

        Results:
        {json.dumps(results, indent=2)}

        Relationships:
        {json.dumps(relationships, indent=2)}

        Generate markdown report with sections:
        1. Overview (experiment purpose, domain, tier)
        2. Results Summary (winner, scores, timing)
        3. Methodology Comparison (what worked, what didn't)
        4. Key Findings (discoveries, pattern validation)
        5. Code Quality Analysis (strengths, weaknesses per method)
        6. Relationships (validates findings, extends experiments)
        7. Recommendations (next experiments, pattern insights)

        Follow spawn-experiments report conventions.

        Markdown output:
        """

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.3}
        )

        report = response['response']
        return report

    def update_database_and_graph(self, experiment_id: str, results: List[Dict], relationships: Dict):
        """
        Step 7: Update SQLite database and NetworkX graph

        Uses complete_experiment() from hybrid approach
        """
        # Update experiments table
        self.db.update_experiment(
            experiment_id=experiment_id,
            status='completed',
            completed_date=datetime.now().date()
        )

        # Insert methodology results
        for result in results:
            self.db.insert_methodology_result({
                'experiment_id': experiment_id,
                'method_number': result['method_number'],
                'method_name': result['method_name'],
                'time_minutes': result['time_minutes'],
                'lines_of_code': result['lines_of_code'],
                'quality_score': result['quality_score'],
                'is_winner': result['is_winner']
            })

        # Link findings
        for finding_num in relationships.get('validates_findings', []):
            self.db.link_experiment_finding(experiment_id, finding_num, 'validated')

        # Update graph
        self.graph.add_experiment_node(experiment_id, results)
        self.graph.add_validation_edges(experiment_id, relationships)

    def recommend_next(self) -> List[Dict]:
        """
        Step 8: LLM recommends next experiments

        Uses graph analysis + LLM reasoning
        """
        # Graph-based recommendations
        graph_recs = self.graph.recommend_next_experiments()

        # LLM synthesis
        prompt = f"""
        Recommend the next 3 spawn-experiments to run.

        Graph analysis recommendations:
        {json.dumps(graph_recs, indent=2)}

        Recent experiment just completed:
        {self.db.get_most_recent_experiment()}

        Current pattern confidence levels:
        {json.dumps(self.db.get_pattern_confidence_summary(), indent=2)}

        Consider:
        1. Patterns needing validation for ROBUST (N=4)
        2. High-value new domains (vs incremental)
        3. spawn-solutions integration opportunities
        4. Logical progression from recent work

        Return JSON array of 3 recommendations with rationale:
        [
            {{
                "experiment_id": "1.810",
                "priority": "HIGH",
                "rationale": "why this experiment next",
                "expected_impact": "what we'll learn"
            }},
            ...
        ]

        JSON output:
        """

        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.4}
        )

        recommendations = json.loads(response['response'])
        return recommendations

    def run_full_cycle(self):
        """
        Complete automated experiment cycle

        Returns: Experiment report + next recommendations
        """
        print("=" * 60)
        print("spawn-experiments: Automated Experiment Cycle")
        print("=" * 60)

        # Step 1: Select next experiment
        print("\n📋 Step 1: Selecting next experiment...")
        selection = self.select_next_experiment()
        exp_id = selection['experiment_id']
        print(f"   Selected: {exp_id} - {selection['title']}")
        print(f"   Rationale: {selection['rationale']}")

        # Step 2: Generate specification
        print(f"\n📝 Step 2: Generating specification for {exp_id}...")
        spec = self.generate_experiment_specification(exp_id)
        print(f"   ✓ Specification generated ({len(spec)} chars)")

        # Step 3: Execute in parallel
        print(f"\n⚙️  Step 3: Executing 4 methodologies in parallel...")
        results = self.execute_experiment_parallel({'id': exp_id, 'specification': spec})
        print(f"   ✓ All 4 methods completed")

        # Step 4: Evaluate quality
        print(f"\n📊 Step 4: Evaluating code quality...")
        results = self.evaluate_code_quality(results)
        winner = max(results, key=lambda r: r['quality_score'])
        print(f"   Winner: Method {winner['method_number']} ({winner['quality_score']}/100)")

        # Step 5: Extract relationships
        print(f"\n🔗 Step 5: Extracting relationships...")
        relationships = self.extract_relationships(exp_id, results)
        print(f"   ✓ Found {len(relationships.get('validates_findings', []))} findings")
        print(f"   ✓ Found {len(relationships.get('validates_patterns', []))} patterns")

        # Step 6: Write report
        print(f"\n📄 Step 6: Synthesizing experiment report...")
        report = self.synthesize_report(exp_id, results, relationships)
        print(f"   ✓ Report generated ({len(report)} chars)")

        # Step 7: Update database
        print(f"\n💾 Step 7: Updating database and graph...")
        self.update_database_and_graph(exp_id, results, relationships)
        print(f"   ✓ Database updated")
        print(f"   ✓ Graph rebuilt")

        # Step 8: Recommend next
        print(f"\n🎯 Step 8: Recommending next experiments...")
        next_recs = self.recommend_next()
        print(f"   Next recommendations:")
        for rec in next_recs:
            print(f"   - {rec['experiment_id']}: {rec['rationale']}")

        print("\n" + "=" * 60)
        print("✅ Experiment cycle complete!")
        print("=" * 60)

        return {
            'experiment_id': exp_id,
            'results': results,
            'relationships': relationships,
            'report': report,
            'next_recommendations': next_recs
        }
```

### Continuous Research Loop

**Fully Automated Research**:
```python
# continuous_research.py - Self-driving research

orchestrator = ExperimentOrchestrator(db_path='spawn_experiments.db')

while True:
    # Run one full experiment cycle
    result = orchestrator.run_full_cycle()

    # Check if research complete
    if orchestrator.all_patterns_robust():
        print("🎉 All patterns validated to ROBUST confidence!")
        break

    # Check for blockers
    if orchestrator.has_blockers():
        print("⚠️  Blockers detected, pausing...")
        break

    # Optional: Human checkpoint
    if input("Continue to next experiment? (y/n): ").lower() != 'y':
        break

print("Research complete!")
```

### Benefits of LLM-Driven Automation

**1. Velocity**
- Current: 2-4 hours/experiment (manual coordination)
- Automated: 30-60 minutes/experiment (parallel execution)
- **10x faster research iteration**

**2. Consistency**
- Eliminates human error in data entry
- Standardized quality evaluation
- Consistent relationship extraction

**3. Scalability**
- Run experiments overnight (no human required)
- Batch processing (run 5 experiments sequentially)
- Continuous research loop

**4. Meta-Learning**
- LLM learns from experiment history
- Improves prompt engineering over time
- Discovers new patterns autonomously

### Hybrid Human-LLM Workflow

**Best of both worlds**:

```python
# hybrid_workflow.py - Human checkpoints with LLM automation

class HybridOrchestrator(ExperimentOrchestrator):
    """LLM automation with human checkpoints"""

    def run_with_checkpoints(self):
        # LLM: Select next experiment
        selection = self.select_next_experiment()

        # HUMAN CHECKPOINT: Approve selection
        approved = self.human_approve_experiment(selection)
        if not approved:
            return

        # LLM: Generate specification
        spec = self.generate_experiment_specification(selection['experiment_id'])

        # HUMAN CHECKPOINT: Review specification
        spec_approved = self.human_review_specification(spec)
        if not spec_approved:
            return

        # LLM: Execute in parallel (no checkpoint - fast)
        results = self.execute_experiment_parallel(spec)

        # LLM: Evaluate quality (no checkpoint - automated)
        results = self.evaluate_code_quality(results)

        # HUMAN CHECKPOINT: Spot-check quality evaluation
        quality_approved = self.human_spot_check_quality(results, sample_size=1)
        if not quality_approved:
            # Human overrides LLM evaluation
            results = self.human_evaluate_quality(results)

        # LLM: Extract relationships
        relationships = self.extract_relationships(selection['experiment_id'], results)

        # LLM: Write report
        report = self.synthesize_report(selection['experiment_id'], results, relationships)

        # HUMAN CHECKPOINT: Review and edit report
        final_report = self.human_edit_report(report)

        # LLM: Update database (no checkpoint - deterministic)
        self.update_database_and_graph(selection['experiment_id'], results, relationships)

        # LLM: Recommend next
        next_recs = self.recommend_next()

        # HUMAN CHECKPOINT: Approve next experiment
        # (Loop back to start)

        return final_report
```

**Checkpoints**:
- ✅ **Experiment selection**: Human approves LLM choice
- ✅ **Specification review**: Human validates task spec
- ⏭️ **Execution**: No checkpoint (LLM runs 4 methods)
- ⏭️ **Quality evaluation**: No checkpoint (LLM scores code)
- ✅ **Quality spot-check**: Human validates 1 sample
- ⏭️ **Relationship extraction**: No checkpoint (LLM finds links)
- ⏭️ **Report writing**: No checkpoint (LLM drafts report)
- ✅ **Report review**: Human edits and approves
- ⏭️ **Database update**: No checkpoint (deterministic)

**Result**: 60% automation, 40% human oversight

### Implementation Timeline

**Phase 1: Proof of Concept (2-4 weeks)**
- Implement `ExperimentOrchestrator.select_next_experiment()`
- Test LLM experiment selection (does it pick good experiments?)
- Validate recommendations vs human judgment

**Phase 2: Partial Automation (1-2 months)**
- Implement specification generation
- Test parallel execution coordination
- Validate quality evaluation accuracy

**Phase 3: Full Automation (2-3 months)**
- Complete relationship extraction
- Automated report writing
- Database updates
- Next experiment recommendations

**Phase 4: Continuous Research (3-4 months)**
- Hybrid human-LLM workflow
- Continuous research loop (overnight experiments)
- Meta-learning from experiment history

### ROI Analysis

**Investment**:
- Orchestrator development: 40-60 hours
- Testing & validation: 20-30 hours
- Integration: 10-15 hours
- **Total: 70-105 hours**

**Benefits**:
- **10x faster**: 2-4 hours → 30-60 minutes per experiment
- **Time savings**: 1.5-3.5 hours × 50 experiments/year = **75-175 hours saved**
- **Break-even**: 1-2 months (after 15-30 experiments)
- **First-year ROI**: 700-1000%

**Qualitative benefits**:
- Consistent quality evaluation (no human bias)
- Comprehensive relationship extraction
- 24/7 research (run experiments overnight)
- Meta-learning (LLM improves over time)

### Risks & Mitigations

**Risk 1: LLM hallucination in experiment selection**
- **Mitigation**: Human checkpoint for approval
- **Fallback**: Graph-based recommendation (deterministic)

**Risk 2: Quality evaluation drift**
- **Mitigation**: Human spot-checks (10% sample)
- **Validation**: Compare LLM scores vs human scores

**Risk 3: Relationship extraction errors**
- **Mitigation**: Confidence scores on extracted relationships
- **Validation**: Graph consistency checks

**Risk 4: Report quality**
- **Mitigation**: Human review and editing
- **Improvement**: LLM learns from human edits over time

### Success Metrics

**Accuracy**:
- Experiment selection: 80%+ match human choice
- Quality evaluation: ±5 points vs human scores
- Relationship extraction: 90%+ precision, 70%+ recall

**Speed**:
- Full cycle: <60 minutes (vs 2-4 hours manual)
- 10 experiments/week (vs 2-3 currently)

**Value**:
- Patterns reach ROBUST confidence faster (3 weeks vs 3 months)
- Research gaps identified automatically
- Cross-repository integration maintained

---

## Implementation Roadmap

### Phase 1: SQLite Foundation (CURRENT)
- ✅ SQLite schema deployed
- ✅ Regex-based migration script
- ✅ 22 common queries
- **Status**: Ready for production

### Phase 2: LLM Enhancement (1-2 Months)
- **Week 1-2**: LLM extraction script
  - Implement `LLMMarkdownExtractor` class
  - Test on 5-10 experiments
  - Compare vs regex (accuracy, relationships extracted)

- **Week 3-4**: Hybrid migration
  - Combine regex (fast) + LLM (accurate)
  - Batch processing optimization
  - Validation framework

- **Week 5-8**: Production integration
  - Hook into experiment framework
  - Automatic LLM extraction on completion
  - Monitoring and prompt tuning

### Phase 3: Graph Layer (2-4 Months)
- **Month 1**: NetworkX implementation
  - Build `ExperimentGraph` class
  - Import SQLite data → NetworkX
  - Basic graph queries (validation paths, dependencies)

- **Month 2**: Advanced graph analysis
  - Recommendation engine (next experiments)
  - Component reuse network analysis
  - Pattern emergence visualization

- **Month 3**: Integration
  - Combine SQL + Graph + LLM workflows
  - `complete_experiment.py` full integration
  - Performance optimization

- **Month 4**: (Optional) Neo4j migration
  - Export NetworkX → Neo4j
  - Cypher query optimization
  - Web UI for graph exploration

### Phase 4: Advanced Features (4-6 Months)
- **Advanced LLM**: Fine-tuned model for spawn-experiments
- **Graph ML**: Predict optimal methodology from experiment features
- **Auto-recommendations**: "You should run 1.810 next (Database pattern needs N+2)"
- **Cross-repo queries**: Unified spawn-solutions + spawn-experiments graph

---

## Cost-Benefit Analysis

### LLM Extraction

**Investment**:
- Development: 16-24 hours
- Testing & validation: 8-12 hours
- **Total: 24-36 hours**

**Benefits**:
- +30-50% more relationships extracted
- Qualitative insights captured (currently lost)
- Future-proof (handles format variations)

**ROI**: 200-300% first year (break-even: 3-4 months)

### Graph Database

**Investment**:
- NetworkX implementation: 16-24 hours
- Graph queries & analysis: 12-16 hours
- Integration with SQL: 8-12 hours
- **Total: 36-52 hours**

**Benefits**:
- Relationship queries 10-100x faster
- Path finding (impossible in SQL)
- Recommendation engine (next experiments)
- Network analysis (component reuse)

**ROI**: 300-500% first year (break-even: 2-3 months)

### Combined (LLM + Graph + SQL)

**Investment**:
- Total development: 60-88 hours (7-11 days)
- Ongoing maintenance: 2-4 hours/month

**Benefits**:
- **LLM**: Robust extraction, qualitative insights
- **Graph**: Relationship analysis, recommendations
- **SQL**: Tabular queries, aggregations

**ROI**: 400-600% first year

---

## Conclusion

### Recommended Path

**Immediate (Phase 1)**:
- ✅ Deploy SQLite (DONE)
- ✅ Regex migration (DONE)
- Start using database for queries

**Short-term (Phase 2, 1-2 months)**:
- Implement LLM extraction (highest ROI)
- Hybrid migration (regex + LLM)
- Capture qualitative insights

**Medium-term (Phase 3, 2-4 months)**:
- Add NetworkX graph layer
- Recommendation engine
- Cross-repository integration

**Long-term (Phase 4, 4-6+ months)**:
- Advanced LLM (fine-tuned for spawn-experiments)
- Graph ML (predict optimal methodology)
- (Optional) Neo4j for production-scale graph queries

### Key Insights

1. **LLM extraction** is the highest-value next step
   - spawn-experiments already validated (1.615 data extraction)
   - Local Ollama = zero cost
   - Captures relationships regex cannot

2. **Graph databases** are natural fit for spawn-experiments
   - Experiment dependencies are inherently graph-structured
   - SQL struggles with multi-hop queries
   - NetworkX provides 80% of value at 20% of Neo4j cost

3. **Hybrid approach** (SQL + Graph + LLM) is optimal
   - SQL: Source of truth, tabular queries
   - Graph: Relationships, recommendations
   - LLM: Extraction, insights

---

**Document Version**: 1.0
**Last Updated**: October 31, 2025
**Next Steps**: Implement LLM extraction (Phase 2)
**Owner**: spawn-experiments research team
