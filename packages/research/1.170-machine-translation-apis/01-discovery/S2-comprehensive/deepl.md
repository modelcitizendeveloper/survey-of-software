# DeepL API (S2-Comprehensive)

*Extends S1 findings with deep feature analysis and integration considerations*

## API Architecture

### Single Version Approach
- Unified API (no v2/v3 split like Google)
- RESTful design with JSON
- Simple authentication (API key)
- Focus on developer simplicity

### Authentication
- **API Key**: Simple header-based auth
- Free vs Pro keys (different endpoints)
- No OAuth complexity
- Suitable for both client and server-side

### Request Format
- Standard HTTP POST with JSON
- Simple parameters (text, target_lang, source_lang, formality, glossary_id)
- Tag handling for HTML/XML preservation
- Split sentences parameter for better context

**Sources:**
- [OpenAPI spec for text translation](https://developers.deepl.com/docs/api-reference/translate/openapi-spec-for-text-translation)
- [DeepL API products](https://www.deepl.com/en/products/api)

## Advanced Features

### 1. Formality Control
**Purpose:** Control formal vs informal language in translations

**Availability (2026):**
- **Japanese (JA)**: ✅ Supported (text and document translation)
- **Chinese (ZH)**: Not documented (likely no support)
- **Korean (KO)**: Not documented (likely no support)
- **European languages**: Extensive support (DE, FR, ES, IT, PT, RU, etc.)

**API Parameter:**
```
formality: "default" | "more" | "less" | "prefer_more" | "prefer_less"
```

**CJK Implications:**
- **Japanese**: Keigo (敬語) vs casual speech - critical for business contexts
- **Chinese/Korean**: Formality exists but not API-supported
- **Workaround**: Use glossaries to enforce formal terminology

**Use Cases:**
- Business communication (EN→JA formal)
- Customer support (informal, friendly tone)
- Legal/medical documents (maximum formality)

**Sources:**
- [Roadmap and release notes](https://developers.deepl.com/docs/resources/roadmap-and-release-notes)
- [DeepL API Documentation](https://developers.deepl.com/docs)

### 2. Glossaries
**Purpose:** Enforce consistent terminology, preserve brand names

**Recent Improvements (2026):**
- **Edit glossaries**: Modify existing glossaries without recreation
- **Multilingual glossaries**: One glossary for multiple language pairs
- **Expanded CJK support**: Chinese (ZH) added as glossary language
- **55 language pairs**: Up from 28 (PT, RU, ZH added)

**Format:**
- TSV (tab-separated values)
- Source term → Target term mapping
- UTF-8 encoding
- Bidirectional entries

**Limitations:**
- Not all language pairs supported
- Beta languages don't support glossaries
- Size limits (check documentation for current max)

**CJK Capabilities:**
- ✅ **Chinese (ZH)**: Glossary support added
- ✅ **Japanese (JA)**: Supported (inferred from expanded support)
- ❓ **Korean (KO)**: Status unclear, likely supported

**Use Cases:**
- Technical documentation (consistent terminology)
- Brand name preservation across scripts
- Product names (e.g., "iPhone" → "iPhone", not translated)
- Domain-specific jargon

**Sources:**
- [Roadmap and release notes](https://developers.deepl.com/docs/resources/roadmap-and-release-notes)
- [DeepL glossary features](https://www.deepl.com/en/features/glossary)

### 3. Document Translation
**Purpose:** Translate formatted documents while preserving layout

**Supported Formats:**
- **Microsoft Office**: DOCX, PPTX, XLSX
- **Web**: HTML, HTM
- **Documents**: PDF, TXT
- **Images (Beta)**: JPEG, PNG (OCR + translation)

**Features:**
- **Original formatting preserved**: Fonts, layout, tables
- **Bulk processing**: Batch translation of multiple files
- **Multiple target languages**: One source → many targets simultaneously
- **Tag handling**: HTML/XML tags preserved
- **Formality support**: Works in document mode (including JA)

**API Workflow:**
1. Upload document (multipart/form-data)
2. Receive document_id and status URL
3. Poll status endpoint
4. Download translated document when complete

**Pricing:** Charged by character count in source document (same $25/M rate)

**CJK Considerations:**
- Font handling for CJK characters in PDFs/DOCX
- Image OCR quality for CJK (Beta status, watch for issues)
- Layout preservation for vertical text (uncommon but exists)
- Character encoding preserved

**Sources:**
- [DeepL API products](https://www.deepl.com/en/products/api)
- [Roadmap and release notes](https://developers.deepl.com/docs/resources/roadmap-and-release-notes)

### 4. Translation Quality: Next-Gen LLM

**2025 Launch:**
- Next-generation LLM model for select languages
- **1.7x improvement** over previous DeepL model (linguist-verified)
- **Supported CJK languages**: Japanese (JA), Simplified Chinese (ZH-CN)

**Quality Claims:**
- Blind tests with professional linguists
- Measurable BLEU score improvements
- Better context handling
- More natural phrasing

**CJK Impact:**
- EN↔JA: Significant quality gains
- EN↔ZH-CN: Significant quality gains
- Traditional Chinese (ZH-TW): Not mentioned in LLM improvements
- Korean (KO): Not mentioned in LLM improvements

**Competitive Position:**
- Historically strongest in European languages
- CJK quality now competitive with Google/Azure (per claims)
- Voice translation added for Mandarin/Japanese/Korean

**Sources:**
- [S1-rapid research findings]
- [DeepL next-gen LLM announcement](https://www.prnewswire.com/news-releases/deepl-bolsters-api-with-next-gen-llm-model-and-write-functionality-302360279.html)

### 5. Features NOT Available

❌ **Batch translation**: No asynchronous bulk text translation (unlike Google Cloud Storage integration)
❌ **Custom model training**: No AutoML equivalent (glossaries only)
❌ **Region selection**: No data residency control
❌ **gRPC API**: REST/JSON only (no binary protocol option)

**Impact:**
- Large corpus translation less convenient (must iterate)
- No domain-specific model training (rely on next-gen LLM quality)
- Compliance-sensitive use cases may have limitations

## Integration & Developer Experience

### Official SDKs
**Languages:**
- **Python** ([deepl-python](https://github.com/DeepLcom/deepl-python))
- **Node.js** ([deepl-node](https://github.com/DeepLcom/deepl-node))
- **.NET** ([deepl-dotnet](https://github.com/DeepLcom/deepl-dotnet))

**Quality:**
- Mature, actively maintained
- Consistent API across languages
- Formality, glossary, document support in all SDKs
- Good documentation with examples

**Community SDKs:** Unofficial libraries for Go, Ruby, PHP (community-maintained)

### Code Example (Python)
```python
import deepl

translator = deepl.Translator("YOUR_AUTH_KEY")

# Text translation with formality
result = translator.translate_text(
    "Hello, how are you?",
    target_lang="JA",
    formality="more"  # Formal Japanese (keigo)
)
print(result.text)

# With glossary
glossary_id = "your-glossary-id"
result = translator.translate_text(
    "Technical term example",
    target_lang="ZH",
    glossary=glossary_id
)
```

### Error Handling
- HTTP status codes (400, 403, 429, 456, 503)
- **429**: Quota exceeded (character limit)
- **456**: Quota exceeded (document limit)
- **503**: Resource temporarily unavailable
- Clear error messages in JSON response

### Rate Limits
- Character limit per month (based on subscription)
- No documented per-second rate limits
- Document translation limits separate from text
- Free tier: 500K chars/month
- Pro tier: Based on purchased characters

**Sources:**
- [DeepL Python library PyPI](https://pypi.org/project/deepl/1.3.0/)
- [DeepL GitHub repositories](https://github.com/DeepLcom)

## Performance & Scalability

### Latency
- Generally fast (no specific SLA published)
- Comparable to Google NMT (~100-200ms for typical requests)
- Next-gen LLM may have slightly higher latency
- Document translation: Depends on file size (async)

### Availability
- No published SLA (unlike Google 99.5%)
- Enterprise support available (Pro subscriptions)
- Generally reliable service

### Monitoring
- No native cloud monitoring integration (unlike GCP/Azure/AWS)
- Usage tracking in DeepL account dashboard
- API returns character count per request (for tracking)

**Limitations:**
- Less transparency than cloud providers
- No CloudWatch/Stackdriver equivalent
- Must build custom monitoring

## CJK-Specific Deep Dive

### Character Encoding
- UTF-8 standard
- Full Unicode support (including rare characters)
- No BOM issues reported

### Formality Handling
| Language | Formality Support | Notes |
|----------|-------------------|-------|
| **Japanese** | ✅ Yes | Keigo (formal) vs casual - critical feature |
| **Chinese** | ❌ No | Use glossaries for formal terminology |
| **Korean** | ❌ No | Use glossaries for formal terminology |

### Glossary Support for CJK
- ✅ **Chinese (ZH)**: Added 2026 (expanded from 28 to 55 pairs)
- ✅ **Japanese (JA)**: Supported
- ✅ **Multilingual glossaries**: One glossary for multiple pairs

### Quality for CJK (Next-Gen LLM)
- ✅ **Japanese**: 1.7x improvement over old model
- ✅ **Simplified Chinese**: 1.7x improvement
- ❓ **Traditional Chinese**: Not mentioned in LLM updates
- ❓ **Korean**: Not mentioned in LLM updates

### Voice Translation (Bonus)
- Mandarin Chinese: ✅ Supported
- Japanese: ✅ Supported
- Korean: ✅ Supported
- (Not part of API, but shows CJK focus)

## Operational Considerations

### Security
- TLS encryption in transit
- API key authentication (simpler than OAuth, less granular)
- No documented compliance certifications (SOC 2, HIPAA)
- Data handling: EU-based (GDPR-compliant)

### Cost Tracking
- Character count returned in API responses
- Account dashboard for usage monitoring
- No tagging/labeling for cost allocation
- Must implement custom tracking

### Logging & Audit
- No built-in audit logs (unlike GCP Cloud Audit Logs)
- Must log API calls client-side
- No request tracing integration

**Enterprise Gap:**
Compared to GCP/Azure/AWS, DeepL lacks enterprise operational features (detailed audit, compliance certifications, granular IAM).

## Integration Complexity

### Easy Integration
✅ Simple API (REST + JSON, no gRPC complexity)
✅ Straightforward auth (API key)
✅ Excellent SDKs (Python, Node.js, .NET)
✅ Good documentation with examples
✅ Generous free tier for testing (500K/mo)

### Moderate Complexity
⚠️ Glossary management (TSV format, upload via API)
⚠️ Document translation (async workflow, polling)
⚠️ No batch text processing (must iterate for large corpora)

### Low Complexity (Fewer Features)
✅ No custom model training (simpler but less customizable)
✅ No multi-region deployment (single service endpoint)
✅ No VPC integration (public API only)

**Verdict:** Easiest to integrate among the four providers - simplicity is a feature.

## S2 Recommendation Updates

### When DeepL is the Best Choice

**Strengths:**
- **Formality control for Japanese** (unique among providers for JA)
- **Next-gen LLM quality** for EN↔JA, EN↔ZH-CN (1.7x improvement)
- **Simple integration** (least complex API)
- **European ↔ CJK bridge** (strongest European language quality)
- **Document translation** with good formatting preservation
- **Glossaries for Chinese** (added 2026)

**Best For:**
- **Japanese business communication** (formality control is critical)
- **European + CJK projects** (leverages DeepL's European strength)
- **Quality-sensitive EN↔JA/ZH-CN** (next-gen LLM gains)
- **Simple integration needs** (no enterprise complexity required)
- **Document translation workflows** (DOCX, PDF, PPTX preservation)

### When to Consider Alternatives

**Choose Google if:**
- Need batch processing (Cloud Storage integration)
- Want custom model training (AutoML)
- Require enterprise features (audit logs, SLAs, compliance)
- Already on GCP ecosystem

**Choose Azure if:**
- Cost is primary concern ($10/M vs DeepL $25/M)
- Need larger permanent free tier (2M vs 500K)
- Already on Azure ecosystem

**Choose Amazon if:**
- AWS-native stack (S3, Lambda)
- Need Active Custom Translation
- Cost-conscious ($15/M vs DeepL $25/M)

### DeepL's Trade-offs

**Premium Pricing:**
- $25/M (most expensive)
- Base fee $5.49/mo adds up at low volume
- 25% more than Google, 2.5x more than Azure

**Missing Enterprise Features:**
- No compliance certifications (SOC 2, HIPAA)
- No audit logging
- No SLA published
- No cloud monitoring integration

**Feature Gaps:**
- No batch text processing
- No custom model training
- No Chinese/Korean formality control
- No region selection

**Verdict:** Pay premium for:
1. Japanese formality control
2. Next-gen LLM quality (EN↔JA/ZH-CN)
3. European language strength
4. Simplicity of integration

Worth it for **Japanese business applications** and **quality-sensitive European↔CJK projects**. Not worth it for **pure CJK↔CJK**, **high-volume cost-sensitive projects**, or **enterprise compliance requirements**.

## Summary: DeepL's Position in Market

**Market Position:** Quality leader for European languages, strong and improving for select CJK pairs, premium pricing

**Key Differentiators:**
- **Formality control for Japanese** (unique capability)
- **Next-gen LLM for JA/ZH-CN** (verified 1.7x improvement)
- **Simplest API** (lowest integration complexity)
- **European language strength** (best for multilingual projects including CJK)

**Best Match:**
- Japanese business communication (formality is critical)
- European HQ with Asian branches (EN/DE/FR ↔ JA/ZH)
- Quality > cost priorities
- Small to medium teams (simplicity advantage)

**Poor Match:**
- Pure CJK↔CJK translation (no unique advantage)
- High-volume cost-sensitive (Azure is 2.5x cheaper)
- Enterprise compliance requirements (missing certifications)
- Complex workflows (no batch processing, custom models)
