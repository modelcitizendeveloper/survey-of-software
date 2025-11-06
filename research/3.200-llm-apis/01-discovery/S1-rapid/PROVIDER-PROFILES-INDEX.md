# LLM API Provider Profiles - Index

**Research Project:** 3.200-llm-apis
**Phase:** S1-Rapid Discovery
**Created:** 2025-11-05
**Total Profiles:** 6

---

## Overview

This directory contains comprehensive profiles for 6 major LLM API providers, covering market leaders, enterprise options, and open-source alternatives. Each profile is ~300-400 lines with 10 standardized sections.

---

## Provider Profiles

### 1. [OpenAI](./provider-openai.md) - Industry Leader
- **Models**: GPT-4, GPT-4 Turbo, GPT-4o, GPT-4o-mini, GPT-3.5 Turbo
- **Best For**: Market-leading quality, mature ecosystem, multimodal excellence
- **Pricing**: $0.50-$60/M input, $1.50-$120/M output
- **Key Strengths**: Best developer experience, comprehensive tooling, enterprise-grade reliability
- **Key Limitations**: Premium pricing, 128K context max, training cutoff Oct 2023
- **Lines**: 326

### 2. [Anthropic (Claude)](./provider-anthropic.md) - Premium Safety-Focused
- **Models**: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku
- **Best For**: Long context (200K), safety-critical apps, cost-effective quality
- **Pricing**: $0.25-$15/M input, $1.25-$75/M output
- **Key Strengths**: Best context windows, superior safety, prompt caching (90% savings), recent training data
- **Key Limitations**: No embeddings API, no audio, smaller ecosystem
- **Lines**: 332

### 3. [Google (Gemini)](./provider-google.md) - Cost Leader
- **Models**: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini Flash-8B
- **Best For**: Longest context (1M+ tokens), aggressive pricing, video understanding
- **Pricing**: $0.0375-$2.50/M input, $0.15-$10/M output
- **Key Strengths**: Cheapest frontier models, massive context, Google Search grounding, native multimodal
- **Key Limitations**: Smaller community, API complexity (Vertex AI vs AI Studio), function calling maturity
- **Lines**: 336

### 4. [Mistral AI](./provider-mistral.md) - European Alternative
- **Models**: Mistral Large, Mistral Medium, Mixtral 8x7B, Codestral
- **Best For**: European data sovereignty, open-source self-hosting, multilingual
- **Pricing**: $0.10-$2.00/M input, $0.30-$6.00/M output
- **Key Strengths**: EU-based (GDPR-native), open-source models, permissive licensing, competitive pricing
- **Key Limitations**: Limited multimodal, 128K context max, smaller ecosystem
- **Lines**: 317

### 5. [Cohere](./provider-cohere.md) - RAG Specialist
- **Models**: Command R+, Command R, Embed v3, Rerank v3
- **Best For**: Production RAG systems, best-in-class embeddings/reranking, enterprise search
- **Pricing**: $0.30-$3.00/M input, $0.60-$15/M output
- **Key Strengths**: Complete RAG stack, best embeddings (MTEB leader), reranking, multilingual
- **Key Limitations**: Text-only (no vision/audio), narrower model range, smaller community
- **Lines**: 374

### 6. [Meta Llama (via Groq/Together AI)](./provider-meta-llama.md) - Open Source
- **Models**: Llama 3.1 405B/70B/8B (via Groq, Together AI, self-hosting)
- **Best For**: Ultra-fast inference (Groq), cost optimization, self-hosting, zero lock-in
- **Pricing**: $0.05-$3.50/M (Groq/Together AI), infrastructure cost for self-hosting
- **Key Strengths**: Open-source freedom, Groq speed (10-20x faster), cost leadership, massive community
- **Key Limitations**: No official Meta API, limited multimodal, fragmented ecosystem, function calling maturity
- **Lines**: 436

---

## Quick Comparison Matrix

| Provider | Best Use Case | Cost Tier | Context Window | Multimodal | Open Source |
|----------|--------------|-----------|----------------|------------|-------------|
| **OpenAI** | General purpose, production apps | High | 128K | Yes (text/vision/audio) | No |
| **Anthropic** | Long context, safety-critical | Mid | 200K | Vision only | No |
| **Google** | Cost optimization, video analysis | Low | 1M+ | Yes (text/vision/audio/video) | No |
| **Mistral** | European sovereignty, self-hosting | Mid | 128K | Vision only | Partial |
| **Cohere** | RAG systems, search, embeddings | Mid | 128K | No (text only) | No |
| **Llama** | Speed (Groq), cost, self-hosting | Low | 128K | Limited | Yes |

---

## Decision Framework

### Choose OpenAI when:
- You need the most mature ecosystem and developer experience
- Quality is more important than cost
- Multimodal capabilities (vision + audio) are required
- Enterprise compliance via Azure is valuable

### Choose Anthropic when:
- Long context processing (200K tokens) is critical
- Safety and reduced hallucinations are priorities
- You want best performance-per-dollar in premium tier
- Prompt caching can reduce costs by 50-90%

