# S3 Scenario 6: Multilingual International Teams - Planning Notes

**Created**: Nov 24, 2025
**Purpose**: Plan the multilingual scenario for S3 Need-Driven analysis

---

## Scenario Overview

**Use Case**: International teams with non-English meetings, multilingual customer support, global content localization

**Key Requirements**:
- Transcribe meetings in native language (Spanish, French, German, Mandarin, etc.)
- High accuracy on non-English languages
- Optional: Translation to English (or other languages)
- Language detection (automatic vs manual specification)
- Accent handling within language (e.g., Mexican vs Castilian Spanish)

---

## Critical Questions This Scenario Answers

1. **Which providers support non-English languages?**
   - Whisper: 99 languages (massively dominant)
   - AssemblyAI: English, Spanish only
   - Deepgram: English, Spanish, limited others
   - Otter: English, Spanish, French (3 languages)
   - Most SaaS: English-only

2. **What's the accuracy gap for non-English?**
   - Whisper accuracy varies by language (best: English, Spanish, French; weaker: low-resource languages)
   - Most SaaS platforms don't publish non-English WER metrics

3. **Translation vs Transcription - what's the difference?**
   - **Transcription**: Audio (Spanish) → Text (Spanish)
   - **Translation**: Text (Spanish) → Text (English) [separate capability]
   - **Instant translation**: Audio (Spanish) → Text (English) [transcribe + translate pipeline]

4. **When do you need translation?**
   - Monolingual teams reviewing non-English customer calls (support)
   - English-speaking managers reviewing international team meetings
   - Content localization (podcast in Spanish → English subtitles)

5. **Cost implications of multilingual?**
   - Whisper API: Same price for all languages ($0.006/min)
   - Translation adds cost: $15/M characters (Google Translate API)
   - Some SaaS platforms charge extra for non-English (check Otter, Fireflies pricing)

---

## Example Sub-Scenarios

### 6A: European Remote Team (Multilingual Same-Meeting)
- **Context**: 10-person team across Germany, France, Spain
- **Challenge**: Meetings often switch between English and native languages mid-conversation
- **Requirement**: Detect language switches, transcribe accurately, optional English translation for meeting notes
- **Provider needs**: Language detection, multilingual support, translation integration

### 6B: Latin American Customer Support
- **Context**: US company with Spanish-speaking customer base
- **Challenge**: Support calls in Spanish need transcription + translation to English for QA/training
- **Requirement**: Spanish transcription + translation, CRM integration
- **Provider needs**: Spanish accuracy (dialect variations), translation API, export to CRM

### 6C: Academic Research Interviews (Global)
- **Context**: Anthropologist conducting interviews in Swahili, Hindi, Mandarin
- **Challenge**: Low-resource languages, need verbatim transcripts in native language + English translation
- **Requirement**: 99-language support, high accuracy on low-resource languages
- **Provider needs**: Whisper (only option), translation service, quality validation

### 6D: Content Localization for YouTube
- **Context**: Spanish YouTube creator wants English subtitles (and vice versa)
- **Challenge**: Auto-generate subtitles in multiple languages, SRT format export
- **Requirement**: Transcription + translation, subtitle formatting, batch processing
- **Provider needs**: SRT export, translation integration, timestamp accuracy

---

## Provider Capabilities (from S1/S2)

### Whisper API (OpenAI)
- **Languages**: 99 languages (most comprehensive)
- **Quality**: Best for high-resource languages (English, Spanish, French, German, Mandarin, Japanese)
- **Limitations**: Variable accuracy on low-resource languages (Swahili, Tagalog)
- **Translation**: Not built-in, requires separate translation API
- **Cost**: $0.006/min (same for all languages)

### AssemblyAI
- **Languages**: English, Spanish (2024)
- **Quality**: Best Spanish accuracy (likely better than Whisper for Spanish-specific use cases)
- **Limitations**: No other languages
- **Translation**: Not offered
- **Cost**: $0.00025/sec ($0.015/min)

### Deepgram
- **Languages**: English, Spanish, plus limited others (check docs)
- **Quality**: Good for supported languages
- **Limitations**: Limited language support compared to Whisper
- **Translation**: Not offered
- **Cost**: $0.0043/min

### Rev AI
- **Languages**: English only (or very limited)
- **Quality**: Best English accuracy (96%+)
- **Limitations**: Not suitable for multilingual use cases
- **Cost**: $0.02/min

### Fireflies.ai
- **Languages**: English, Spanish, French, German, Portuguese, Italian, Dutch, Japanese (8 languages claimed - verify)
- **Quality**: Unknown (no published WER for non-English)
- **Limitations**: Likely uses Whisper backend for multilingual
- **Translation**: Not offered (transcription only)
- **Cost**: $120/user/year (Pro tier)

### Otter.ai
- **Languages**: English, Spanish, French (3 languages)
- **Quality**: Unknown (no published benchmarks)
- **Limitations**: Very limited language support
- **Translation**: Not offered
- **Cost**: $100/user/year (Pro tier)

