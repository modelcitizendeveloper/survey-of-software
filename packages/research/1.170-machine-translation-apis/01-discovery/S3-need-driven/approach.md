# S3-Need-Driven Approach: Machine Translation APIs

## Objective
Evaluate machine translation APIs through the lens of specific CJK use cases, validating S1/S2 recommendations against real-world translation needs.

## Scope
- **3-5 concrete CJK translation scenarios**
- **All four providers**: Google, Azure, Amazon, DeepL
- **Time**: 1-2 hours per use case
- **Depth**: Requirements mapping, feature fit analysis, trade-off assessment

## Use Case Selection Criteria
- **Representative**: Cover common CJK translation needs
- **Differentiating**: Expose strengths/weaknesses of each provider
- **Testable**: Clear success criteria, verifiable outcomes
- **CJK-specific**: Highlight language-specific challenges

## Selected Use Cases

### 1. Japanese Business Communication (Formality-Critical)
**Scenario:** Japanese corporation with US subsidiary needs EN↔JA translation for:
- Internal memos (formal keigo)
- Customer emails (varying formality)
- HR policies (maximum formality)

**Key Requirements:**
- Formality control (keigo vs casual)
- Cultural appropriateness
- Consistent terminology (company names, titles)

**Expected Differentiator:** DeepL/Amazon formality control vs Google/Azure workarounds

### 2. E-commerce Product Localization (Volume + Quality)
**Scenario:** Online marketplace with 10K products needs:
- EN→ZH-CN, ZH-TW, JA, KO (4 targets = 40K translations)
- Product titles, descriptions, reviews
- Brand name preservation
- Monthly updates (new products)

**Key Requirements:**
- High volume (10K items × 4 languages = 40K translations/month)
- Cost efficiency
- Glossary for brand/product names
- Consistent quality across languages

**Expected Differentiator:** Azure cost advantage vs Google quality vs Amazon ACT

### 3. Technical Documentation Translation (Domain-Specific)
**Scenario:** Software company needs API documentation translated:
- EN→JA, ZH-CN (developer audience)
- 500 pages DOCX format
- Technical jargon (REST, JSON, OAuth, etc.)
- Code snippets preserved
- Quarterly updates

**Key Requirements:**
- Document format preservation
- Technical terminology consistency (glossary)
- Code snippet handling (no translation of code)
- Domain-specific accuracy

**Expected Differentiator:** DeepL document translation vs Google AutoML vs Amazon ACT

### 4. Content Localization for Marketing (European+CJK)
**Scenario:** German company expanding to Asia needs:
- DE/EN→JA, ZH-CN (blog posts, landing pages, social media)
- 20 articles/month (5K words each)
- Tone: casual, conversational
- Cultural adaptation (not just literal translation)

**Key Requirements:**
- Strong European language support (German)
- Good CJK quality
- Conversational tone (informal)
- Volume: 100K words/month = ~150K chars/month

**Expected Differentiator:** DeepL European strength vs pure CJK providers

### 5. Customer Support Chat Translation (Real-Time)
**Scenario:** SaaS company needs real-time translation for support chat:
- EN↔JA, ZH-CN, KO (bidirectional)
- Informal, conversational tone
- Low latency (<200ms)
- High throughput (100 concurrent chats)
- 1M chars/month

**Key Requirements:**
- Low latency (real-time chat)
- Informal tone (friendly, helpful)
- High reliability (SLA)
- Cost-effective at scale

**Expected Differentiator:** Latency + cost + quality balance

## Evaluation Framework

For each use case, assess:

### 1. Requirements Fit
- ✅ **Full support**: Feature available, works well
- ⚠️ **Partial support**: Feature available but limited or workaround needed
- ❌ **No support**: Feature not available, significant gap

### 2. Cost Analysis
- Calculate actual cost for use case volume
- Include hidden costs (custom models, hosting, document fees)
- Compare break-even points

### 3. Integration Complexity
- **Low**: Simple API call, standard SDK
- **Medium**: Glossary setup, batch processing, IAM configuration
- **High**: Custom model training, complex workflows

### 4. Quality Expectations
- **Critical**: Quality issues block adoption
- **Important**: Quality affects user satisfaction but not blocking
- **Nice-to-have**: Better quality is bonus, acceptable quality is fine

### 5. Trade-offs
- What you gain by choosing this provider
- What you give up compared to alternatives
- Deal-breakers if any

## Method

For each use case:
1. **Define requirements** (features, volume, budget, quality bar)
2. **Map to provider capabilities** (S1/S2 findings)
3. **Assess fit** (full/partial/no support)
4. **Calculate costs** (realistic usage, including hidden costs)
5. **Identify trade-offs** (pros/cons per provider)
6. **Recommend** (best fit, alternatives, red flags)

## Constraints
- No hands-on testing (rely on documented capabilities)
- No live API calls (cost prohibitive for S3)
- Focus on feature fit and cost analysis
- Defer actual quality testing to production pilots

## Deliverables
- `use-case-*.md` files (one per scenario)
- `recommendation.md` (synthesized guidance based on real needs)