### Choose Google when:
- Budget constraints are primary concern
- You need massive context windows (1M+ tokens)
- Video understanding is required
- Already using Google Cloud infrastructure

### Choose Mistral when:
- European data sovereignty is required
- Open-source self-hosting is valuable
- Multilingual support (European languages) is critical
- Cost-effective frontier intelligence needed

### Choose Cohere when:
- Building production RAG systems
- Need best-in-class embeddings and reranking
- Enterprise search or customer service applications
- Integrated retrieval+generation pipeline desired

### Choose Llama when:
- Ultra-fast inference needed (Groq's LPUs)
- Cost optimization is critical (cheapest frontier models)
- Self-hosting for data sovereignty required
- Want to eliminate vendor lock-in completely

---

## Pricing Comparison (500 input + 200 output tokens @ 1M requests/month)

| Provider | Model | Monthly Cost | Notes |
|----------|-------|--------------|-------|
| **Google** | Gemini 1.5 Flash | $625 + $300 = **$925** | Cheapest option |
| **Llama (Groq)** | Llama 3.1 70B | $295 + $158 = **$453** | 10x faster than competitors |
| **Cohere** | Command R | $250 + $300 = **$550** | Best for RAG workflows |
| **Anthropic** | Claude 3 Haiku | $125 + $250 = **$375** | Fastest premium model |
| **Anthropic** | Claude 3.5 Sonnet | $1,500 + $3,000 = **$4,500** | Best quality/cost balance |
| **OpenAI** | GPT-4o | $2,500 + $3,000 = **$5,500** | Industry-leading quality |
| **Mistral** | Mistral Large | $1,000 + $1,200 = **$2,200** | EU sovereignty |
| **Google** | Gemini 1.5 Pro | $625 + $1,000 = **$1,625** | Best value for long context |

---

## Key Insights

### Performance Trends
1. **Context Windows**: Google leads (1M+) > Anthropic (200K) > Others (128K)
2. **Speed**: Groq (LPU) >> Google Flash > Others
3. **Quality**: GPT-4o ≈ Claude 3.5 Sonnet ≈ Gemini 1.5 Pro > Llama 3.1 70B > Others

### Cost Trends
1. **Cheapest**: Gemini Flash ($0.075/M) > Llama 8B ($0.05/M Groq) > Claude Haiku ($0.25/M)
2. **Best Value**: Claude 3.5 Sonnet ($3/$15) > Gemini Pro ($1.25/$5) > Command R ($0.50/$1.50)
3. **Premium**: OpenAI GPT-4 ($30/$60) > Claude Opus ($15/$75) > Llama 405B ($3.50/$3.50)

### Strategic Considerations
1. **Lock-in Risk**: Llama (open-source) < Mistral (partial open) < Others (proprietary)
2. **Vendor Viability**: Google/Meta > OpenAI > Anthropic > Cohere > Mistral
3. **Ecosystem Maturity**: OpenAI >> Anthropic > Google > Others

---

## Multi-Provider Strategy Recommendations

### Optimal 3-Provider Stack
1. **Primary**: Claude 3.5 Sonnet (best performance/cost, 200K context)
2. **Budget**: Gemini 1.5 Flash (high-volume, cost-sensitive tasks)
3. **Fallback**: GPT-4o (capacity overflow, specific capabilities)
4. **Embeddings**: Cohere Embed v3 (best quality) or OpenAI (ecosystem integration)

### Cost-Optimized Stack
1. **Primary**: Gemini 1.5 Flash (cheapest, good quality)
2. **Complex Tasks**: Llama 3.1 70B via Groq (fast + affordable)
3. **Embeddings**: Cohere Embed v3 ($0.10/M)

### Quality-First Stack
1. **Primary**: GPT-4o (best overall quality)
2. **Long Context**: Claude 3.5 Sonnet (200K tokens)
3. **Video**: Gemini 1.5 Pro (native video understanding)

### Enterprise Stack
1. **Primary**: OpenAI via Azure (compliance, SLAs)
2. **RAG**: Cohere (embeddings + reranking + generation)
3. **Sovereignty**: Mistral (EU data residency) or self-hosted Llama

---

## File Locations

All profiles located in:
```
/home/ivanadamin/spawn-solutions/research/3.200-llm-apis/01-discovery/S1-rapid/
```

- `provider-openai.md` (326 lines)
- `provider-anthropic.md` (332 lines)
- `provider-google.md` (336 lines)
- `provider-mistral.md` (317 lines)
- `provider-cohere.md` (374 lines)
- `provider-meta-llama.md` (436 lines)

**Total**: 2,121 lines of comprehensive analysis

---

## Next Steps

1. **S2-Deep Dive**: Conduct hands-on testing with each provider
2. **Benchmark Suite**: Create standardized benchmark tests (speed, quality, cost)
3. **Integration Guides**: Develop migration and multi-provider abstraction patterns
4. **Cost Modeling**: Build interactive calculator for workload-specific cost projections
5. **Decision Matrix**: Create weighted scoring system for use-case-specific recommendations

---

**Profile Version:** 1.0
**Last Updated:** November 5, 2025
**Next Review:** December 2025 (pricing and model updates frequent)
