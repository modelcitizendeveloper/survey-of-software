# Discovery Table of Contents

**Research:** 1.031 Text Diff Libraries (Myers, patience diff, semantic diff)

**Status:** Complete - All 4 passes (S1-S4) + Domain Explainer

---

## How to Navigate This Research

### Quick Decision (15 minutes)
1. Read **[S1 Recommendation](S1-rapid/recommendation.md)** - Quick decision matrix
2. Scan **[DOMAIN_EXPLAINER](../DOMAIN_EXPLAINER.md)** - Understand the basics
3. Pick library, validate with small test

### Thorough Analysis (1-2 hours)
1. **[DOMAIN_EXPLAINER](../DOMAIN_EXPLAINER.md)** - Build foundational understanding
2. **[S1 Rapid Discovery](S1-rapid/)** - See what exists, quick comparison
3. **[S4 Strategic](S4-strategic/)** - Long-term viability, risk assessment
4. **[S3 Need-Driven](S3-need-driven/)** - Match to your use case
5. **[S2 Comprehensive](S2-comprehensive/)** - Deep technical dive (if needed)

### Architecture Planning
1. **[S4 Strategic](S4-strategic/)** - Risk analysis, team considerations
2. **[S3 Need-Driven](S3-need-driven/)** - Requirement mapping
3. **[S2 Comprehensive](S2-comprehensive/)** - Technical capabilities

---

## S1: Rapid Discovery

**Goal:** Quick comparison for fast decisions (5-15 minute read)

**Approach:** [approach.md](S1-rapid/approach.md)

### Library Overviews (~30-40 lines each, NO code/installation)
- [difflib](S1-rapid/difflib.md) - Python stdlib, safe default
- [diff-match-patch](S1-rapid/diff-match-patch.md) - Production diff/patch
- [GitPython](S1-rapid/GitPython.md) - Git integration, advanced algorithms
- [tree-sitter](S1-rapid/tree-sitter.md) - Code parsing, semantic diff
- [DeepDiff](S1-rapid/DeepDiff.md) - Python object comparison
- [jsondiff](S1-rapid/jsondiff.md) - JSON-specific diff
- [xmldiff](S1-rapid/xmldiff.md) - XML tree diff
- [unidiff](S1-rapid/unidiff.md) - Parse existing diffs
- [python-Levenshtein](S1-rapid/python-Levenshtein.md) - Edit distance metrics

**Decision Support:** [recommendation.md](S1-rapid/recommendation.md)

---

## S2: Comprehensive Analysis

**Goal:** Deep technical analysis (30-60 minute read)

**Approach:** [approach.md](S2-comprehensive/approach.md)

### Technical Resources
- [Feature Comparison Matrix](S2-comprehensive/feature-comparison.md) - Algorithms, formats, capabilities

**TODO (from previous session):** Individual library files with code examples, recommendation.md

---

## S3: Need-Driven Discovery

**Goal:** Map requirements to libraries through use cases (20-40 minute read)

**Approach:** [approach.md](S3-need-driven/approach.md)

### Use Cases (WHO + WHY format)
- [Testing Engineers](S3-need-driven/use-case-testing-engineers.md) - Comparing test outputs
- [Code Review Automation](S3-need-driven/use-case-code-review-automation.md) - Git integration for CI/CD
- [Data Engineers](S3-need-driven/use-case-data-engineers.md) - Comparing structured data
- [Developer Tool Creators](S3-need-driven/use-case-developer-tool-creators.md) - Semantic code analysis
- [Text Processing Apps](S3-need-driven/use-case-text-processing-apps.md) - Fuzzy matching, deduplication

**Decision Support:** [recommendation.md](S3-need-driven/recommendation.md)

---

## S4: Strategic Selection

**Goal:** Long-term viability, risk assessment (40-60 minute read)

**Approach:** [approach.md](S4-strategic/approach.md)

### Viability Analyses
- [difflib](S4-strategic/difflib-viability.md) - Stdlib baseline, zero risk
- [GitPython](S4-strategic/GitPython-viability.md) - Very active, git-dependent
- [DeepDiff](S4-strategic/DeepDiff-viability.md) - Very active, Python-focused
- [tree-sitter](S4-strategic/tree-sitter-viability.md) - Infrastructure-grade, high complexity

**Strategic Guidance:** [recommendation.md](S4-strategic/recommendation.md)

---

## Domain Explainer

**For:** Technical decision makers, product managers, architects without deep diff expertise

**[DOMAIN_EXPLAINER.md](../DOMAIN_EXPLAINER.md)** - Universal analogies, accessible explanations

Covers:
- What diff libraries solve
- When you need them
- Trade-offs (complexity, performance, capability)
- Implementation reality (timelines, skills, pitfalls)

---

## Quick Reference

### Decision Matrix

| Your Need | Primary Library | Alternative |
|-----------|----------------|-------------|
| Text/code diff | difflib | diff-match-patch |
| Git integration | GitPython | - |
| Python objects | DeepDiff | - |
| JSON | DeepDiff | jsondiff |
| XML | xmldiff | difflib |
| Semantic code | tree-sitter | GitPython (simpler) |
| Fuzzy matching | python-Levenshtein | difflib |
| Parse git diffs | unidiff | - |

### Strategic Tiers (by risk)

**Tier 1 (Minimal Risk):** difflib - Stdlib, zero dependencies

**Tier 2 (Low Risk):** DeepDiff, diff-match-patch - Stable, specialized

**Tier 3 (Medium Risk):** GitPython - Very active, git-dependent

**Tier 4 (High Capability, High Complexity):** tree-sitter - Infrastructure-grade, steep learning curve

### Common Patterns

**Testing stack:** difflib (text) + DeepDiff (objects)

**CI/CD pipeline:** GitPython (generate diffs) + unidiff (parse)

**Data validation:** DeepDiff + jsondiff (JSON) + xmldiff (XML)

**Code intelligence:** tree-sitter (semantic) + GitPython (git integration)

---

## Research Metadata

**Libraries covered:** 9 (difflib, diff-match-patch, GitPython, tree-sitter, DeepDiff, jsondiff, xmldiff, unidiff, python-Levenshtein)

**Completion status:**
- ✅ S1 Rapid Discovery (complete)
- ⚠️ S2 Comprehensive (approach + feature comparison done, individual library files TODO)
- ✅ S3 Need-Driven (complete, 5 use cases)
- ✅ S4 Strategic (complete, 4 viability analyses)
- ✅ DOMAIN_EXPLAINER (complete)

**Estimated reading time:**
- Quick decision: 15 minutes (S1 + Domain Explainer)
- Thorough analysis: 1-2 hours (all passes)
- Reference lookup: 5-10 minutes (use TOC to find specific library/use case)

---

**Navigation tip:** Use Ctrl+F (Cmd+F) to search for specific libraries, use cases, or keywords across files.
