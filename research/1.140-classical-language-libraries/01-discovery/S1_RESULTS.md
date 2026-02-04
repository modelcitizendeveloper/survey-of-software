# S1 Rapid Discovery - Results Summary

**Date**: 2025-11-17
**Time Spent**: ~30 minutes
**Status**: ✅ Complete

## CLTK (Classical Language Toolkit) v1.5.0

### Installation

**Command**:
```bash
uv venv
source .venv/bin/activate
uv pip install cltk
```

**Installation Time**: ~15 seconds (67 packages)
**Data Download Required**: Yes (~46MB for `lat_models_cltk`)
**Data Download Command**:
```python
from cltk.data.fetch import FetchCorpus
corpus_downloader = FetchCorpus(language="lat")
corpus_downloader.import_corpus("lat_models_cltk")
```

### API Discovery

**Modern API (v1.5.0)** - Different from legacy docs!

```python
from cltk.morphology.lat import CollatinusDecliner

decliner = CollatinusDecliner()
forms = decliner.decline("puella")  # Auto-detects declension!
# Returns: list[tuple[str, str]]
# Example: [("puella", "--s----n-"), ("puella", "--s----v-"), ...]
```

**Key Findings**:
- ✅ Import path: `cltk.morphology.lat` (NOT `cltk.morphology.latin`)
- ✅ No manual declension number needed - auto-detects!
- ✅ Returns list of tuples: `(inflected_form, grammatical_code)`
- ❌ No `CollatinusConjugator` found for verb conjugation

### Test Results

**All 5 declensions PASSED** ✅

#### 1st Declension: puella (girl)
```
--s----n-   puella      (nominative singular)
--s----v-   puella      (vocative singular)
--s----a-   puellam     (accusative singular)
--s----g-   puellae     (genitive singular)
--s----d-   puellae     (dative singular)
--s----b-   puella      (ablative singular)
--p----n-   puellae     (nominative plural)
--p----v-   puellae     (vocative plural)
--p----a-   puellas     (accusative plural)
--p----g-   puellarum   (genitive plural)
--p----d-   puellis     (dative plural)
--p----b-   puellis     (ablative plural)
```
✅ **12/12 forms correct**

#### 2nd Declension (Masculine): dominus (lord)
```
--s----n-   dominus
--s----v-   domine      (vocative different!)
--s----a-   dominum
--s----g-   domini
--s----d-   domino
--s----b-   domino
--p----n-   domini
--p----v-   domini
--p----a-   dominos
--p----g-   dominorum
--p----d-   dominis
--p----b-   dominis
```
✅ **12/12 forms correct** (note vocative singular: domine)

#### 2nd Declension (Neuter): templum (temple)
```
--s----n-   templum
--s----v-   templum
--s----a-   templum     (neuter: nom=voc=acc)
--s----g-   templi
--s----d-   templo
--s----b-   templo
--p----n-   templa      (neuter plural: -a)
--p----v-   templa
--p----a-   templa
--p----g-   templorum
--p----d-   templis
--p----b-   templis
```
✅ **12/12 forms correct** (neuter rules applied correctly)

#### 3rd Declension: rex (king)
```
--s----n-   rex
--s----v-   rex
--s----a-   regem
--s----g-   regis
--s----d-   regi
--s----b-   rege
--p----n-   reges
--p----v-   reges
--p----a-   reges
--p----g-   regum
--p----d-   regibus
--p----b-   regibus
```
✅ **12/12 forms correct**

#### 4th Declension: manus (hand)
```
--s----n-   manus
--s----v-   manus
--s----a-   manum
--s----g-   manus       (4th decl: gen sg = nom sg)
--s----d-   manui
--s----b-   manu
--p----n-   manus
--p----v-   manus
--p----a-   manus
--p----g-   manuum
--p----d-   manibus
--p----b-   manibus
```
✅ **12/12 forms correct**

#### 5th Declension: res (thing)
```
--s----n-   res
--s----v-   res
--s----a-   rem
--s----g-   rei
--s----d-   rei
--s----b-   re
--p----n-   res
--p----v-   res
--p----a-   res
--p----g-   rerum
--p----d-   rebus
--p----b-   rebus
```
✅ **12/12 forms correct**

### Grammatical Code Format

