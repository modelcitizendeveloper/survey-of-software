# Use Case: E-commerce Product Localization (Volume + Cost)

## Scenario
Online marketplace with 10,000 products needs multi-language translation for product listings.

**Content Types:**
- Product titles (short, 20-50 chars)
- Product descriptions (medium, 200-500 chars)
- Customer reviews (user-generated, informal)
- Category names and filters

**Target Languages:** EN→ZH-CN, ZH-TW, JA, KO (4 targets)

**Volume:**
- Initial: 10K products × 4 languages × 300 chars avg = **12M chars (one-time)**
- Monthly updates: 500 new products × 4 languages × 300 chars = **600K chars/month**
- Annual: 12M + (600K × 12) = **19.2M chars/year**

**Quality Bar:** **Important** but not critical - readable, accurate product info

## Requirements

| Requirement | Priority | Notes |
|-------------|----------|-------|
| **High volume processing** | ✅ Critical | 12M chars initial + 600K/mo |
| **Cost efficiency** | ✅ Critical | Budget-conscious startup |
| **Brand name preservation** | ✅ Critical | Glossary for 200+ brand names |
| **Consistent quality** | ⚠️ Important | Good enough > perfect |
| **Batch processing** | ⚠️ Important | Async workflows acceptable |

## Provider Assessment

### Azure Translator
**Fit:**
- ✅ High volume support (unlimited paid tier)
- ✅ **Lowest cost** ($10/M - half the price of Google)
- ✅ Glossary support (brand names)
- ✅ Batch translation (Blob Storage integration)
- ✅ Direct CJK-CJK (if cross-listing between Asian markets)
- ✅ 2M free tier (covers 3+ months of monthly updates)

**Cost Analysis:**
- **Initial (12M chars):** (12M - 2M free) × $10/M = **$100**
- **Monthly (600K chars):** Covered by 2M free tier = **$0**
- **Annual:** $100 (initial) + $0 (monthly) = **$100**

**Trade-offs:**
- ✅ **Lowest cost** (saves $100-150/year vs Google/DeepL)
- ✅ Competitive quality for e-commerce (good enough)
- ✅ Largest free tier (2M/mo permanent)
- ❌ No formality control (not needed for product descriptions)
- ✅ Azure ecosystem (if already on Azure, seamless)

**Verdict:** ⭐⭐⭐⭐⭐ **Best fit** - Cost is critical, quality is sufficient

---

### Amazon Translate
**Fit:**
- ✅ High volume support
- ✅ Mid-tier cost ($15/M)
- ✅ Custom terminology (10K terms, no extra cost - plenty for 200 brands)
- ✅ Batch translation (S3 integration)
- ✅ Active Custom Translation (if product-specific jargon needed)
- ✅ 2M free tier (covers first 12 months)

**Cost Analysis:**
- **Initial (12M chars):**
  - Year 1: (12M - 2M free) × $15/M = **$150**
  - Year 2+: 12M × $15/M = **$180**
- **Monthly (600K chars):**
  - Year 1: Covered by 2M free tier = **$0**
  - Year 2+: 600K × $15/M = **$9/month**
- **Annual Year 1:** $150
- **Annual Year 2+:** $180 + ($9 × 12) = **$288**

**Trade-offs:**
- ✅ Free for first year (2M/mo)
- ✅ ACT if product-specific customization needed
- ✅ No glossary fees (10K terms included)
- ❌ 50% more expensive than Azure ($15/M vs $10/M)
- ❌ Free tier expires (vs Azure permanent)
- ⚠️ AWS setup overhead if not already on AWS

**Verdict:** ⭐⭐⭐⭐ **Good alternative** - Cost-effective year 1, but Azure cheaper long-term

---

### Google Cloud Translation
**Fit:**
- ✅ High volume support
- ✅ Proven CJK quality (longest track record)
- ✅ Glossary support (unlimited size)
- ✅ Batch translation (Cloud Storage integration)
- ✅ Translation LLM (higher quality option)
- ❌ Premium pricing ($20/M - double Azure)

**Cost Analysis:**
- **Initial (12M chars):** (12M - 0.5M free) × $20/M = **$230**
- **Monthly (600K chars):** (600K - 500K free) × $20/M = **$2/month**
- **Annual:** $230 + ($2 × 12) = **$254**

**Trade-offs:**
- ✅ Highest quality (longest CJK track record)
- ✅ Translation LLM option for critical content
- ❌ **Double the cost** of Azure ($20/M vs $10/M)
- ❌ Smaller free tier (500K vs 2M)
- ⚠️ Premium pricing not justified for e-commerce product descriptions

**Verdict:** ⭐⭐⭐ **Not recommended** - Premium pricing without clear ROI for this use case

---

### DeepL
**Fit:**
- ✅ Good CJK quality (1.7x improvement for JA/ZH-CN)
- ✅ Glossary support (multilingual, 55 pairs)
- ✅ Simple integration
- ❌ **Most expensive** ($25/M + $5.49/mo base fee)
- ❌ No batch text processing (must iterate)

