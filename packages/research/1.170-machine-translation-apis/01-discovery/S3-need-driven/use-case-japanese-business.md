# Use Case: Japanese Business Communication (Formality-Critical)

## Scenario
Japanese corporation with US subsidiary needs EN↔JA translation for formal business communication.

**Content Types:**
- Internal memos (formal keigo required)
- Customer emails (varying formality based on relationship)
- HR policies (maximum formality)
- Executive announcements (very formal)

**Volume:** ~500K chars/month (50-100 documents)

**Quality Bar:** **Critical** - Inappropriate formality can damage business relationships

## Requirements

| Requirement | Priority | Notes |
|-------------|----------|-------|
| **Formality control (keigo)** | ✅ Critical | Must support formal/informal Japanese |
| **Glossary (company terms)** | ✅ Critical | Company names, titles, product names |
| **Document translation** | ⚠️ Important | DOCX format preferred, plain text acceptable |
| **Low latency** | ⚠️ Important | <500ms for interactive use |
| **Cost-effective** | Nice-to-have | Budget is secondary to quality |

## Provider Assessment

### DeepL
**Formality Support:** ✅ **Yes** - Full keigo support for Japanese

**Fit:**
- ✅ Japanese formality parameter (`formality: "more"` for keigo)
- ✅ Document translation (DOCX support)
- ✅ Glossary support (multilingual glossaries, 2026)
- ✅ Next-gen LLM (1.7x improvement for EN↔JA, verified)
- ✅ Simple integration (easy to deploy quickly)

**Cost (500K chars/month):**
- First 500K: **Free** (covered by free tier)
- Beyond: $25/M → negligible for this volume
- **Monthly: $0-5.49** (base fee only at low volume)

**Trade-offs:**
- ✅ Best Japanese formality control
- ✅ Verified quality improvement (1.7x)
- ❌ Most expensive if volume grows
- ❌ No enterprise compliance (if needed)

**Verdict:** ⭐⭐⭐⭐⭐ **Best fit** - Formality is critical, quality is proven

---

### Amazon Translate
**Formality Support:** ✅ **Yes** - Japanese formality via Settings parameter

**Fit:**
- ✅ Japanese formality (`Settings: { Formality: "FORMAL" }`)
- ✅ Custom terminology (10K terms, no extra cost)
- ✅ Active Custom Translation (if domain-specific adaptation needed)
- ❌ No document translation (DOCX → must extract text first)
- ⚠️ AWS ecosystem (good if already on AWS, overhead if not)

**Cost (500K chars/month):**
- First 2M: **Free** (12-month free tier)
- Beyond: $15/M
- **Year 1: $0/month**
- **Year 2+: $7.50/month**

**Trade-offs:**
- ✅ Japanese formality support
- ✅ Free for first year (2M/mo covers this use case)
- ✅ ACT for domain-specific customization
- ❌ No document translation (extra processing needed)
- ❌ Free tier expires (vs DeepL permanent)
- ⚠️ AWS setup overhead if not already on AWS

**Verdict:** ⭐⭐⭐⭐ **Strong alternative** - Good fit if AWS-native, missing document translation

---

### Google Cloud Translation
**Formality Support:** ❌ **No** - No built-in formality control

**Fit:**
- ❌ No formality parameter
- ⚠️ Glossary workaround (define formal terms, but not comprehensive)
- ✅ Document translation (v3 Advanced, $0.08/page)
- ✅ Translation LLM (higher quality option)
- ✅ Longest CJK track record

**Cost (500K chars/month):**
- First 500K: **Free** (permanent free tier)
- Beyond: $20/M
- **Monthly: $0** (covered by free tier)

**Workarounds for Formality:**
- Custom glossary with formal Japanese terms
- Adaptive Translation ($50/M) with formal reference translations
- AutoML custom model trained on formal Japanese corpus (expensive, complex)

**Trade-offs:**
- ✅ Highest baseline Japanese quality (longest track record)
- ✅ Free at this volume (500K free tier)
- ❌ **No formality control** (critical gap)
- ⚠️ Workarounds are complex and expensive

**Verdict:** ⭐⭐ **Not recommended** - Missing critical feature (formality)

---

### Azure Translator
**Formality Support:** ❌ **No** - No built-in formality control

**Fit:**
- ❌ No formality parameter
- ⚠️ Custom model workaround (train on formal corpus, $10/mo hosting)
- ✅ Document translation (DOCX, PDF support)
- ✅ Direct JA↔EN translation
- ✅ 2M free tier (4x larger than Google)

