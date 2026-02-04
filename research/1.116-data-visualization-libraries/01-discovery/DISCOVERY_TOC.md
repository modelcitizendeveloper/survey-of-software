# Data Visualization Libraries: Discovery Table of Contents

## Overview

This directory contains a **four-pass discovery process** (4PS methodology) for evaluating data visualization libraries in the JavaScript/React ecosystem.

Each pass answers a different question:
- **S1 (Rapid):** WHICH libraries exist? (ecosystem scan)
- **S2 (Comprehensive):** HOW do they work? (technical deep-dive)
- **S3 (Need-Driven):** WHO needs them? (use cases and personas)
- **S4 (Strategic):** WHICH will last? (long-term viability)

## S1: Rapid Discovery

**Focus:** Quick ecosystem scan and initial recommendations

**Files:**
- `S1-rapid/README.md` - Quick decision guide, landscape overview
- `S1-rapid/recharts.md` - The default React choice (9M downloads)
- `S1-rapid/d3.md` - The foundational library (108K stars)
- `S1-rapid/chartjs.md` - Framework-agnostic, small bundle
- `S1-rapid/echarts.md` - Enterprise, large datasets
- `S1-rapid/nivo.md` - SSR-focused React wrapper
- `S1-rapid/visx.md` - D3 + React primitives (Airbnb)
- `S1-rapid/victory.md` - React Native support
- `S1-rapid/comparison-matrix.md` - Side-by-side comparison
- `S1-rapid/recommendation.md` - Initial recommendations

**Key Findings:**
- Recharts dominates React ecosystem (9M vs 500K downloads)
- D3 is foundational (most libraries wrap it)
- Rendering technology (SVG vs Canvas vs WebGL) determines performance ceiling
- Clear tier structure: High-level (Recharts) → Low-level (visx) → Foundational (D3)

## S2: Comprehensive Technical Analysis

**Focus:** Architecture, algorithms, performance, API design

**Files:**
- `S2-comprehensive/approach.md` - Technical analysis framework
- `S2-comprehensive/recharts.md` - React component architecture, D3 integration
- `S2-comprehensive/d3.md` - Module system, scales, shapes, force layouts
- `S2-comprehensive/chartjs.md` - Canvas rendering, plugin system
- `S2-comprehensive/echarts.md` - ZRender engine, WebGL, massive datasets
- `S2-comprehensive/visx.md` - React primitives pattern, composition
- `S2-comprehensive/feature-comparison.md` - Detailed feature matrix
- `S2-comprehensive/recommendation.md` - Technical recommendations

**Key Findings:**
- **SVG ceiling:** ~1000 elements (Recharts, visx, Nivo, Victory)
- **Canvas scales:** 1000-10,000 elements (Chart.js)
- **WebGL handles millions:** ECharts-GL only option
- **React integration patterns:** Library owns DOM (Recharts) vs D3 math + React rendering (visx)
- **Bundle size:** Chart.js (60 KB) < visx (60 KB) < Recharts (130 KB) < ECharts (150-320 KB)

## S3: Need-Driven Use Cases

**Focus:** User personas, pain points, recommended solutions

**Files:**
- `S3-need-driven/approach.md` - Persona analysis framework
- `S3-need-driven/use-case-react-dashboard-developer.md` - Sarah: Building internal analytics (Recharts)
- `S3-need-driven/use-case-data-scientist.md` - Dr. Alex: 100K point datasets (ECharts)
- `S3-need-driven/use-case-custom-visualization-designer.md` - Maya: Pixel-perfect branded charts (visx)
- `S3-need-driven/use-case-mobile-app-developer.md` - Jordan: React Native fitness app (Victory Native)
- `S3-need-driven/recommendation.md` - Persona-based decision tree

**Key Findings:**
- **Different users, different priorities:** Dashboard devs need speed, data scientists need performance, designers need control
- **Experience level matters:** Juniors need Recharts (easy), seniors benefit from visx (flexible)
- **Team constraints shape decisions:** Small teams need stability, large teams can handle complexity
- **Common anti-patterns:** Choosing D3 for standard charts, premature optimization, ignoring team skills

## S4: Strategic Long-Term Analysis

**Focus:** Ecosystem health, adoption trends, migration risk, future-proofing

