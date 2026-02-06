---
title: "Methodology"
weight: 9999.0
---

# 4PS Research Methodology

**Four-Pass Survey (4PS)** is the research methodology used for all library, standard, and service research in this repository. This document defines the MANDATORY requirements for each pass, with particular emphasis on source documentation requirements.

---

## Core Principles

1. **Multi-pass approach**: Four distinct passes (S1-S4) building progressively deeper understanding
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
- **Title**: Descriptive link text (not just "source 1")
- **URL**: Direct link to the source
- **Access date**: When you retrieved the information (YYYY-MM-DD format)
- **Specific location** (if applicable): Commit hash, line number, section anchor

### Source Attribution Patterns

**Typical sources for library/algorithm research**:
- GitHub repositories (with commit hashes)
- Library documentation (with version numbers)
- PyPI package pages (with version/release dates)
- Academic papers (with DOI or arXiv links)
- Benchmark repositories (with specific versions)

**Example** (from 1.001 Sorting Libraries):
```markdown
## Sources

- [Python Timsort Implementation](https://github.com/python/cpython/blob/v3.12.0/Python/bltinmodule.c#L2456) - CPython 3.12.0
- [NumPy Radix Sort](https://github.com/numpy/numpy/blob/v1.26.0/numpy/core/src/multiarray/sort.c.src#L342) - NumPy 1.26.0
- [SortedContainers Documentation](https://grantjenks.com/docs/sortedcontainers/) - Accessed 2025-11-14
- [Timsort Analysis Paper](https://drops.dagstuhl.de/opus/volltexte/2018/9467/pdf/LIPIcs-ESA-2018-4.pdf) - Auger et al., 2018
```

**Note**: Code sources include specific commit hashes and line numbers for exact replicability. Time-sensitive information (like pricing or feature availability) should always include access dates.

### Enforcement: Pass Incomplete Without Sources

**A research pass is NOT considered complete until sources are documented.**

This is enforced via metadata.yaml checklist (see below).

---

## The Four Passes

### Pass S1: Rapid Discovery

**Goal**: Quick overview, identify key providers/libraries, create breadth-first map

**Time**: 2-4 hours

**Deliverables**:
- `approach.md` - Methodology for S1
- Provider/library profiles (6-8 profiles, ~300 lines each)
- `recommendations.md` - Synthesis and initial decision matrix

**Mandatory metadata.yaml checklist**:
```yaml
s1_rapid:
  status: completed
  completed_date: '2025-11-05'
  deliverables:
    - approach.md
    - provider-openai.md
    - provider-anthropic.md
    - provider-google.md
    - recommendations.md
  sources_documented:
    - Library documentation (PyPI, GitHub README) ✅
    - Official pricing pages ✅
    - Vendor homepages ✅
    - Quick-start guides ✅
  source_examples:
    - "https://openai.com/pricing - Accessed 2025-11-05"
    - "https://github.com/numpy/numpy/blob/v1.26.0/README.md"
```

**Source requirements for S1**:
- Library docs (PyPI, README files)
- Official vendor pages (homepage, pricing, getting started)
- Repository links (GitHub/GitLab)
- Quick-start tutorials

**Cannot complete S1 until**: Each profile has a `## Sources` section with at least 3-5 primary sources.

---

### Pass S2: Comprehensive Analysis

**Goal**: Deep dive into features, pricing, integrations, performance

**Time**: 1-2 days

**Deliverables**:
- `approach.md` - S2 methodology
- `feature-matrix.md` - Detailed feature comparison (50+ features)
- `pricing-tco.md` - Total cost of ownership analysis (3-year, 5-year)
- `performance-benchmarks.md` - Speed, accuracy, reliability data
- `integration-complexity.md` - SDK maturity, migration effort
- `synthesis.md` - Cross-cutting insights

**Mandatory metadata.yaml checklist**:
```yaml
s2_comprehensive:
  status: completed
  completed_date: '2025-11-05'
  deliverables:
    - approach.md
    - feature-matrix.md
    - pricing-tco.md
    - performance-benchmarks.md
    - synthesis.md
  sources_documented:
    - Detailed feature documentation ✅
    - Pricing calculators (with screenshots/calculations) ✅
    - Third-party benchmarks (with methodology) ✅
    - SDK documentation (with version) ✅
    - Case studies (with dates) ✅
  source_examples:
    - "https://docs.anthropic.com/api - Version 2024-10-01"
    - "https://artificialanalysis.ai/models - Benchmarks accessed 2025-11-05"
    - "https://aws.amazon.com/bedrock/pricing/ - Accessed 2025-11-05"
```

**Source requirements for S2**:
- Full API/feature documentation (with version numbers)
- Pricing pages + pricing calculators (with access dates)
- Third-party benchmarks (MTEB, HumanEval, Chatbot Arena) with methodology
- Case studies with publication dates
- Integration guides and SDK docs

**Cannot complete S2 until**: Each analysis document has 10-15 sources, including third-party validation sources.

---

### Pass S3: Need-Driven Scenarios

**Goal**: Real-world use case scenarios with architecture patterns and decision trees

**Time**: 1-2 days

