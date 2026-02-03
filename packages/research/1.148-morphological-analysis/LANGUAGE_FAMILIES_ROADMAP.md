# Morphological Analysis: Language Families Roadmap

**Purpose**: Map the full morphological analysis space for language learning applications
**Status**: 1.148 (base) covers Japanese, Russian, Czech. This document catalogs future research.

---

## Hardware Store Philosophy

**"In Stock Now"** (1.148 base research):
- Japanese (Japonic family)
- Russian (Slavic family)
- Czech (Slavic family)

**"Catalog Entries"** (future 1.148.X research):
- Listed below, available for future research when needed
- Each represents a distinct morphological pattern or script system
- No need to research everything upfront - catalog the questions instead

---

## Language Family Catalog

### 1.148.1: Semitic Languages (Arabic, Hebrew)

**Morphological pattern**: Root + pattern system
**Complexity**: Very high (triliteral roots, vowel patterns, RTL script)

**Languages**:
- **Arabic**: Modern Standard Arabic, Egyptian, Levantine, Gulf dialects
- **Hebrew**: Modern Hebrew, Biblical Hebrew

**Key challenges**:
- Root + pattern morphology (k-t-b → kataba, kitaab, maktaba)
- Short vowels often omitted in writing
- Right-to-left script
- Diacritics critical for learners but absent in native text

**Library candidates**:
- camel-tools (Arabic NLP)
- MADAMIRA (Arabic morphological analyzer)
- Hebrew NLP tools (spaCy, NLPH)

**Use case**: Arabic learner parsing Quran, news articles; Hebrew learner parsing Torah, modern texts

---

### 1.148.2: Sinitic Languages (Chinese, Mandarin, Cantonese)

**Morphological pattern**: Minimal inflection, character-based
**Complexity**: Low morphology, high character complexity

**Languages**:
- **Mandarin Chinese**: Standard Chinese, simplified/traditional
- **Cantonese**: Hong Kong, Guangdong
- **Other**: Hokkien, Hakka

**Key challenges**:
- Characters ≠ words (need tokenization: 中国 = one word "China")
- Minimal inflection (aspect markers: 了, 过, 着)
- Tone marking (not in writing)
- Pinyin vs characters

**Library candidates**:
- jieba (Chinese segmentation)
- pkuseg (Peking University segmenter)
- spaCy Chinese models
- Stanford CoreNLP Chinese

**Use case**: Chinese learner parsing news, literature, social media

---

### 1.148.3: Slavic Expansion (Polish, Bosnian/Serbian/Croatian, Ukrainian)

**Morphological pattern**: Fusional (6-7 cases, aspect)
**Complexity**: High (similar to Russian/Czech)

**Languages**:
- **Polish**: 7 cases, complex phonology
- **Bosnian/Serbian/Croatian**: 6 cases, Cyrillic/Latin variants
- **Ukrainian**: 7 cases, Cyrillic, similar to Russian

**Key challenges**:
- Case systems (6-7 cases)
- Aspect pairs (perfective/imperfective)
- Script variants (Cyrillic ↔ Latin for Serbian/Bosnian)

**Library candidates**:
- spaCy (hr, sr, pl, uk models)
- UDPipe (Universal Dependencies)
- Language-specific analyzers

**Use case**: Slavic learner parsing literature, news, conversational text

---

### 1.148.4: Germanic Expansion (Dutch, Swedish, Norwegian, Danish)

**Morphological pattern**: Moderate inflection (declining case system)
**Complexity**: Medium

**Languages**:
- **Dutch**: Remnant case system, separable verbs
- **Swedish/Norwegian/Danish**: Minimal cases, definite suffixes
- **Icelandic**: High complexity (4 cases, strong/weak inflection)

**Key challenges**:
- Separable verbs (German: aufstehen → steht auf)
- Definite article as suffix (Swedish: hus → huset "the house")
- Compound words (Dutch: hypotheekrenteaftrekdebat)

**Library candidates**:
- spaCy (nl, sv, da models)
- UDPipe
- Language-specific tools

**Use case**: Germanic learner parsing news, literature, everyday text

---

### 1.148.5: Romance Expansion (Italian, Portuguese, Romanian)

**Morphological pattern**: Verb-heavy inflection
**Complexity**: Medium (simpler than Latin)

