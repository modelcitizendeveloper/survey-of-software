# Morphological Analysis Libraries - Domain Explainer

**For**: Business stakeholders, non-linguists, developers new to NLP
**Purpose**: Understand what morphological analysis is and why it matters for language learning applications

---

## What is Morphological Analysis?

**Morphological analysis** breaks down words into their component parts and identifies grammatical features.

### Simple Example (English)

**Word**: "running"
- **Lemma** (base form): "run"
- **Part of Speech**: VERB
- **Features**: present participle, -ing form

**Word**: "cats"
- **Lemma**: "cat"
- **Part of Speech**: NOUN
- **Features**: plural, nominative case

---

## Why It Matters for Language Learning

### Problem: You Can't Learn Languages Word-by-Word

When you see "Я читаю книгу" (Russian: "I'm reading a book"), you need to know:
- **читаю** is the verb "читать" (to read) in 1st person singular
- **книгу** is the noun "книга" (book) in **accusative case** (direct object)

A dictionary won't help if you don't know the grammatical forms.

### Solution: Morphological Analysis

Parse the sentence to identify:
1. **Lemma** (dictionary form) - so you can look it up
2. **Part of speech** - noun, verb, adjective, etc.
3. **Grammatical features** - case, tense, number, gender, etc.

This lets the trainer ask: "What case is книгу?" (Answer: accusative)

---

## The Three Languages

### Japanese: 3 Scripts + Agglutinative Morphology

**Challenge**: Multiple scripts in one sentence
```
私は本を読んでいます
(watashi wa hon wo yonde imasu)
"I am reading a book"
```

**What we need**:
- **私** (watashi) → pronoun, "I"
- **は** (wa) → **particle** (topic marker)
- **本** (hon) → noun, "book"
- **を** (wo) → **particle** (direct object marker)
- **読んでいます** (yonde imasu) → verb "読む" (yomu, "to read") + present progressive form

**Key insight**: Particles are critical for understanding Japanese grammar.

---

### Russian: 6 Cases + Aspect System

**Challenge**: Case inflection changes word endings
```
Я читаю книгу в библиотеке
"I'm reading a book in the library"
```

**What we need**:
- **книгу** → "книга" (book), accusative case (direct object)
- **библиотеке** → "библиотека" (library), prepositional case (location)
- **читаю** → "читать" (to read), imperfective aspect, present tense

**Key insight**: Same word has 12 forms (6 cases × 2 numbers). You must identify which form you're seeing.

---

### Czech: 7 Cases + Complex Declension

**Challenge**: Even more complex than Russian
```
Čtu knihu v knihovně
"I'm reading a book in the library"
```

**What we need**:
- **knihu** → "kniha" (book), accusative case
- **knihovně** → "knihovna" (library), locative case (7th case!)
- **Čtu** → "číst" (to read), 1st person singular