**Files:**
- `S4-strategic/approach.md` - Viability analysis framework
- `S4-strategic/recharts-viability.md` - 5-year outlook for Recharts (LOW RISK)
- `S4-strategic/d3-echarts-viability.md` - D3 (immortal) and ECharts (Apache backing)
- `S4-strategic/recommendation.md` - Strategic recommendations

**Key Findings:**
- **D3 is immortal:** 13 years old, will outlast frameworks (LOWEST RISK)
- **ECharts enterprise-grade:** Apache backing ensures longevity (LOW RISK)
- **Recharts stable leader:** 5+ years without breaking changes (LOW RISK)
- **visx/Nivo/Victory viable:** Corporate backing (Airbnb, Formidable) but smaller communities (MEDIUM RISK)
- **Future trends:** WebGPU, AI-assisted charts, accessibility mandates, React Server Components

## Quick Reference Guide

### By Use Case

| Need | Recommended Library | Pass Reference |
|------|---------------------|----------------|
| React dashboard, < 1K points | Recharts | S1, S3 (react-dashboard) |
| Large datasets (10K-1M points) | ECharts | S2 (echarts), S3 (data-scientist) |
| Custom visualizations | visx or D3 | S2 (visx/d3), S3 (custom-designer) |
| React Native | Victory Native | S3 (mobile-developer) |
| Framework-agnostic | Chart.js | S1, S2 (chartjs) |
| SSR-critical | Nivo | S3-need-driven/recommendation |
| Maximum longevity (10+ years) | D3 | S4 (d3-echarts-viability) |

### By Technical Requirement

| Requirement | Solution | Pass Reference |
|-------------|----------|----------------|
| < 1000 data points | Any SVG library | S2/feature-comparison |
| 1K-10K points | Canvas (Chart.js, ECharts) | S2/chartjs, S2/echarts |
| 10K-1M points | ECharts Canvas/WebGL | S2/echarts |
| Pixel-perfect design | visx + react-spring | S3/custom-designer |
| Smallest bundle | Chart.js (60 KB) | S2/feature-comparison |
| TypeScript | Recharts, visx, Chart.js | S2/feature-comparison |
| Accessibility | Victory, ECharts SVG mode | S2/feature-comparison |

### By Risk Tolerance

| Risk Level | Libraries | Pass Reference |
|------------|-----------|----------------|
| 🟢 Lowest (10+ years) | D3 | S4/d3-echarts-viability |
| 🟢 Low (5+ years) | ECharts, Recharts, Chart.js | S4/recommendation |
| 🟡 Medium (3-5 years) | visx, Nivo, Victory | S4/recommendation |
| 🔴 High | Archived libraries | S4/approach |

## Decision Trees

### React Projects

```
Are you building a React project?
  YES →
    Data size?
      < 1000 → Standard charts?
                 YES → Recharts (S1, S3)
                 NO → visx (S2, S3)
      1K-10K → ECharts (S2)
      10K+ → ECharts WebGL (S2, S3)

  NO →
    Framework-agnostic →
      < 10K → Chart.js (S1, S2)
      10K+ → ECharts (S2, S3)
```

### By Timeline

```
Project timeline?
  1-2 years → Optimize for speed
               → Recharts or Chart.js (S3)

  3-5 years → Balance speed and longevity
               → Recharts, Chart.js, ECharts (S4)

  5+ years → Only low-risk libraries
              → D3, ECharts, Recharts (S4)

  10+ years → Framework-agnostic only
               → D3 (S4)
```

## Cross-Pass Insights

### Insight 1: Rendering Technology Determines Everything

- **S1:** Identified rendering as key differentiator
- **S2:** Benchmarked exact performance ceilings (SVG: 1K, Canvas: 10K, WebGL: 1M+)
- **S3:** Matched rendering tech to user needs (data scientist needs Canvas/WebGL)
- **S4:** ECharts' WebGL support is strategic advantage (future-proof)

### Insight 2: React Integration Patterns Matter

- **S1:** Noted Recharts vs visx API differences
- **S2:** Explained three patterns (library owns DOM, D3 math + React rendering, D3 controls DOM)
- **S3:** Showed dashboard devs prefer declarative (Recharts), designers need control (visx)
- **S4:** React-specific libraries risk framework lock-in, but ecosystem is stable