**Languages**:
- **Italian**: Rich verb conjugation, minimal cases
- **Portuguese**: European vs Brazilian variants
- **Romanian**: 5 cases (most among Romance), Slavic influence

**Key challenges**:
- Complex verb conjugation (6 tenses, subjunctive)
- Gender agreement
- Clitic pronouns (Italian: me lo dai → "you give it to me")

**Library candidates**:
- spaCy (it, pt, ro models)
- Language-specific analyzers

**Use case**: Romance learner parsing literature, news, conversation

---

### 1.148.6: Turkic Languages (Turkish, Uzbek, Kazakh)

**Morphological pattern**: Agglutinative, vowel harmony
**Complexity**: Very high (suffix stacking)

**Languages**:
- **Turkish**: Agglutinative, vowel harmony, 8 cases
- **Uzbek**: Latin/Cyrillic scripts
- **Kazakh**: Cyrillic/Latin transition

**Key challenges**:
- Vowel harmony (suffixes match vowel of stem)
- Agglutination (evlerinizden = ev-ler-iniz-den "from your houses")
- Long suffix chains

**Library candidates**:
- Turkish NLP tools (Zemberek)
- spaCy experimental models
- Rule-based analyzers

**Use case**: Turkic learner parsing news, social media, formal text

---

### 1.148.7: Dravidian Languages (Tamil, Telugu, Malayalam)

**Morphological pattern**: Agglutinative
**Complexity**: High (case stacking, verb complexity)

**Languages**:
- **Tamil**: 8 cases, agglutinative, Dravidian script
- **Telugu**: Similar complexity, different script
- **Malayalam**: Complex script, agglutinative

**Key challenges**:
- Case stacking (multiple case markers on one noun)
- Complex verb conjugation
- Unique scripts (no relation to Latin/Cyrillic)

**Library candidates**:
- Indic NLP Library
- spaCy Dravidian models (experimental)
- Language-specific analyzers

**Use case**: Dravidian learner parsing literature, religious texts, conversation

---

### 1.148.8: Sign Languages (ASL, BSL, ISL)

**Morphological pattern**: Visual-spatial morphology
**Complexity**: No written form, unique linguistic structure

**Languages**:
- **ASL**: American Sign Language
- **BSL**: British Sign Language
- **ISL**: Irish Sign Language
- (Note: Mutually unintelligible despite shared spoken language)

**Key challenges**:
- No traditional written form (no "letters" to parse)
- Morphology through space, movement, facial expression
- SignWriting notation exists but not widely used
- Video-based analysis required

**Library candidates**:
- SignWriting parsers
- Video analysis for sign recognition
- Specialized sign language NLP tools

**Use case**: Sign language learner analyzing signed videos, transcripts, conversations

---

### 1.148.9: Isolating Languages (Vietnamese, Thai, Laotian)

**Morphological pattern**: Minimal inflection, tonal
**Complexity**: Low morphology, high tone complexity

**Languages**:
- **Vietnamese**: No inflection, 6 tones, Latin script with diacritics
- **Thai**: No inflection, 5 tones, unique script
- **Laotian**: Similar to Thai

**Key challenges**:
- Tones critical for meaning (not always marked)
- Word segmentation (no spaces in Thai/Laotian)
- Minimal morphology = few grammatical markers

**Library candidates**:
- pythainlp (Thai NLP)
- Vietnamese NLP tools
- spaCy experimental models

**Use case**: Tonal language learner parsing conversational text, news

---

### 1.148.10: Polysynthetic Languages (Inuktitut, Navajo, Yup'ik)

**Morphological pattern**: Extreme agglutination (entire sentence = one word)
**Complexity**: Very high (longest words, complex morphology)

**Languages**:
- **Inuktitut**: Canadian Arctic, syllabic script
- **Navajo**: Southwestern US, Latin script
- **Yup'ik**: Alaska, Latin script

**Key challenges**:
- Entire sentences as single words (tusaatsiarunnanngittualuujunga = "I can't hear very well")
- Complex verb morphology (10+ affixes possible)
- Limited NLP tools (endangered languages)

**Library candidates**:
- Uqailaut (Inuktitut analyzer)
- Specialized academic tools
- Rule-based morphological parsers