### Grain, Fathom
- **Languages**: English-only (or extremely limited)
- **Limitations**: Not suitable for multilingual

---

## Translation Service Options (Separate Category)

For scenarios requiring translation (Spanish transcription → English text):

1. **Google Cloud Translation API**
   - Cost: $20/M characters
   - Languages: 100+
   - Quality: Good for common language pairs

2. **DeepL API**
   - Cost: $25/M characters (higher quality)
   - Languages: 30+ (European languages, Japanese, Chinese)
   - Quality: Best-in-class for European languages

3. **LLM-based translation** (GPT-4, Claude)
   - Cost: $3-30/M tokens (variable)
   - Languages: All major languages
   - Quality: Best for context-aware translation, idioms

4. **Built-in platform translation**
   - Some platforms may add this (check Fireflies, Otter roadmaps)
   - Current state: Mostly unavailable

---

## Workflow Patterns

### Pattern 1: Transcribe Only (Native Language)
- **Use case**: Spanish-speaking team needs Spanish meeting notes
- **Workflow**: Audio (Spanish) → Whisper API → Text (Spanish)
- **Cost**: $0.006/min
- **Best for**: Teams fluent in native language

### Pattern 2: Transcribe + Translate (Sequential)
- **Use case**: Spanish customer call → English for QA review
- **Workflow**: Audio (Spanish) → Whisper API → Text (Spanish) → Google Translate → Text (English)
- **Cost**: $0.006/min + $20/M characters (~$0.01/min for 500 words)
- **Best for**: Cross-language review, archival

### Pattern 3: Instant Translation (Real-Time)
- **Use case**: Live meeting in Spanish, English-speaking participant needs real-time captions
- **Workflow**: Audio (Spanish) → Deepgram streaming → Text (Spanish) → DeepL → Text (English) (all real-time)
- **Cost**: Higher (streaming + translation)
- **Best for**: Accessibility, live interpretation replacement

### Pattern 4: Multilingual Same-Meeting
- **Use case**: European team switches between English and German mid-conversation
- **Workflow**: Audio → Whisper with language detection → Text (mixed English/German)
- **Challenge**: Language detection per speaker or per sentence
- **Best for**: Multinational teams

---

## Cost Comparison: Multilingual Scenario

**Scenario**: 10-person Latin American customer support team, 50 calls/week in Spanish, need English translation for QA

**Option A: Whisper API + Google Translate**
- Whisper: 50 calls × 10 min × $0.006/min = $3/week
- Translation: 50 calls × 1,500 words × 7.5 chars × $20/M = $11.25/week
- **Total**: $742/year (transcription + translation)

**Option B: AssemblyAI (Spanish only, no translation)**
- AssemblyAI: 50 calls × 10 min × $0.015/min = $7.50/week
- Translation: (same as Option A) $11.25/week
- **Total**: $975/year

**Option C: SaaS Platform (Fireflies - if Spanish supported)**
- Fireflies Pro: 10 users × $120/year = $1,200/year
- No translation included (would need separate service)
- **Total**: $1,200/year + translation cost

**Insight**: API approach (Whisper + Google Translate) is 40% cheaper than SaaS for multilingual use cases.

---

## Key Insights for S3 Document

1. **Whisper dominates multilingual** - 99 languages vs 1-8 for competitors
2. **Translation is separate capability** - May warrant 3.20X category research
3. **Cost advantage for APIs** - Whisper $0.006/min for any language
4. **SaaS platforms lag on i18n** - Most English-only or limited languages
5. **Low-resource language challenge** - Whisper accuracy drops for Swahili, Tagalog, etc.
6. **Real-time translation complex** - Requires streaming transcription + translation pipeline

---

## Questions to Research for S3

1. What is Fireflies' actual language support? (Claims 8+ languages, verify)
2. Does Otter charge extra for Spanish/French? (Check pricing tiers)
3. What's Whisper accuracy on Spanish vs English? (Compare WER benchmarks)
4. Does AssemblyAI plan more languages? (Roadmap check)
5. Are there multilingual-specific SaaS platforms? (Amberscript, Sonix, Trint - add to research?)
6. What's the quality difference: Whisper Spanish vs AssemblyAI Spanish?

---

## Related Research Categories (Future)

- **3.203: Translation & Localization Services** (Google Translate, DeepL, LLM-based)
- **3.204: Subtitling & Captioning Platforms** (Rev.com, 3Play Media, Amara)
- **3.205: Real-Time Interpretation** (Live translation for meetings)

These are distinct from transcription but highly related - consider cross-referencing.

---

## Next Steps

1. Add scenario 6 to S3 research scope
2. Research multilingual-specific providers (Amberscript, Sonix, Trint)
3. Benchmark Whisper accuracy across languages (if data available)
4. Create decision tree: monolingual vs multilingual vs translation-required
5. Update TERMS-TO-EXPLAIN.md with i18n terminology
