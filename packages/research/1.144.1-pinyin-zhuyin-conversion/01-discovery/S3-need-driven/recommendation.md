# S3-Need-Driven Recommendation

## Use Case Summary Matrix

| Use Case | pypinyin | dragonmapper | Winner | Why |
|----------|----------|--------------|--------|-----|
| **IME** | ❌ Wrong direction | ⚠️ Partial fit | Neither (need dict) | Missing core: romanization → characters |
| **Learning Apps** | ✅✅ Excellent | ⚠️ Adequate | pypinyin | Rich formats, context awareness, pedagogical features |
| **Search/Indexing** | ✅✅ Excellent | ⚠️ Limited | pypinyin | Multiple variants for fuzzy matching |
| **Transcription Tools** | ❌ Wrong direction | ✅✅ Excellent | dragonmapper | Direct format conversion, validation |

## Decision Framework

### Start Here: What is Your Source Data?

```
┌─────────────────────┐
│  What's your input? │
└──────────┬──────────┘
           │
           ├─ Chinese characters ────────→ pypinyin
           │                              (Character → romanization)
           │
           ├─ Romanized text ─────────────→ dragonmapper
           │  (Pinyin/Zhuyin/IPA)          (Transcription conversion)
           │
           └─ User-generated input ───────→ Need character dictionary
              (IME scenario)                (Neither library sufficient)
```

### Decision Tree

```
Are you converting FROM Chinese characters?
├─ YES → Use pypinyin
│        ├─ Need multiple Pinyin styles? → pypinyin perfect
│        ├─ Need context-aware accuracy? → pypinyin perfect
│        └─ Then need Pinyin→Zhuyin? → Add dragonmapper
│
└─ NO → Working with romanized text?
         ├─ YES → Use dragonmapper
         │        ├─ Converting between formats? → dragonmapper perfect
         │        ├─ Need format detection? → dragonmapper perfect
         │        └─ Need IPA? → dragonmapper only option
         │
         └─ NO → Need romanization→characters?
                  └─ Use character dictionary (CC-CEDICT, etc.)
                       └─ Then use pypinyin/dragonmapper for display
```

## Recommendations by Application Type

### Language Learning Applications
**Recommendation**: pypinyin (primary), dragonmapper (optional)

**Why pypinyin**:
- Multiple display formats support different learning stages
- Context-aware pronunciation teaches correctness
- Component extraction (initials/finals) has pedagogical value
- Customization handles edge cases (names, specialized vocab)

**When to add dragonmapper**:
- If you also need IPA for linguistics courses
- If offering Pinyin↔Zhuyin format switching for user preference

**Implementation priority**:
1. pypinyin for character display with romanization
2. (Optional) dragonmapper for format switching features

### Search & E-Commerce Applications
**Recommendation**: pypinyin (essential)

**Why pypinyin**:
- Generate multiple search keys (tone marks, tone-less, abbreviations)
- Heteronym support ensures comprehensive indexing
- First-letter extraction enables fast prefix matching
- Essential for fuzzy, user-friendly Chinese search

**Index creation pattern**:
```python
# Use pypinyin to create search index
keys = {
    'pinyin_notone': lazy_pinyin(text),      # Most important
    'pinyin_abbrev': first_letters(text),     # Fast prefix
    'zhuyin': pinyin(text, style=BOPOMOFO),  # Taiwan users
}
```

**dragonmapper not needed** unless query preprocessing requires format detection.

### Publishing & Annotation Tools
**Recommendation**: pypinyin (primary), dragonmapper (secondary)

**Why pypinyin**:
- Generate annotations from Chinese text
- Multiple styles for different audiences
- Context-aware accuracy matters for publication quality

**When to add dragonmapper**:
- If converting existing annotations between formats
- If source material has mixed romanization formats

**Workflow**:
1. Chinese text → pypinyin → Pinyin/Zhuyin annotations
2. (If needed) Pinyin → dragonmapper → Zhuyin (format conversion)

### Transcription & Conversion Utilities
**Recommendation**: dragonmapper (primary), pypinyin (secondary)

**Why dragonmapper**:
- Direct Pinyin ↔ Zhuyin conversion
- Format detection and validation (critical for automation)
- Works with romanized text (your actual input)
- IPA support for linguistic research

**When to add pypinyin**:
- If you also need to convert FROM Chinese characters
- If source is Chinese and you need to generate initial romanization

**Workflow**:
- Romanized text → dragonmapper → Different romanization format
- (If needed) Chinese text → pypinyin → Romanization → dragonmapper → Format conversion