**Deliverables**:
- `approach.md` - S3 methodology
- 5-6 scenario documents (customer-support-chatbot.md, document-analysis.md, etc.)
- `synthesis.md` - Cross-scenario patterns and insights

**Mandatory metadata.yaml checklist**:
```yaml
s3_need_driven:
  status: completed
  completed_date: '2025-11-05'
  deliverables:
    - approach.md
    - customer-support-chatbot.md
    - document-analysis.md
    - code-generation.md
    - synthesis.md
  sources_documented:
    - Architecture blogs (with dates) ✅
    - Real-world case studies (with company names) ✅
    - Implementation guides ✅
    - Performance reports (with workload specs) ✅
  source_examples:
    - "https://stripe.com/blog/how-stripe-uses-gpt-4 - Published 2024-08-12"
    - "https://docs.llamaindex.ai/en/stable/examples/chat_engine/ - Accessed 2025-11-05"
```

**Source requirements for S3**:
- Architecture blogs and engineering posts (with dates)
- Case studies from real companies (with publication dates)
- Implementation guides and best practices
- Performance reports with specific workload characteristics

**Cannot complete S3 until**: Each scenario has 5-8 sources showing real-world implementations.

---

### Pass S4: Strategic Analysis

**Goal**: Vendor viability, lock-in mitigation, 5-10 year trajectory, strategic frameworks

**Time**: 1-2 days

**Deliverables**:
- `approach.md` - S4 methodology
- `vendor-viability.md` - 5-year and 10-year survival probability
- `lock-in-mitigation.md` - Migration playbooks, abstraction strategies
- `api-compatibility.md` or `standards-analysis.md` - Standardization trends
- `trajectory.md` - Market evolution, 5-10 year outlook
- `synthesis.md` - Strategic decision frameworks

**Mandatory metadata.yaml checklist**:
```yaml
s4_strategic:
  status: completed
  completed_date: '2025-11-05'
  deliverables:
    - approach.md
    - vendor-viability.md
    - lock-in-mitigation.md
    - api-compatibility.md
    - trajectory.md
    - synthesis.md
  sources_documented:
    - Funding announcements (Crunchbase, press releases) ✅
    - Market reports (Gartner, Forrester, if public) ✅
    - Standards documentation (W3C, IETF, CNCF) ✅
    - Analyst predictions (with dates) ✅
    - Historical trends (with date ranges) ✅
  source_examples:
    - "https://www.crunchbase.com/organization/anthropic - Funding accessed 2025-11-05"
    - "https://www.w3.org/TR/json-ld11/ - JSON-LD 1.1 Specification"
    - "https://techcrunch.com/2024/06/18/anthropic-raises-450m/ - Published 2024-06-18"
```

**Source requirements for S4**:
- Funding data (Crunchbase, press releases)
- Market reports (Gartner, Forrester, or public analyst reports)
- Standards documentation (W3C, IETF, CNCF specs)
- Trend articles with timestamps
- Historical data with date ranges

**Cannot complete S4 until**: Each strategic analysis has 8-12 sources, including authoritative market/funding data.

---

## Metadata.yaml Integration

Every research piece's `metadata.yaml` must include a `sources_documented` checklist for each completed stage.

### Example metadata.yaml:

```yaml
code: '1.001'
title: Advanced Sorting Libraries
status: completed

research_output:
  stages:
    S1-rapid:
      sources_documented:
        library_docs: ✅
        github_repos: ✅
        pypi_pages: ✅
        academic_papers: ✅
      source_count: 18
      source_quality: "Primary (GitHub commits, PyPI, academic papers)"

    S2-comprehensive:
      sources_documented:
        benchmark_repos: ✅
        implementation_code: ✅
        complexity_analysis: ✅
        library_comparisons: ✅
      source_count: 31
      source_quality: "Code-level (specific commits, line numbers)"

    S3-need-driven:
      sources_documented:
        implementation_examples: ✅
        performance_data: ✅
        edge_case_docs: ✅
      source_count: 24
      source_quality: "Implementation-focused (code examples, benchmarks)"

    S4-strategic:
      sources_documented:
        historical_papers: ✅
        hardware_evolution: ✅
        future_research: ✅
        sustainability_analysis: ✅
      source_count: 29
      source_quality: "Historical + predictive (papers, hardware trends)"
```

---

## Source Quality Standards

Not all sources are equal. Prioritize in this order:

### Tier 1: Primary Authoritative Sources
- Official vendor documentation
- Official pricing pages
- GitHub repositories (with commit hashes)
- W3C/IETF/CNCF specifications
- Academic papers (peer-reviewed, with DOI)
- Official blog announcements

### Tier 2: Verified Third-Party Sources
- Established benchmarks (MTEB, HumanEval, Chatbot Arena)
- Crunchbase funding data
- Published case studies (company engineering blogs)
- Market analysts (Gartner, Forrester - if publicly available)

### Tier 3: Community Sources (use sparingly)
- Stack Overflow (for implementation patterns)
- Reddit/HN discussions (for sentiment, not facts)
- Personal blogs (only if no better source exists)

