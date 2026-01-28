# Use Case: Multi-Tenant SaaS Platform

**Scenario:** B2B SaaS product serving customers across China, Taiwan, and Hong Kong with user-generated content that must be displayed in the correct regional variant.

---

## Requirements

### Must-Have (Deal-Breakers)

1. **Regional Variant Accuracy** - Taiwan users see Taiwan vocabulary (軟體 not 軟件)
2. **Phrase-Level Conversion** - Idioms and multi-character terms convert correctly
3. **Production-Grade Stability** - Proven at scale, active maintenance
4. **Performance** - <50ms conversion for typical content (5,000 chars)
5. **Long-Term Viability** - Library won't be abandoned in next 3-5 years

### Nice-to-Have (Preferences)

6. **Custom Dictionaries** - Add company/product terminology
7. **Runtime Configuration** - No redeployment to add terms
8. **Strong Community** - Stack Overflow answers, GitHub activity
9. **Comprehensive Docs** - Examples for edge cases
10. **Type Safety** - TypeScript/Python type hints

### Constraints

- **Budget:** <$500/month compute cost (100M conversions/month)
- **Platform:** Docker on Kubernetes (Linux x86-64)
- **Team:** Python developers (prefer Python API)

---

## Library Evaluation

### OpenCC

#### Must-Haves
- ✅ **Regional variants:** s2tw, s2hk with full vocabulary support
- ✅ **Phrase-level:** Multi-pass algorithm handles idioms
- ✅ **Stability:** 10+ years, Wikipedia production use
- ✅ **Performance:** 1.5ms for 5,000 chars (well under 50ms)
- ✅ **Long-term:** 50+ contributors, active maintenance

#### Nice-to-Haves (8/10 points)
- ✅ **Custom dictionaries:** JSON/TXT format, runtime loading
- ✅ **Runtime config:** Can add terms without redeploy
- ✅ **Community:** 9,400 stars, large Stack Overflow presence
- ✅ **Documentation:** Excellent (multi-language examples)
- ⚠️ **Type safety:** Python type hints partial

#### Constraints
- ✅ **Budget:** $0.09 per million = ~$9/month (well under $500)
- ✅ **Platform:** Pre-built wheels for Linux x86-64
- ✅ **Team:** Python bindings available

**Fit Score:** **98/100** (60 must-haves + 38 nice-to-haves)

---

### zhconv-rs

#### Must-Haves
- ✅ **Regional variants:** zh-tw, zh-hk with full vocabulary
- ✅ **Phrase-level:** Aho-Corasick single-pass, phrase tables
- ⚠️ **Stability:** ~5 years, growing adoption BUT smaller community
- ✅ **Performance:** <1ms for 5,000 chars (excellent)
- ⚠️ **Long-term:** Active but newer project (medium risk)

#### Nice-to-Haves (6/10 points)
- ❌ **Custom dictionaries:** Compile-time only (must rebuild)
- ❌ **Runtime config:** No (rebuild required for new terms)
- ⚠️ **Community:** Smaller (fewer Stack Overflow answers)
- ⚠️ **Documentation:** Good but less comprehensive than OpenCC
- ✅ **Type safety:** Rust types exposed to Python

#### Constraints
- ✅ **Budget:** $0.03 per million = ~$3/month (excellent)
- ✅ **Platform:** Pre-built wheels for Linux x86-64
- ✅ **Team:** Python bindings available

**Fit Score:** **76/100** (50 must-haves (partial) + 26 nice-to-haves)

**Issue:** Can't add custom dictionaries at runtime = deal-breaker for multi-tenant SaaS with evolving terminology.

---

### HanziConv

#### Must-Haves
- ❌ **Regional variants:** NO Taiwan/HK vocabulary support
- ❌ **Phrase-level:** Character-only (5-15% error rate)
- ❌ **Stability:** 2 contributors, unclear maintenance
- ⚠️ **Performance:** 10-50ms for 5,000 chars (marginal)
- ❌ **Long-term:** High abandonment risk

#### Nice-to-Haves (2/10 points)
- ❌ **Custom dictionaries:** Not supported
- ❌ **Runtime config:** Not supported
- ❌ **Community:** Very small (189 stars)
- ⚠️ **Documentation:** Basic README only
- ❌ **Type safety:** No type hints

#### Constraints
- ⚠️ **Budget:** $1.50 per million = ~$150/month (acceptable but wasteful)
- ✅ **Platform:** Pure Python (universal)
- ✅ **Team:** Python native

**Fit Score:** **2/100** (0 must-haves + 2 nice-to-haves)

**Eliminated:** Fails regional variants (critical requirement).

---

## Recommendation

### Winner: **OpenCC**

**Rationale:**
1. **Only library meeting ALL must-haves** (98/100 fit score)
2. **Runtime custom dictionaries** critical for SaaS (product names, industry jargon evolve)
3. **Maturity reduces operational risk** (Wikipedia proven at billion+ conversions)
4. **Strong community** = faster issue resolution when edge cases arise

**Trade-off Accepted:**
- zhconv-rs is 3-10x faster, but OpenCC's 1.5ms is already fast enough (<50ms requirement)
- Runtime flexibility > raw performance for this use case

### Implementation Notes

```python
import opencc

# Initialize converters for each region (cache these)
converters = {
    'zh-tw': opencc.OpenCC('s2twp.json'),  # Taiwan + idioms
    'zh-hk': opencc.OpenCC('s2hk.json'),   # Hong Kong
    'zh-cn': opencc.OpenCC('s2t.json'),     # Generic Traditional
}

# Add custom dictionary for product names
custom_dict = {
    "MyProduct": "MyProduct",  # Don't convert
    "AcmeWidget": "AcmeWidget",  # Protect brand
}

# Convert based on user's region preference
def convert_content(text, user_region):
    converter = converters.get(user_region)
    if not converter:
        return text  # Fallback to original

    result = converter.convert(text)

    # Post-process to restore custom terms
    for original, protected in custom_dict.items():
        result = result.replace(converter.convert(original), protected)

    return result
```

### Cost Projection

- **Volume:** 100M conversions/month
- **Avg size:** 5,000 characters
- **Compute cost:** ~$9/month (OpenCC)
- **Engineering cost:** ~20 hours integration ($2,500 one-time)
- **Annual TCO:** $2,500 + $108 = **$2,608**

**ROI:** If correct regional variants reduce churn by even 1% for Chinese users (conservative), easily pays for itself.

---

## Alternative Scenario: If Runtime Dicts Not Needed

If your SaaS has stable terminology (no frequent custom term additions), **zhconv-rs becomes competitive**:

- **Fit Score:** 86/100 (if runtime config demoted to nice-to-have)
- **Cost:** $3/month vs $9/month (3x cheaper)
- **Performance:** 3-10x faster (better UX for high-volume users)

**Decision:** OpenCC for flexibility, zhconv-rs for performance if constraints allow.

---

**Use Case Winner:** **OpenCC** (98/100 fit, all must-haves met)
