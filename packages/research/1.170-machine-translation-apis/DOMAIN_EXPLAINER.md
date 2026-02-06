# Machine Translation APIs for CJK: Domain Explainer

## What This Solves

**The problem:** Your application needs to translate content between Chinese, Japanese, Korean, and other languages automatically, at scale, with acceptable quality.

**Who encounters this:** Product managers launching in Asian markets, engineering teams building international features, content creators localizing for CJK audiences.

**Why it matters:** Manual translation is slow and expensive ($0.10-0.30 per word). Machine translation APIs cost $0.00001-0.000025 per character (1000-3000x cheaper) and translate instantly, enabling use cases that manual translation can't support (real-time chat translation, million-product e-commerce catalogs, user-generated content moderation).

## Accessible Analogies

### Translation as a Service (Not a Product)

Think of machine translation APIs like electricity: you don't build a power plant, you plug into the grid and pay for what you use. The "grid" is a cloud-hosted neural network trained on billions of words.

**Before APIs:** You'd need to:
- Hire linguists familiar with both languages
- Build terminology databases
- Manage translation workflows
- Wait days or weeks for results
- Pay $0.10-0.30 per word

**With APIs:** You:
- Send text to a URL
- Receive translated text instantly
- Pay $0.00001-0.000025 per character (100-1000x cheaper)
- Scale to millions of characters automatically

### Quality as a Spectrum (Not Binary)

Machine translation isn't "perfect" vs "broken" - it's a spectrum from "good enough for gist" to "publication-ready":

| Quality Level | Use Case | Human Analogy |
|---------------|----------|---------------|
| **Gist** | Customer support tickets (understand complaint) | Overhearing conversation in foreign language - catch main point |
| **Good enough** | Product descriptions (understand features) | Tourist asking for directions - get usable information |
| **Business-appropriate** | Internal memos, business correspondence | Colleague email - professional, clear communication |
| **Publication-ready** | Marketing materials, legal documents | Professionally edited book - polished, culturally appropriate |

APIs typically deliver "good enough" to "business-appropriate" - not "gist" (too low) or "publication-ready" (still needs human polish).

### CJK-Specific Challenges (Character vs Word Systems)

**Analogy:** Translating CJK is like converting between Lego blocks (Chinese/Japanese characters) and assembled structures (English words).

- **English**: Space-delimited words (easy to count, "Hello world" = 2 words)
- **Chinese/Japanese**: No spaces between words (need algorithm to detect word boundaries, "你好世界" = looks like 4 characters, actually 2 words: "你好"=hello, "世界"=world)
- **Korean**: Hybrid system (spaces between words but grammar packed into single characters)

**Impact on APIs:**
- Billing by characters (not words) for CJK
- Chinese character = 1 char, English word = ~5 chars on average
- 1000 Chinese characters ≈ 200 English words (not 1000 words)

### Formality as a Dimension (Not Just Formal/Informal)

**Analogy:** Japanese formality (keigo) is like dress codes - you don't wear beach clothes to a wedding.

- **Casual:** Friends chatting (beach attire)
- **Polite:** Default business (business casual)
- **Formal:** Corporate email to client (business formal)
- **Honorific:** Email to company president (tuxedo/evening gown)

**Why APIs matter:** Some APIs (DeepL, Amazon) can switch between casual and formal Japanese with a parameter (`formality: "more"`). Others (Google, Azure) produce fixed formality level - you can't control it.

**Real-world impact:** Sending casual Japanese to a business partner is like showing up to a board meeting in flip-flops - culturally inappropriate, damages relationships.

## When You Need This

### Clear "Yes" Signals

- ✅ **Volume beyond manual**: >100,000 words/month ($10K-30K manual translation cost)
- ✅ **Real-time translation**: Customer support chat, live collaboration, instant messaging
- ✅ **User-generated content**: Product reviews, forum posts, social media (too much to manually translate)
- ✅ **Frequent updates**: Daily product listings, news articles, documentation changes
- ✅ **Multi-language scaling**: 5+ target languages (manual cost multiplies per language)

### Clear "No" Signals

- ❌ **Under 10,000 words/month**: Manual translation may be cheaper and higher quality
- ❌ **Legal/medical critical content**: APIs aren't reliable enough, need certified human translators
- ❌ **Marketing slogans**: Cultural nuance, wordplay, emotion - APIs miss subtlety
- ❌ **Literary translation**: Poetry, novels, creative writing - APIs lack artistic sensibility
- ❌ **One-time project**: 10-page document, $50 to manually translate vs setup overhead for API

### Gray Area (Depends on Quality Bar)

