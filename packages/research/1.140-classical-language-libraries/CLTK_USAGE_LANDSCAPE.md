# CLTK Usage Landscape & Our Novel Approach

**Research Area:** 1.140 - Classical Language Libraries
**Date:** 2025-01-18

---

## Executive Summary

CLTK (Classical Language Toolkit) is a powerful NLP library for pre-modern languages, but it's almost exclusively used for **academic corpus analysis**, not **interactive language learning**. We've identified a major gap and built something novel: real-time grammar training tools using Unix philosophy.

---

## What is CLTK?

### CLTK v1.x (Modern - What We Use)
- **Backend:** Stanza (Stanford NLP's deep learning models)
- **Languages:** Ancient Greek, Latin, Akkadian, Old French, Sanskrit, Classical Chinese, etc.
- **Models:** Pre-trained neural networks (~224MB for Latin)
- **API:** Simple one-liner: `NLP(language="lat")`
- **Accuracy:** Research-grade (trained on Universal Dependencies treebanks)
- **Recent (2024):** Added LLM integration (Ollama, GPT)

### CLTK v0 (Old - Obsolete)
- Manual POS training sets
- Bayesian backoff taggers, TnT, CRF
- Dictionary-based approaches
- Lower accuracy, manual configuration
- **Note:** Old documentation (v0.cltk.org) is obsolete - ignore it

---

## Current CLTK Usage (What Scholars Do)

### 1. Academic Corpus Analysis (Primary Use)
**Who:** Digital humanists, classicists, computational linguists
**What:**
- Analyzing entire Perseus Digital Library (~10M words)
- Stylometric studies (authorship, dating)
- Tracking linguistic patterns across centuries
- Example queries:
  - "How often does Cicero use ablative absolute vs Caesar?"
  - "Track evolution of passive voice from Classical to Medieval Latin"
  - "Find all instances of indirect discourse in Livy"

**Tools:**
- Batch processing of large corpora
- Statistical analysis (word frequencies, n-grams)
- Dependency treebanks (sentence structure annotations)

### 2. Digital Editions & Databases
**Projects:**
- **Perseus Digital Library:** Auto-linking words to dictionary entries
- **Tesserae Project:** Intertextual reference detection
- **Scaife Viewer:** Reading environment with annotations
- **DICES:** Dictionary of Classical Epic Similes (searchable DB)

**Workflow:**
1. Parse texts with CLTK
2. Store morphological annotations in database
3. Create web interface for scholars
4. Enable complex search queries

### 3. Resource Generation (Educational Support)
**Common Use Cases:**
- Generate vocabulary lists from difficult passages
- Create frequency-based word lists for textbooks
- Macronize texts (add long vowel marks)
- Export to Anki decks (but not interactive)
- Automated grammar reference tables

**Example:**
```python
# Parse Aeneid Book 1, export vocab by frequency
doc = nlp.analyze(text=aeneid_book1)
vocab = Counter([w.lemma for w in doc.words])
print(vocab.most_common(100))  # Top 100 words
```

### 4. Research Papers & Linguistics
**Recent Publications:**
- Oxford Academic: "Direct speech acts in Greek and Latin epic" (2022)
- Harvard Classics@: "Future of Ancient Literacy" (2017)
- Digital Classical Philology conferences

**Research Questions:**
- Morphological variation over time
- Syntactic complexity analysis
- Machine translation quality assessment
- Computational philology

---

## What's Missing (Our Niche)

### Nobody Is Building This

**Interactive Language Acquisition Tools:**
- ❌ Real-time grammar identification trainers
- ❌ Fluency-focused reading practice
- ❌ Rapid keyboard-driven interfaces
- ❌ Unix-style composable CLI tools for learners

**Why the Gap?**
1. **Different mindsets:**
   - Scholars think: "Analyze 1000 texts to find patterns"
   - We think: "Help me read this ONE sentence faster"

2. **Different goals:**
   - Research: Accuracy, comprehensiveness, reproducibility
   - Learning: Speed, fluency, immediate feedback

3. **Tool orientation:**
   - Academic: Batch processing, export to CSV/JSON
   - Our approach: Interactive loops, real-time validation

---

## Our Novel Approach

### 1. Interactive Grammar Trainer (Exercitatio Latina)
**What makes it unique:**
- Uses CLTK's research-grade NLP for **real-time feedback**
- Vim-like keyboard interface (n/v/a/p, 1-5 declension)
- Checks grammar **instantly** (not batch mode)
- Designed for **fluency** (rapid input, auto-advance)

**Innovation:**
```python
# Traditional CLTK usage (batch)
texts = load_corpus()
for text in texts:
    doc = nlp.analyze(text)
    export_to_database(doc)

# Our usage (interactive)
while training:
    sentence = get_next_sentence()
    doc = nlp.analyze(sentence)  # Pre-parsed
    user_answer = get_keyboard_input()  # Real-time
    check_correctness(user_answer, doc)  # Instant feedback
    advance_to_next_word()
```

### 2. Unix Philosophy for Language Learning
**Three composable utilities:**

**latin-parse** (Text → JSONL)
```bash
latin-parse caesar.txt > caesar_parsed.jsonl
```
- One-time parsing (slow)
- Cached results (instant retrieval)
- Portable, version-controllable

**latin-train** (Interactive Trainer)
```bash
latin-train caesar_parsed.jsonl --output attempts.jsonl --resume
```
- Reads pre-parsed sentences (no delay)
- Appends results (never overwrites)
- Resume from last position

**latin-analyze** (Statistics)
```bash
latin-analyze attempts.jsonl
latin-analyze attempts.jsonl --mistakes
latin-analyze attempts.jsonl --export srs.json
```
- Identifies confusion patterns
- Shows strengths/weaknesses
- Exports to SRS format

**Why this is novel:**
- **Files are the database** (no PostgreSQL needed)
- **Composable** (pipe to jq, grep, awk)
- **Fast** (pre-parsing strategy)
- **Portable** (git-friendly JSONL)

### 3. Fluency-First Design
**Traditional approach:**
- "Parse this text and tell me all the grammar"
- Focus: Comprehensive analysis

**Our approach:**
- "How fast can you identify this word's case?"
- Focus: Speed, automaticity, fluency

**Example workflow:**
```
# Traditional (slow, comprehensive)
1. Read sentence
2. Look up each word in dictionary
3. Identify all grammatical features
4. Write notes
5. Move to next sentence

# Our approach (fast, targeted)
1. See word
2. Type: n1n (NOUN, 1st declension, nominative)
3. Auto-advance (prepositions immediately advance)
4. Complete sentence in ~5 seconds
5. Instant feedback (✓/✗)
```

---

## Technical Comparison

### Standard CLTK Usage Pattern
```python
from cltk import NLP

nlp = NLP(language="lat")

# Batch process corpus
corpus = load_texts()
for text in corpus:
    doc = nlp.analyze(text=text)

    # Extract features
    for word in doc.words:
        features = {
            'lemma': word.lemma,
            'pos': word.upos,
            'xpos': word.xpos,
        }
        database.insert(features)

# Later: Query database
results = database.query("SELECT * WHERE pos='VERB'")
```

### Our Usage Pattern
```python
from cltk import NLP

nlp = NLP(language="lat", suppress_banner=True)

# Pre-parse once, save to file
sentences = parse_file("texts/caesar.txt")
for sentence in sentences:
    doc = nlp.analyze(text=sentence)
    save_to_jsonl(doc)  # Instant retrieval later

# Interactive training loop
doc = load_from_jsonl("sentence_001")  # No parsing delay!
for word in doc.words:
    user_input = get_keyboard_input()  # Real-time

    if correct(user_input, word):
        display_green_checkmark()
    else:
        display_red_x_with_correction()

    auto_advance_to_next_word()
```

---

## Why This Matters

### Gap in Language Learning Tools

**Current options:**
- **Duolingo:** Gamified, but no real Latin grammar depth
- **Textbooks:** Static exercises, no instant feedback
- **Flashcards (Anki):** Recognition only, not contextual
- **Reading apps:** Show translations, but don't train grammar identification

**What's missing:**
- Real-time grammar validation (we have this!)
- Fluency-focused practice (we have this!)
- Progressive difficulty (we're building this with training corpus)
- Spaced repetition integration (planned with latin-analyze --export)

### Academic → Practical Pipeline

**Research-grade tools → Learner-focused applications**

CLTK provides:
- Accurate POS tagging
- Morphological analysis
- Dependency parsing

We translate this into:
- "Is this nominative or accusative?" (instant answer)
- "Did I get the tense right?" (immediate feedback)
- "Where are my weak spots?" (pattern analysis)

---

## Future Directions

### 1. Training Corpus (1200+ Sentences)
- Progressive difficulty (nominative only → all 6 cases)
- Systematic coverage (prepositions, tenses, declensions)
- Integration with CLTK parsing

### 2. Fill-in-the-Blank Mode (Production Practice)
```
Prompt: puella, accusative singular
User types: puellam
Validation: CLTK CollatinusDecliner → ✓
```

### 3. i+1 Text Selection
- Calculate text difficulty (% known vocabulary)
- Filter to 75-85% comprehensibility
- Auto-recommend next texts

### 4. SRS Integration
- Export mistakes from latin-analyze
- Generate targeted review decks
- Track long-term retention

### 5. Multi-Language Expansion
- Same architecture for Ancient Greek
- French, Spanish, German (modern languages)
- Russian, Czech, Bosnian/Serbian/Croatian (Slavic)
- Japanese (kanji/grammar)

**Key insight:** Unix CLI tools are language-agnostic. We can use the same pattern:
```bash
greek-parse homer.txt > homer_parsed.jsonl
greek-train homer_parsed.jsonl --output attempts.jsonl
greek-analyze attempts.jsonl
```

---

## Conclusion

**CLTK is incredibly powerful, but underutilized for language learning.**

**What scholars do:**
- Batch analyze thousands of texts
- Build searchable databases
- Publish research papers

**What we're doing:**
- Interactive real-time training
- Fluency-focused practice
- Unix-style composable tools

**The innovation:**
- Using research-grade NLP for practical learning
- Applying software engineering patterns (Unix philosophy) to pedagogy
- Bridging the gap between digital humanities and language acquisition

**Impact potential:**
- First interactive CLTK-based grammar trainer
- Novel approach to fluency training
- Reusable pattern for any language with NLP support
- Could influence how digital tools are built for classical languages

---

## References

- CLTK GitHub: https://github.com/cltk/cltk
- CLTK Documentation: https://docs.cltk.org
- Perseus Digital Library: https://www.perseus.tufts.edu
- Universal Dependencies (Latin): https://universaldependencies.org/la/
- Stanza (Stanford NLP): https://stanfordnlp.github.io/stanza/

---

**Research Status:** Proof of concept complete
**Next Steps:** Build training corpus, integrate SRS, expand to other languages
**Innovation Level:** High (novel application of existing research tools)
