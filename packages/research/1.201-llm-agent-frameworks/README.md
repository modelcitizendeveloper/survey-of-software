# 1.201: LLM Agent Frameworks

**Research on multi-agent orchestration frameworks for building collaborative AI systems.**

## Quick Answer

**Which framework should I use?**

- **Most teams (80%):** CrewAI - Role-based, production-ready, proven (Piracanjuba, PwC)
- **Microsoft ecosystem:** AutoGen/Agent Framework - Cross-language, enterprise support
- **Software development:** MetaGPT - Code generation specialist (PRD → implementation)

**See [DISCOVERY_TOC.md](01-discovery/DISCOVERY_TOC.md) for full decision framework.**

## What This Research Covers

Multi-agent frameworks for building collaborative AI systems where multiple specialized agents work together:

**Frameworks Analyzed:**
1. **AutoGen** (Microsoft) - 50.4k stars, conversation-first, cross-language agents
2. **CrewAI** - Role-based teams, fastest production deployment
3. **MetaGPT** - 59.2k stars, software development specialist

**Research Methodology:** Four-Pass Solution Survey (4PS) v1.0
- S1: Rapid Discovery (ecosystem signals, 10 minutes)
- S2: Comprehensive Analysis (technical depth, 60 minutes)
- S3: Need-Driven Discovery (use case validation, 20 minutes)
- S4: Strategic Selection (long-term viability, 15 minutes)

## Key Findings

### Framework Strengths

**CrewAI:**
- Production-ready (Piracanjuba customer support, PwC code generation: 10→70% accuracy)
- Role-based structure (intuitive team mental model)
- Fastest time-to-production
- **Best for:** Customer support, code review, team collaboration workflows

**AutoGen:**
- Conversation-based flexibility (unpredictable workflows)
- Cross-language agents (Python ↔ .NET, unique capability)
- Microsoft enterprise backing
- **Best for:** Microsoft ecosystem, research workflows, human-in-the-loop

