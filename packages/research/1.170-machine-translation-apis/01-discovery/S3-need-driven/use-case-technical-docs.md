# Use Case: Technical Documentation Translation (Format + Terminology)

## Scenario
Software company needs API documentation translated for developer audience in Asia.

**Content Types:**
- API reference documentation (DOCX format, 500 pages)
- Code examples (must preserve syntax, not translate)
- Technical terminology (REST, JSON, OAuth, webhook, etc.)
- Quarterly updates (50-100 pages changes)

**Target Languages:** EN→JA, ZH-CN (developer-focused markets)

**Volume:**
- Initial: 500 pages × 1,000 chars/page × 2 languages = **1M chars**
- Quarterly updates: 75 pages avg × 1,000 chars × 2 languages = **150K chars/quarter** = **50K chars/month avg**
- Annual: 1M + (150K × 4) = **1.6M chars/year**

**Quality Bar:** **Critical** - Technical inaccuracies confuse developers, damage trust

## Requirements

| Requirement | Priority | Notes |
|-------------|----------|-------|
| **Document format preservation** | ✅ Critical | DOCX with code blocks, tables, formatting |
| **Code snippet handling** | ✅ Critical | Do NOT translate code, only comments |
| **Technical terminology** | ✅ Critical | Consistent translation of tech terms |
| **Glossary (200+ terms)** | ✅ Critical | REST, JSON, API, webhook, endpoint, etc. |
| **Quarterly batch processing** | ⚠️ Important | Async acceptable, not time-sensitive |

## Provider Assessment

### Google Cloud Translation (v3 Advanced)
**Fit:**
- ✅ Document translation (DOCX native support)
- ✅ Glossary support (unlimited terms)
- ✅ Tag handling (preserve XML/HTML in code examples)
- ✅ Batch processing (Cloud Storage integration)
- ✅ Translation LLM (higher quality for technical content)
- ✅ Longest CJK track record

**Cost Analysis:**
- **Document pricing:** $0.08/page
- **Initial:** 500 pages × 2 languages × $0.08 = **$80**
- **Quarterly:** 75 pages × 2 languages × $0.08 = **$12/quarter**
- **Annual:** $80 + ($12 × 4) = **$128**

**OR Text-based pricing:**
- **Initial:** 1M chars × $20/M = **$20**
- **Quarterly:** 150K chars × $20/M = **$3/quarter**
- **Annual:** $20 + ($3 × 4) = **$32**

**Best: Text-based** ($32 vs $128 document pricing)

**Trade-offs:**
- ✅ Native DOCX support (preserves formatting, code blocks)
- ✅ Unlimited glossary (200+ tech terms, no problem)
- ✅ Proven technical content quality
- ✅ Translation LLM for complex technical language
- ⚠️ Premium pricing ($20/M vs Azure $10/M)
- ✅ Covered by 500K free tier initially = **$10 annual** (initial exceeds free tier by 500K)

**Verdict:** ⭐⭐⭐⭐⭐ **Best fit** - Technical quality and DOCX support justify premium

---

### DeepL
**Fit:**
- ✅ Document translation (DOCX, best formatting preservation reported)
- ✅ Glossary support (multilingual, 55 pairs)
- ✅ Next-gen LLM (1.7x improvement for JA/ZH-CN)
- ✅ Simple integration
- ❌ No batch text processing (batch document API exists)
- ⚠️ Premium pricing

**Cost Analysis:**
- **Initial:** (1M - 500K free) × $25/M + $5.49 = **$18**
- **Quarterly:** (150K - 125K free) × $25/M + $5.49 = **$6.12/quarter**
- **Annual:** $18 + ($6.12 × 4) = **$42.48**

**Trade-offs:**
- ✅ **Best document formatting** preservation (reported by users)
- ✅ Next-gen LLM quality (1.7x for JA/ZH-CN)
- ✅ Simple API (easy integration)
- ✅ Glossary for tech terms
- ⚠️ Most expensive ($42.48 vs Google $32 vs Azure $10)
- ⚠️ Smaller free tier (500K vs Azure 2M)

