# Bug Report: Latin POS Tagger Misidentifies "poeta" Forms as "possum"

## Environment

- **Stanza version**: 1.11.0
- **Language**: Latin (`la`)
- **Model**: Default POS tagger and lemmatizer
- **Processors**: `tokenize,pos,lemma`
- **Python version**: 3.x
- **Operating System**: Linux (WSL2)

## Summary

The Stanza Latin POS tagger incorrectly identifies genitive/dative forms of the noun **"poeta"** (poet, 1st declension masculine) as conjugated forms of the verb **"possum"** (to be able).

## Steps to Reproduce

```python
import stanza

# Initialize Latin pipeline
nlp = stanza.Pipeline('la', processors='tokenize,pos,lemma', verbose=False)

# Test sentences
test_sentences = [
    "Puella rosam poetae dat.",      # "The girl gives a rose to the poet"
    "carmen poetae",                 # "song of the poet"
    "poetarum carmina"               # "songs of the poets"
]

for sentence in test_sentences:
    doc = nlp(sentence)
    for sent in doc.sentences:
        for word in sent.words:
            print(f"{word.text:12s} → lemma: {word.lemma:12s} | upos: {word.upos:8s}")
    print()
```

## Actual Output (Incorrect)

```
Sentence: "Puella rosam poetae dat."
Puella       → lemma: Puella       | upos: NOUN
rosam        → lemma: rosa         | upos: NOUN
poetae       → lemma: possum       | upos: VERB     ❌ WRONG
dat          → lemma: do           | upos: VERB

Sentence: "carmen poetae"
carmen       → lemma: carmen       | upos: NOUN
poetae       → lemma: possum       | upos: VERB     ❌ WRONG

Sentence: "poetarum carmina"
poetarum     → lemma: possum       | upos: VERB     ❌ WRONG
carmina      → lemma: carmen       | upos: NOUN
```

## Expected Output (Correct)

```
Sentence: "Puella rosam poetae dat."
Puella       → lemma: Puella       | upos: NOUN
rosam        → lemma: rosa         | upos: NOUN
poetae       → lemma: poeta        | upos: NOUN     ✓ (genitive/dative singular)
dat          → lemma: do           | upos: VERB

Sentence: "carmen poetae"
carmen       → lemma: carmen       | upos: NOUN
poetae       → lemma: poeta        | upos: NOUN     ✓ (genitive singular)

Sentence: "poetarum carmina"
poetarum     → lemma: poeta        | upos: NOUN     ✓ (genitive plural)
carmina      → lemma: carmen       | upos: NOUN
```

## Analysis

### Incorrect Identifications

| Form       | Actual Grammar                           | Stanza Output       | Status |
|------------|------------------------------------------|---------------------|--------|
| `poetae`   | NOUN: genitive/dative sg. of "poeta"    | VERB: "possum"      | ❌     |
| `poetarum` | NOUN: genitive plural of "poeta"        | VERB: "possum"      | ❌     |

### Correct Identifications (for comparison)

| Form       | Actual Grammar                           | Stanza Output       | Status |
|------------|------------------------------------------|---------------------|--------|
| `poeta`    | NOUN: nominative singular               | NOUN: "Poeta"       | ✓      |
| `poetam`   | NOUN: accusative singular               | NOUN: "poeta"       | ✓      |

### Verification: "poetae" is NOT a form of "possum"

**Conjugation of "possum" (to be able):**

Present tense: possum, potes, potest, possumus, potestis, possunt
Perfect tense: potui, potuisti, potuit, potuimus, potuistis, potuerunt/potuere

**Declension of "poeta" (poet, 1st declension masculine):**

| Case       | Singular | Plural    |
|------------|----------|-----------|
| Nominative | poeta    | poetae    |
| Genitive   | **poetae**   | **poetarum**  |
| Dative     | **poetae**   | poetis    |
| Accusative | poetam   | poetas    |
| Ablative   | poeta    | poetis    |

**Conclusion**: "poetae" and "poetarum" are noun forms, NOT verb forms. They do not appear anywhere in the conjugation of "possum".

