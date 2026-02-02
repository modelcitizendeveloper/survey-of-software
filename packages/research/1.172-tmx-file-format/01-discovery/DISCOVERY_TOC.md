# 1.172 TMX File Format Libraries - Discovery Phase

Complete 4PS research on Python libraries for TMX (Translation Memory eXchange) file format.

## Research Scope

**TMX Format**: XML-based standard for translation memory exchange between CAT (Computer-Aided Translation) tools. Contains source/target language pairs with metadata for translation reuse.

**Libraries Researched**:
- translate-toolkit (production-ready, multi-format)
- hypomnema (modern, TMX-focused, MIT license)
- polib (gettext library with TMX conversion support)

**Critical Name Collision**: "TMX" also refers to Tiled Map XML format (game development). This research covers Translation Memory eXchange ONLY.

## Navigation Guide

### S1: Rapid Discovery (15-20 min read)
**When to use**: Quick library selection, initial comparison

- [approach.md](S1-rapid/approach.md) - Research methodology, library identification, name collision warning
- [translate-toolkit.md](S1-rapid/translate-toolkit.md) - Production-ready, GPL-2.0+, TMX Level 1, 933 stars
- [hypomnema.md](S1-rapid/hypomnema.md) - Modern, MIT, TMX Level 2, pre-1.0, streaming API
- [polib.md](S1-rapid/polib.md) - Mature PO/POT/MO library, indirect TMX support
- [recommendation.md](S1-rapid/recommendation.md) - Quick decision guide, comparison table

**Key output**: Decision tree, quick comparison, default recommendations

### S2: Comprehensive Analysis (45-60 min read)
**When to use**: Deep technical understanding, performance requirements

- [approach.md](S2-comprehensive/approach.md) - Technical analysis methodology
- [translate-toolkit.md](S2-comprehensive/translate-toolkit.md) - Architecture, lxml DOM, 2-4 KB/unit memory, ~5 sec/100K units
- [hypomnema.md](S2-comprehensive/hypomnema.md) - Dataclass-based, 1.5-2 KB/unit, ~2 sec/100K units, streaming API
- [polib.md](S2-comprehensive/polib.md) - Pure Python, ~1 KB/unit, zero dependencies, PO-centric
- [feature-comparison.md](S2-comprehensive/feature-comparison.md) - Detailed feature matrix, performance metrics
- [recommendation.md](S2-comprehensive/recommendation.md) - Technical selection criteria, trade-off analysis

**Key output**: Performance characteristics, memory usage, API design patterns, risk assessment

### S3: Need-Driven Discovery (30-45 min read)
**When to use**: Match library to specific use case or persona

- [approach.md](S3-need-driven/approach.md) - Persona-driven selection methodology
- [use-case-freelance-translators.md](S3-need-driven/use-case-freelance-translators.md) - Personal TM management, simple workflows
- [use-case-localization-agencies.md](S3-need-driven/use-case-localization-agencies.md) - Multi-client LSPs, large-scale CAT integration
- [use-case-nlp-researchers.md](S3-need-driven/use-case-nlp-researchers.md) - Parallel corpus extraction, ML training data
- [use-case-enterprise-localization.md](S3-need-driven/use-case-enterprise-localization.md) - CI/CD pipelines, continuous localization
- [use-case-cat-tool-developers.md](S3-need-driven/use-case-cat-tool-developers.md) - Commercial translation software development
- [recommendation.md](S3-need-driven/recommendation.md) - Requirement-driven selection guide

**Key output**: WHO needs what, WHY choose library X for scenario Y

### S4: Strategic Selection (25-35 min read)
**When to use**: Long-term architectural decisions, 5-year planning

- [approach.md](S4-strategic/approach.md) - Strategic assessment framework, 5-pillar methodology
- [translate-toolkit-viability.md](S4-strategic/translate-toolkit-viability.md) - 15+ year history, Translate House backing, B+ rating, maintenance mode likely
- [hypomnema-viability.md](S4-strategic/hypomnema-viability.md) - Pre-1.0 risk/reward, single-maintainer, C+ to A- potential
- [polib-viability.md](S4-strategic/polib-viability.md) - Mature legacy, Django/Flask integration, A- for PO, D for TMX
- [recommendation.md](S4-strategic/recommendation.md) - 5-year outlook, ecosystem trends, migration paths

