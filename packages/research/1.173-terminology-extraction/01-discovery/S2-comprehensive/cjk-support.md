# CJK Language Support Analysis

**Relevance**: Research bead has `cjk` label, indicating Chinese, Japanese, Korean support is a priority.

## Summary Table

| Library | Chinese | Japanese | Korean | Status | Notes |
|---------|---------|----------|--------|--------|-------|
| **pyate** | ❌ No | ❌ No | ❌ No | Blocked | No general corpora |
| **KeyBERT** | ✅ Yes | ✅ Yes | ✅ Yes | Works | Multilingual BERT |
| **chinese_keybert** | ✅ Best | ❌ No | ❌ No | Works | Chinese-specific fork |

## pyate CJK Support

### Technical Capability:
✅ spaCy models exist for Chinese, Japanese, Korean
✅ pyate can load spaCy CJK models via `set_language()`

### Actual Status:
❌ **No CJK support** due to missing general domain corpora

### Why Blocked:

Per [GitHub Issue #13](https://github.com/kevinlu1248/pyate/issues/13):
> As of version 0.4.2, only English and Italian are supported. The library's language support depends on having appropriate spaCy models **and general domain corpora** for those languages.

**What's Missing**:
- **Weirdness algorithm**: Requires **general corpus** to contrast against technical corpus
- **Term Extractor algorithm**: Requires **reference corpus**

**Available spaCy Models**:
- Chinese: `zh_core_web_sm`, `zh_core_web_md`, `zh_core_web_lg`
- Japanese: `ja_core_news_sm`, `ja_core_news_md`, `ja_core_news_lg`
- Korean: Rule-based tokenizer, trained pipelines available

**Workaround**: Provide your own general corpus
```python
from pyate import combo_basic

chinese_text = "您的中文技术文档..."
general_corpus = "Your own Chinese general domain corpus..."

# This WILL work if you provide general_corpus
terms = combo_basic(chinese_text, general_corpus=general_corpus)
```

**Verdict**: pyate is **NOT recommended for CJK** unless you can build general domain corpora (non-trivial effort).

## KeyBERT CJK Support

### Technical Capability:
✅ Multilingual BERT models support 50-109 languages including CJK
✅ Out-of-box support, no additional corpora needed

### CJK Tokenization Behavior

Per [Google BERT Multilingual Docs](https://github.com/google-research/bert/blob/master/multilingual.md):

**Chinese (and Japanese Kanji, Korean Hanja)**:
- Character-tokenized (spaces added around every CJK Unicode character)
- Effectively treats Chinese as character-level (not word-level)
- May extract character-level "terms" instead of proper words

**Japanese Katakana/Hiragana, Korean Hangul**:
- Whitespace + WordPiece tokenization (normal BERT behavior)
- Better term extraction quality

**Example**:
- Input: "自然语言处理" (natural language processing in Chinese)
- BERT tokenization: ["自", "然", "语", "言", "处", "理"] (6 characters)
- KeyBERT may extract: "语言" (language), "处理" (processing) as separate "keywords"

**Implication**: Character-level tokenization may miss proper word boundaries for Chinese/Japanese.

### Recommended Models for CJK

| Model | Languages | CJK Quality | Size |
|-------|-----------|-------------|------|
| `paraphrase-multilingual-MiniLM-L12-v2` | 50+ incl. CJK | Good | 420MB |
| `paraphrase-multilingual-mpnet-base-v2` | 50+ incl. CJK | Better (higher quality) | 1.1GB |
| `distiluse-base-multilingual-cased-v1` | 15 incl. Chinese, Korean | Lightweight | 480MB |
| `LaBSE` | **109 languages** | Max coverage | 470MB |

**Recommendation**: Start with `paraphrase-multilingual-MiniLM-L12-v2` (balance of size and quality).

### Chinese-Specific: chinese_keybert Fork

**Repository**: [JacksonCakes/chinese_keybert](https://github.com/JacksonCakes/chinese_keybert)

**Improvements over Generic KeyBERT**:
- ✅ Uses **CKIP library** for Chinese word segmentation (proper word boundaries)
- ✅ Chinese POS tagging (identifies noun phrases correctly)
- ✅ Integrates sentence-transformers for embeddings

**Usage**:
```python
from chinese_keybert import ChineseKeyBERT

kw_model = ChineseKeyBERT()
keywords = kw_model.extract_keywords("自然语言处理技术...")
```

**Trade-off**:
- ✅ Better Chinese word segmentation (vs character-level generic BERT)
- ❌ Chinese-only (no Japanese, Korean support)
- ❌ Additional dependency (CKIP library)

**Verdict**: Use `chinese_keybert` if Chinese-only, use generic KeyBERT with multilingual model if multi-CJK.

## Other Libraries: CJK Status

### YAKE
✅ **Language-agnostic** (no language-specific models needed)
✅ Works on CJK text (statistical approach)
⚠️ Character-level statistics may affect quality for Chinese

### RAKE-NLTK
❌ **English-centric** (depends on English stopwords)
❌ Not recommended for CJK

### textacy
⚠️ **Depends on spaCy models** (same as pyate)
✅ spaCy CJK models exist (Chinese, Japanese, Korean)
✅ Should work for CJK if using spaCy CJK models
? Unknown if TextRank algorithm requires additional corpora

## Real-World CJK Use Cases

### Translation (Chinese ↔ English)
**Need**: Extract Chinese technical terms for translation glossaries

**Recommendation**:
1. **KeyBERT** with `paraphrase-multilingual-MiniLM-L12-v2` (works, but character-level)
2. **chinese_keybert** (better Chinese word segmentation)
3. **Hybrid**: Manual review + filtering (BERT may miss proper terms)

**Challenge**: Character-level tokenization may extract "语言" (language) and "处理" (processing) separately, missing "自然语言处理" (natural language processing) as a complete term.

### Multilingual Technical Documentation (Chinese, Japanese, Korean)
**Need**: Consistent terminology across CJK languages

**Recommendation**:
1. **KeyBERT** with multilingual model (supports all three)
2. **Per-language**: chinese_keybert (Chinese), generic KeyBERT (Japanese, Korean)

**Trade-off**: Consistency (single model) vs quality (language-specific models).

### Japanese Technical Writing
**Need**: Extract Japanese technical terms (mix of Kanji, Hiragana, Katakana)

**Recommendation**:
1. **KeyBERT** with multilingual model (handles all scripts)
2. Consider spaCy Japanese model + textacy (if KeyBERT quality insufficient)

**Note**: Japanese mixes character sets (Kanji = character-level, Kana = syllabic). BERT handles this natively.

## Verdict: CJK Support

### For Chinese:
🥇 **chinese_keybert** (best word segmentation)
🥈 **KeyBERT** with multilingual model (works, but character-level)
❌ **pyate** (no general corpus)

### For Japanese:
🥇 **KeyBERT** with multilingual model (native support)
🥈 **textacy** + spaCy Japanese model (if KeyBERT insufficient)
❌ **pyate** (no general corpus)

### For Korean:
🥇 **KeyBERT** with multilingual model (native support)
❌ **pyate** (no general corpus)

### For Multi-CJK (all three languages):
🥇 **KeyBERT** with `paraphrase-multilingual-MiniLM-L12-v2` or `LaBSE`
- Single model for all three languages
- Consistent approach across CJK
- Trade-off: Character-level for Chinese may reduce term quality

## Recommendations

**If CJK support is required** (per research label):
1. **Default choice**: KeyBERT with multilingual model (`paraphrase-multilingual-MiniLM-L12-v2`)
2. **Chinese-only**: chinese_keybert fork (better word segmentation)
3. **NOT recommended**: pyate (no CJK corpora)

**If CJK + English mixed**:
- KeyBERT works across languages in single model
- Useful for multilingual technical documentation
- Example: Code comments mixing English and Chinese

**If terminology precision is critical**:
- Consider manual review + filtering of KeyBERT output
- Character-level tokenization may miss multi-character technical terms
- Hybrid approach: KeyBERT extraction + human validation