**Key insight**: 7 cases (vs Russian's 6) + complex declension patterns.

---

## The Business Problem

### Without Morphological Analysis:
❌ Can't parse real text (only memorize vocabulary lists)
❌ Can't identify grammar patterns in context
❌ Limited to artificial examples (not authentic texts)
❌ Slow learning (decontextualized grammar drills)

### With Morphological Analysis:
✅ Parse Caesar, Pushkin, Japanese manga
✅ Identify grammar in real sentences
✅ Progressive difficulty (i+1 principle)
✅ Context-based learning (proven more effective)

---

## The Library Selection Problem

### Challenge: Each Language Has Different Ecosystems

**Japanese**:
- **MeCab**: Classic (2003), widely used, requires system dictionary
- **SudachiPy**: Modern (2017), better accuracy, pure Python
- **spaCy**: General NLP, moderate Japanese support

**Russian**:
- **pymorphy2**: Morphology specialist, excellent accuracy
- **spaCy**: General NLP, good Russian model
- **UDPipe**: Universal Dependencies, academic

**Czech**:
- **UDPipe**: Best Czech support (Universal Dependencies)
- **spaCy**: Experimental Czech model
- **MorphoDiTa**: Czech-specific, academic

### Decision Framework:

| Priority | Criterion | Why It Matters |
|----------|-----------|----------------|
| 1 | **Accuracy** | Wrong analysis = wrong training |
| 2 | **Installation** | pip install vs binary dependencies |
| 3 | **Performance** | Real-time parsing (<100ms/sentence) |
| 4 | **API consistency** | Same pattern across languages |
| 5 | **Maintenance** | Active development, bug fixes |

---

## Expected Output Format

### Goal: JSONL (like latin-parse)

```json
{
  "sentence": "私は本を読んでいます",
  "words": [
    {"text": "私", "lemma": "私", "pos": "PRON", "reading": "わたし"},
    {"text": "は", "lemma": "は", "pos": "ADP", "type": "particle"},
    {"text": "本", "lemma": "本", "pos": "NOUN", "reading": "ほん"},
    {"text": "を", "lemma": "を", "pos": "ADP", "type": "particle"},
    {"text": "読んでいます", "lemma": "読む", "pos": "VERB", "tense": "present", "reading": "よんでいます"}
  ]
}
```

This feeds into:
- **japanese-train**: Interactive trainer (latin-train pattern)
- **japanese-analyze**: Progress analysis (latin-analyze pattern)

---

## ROI: Why This Research Matters

### Time Investment:
- **Research**: 8-12 hours (library selection)
- **Implementation**: 20-30 hours per language (parser + trainer)
- **Total**: ~100 hours for 3-language system

### Value Created:
- **Reusable pattern** across all future languages
- **Context-based learning** (proven effective)
- **No ongoing costs** (self-hosted, no API fees)
- **Multi-language support** (Japanese, Russian, Czech immediately)
- **Extensible** (add Korean, Arabic, etc. with same pattern)

### Strategic Value:
- Validates **Path 1 (self-operated)** for language learning
- Creates **competitive moat** (most language apps don't parse real text)
- Enables **progressive corpus training** (i+1 principle)
- Foundation for **polyglot learning system**

---

## Success Criteria

**For each language**, we need:
1. ✅ Accurate morphological analysis (>90% lemma + POS accuracy)
2. ✅ pip installable (or minimal binary deps)
3. ✅ <100ms per sentence (real-time performance)
4. ✅ JSONL output format (consistent across languages)
5. ✅ Active maintenance (not abandoned projects)

**Overall**:
- Choose 1 library per language (Japanese, Russian, Czech)
- Prototype parser for each (japanese-parse, russian-parse, czech-parse)
- Validate with 10-20 real sentences per language
- Document trade-offs and limitations

---

## Questions This Research Answers

1. **Japanese**: MeCab vs SudachiPy vs spaCy?
2. **Russian**: pymorphy2 vs spaCy vs UDPipe?
3. **Czech**: UDPipe vs spaCy vs MorphoDiTa?
4. **Unified API**: Can we use spaCy for all three? Or per-language specialists?
5. **Installation**: Which libraries have minimal dependencies?
6. **Performance**: Which are fast enough for interactive training?
7. **Accuracy**: Which give correct morphological features?

---

## What Happens After This Research

### Immediate (Research Complete):
- Know which library to use for each language
- Understand installation + performance characteristics
- Clear decision: spaCy everywhere vs per-language specialists

### Next Steps (Implementation):
- **Experiment 1.950**: japanese-parse (MeCab/SudachiPy + JSONL)
- **Experiment 1.951**: russian-parse (pymorphy2/spaCy + JSONL)
- **Experiment 1.952**: czech-parse (UDPipe/spaCy + JSONL)

### Long-term (Application):
- **japanese-train**: Interactive Japanese grammar trainer
- **russian-train**: Interactive Russian grammar trainer
- **czech-train**: Interactive Czech grammar trainer
- **Multi-language app**: Unified language learning system

---

## Glossary

**Morphological analysis**: Breaking words into parts and identifying grammatical features

**Lemma**: Base form of word (dictionary entry)
Example: "running" → "run", "books" → "book"

**Part of Speech (POS)**: Grammatical category (noun, verb, adjective, etc.)

**Case**: Grammatical role in sentence (nominative=subject, accusative=object, etc.)
Russian/Czech have 6-7 cases; English has remnants (he/him, who/whom)

**Aspect**: Russian/Czech verbs have two forms:
- **Imperfective**: ongoing action (Я читаю - "I am reading")
- **Perfective**: completed action (Я прочитал - "I have read")

**Particle**: Japanese grammatical markers (は, が, を, に, etc.)
Indicate grammatical relationships without inflecting words

**Agglutinative** (Japanese): Grammar added by stacking suffixes
Example: 読む (read) → 読んでいます (reading now)

**Fusional** (Russian, Czech): Grammar encoded in word endings
Example: книга (book) → книгу (book-ACC), книге (book-PREP)

**JSONL**: JSON Lines format - one JSON object per line, easy to stream
