# TTS Platform Pricing & Total Cost of Ownership (TCO)

**Last Updated**: November 25, 2025
**Analysis Period**: 3 years (36 months)
**Scenarios**: 6 volume levels (100K to 100M chars/month)

---

## Pricing Models Summary

| Platform | Model | Base Price | Free Tier | Notes |
|----------|-------|------------|-----------|-------|
| **Google Cloud TTS** | Pay-per-use | $4-16/M chars | 4M chars/month (ongoing) | Neural = $16/M |
| **Amazon Polly** | Pay-per-use | $4-16/M chars | 1M chars/month (12 months) | Neural = $16/M |
| **Azure TTS** | Pay-per-use | $16/M chars | F0 tier (limited) | Neural standard |
| **ElevenLabs** | Subscription | $5-1,320/month | 10K chars/month | Effective $20-66/M |
| **Play.ht** | Subscription | $31-99/month | 12.5K chars/month | Unlimited = $99/month |
| **Coqui TTS** | Self-hosted | Infrastructure only | Unlimited | GPU hosting $200-1,500/mo |
| **Piper TTS** | Self-hosted | Infrastructure only | Unlimited | CPU hosting $10-100/mo |

---

## Scenario 1: Startup MVP (100K chars/month)

**Profile**: Early-stage language learning app, 100 active users, 1,000 vocabulary sentences/day

### Monthly Costs (Year 1)

| Platform | Month 1-12 Cost | Breakdown | Free Tier Coverage |
|----------|----------------|-----------|-------------------|
| **Google Cloud TTS** | **$0** | Free tier covers 4M/mo | ✅ 100% covered |
| **Amazon Polly** | **$0** | Free tier covers 1M/mo | ✅ 100% covered (12mo) |
| **Azure TTS** | **$0** | F0 tier covers | ✅ 100% covered |
| **ElevenLabs** | $5 | Starter plan (90K included, 10K overage) | ⚠️ Need paid plan |
| **Play.ht** | $31 | Creator plan (3M included) | ⚠️ Need paid plan |
| **Coqui TTS** | $20 | Small VPS (2 CPU, 4GB) | N/A |
| **Piper TTS** | $10 | Budget VPS (1 CPU, 2GB) | N/A |

### 3-Year TCO

| Platform | Year 1 | Year 2 | Year 3 | Total (36mo) | Avg/Month |
|----------|--------|--------|--------|--------------|-----------|
| **Google Cloud TTS** | $0 | $0 | $0 | **$0** | $0 |
| **Amazon Polly** | $0 | $19 | $19 | **$38** | $1 |
| **Azure TTS** | $0 | $19 | $19 | **$38** | $1 |
| **ElevenLabs** | $60 | $60 | $60 | **$180** | $5 |
| **Play.ht** | $374 | $374 | $374 | **$1,122** | $31 |
| **Coqui TTS** | $240 | $240 | $240 | **$720** | $20 |
| **Piper TTS** | $120 | $120 | $120 | **$360** | $10 |

**Winner**: Google Cloud TTS ($0) — free tier covers 100K chars/mo forever

**Recommendation**: Start with Google Cloud TTS (free), upgrade to Amazon Polly if need speech marks, or Azure if need pronunciation assessment.

---

## Scenario 2: Growing App (1M chars/month)

**Profile**: Language learning app, 1,000 active users, early traction, consistent growth

### Monthly Costs (Steady State)

| Platform | Monthly Cost | Breakdown |
|----------|-------------|-----------|
| **Google Cloud TTS** | **$0** | Free tier covers 4M/mo |
| **Amazon Polly** (yr 1) | **$0** | Free tier covers 1M/mo |
| **Amazon Polly** (yr 2+) | $16 | 1M × $16/M |
| **Azure TTS** | $16 | 1M × $16/M (F0 exhausted) |
| **ElevenLabs** | $22 | Creator plan (500K included, 500K overage × $44/M) |
| **Play.ht** | $31 | Creator plan (3M included) |
| **Coqui TTS** | $50 | Medium VPS (4 CPU, 8GB) |
| **Piper TTS** | $20 | Small VPS (2 CPU, 4GB) |