**Cost Analysis:**
- **Initial (12M chars):**
  - (12M - 0.5M free) × $25/M + $5.49 = **$292.99**
- **Monthly (600K chars):**
  - (600K - 500K free) × $25/M + $5.49 = **$8.00/month**
- **Annual:** $292.99 + ($8 × 12) = **$389**

**Trade-offs:**
- ✅ Next-gen LLM quality (1.7x for JA/ZH-CN)
- ✅ Simple integration (easy to start)
- ❌ **Most expensive** (3.9x Azure, 1.5x Google)
- ❌ No batch processing (manual iteration)
- ⚠️ Premium not justified for e-commerce volume use case

**Verdict:** ⭐⭐ **Not recommended** - Cost is prohibitive for high-volume e-commerce

## Cost Comparison (Annual)

| Provider | Initial (12M) | Monthly (600K) | Annual Total | Savings vs Google |
|----------|---------------|----------------|--------------|-------------------|
| **Azure** | **$100** | **$0** | **$100** | **$154 (60%)** |
| **Amazon (Y1)** | **$150** | **$0** | **$150** | **$104 (41%)** |
| **Amazon (Y2+)** | $180 | $9/mo | $288 | -$34 (-13%) |
| **Google** | $230 | $2/mo | $254 | — |
| **DeepL** | $293 | $8/mo | $389 | -$135 (-53%) |

**Azure saves $154/year (60%) compared to Google, $239/year (61%) compared to DeepL.**

## Decision Matrix

| Provider | Cost (Annual) | Quality | Ease | Batch | Verdict |
|----------|---------------|---------|------|-------|---------|
| **Azure** | **$100** ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ **Best** |
| **Amazon (Y1)** | **$150** ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ **Good** |
| **Google** | $254 ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐ **No** |
| **DeepL** | $389 ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ⭐⭐ **No** |

## Recommendation

### Primary: **Azure Translator**
**Why:**
- ✅ **60% cost savings** vs Google ($100 vs $254/year)
- ✅ **61% cost savings** vs DeepL ($100 vs $389/year)
- ✅ Competitive quality (modern NMT, good enough for e-commerce)
- ✅ Batch translation (Blob Storage integration)
- ✅ 2M free tier covers monthly updates (600K/mo) permanently
- ✅ Glossary for brand name preservation
- ✅ Direct CJK-CJK pairs (cross-listing advantage)

**When to reconsider:**
- Quality issues detected (test with sample products first)
- Already on AWS (ecosystem integration advantage lost)

### Alternative: **Amazon Translate (Year 1)**
**Why:**
- ✅ Free first year (2M/mo covers all usage)
- ✅ Custom terminology (10K terms, no extra cost)
- ✅ ACT if product-specific jargon needs customization
- ✅ S3 batch processing (if already on AWS)

**Trade-offs:**
- ⚠️ Free tier expires after 12 months → $288/year ongoing (vs Azure $100)
- ⚠️ 188% more expensive than Azure in year 2+
- ⚠️ AWS setup overhead if not already on AWS

**Verdict:** Good for year 1, but migrate to Azure year 2 unless AWS-native

### Not Recommended: **Google** or **DeepL**
**Why:**
- ❌ Premium pricing ($254-389/year vs Azure $100/year)
- ⚠️ Quality premium not justified for e-commerce product descriptions
- ❌ DeepL: No batch processing (manual iteration for 12M chars)
- ⚠️ Google: Free tier too small (500K vs Azure 2M)

## Implementation Strategy

### Phase 1: Initial Load (Week 1-2)
1. Set up Azure Translator account
2. Create glossary with 200 brand names
3. Upload initial 10K product data to Azure Blob Storage
4. Submit batch translation jobs (4 target languages)
5. Cost: **$100** for 12M chars

### Phase 2: Monthly Updates (Ongoing)
1. Automate: New product → Blob Storage → Azure Translator → Database
2. Use Azure Functions for serverless processing
3. 600K chars/month covered by 2M free tier
4. Cost: **$0/month**

### Phase 3: Quality Monitoring (Month 2+)
1. Spot-check 1% of translations monthly
2. Track customer complaints about translated product info
3. Refine glossary based on feedback (brand names, product categories)
4. Monitor Azure cost dashboard (should stay at $0/mo after initial load)

## Break-Even Analysis

If quality issues require switching to Google:

| Scenario | Cost Difference (Annual) | Required Quality Improvement |
|----------|-------------------------|------------------------------|
| Azure → Google | +$154/year | **60% better** to justify |
| Azure → DeepL | +$289/year | **289% better** to justify |

**Verdict:** For e-commerce product descriptions (good enough > perfect), Azure's 60% cost savings are hard to justify giving up unless quality is noticeably worse.

## Success Criteria

After 3 months:
- ✅ All 10K products translated to 4 languages
- ✅ Monthly updates automated (<1 hour manual effort)
- ✅ Cost under $110 total (initial $100 + buffer)
- ✅ <5% customer complaints about translated product info
- ✅ Brand names consistently preserved (via glossary)
- ✅ Zero ongoing monthly costs (covered by free tier)