- ⚠️ **Technical documentation**: APIs work well for straightforward instructions, struggle with ambiguity
- ⚠️ **Business correspondence**: Acceptable for internal memos, risky for external client communication (especially Japanese formality)
- ⚠️ **E-commerce product descriptions**: Good enough for catalog browsing, may need human polish for flagship products

**Decision criterion:** If translation errors cause customer confusion or lost trust, API-only is risky. If errors are tolerable (user can figure it out), APIs work.

## Trade-offs

### Quality vs Cost Spectrum

| Approach | Cost per 1M Words | Quality | Turnaround | Use When |
|----------|-------------------|---------|------------|----------|
| **Human (agency)** | $100K-300K | ⭐⭐⭐⭐⭐ | Days-weeks | Publication-critical |
| **Human (freelance)** | $50K-100K | ⭐⭐⭐⭐ | Hours-days | Important content |
| **Machine + human post-edit** | $20K-50K | ⭐⭐⭐⭐ | Hours | Volume + quality needed |
| **Machine translation API** | **$10-25** | ⭐⭐⭐ | Seconds | High volume, acceptable errors |

**Key insight:** APIs are 10,000x cheaper but 20-40% lower quality than humans. The cost-quality trade-off determines when APIs make sense.

### Build vs Buy

**Build your own model:**
- **Cost**: $50K-500K (ML engineer, infrastructure, training data)
- **Timeline**: 6-12 months
- **Maintenance**: Ongoing (model updates, retraining, infrastructure)
- **Control**: Full customization

**Buy API:**
- **Cost**: $10-25 per million characters ($100-250/month at 10M chars)
- **Timeline**: Days to integrate
- **Maintenance**: Zero (provider handles updates)
- **Control**: Limited (glossaries, some providers allow custom models)

**Build only if:**
- Volume is massive (>100B chars/year = $1M+ API costs)
- Domain is hyper-specialized (medical, legal terminology that APIs miss)
- Data privacy prevents cloud APIs (financial, healthcare regulations)
- You have ML expertise in-house (not hiring new)

**For 99% of use cases, buy the API.**

### Self-Hosted vs Cloud Services

**Self-hosted (open source models like Opus-MT, NLLB):**
- **Pros**: No per-character costs, data stays on-prem, no vendor lock-in
- **Cons**: Infrastructure costs ($500-5K/month servers), quality lags commercial APIs, maintenance burden, no SLA

**Cloud APIs (Google, Azure, Amazon, DeepL):**
- **Pros**: Zero infrastructure, best quality, SLAs, automatic updates, pay-per-use
- **Cons**: Per-character costs, vendor lock-in, data leaves your network

**Self-host only if:**
- Compliance requires (HIPAA, financial regulations)
- Volume is extreme (>100B chars/year where infrastructure < API costs)
- Data sovereignty (China requires local hosting)

## Cost Considerations

### Pricing Models (Per Million Characters)

| Provider | Cost/M | Free Tier | Hidden Costs |
|----------|--------|-----------|--------------|
| **Azure** | **$10** | 2M/mo (permanent) | Custom models: $10/mo hosting |
| **Amazon** | $15 | 2M/mo (12 months) | None (ACT included) |
| **Google** | $20 | 500K/mo (permanent) | Document: $0.08/page (alternative) |
| **DeepL** | $25 + $5.49/mo base | 500K/mo (permanent) | Base fee adds up at low volume |

### Break-Even Analysis (vs Manual Translation)

**Assumptions:**
- Manual translation: $0.15/word ($150K per 1M words, ~5M chars)
- API translation: $10-25 per 1M chars ($50-125 per 1M words)

**Break-even:** APIs are cheaper starting at ~1K words/month

| Monthly Volume | Manual Cost | API Cost (Azure) | Savings |
|----------------|-------------|------------------|---------|
| 10K words | $1,500 | **$10** | **99.3%** |
| 100K words | $15,000 | **$100** | **99.3%** |
| 1M words (200K chars) | $150,000 | **$2,000** | **98.7%** |

**Insight:** At any meaningful volume, APIs are dramatically cheaper. Cost is rarely a reason to avoid APIs.

### ROI Calculation Example

**Scenario:** E-commerce company with 10,000 products, translating to 4 languages (JA, ZH-CN, ZH-TW, KO)

**Manual translation:**
- 10K products × 300 words/product × 4 languages = 12M words
- 12M words × $0.15/word = **$1.8M one-time**
- Monthly updates (500 products): 500 × 300 × 4 × $0.15 = **$90K/month**

**API translation (Azure $10/M):**
- 12M words × 5 chars/word = 60M chars
- 60M × $10/M = **$600 one-time** (vs $1.8M manual)
- Monthly: 500 products = 3M chars = **$30/month** (vs $90K manual)

**Savings:** $1.799M year 1, $1.08M/year ongoing