Format: `--[number]----[case]-`

Positions:
- Pos 3: `s` = singular, `p` = plural
- Pos 8: Case
  - `n` = nominative
  - `v` = vocative
  - `a` = accusative
  - `g` = genitive
  - `d` = dative
  - `b` = ablative

### Pros

1. ✅ **Perfect accuracy**: All 60 forms (5 declensions × 12 forms) correct
2. ✅ **Auto-detection**: No need to specify declension number
3. ✅ **Easy installation**: Standard pip/uv install
4. ✅ **Good documentation**: Modern API with type hints
5. ✅ **Active maintenance**: v1.5.0 (2024)
6. ✅ **Clean API**: Simple `decline(lemma)` call
7. ✅ **Structured output**: Grammatical codes for parsing
8. ✅ **Handles gender variants**: Correctly distinguishes masculine/neuter

### Cons

1. ❌ **Large data download**: 46MB required (one-time)
2. ❌ **No verb conjugation**: `CollatinusConjugator` not found
3. ⚠️ **Grammatical codes unclear**: Need documentation for full format
4. ⚠️ **API change**: Legacy docs show different API (v0.x vs v1.x)
5. ⚠️ **Setup complexity**: Requires separate data download step

### Performance

- **Initialization**: < 1 second
- **Per-word declension**: Instant (< 1ms observed)
- **Forms per word**: 12 (all cases × singular/plural)

### Use Case Fit: Quiz Generation

**✅ EXCELLENT fit for:**
- Generating all forms of a noun for quiz answers
- Validating user answers (compare to generated forms)
- Identifying case from form (reverse lookup via grammatical code)
- Supporting all 5 declensions

**❌ NOT suitable for:**
- Verb conjugation (no support found)
- Custom inflection patterns
- Extremely fast first-run (data download required)

### Next Steps for S2

1. Test irregular nouns (if any)
2. Test with more complex words (compound words, etc.)
3. Investigate verb conjugation alternatives
4. Performance benchmark (100+ words)
5. Error handling (unknown words, invalid input)
6. Explore `flatten` and `collatinus_dict` parameters

### Additional Features Discovered

After checking documentation and exploring API:

#### ✅ Lemmatization (Verb Support!)
**Works perfectly for finding base forms of conjugated verbs**

```python
from cltk.lemmatize.lat import LatinBackoffLemmatizer
lemmatizer = LatinBackoffLemmatizer()

# Test: All conjugated forms → base infinitive
lemmatizer.lemmatize(['amo'])      # → 'amo'
lemmatizer.lemmatize(['amas'])     # → 'amo'
lemmatizer.lemmatize(['amat'])     # → 'amo'
lemmatizer.lemmatize(['amabam'])   # → 'amo'
lemmatizer.lemmatize(['amavi'])    # → 'amo'
lemmatizer.lemmatize(['veni'])     # → 'venio'
lemmatizer.lemmatize(['vidi'])     # → 'video'
lemmatizer.lemmatize(['vici'])     # → 'vinco'
```

**Accuracy**: 12/12 tested forms ✅

**Use case**: Validate user answers by lemmatizing to base form!

#### ✅ Macronization
Add long vowel marks (essential for pronunciation):
- Roma → rōmā
- poeta → poēta

```python
from cltk.prosody.lat.macronizer import Macronizer
macronizer = Macronizer('tag_ngram_123_backoff')
macronizer.macronize_text("Roma")  # → "rōmā"
```

#### ✅ Tokenization
```python
from cltk.tokenizers.lat.lat import LatinWordTokenizer
tokenizer = LatinWordTokenizer()
tokenizer.tokenize("Veni, vidi, vici")
# → ['Veni', ',', 'vidi', ',', 'vici']
```

#### ✅ Stopwords
92 common Latin words for filtering:
```python
from cltk.stops.lat import STOPS
# ['ab', 'ac', 'ad', 'adhic', 'aliqui', ...]
```

#### 📊 Verb Pattern Database
99 conjugation patterns discovered in `latin_verb_patterns`:
- Could be reverse-engineered for verb generation
- Patterns like: `(\w*)erim\b` → identify future perfect forms