**Cost (500K chars/month):**
- First 2M: **Free** (permanent free tier)
- Beyond: $10/M
- **Monthly: $0** (covered by free tier)

**Workarounds for Formality:**
- Train custom model on formal Japanese corpus
- Hosting fee: $10/month per model
- Requires substantial training data

**Trade-offs:**
- ✅ Free at this volume (2M free tier)
- ✅ Cheapest if volume grows
- ❌ **No formality control** (critical gap)
- ⚠️ Custom model workaround is expensive and complex

**Verdict:** ⭐⭐ **Not recommended** - Missing critical feature (formality)

## Cost Comparison (500K chars/month)

| Provider | Monthly Cost | Annual Cost | Notes |
|----------|--------------|-------------|-------|
| **Azure** | **$0** | **$0** | 2M free tier covers use case |
| **Google** | **$0** | **$0** | 500K free tier covers use case |
| **Amazon** | **$0** | **$0** | 2M free tier (year 1 only) |
| **DeepL** | **$5.49** | **$66** | Base fee (within 500K free tier) |

**Cost is NOT a differentiator at this volume** - all providers are free or nearly free.

## Decision Matrix

| Provider | Formality | Quality | Cost | Ease | Verdict |
|----------|-----------|---------|------|------|---------|
| **DeepL** | ✅ Native | ⭐⭐⭐⭐⭐ | $5.49/mo | Easy | ⭐⭐⭐⭐⭐ **Best** |
| **Amazon** | ✅ Native | ⭐⭐⭐⭐ | $0 (Y1) | Medium | ⭐⭐⭐⭐ **Good** |
| **Google** | ❌ Workaround | ⭐⭐⭐⭐⭐ | $0 | Hard | ⭐⭐ **No** |
| **Azure** | ❌ Workaround | ⭐⭐⭐⭐ | $0 | Hard | ⭐⭐ **No** |

## Recommendation

### Primary: **DeepL**
**Why:**
- ✅ Native Japanese formality control (critical requirement)
- ✅ Verified 1.7x quality improvement for EN↔JA
- ✅ Document translation (DOCX support)
- ✅ Simple integration (fastest time-to-value)
- ✅ Glossary support for company terms
- ✅ Cost is negligible at this volume ($5.49/mo base fee)

**When to reconsider:**
- Volume grows significantly (>10M chars/month) → Cost adds up

### Alternative: **Amazon Translate**
**Why:**
- ✅ Japanese formality support
- ✅ Free for first year (2M/mo tier)
- ✅ Custom terminology (company terms, no extra cost)
- ✅ ACT if domain-specific adaptation needed

**Trade-offs:**
- ❌ No document translation (extra processing step)
- ⚠️ AWS setup overhead if not already on AWS
- ⚠️ Free tier expires after 12 months

### Not Recommended: **Google** or **Azure**
**Why:**
- ❌ No formality control (critical gap)
- ⚠️ Workarounds are complex, expensive, and incomplete
- ✅ Baseline quality is good, but formality is essential for business Japanese

## Implementation Strategy

### Phase 1: Deploy DeepL (Week 1)
1. Sign up for DeepL API Free tier
2. Create glossary for company terms
3. Integrate formality parameter into translation workflow
4. Test with sample internal memos (formal)
5. Validate quality with native Japanese speakers

### Phase 2: Production Rollout (Week 2-3)
1. Integrate into email/document workflows
2. Train users on formality levels (when to use formal vs informal)
3. Monitor usage and quality feedback
4. Track costs (should stay at $5.49/mo base fee)

### Phase 3: Optimization (Month 2+)
1. Refine glossary based on feedback
2. Evaluate Amazon Translate as backup (if AWS migration happens)
3. If volume grows >10M/month, reassess cost (consider Amazon/Azure)

## Red Flags / Deal-Breakers

### Google/Azure without Formality Control
- **Risk:** Inappropriate formality damages business relationships
- **Impact:** HIGH - Cultural misstep in Japanese business communication
- **Workaround cost:** High (custom models, complex glossaries)
- **Workaround effectiveness:** Partial at best

### Verdict: **Formality control is non-negotiable for Japanese business communication. Choose DeepL or Amazon only.**

## Success Criteria

After 3 months:
- ✅ Zero formality-related complaints from Japanese team
- ✅ Consistent company terminology (via glossary)
- ✅ <5 minutes translation time per document
- ✅ Cost under $20/month (should be $5.49 for DeepL)
- ✅ Native speakers rate quality as "business-appropriate"