### 3-Year TCO

| Platform | Year 1 | Year 2 | Year 3 | Total (36mo) | Avg/Month |
|----------|--------|--------|--------|--------------|-----------|
| **Google Cloud TTS** | $0 | $0 | $0 | **$0** | $0 |
| **Amazon Polly** | $0 | $192 | $192 | **$384** | $11 |
| **Azure TTS** | $192 | $192 | $192 | **$576** | $16 |
| **ElevenLabs** | $264 | $264 | $264 | **$792** | $22 |
| **Play.ht** | $374 | $374 | $374 | **$1,122** | $31 |
| **Coqui TTS** | $600 | $600 | $600 | **$1,800** | $50 |
| **Piper TTS** | $240 | $240 | $240 | **$720** | $20 |

**Winner**: Google Cloud TTS ($0) — free tier still covers

**Recommendation**: Google Cloud TTS (free) until growth exceeds 4M chars/month.

---

## Scenario 3: Profitable SaaS (5M chars/month)

**Profile**: Language learning app, 5,000 paying users, $15/month avg subscription, $75K MRR

### Monthly Costs (Steady State)

| Platform | Monthly Cost | Breakdown |
|----------|-------------|-----------|
| **Google Cloud TTS** | $16 | 1M × $16/M (4M free + 1M paid) |
| **Amazon Polly** | $80 | 5M × $16/M |
| **Azure TTS** | $80 | 5M × $16/M |
| **ElevenLabs** | $99 | Pro plan (2M included, 3M overage × $49/M = $147) |
| **Play.ht** | $31 | Creator plan (3M included, 2M overage × $12.48/M = $25) |
| **Coqui TTS** | $100 | VPS with GPU (g5.xlarge spot) |
| **Piper TTS** | $30 | Medium VPS (4 CPU, 8GB) |

### 3-Year TCO

| Platform | Year 1 | Year 2 | Year 3 | Total (36mo) | Avg/Month | % of Revenue |
|----------|--------|--------|--------|--------------|-----------|--------------|
| **Google Cloud TTS** | $192 | $192 | $192 | **$576** | $16 | 0.02% |
| **Amazon Polly** | $960 | $960 | $960 | **$2,880** | $80 | 0.11% |
| **Azure TTS** | $960 | $960 | $960 | **$2,880** | $80 | 0.11% |
| **ElevenLabs** | $1,188 | $1,188 | $1,188 | **$3,564** | $99 | 0.13% |
| **Play.ht** | $374 | $374 | $374 | **$1,122** | $31 | 0.04% |
| **Coqui TTS** | $1,200 | $1,200 | $1,200 | **$3,600** | $100 | 0.13% |
| **Piper TTS** | $360 | $360 | $360 | **$1,080** | $30 | 0.04% |

**Winner**: Google Cloud TTS ($16/mo) — free tier still covers 80%

**Recommendation**: Google Cloud TTS (cheapest) or Play.ht Creator (flat rate, predictable).

**Note**: TTS costs <0.15% of revenue at this scale (negligible).

---

## Scenario 4: High-Volume App (10M chars/month)

**Profile**: Popular language learning app, 10,000 paying users, $150K MRR

### Monthly Costs (Steady State)

| Platform | Monthly Cost | Breakdown |
|----------|-------------|-----------|
| **Google Cloud TTS** | $96 | 6M × $16/M (4M free + 6M paid) |
| **Amazon Polly** | $160 | 10M × $16/M |
| **Azure TTS** | $160 | 10M × $16/M |
| **ElevenLabs** | $330 | Scale plan (11M included, no overage) |
| **Play.ht** | **$99** | Unlimited plan (flat rate) ⭐ |
| **Coqui TTS** | $200 | GPU VPS (g5.xlarge reserved) |
| **Piper TTS** | $50 | Large VPS (8 CPU, 16GB) |