**Verdict:** ⭐⭐⭐⭐⭐ **Strong alternative** - Best formatting, premium quality, competitive cost for docs

---

### Azure Translator
**Fit:**
- ✅ Document translation (DOCX, PDF support)
- ✅ Glossary support
- ✅ Batch processing (Blob Storage)
- ✅ **Lowest cost** ($10/M)
- ✅ 2M free tier (covers all usage for year 1+)
- ⚠️ Fewer public technical content benchmarks

**Cost Analysis:**
- **Initial:** Covered by 2M free tier = **$0**
- **Monthly (50K avg):** Covered by 2M free tier = **$0**
- **Annual:** **$0** (entire use case covered by free tier)

**Trade-offs:**
- ✅ **Free** (2M free tier covers 1.6M/year usage)
- ✅ DOCX document translation
- ✅ Glossary for tech terms
- ✅ Azure ecosystem (if already on Azure)
- ⚠️ Less proven for technical content (fewer benchmarks)
- ⚠️ Document formatting may be less polished than DeepL

**Verdict:** ⭐⭐⭐⭐ **Best value** - Free tier covers usage, competitive quality

---

### Amazon Translate
**Fit:**
- ❌ **No document translation** (text-only)
- ✅ Custom terminology (10K terms, no extra cost)
- ✅ Active Custom Translation (for technical jargon)
- ✅ Batch processing (S3)
- ⚠️ Requires text extraction from DOCX (pre-processing overhead)

**Cost Analysis:**
- **Initial:** (1M - 2M free) = **$0** (covered by free tier year 1)
- **Quarterly:** Covered by 2M free tier = **$0**
- **Annual Year 1:** **$0**
- **Annual Year 2+:** 1.6M × $15/M = **$24**

**Trade-offs:**
- ✅ Free year 1 (2M/mo covers usage)
- ✅ ACT for technical terminology customization
- ❌ **No DOCX support** (must extract text → translate → re-format)
- ⚠️ Re-formatting overhead (lose formatting, code blocks)
- ❌ **Critical gap**: Document workflows broken without native DOCX

**Verdict:** ⭐⭐ **Not recommended** - Missing critical feature (document translation)

## Cost Comparison (Annual)

| Provider | Cost (Annual) | Document Support | Quality | Verdict |
|----------|---------------|------------------|---------|---------|
| **Azure** | **$0** | ✅ DOCX | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ **Best value** |
| **Google** | **$32** | ✅ DOCX | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ **Best quality** |
| **DeepL** | **$42** | ✅ DOCX (best) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ **Good** |
| **Amazon** | **$0** (Y1) | ❌ **No DOCX** | ⭐⭐⭐⭐ | ⭐⭐ **No** |

**Azure is free** (covered by 2M free tier), **Google is $32** (proven quality), **DeepL is $42** (best formatting).

## Decision Matrix

| Provider | Document | Glossary | Quality | Cost | Verdict |
|----------|----------|----------|---------|------|---------|
| **Google** | ✅ Native | ✅ Unlimited | ⭐⭐⭐⭐⭐ | $32/year | ⭐⭐⭐⭐⭐ **Best** |
| **Azure** | ✅ Native | ✅ Yes | ⭐⭐⭐⭐ | **$0**/year | ⭐⭐⭐⭐ **Value** |
| **DeepL** | ✅ Best | ✅ Yes | ⭐⭐⭐⭐⭐ | $42/year | ⭐⭐⭐⭐ **Good** |
| **Amazon** | ❌ None | ✅ Yes | ⭐⭐⭐⭐ | $0 (Y1) | ⭐⭐ **No** |

## Recommendation

### Primary: **Google Cloud Translation (v3 Advanced)**
**Why:**
- ✅ Native DOCX support (preserves code blocks, tables, formatting)
- ✅ Unlimited glossary (200+ tech terms, no problem)
- ✅ **Proven technical content quality** (longest CJK track record)
- ✅ Translation LLM option (higher quality for complex technical language)
- ✅ Tag handling (preserves XML/HTML in code examples)
- ✅ Batch processing (Cloud Storage integration for quarterly updates)
- ✅ Cost is negligible ($32/year) for critical developer-facing content

