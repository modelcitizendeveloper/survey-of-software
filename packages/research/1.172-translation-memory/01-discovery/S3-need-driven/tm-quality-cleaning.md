# TM Quality Management and Cleaning

## Why TM Cleaning Matters

**Problem:** Over time, TM accumulates:
- Duplicate segments
- Low-quality translations
- Outdated terminology
- Segments with errors
- Auto-extracted web content (often poor quality)

**Impact:** A typical scan removes **20-45% of TMX database** as problematic

**Source:** [TMX Cleaning Service](https://custom.mt/translation-memory-tmx-cleaning-2/)

## Automated TM Cleaning Tools

### TMOP (Translation Memory Open-source Purifier)

**Platform:** Python
**License:** Open source
**Repository:** [GitHub - TMOP](https://github.com/hlt-mt/TMOP)

**Features:**
- Unsupervised cleaning (no training data needed)
- Identifies problematic translation units
- Rule-based + neural network approaches

**Use Case:** Cleaning large, collaboratively-built TMs

**Reference:** [TMop: a Tool for Unsupervised Translation Memory Cleaning](https://aclanthology.org/P16-4009.pdf)

### Commercial Cleaning Services

**Inten.to, Custom.MT, ChilliStore:**
- Professional TM cleanup services
- Use LQA (Linguistic Quality Assurance) metrics
- AI-powered analysis (hundreds of automated tests)
- RegEx rules + neural networks

**Typical Process:**
1. Upload TMX file
2. Automated scan identifies issues
3. Human review of flagged segments
4. Cleaned TMX delivered

**Sources:**
- [Translation Memory (TM) Clean Up - Inten.to](https://inten.to/translation-memory-cleanup/)
- [Translation Memory and Term Base Tune-up - ChilliStore](https://www.chillistore.com/blog/translation-memory-and-term-base-tune-up/)

## Common Quality Issues

### 1. Duplicates

**Types:**
- Exact duplicates (same source, same target, different metadata)
- Near-duplicates (same source, slightly different targets)

**Detection:**
```python
# Exact duplicate detection
seen = {}
duplicates = []

for tu in tmx.body.translation_units:
    key = (source_seg, target_seg)
    if key in seen:
        duplicates.append(tu)
    else:
        seen[key] = tu
```

### 2. Source = Target

**Problem:** Translation equals source (untranslated segment)

**Detection:**
```python
for tu in tmx.body.translation_units:
    source_seg = tu.get_variant(source_lang).segment
    target_seg = tu.get_variant(target_lang).segment

    if source_seg == target_seg:
        # Flag as potentially untranslated
        print(f"Source=Target: {source_seg}")
```

**Exception:** Proper nouns, product names may legitimately be identical

### 3. Formatting Issues

**Problems:**
- Extra whitespace
- Inconsistent capitalization
- Missing/extra punctuation

**Detection via Regex:**
```python
import re

# Multiple spaces
if re.search(r'  +', target_seg):
    # Flag

# Inconsistent capitalization (source capitalized, target not)
if source_seg[0].isupper() and target_seg[0].islower():
    # Flag (may be intentional for some languages)
```

### 4. Length Mismatch

**Heuristic:** Extreme length differences may indicate errors

```python
source_len = len(source_seg)
target_len = len(target_seg)

ratio = target_len / source_len if source_len > 0 else 0

# Flag if ratio outside expected range (adjust per language pair)
if ratio < 0.5 or ratio > 2.0:
    # Suspicious length mismatch
    pass
```

**Note:** Expected ratio varies by language pair (German often 20% longer than English)

### 5. Incomplete Translations

**Indicators:**
- Contains placeholder text ("TODO", "[TBD]")
- Source language words mixed into target

**Detection:**
```python
if "TODO" in target_seg or "[TBD]" in target_seg:
    # Incomplete translation
    pass

# Detect source language words in target (requires language detection library)
```

## Quality Metrics

### MQM (Multidimensional Quality Metrics)

Framework for evaluating translation quality with categories:
- **Accuracy:** Mistranslation, addition, omission
- **Fluency:** Grammar, spelling, punctuation
- **Terminology:** Inconsistent terms
- **Style:** Inappropriate tone, register

**Application:** Manual review uses MQM to score segments

**Source:** [Automatic translation memory cleaning | Machine Translation](https://link.springer.com/article/10.1007/s10590-017-9191-5)

### Automated Scoring

```python
def quality_score(source, target):
    """Simple automated quality score (0-100)"""
    score = 100

    # Penalties
    if source == target:
        score -= 50  # Likely untranslated

    if len(target) == 0:
        score -= 100  # Empty translation

    length_ratio = len(target) / len(source) if len(source) > 0 else 0
    if length_ratio < 0.3 or length_ratio > 3.0:
        score -= 30  # Extreme length mismatch

    if re.search(r'  +', target):
        score -= 10  # Extra whitespace

    return max(0, score)
```

## Cleaning Workflow

### Step 1: Analyze

```python
from pythontmx import TmxFile

tmx = TmxFile.read("dirty.tmx")

issues = {
    'duplicates': 0,
    'source_equals_target': 0,
    'length_mismatch': 0,
    'empty_target': 0
}

for tu in tmx.body.translation_units:
    # Run quality checks, count issues
    pass

print(f"Found {sum(issues.values())} total issues")
```

### Step 2: Clean

```python
cleaned = TmxFile(source_lang=tmx.header.source_lang)

for tu in tmx.body.translation_units:
    score = quality_score(source_seg, target_seg)

    if score >= 70:  # Threshold
        cleaned.body.add_translation_unit(tu)

cleaned.write("cleaned.tmx")
```

### Step 3: Manual Review

Export flagged segments to Excel for human review:

```python
flagged_df = pd.DataFrame(flagged_segments)
flagged_df.to_excel("review.xlsx")
```

Translators review, correct issues, re-import.

## Best Practices

1. **Regular Cleaning:** Schedule quarterly TM cleanup
2. **Pre-delivery:** Clean TM before client handoff
3. **Version Control:** Keep pre-cleaning version as backup
4. **Quality Thresholds:** Use consistent scoring criteria
5. **Human Review:** Automated tools flag, humans decide

## Sources

- [Translation Memory (TM) Clean Up - Inten.to](https://inten.to/translation-memory-cleanup/)
- [The first Automatic Translation Memory Cleaning Shared Task](https://dl.acm.org/doi/10.1007/s10590-016-9183-x)
- [Automatic translation memory cleaning | Machine Translation](https://link.springer.com/article/10.1007/s10590-017-9191-5)
- [Translation Memory and Term Base Tune-up - ChilliStore](https://www.chillistore.com/blog/translation-memory-and-term-base-tune-up/)
- [Cleaning up and harmonizing your translation memory - tcworld](https://www.tcworld.info/e-magazine/translation-and-localization/cleaning-up-and-harmonizing-your-translation-memory-822/)
- [GitHub - TMOP](https://github.com/hlt-mt/TMOP)
- [TMop: a Tool for Unsupervised Translation Memory Cleaning](https://aclanthology.org/P16-4009.pdf)
- [Translation Memory Quality – Phrase](https://support.phrase.com/hc/en-us/articles/9386879702044-Translation-Memory-Quality)