### 3-Year TCO

| Platform | Year 1 | Year 2 | Year 3 | Total (36mo) | Avg/Month | % of Revenue |
|----------|--------|--------|--------|--------------|-----------|--------------|
| **Google Cloud TTS** | $1,152 | $1,152 | $1,152 | **$3,456** | $96 | 0.06% |
| **Amazon Polly** | $1,920 | $1,920 | $1,920 | **$5,760** | $160 | 0.11% |
| **Azure TTS** | $1,920 | $1,920 | $1,920 | **$5,760** | $160 | 0.11% |
| **ElevenLabs** | $3,960 | $3,960 | $3,960 | **$11,880** | $330 | 0.22% |
| **Play.ht** | **$1,188** | **$1,188** | **$1,188** | **$3,564** | $99 | 0.07% |
| **Coqui TTS** | $2,400 | $2,400 | $2,400 | **$7,200** | $200 | 0.13% |
| **Piper TTS** | $600 | $600 | $600 | **$1,800** | $50 | 0.03% |

**Winner**: Play.ht Unlimited ($99/mo flat) — break-even at 6M chars/month vs cloud

**Recommendation**: Play.ht Unlimited (best value) or Piper TTS (if can self-host).

**Note**: This is the **break-even point** where Play.ht Unlimited becomes cheaper than cloud providers.

---

## Scenario 5: Enterprise Scale (50M chars/month)

**Profile**: Large EdTech platform, 50,000 users, $500K MRR, multi-language support

### Monthly Costs (Steady State)

| Platform | Monthly Cost | Breakdown |
|----------|-------------|-----------|
| **Google Cloud TTS** | $736 | 46M × $16/M (4M free + 46M paid) |
| **Amazon Polly** | $800 | 50M × $16/M |
| **Azure TTS** | $800 | 50M × $16/M |
| **ElevenLabs** | $1,320 | Business plan (66M included, no overage) |
| **Play.ht** | **$99** | Unlimited plan (flat rate) ⭐⭐ |
| **Coqui TTS** | $500 | Multi-GPU cluster (3× g5.xlarge spot) |
| **Piper TTS** | $150 | Load-balanced VPS cluster (3× servers) |

### 3-Year TCO

| Platform | Year 1 | Year 2 | Year 3 | Total (36mo) | Avg/Month | % of Revenue |
|----------|--------|--------|--------|--------------|-----------|--------------|
| **Google Cloud TTS** | $8,832 | $8,832 | $8,832 | **$26,496** | $736 | 0.15% |
| **Amazon Polly** | $9,600 | $9,600 | $9,600 | **$28,800** | $800 | 0.16% |
| **Azure TTS** | $9,600 | $9,600 | $9,600 | **$28,800** | $800 | 0.16% |
| **ElevenLabs** | $15,840 | $15,840 | $15,840 | **$47,520** | $1,320 | 0.26% |
| **Play.ht** | **$1,188** | **$1,188** | **$1,188** | **$3,564** | $99 | 0.02% |
| **Coqui TTS** | $6,000 | $6,000 | $6,000 | **$18,000** | $500 | 0.10% |
| **Piper TTS** | $1,800 | $1,800 | $1,800 | **$5,400** | $150 | 0.03% |

**Winner**: Play.ht Unlimited ($99/mo) — **8× cheaper** than cloud providers at this scale

**Recommendation**: Play.ht Unlimited (best value) or Piper TTS (if DevOps capacity).

**Break-even analysis**: Play.ht saves $22K/year vs Google Cloud TTS at 50M chars/month.

---

## Scenario 6: Massive Scale (100M chars/month)

**Profile**: Global EdTech giant, 100,000+ users, enterprise deployment, $1M+ MRR

### Monthly Costs (Steady State)