**Rule**: Every factual claim must have a Tier 1 or Tier 2 source. Tier 3 sources can supplement but never replace authoritative sources.

---

## Common Source Documentation Mistakes

### ❌ Bad Example 1: No sources
```markdown
OpenAI charges $30/M for GPT-4. It's expensive.
```
**Problem**: No source to verify the claim or access date.

### ✅ Good Example 1: Sourced claim
```markdown
OpenAI charges $30/M input for GPT-4 ([source](https://openai.com/pricing) - Accessed 2025-11-05). This is 4× more expensive than Claude 3.5 Sonnet at $3/M ([source](https://www.anthropic.com/pricing) - Accessed 2025-11-05).
```

---

### ❌ Bad Example 2: Generic "documentation" reference
```markdown
According to the documentation, NumPy uses radix sort for integers.
```
**Problem**: Which documentation? Which version? Where in the docs?

### ✅ Good Example 2: Specific source
```markdown
NumPy uses radix sort for integer arrays when `kind='stable'` is specified ([source](https://github.com/numpy/numpy/blob/v1.26.0/numpy/core/src/multiarray/sort.c.src#L342) - NumPy 1.26.0, lines 342-387).
```

---

### ❌ Bad Example 3: Undated pricing claim
```markdown
Gemini Flash costs $0.0375/M tokens.
```
**Problem**: Pricing changes. Without a date, this claim is unverifiable.

### ✅ Good Example 3: Timestamped pricing
```markdown
Gemini Flash costs $0.0375/M input tokens ([source](https://ai.google.dev/pricing) - Accessed 2025-11-05). This makes it 7× cheaper than Claude Haiku ($0.25/M) at the time of research.
```

---

### ❌ Bad Example 4: Sources section without access dates
```markdown
## Sources
- https://openai.com/pricing
- https://docs.anthropic.com
```
**Problem**: No access dates, no descriptive titles, no context.

### ✅ Good Example 4: Proper sources section
```markdown
## Sources

- [OpenAI Pricing](https://openai.com/pricing) - Accessed 2025-11-05
- [Claude API Documentation](https://docs.anthropic.com/api) - Version 2024-10-01, Accessed 2025-11-05
- [Gemini Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits) - Accessed 2025-11-05
```

---

## Enforcement and Validation

### Pre-commit Checklist

Before marking a stage as `completed` in metadata.yaml:

1. ✅ Every markdown file has a `## Sources` section
2. ✅ Every claim with a number (pricing, performance, features) has a source
3. ✅ Every source includes an access date or version number
4. ✅ Tier 1 (primary) sources used for all factual claims
5. ✅ metadata.yaml includes `sources_documented` checklist with ✅ marks

### Review Checklist

When reviewing research:

1. Open 3 random sources from each stage - do they load?
2. Pick 3 specific claims (pricing, features, benchmarks) - can you find them in the sources?
3. Check access dates - are they within the research date range?
4. Verify Tier 1/2 sources used for critical claims

---

## Why This Matters: Real-World Example

### Scenario: 6 months after research completion

**User question**: "You said Claude was $3/M. Now it's $5/M. Was your research wrong?"

**Without sources**:
- ❌ Cannot prove what pricing was at time of research
- ❌ Cannot show when pricing changed
- ❌ Research credibility damaged

**With proper sources**:
- ✅ "Research was conducted 2025-11-05. Source: [Claude Pricing](https://www.anthropic.com/pricing) - Accessed 2025-11-05 showed $3/M"
- ✅ "Pricing increased between 2025-11-05 and 2026-05-01"
- ✅ Research remains credible - we documented what was true THEN
- ✅ User knows to check for updates

**This is why timestamps matter.**

---

## Template for New Research

When starting a new research experiment, create this file structure:

```
research/X.XXX-experiment-name/
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

## Summary: The Golden Rule

> **A research pass is NOT complete until sources are documented.**

- Every factual claim needs a source
- Every source needs an access date or version
- Every stage needs a sources_documented checklist in metadata.yaml
- Replicability is not optional - it's the foundation of credible research

**If you can't cite it, you can't claim it.**

---

## Appendix: Source Documentation Tools

### Recommended Tools

**Browser extensions**:
- Wayback Machine extension - Capture page snapshots
- Link Archiver - Auto-save accessed URLs

**Documentation helpers**:
- `wget --mirror --page-requisites URL` - Archive entire doc sites
- Screenshot tool (Flameshot, macOS Screenshot) - Capture pricing pages
- Git commit hash finder - For linking to specific code versions

**Markdown formatters**:
```bash
# Quick source link generator
echo "- [Title](URL) - Accessed $(date +%Y-%m-%d)"
```

### Source Archival Best Practices

For critical sources (pricing, features that may change):

1. **Take screenshots**: Pricing pages, feature matrices
2. **Archive URLs**: Use Wayback Machine for important claims
3. **Save PDFs**: Technical whitepapers, case studies
4. **Git commit references**: Always use commit hashes, not branch names

**Store these in** `research/X.XXX-experiment-name/sources/` directory for future verification.

---

**Version**: 1.0
**Last Updated**: 2026-01-30
**Authority**: This methodology is MANDATORY for all research in this repository
