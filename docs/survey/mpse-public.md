---
sidebar_position: 101
slug: /survey/methodology
id: four-pass-solution-survey
title: "Methodology"
---

# Four-Pass Discovery (4PS)

**Systematic Library Research Using Four Independent Perspectives**

> A replicable methodology for discovering and evaluating general-purpose software libraries. Four independent agents explore the same problem space using different approaches, revealing optimal solutions through convergence analysis.

---

## Framework Purpose

This framework provides a systematic approach to library discovery that reveals the solution space from multiple angles. Different discovery methodologies uncover different optimal solutions—single-methodology discovery misses potentially better paths.

**Core Principle:** Four independent agents explore the same problem space using different approaches, then we analyze where they converge (strong signal) and diverge (reveals trade-offs).

**Use Cases:**
- Algorithm libraries (sorting, graph algorithms, compression)
- Data processing tools (JSON parsing, serialization, streaming)
- ML frameworks (PyTorch, TensorFlow, ONNX)
- Infrastructure libraries (caching, logging, testing)

---

## The Four Methodologies

### S1: Rapid Discovery
**Philosophy:** "Popular libraries exist for a reason"

**Approach:**
- Speed-focused, ecosystem-driven discovery
- GitHub stars, download counts, community adoption
- Quick validation: "does it work?"
- 5-10 minute landscape scan

**Discovery Tools:**
- GitHub trending, awesome-lists
- Package registries (PyPI, npm, Maven)
- Stack Overflow mentions
- Reddit/HN discussions

**Selection Criteria:**
- Popularity (stars, downloads)
- Recent activity (commits in last 6 months)
- Active maintenance
- Clear documentation

**Output:**
- Top 3-5 libraries
- Quick pros/cons per library
- Recommendation with confidence level

---

### S2: Comprehensive Analysis
**Philosophy:** "Understand the entire solution space before choosing"

**Approach:**
- Thorough, evidence-based, optimization-focused
- Performance benchmarks, feature matrices
- Deep trade-off analysis
- 30-60 minute deep dive

**Discovery Tools:**
- Benchmark suites (pytest-benchmark, JMH)
- Feature comparison matrices
- Architecture analysis
- Dependency trees

**Selection Criteria:**
- Performance (speed, memory, throughput)
- Feature completeness
- API design quality
- Ecosystem integration

**Output:**
- Complete solution space map
- Benchmark results
- Feature comparison matrix
- Trade-off analysis
- Optimized recommendation

---

### S3: Need-Driven Discovery
**Philosophy:** "Start with requirements, find exact-fit solutions"

**Approach:**
- Requirement-focused, validation-oriented
- Use case mapping
- Gap analysis
- "Does this solve my specific problem?"

**Discovery Tools:**
- Requirement checklists
- Use case scenarios
- Validation testing
- Edge case exploration

**Selection Criteria:**
- Requirement satisfaction (must-haves met?)
- Use case fit (solves actual problem?)
- Constraints respected (licensing, dependencies)
- Implementation complexity

**Output:**
- Requirement mapping per library
- Use case validation results
- Gap analysis
- Best-fit recommendation

---

### S4: Strategic Selection
**Philosophy:** "Think long-term and consider broader context"

**Approach:**
- Future-focused, ecosystem-aware
- Maintenance health, long-term viability
- Community sustainability
- 5-10 year outlook

**Discovery Tools:**
- Commit history analysis
- Maintainer health (bus factor)
- Issue resolution speed
- Breaking change frequency

**Selection Criteria:**
- Maintenance activity (not abandoned)
- Community health (contributors, responsiveness)
- Stability (semver compliance, breaking changes)
- Ecosystem momentum (growing vs declining)

**Output:**
- Long-term viability assessment
- Maintenance health scores
- Ecosystem trajectory
- Strategic recommendation

---

## Methodology Independence Protocol

**Critical Requirements:**

Each methodology agent MUST:
1. **Complete Independence**: NO ACCESS to other methodology analyses
2. **Method Purity**: Apply ONLY your methodology's approach
3. **No Cross-References**: Do NOT coordinate with other agents
4. **Authentic Application**: Stay true to methodology philosophy
5. **Workspace Isolation**: Write only to your designated directory

**Why Independence Matters:**

Contamination destroys the value of multi-methodology discovery. If S3 reads S2's analysis, you lose the distinct perspective that makes S3 valuable.

---

## Directory Structure

```
research/1.XXX-library-name/
├── LIBRARY_EXPLAINER.md              # Technical concepts
└── 01-discovery/
    ├── S1-rapid/
    │   ├── approach.md              # Methodology (50-100 lines)
    │   ├── library-X.md             # Per-library assessment
    │   └── recommendation.md        # Final choice (50-100 lines)
    ├── S2-comprehensive/
    │   ├── approach.md
    │   ├── library-X.md             # Per-library deep analysis
    │   ├── feature-comparison.md    # Matrix across libraries
    │   └── recommendation.md
    ├── S3-need-driven/
    │   ├── approach.md
    │   ├── use-case-X.md            # Per use case analysis
    │   └── recommendation.md
    ├── S4-strategic/
    │   ├── approach.md
    │   ├── library-X-maturity.md    # Per-library viability
    │   └── recommendation.md
    └── DISCOVERY_TOC.md             # Index + quick summaries
```