| Platform | Monthly Cost | Breakdown |
|----------|-------------|-----------|
| **Google Cloud TTS** | $1,536 | 96M × $16/M (4M free + 96M paid) |
| **Amazon Polly** | $1,600 | 100M × $16/M |
| **Azure TTS** | $1,600 | 100M × $16/M (potential volume discount) |
| **ElevenLabs** | $2,000 | Enterprise custom (est. $20/M at scale) |
| **Play.ht** | **$99** | Unlimited plan (flat rate) ⭐⭐⭐ |
| **Coqui TTS** | $1,000 | Large GPU cluster (6× g5.xlarge reserved) |
| **Piper TTS** | $300 | Large CPU cluster (10× servers) |

### 3-Year TCO

| Platform | Year 1 | Year 2 | Year 3 | Total (36mo) | Avg/Month | % of Revenue |
|----------|--------|--------|--------|--------------|-----------|--------------|
| **Google Cloud TTS** | $18,432 | $18,432 | $18,432 | **$55,296** | $1,536 | 0.15% |
| **Amazon Polly** | $19,200 | $19,200 | $19,200 | **$57,600** | $1,600 | 0.16% |
| **Azure TTS** | $19,200 | $19,200 | $19,200 | **$57,600** | $1,600 | 0.16% |
| **ElevenLabs** | $24,000 | $24,000 | $24,000 | **$72,000** | $2,000 | 0.20% |
| **Play.ht** | **$1,188** | **$1,188** | **$1,188** | **$3,564** | $99 | 0.01% |
| **Coqui TTS** | $12,000 | $12,000 | $12,000 | **$36,000** | $1,000 | 0.10% |
| **Piper TTS** | $3,600 | $3,600 | $3,600 | **$10,800** | $300 | 0.03% |

**Winner**: Play.ht Unlimited ($99/mo) — **16× cheaper** than cloud providers

**Alternative**: Piper TTS ($300/mo) — **5× cheaper** than cloud, if DevOps capacity

**Recommendation**:
1. **Play.ht Unlimited** (simplest, best value)
2. **Piper TTS** (if can self-host, 3× cheaper than Play.ht)
3. **Negotiate enterprise contracts** with cloud providers (volume discounts)

**Break-even analysis**: Play.ht saves $51K/year vs Google Cloud TTS at 100M chars/month.

---

## TCO Summary Across All Scenarios

| Scenario | Monthly Volume | Best Platform | Monthly Cost | 2nd Best | Cost Difference |
|----------|---------------|---------------|--------------|----------|-----------------|
| **1. Startup MVP** | 100K | Google Cloud TTS | $0 | Amazon Polly | $0 (tie) |
| **2. Growing** | 1M | Google Cloud TTS | $0 | Amazon Polly | $0 (tie) |
| **3. Profitable** | 5M | Google Cloud TTS | $16 | Play.ht | +$15/mo |
| **4. High Volume** | 10M | Play.ht Unlimited | $99 | Google Cloud | +$3/mo |
| **5. Enterprise** | 50M | Play.ht Unlimited | $99 | Piper TTS | +$51/mo |
| **6. Massive** | 100M | Play.ht Unlimited | $99 | Piper TTS | +$201/mo |

### Break-Even Points

**Play.ht Unlimited vs Google Cloud TTS**:
- $99/month = (96M - 4M free) × $16/M
- Break-even: **6.2M chars/month**
- Below 6.2M → Google Cloud cheaper
- Above 6.2M → Play.ht cheaper

**Piper TTS vs Google Cloud TTS** (assumes $150/mo hosting):
- $150/month = (96M - 4M free) × $16/M
- Break-even: **9.4M chars/month**
- Below 9.4M → Google Cloud cheaper (or equal if free tier)
- Above 9.4M → Piper cheaper

**Coqui TTS vs Google Cloud TTS** (assumes $500/mo GPU hosting):
- $500/month = (96M - 4M free) × $16/M
- Break-even: **31.3M chars/month**
- Below 31.3M → Google Cloud cheaper
- Above 31.3M → Coqui cheaper