**Key output**: Maintenance sustainability, ecosystem momentum, strategic risk assessment

## Quick Start Paths

### Path 1: Rapid Decision (15 min)
1. Read S1/recommendation.md
2. Check S4/recommendation.md for strategic red flags
3. Pick library and validate with sample TMX files

**Result**: Fast selection with confidence

### Path 2: Informed Decision (60 min)
1. Read S1/approach.md + recommendation.md
2. Find matching persona in S3
3. Verify technical requirements in S2/feature-comparison.md
4. Review S4 strategic considerations

**Result**: Well-validated selection

### Path 3: Architecture Planning (90 min)
1. Read DOMAIN_EXPLAINER.md (if new to TMX)
2. Study S4 strategic analysis
3. Map requirements using S3 use cases
4. Deep-dive S2 for top 2 candidates
5. Validate with S1 quick comparison

**Result**: Strategic library selection with long-term considerations

## Key Findings Summary

### Library Ecosystem
- **Small ecosystem**: Only 2-3 libraries for TMX translation memory in Python
- **Name collision**: "tmxlib" is for game tile maps (NOT translation memory)
- **Active development**: translate-toolkit (monthly releases), hypomnema (pre-1.0)

### Library Comparison

| Library | Status | License | TMX Level | Stars | Best For |
|---------|--------|---------|-----------|-------|----------|
| translate-toolkit | Production | GPL-2.0+ | Level 1 | 933 | Multi-format pipelines |
| hypomnema | Pre-1.0 | MIT | Level 2 | 8 | TMX-only, commercial use |
| polib | Mature | MIT | Via conversion | N/A | PO workflows + TMX export |

### Default Recommendations

**For most projects**: translate-toolkit (production-ready, comprehensive)

**For specific needs**:
- TMX Level 2 required → hypomnema (only option)
- Commercial software → hypomnema or polib (MIT license)
- PO-based workflow → polib + translate-toolkit for conversion
- NLP/ML pipelines → hypomnema (streaming API)
- Python <3.11 → polib only

### Critical Decision Factors

1. **TMX Level**: Level 1 (basic) vs Level 2 (nested inline markup)
2. **Licensing**: GPL vs MIT for commercial use
3. **Maturity**: Production-stable vs pre-1.0 risk
4. **Format focus**: TMX-only vs multi-format ecosystem
5. **File size**: In-memory vs streaming for large corpora

## Domain Context

See [DOMAIN_EXPLAINER.md](../DOMAIN_EXPLAINER.md) for:
- What is TMX and translation memory?
- How CAT tools use TMX files
- When you need TMX libraries vs end-user tools
- Trade-offs in translation memory automation

## Research Metadata

**Research Date**: January 2026
**Python Version**: 3.11-3.13 (library-dependent)
**TMX Spec**: TMX 1.4b (GALA standard)

**Library Versions Analyzed**:
- translate-toolkit: 3.18.1 (Jan 2026)
- hypomnema: Pre-1.0 (active development)
- polib: 1.2.0 (Feb 2023)

**Estimated Decay**:
- S1/S2: 70-80% accurate at publication, 50-70% at 12 months
- S3: 75-85% accurate (use cases change slower than implementations)
- S4: 60-70% accurate (strategic predictions inherently uncertain)

## Next Steps

1. **Select library** using appropriate pass (S1 for speed, S2 for depth, S3 for use case, S4 for strategy)
2. **Validate selection** with representative TMX files from your workflow
3. **Verify licensing** compatibility with your project
4. **Test integration** with existing CAT tools or pipelines
5. **Benchmark performance** with actual file sizes

## References

- TMX 1.4b Specification: https://www.gala-global.org/tmx-14b
- translate-toolkit: https://github.com/translate/translate
- hypomnema: https://github.com/EnzoAgosta/hypomnema
- polib: https://github.com/izimobil/polib