**Payback:** Immediate (API integration takes 1-2 weeks, costs ~$5K dev time)

## Implementation Reality

### Realistic Timeline Expectations

| Phase | Timeline | What Happens |
|-------|----------|--------------|
| **Proof of concept** | 1-3 days | API key, test 100 sentences, evaluate quality |
| **Integration** | 1-2 weeks | Connect to your app, handle errors, glossary setup |
| **Quality validation** | 2-4 weeks | Test with real content, get native speaker feedback, iterate glossary |
| **Production rollout** | 1-2 weeks | Gradual rollout, monitoring, user feedback |
| **Total: MVP** | **6-10 weeks** | From decision to production |

**Common misconception:** "API integration takes 1 day" - technically true (API call works), but quality validation and glossary tuning take 90% of the time.

### Team Skill Requirements

**Minimum viable:**
- Backend engineer (API integration, error handling)
- Native speaker for target language (quality validation)

**Ideal:**
- Backend engineer (integration)
- Native speaker per target language (quality validation)
- Product manager (requirements, quality bar decisions)
- DevOps engineer (monitoring, cost tracking)

**You don't need:** Machine learning expertise (provider handles models)

### Common Pitfalls and Misconceptions

**Pitfall 1: "API quality is good enough, ship it"**
- **Reality**: Always test with native speakers before launch
- **Impact**: Cultural missteps (wrong formality, offensive translations) damage brand
- **Fix**: Budget 2-4 weeks for quality validation

**Pitfall 2: "One API call per sentence"**
- **Reality**: Context matters - translate paragraphs, not sentences
- **Impact**: APIs lose context across sentences ("he" vs "she", topic coherence)
- **Fix**: Send 2-3 sentences or full paragraphs per API call

**Pitfall 3: "Free tier covers us forever"**
- **Reality**: Azure 2M/mo is generous, but Google (500K) and Amazon (12-month expiration) fill up fast
- **Impact**: Surprise bills when volume exceeds free tier
- **Fix**: Monitor usage, set billing alerts, budget for paid tier

**Pitfall 4: "All APIs are the same quality"**
- **Reality**: Quality varies by language pair (Google strong for CJK, DeepL strong for European)
- **Impact**: Wrong provider choice = noticeably worse translations
- **Fix**: Test with your specific language pairs before committing

**Pitfall 5: "No formality control needed"**
- **Reality**: Japanese business communication REQUIRES formal language (keigo)
- **Impact**: Casual Japanese to business partners damages relationships
- **Fix**: Use DeepL or Amazon (only providers with Japanese formality control)

### First 90 Days: What to Expect

**Month 1: Integration and Testing**
- Week 1-2: API integration, basic error handling
- Week 3-4: Quality testing with native speakers, glossary creation
- **Expect**: 20-30% of translations need glossary tuning (brand names, product terms)

**Month 2: Soft Launch and Iteration**
- Week 5-6: Gradual rollout to 10% of users
- Week 7-8: Collect feedback, refine glossary, adjust quality thresholds
- **Expect**: 5-10% user complaints about translation quality (acceptable for soft launch)

**Month 3: Production and Optimization**
- Week 9-10: Full rollout to 100% of users
- Week 11-12: Cost optimization (monitor usage, adjust batching, evaluate providers)
- **Expect**: <2% user complaints, stable quality, cost within budget

**Success criteria at 90 days:**
- ✅ Translations live in production
- ✅ <5% user complaints about quality
- ✅ Cost predictable (within 20% of budget)
- ✅ Glossary covers 80%+ of domain-specific terms
- ✅ Native speakers rate quality as "acceptable" (7+/10)

---

## Summary

**Machine translation APIs solve high-volume translation needs** at 1000-10,000x lower cost than humans, with 60-80% of human quality.

**Choose APIs when:**
- Volume exceeds 100K words/month
- Real-time translation needed
- Budget for manual translation is prohibitive
- Content is "good enough" quality bar (not publication-critical)

**Avoid APIs when:**
- Legal/medical/literary content (certified humans required)
- Marketing slogans (cultural nuance critical)
- Low volume (<10K words/month - manual may be cheaper and better)

**For CJK translation specifically:**
- Google Cloud Translation: Best proven track record, premium pricing
- Azure Translator: Best cost ($10/M, 50% cheaper), competitive quality
- Amazon Translate: Best for AWS-native, unique customization (ACT)
- DeepL: Best Japanese formality control, premium quality, most expensive

**Implementation reality:** 6-10 weeks from decision to production, 20-30% initial translations need glossary tuning, expect 5-10% user complaints during soft launch.

**ROI:** At any meaningful volume (>10K words/month), APIs are dramatically cheaper (99%+ savings) than manual translation, with acceptable quality trade-offs for most use cases.