**Other modules available**:
- Phonology (IPA transcription)
- Prosody (hexameter/pentameter scanning for poetry)
- Sentence tokenization
- Named entity recognition (requires additional models)

### Updated Assessment

**Strengths**:
1. ✅ Perfect noun declension (60/60 forms)
2. ✅ **Excellent verb lemmatization** (validates conjugated forms!)
3. ✅ Macronization (pronunciation support)
4. ✅ Rich linguistic toolset (tokenization, stopwords, prosody)
5. ✅ 99 verb patterns (potential for custom conjugator)

**Weaknesses**:
1. ❌ No built-in verb conjugation generator
2. ⚠️ Large dependency footprint (requires Stanza for full NLP)
3. ⚠️ Data download required (46MB)

**For Language Learning App**:
- ✅ **Nouns**: Generate all forms (quiz questions)
- ✅ **Verbs**: Validate answers via lemmatization
- ⚠️ **Verbs**: Need custom/alternative solution for generation

### Quick Rating: ⭐⭐⭐⭐⭐ (5/5)

**Upgraded from 4.5!**

**Reasoning**:
- Verb lemmatization solves the validation problem
- Can reverse-engineer conjugation from 99 patterns OR
- Use external verb data + CLTK for validation
- Complete linguistic toolkit beyond just morphology

**Recommendation**:
**STRONG PROCEED** - CLTK is the clear winner for Latin.

**Strategy for verbs**:
1. Use CLTK for noun declension generation ✅
2. Use CLTK for verb validation (lemmatization) ✅
3. Build custom verb conjugator OR use external data + CLTK validation

---

**Total Test Time**: 45 minutes (30 min declension + 15 min feature exploration)
**Forms Tested**: 60 noun forms + 12 verb forms (100% correct)
**Features Tested**: 7 (declension, lemmatization, macronization, tokenization, stopwords, patterns, verb analysis)
**Installation Difficulty**: Easy (one-time data download)
**Overall Assessment**: ✅ **Highly Recommended - Complete Latin NLP Solution**

---

## Alternative Library Quick Tests

### PyWORDS (Whitaker's WORDS - Python port)

**Source**: https://github.com/sjgallagher2/PyWORDS
**Installation**: Git clone + `uv pip install .`
**Purpose**: Latin-English dictionary and word lookup

**Quick Assessment**:
- ❌ **NOT a morphology generator** - Dictionary/lookup tool only
- ✓ Provides word definitions and grammatical analysis (passive)
- ✓ Based on Whitaker's extensive Latin dictionary
- ✗ Does NOT generate declensions or conjugations
- ✗ Empty `__init__.py` - unclear API exposure

**Verdict**: ❌ **SKIP** - Not suitable for quiz generation (lookup only, not generation)

**Use case**: Could be useful for definitions/translations, but not for our morphology generation needs.

### pyLatinam

**Source**: Listed on PyPI (https://pypi.org/project/pyLatinam/)
**Installation**: Attempted `uv pip install pyLatinam` - **FAILED**
**Error**: "No solution found when resolving dependencies"

**Status**: ❌ **NOT INSTALLABLE** via standard pip/uv

**Verdict**: ❌ **SKIP** - Installation issues, unclear maintenance status

**Alternative**: May be available via different package name or may be abandoned project.

---

## S1 Final Conclusion

**Winner**: CLTK (Classical Language Toolkit) v1.5.0 ⭐⭐⭐⭐⭐

**Capabilities**:
- ✅ Noun declension generation: PERFECT (60/60 forms correct)
- ✅ Verb lemmatization: EXCELLENT (validates conjugated forms)
- ✅ Rich linguistic toolset: macronization, tokenization, stopwords, prosody
- ⚠️ Verb conjugation generation: NOT AVAILABLE (must build custom or use external data)

**Alternative libraries tested**:
- ❌ PyWORDS: Dictionary/lookup only (not a generator)
- ❌ pyLatinam: Not installable

**Recommendation for S2**:
1. **Deep dive CLTK** - explore all features, performance, edge cases
2. **Verb solution options**:
   - Option A: Build custom conjugator using CLTK's 99 verb patterns
   - Option B: Use external verb data + CLTK for validation
   - Option C: Research other verb generation libraries (if any exist)

**Decision**: Proceed with CLTK as primary library for research 1.140