**Modular Design:** Each library gets its own file, enabling cross-research reuse.

---

## Execution Protocol

### Parallel Execution (Recommended)

**Launch all 4 methodologies simultaneously:**

```python
# Launch S1, S2, S3, S4 in parallel (single message, multiple tasks)
# Each writes to separate directory
# No coordination, complete independence
# 60-90 minutes total vs 3-4 hours sequential
```

**Benefits:**
- Maximum throughput (2-3× faster)
- Guaranteed independence (no cross-contamination)
- Minimal human intervention

### Post-Execution Workflow

1. **File Validation**: Ensure all 4 directories created
2. **Independence Verification**: Check approaches stayed pure
3. **TOC Generation**: Create DISCOVERY_TOC.md (5-10 minutes)
   - Reads S1-S4 recommendation.md files
   - Creates index with summaries
   - Notes convergence patterns
4. **Explainer Creation** (optional): Technical concepts document

---

## Convergence Analysis

### Recommendation Mapping

| Method | Primary Rec | Confidence | Key Rationale |
|--------|-------------|------------|---------------|
| S1     | Library A   | High       | Most popular  |
| S2     | Library A   | High       | Best performance |
| S3     | Library B   | Medium     | Better fit for use case X |
| S4     | Library A   | High       | Active maintenance |

### Convergence Patterns

- **High Convergence** (3-4 methods agree): Strong signal
- **Medium Convergence** (2 methods agree): Context-dependent
- **Low Convergence** (all different): Complex trade-offs
- **Polarized Disagreement**: Fundamental approach differences

**Example:**
- If S1, S2, S4 all choose orjson: Strong confidence
- If S3 chooses msgspec: Performance vs ease-of-use trade-off revealed

---

## Quality Standards

### Research-Grade Confidence

- **S1 Rapid:** 70-80% confidence (speed-optimized)
- **S2 Comprehensive:** 80-90% confidence (depth-optimized)
- **S3 Need-Driven:** 75-85% confidence (context-specific)
- **S4 Strategic:** 60-70% confidence (forward-looking)

**Not Consumer Reports 95%+ certainty.** This provides **strategic direction**, not guarantees.

### Information Decay

Library ecosystems evolve:
- **At publication:** 70-80% accuracy
- **12 months:** 50-70% accuracy
- **36 months:** &lt;30% accuracy

Treat research as living documents that guide investigation, not gospel truth.

### Data Sources (Safe for Open Source)

**Always Safe:**
- Official documentation
- Public repository data (GitHub stars, issues, commits)
- Package registry stats (PyPI downloads, npm downloads)
- Your own benchmarks
- Academic papers with proper citation
- Public GitHub issues/discussions

**Attribution:** Document sources in research for transparency.

---

## Methodology Prompt Templates

### Base Template Structure

```
You are applying the [METHOD_NAME] discovery methodology in complete isolation.

DISCOVERY CHALLENGE: [Problem statement]

METHODOLOGY INDEPENDENCE REQUIREMENTS:
- You have NO ACCESS to other methodology analyses
- Do NOT reference other discovery methods
- Focus solely on YOUR methodology's approach
- Make independent recommendations

YOUR METHODOLOGY: [S1/S2/S3/S4]
[Method-specific philosophy and tools]

WORKSPACE: research/1.XXX-library/01-discovery/[METHOD]/

DELIVERABLE: Create the following files:
- approach.md: Your methodology and discovery process
- library-X.md: Per-library analysis
- recommendation.md: Final choice with confidence level

CRITICAL: Stay authentic to your methodology.
```

---

## Example: JSON Library Research

**S1 Rapid Discovery** finds:
- `orjson` (most popular, fastest)
- `ujson` (legacy, maintenance mode)
- `simplejson` (pure Python, portable)

**S2 Comprehensive** benchmarks:
- `orjson` 3× faster than stdlib
- Memory profiles
- Feature completeness matrix
- Recommends `orjson` for performance

**S3 Need-Driven** validates:
- Use case: API serialization → `orjson`
- Use case: Config files → stdlib (simple, portable)
- Use case: Complex schema → `pydantic` + stdlib

**S4 Strategic** assesses:
- `orjson`: Active maintenance, growing
- `ujson`: Declining, avoid for new projects
- stdlib: Safe long-term, slow updates

**Convergence:** 3/4 recommend `orjson` for performance-critical work, but S3 reveals context matters.

---

## When to Use 4PS

**Good Candidates:**
- General-purpose libraries
- Algorithm implementations
- Data processing tools
- Infrastructure components
- Development frameworks

**Not a Fit:**
- Application-specific solutions
- Proprietary business tools
- Vertical-specific software

**The Hardware Store Principle:** 4PS works for components you'd find in a hardware store—general-purpose tools, not custom applications.

---

## Applying This Framework

1. **Identify your library category** (sorting, JSON, ML, etc.)
2. **Start with S1** rapid discovery (70% of value in 10 minutes)
3. **Deepen with S2-S4** as needed
4. **Analyze convergence** patterns across methodologies
5. **Document your findings** using the directory structure

**Remember:** Different methodologies reveal different optimal solutions. Single-methodology discovery misses potentially better paths.

---

**Four-Pass Survey (4PS)** - Systematic, replicable, open methodology for evaluating general-purpose software libraries.