---

## Cost Per Hour of Audio

**Assumption**: 1 hour of audio ≈ 5,000 characters (average speech rate 80 words/min × 60 min × 1.04 chars/word)

| Platform | Cost per 1M chars | Cost per Hour of Audio |
|----------|-------------------|----------------------|
| **Google Cloud TTS** (free tier) | $0 | $0 |
| **Google Cloud TTS** (paid) | $16 | $0.08 |
| **Amazon Polly** | $16 | $0.08 |
| **Azure TTS** | $16 | $0.08 |
| **ElevenLabs** (Scale) | $30 | $0.15 |
| **Play.ht** (10M/mo) | $9.90 effective | $0.05 |
| **Play.ht** (100M/mo) | $0.99 effective | $0.005 |
| **Coqui TTS** (50M/mo) | $10 effective | $0.05 |
| **Piper TTS** (50M/mo) | $3 effective | $0.015 |

**Cheapest per hour**: Play.ht Unlimited at high volume ($0.005/hour = 0.5¢)

---

## Hidden Costs & Considerations

### Cloud Providers (Google, Amazon, Azure)

**Additional costs**:
- ❌ None (pay-per-use includes everything)

**Hidden benefits**:
- ✅ Free tier (Google 4M/mo forever, Amazon 1M/mo × 12mo)
- ✅ No infrastructure management
- ✅ Auto-scaling (no capacity planning)
- ✅ 99.9% SLA (guaranteed uptime)

### Premium SaaS (ElevenLabs, Play.ht)

**Additional costs**:
- ⚠️ Overage charges (ElevenLabs, Play.ht Creator)
- ⚠️ Voice cloning fees (professional tier)

**Hidden benefits**:
- ✅ Flat-rate option (Play.ht Unlimited)
- ✅ Predictable monthly costs
- ✅ Voice cloning included (Instant tier)

### Self-Hosted (Coqui, Piper)

**Additional costs**:
- ❌ Infrastructure (VPS, GPU, storage)
- ❌ DevOps time (deployment, monitoring, scaling)
- ❌ Bandwidth (egress costs if cloud-hosted)
- ❌ Backup & disaster recovery
- ❌ Security updates & patches

**Hidden benefits**:
- ✅ $0 per-character costs (infinite margin)
- ✅ No vendor lock-in (full control)
- ✅ Privacy (data never leaves premises)
- ✅ HIPAA/FERPA compliance easier

**DevOps cost estimation**:
- Setup: 20-40 hours ($2,000-4,000 at $100/hr)
- Ongoing maintenance: 5-10 hours/month ($500-1,000/month)
- **Total Year 1**: $8,000-16,000 (setup + 12 months maintenance)

**Break-even with DevOps**:
- Coqui (GPU $500/mo + DevOps $750/mo) = $1,250/mo total
- vs Google Cloud TTS: $1,250 = (77M chars/month × $16/M) - 4M free
- Break-even: **78M chars/month** (including DevOps costs)

**Conclusion**: Self-hosting only cost-effective at **>50M chars/month** when DevOps costs included.

---

## ROI Analysis: Language Learning App

**Scenario**: 10,000 paying users, $15/month subscription, 10M chars/month

| Platform | Monthly Cost | Annual Cost | Annual Revenue | TTS Cost % | ROI |
|----------|-------------|-------------|----------------|------------|-----|
| **Google Cloud TTS** | $96 | $1,152 | $1,800,000 | 0.06% | 156,250% |
| **Play.ht Unlimited** | $99 | $1,188 | $1,800,000 | 0.07% | 151,515% |
| **Amazon Polly** | $160 | $1,920 | $1,800,000 | 0.11% | 93,750% |
| **Azure TTS** | $160 | $1,920 | $1,800,000 | 0.11% | 93,750% |
| **ElevenLabs** | $330 | $3,960 | $1,800,000 | 0.22% | 45,455% |
| **Piper TTS** | $50 | $600 | $1,800,000 | 0.03% | 300,000% |

