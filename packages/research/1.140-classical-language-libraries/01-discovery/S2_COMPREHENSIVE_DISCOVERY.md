# S2: Comprehensive Discovery - Classical Language Libraries

**Methodology**: Comprehensive Discovery (S2)
**Time Budget**: 3-4 hours
**Goal**: Deep technical validation, performance testing, edge case analysis

**Focus**: CLTK (winner from S1)

---

## Test Plan

### 1. API Deep Dive (30 min)
- Explore `decline()` parameters: flatten, collatinus_dict
- Test all methods on CollatinusDecliner
- Understand grammatical code format
- Test lemmas database access

### 2. Performance Benchmarking (30 min)
- Declension generation speed (1, 10, 100, 1000 words)
- Lemmatization speed
- Memory usage patterns
- Initialization overhead

### 3. Edge Cases & Error Handling (45 min)
- Unknown/invalid words
- Misspelled words
- Irregular nouns (if any)
- Mixed case input
- Empty strings, special characters
- Non-Latin characters

### 4. Coverage Testing (30 min)
- Test irregular nouns (corpus, os, vis, etc.)
- Test Greek loanwords (basis, crisis, poesis)
- Test defective nouns (only certain cases exist)
- Test indeclinable words

### 5. Verb Conjugation Research (60 min)
- Deep dive into latin_verb_patterns
- Reverse-engineer pattern system
- Research external verb conjugation data sources
- Prototype custom conjugator concept

### 6. Integration Patterns (30 min)
- Quiz generation workflow
- Answer validation workflow
- Error messages for users
- Database storage patterns

---

## 1. API Deep Dive

### CollatinusDecliner Parameters

**Signature**: `decline(lemma: str, flatten: bool = False, collatinus_dict: bool = False)`

#### Test: flatten parameter

**Purpose**: Unknown - test to discover

```python
from cltk.morphology.lat import CollatinusDecliner

decliner = CollatinusDecliner()

# Test with flatten=False (default)
forms_nested = decliner.decline("puella", flatten=False)
print(f"flatten=False: {type(forms_nested)}, length: {len(forms_nested)}")
print(f"First 3 items: {forms_nested[:3]}")

# Test with flatten=True
forms_flat = decliner.decline("puella", flatten=True)
print(f"flatten=True: {type(forms_flat)}, length: {len(forms_flat)}")
print(f"First 3 items: {forms_flat[:3]}")
```

**Results**:
```
[PASTE RESULTS HERE]
```

**Analysis**:
- flatten=False returns: [description]
- flatten=True returns: [description]
- Use case: [when to use which]

#### Test: collatinus_dict parameter

```python
# Test with collatinus_dict=False (default)
forms_standard = decliner.decline("puella", collatinus_dict=False)

# Test with collatinus_dict=True
forms_collatinus = decliner.decline("puella", collatinus_dict=True)

print(f"Standard format: {forms_standard[:2]}")
print(f"Collatinus format: {forms_collatinus[:2]}")
```

**Results**:
```
[PASTE RESULTS HERE]
```

#### Test: lemmas attribute

```python
# Check if we can access the lemma database
print(f"decliner.lemmas type: {type(decliner.lemmas)}")
print(f"Number of lemmas: {len(decliner.lemmas) if hasattr(decliner.lemmas, '__len__') else 'N/A'}")

# Try to lookup a specific lemma
if hasattr(decliner.lemmas, 'get') or hasattr(decliner.lemmas, '__getitem__'):
    print("Lemma lookup available")
    # Try accessing
```

**Results**:
```
[PASTE RESULTS HERE]
```

### Grammatical Code Deep Dive

**Format**: `--s----n-` (example)

**Documented positions**:
- Position 3: s=singular, p=plural
- Position 8: n=nom, v=voc, a=acc, g=gen, d=dat, b=abl

**Unknown positions**: 1, 2, 4, 5, 6, 7, 9

**Research**: Test various nouns to decode full format

```python
# Test different genders
masculine = decliner.decline("dominus")  # masculine
feminine = decliner.decline("puella")    # feminine
neuter = decliner.decline("templum")     # neuter

# Compare codes to identify gender position
print("Masculine codes:", [code for form, code in masculine])
print("Feminine codes:", [code for form, code in feminine])
print("Neuter codes:", [code for form, code in neuter])
```