### Insight 3: One Size Does NOT Fit All

- **S1:** Warned against "most popular = best" thinking
- **S2:** Showed technical trade-offs (bundle size, performance, customization)
- **S3:** Demonstrated different personas need different libraries
- **S4:** Confirmed no single library dominates all scenarios

### Insight 4: D3 is Infrastructure

- **S1:** Noted most libraries wrap D3
- **S2:** Explained D3 module system, how Recharts uses d3-scale/d3-shape
- **S3:** Showed when teams need raw D3 power (custom visualizations)
- **S4:** D3 will outlast frameworks (rendering-agnostic, timeless algorithms)

## Implementation Recommendations

### Standard React Dashboard (80% of projects)

**Path:** S1 → S3 (react-dashboard)

**Recommendation:** Recharts

**Why:**
- Fastest time to first chart (< 1 hour)
- Covers all common chart types
- Large community (9M downloads)

**Validation:** Read S2 (recharts) for technical details, S4 (recharts-viability) for risk assessment

### Large Dataset Visualization (data analysis tools)

**Path:** S1 → S2 (echarts) → S3 (data-scientist)

**Recommendation:** ECharts

**Why:**
- Only library handling 100K-1M points
- WebGL for massive datasets
- Built-in zoom/pan/export

**Validation:** S4 (d3-echarts-viability) confirms Apache backing ensures longevity

### Custom Branded Visualizations (agencies, marketing sites)

**Path:** S1 → S2 (visx, d3) → S3 (custom-designer)

**Recommendation:** visx (React) or D3 (agnostic)

**Why:**
- Pixel-perfect control
- Can implement any design
- D3 power without DOM conflicts (visx)

**Validation:** S4 confirms medium risk for visx (Airbnb backing), lowest risk for D3

### React Native Mobile App

**Path:** S3 (mobile-developer)

**Recommendation:** Victory Native

**Why:**
- Only viable option
- Touch-optimized
- Cross-platform (iOS + Android)

**Validation:** S4 confirms medium risk (Formidable Labs backing), but no alternative

## Reading Recommendations

### Quick Start (15 minutes)
1. Read S1/README.md (overview)
2. Read S1/recommendation.md (initial guidance)
3. Pick library, read S1/<library>.md

### Thorough Evaluation (2 hours)
1. S1/README.md + S1/recommendation.md (context)
2. S2/<library>.md for top 2-3 candidates (technical deep-dive)
3. S3/use-case-<matching-persona>.md (validate fit)
4. S4/recommendation.md (risk assessment)

### Strategic Planning (1 day)
1. Read all S1 files (ecosystem landscape)
2. Read S2/approach.md + S2/feature-comparison.md (technical framework)
3. Read all S3 use cases (understand personas)
4. Read all S4 files (long-term planning)
5. Create decision matrix for your specific needs

## Methodology Notes

### The 4PS Framework

**S1 (Rapid):** WHAT exists? (1-2 days)
- Ecosystem scan
- Initial filtering
- Quick decision guide

**S2 (Comprehensive):** HOW does it work? (3-5 days)
- Technical deep-dive
- Architecture analysis
- Performance benchmarks

**S3 (Need-Driven):** WHO needs it? (2-3 days)
- User personas
- Use cases
- Pain points and solutions

**S4 (Strategic):** WHICH will last? (1-2 days)
- Ecosystem health
- Adoption trends
- Long-term viability

**Total time:** 1-2 weeks for complete analysis

### Why This Structure?

**Progressive refinement:**
- S1 gets you 80% of the answer in 20% of the time
- S2 adds technical depth
- S3 validates with real-world use cases
- S4 de-risks long-term decisions

**Multiple entry points:**
- Quick decision? Start with S1
- Technical validation? Jump to S2
- Use case matching? Start with S3
- Risk assessment? Go to S4

**Comprehensive coverage:**
- Each pass adds a different lens
- Cross-pass insights emerge
- No single pass tells the whole story

## Future Updates

This research will be updated when:
- Major version releases (React 19, D3 v8, ECharts v6)
- New libraries emerge (e.g., Web Components-based charts)
- Ecosystem shifts (e.g., WebGPU adoption)
- Library abandonments or major changes

**Last updated:** 2026-02-02
**Next review:** 2026-08-02 (6 months)
