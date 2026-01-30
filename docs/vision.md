---
sidebar_position: 2
slug: /vision
id: vision
title: "Vision"
---

# Stop Guessing. Start Building.

> **The Great Trigonometric Survey of India (1802-1880) mapped an entire subcontinent—including Mt. Everest—using triangulation from known points. We're doing the same for software: systematically surveying the library landscape so you can assemble your own mountains.**

## The Origin Story

Back in September 2025, at PuPPy Talk Night, I presented research on comparative AI coding methodologies. I took the Claude Code task tool and said "build this thing" with four different approaches working in parallel:
- Immediate implementation
- Specs-driven development
- Test-driven development (TDD)
- Adaptive TDD with mutation testing

The result: a model showing which methodologies fit which programming problems. Adaptive TDD excels at input validation. Specs-driven is ideal for LLM wrappers. Great! Now I knew **how to tell AI to write code** for different purposes.

But then came the real question: **WHY WRITE CODE AT ALL?**

We have thousands of excellent Python libraries. All I needed was a way to figure out which library was right for what I'm building, then write glue code to make it all work together.

## The Great Trigonometric Survey (But for Software)

Think about the [Great Trigonometric Survey of India](https://en.wikipedia.org/wiki/Great_Trigonometrical_Survey), started in 1802 to map the geography of the Indian subcontinent. If you want to know the exact height of Mt. Everest, you don't climb it with a measuring tape. You start from two points X and Y at sea level, take sightings of point Z on land, and use triangulation to calculate Z's height. Keep adding triangles and soon you've mapped not just the peak, but the entire landscape.

**Now think about the most complex software system you can imagine—call it "Mt. Everest."** What is it really? Just an accumulation of smaller pieces: libraries, frameworks, modules, APIs. And now that we can generate software modules quickly with AI, what's stopping us from assembling our own code mountains?

**Answer: Nothing! We're limited only by our imagination.** (Oh, and token budget.)

## The Dewey Decimal System for Algorithms

I created a classification system for software libraries, organized like the Dewey Decimal System:

- **1.001-1.009** - Sorting & Searching Libraries
- **1.010-1.019** - Graph & Network Analysis
- **1.020-1.029** - Math & Statistics
- **1.030-1.059** - String & Text Processing
- **1.060-1.069** - Cryptographic & Hashing
- **1.070-1.099** - Data Structures & Algorithms
- **1.100-1.149** - Machine Learning & AI
- **1.150-1.159** - Geometric & Spatial
- **1.160-1.169** - Compression & Encoding
- **1.170-1.209** - LLMs & Natural Language

The system starts from **1.001 Sorting Libraries** and continues expanding across algorithms, data structures, ML frameworks, and infrastructure components.

## The 4PS Methodology: Four-Pass Survey

I conduct deep research in each category following what I call **4PS - The Four-Pass Survey:**

### S1: Rapid Discovery
Find the popular libraries. Quick comparison table. When you need an answer *now*.

### S2: Comprehensive Analysis
Understand the entire solution space. Feature matrices. Deep comparisons. When you need to know *everything*.

### S3: Need-Driven Discovery
Start with requirements, find exact-fit solutions. Scenario-based selection. When you know *exactly what you're building*.

### S4: Strategic Selection
Think long-term. Consider maintenance, team expertise, ecosystem fit, vendor stability. When you're making *architectural decisions*.

**Plus:** An explainer pass for technical generalists who need context without overwhelming detail.

## The Research

Each survey piece represents deep investigation using the 4PS methodology:
- **Systematic coverage** across algorithms, data processing, ML, and infrastructure
- **40,000+ tokens** of analysis per category
- **Publicly accessible** at research.modelcitizendeveloper.com

Having this repository makes it possible to do **extremely rapid development with greater confidence** because I don't have to:
- Guess which library is right
- Let Claude pick one randomly
- Roll the dice on unmaintained packages
- Stop what I'm doing to do deep research

The map already exists. I just consult it and build.

## What Makes This Different

### NOT: Another Tutorial Site
- Tutorials teach "how to use X"
- **We teach:** "Why X over Y, with measured evidence"

### NOT: Another Awesome List
- Awesome lists are curated links
- **We provide:** Deep analysis with methodology and confidence levels

### NOT: Another Framework
- Frameworks lock you in
- **We give you:** Components you understand and own

### YES: A Surveyed Landscape
- "Here's what we measured"
- "Here's how we measured it"
- "Here's the working implementation"
- **"Replicate it yourself"**

---

## Build Your Own Mountain

If you build something using this survey, **I want to hear about it!**

I write case studies and would love to feature your project. Whether it's a production system, a research project, or a weekend hack—if you assembled your code mountain using this map, let's share the story.

**The vision:** Make it possible for developers and organizations to DIY solutions they would have paid vendors for before. The map is open. The methodology is transparent. The code is yours.

---

## Quality Bar & Limitations

### Research-Grade Confidence
**Overall confidence:** 70-80% (directionally strong guidance)
**Not:** Consumer Reports 95%+ certainty

This research provides **strategic direction**, not absolute guarantees:
- S1 Rapid: 70-80% confidence (speed-optimized)
- S2 Comprehensive: 80-90% confidence (depth-optimized)
- S3 Need-Driven: 75-85% confidence (context-specific)
- S4 Strategic: 60-70% confidence (forward-looking analysis)

### Information Decay

Library ecosystems evolve constantly:
- Pricing changes
- Feature updates
- New entrants
- Vendor pivots
- Acquisitions

**Estimated accuracy:**
- **At publication:** 70-80%
- **12 months:** 50-70%
- **36 months:** \<30%

We aim for **quarterly updates** to major categories and treat research as **living documents** that guide investigation, not gospel truth.

---

## The Road Ahead: Systematic Expansion

The Great Trigonometric Survey took 70 years to map India. We're mapping a different kind of landscape, but the principle holds: **systematic measurement, one triangulation point at a time.**

Each new survey makes the next easier. Patterns emerge across categories. Reusable methodologies compound.

**India wasn't mapped in a day. Neither will the software landscape be.** But every measurement adds value immediately—you don't wait for completion to use the map.

When enough triangulation points exist, you'll see the whole landscape and assemble code mountains with confidence.

---

## Disclaimers

This research is provided "as-is" for informational purposes. While we apply rigorous methodology (4PS), research-grade confidence (~70-80%) is not professional consulting advice. Findings decay as ecosystems evolve. Verify critical decisions with hands-on testing.

No vendor relationships, sponsorships, or financial incentives influence research findings. Pure systematic measurement.