**Use case**: Indigenous language learner, linguistic research, preservation efforts

---

### 1.148.11: Mixed Systems (Korean, Uyghur)

**Morphological pattern**: Multiple systems combined
**Complexity**: High (script + morphology complexity)

**Languages**:
- **Korean**: Agglutinative + Chinese characters (Hanja), Hangul script
- **Uyghur**: Arabic script + Turkic morphology

**Key challenges**:
- Korean: Hangul + Hanja, complex honorific system
- Multiple writing systems in same text
- Particles (Korean: 은/는, 이/가, 을/를)

**Library candidates**:
- KoNLPy (Korean NLP)
- mecab-ko (Korean MeCab fork)
- spaCy Korean models

**Use case**: Korean learner parsing K-dramas, news, literature

---

## Research Priority Framework

**Tier 1** (High value, ready to research):
- 1.148.3: Slavic expansion (Polish, Bosnian/Serbian/Croatian) - similar to Russian/Czech
- 1.148.11: Korean - large learner base, good library support

**Tier 2** (Moderate value, needs demand signal):
- 1.148.1: Arabic/Hebrew - high complexity, specialized domain
- 1.148.6: Turkish - agglutinative pattern different from Japanese
- 1.148.9: Vietnamese/Thai - isolating languages (different paradigm)

**Tier 3** (Low priority, niche):
- 1.148.7: Dravidian - specialized domain
- 1.148.10: Polysynthetic - academic interest, endangered languages
- 1.148.8: Sign languages - specialized tools, different paradigm

**Not Yet Prioritized**:
- 1.148.4: Germanic expansion (spaCy already handles well)
- 1.148.5: Romance expansion (spaCy already handles well)
- 1.148.2: Chinese (low morphology, primarily segmentation problem)

---

## Pattern Recognition: What We Learn From Each Family

| Language Family | Morphology Type | Key Pattern | Representative |
|-----------------|-----------------|-------------|----------------|
| **Japonic** | Agglutinative | Particles + verb suffixes | Japanese |
| **Slavic** | Fusional | 6-7 cases + aspect | Russian, Czech |
| **Semitic** | Root + pattern | Triliteral roots | Arabic, Hebrew |
| **Sinitic** | Isolating | Minimal inflection | Chinese |
| **Turkic** | Agglutinative | Vowel harmony | Turkish |
| **Dravidian** | Agglutinative | Case stacking | Tamil |
| **Polysynthetic** | Extreme agglutination | Sentence = word | Inuktitut |
| **Sign** | Visual-spatial | No written script | ASL, BSL |

---

## Decision Framework: When to Research a New Language Family

**Research 1.148.X when**:
1. ✅ User demand (building app for that language)
2. ✅ Represents new morphological pattern not yet covered
3. ✅ Library ecosystem exists (not building from scratch)
4. ✅ Complements existing language learning app

**Skip 1.148.X when**:
1. ❌ Already covered by existing research (French → spaCy from 1.033)
2. ❌ No viable libraries (would require building analyzer from scratch)
3. ❌ Minimal morphology (Chinese segmentation ≠ morphological analysis)
4. ❌ Low demand signal (no current use case)

---

## Integration with Language Learning Roadmap

**Current state** (Nov 2025):
- ✅ **Latin**: 1.140 (CLTK) → latin-parse → latin-train
- 🔄 **Japanese, Russian, Czech**: 1.148 (base) → *-parse → *-train
- ⏸️ **French, Spanish, German**: spaCy (from 1.033) - no morphology research needed
- ⏸️ **All others**: Catalog entries (1.148.X) - research when needed

**Future expansion**:
When user says "I want to add Arabic support":
1. Consult 1.148.1 (Semitic languages catalog entry)
2. Research Arabic morphological analyzers (camel-tools, MADAMIRA)
3. Implement arabic-parse following latin-parse pattern
4. Build arabic-train following latin-train pattern

---

## Maintenance Notes

**When to update this roadmap**:
- New language family discovered (add 1.148.X entry)
- Library ecosystem matures (update "candidates")
- User demand signal (reprioritize tiers)
- Research completed (move from catalog to completed)

**This is a living catalog**, not a commitment to research everything. The hardware store has a full catalog, but we only stock what's actively needed.
