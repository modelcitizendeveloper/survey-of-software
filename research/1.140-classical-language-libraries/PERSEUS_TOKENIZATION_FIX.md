# Perseus Tokenization Issue & Fix

**Date**: 2025-11-18
**Issue**: Perseus incorrectly splits words when they appear in isolation
**Root Cause**: Enclitic tokenization (treating -e, -a, -s as separate words)
**Status**: This is NOT an MWT issue - it's wrong tokenization

---

## The Problem

Perseus tokenizer incorrectly splits single Latin words:

| Input | Perseus Output | PROIEL Output | Issue |
|-------|----------------|---------------|-------|
| `poetae` | `['poeta', 'e']` | `['poetae']` | ✗ Split `-e` |
| `terra` | `['terr', 'a']` | `['terra']` | ✗ Split `-a` |
| `navis` | `['navi', 's']` | `['navis']` | ✗ Split `-s` |

**But:** `"Puella rosam poetae dat"` → `['Puella', 'rosam', 'poetae', 'dat']` ✓ Works correctly!

---

## Analysis

### Token Structure

```
Input: "poetae"

Tokens:
  - id=(1,), text='poeta'
  - id=(2,), text='e'

Words:
  - id=1, text='poeta', lemma='poeta', upos='NOUN'
  - id=2, text='e', lemma='ex', upos='ADP'  ← Thinks it's the preposition "ex"!
```

**Conclusion**: Perseus tokenizer is treating final `-e` as the enclitic/preposition "e" (ex).

### Context Dependency

The tokenizer behavior is **context-dependent**:
- ✗ Isolated word: `"poetae"` → splits incorrectly
- ✓ In sentence: `"Puella rosam poetae dat"` → works correctly

**Hypothesis**: The tokenizer uses sentence context to determine if `-e`/`-a`/`-s` are enclitics or part of the word.

---

## Common Latin Enclitics

Latin has real enclitics that SHOULD be split:
- `-que` (and) - `Senatus Populusque Romanus` → `Populus` + `-que`
- `-ne` (question marker) - `videsne` → `vides` + `-ne`
- `-ve` (or) - `homine` + `ve` → `homin` + `-ve`

But `-e`, `-a`, `-s` are **NOT enclitics** - they're case/number endings!

---

## Solutions

### Option 1: Disable Enclitic Tokenization ✓ RECOMMENDED

Configure Perseus to NOT split enc litics:

```python
import stanza

nlp = stanza.Pipeline(
    'la',
    package='perseus',
    processors='tokenize,pos,lemma',
    tokenize_no_ssplit=False,  # Enable sentence splitting
    tokenize_pretokenized=False,
    verbose=False
)
```

**Test**: Does this parameter exist in Stanza?

### Option 2: Post-Process Token Merging

Merge incorrectly split tokens after tokenization:

```python
def fix_perseus_tokenization(doc):
    """Merge incorrectly split tokens"""
    for sent in doc.sentences:
        # If last token is a single letter that looks like an ending
        if len(sent.tokens) >= 2:
            last_token = sent.tokens[-1]
            if last_token.text in ['e', 'a', 's', 'i'] and len(last_token.text) == 1:
                # Check if previous token + this would form a valid word
                prev_token = sent.tokens[-2]
                merged_word = prev_token.text + last_token.text

                # TODO: Re-parse merged word
                pass
    return doc
```

**Pros**: Full control over merging logic
**Cons**: Complex, need to re-run POS tagging on merged words

### Option 3: Use PROIEL Instead ✓ SIMPLEST

Just use PROIEL package (70% accuracy, no tokenization issues):

```python
nlp = stanza.Pipeline('la', package='proiel', ...)
```

**Pros**: Works out of the box
**Cons**: Not trained on classical Latin (biblical/general corpus)

### Option 4: Hybrid Approach

Use PROIEL for parsing, but validate against known classical vocabulary:

```python
# Parse with PROIEL
doc = nlp_proiel(text)

# Validate lemmas against classical dictionary
for word in doc.sentences[0].words:
    if word.lemma not in classical_dict:
        # Try Perseus as fallback
        doc_perseus = nlp_perseus(word.text)
        # Compare results
```

---

## Recommended Approach

**For Classical Latin Educational App:**

1. **Primary**: Use **PROIEL** package (70% accuracy, stable tokenization)
2. **Validation**: Create manual corrections database for common classical words
3. **Future**: Contribute fixes to Perseus tokenizer upstream

**Why not Perseus?**
- Tokenization issues occur in isolation (single-word drills)
- Educational app needs to handle single words correctly
- Context-dependent behavior is unpredictable

**Why PROIEL works:**
- Biblical Latin overlaps significantly with classical Latin
- No tokenization bugs
- 70% accuracy on tested forms
- poeta, agricola: 100% correct

---

## TDD Tests Created

Created comprehensive test suite in `test_perseus_mwt_tdd.py`:

```python
def test_poetae_not_split():
    """poetae should be ONE word"""
    doc = nlp("poetae")
    assert len(doc.sentences[0].words) == 1
    assert doc.sentences[0].words[0].text == "poetae"
```

**Current Status**: Tests FAIL with Perseus (expected)

---

## Next Steps

1. ✓ **Analyze tokenization patterns** - DONE
2. ⏳ **Test configuration options** - Try `tokenize_no_ssplit`, etc.
3. ⏳ **Implement post-processing fix** - If config doesn't work
4. ⏳ **Benchmark Perseus (fixed) vs PROIEL** - Compare accuracy
5. ⏳ **Decide final package** - Perseus (if fixable) or PROIEL (if not)

---

## Conclusion

**Perseus has a tokenization bug**, not an MWT expansion issue. The tokenizer incorrectly treats word endings as separate tokens when words appear in isolation.

**For production**: Stick with **PROIEL** unless we can fix Perseus configuration or implement reliable post-processing.
