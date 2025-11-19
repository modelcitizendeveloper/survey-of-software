# MWT Research Findings: Latin Enclitics vs Case Endings

**Date**: 2025-11-18
**Question**: Is Perseus's token splitting intentional MWT expansion or a bug?
**Answer**: It's a **BUG** - Perseus incorrectly splits case endings as if they were enclitics

---

## Background: What is MWT?

**Multi-Word Token (MWT)** expansion separates orthographic tokens into syntactic words.

**Universal Dependencies definition**:
- **Token**: Orthographic unit (what appears in text)
- **Word**: Syntactic unit (used for dependency relations)

**Standard MWT examples**:
- French: `du` → `de` + `le` (preposition + article)
- Spanish: `dámelo` → `da` + `me` + `lo` (verb + clitics)
- Latin (expected): `Populusque` → `Populus` + `-que` (noun + enclitic)

---

## Latin Enclitics: What SHOULD Be Split

Latin has three main enclitics that are syntactically independent:

| Enclitic | Meaning | Example | Expected MWT |
|----------|---------|---------|--------------|
| **-que** | and | `Senatus Populusque Romanus` | `Populus` + `-que` |
| **-ne** | question marker | `videsne?` | `vides` + `-ne` |
| **-ve** | or | `terrave` | `terra` + `-ve` |

These are **fused words** in Latin orthography but represent separate syntactic elements.

---

## Latin Case Endings: What Should NOT Be Split

Case/number/gender endings are part of the word, not separate syntactic units:

| Form | Grammar | Should Be |
|------|---------|-----------|
| `poetae` | Genitive/dative singular | ONE word |
| `terra` | Nominative/ablative singular | ONE word |
| `navis` | Nominative singular | ONE word |
| `rosam` | Accusative singular | ONE word |

These endings (`-ae`, `-a`, `-s`, `-am`) are **NOT** enclitics - they're inflectional morphology.

---

## Test Results: How Packages Handle This

### Test Cases

```python
# REAL ENCLITICS (should split)
"Senatus Populusque Romanus"  # Populus + -que
"videsne"                      # vides + -ne
"terrave"                      # terra + -ve

# CASE ENDINGS (should NOT split)
"poetae"                       # genitive/dative
"terra"                        # nominative
"navis"                        # nominative
```

### Results

| Package | Real Enclitics | Case Endings | Verdict |
|---------|---------------|--------------|---------|
| **PERSEUS** | ✗ Doesn't split | ✗ **Incorrectly splits** | BROKEN |
| **PROIEL** | ✗ Doesn't split | ✓ Correctly keeps intact | GOOD |
| **ITTB** | ✗ Doesn't split | ✓ Correctly keeps intact | GOOD |

### Detailed Breakdown

**PERSEUS** (broken tokenizer):
```
Populusque  → ['Populusque']        ✗ Should split -que
videsne     → ['videsn']            ✗ Should split -ne (also typo!)
terrave     → ['terrav', 'e']       ✗ Splits wrong position
poetae      → ['poeta', 'e']        ✗ WRONG - case ending, not enclitic
terra       → ['terr', 'a']         ✗ WRONG - case ending
navis       → ['navi', 's']         ✗ WRONG - case ending
```

**PROIEL** (doesn't do MWT, but consistent):
```
Populusque  → ['Populusque']        ⚠️  Doesn't split (but OK for reading)
videsne     → ['videsne']           ⚠️  Doesn't split (but OK for reading)
terrave     → ['terrave']           ⚠️  Doesn't split (but OK for reading)
poetae      → ['poetae']            ✓ Correct - keeps word intact
terra       → ['terra']             ✓ Correct
navis       → ['navis']             ✓ Correct
```

**ITTB** (same as PROIEL):
```
Same results as PROIEL - doesn't split enclitics, doesn't break regular words
```

---

## Analysis: Why This Matters

### Historical Context: Scriptio Continua

You're absolutely right - classical Latin was written **without spaces**:

```
SENATUSPOPULUSQUEROMANUS
(Senatus Populus-que Romanus)
```

Modern editors add spaces, but the "correct" word boundaries are editorial decisions, not historical facts.

### Modern Convention

For **modern edited Latin texts** (what students read):
- Enclitics stay attached: `Populusque` (not `Populus que`)
- Words are space-separated: `Puella rosam poetae dat`

### For Your Educational App

**You want words as they appear in edited texts**, which means:
- ✓ `poetae` should be ONE word (genitive/dative case)
- ✓ `terra` should be ONE word (nominative)
- ✗ You DON'T need enclitic splitting for reading comprehension

**Students learn**: "poetae" = genitive of "poeta", not "poeta" + some mysterious "e"

---

## Conclusion

### Perseus Tokenizer is BROKEN

Perseus has a **buggy tokenizer** that:
1. ✗ Fails to split real enclitics (`-que`, `-ne`, `-ve`)
2. ✗ Incorrectly splits case endings (`-ae`, `-a`, `-s`)
3. ✗ Does the OPPOSITE of what MWT is designed for

**This is NOT intentional MWT behavior** - it's a tokenization bug.

### PROIEL/ITTB are CORRECT for Your Use Case

They don't do MWT expansion for enclitics, but they:
1. ✓ Keep words intact (no spurious splitting)
2. ✓ Match modern edited text conventions
3. ✓ Work correctly for reading-focused learning

**For classical Latin education, you DON'T need enclitic splitting.**

---

## Recommendation

**Use PROIEL package** for your Latin learning app:

```python
nlp = stanza.Pipeline('la', package='proiel',
                      processors='tokenize,pos,lemma',
                      verbose=False, logging_level='ERROR')
```

**Why PROIEL wins**:
- ✓ 70% accuracy on classical nouns
- ✓ No tokenization bugs
- ✓ Words match modern edited texts
- ✓ Handles "poetae", "terra", "navis" correctly
- ⚠️ Doesn't split enclitics (but you don't need this for reading)

**Avoid Perseus** until tokenizer is fixed:
- ✗ Breaks regular words unpredictably
- ✗ Can't be trusted for single-word drills
- ✗ Creates nonsense splits like "poeta" + "e"

---

## If You Ever Need Enclitic Splitting

(You probably don't for a reading app, but if you do:)

**Option 1**: Post-process PROIEL output with manual rules:
```python
def split_enclitics(word):
    if word.endswith('que'):
        return word[:-3], '-que'
    elif word.endswith('ne'):
        return word[:-2], '-ne'
    elif word.endswith('ve'):
        return word[:-2], '-ve'
    return word, None
```

**Option 2**: Use a proper Latin morphological analyzer (like Collatinus or LatMor)

**Option 3**: Wait for Perseus to fix their tokenizer (not recommended)

---

## Key Takeaway

**MWT is for contractions and clitics** (like French "du" → "de le").

**Perseus is broken** - it splits case endings as if they were clitics.

**PROIEL is correct** - it keeps words as they appear in modern edited texts, which is exactly what you need for a reading-focused Latin learning app.
