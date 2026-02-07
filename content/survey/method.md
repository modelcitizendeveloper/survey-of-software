---
title: "Method"
weight: 999999
description: "4PS research methodology and replication guide"
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

### What You Get

The complete methodology includes:

- **Agent prompt templates** for each methodology (S1-S4)
- **Independence protocols** (prevent cross-contamination)
- **Directory structures** for organizing research
- **Execution workflows** (parallel vs sequential)
- **Quality standards** and confidence levels
- **Step-by-step replication guide** (copy-paste prompts for Claude Code)

**Everything used to create the 135+ research pieces in this survey.**

### How to Replicate

1. **Choose your topic** (general-purpose library/tool)
2. **Run S1-S4 passes** independently (use provided prompts)
3. **Document sources** for every claim
4. **Cross-reference findings** to identify convergence/divergence
5. **Publish with methodology notes**

Full replication guide available in the internal repository.

---

## Questions or Contributions?

This is open research. If you:
- Find errors or outdated information
- Want to contribute research on new topics
- Have questions about the methodology

Open an issue: https://github.com/modelcitizendeveloper/survey-of-software/issues
