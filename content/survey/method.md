---
description: 4PS research methodology and replication guide
title: Method
weight: 9997000
---

# Research Method

> **Systematic library research is replicable.** The methodology behind every research piece is open, documented, and ready for you to apply to your own challenges.

---

## Why Open the Methodology?

**Open source tools are available to everyone now.** The vision is to help organizations DIY solutions they would have paid vendors for before. This research—and the methodology behind it—accelerates that.

**If the research helps you, the methodology can help you research what *you* need.**

---

## The Four-Pass Survey (4PS)

**Four-Pass Survey (4PS)** is the research methodology used for all library, standard, and service research in this repository. Four distinct passes (S1-S4) build progressively deeper understanding using independent discovery methodologies that explore solution spaces from different angles.

### S1: Rapid Discovery
**Philosophy:** "Popular libraries exist for a reason"

Speed-focused, ecosystem-driven. GitHub stars, download counts, community adoption. Get 70% of the value in 10 minutes.

**Confidence:** 70-80% (speed-optimized)

### S2: Comprehensive Analysis
**Philosophy:** "Understand the entire solution space before choosing"

Performance benchmarks, feature matrices, deep trade-off analysis. Know everything before committing.

**Confidence:** 80-90% (depth-optimized)

### S3: Need-Driven Discovery
**Philosophy:** "Start with requirements, find exact-fit solutions"

Use case mapping, requirement validation. Does this actually solve your specific problem?

**Confidence:** 75-85% (context-specific)

### S4: Strategic Selection
**Philosophy:** "Think long-term and consider broader context"

Maintenance health, vendor risk, ecosystem momentum. Will this survive for years?

**Confidence:** 60-70% (forward-looking)

---

## Why Four Approaches?

**Different methodologies reveal different optimal solutions.** Single-methodology discovery misses potentially better paths.

- S1 finds what works fast
- S2 finds what optimizes best
- S3 finds what fits requirements exactly
- S4 finds what survives long-term

**The convergence pattern:** When 3-4 methodologies agree, that's a strong signal. When they disagree, you've discovered a trade-off worth understanding.

---

## Core Principles

1. **Multi-pass approach**: Four distinct passes building progressively deeper understanding
2. **Hardware store model**: Create generic catalogs, not client-specific recommendations
3. **Source documentation is MANDATORY**: Every claim must be attributable to a verifiable source
4. **Replicability**: Another researcher must be able to verify every finding using documented sources

---

## Source Documentation (REQUIRED)

### Why Source Documentation is Mandatory

**Replicability = Academic Credibility**

Research without sources is opinion. Research with sources is evidence.

- **For verification**: Readers can validate claims independently
- **For updates**: When pricing/features change, sources show what to re-check
- **For credibility**: Timestamped sources prove claims were accurate at time of research
- **For learning**: Sources are the raw material for future researchers
- **For accountability**: Sources distinguish research from speculation

**Critical for time-sensitive data**: Pricing and feature availability change constantly. A source with a timestamp proves "this was true on DATE" even if it's outdated today.

### Source Documentation Format

Every research document MUST include a `## Sources` section at the end, formatted as:

```markdown
## Sources

- [OpenAI Pricing](https://openai.com/pricing) - Accessed 2025-11-05
- [Claude API Documentation](https://docs.anthropic.com/api) - Accessed 2025-11-05
- [Gemini Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits) - Accessed 2025-11-05
- [NumPy Radix Sort Implementation](https://github.com/numpy/numpy/blob/v1.26.0/numpy/core/src/multiarray/sort.c.src#L342) - Specific commit/line
```

**Required elements**:
1. Descriptive link text
2. Full URL
3. Access date (for time-sensitive info like pricing)
4. Specific commit/line for code references

**What counts as a source:**
- ✅ Official documentation
- ✅ Academic papers with DOI
- ✅ GitHub repos/issues (with commit hash when referencing code)
- ✅ Blog posts from library authors
- ✅ Benchmark reports with methodology
- ❌ "Common knowledge" (cite a tutorial or docs instead)
- ❌ Your own experience without external validation
- ❌ Secondary sources without checking primary

