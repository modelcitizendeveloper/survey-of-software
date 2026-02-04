# Pricing & Total Cost of Ownership Analysis
## Experiment 3.202: Speech & Audio AI Services

**Research Phase**: S2 - Comprehensive Analysis
**Date**: 2025-11-24
**Pricing Data**: November 2024

---

## Overview

This document analyzes the Total Cost of Ownership (TCO) for speech/audio AI services across **5 realistic scenarios** over a **3-year period**. We compare SaaS meeting platforms (Fireflies, Otter, Grain, Fathom) against custom API builds (Whisper + Claude for summaries) to identify cost breakpoints and optimal solutions for different use cases.

---

## Pricing Summary: SaaS Platforms

### Fireflies.ai

| Plan | Monthly | Annual | Features |
|------|---------|--------|----------|
| **Free** | $0 | $0 | 3 transcription credits (desktop), 800min storage/seat |
| **Pro** | $18/user | $10/user/mo ($120/year) | Unlimited transcription, AI summaries, CRM integrations (limited) |
| **Business** | Custom | $19/user/mo ($228/year) | Unlimited storage, advanced CRM (Salesforce/HubSpot), team analytics |
| **Enterprise** | Custom | Custom | Private storage, SSO, advanced security, API access |

**Source**: [Fireflies Pricing Guide](https://www.cloudeagle.ai/blogs/blogs-fireflies-ai-pricing-guide), [G2 Fireflies Pricing 2025](https://www.g2.com/products/fireflies-ai/pricing)

---

### Otter.ai

| Plan | Monthly | Annual | Features |
|------|---------|--------|----------|
| **Basic** | $0 | $0 | 300min/month, 30min/meeting limit, 25 meeting history |
| **Pro** | $16.99/user | $8.33/user/mo ($100/year) | 1,200min/month, 90min/meeting, custom vocabulary, action items |
| **Business** | $30/user | $20/user/mo ($240/year) | 6,000min/month, 4hr/meeting, team analytics, admin controls |
| **Enterprise** | Custom | Custom | SSO, advanced security, OtterPilot for Sales |

**Source**: [Fireflies Blog: Otter Pricing](https://fireflies.ai/blog/otter-pricing-plans/)

---

### Grain

| Plan | Monthly | Annual | Features |
|------|---------|--------|----------|
| **Free** | $0 | $0 | 20 meetings total (trial only) |
| **Starter** | Not disclosed | $15/user/mo | Unlimited meetings, basic AI summaries |
| **Business** | Not disclosed | $15-19/user/mo | Advanced AI, HubSpot integration, video clips, Stories |
| **Enterprise** | Custom | Custom | SSO, compliance, volume discounts |

**Source**: S1 Grain profile, [Grain Alternatives 2025](https://www.bluedothq.com/blog/grain-alternatives)

---

### Fathom

| Plan | Monthly | Annual | Features |
|------|---------|--------|----------|
| **Free (Individual)** | $0 | $0 | Unlimited recordings, transcription, storage; 5 GPT-4 summaries/month |
| **Standard (Teams)** | $24/user | Not disclosed | GPT-4 summaries (all meetings), custom templates, team search |
| **Pro (Teams)** | $29/user | Not disclosed | Advanced AI, enhanced integrations, admin controls |
| **Alternative pricing** | Varies | $15-19/user/mo | (Some sources cite different pricing structures) |

**Source**: S1 Fathom profile

---

## Pricing Summary: APIs

### OpenAI Whisper API

| Model | Price per minute | Price per hour |
|-------|------------------|----------------|
| **Whisper** | $0.006 | $0.36 |
| **GPT-4o Transcribe** | $0.006 | $0.36 |
| **GPT-4o Mini Transcribe** | $0.003 | $0.18 |

**Free Credits**: $5 (expires in 3 months) = 833 minutes (13.9 hours) with Whisper

**Source**: [OpenAI Pricing](https://platform.openai.com/docs/pricing), [CostGoat OpenAI Transcription](https://costgoat.com/pricing/openai-transcription)

---

### Claude API (for Summarization)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| **Claude Haiku 4.5** | $1 | $5 |
| **Claude Sonnet 3.7** | $3 | $15 |
| **Claude Opus 4.5** | $5 | $25 |

**Free Credits**: 50 hours/day code execution (additional $0.05/hour)

**Typical Transcript Token Count**:
- 1 hour meeting = ~10,000-15,000 tokens (input)
- Summary output = ~500-1,000 tokens

**Estimated Cost per Summary (Haiku 4.5)**:
- Input: 15,000 tokens = $0.015
- Output: 1,000 tokens = $0.005
- **Total: ~$0.02 per meeting summary**

**Source**: [Anthropic Pricing](https://www.anthropic.com/pricing), [Finout Anthropic API Pricing](https://www.finout.io/blog/anthropic-api-pricing)

---

### AssemblyAI

| Service | Price per hour |
|---------|----------------|
| **Async Speech-to-Text (Best)** | $0.37 |
| **Async Speech-to-Text (Nano)** | $0.047 (estimated) |
| **Real-time Speech-to-Text** | $0.47 |

**Free Credits**: $50 = ~135 hours (Best tier)

**Add-ons**: Many features included (diarization, sentiment); some advanced features (PII redaction, summarization) may have additional costs

**Source**: S1 AssemblyAI profile

---

### Deepgram

| Service | Price per hour |
|---------|----------------|
| **Nova-2 STT** | $0.258 (starts at $0.0043/min) |

**Free Credits**: $150-200 = ~580-775 hours

**Source**: S1 Deepgram profile

---

### Rev AI

| Service | Price per hour |
|---------|----------------|
| **Standard API** | $2.10 ($0.035/min) |
| **Enterprise API** | $1.20 ($0.02/min with volume) |

**Source**: S1 Rev AI profile

---

## Custom API Build Cost Components

### Infrastructure & Development

For a basic Whisper + Claude transcription/summary pipeline:

**One-time Development Costs**:
- Backend API integration: 20-40 hours @ $100/hr = $2,000-4,000
- Front-end UI (upload, playback, transcript display): 40-60 hours @ $100/hr = $4,000-6,000
- Calendar integration (auto-join meetings): 60-80 hours @ $100/hr = $6,000-8,000
- **Total Development**: $12,000-18,000

**Infrastructure Costs** (monthly):
- Web hosting (Vercel, Netlify): $0-50/month
- Database (transcript storage): $10-30/month (Supabase, Firebase)
- File storage (audio/video): $20-100/month (AWS S3, Cloudflare R2)
- **Total Infrastructure**: ~$50-200/month = $600-2,400/year

**Ongoing Maintenance** (annual):
- Bug fixes, updates, security patches: 10-20 hours/year @ $100/hr = $1,000-2,000/year

**Amortized 3-Year Development Cost**:
- Development: $12,000-18,000 ÷ 3 = $4,000-6,000/year
- Infrastructure: $600-2,400/year
- Maintenance: $1,000-2,000/year
- **Total Fixed Cost**: ~$5,600-10,400/year

---

## TCO SCENARIO 1: Solo Consultant

### Profile
- **Users**: 1
- **Meetings**: 10/week, 1 hour avg
- **Monthly Volume**: 40 hours transcription
- **Annual Volume**: 480 hours
- **Requirements**: Basic transcription, summaries, no CRM integration
- **Technical Capacity**: Non-technical (prefers SaaS)

### 3-Year TCO Comparison

| Option | Year 1 | Year 2 | Year 3 | 3-Year Total | Notes |
|--------|--------|--------|--------|--------------|-------|
| **Fathom Free** | $0 | $0 | $0 | **$0** | Unlimited storage, 5 GPT-4 summaries/mo (limited) |
| **Fathom Standard** | $288 | $288 | $288 | **$864** | Unlimited GPT-4 summaries, custom templates |
| **Otter Pro (Annual)** | $100 | $100 | $100 | **$300** | 1,200min/mo limit OK (480hrs/year = 1,000min/mo avg) |
| **Fireflies Pro (Annual)** | $120 | $120 | $120 | **$360** | Unlimited transcription, fair-use policy |
| **Grain Business** | $180 | $180 | $180 | **$540** | Overkill for solo user (customer-facing focus) |
| **Whisper + Claude API** | $173 + $115 = $288 | $288 | $288 | **$864** | Whisper: $173/yr (480hrs x $0.36), Claude: ~$115/yr (480 summaries x $0.24) |
| **AssemblyAI Best** | $178 | $178 | $178 | **$534** | $0.37/hr x 480hrs = $178/year (no summary API cost) |

**Analysis**:
- **Best Free Option**: Fathom (genuinely unlimited, but only 5 GPT-4 summaries/month)
- **Best Paid Value**: Otter Pro Annual ($300 over 3 years)
- **API Build**: Not worth it for solo user ($12K-18K dev cost + $864 API costs = $13K-19K total)

**Recommendation Zone**: Fathom Free → Otter Pro (if need more summaries)

---

## TCO SCENARIO 2: Small Team

### Profile
- **Users**: 5
- **Meetings**: 20/week total (4 per user)
- **Monthly Volume**: 80 hours transcription
- **Annual Volume**: 960 hours
- **Requirements**: Team collaboration, shared workspace, basic integrations (Slack, calendar)
- **Technical Capacity**: Limited (1 developer, but focused on product)

### 3-Year TCO Comparison

| Option | Year 1 | Year 2 | Year 3 | 3-Year Total | Cost per User per Year |
|--------|--------|--------|--------|--------------|----------------------|
| **Fathom Free (5 users)** | $0 | $0 | $0 | **$0** | $0 |
| **Fathom Standard (5 users)** | $1,440 | $1,440 | $1,440 | **$4,320** | $288/user/year |
| **Otter Pro (5 users, annual)** | $500 | $500 | $500 | **$1,500** | $100/user/year |
| **Otter Business (5 users, annual)** | $1,200 | $1,200 | $1,200 | **$3,600** | $240/user/year |
| **Fireflies Pro (5 users, annual)** | $600 | $600 | $600 | **$1,800** | $120/user/year |
| **Grain Business (5 users)** | $900 | $900 | $900 | **$2,700** | $180/user/year |
| **Whisper + Claude API** | $346 + $230 = $576 | $576 | $576 | **$1,728** | N/A (shared pool) |
| **API Build (Whisper + Claude)** | $5,600 + $576 = $6,176 | $5,600 + $576 = $6,176 | $5,600 + $576 = $6,176 | **$18,528** | $1,234/user/year |

**Whisper + Claude Calculation**:
- Whisper: 960 hours x $0.36 = $346/year
- Claude Haiku: 960 summaries x $0.024 = $230/year (assuming 1 summary per meeting)
- Total API cost: $576/year

**API Build Cost**:
- Fixed costs: $5,600/year (amortized dev + infrastructure + maintenance)
- Variable API costs: $576/year
- Total: $6,176/year

**Analysis**:
- **Best Free**: Fathom Free (unlimited for all 5 users, but limited summaries)
- **Best Value Paid**: Otter Pro Annual ($1,500 over 3 years = $100/user/year)
- **Best Features**: Fireflies Pro ($1,800) or Otter Business ($3,600) for team analytics
- **API Build**: Not justified ($18K vs $1.5K-3.6K for SaaS)

**Break-even**: API never breaks even due to high fixed dev costs vs low variable API costs

**Recommendation Zone**: Fathom Free → Otter Pro → Fireflies Pro (if need advanced features)

---

## TCO SCENARIO 3: Sales Team (CRM Integration Required)

### Profile
- **Users**: 10 (sales reps)
- **Meetings**: 50 calls/week (5 per rep)
- **Monthly Volume**: 100 hours transcription
- **Annual Volume**: 1,200 hours
- **Requirements**: Salesforce or HubSpot CRM integration (deep sync), deal intelligence, call analytics
- **Technical Capacity**: Moderate (IT team can support SaaS integrations)

### 3-Year TCO Comparison

| Option | Year 1 | Year 2 | Year 3 | 3-Year Total | Cost per User per Year |
|--------|--------|--------|--------|--------------|----------------------|
| **Fireflies Business (10 users)** | $2,280 | $2,280 | $2,280 | **$6,840** | $228/user/year |
| **Grain Business (10 users)** | $1,800 | $1,800 | $1,800 | **$5,400** | $180/user/year (HubSpot focus) |
| **Otter Business (10 users)** | $2,400 | $2,400 | $2,400 | **$7,200** | $240/user/year (limited CRM) |
| **Fathom Pro (10 users)** | $3,480 | $3,480 | $3,480 | **$10,440** | $348/user/year (export only, no deep CRM) |
| **API Build + Custom CRM Integration** | $8,000 + $432 = $8,432 | $5,600 + $432 = $6,032 | $5,600 + $432 = $6,032 | **$20,496** | $683/user/year |

**API Build Details**:
- Base dev cost: $12,000-18,000 (using $15,000 midpoint)
- CRM integration dev: $6,000-10,000 (Salesforce/HubSpot API integration)
- Total dev: $21,000-28,000 (using $24,000 midpoint)
- Amortized: $8,000/year
- Fixed annual: $5,600/year (infrastructure + maintenance)
- Whisper API: 1,200hrs x $0.36 = $432/year
- Claude API: 1,200 summaries x $0.024 = ~$29/year (negligible)

**Analysis**:
- **Best CRM Integration**: Grain Business ($5,400) for HubSpot users; Fireflies Business ($6,840) for Salesforce
- **Weakest CRM**: Fathom (export only, no bi-directional sync)
- **API Build**: Still not justified ($20K vs $5-7K for SaaS with native CRM)

**Key Insight**: Deep CRM integration (Salesforce, HubSpot) is **only available on Business tier** for Fireflies and Grain. This is a critical cost gate.

**Recommendation Zone**: Grain Business (HubSpot) or Fireflies Business (Salesforce/HubSpot)

---

## TCO SCENARIO 4: High Volume Transcription

### Profile
- **Users**: N/A (API-focused, custom application)
- **Monthly Volume**: 100 hours transcription
- **Annual Volume**: 1,200 hours
- **Requirements**: Speed, cost optimization, custom integration, no CRM
- **Technical Capacity**: High (dev team building product)

### 3-Year TCO Comparison

| Option | Year 1 | Year 2 | Year 3 | 3-Year Total | Cost per Hour |
|--------|--------|--------|--------|--------------|---------------|
| **Whisper API** | $432 | $432 | $432 | **$1,296** | $0.36/hour |
| **Whisper + Claude Summaries** | $461 | $461 | $461 | **$1,383** | $0.38/hour |
| **Deepgram Nova-2** | $310 | $310 | $310 | **$930** | $0.258/hour |
| **AssemblyAI Best** | $444 | $444 | $444 | **$1,332** | $0.37/hour |
| **AssemblyAI Nano** | $56 | $56 | $56 | **$168** | $0.047/hour (est) |
| **Rev AI Standard** | $2,520 | $2,520 | $2,520 | **$7,560** | $2.10/hour |
| **Rev AI Enterprise (volume)** | $1,440 | $1,440 | $1,440 | **$4,320** | $1.20/hour |
| **API Build (Whisper + Claude + Dev)** | $8,000 + $461 = $8,461 | $5,600 + $461 = $6,061 | $5,600 + $461 = $6,061 | **$20,583** | $5.72/hour (avg) |

**Whisper + Claude Calculation**:
- Whisper: 1,200 x $0.36 = $432
- Claude Haiku: 1,200 x $0.024 = $29
- Total: $461/year

**Analysis**:
- **Cheapest API**: AssemblyAI Nano ($168 over 3 years) if quality acceptable
- **Best Speed**: Deepgram Nova-2 ($930) - fastest processing (5s for 14min audio)
- **Best Accuracy**: Rev AI ($7,560 for standard; $4,320 for enterprise volume) - 96%+ accuracy
- **Best Balance**: Whisper ($1,296) - good accuracy, lowest cost for quality tier
- **API Build**: Only justifies if need proprietary features (still $20K vs $168-1,296 for APIs)

**Break-even Analysis**: At 1,200 hours/year, pure API usage is cheaper than custom build. Break-even would require **extremely high volume** (10,000+ hours/year) or specialized requirements justifying dev cost.

**Recommendation Zone**: Deepgram Nova-2 (speed) or Whisper (cost)

---

## TCO SCENARIO 5: Enterprise (50+ Users, Compliance)

### Profile
- **Users**: 50
- **Meetings**: 200/week (4 per user)
- **Monthly Volume**: 400 hours transcription
- **Annual Volume**: 4,800 hours
- **Requirements**: HIPAA BAA, SOC 2, SSO, admin controls, SLA, compliance
- **Technical Capacity**: High (enterprise IT team)

### 3-Year TCO Comparison

| Option | Year 1 | Year 2 | Year 3 | 3-Year Total | Cost per User per Year |
|--------|--------|--------|--------|--------------|----------------------|
| **Fireflies Enterprise** | Custom (~$15,000) | $15,000 | $15,000 | **~$45,000** | $300/user/year (est) |
| **Otter Enterprise** | Custom (~$18,000) | $18,000 | $18,000 | **~$54,000** | $360/user/year (est) |
| **Grain Enterprise** | Custom (~$12,000) | $12,000 | $12,000 | **~$36,000** | $240/user/year (est) |
| **Fathom Pro (50 users)** | $17,400 | $17,400 | $17,400 | **$52,200** | $348/user/year (no Enterprise tier disclosed) |
| **AssemblyAI (HIPAA BAA)** | $1,776 | $1,776 | $1,776 | **$5,328** | N/A (API, not per-user) |
| **Rev AI Enterprise (HIPAA BAA)** | $5,760 | $5,760 | $5,760 | **$17,280** | N/A |
| **API Build (AssemblyAI + Compliance)** | $10,000 + $1,776 = $11,776 | $6,000 + $1,776 = $7,776 | $6,000 + $1,776 = $7,776 | **$27,328** | $182/user/year |

**API Build for Enterprise** (AssemblyAI):
- Enhanced dev cost: $30,000 (compliance features, SSO, admin dashboard, SLA monitoring)
- Amortized: $10,000/year (Year 1), $6,000/year (Year 2-3 with lower maintenance)
- AssemblyAI API: 4,800hrs x $0.37 = $1,776/year
- Total Year 1: $11,776; Year 2-3: $7,776/year

**Analysis**:
- **Cheapest Compliant Option**: API Build with AssemblyAI ($27K over 3 years)
- **SaaS Enterprise**: $36K-54K depending on platform
- **Break-even**: API build becomes cost-effective at **enterprise scale** due to high per-user SaaS costs vs usage-based API pricing
- **Compliance**: AssemblyAI, Rev AI, Fireflies, Fathom offer HIPAA BAA; Otter has "safeguards" but less clear
- **SSO/Admin**: Enterprise tiers required for SaaS; custom build needs development

**Key Insight**: At 50+ users, **custom API build starts to make financial sense** if technical capacity exists. SaaS per-user costs ($240-360/user/year) exceed API + dev amortization ($182/user/year).

**Recommendation Zone**:
- If technical capacity high: API Build (AssemblyAI or Rev AI)
- If prefer managed: Grain Enterprise (lowest SaaS cost) or Fireflies Enterprise

---

## Break-Even Analysis: SaaS vs API Build

### When Does API Build Make Sense?

**Variable Costs** (API usage grows with volume):
- Whisper: $0.36/hour
- AssemblyAI: $0.37/hour
- Deepgram: $0.26/hour

**Fixed Costs** (SaaS per-user pricing):
- Otter Pro: $100/user/year (8.33 hours/month at $1/hour equivalent)
- Fireflies Pro: $120/user/year (10 hours/month at $1/hour equivalent)
- Grain Business: $180/user/year (15 hours/month at $1/hour equivalent)

**Development Investment**: $12,000-18,000 (basic) to $25,000-30,000 (enterprise-grade)

### Break-Even Calculation

**Scenario: 10 Users**

**SaaS Annual Cost**:
- Otter Pro: $1,000/year (10 users x $100)
- Fireflies Pro: $1,200/year
- Grain Business: $1,800/year

**API Annual Cost** (1,200 hours/year):
- Whisper: $432/year
- AssemblyAI: $444/year
- Deepgram: $310/year

**API Build Total Cost** (Year 1):
- Dev: $15,000 (amortized: $5,000/year)
- Infrastructure: $1,200/year
- Maintenance: $1,500/year
- API (Whisper): $432/year
- **Total Year 1**: $18,132
- **Total Year 2-3**: $7,132/year

**Break-Even Point**: API build breaks even in **Year 3** if:
- Team grows to 20+ users (SaaS cost: $2,000-3,600/year)
- Volume exceeds 2,000 hours/year
- Enterprise features needed (SSO, compliance)

**Conclusion**: For **small teams (< 20 users)** and **moderate volume (< 1,000 hours/year)**, SaaS platforms are more cost-effective. API builds justify at **enterprise scale** or for **specialized requirements** (custom workflows, proprietary features, compliance).

---

## Cost Optimization Strategies

### For SaaS Platforms

1. **Start with Free Tiers**:
   - Fathom (best free tier: unlimited storage)
   - Otter Basic (300min/month)
   - Test before committing to paid

2. **Annual Billing**: Save 40-50%
   - Otter Pro: $100/year vs $204/year (monthly)
   - Fireflies Pro: $120/year vs $216/year (monthly)

3. **Right-Size Plan**:
   - Don't pay for Business tier if don't need CRM integration
   - Otter Pro adequate for most teams (vs Business)

4. **Volume Discounts**:
   - Enterprise plans (25+ users) negotiate custom pricing
   - Contact sales for volume deals

### For API Builds

1. **Choose Right Model**:
   - Whisper: Best accuracy/cost for batch processing
   - Deepgram: Fastest, cost-effective for real-time
   - AssemblyAI Nano: Cheapest for acceptable quality

2. **Self-Host Whisper** (if extremely high volume):
   - Break-even at ~500+ hours/month
   - Requires GPU infrastructure ($276+/month)
   - DevOps overhead significant

3. **Optimize Summary Costs**:
   - Use Claude Haiku 4.5 ($1/$5 per million tokens) vs Opus
   - Cache prompts to reduce input token costs
   - Batch process with Batch API (50% discount)

4. **Infrastructure Savings**:
   - Use Cloudflare R2 vs AWS S3 for storage (cheaper egress)
   - Serverless functions (Vercel, Cloudflare Workers) vs dedicated servers
   - Database: Supabase free tier (up to 500MB) before scaling

---

## Summary: Cost Comparison by Scenario

| Scenario | Best Free Option | Best Paid SaaS | Best API Option | Winner |
|----------|------------------|----------------|-----------------|--------|
| **Solo Consultant** | Fathom Free ($0) | Otter Pro ($300/3yr) | Whisper + Claude ($864/3yr) | **Fathom Free** |
| **Small Team (5)** | Fathom Free ($0) | Otter Pro ($1,500/3yr) | API Build ($18,528/3yr) | **Otter Pro** |
| **Sales Team (10)** | N/A (CRM required) | Grain Business ($5,400/3yr) | API Build ($20,496/3yr) | **Grain Business** |
| **High Volume** | N/A | N/A | Deepgram ($930/3yr) | **Deepgram** |
| **Enterprise (50)** | N/A | Grain Enterprise (~$36,000/3yr) | API Build ($27,328/3yr) | **API Build** |

---

## Key Findings

1. **Fathom Free is genuinely unlimited** - best free tier for solo professionals and small teams
2. **SaaS wins for small teams** (< 20 users, < 1,000 hours/year) due to low dev cost barrier
3. **CRM integrations gated on Business tier** - major cost jump ($180-240/user/year)
4. **APIs win for high volume** - usage-based pricing cheaper than per-user at scale
5. **Enterprise break-even** - API build justifies at 50+ users or specialized compliance needs
6. **Whisper cheapest API** - $0.36/hour vs $0.37 (AssemblyAI), $2.10 (Rev AI)
7. **Annual billing saves 40-50%** - always choose annual over monthly

---

## Data Sources

- [CloudEagle: Fireflies Pricing Guide](https://www.cloudeagle.ai/blogs/blogs-fireflies-ai-pricing-guide)
- [G2: Fireflies Pricing 2025](https://www.g2.com/products/fireflies-ai/pricing)
- [Fireflies Blog: Otter Pricing Plans](https://fireflies.ai/blog/otter-pricing-plans/)
- [OpenAI Pricing Documentation](https://platform.openai.com/docs/pricing)
- [CostGoat: OpenAI Transcription Pricing Nov 2025](https://costgoat.com/pricing/openai-transcription)
- [Anthropic Claude Pricing](https://www.anthropic.com/pricing)
- [Finout: Anthropic API Pricing Guide 2025](https://www.finout.io/blog/anthropic-api-pricing)
- [Brass Transcripts: Whisper API Pricing 2025](https://brasstranscripts.com/blog/openai-whisper-api-pricing-2025-self-hosted-vs-managed)
- S1 provider profiles (Fireflies, Otter, Grain, Fathom, Whisper, AssemblyAI, Deepgram, Rev AI)

---

**Last Updated**: 2025-11-24
**Next Document**: accuracy-benchmarks.md (transcription quality comparison)