**Code format hypothesis**:
```
Position 1: [unknown]
Position 2: [unknown]
Position 3: number (s/p)
Position 4: [unknown]
Position 5: [unknown - tense for verbs?]
Position 6: [unknown - mood for verbs?]
Position 7: [unknown - voice for verbs?]
Position 8: case (n/v/a/g/d/b)
Position 9: [unknown - gender?]
```

**Results**:
```
[PASTE ANALYSIS HERE]
```

---

## 2. Performance Benchmarking

### Test Setup

```python
import time
from cltk.morphology.lat import CollatinusDecliner

decliner = CollatinusDecliner()

# Test words (mix of declensions)
test_words = [
    "puella",   # 1st
    "dominus",  # 2nd masc
    "templum",  # 2nd neut
    "rex",      # 3rd
    "manus",    # 4th
    "res",      # 5th
]
```

### Benchmark 1: Single word declension

```python
# Warm-up
decliner.decline("puella")

# Actual test
start = time.perf_counter()
forms = decliner.decline("puella")
elapsed = time.perf_counter() - start

print(f"Single declension: {elapsed*1000:.2f} ms")
print(f"Forms generated: {len(forms)}")
```

**Results**:
```
Single declension: ___ ms
Forms generated: ___
```

### Benchmark 2: Batch declensions (10 words)

```python
start = time.perf_counter()
for word in test_words * 2:  # 12 words total
    forms = decliner.decline(word)
elapsed = time.perf_counter() - start

print(f"10 declensions: {elapsed*1000:.2f} ms")
print(f"Average per word: {elapsed*1000/12:.2f} ms")
```

**Results**:
```
10 declensions: ___ ms
Average: ___ ms/word
```

### Benchmark 3: Large batch (100 words)

```python
large_batch = test_words * 17  # ~100 words

start = time.perf_counter()
for word in large_batch:
    forms = decliner.decline(word)
elapsed = time.perf_counter() - start

print(f"100 declensions: {elapsed*1000:.2f} ms")
print(f"Average: {elapsed*1000/len(large_batch):.2f} ms/word")
```

**Results**:
```
100 declensions: ___ ms
Average: ___ ms/word
Throughput: ___ words/second
```

### Benchmark 4: Initialization overhead

```python
# Test decliner initialization time
start = time.perf_counter()
new_decliner = CollatinusDecliner()
init_time = time.perf_counter() - start

print(f"Initialization time: {init_time*1000:.2f} ms")
```

**Results**:
```
Initialization: ___ ms
```

### Benchmark 5: Lemmatization speed

```python
from cltk.lemmatize.lat import LatinBackoffLemmatizer

lemmatizer = LatinBackoffLemmatizer()

verb_forms = ['amo', 'amas', 'amat', 'amabam', 'amavi', 'veni', 'vidi', 'vici']

start = time.perf_counter()
for form in verb_forms * 10:  # 80 lemmatizations
    lemma = lemmatizer.lemmatize([form])
elapsed = time.perf_counter() - start

print(f"80 lemmatizations: {elapsed*1000:.2f} ms")
print(f"Average: {elapsed*1000/80:.2f} ms/word")
```

**Results**:
```
80 lemmatizations: ___ ms
Average: ___ ms/word
```

### Performance Summary

| Operation | Single | Batch (10) | Batch (100) | Notes |
|-----------|--------|------------|-------------|-------|
| Declension | ___ ms | ___ ms | ___ ms | |
| Lemmatization | ___ ms | ___ ms | ___ ms | |
| Initialization | ___ ms | N/A | N/A | One-time cost |

**Assessment**:
- Fast enough for interactive quiz? (target: <100ms) YES/NO
- Suitable for batch generation? YES/NO
- Caching needed? YES/NO

---

## 3. Edge Cases & Error Handling

### Test 1: Unknown words

```python
unknown_words = [
    "foobar",      # Nonsense
    "computer",    # English word
    "pizza",       # Modern Italian
]

for word in unknown_words:
    try:
        forms = decliner.decline(word)
        print(f"{word}: {len(forms)} forms - {forms[:2]}")
    except Exception as e:
        print(f"{word}: ERROR - {type(e).__name__}: {e}")
```

**Results**:
```
[PASTE RESULTS]
```

**Behavior**:
- Returns empty list? YES/NO
- Throws exception? YES/NO
- Returns similar words? YES/NO

### Test 2: Misspelled words