---

## When to Use 4PS

**The hardware store principle:** This methodology works for general-purpose libraries, tools, and infrastructure—not application-specific solutions.

**Good candidates:**
- Algorithm libraries (sorting, graph algorithms, compression)
- Data processing tools (JSON, serialization, streaming)
- ML frameworks (PyTorch, TensorFlow, ONNX)
- Infrastructure components (caching, logging, testing)
- Development tools (linters, formatters, bundlers)

**Poor candidates:**
- Vertical SaaS products
- Highly specialized domain solutions
- One-off utilities
- Application frameworks requiring deep integration

---

## Confidence Levels & Information Decay

This research provides **strategic direction**, not Consumer Reports certainty:

**At publication:** 70-80% accuracy
**After 12 months:** 50-70% accuracy
**After 36 months:** <30% accuracy

Library ecosystems evolve. Treat research as living documents that guide investigation, not gospel truth.

---

## Replicating This Research

### The Four Passes: Detailed Requirements

#### Pass S1: Rapid Discovery

**Goal**: Quick overview, identify key providers/libraries, create breadth-first map

**Time**: 2-4 hours

**Deliverables**:
- `approach.md` - Methodology for S1
- Provider/library profiles (6-8 profiles, ~300 lines each)
- `recommendations.md` - Synthesis and initial decision matrix

**Source requirements for S1**:
- Library docs (PyPI, README files)
- Official vendor pages (homepage, pricing, getting started)
- Repository links (GitHub/GitLab)
- Quick-start tutorials

**Cannot complete S1 until**: Each profile has a `## Sources` section with at least 3-5 primary sources.

---

#### Pass S2: Comprehensive Analysis

**Goal**: Deep dive into features, pricing, integrations, performance

**Time**: 1-2 days

**Deliverables**:
- `approach.md` - S2 methodology
- `feature-matrix.md` - Detailed feature comparison (50+ features)
- `pricing-tco.md` - Total cost of ownership analysis (3-year, 5-year)
- `performance-benchmarks.md` - Speed, accuracy, reliability data
- `integration-complexity.md` - SDK maturity, migration effort
- `synthesis.md` - Cross-cutting insights

**Source requirements for S2**:
- Full API/feature documentation (with version numbers)
- Pricing pages + pricing calculators (with access dates)
- Third-party benchmarks (MTEB, HumanEval, Chatbot Arena) with methodology
- Case studies with publication dates
- Integration guides and SDK docs

**Cannot complete S2 until**: Each analysis document has 10-15 sources, including third-party validation sources.

---

#### Pass S3: Need-Driven Scenarios

**Goal**: Real-world use case scenarios with architecture patterns and decision trees

**Time**: 1-2 days

**Deliverables**:
- `approach.md` - S3 methodology
- 5-6 scenario documents (customer-support-chatbot.md, document-analysis.md, etc.)
- `synthesis.md` - Cross-scenario patterns and insights

**Source requirements for S3**:
- Architecture blogs with implementation details
- GitHub examples with commit hashes
- Case studies from company engineering blogs
- Stack Overflow for implementation patterns (supplementary only)

---

#### Pass S4: Strategic Selection

**Goal**: Long-term viability analysis, vendor risk assessment, ecosystem health

**Time**: 1-2 days

**Deliverables**:
- `approach.md` - S4 methodology
- `vendor-viability.md` - Funding, acquisition risk, company health
- `ecosystem-momentum.md` - Community activity, fork potential, standards alignment
- `synthesis.md` - Strategic recommendations

**Source requirements for S4**:
- GitHub activity metrics (commits, issues, contributors)
- Funding data (Crunchbase, company announcements)
- Company blogs and roadmaps
- Community forums and discussion trends

---

### Template for New Research

When starting a new research topic, create this file structure:

```
research/X.XXX-topic-name/
├── metadata.yaml                    # Include sources_documented checklist
├── 01-discovery/
│   ├── S1-rapid/
│   │   ├── approach.md              # Must end with ## Sources
│   │   ├── provider-1.md            # Must end with ## Sources
│   │   ├── provider-2.md            # Must end with ## Sources
│   │   └── recommendations.md       # Must end with ## Sources
│   ├── S2-comprehensive/
│   │   ├── approach.md              # Must end with ## Sources
│   │   ├── feature-matrix.md        # Must end with ## Sources
│   │   ├── pricing-tco.md           # Must end with ## Sources
│   │   └── synthesis.md             # Must end with ## Sources
│   ├── S3-need-driven/
│   │   ├── approach.md              # Must end with ## Sources
│   │   ├── scenario-1.md            # Must end with ## Sources
│   │   └── synthesis.md             # Must end with ## Sources
│   └── S4-strategic/
│       ├── approach.md              # Must end with ## Sources
│       ├── vendor-viability.md      # Must end with ## Sources
│       └── synthesis.md             # Must end with ## Sources
```

**Every `.md` file must end with `## Sources` section.**

---

### Source Documentation Best Practices

**Common mistakes to avoid**:

❌ **Bad**: "OpenAI charges $30/M for GPT-4. It's expensive."
- Problem: No source, no date

✅ **Good**: "OpenAI charges $30/M input for GPT-4 ([source](https://openai.com/pricing) - Accessed 2025-11-05). This is 4× more expensive than Claude 3.5 Sonnet at $3/M ([source](https://www.anthropic.com/pricing) - Accessed 2025-11-05)."

---

❌ **Bad**: "According to the documentation, NumPy uses radix sort for integers."
- Problem: Which docs? Which version? Where?

✅ **Good**: "NumPy uses radix sort for integer arrays when `kind='stable'` is specified ([source](https://github.com/numpy/numpy/blob/v1.26.0/numpy/core/src/multiarray/sort.c.src#L342) - NumPy 1.26.0, lines 342-387)."

---

### Enforcement: Pre-Commit Checklist

Before marking a stage as complete:

1. ✅ Every markdown file has a `## Sources` section
2. ✅ Every claim with a number (pricing, performance, features) has a source
3. ✅ Every source includes an access date or version number
4. ✅ Primary sources used for all factual claims
5. ✅ File structure matches template

**Rule**: A research pass is NOT complete until sources are documented.

---

### Source Tiers

**Tier 1: Primary Sources (REQUIRED)**
- Official documentation (with version)
- Library source code (with commit hash)
- Vendor pricing pages (with access date)
- Academic papers (with DOI)

**Tier 2: Verified Third-Party Sources**
- Established benchmarks (MTEB, HumanEval, Chatbot Arena)
- Published case studies (company engineering blogs)
- Market analysts (Gartner, Forrester - if publicly available)

**Tier 3: Community Sources (use sparingly)**
- Stack Overflow (for implementation patterns)
- Reddit/HN discussions (for sentiment, not facts)
- Personal blogs (only if no better source exists)

**Rule**: Every factual claim must have a Tier 1 or Tier 2 source.

---

### How to Replicate

**Step-by-step**:

1. **Choose your topic** (general-purpose library/tool)
2. **Create directory structure** (use template above)
3. **Run S1-S4 passes** independently
   - Each pass uses different discovery methodology
   - Document sources as you work (not at the end)
4. **Cross-reference findings** to identify convergence/divergence
5. **Validate completeness** (pre-commit checklist)
6. **Publish with methodology notes**

**Time commitment**:
- S1: 2-4 hours
- S2: 1-2 days
- S3: 1-2 days
- S4: 1-2 days
- **Total**: ~1 week for complete coverage

**You can stop after any pass** - S1 alone gives 70% of the value. Deeper passes add precision and confidence.

---

## Questions or Contributions?

This is open research. If you:
- Find errors or outdated information
- Want to contribute research on new topics
- Have questions about the methodology

Open an issue: https://github.com/modelcitizendeveloper/survey-of-software/issues
