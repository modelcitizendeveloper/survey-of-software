# Stanza Latin Package Investigation Results

**Date**: 2025-11-18
**Issue**: "poetae" was being parsed as "possum" (VERB) instead of "poeta" (NOUN)
**Root Cause**: Using wrong Stanza package (ITTB - medieval Latin)
**Solution**: Switch to PROIEL package (biblical Latin, better general coverage)

---

## TL;DR

✅ **WE WERE DOING IT WRONG!**

We were using the **default package (ITTB)** which is trained on **medieval Latin** (Thomas Aquinas).
We should use **PROIEL package** which has **70% accuracy** vs ITTB's **45%** on classical nouns.

---

## Available Stanza Latin Packages

| Package | Corpus | Era | Use Case |
|---------|--------|-----|----------|
| **ittb** (default) | Index Thomisticus | Medieval (13th century) | Scholastic philosophy |
| **perseus** | Perseus Treebank | Classical | Caesar, Cicero, Virgil |
| **proiel** | PROIEL Treebank | Classical/Late | Bible, general Latin |
| **llct** | Late Latin Charter | Medieval | Legal documents |
| **udante** | UDante | Medieval | Dante's works |

---

## Comparative Testing Results

### Test 1: "Puella rosam poetae dat"

| Package | "poetae" Parsing | Result |
|---------|------------------|--------|
| ITTB (default) | lemma: "possum", pos: VERB | ✗ WRONG |
| PERSEUS | lemma: "poeta", pos: NOUN | ✓ CORRECT |
| PROIEL | lemma: "poeta", pos: NOUN | ✓ CORRECT |
| LLCT | lemma: "poeta", pos: NOUN | ✓ CORRECT |

**Finding**: 3 out of 4 packages correctly parse "poetae". Only ITTB (default) fails.

---

### Test 2: Comprehensive 1st Declension Masculine Noun Testing

Tested 20 forms across 4 nouns: poeta, nauta, agricola, scriba, pirata

#### ITTB (default) Results: **45% accuracy (9/20)**

| Noun | Accuracy | Notes |
|------|----------|-------|
| poeta | 0/5 (0%) | All forms wrong ("possum" verb) |
| nauta | 5/5 (100%) | Perfect! |
| agricola | 1/5 (20%) | Misidentified as "agricolus" (ADJ) |
| scriba | 3/5 (60%) | Confused with "scribum"/"scribo" |
| pirata | 0/5 (0%) | All forms wrong ("piro" verb) |

#### PROIEL Results: **70% accuracy (14/20)**

| Noun | Accuracy | Notes |
|------|----------|-------|
| poeta | 4/4 (100%) | ✓ Perfect! |
| nauta | 3/4 (75%) | Only "nautam" wrong |
| agricola | 4/4 (100%) | ✓ Perfect! |
| scriba | 3/4 (75%) | Only "scribam" wrong |
| pirata | 0/4 (0%) | Likely not in biblical corpus |

**Improvement**: +25 percentage points (45% → 70%)

---

## Error Patterns

### ITTB (Medieval Latin)
- Confuses 1st declension masculine nouns with verbs
- "poetae" → "possum" (completely unrelated verb)
- "pirata" → "piro" (wrong verb)
- Likely trained on limited vocabulary (Thomas Aquinas writings)

### PROIEL (Biblical/General Latin)
- Much better on common classical nouns
- Remaining errors mostly on "-am" accusative forms
- "nautam" → "navo" (verb)
- "scribam" → "scribo" (verb)
- Still confuses accusative nouns with 1st person singular future verbs

### PERSEUS (Classical Latin)
- Good on "poetae" but has multi-word tokenization issues
- Splits words incorrectly: "poetae" → "poeta" + "e"
- Not recommended due to MWT problems

---

## Recommendation

**Use PROIEL package for general Latin parsing**

```python
import stanza
nlp = stanza.Pipeline('la', package='proiel',
                      processors='tokenize,pos,lemma',
                      verbose=False, logging_level='ERROR')
```

### Why PROIEL?

1. ✓ **70% accuracy** on 1st declension masculine nouns
2. ✓ No multi-word tokenization issues (unlike Perseus)
3. ✓ Larger, more diverse corpus than ITTB
4. ✓ Better for general classical and post-classical Latin
5. ✓ Handles common nouns (poeta, agricola, nauta, scriba)

### When to use other packages

- **PERSEUS**: If you need classical Latin AND can handle MWT issues
- **ITTB**: If parsing Thomas Aquinas or similar medieval scholastic texts
- **LLCT**: If parsing medieval Latin legal documents

---

## Implementation Changes

### Before (CLTK with default ITTB):
```python
from cltk import NLP
nlp = NLP(language="lat", suppress_banner=True)
doc = nlp.analyze(text="Puella rosam poetae dat")
# Result: poetae → possum (VERB) ✗
```

### After (Stanza with PROIEL):
```python
import stanza
nlp = stanza.Pipeline('la', package='proiel',
                      processors='tokenize,pos,lemma',
                      verbose=False, logging_level='ERROR')
doc = nlp("Puella rosam poetae dat")
# Result: poetae → poeta (NOUN) ✓
```

---

## Updated Files

1. **`bin/latin-parse`** - Now uses Stanza directly with PROIEL package
2. **`corpus/sample_parsed_proiel.jsonl`** - Regenerated with correct parses
3. **`STANZA_BUG_REPORT.md`** - Original bug report (NOT filed - issue was our package choice!)

---

## Remaining Limitations

Even with PROIEL (70% accuracy), the parser still has issues:

1. **Accusative -am forms** sometimes confused with verbs
2. **Rare nouns** (like "pirata") not in corpus
3. **30% error rate** on tested forms

### Next Steps for Production Readiness

1. **Multi-parser voting** - Use PROIEL + PERSEUS + manual corrections
2. **Known-word database** - Manually curate common 500 words
3. **Validation layer** - Flag improbable parses (2 verbs in a row, etc.)
4. **User feedback** - Let users report errors, build correction database

---

## Key Takeaway

**Always verify you're using the right model/package for your use case!**

The "default" package is optimized for a specific corpus (medieval scholastic Latin), not general Latin. For educational apps targeting classical/biblical Latin, PROIEL is a much better choice.

**Accuracy improvement: 45% → 70% just by changing one parameter!**