**MetaGPT:**
- Software development specialist (complete PRD → code generation)
- Highest GitHub stars (59.2k, #2 framework)
- SOP-driven predictable workflows
- **Best for:** Greenfield code generation, dev tool building

### Proven Production Use Cases

- **Piracanjuba:** Customer support automation with CrewAI (replaced legacy RPA)
- **PwC:** Code generation with CrewAI (10% → 70% accuracy)
- **Microsoft:** Enterprise deployments across industries with AutoGen
- **MGX:** Commercial AI development platform with MetaGPT (launched Feb 2025)

## Repository Structure

```
1.201-llm-agent-frameworks/
├── README.md (this file)
├── DOMAIN_EXPLAINER.md (what are multi-agent frameworks?)
└── 01-discovery/
    ├── DISCOVERY_TOC.md (convergence analysis, start here)
    ├── S1-rapid/ (10 min: ecosystem signals)
    │   ├── approach.md
    │   ├── autogen.md, crewai.md, metagpt.md
    │   └── recommendation.md
    ├── S2-comprehensive/ (60 min: technical depth)
    │   ├── approach.md
    │   ├── autogen.md, crewai.md, metagpt.md
    │   ├── feature-comparison.md (comparison matrix)
    │   └── recommendation.md
    ├── S3-need-driven/ (20 min: use case validation)
    │   ├── approach.md
    │   ├── use-case-*.md (5 scenarios)
    │   └── recommendation.md
    └── S4-strategic/ (15 min: long-term viability)
        ├── approach.md
        ├── autogen-maturity.md, crewai-maturity.md, metagpt-maturity.md
        └── recommendation.md
```

## Quick Start Guide

### 1. New to Multi-Agent Systems?

Start with [DOMAIN_EXPLAINER.md](DOMAIN_EXPLAINER.md) - 5 minute read on what multi-agent frameworks are and when to use them.

### 2. Need a Quick Recommendation?

Read [S1-rapid/recommendation.md](01-discovery/S1-rapid/recommendation.md) - 10 minute ecosystem overview with immediate recommendation.

### 3. Evaluating Frameworks for Production?

Read [DISCOVERY_TOC.md](01-discovery/DISCOVERY_TOC.md) - Synthesized recommendations across all methodologies with decision framework.

### 4. Deep Technical Comparison?

Read [S2-comprehensive/feature-comparison.md](01-discovery/S2-comprehensive/feature-comparison.md) - Detailed comparison matrix across 15+ dimensions.

### 5. Specific Use Case Validation?

See [S3-need-driven/](01-discovery/S3-need-driven/) - Use case analyses for customer support, code generation, research workflows, etc.

## Decision Framework

```
Q: What's your primary use case?

├─ Software development automation (greenfield)
│   → MetaGPT
│
├─ Microsoft/Azure ecosystem
│   → AutoGen/Agent Framework
│
└─ General multi-agent orchestration
    ├─ Unpredictable workflows → AutoGen
    └─ Known workflows → CrewAI
```

**See [DISCOVERY_TOC.md](01-discovery/DISCOVERY_TOC.md) for detailed decision tree.**

## Research Highlights

### Methodology Convergence (High Confidence)

All 4 methodologies (S1-S4) converge on:
- **CrewAI:** Best for 80% of teams (role-based general use)
- **AutoGen:** Best for Microsoft ecosystem + flexibility
- **MetaGPT:** Best for software development specialization

**Confidence:** 77.5% average (high convergence across independent methodologies)

### Production Evidence Wins

**CrewAI's proven deployments** (Piracanjuba, PwC) outweigh **MetaGPT's higher GitHub stars** (59.2k vs undisclosed).

**Insight:** Real-world validation > community interest signals.

### Long-Term Viability (5-10 years)

| Framework | Viability | Key Factor |
|-----------|-----------|------------|
| CrewAI | ⭐⭐⭐⭐ (4/5) | Commercial model (CrewAI AMP revenue) |
| AutoGen/Agent Framework | ⭐⭐⭐⭐ (4/5) | Microsoft strategic commitment |
| MetaGPT | ⭐⭐⭐ (3/5) | Academic backing + MGX commercial (niche specialization risk) |

## Key Trade-offs

**CrewAI:** Fast start ↔ Scaling ceiling (6-12 months for some teams)
**AutoGen:** Flexibility ↔ Complexity (steeper learning curve)
**MetaGPT:** Software dev depth ↔ Narrow specialization (limited general use)

## When This Research Was Conducted

**Date:** January 2026
**Methodology:** Four-Pass Solution Survey (4PS) v1.0
**Time Investment:** ~90 minutes total research
**Data Sources:** Official documentation, GitHub repositories, production case studies, technical blogs (2025-2026)

## Limitations

**No hands-on prototyping:** Research based on documented capabilities and production evidence.
**No performance benchmarks:** Time constraints prevented reproducible performance testing.
**Forward-looking uncertainty:** S4 strategic assessment inherently speculative (70% confidence).

**Recommendation:** Use this research for strategic direction, then prototype top 2 candidates for validation.

## Related Research

- **1.200 LLM Orchestration** - LangChain, LlamaIndex, Haystack (single-agent + RAG)
- **3.200 LLM APIs** - OpenAI, Anthropic, Google (LLM providers these frameworks use)
- **1.203 Vector Databases** - Pinecone, Chroma (RAG storage for agent knowledge)

## Official Resources

- **AutoGen:** https://microsoft.github.io/autogen/
- **CrewAI:** https://docs.crewai.com/
- **MetaGPT:** https://docs.deepwisdom.ai/
- **Microsoft Agent Framework:** https://learn.microsoft.com/en-us/agent-framework/

---

**For detailed analysis, start with [DISCOVERY_TOC.md](01-discovery/DISCOVERY_TOC.md) - convergence analysis and decision framework.**