```python
misspelled = [
    "puella",   # correct
    "puela",    # missing 'l'
    "puellaa",  # extra 'a'
    "PUELLA",   # uppercase
    "Puella",   # capitalized
]

for word in misspelled:
    forms = decliner.decline(word)
    print(f"{word}: {len(forms)} forms")
```

**Results**:
```
[PASTE RESULTS]
```

**Case sensitivity**: YES/NO
**Typo tolerance**: YES/NO

### Test 3: Invalid input

```python
invalid_inputs = [
    "",          # empty string
    " ",         # whitespace
    "123",       # numbers
    "puella123", # mixed
    "puel-la",   # hyphen
    "puélla",    # accented
]

for word in invalid_inputs:
    try:
        forms = decliner.decline(word)
        print(f"'{word}': {len(forms)} forms")
    except Exception as e:
        print(f"'{word}': ERROR - {type(e).__name__}")
```

**Results**:
```
[PASTE RESULTS]
```

### Test 4: Lemmatization edge cases

```python
from cltk.lemmatize.lat import LatinBackoffLemmatizer
lemmatizer = LatinBackoffLemmatizer()

edge_cases = [
    "foobar",    # unknown word
    "sum",       # irregular verb
    "est",       # irregular verb form
    "AMAT",      # uppercase
]

for word in edge_cases:
    lemma = lemmatizer.lemmatize([word])
    print(f"{word}: {lemma}")
```

**Results**:
```
[PASTE RESULTS]
```

---

## 4. Coverage Testing

### Irregular Nouns

```python
# Test known irregular or special nouns
irregular_nouns = [
    "vis",      # force (irregular 3rd declension)
    "bos",      # ox (irregular 3rd)
    "domus",    # house (mixed 2nd/4th declension)
    "Iuppiter", # Jupiter (irregular)
    "os",       # bone (3rd declension neuter)
    "corpus",   # body (3rd declension neuter)
]

for noun in irregular_nouns:
    try:
        forms = decliner.decline(noun)
        print(f"\n{noun}:")
        for form, code in forms[:6]:  # Show first 6
            print(f"  {code} {form}")
    except Exception as e:
        print(f"{noun}: ERROR - {e}")
```

**Results**:
```
[PASTE RESULTS]
```

**Irregular handling**: GOOD/FAIR/POOR

### Greek Loanwords

```python
greek_words = [
    "basis",    # basis
    "crisis",   # crisis
    "poesis",   # poetry
    "analysis", # analysis
]

for word in greek_words:
    forms = decliner.decline(word)
    print(f"{word}: {len(forms)} forms")
    if forms:
        print(f"  Sample: {forms[0]}")
```

**Results**:
```
[PASTE RESULTS]
```

### Defective/Indeclinable

```python
defective = [
    "fas",      # divine law (indeclinable)
    "nefas",    # sacrilege (indeclinable)
]

for word in defective:
    forms = decliner.decline(word)
    print(f"{word}: {len(forms)} forms")
```

**Results**:
```
[PASTE RESULTS]
```

---

## 5. Verb Conjugation Research

*[TO BE COMPLETED]*

### latin_verb_patterns Analysis

**Total patterns**: 99

**Categories to identify**:
- Present tense patterns
- Imperfect patterns
- Perfect patterns
- Future patterns
- Subjunctive patterns

**Reverse engineering approach**:
[RESEARCH NOTES]

### External Data Sources

**Option 1**: Wiktionary data
**Option 2**: Custom conjugation tables
**Option 3**: Build from CLTK patterns

**Decision**: [TBD]

---

## 6. Integration Patterns

*[TO BE COMPLETED]*

### Quiz Generation Workflow

```python
# Pseudocode for quiz generation
def generate_declension_quiz(word, target_case, target_number):
    # 1. Get all forms
    forms = decliner.decline(word)

    # 2. Find target form
    target_form = find_form(forms, target_case, target_number)

    # 3. Generate distractors (wrong answers)
    distractors = generate_distractors(forms, target_form)

    # 4. Return quiz
    return {
        'question': f"What is the {target_case} {target_number} of {word}?",
        'correct_answer': target_form,
        'options': shuffle([target_form] + distractors)
    }
```

---

## S2 Status

**Started**: 2025-11-17
**Estimated completion**: [TBD]
**Time spent**: ___ hours

**Sections complete**:
- [ ] 1. API Deep Dive
- [ ] 2. Performance Benchmarking
- [ ] 3. Edge Cases
- [ ] 4. Coverage Testing
- [ ] 5. Verb Research
- [ ] 6. Integration Patterns