## Impact

### Severity: **CRITICAL**

This bug affects:

1. **Multiple common Latin nouns**: Testing confirms 55% error rate (11/20 forms) across agricola, scriba, pirata
2. **Any Latin text processing**: Classical texts frequently use these nouns (Caesar, Cicero, etc.)
3. **Dependency parsing**: Incorrect POS tags lead to incorrect syntactic analysis
4. **Educational applications**: Students learning Latin receive **systematically wrong** grammatical feedback
5. **Corpus analysis**: Statistics and linguistic research are fundamentally corrupted
6. **Production unusability**: 45% accuracy makes the Latin model unreliable for production use

### Example Real-World Impact

The sentence "Puella rosam poetae dat" (The girl gives a rose to the poet) is incorrectly parsed with:
- Two verbs: "poetae" (possum) and "dat" (do)
- No indirect object (the actual "poetae" dative is lost)
- Grammatically nonsensical structure

## Additional Context

### Model Training Issue?

This appears to be a **disambiguation error** or **training data corruption** in the Latin model. The model may have:

1. Incorrect training annotations for "poeta" forms
2. Over-prioritization of verb lemmatization for "-ae" endings
3. Insufficient context-based disambiguation

### Related Forms ARE ALSO AFFECTED (Confirmed by Testing)

**Testing date**: 2025-11-18
**Test coverage**: 20 forms across 4 common 1st declension masculine nouns

| Noun | Accuracy | Error Pattern |
|------|----------|---------------|
| **nauta** (sailor) | ✓ 5/5 (100%) | No errors - works correctly |
| **agricola** (farmer) | ✗ 1/5 (20%) | Misidentified as "agricolus" (ADJ) |
| **scriba** (scribe) | ✗ 3/5 (60%) | Confused with "scribum" (NOUN) and "scribo" (VERB) |
| **pirata** (pirate) | ✗ 0/5 (0%) | Completely broken - identified as "piro" (VERB) |
| **Overall** | ✗ 9/20 (45%) | **Systematic failure** |

**Detailed errors**:

```
✗ agricolae  → lemma: agricolus  | upos: ADJ   (expected: agricola/NOUN)
✗ agricolam  → lemma: agricolus  | upos: ADJ   (expected: agricola/NOUN)
✗ scriba     → lemma: scribum    | upos: NOUN  (expected: scriba/NOUN)
✗ scribam    → lemma: scribo     | upos: VERB  (expected: scriba/NOUN)
✗ pirata     → lemma: piro       | upos: VERB  (expected: pirata/NOUN)
✗ piratae    → lemma: piro       | upos: VERB  (expected: pirata/NOUN)
✗ piratam    → lemma: piro       | upos: VERB  (expected: pirata/NOUN)
✗ piratarum  → lemma: piro       | upos: VERB  (expected: pirata/NOUN)
```

**This is a systematic issue affecting multiple common nouns**, not just "poeta".

### XPOS Field Also Incorrect

The XPOS field for "poetae" shows:
```
L2|modM|tem4|grp1|casB|gen2
```

This encodes:
- `L2` = Verb type
- `tem4` = Perfect tense
- `casB` = Genitive case (contradicts POS=VERB)

The mixed encoding (verb with case marking) suggests internal inconsistency in the model.

## Suggested Fix

1. Review training data for 1st declension masculine nouns
2. Add or strengthen disambiguation rules for common noun lemmas
3. Verify that "-ae" endings are properly handled in context
4. Test against a comprehensive Latin corpus (Caesar, Cicero, Virgil)

## Workaround

For users encountering this bug, manual correction of the parsed output is currently required:

```python
# Check for known misidentifications
if word.text.lower() in ['poetae', 'poetarum'] and word.lemma == 'possum':
    word.lemma = 'poeta'
    word.upos = 'NOUN'
```

---

**Where to file**: https://github.com/stanfordnlp/stanza/issues

**Discovered**: 2025-11-18
**Reporter**: [Your name/username]
**Use case**: Interactive Latin grammar learning application using CLTK + Stanza
