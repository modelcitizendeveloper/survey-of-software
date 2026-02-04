# S1-Rapid: LLM API Provider Discovery - Approach

**Experiment**: 3.200 LLM APIs
**Stage**: S1 - Rapid Discovery
**Date**: November 5, 2025
**Time Budget**: 2-3 hours

---

## Research Question

**"Which LLM API service provides the best combination of capabilities, cost, reliability, and strategic positioning for different use cases?"**

---

## S1 Objectives

1. **Identify major LLM API providers** (6-8 platforms)
2. **Quick capability comparison** (model intelligence, context windows, modalities)
3. **Basic pricing overview** (token costs, context premiums)
4. **Initial recommendations** (which provider for which scenario)

**Out of scope for S1**:
- Detailed pricing calculations (S2)
- Use case matching (S3)
- Vendor viability deep-dive (S4)
- Performance benchmarking (S2)

---

## Provider Selection Criteria

### Tier 1: Frontier Model Providers (Must Include)
Providers with state-of-the-art models, largest context windows, multimodal capabilities:
1. **OpenAI** (GPT-4, GPT-4 Turbo, GPT-3.5)
2. **Anthropic** (Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku)
3. **Google** (Gemini 1.5 Pro, Gemini 1.5 Flash)

### Tier 2: Alternative Commercial (Include 2-3)
Competitive commercial providers with strong differentiation:
4. **Mistral AI** (Mistral Large, Mixtral 8x7B)
5. **Cohere** (Command R+, Command R)
6. **xAI** (Grok-2) - if accessible

### Tier 3: Open-Source / Aggregators (Include 1-2)
Open-source models or multi-provider platforms:
7. **Meta Llama** (via Together AI, Replicate, or Groq)
8. **OpenRouter** (multi-provider aggregator)

---

## Research Methodology

### Per-Provider Profile Structure

Each provider profile will include:

#### 1. Company Overview (2-3 paragraphs)
- Founding year, headquarters
- Funding status (public, PE-backed, VC-backed)
- Market positioning

#### 2. Model Portfolio (table format)
| Model | Intelligence Tier | Context Window | Input Price | Output Price | Use Case |
|-------|------------------|----------------|-------------|--------------|----------|
| ... | ... | ... | ... | ... | ... |

**Intelligence tiers**:
- **Frontier**: Best reasoning, most expensive (GPT-4, Claude Opus, Gemini 1.5 Pro)
- **Mid-Range**: 80-90% quality, 3-5× cheaper (GPT-4 Turbo, Claude Sonnet, Gemini Flash)
- **Fast/Cheap**: 60-70% quality, 10-30× cheaper (GPT-3.5, Claude Haiku, Mixtral)

#### 3. Key Capabilities (bullet list)
- Context window range (8K → 1M tokens)
- Modalities (text, vision, audio, video)
- Function calling / tool use
- Fine-tuning availability
- Embeddings API

#### 4. Pricing Overview (ranges)
- **Input tokens**: $X-Y per million
- **Output tokens**: $X-Y per million
- **Context multipliers**: Long context premium (if any)
- **Rate limits**: Requests per minute (RPM)

#### 5. Differentiators (3-5 key points)
What makes this provider unique vs competitors?

#### 6. Limitations (3-5 key points)
What are the known weaknesses or constraints?

#### 7. Quick Verdict (1-2 sentences)
When to choose this provider?

---

## Comparison Dimensions

### 1. Model Intelligence
- **Measurement**: MMLU score, reasoning benchmarks
- **Tiers**: Frontier (85%+), Mid-range (70-85%), Fast (60-70%)
- **S1 approach**: Qualitative comparison (best/good/acceptable)

### 2. Pricing
- **Measurement**: $/million tokens (input + output)
- **Range**: $0.50 (cheap) → $60 (premium) per million tokens
- **S1 approach**: Price tier bucketing (cheap/mid/expensive)

### 3. Context Window
- **Measurement**: Maximum tokens (8K → 2M)
- **Range**: Small (8K), Medium (32K), Large (128K), XL (200K+), XXL (1M+)
- **S1 approach**: Context tier classification

### 4. Modalities
- **Options**: Text-only, Text+Vision, Text+Vision+Audio
- **S1 approach**: List supported modalities

### 5. Reliability
- **Measurement**: Uptime %, SLA availability
- **S1 approach**: Qualitative (high/medium/low)

### 6. API Compatibility
- **Measurement**: OpenAI-compatible API format
- **S1 approach**: Binary (compatible/proprietary)

---

## Deliverables

### Individual Provider Profiles (6-8 files)
- `provider-openai.md` (300-400 lines)
- `provider-anthropic.md` (300-400 lines)
- `provider-google.md` (300-400 lines)
- `provider-mistral.md` (250-350 lines)
- `provider-cohere.md` (250-350 lines)
- `provider-llama.md` (250-350 lines)
- Optional: `provider-openrouter.md` (200-300 lines)
- Optional: `provider-xai.md` (200-300 lines)

### Synthesis Document
- `recommendations.md` (400-500 lines)
  - Quick decision tree (30-second recommendations)
  - Provider comparison table
  - Use case → provider mapping
  - Cost tier analysis
  - Strategic positioning

---

## Success Criteria

**S1 complete when**:
1. ✅ 6-8 provider profiles created (300-400 lines each)
2. ✅ Quick comparison table (all providers × key dimensions)
3. ✅ Initial recommendations (which provider for which scenario)
4. ✅ Synthesis document with decision framework

**Time constraint**: 2-3 hours maximum (rapid discovery, not comprehensive)

---

## Research Sources

### Primary Sources
- Provider websites and documentation
- Pricing pages (as of November 2025)
- Model cards and technical specs
- API documentation

### Secondary Sources
- LLM leaderboards (LMSYS, Chatbot Arena)
- Artificial Analysis benchmarks
- Industry news (last 6 months)
- Developer community discussions

---

## Key Questions for S1

1. **Which provider has the best cost/performance ratio?**
2. **Which provider offers the longest context window?**
3. **Which provider has the most reliable API?**
4. **Which provider is cheapest for high-volume use cases?**
5. **Which provider supports the most modalities?**
6. **Are there any OpenAI-compatible alternatives?**
7. **What's the pricing range across providers?** (min/max)
8. **Which provider has the best developer experience?**

---

## S1 → S2 Handoff

**What S2 will expand on**:
- Detailed pricing scenarios (chatbot, document analysis, code generation)
- Feature comparison matrix (50+ features across providers)
- Performance benchmarking (speed, quality, reliability)
- Integration complexity (SDKs, streaming, function calling)
- Enterprise features (data residency, SOC2, SLAs)

**What S1 provides**:
- Provider landscape overview (6-8 platforms)
- High-level capability comparison
- Initial cost bucketing (cheap/mid/expensive)
- Quick recommendations (30-second decision tree)

---

**Time Budget**: 2-3 hours
**Output**: 2,500-3,500 lines (6-8 provider profiles + synthesis)
**Confidence Target**: Medium (70%) - sufficient for initial shortlist, deeper validation in S2