**Conclusion**: TTS costs are **negligible** at <0.25% of revenue for all platforms. **Choose based on features, not cost.**

---

## Cost Optimization Strategies

### 1. Leverage Free Tiers
- **Google Cloud TTS**: 4M chars/month forever
- **Amazon Polly**: 1M chars/month × 12 months
- **Strategy**: Use Google for base load, Amazon for 12-month boost

**Savings**: $0 vs $16-32/month for <5M chars/month

### 2. Play.ht Unlimited Break-Even
- Switch to Play.ht Unlimited at **>6M chars/month**
- Savings: $96 - $99 = -$3/month at 10M (minimal)
- Savings: $736 - $99 = **$637/month at 50M** (huge)

**Recommendation**: Switch to Play.ht at >10M chars/month for predictable costs.

### 3. Self-Host at Scale
- Self-host Piper TTS at >20M chars/month
- Savings: $320 - $150 = **$170/month at 20M**
- Savings: $1,536 - $300 = **$1,236/month at 100M**

**Caveat**: Requires DevOps expertise (+$500-1,000/month effective cost).

### 4. Hybrid Strategy
- **0-4M chars/month**: Google Cloud TTS (free tier)
- **4-10M chars/month**: Google Cloud TTS (paid)
- **10M+ chars/month**: Play.ht Unlimited ($99 flat)
- **50M+ chars/month** (with DevOps): Piper TTS (self-hosted)

### 5. Negotiate Enterprise Contracts
At **>50M chars/month**, negotiate with cloud providers:
- Volume discounts (20-40% off standard pricing)
- Reserved capacity pricing
- Custom SLAs and support

**Potential savings**: $12,000-25,000/year at 100M chars/month

---

## Platform Recommendations by Budget

### $0/month Budget
**Recommendation**: Google Cloud TTS (free tier 4M/month)
- Covers up to 4M chars/month forever
- Upgrade to paid when exceed 4M

### $0-100/month Budget
**Recommendation**:
- <6M chars/month: Google Cloud TTS (pay-per-use)
- >6M chars/month: Play.ht Unlimited ($99/month)

### $100-500/month Budget
**Recommendation**:
- **For quality**: ElevenLabs Scale ($330/month, 11M chars)
- **For volume**: Play.ht Unlimited ($99/month, unlimited)
- **For cloud**: Google/Azure/Amazon (6-31M chars)

### $500+/month Budget
**Recommendation**:
- **High volume** (>50M): Play.ht Unlimited ($99) or Piper TTS ($150-300)
- **Premium quality**: ElevenLabs Business ($1,320/month, 66M chars)
- **Enterprise features**: Azure (pronunciation assessment, 140+ languages)

---

## 5-Year Cost Projections

**Assumption**: Language learning app growing 2× annually (1M → 2M → 4M → 8M → 16M chars/month)

| Platform | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 | 5-Year Total |
|----------|--------|--------|--------|--------|--------|--------------|
| **Google Cloud TTS** | $0 | $0 | $0 | $77 | $2,304 | **$2,381** |
| **Amazon Polly** | $0 | $192 | $768 | $1,536 | $3,072 | **$5,568** |
| **Play.ht Unlimited** | $1,188 | $1,188 | $1,188 | $1,188 | $1,188 | **$5,940** |
| **ElevenLabs (Scale)** | $3,960 | $3,960 | $3,960 | $3,960 | $3,960 | **$19,800** |

**Winner**: Google Cloud TTS ($2,381 over 5 years) — free tier covers years 1-3

**Note**: Play.ht becomes cheaper than Amazon/Azure in Year 5 (16M chars/month).

---

## Next Steps

See companion documents:
- **01-feature-matrix.md**: 60+ features across 7 platforms
- **03-quality-latency-benchmarks.md**: Voice quality MOS scores and latency measurements
- **04-integration-complexity.md**: Time-to-first-audio comparison