**When to reconsider:**
- Cost is absolutely critical (Azure is free)
- Document formatting issues detected (DeepL may be better)

### Alternative 1: **Azure Translator**
**Why:**
- ✅ **Free** (2M free tier covers 1.6M/year usage permanently)
- ✅ DOCX document translation
- ✅ Glossary for tech terms
- ✅ Competitive quality

**Trade-offs:**
- ⚠️ Less proven for technical content (fewer public benchmarks)
- ⚠️ Document formatting may not be as polished as Google/DeepL
- ✅ **Zero cost** is compelling for budget-conscious teams

**Verdict:** Excellent value proposition - free tier covers entire use case

### Alternative 2: **DeepL**
**Why:**
- ✅ **Best document formatting** preservation (user reports)
- ✅ Next-gen LLM (1.7x quality for JA/ZH-CN)
- ✅ Glossary for tech terms
- ✅ Simple integration

**Trade-offs:**
- ⚠️ Most expensive ($42/year vs Azure $0, Google $32)
- ⚠️ Premium not strongly justified for this use case

**Verdict:** Good quality but not enough differentiation to justify premium over Google

### Not Recommended: **Amazon Translate**
**Why:**
- ❌ **No document translation** (text-only)
- ❌ Requires manual text extraction + re-formatting (significant overhead)
- ❌ **Critical workflow gap** for technical documentation

## Implementation Strategy

### Phase 1: Initial Translation (Month 1)

**Using Google (recommended):**
1. Set up Google Cloud Translation v3 Advanced
2. Create glossary with 200+ technical terms
   - REST API, JSON, OAuth, webhook, endpoint, etc.
   - Include code-related terms that should NOT be translated
3. Upload 500-page DOCX to Cloud Storage
4. Submit document translation job
5. Review formatting preservation (code blocks, tables)
6. **Cost: $20** (text-based, 1M chars after free tier)

**Alternative using Azure (free):**
1. Set up Azure Translator
2. Create glossary with technical terms
3. Upload DOCX to Blob Storage
4. Submit batch translation job
5. Compare formatting quality with Google sample
6. **Cost: $0** (covered by 2M free tier)

### Phase 2: Quality Validation (Month 2)
1. Developer review of technical accuracy
2. Test code examples (ensure NOT translated)
3. Verify terminology consistency (glossary effectiveness)
4. Check formatting preservation (code blocks, tables)
5. Iterate glossary based on feedback

### Phase 3: Quarterly Updates (Ongoing)
1. Automate: DOCX update → Cloud Storage → Translation → Review
2. Maintain glossary (add new technical terms)
3. Monitor costs (should stay <$10/quarter)
4. Developer sign-off before publishing

## Break-Even Analysis

| Scenario | Cost Comparison (Annual) | Quality Trade-off |
|----------|-------------------------|-------------------|
| Azure (free) vs Google ($32) | **Save $32/year** | Accept slightly lower quality? |
| Azure (free) vs DeepL ($42) | **Save $42/year** | Accept possibly worse formatting? |
| Google ($32) vs DeepL ($42) | **Save $10/year** | Accept possibly worse formatting? |

**For technical documentation ($32-42/year is negligible):**
- Quality and developer trust are paramount
- Formatting preservation is critical (code blocks, tables)
- Cost savings of $32/year not material for software company

**Verdict:** **Choose Google** for proven technical quality unless:
- Budget is extremely tight → Azure (free)
- Formatting issues detected → DeepL (best formatting reported)

## Success Criteria

After 6 months:
- ✅ 500-page initial docs translated and published
- ✅ 2 quarterly updates completed (150 pages)
- ✅ Zero developer complaints about technical inaccuracies
- ✅ Code examples preserved correctly (not translated)
- ✅ Technical terminology consistent (via glossary)
- ✅ Cost under $50 total (well within budget)
- ✅ Formatting preserved (code blocks, tables, styling)