### IME (Input Method Editor) Development
**Recommendation**: dragonmapper (partial), + character dictionary (essential)

**Critical gap**: Neither library provides romanization → Chinese character conversion.

**What dragonmapper provides**:
- Input validation (is this valid Pinyin/Zhuyin?)
- Format detection (what did the user type?)
- Format switching (Pinyin ↔ Zhuyin modes)

**What's missing** (need additional library):
- Character candidates lookup (need CC-CEDICT, Unihan, or commercial dict)
- Frequency-based ranking
- Context prediction
- User learning

**Architecture**:
```python
# dragonmapper for input processing
format = transcriptions.identify(user_input)
if format == 'Pinyin':
    # Validate input
    if transcriptions.is_pinyin(user_input):
        # Look up characters (EXTERNAL DICTIONARY)
        candidates = character_dict.lookup(user_input)

        # Annotate results with pypinyin (optional)
        for candidate in candidates:
            candidate.zhuyin = pypinyin_annotate(candidate.char)
```

### Data Cleaning & Normalization
**Recommendation**: dragonmapper

**Why dragonmapper**:
- Format detection finds mixed-format data
- Validation identifies corrupted romanization
- Conversion standardizes to single format

**Pattern**:
```python
# Detect and standardize mixed formats
detected = transcriptions.identify(text)
if detected == 'Pinyin':
    standardized = transcriptions.pinyin_to_zhuyin(text)
elif detected == 'Zhuyin':
    standardized = text  # Already in target format
else:
    flag_for_manual_review(text)
```

## Common Anti-Patterns

### Anti-Pattern 1: Using pypinyin for Transcription Conversion
**Problem**: Trying to convert Pinyin → Zhuyin using pypinyin

**Why it fails**: pypinyin works with Chinese characters, not romanized text

**Symptom**:
```python
# This DOESN'T work
input_pinyin = "ni hao"
output = pinyin(input_pinyin, style=Style.BOPOMOFO)
# ERROR: pypinyin expects Chinese characters, not romanization
```

**Solution**: Use dragonmapper
```python
input_pinyin = "nǐ hǎo"
output = transcriptions.pinyin_to_zhuyin(input_pinyin)
# ✅ Correct: ㄋㄧˇ ㄏㄠˇ
```

### Anti-Pattern 2: Using dragonmapper for Character Conversion
**Problem**: Trying to get romanization from Chinese text with dragonmapper alone

**Why it's suboptimal**: dragonmapper can do it, but pypinyin is better

**Works but limited**:
```python
from dragonmapper import hanzi
hanzi.to_pinyin('你好')  # Works, returns 'nǐhǎo'
```

**Better with pypinyin**:
```python
from pypinyin import pinyin, Style
pinyin('你好', style=Style.TONE)     # More style options
pinyin('你好', style=Style.BOPOMOFO) # Better context handling
```

### Anti-Pattern 3: Building IME with Only These Libraries
**Problem**: Expecting pypinyin or dragonmapper to provide full IME functionality

**What's missing**: Romanization → Character lookup (core IME feature)

**Solution**: Use these libraries for supplementary features only:
- dragonmapper: Input validation, format switching
- pypinyin: Candidate annotation
- **Plus**: Character dictionary for actual character lookup

### Anti-Pattern 4: Indexing with dragonmapper
**Problem**: Using dragonmapper to create search indexes

**Why it's suboptimal**: Limited romanization variants (only 2 vs pypinyin's 13+)

**Consequence**: Missing search matches (e.g., no first-letter abbreviation index)

**Solution**: Use pypinyin for index creation
```python
# pypinyin: Rich index
lazy_pinyin(text)           # Tone-less
first_letters(text)         # Abbreviation
pinyin(text, heteronym=True) # All pronunciations

# dragonmapper: Limited options
to_pinyin(text)             # Only one format
```

## Combined Usage Patterns

### Pattern 1: Character Conversion + Format Switching
Use both libraries when you need both capabilities:

```python
from pypinyin import pinyin, Style
from dragonmapper import transcriptions

# Step 1: Convert Chinese to Pinyin (pypinyin)
chinese = "中文"
pinyin_text = ' '.join([p[0] for p in pinyin(chinese, style=Style.TONE)])

# Step 2: Convert Pinyin to Zhuyin (dragonmapper)
zhuyin_text = transcriptions.pinyin_to_zhuyin(pinyin_text)
```

**Use case**: Multi-format language learning app

### Pattern 2: Validation + Annotation
Validate user input, then annotate with romanization:

```python
from dragonmapper import transcriptions
from pypinyin import pinyin, Style

# Step 1: Validate user input (dragonmapper)
user_input = "nǐhǎo"
if not transcriptions.is_pinyin(user_input):
    show_error("Invalid Pinyin")

# Step 2: Convert to characters (external dict)
characters = lookup_characters(user_input)

# Step 3: Annotate results (pypinyin)
for char in characters:
    char.zhuyin = pinyin(char, style=Style.BOPOMOFO)[0][0]
```

**Use case**: Educational IME or typing tutor

### Pattern 3: Comprehensive Search Index
Create rich search index with all formats:

```python
from pypinyin import lazy_pinyin, pinyin, Style
from dragonmapper import hanzi

# pypinyin: Character → Pinyin variants
pinyin_variants = {
    'notone': lazy_pinyin(chinese_text),
    'abbrev': first_letters(chinese_text),
}

# pypinyin: Character → Zhuyin
zhuyin_variant = pinyin(chinese_text, style=Style.BOPOMOFO)

# Store all in search index
index[doc_id] = {
    'chinese': chinese_text,
    **pinyin_variants,
    'zhuyin': zhuyin_variant
}
```

**Use case**: Cross-platform search (mainland + Taiwan)

## Cost-Benefit Analysis

### pypinyin
**Benefits**:
- ✅ Rich feature set (13+ styles)
- ✅ Context-aware accuracy
- ✅ Active maintenance
- ✅ Large community

**Costs**:
- ⚠️ Larger memory footprint
- ⚠️ API complexity (more to learn)
- ⚠️ Overkill for simple needs

**Worth it when**: Building sophisticated applications where romanization quality and flexibility matter (learning, search, publishing)

### dragonmapper
**Benefits**:
- ✅ Focused, simple API
- ✅ Unique transcription features (Pinyin↔Zhuyin, IPA)
- ✅ Format detection/validation

**Costs**:
- ⚠️ Less active maintenance
- ⚠️ Limited style options
- ⚠️ Smaller community

**Worth it when**: Building transcription tools or need format detection/conversion between romanization systems

### Both Libraries
**Benefits**:
- ✅ Maximum flexibility
- ✅ Cover all use cases

**Costs**:
- ❌ Two dependencies
- ❌ More complexity
- ❌ Learning curve for both APIs

**Worth it when**: Building comprehensive Chinese processing platforms that need both character conversion AND transcription conversion

## Final Recommendations

### Choose pypinyin if:
- [x] Converting FROM Chinese characters (primary workflow)
- [x] Building language learning applications
- [x] Building Chinese search/indexing features
- [x] Need multiple romanization output formats
- [x] Context-aware pronunciation is important
- [x] Need pedagogical features (initials/finals)

### Choose dragonmapper if:
- [x] Converting BETWEEN romanization formats (Pinyin ↔ Zhuyin)
- [x] Building transcription conversion tools
- [x] Need format detection/validation
- [x] Need IPA support
- [x] Source data is already romanized (not Chinese characters)
- [x] Building data cleaning pipelines for mixed formats

### Choose both if:
- [x] Building comprehensive Chinese platform
- [x] Need character conversion AND transcription conversion
- [x] Multi-format support is critical (mainland + Taiwan + international)
- [x] Two dependencies are acceptable

### Choose neither if:
- [x] Building full IME (need character dictionary instead)
- [x] Only need audio pronunciation (need TTS instead)
- [x] Only need character recognition (need OCR instead)

## Gap Analysis

### Missing from Both Libraries
1. **Romanization → Character lookup** (essential for IME)
2. **Audio pronunciation** (need TTS)
3. **Stroke order data** (need separate database)
4. **Character etymology** (need separate resources)
5. **Spaced repetition algorithms** (need separate logic)
6. **Natural language processing** (need NLP tools)
7. **Machine translation** (need MT systems)

These capabilities require additional tools beyond romanization libraries.

### Ecosystem Recommendations
For comprehensive Chinese text processing, combine:
- **pypinyin**: Character → romanization
- **dragonmapper**: Transcription conversion, validation
- **CC-CEDICT / Unihan**: Character dictionary (romanization → characters)
- **jieba / pkuseg**: Word segmentation
- **opencc**: Traditional ↔ Simplified conversion
- **chinese / hanzident**: Character property detection

## Conclusion

**Most projects should start with pypinyin** as it handles the most common use case (Chinese characters → romanization) with excellent flexibility and quality.

**Add dragonmapper when** you need transcription conversion features (Pinyin ↔ Zhuyin) or format detection.

**Both libraries are specialized tools**, not general-purpose Chinese NLP. Know their strengths and combine with other tools as needed for comprehensive Chinese text processing.
