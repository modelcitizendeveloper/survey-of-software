# Grammaticus for Slavic Languages: B/C/S Adaptation

## Core Idea

Adapt the Latin grammar training toolkit to **Bosnian/Croatian/Serbian (B/C/S)** and other highly inflected languages. The architecture is language-agnostic: morphological templates define grammar rules, NLP parsers extract features, and the trainer drills recognition through reading comprehension.

**Value Proposition**: Learn inflected languages by reading texts you care about, with automatic grammar exercise generation and vocabulary progression tracking.

## Why B/C/S is an Ideal Target

### 1. Structural Similarity to Latin
- **7 cases** (nom/gen/dat/acc/voc/loc/inst) vs Latin's 6
- **3 genders** (m/f/n)
- **2 numbers** (singular/plural)
- **Declension patterns** (different paradigms per gender/animacy)
- Same pedagogical challenge: recognizing inflected forms in context

### 2. Superior NLP Infrastructure
**Parser**: Stanza already supports Croatian (`hr`) and Serbian (`sr`)
- Trained on billions of tokens
- Extracts full morphological features (case, gender, number, animacy, definiteness)
- Likely MORE accurate than Latin parsers due to modern training data

**Corpus availability**: Orders of magnitude larger than Latin
- hrWaC: 1.2 billion tokens
- srWaC: similar scale
- Daily newspapers, Wikipedia, digitized literature
- Domain-specific texts (sports, news, technical, literature)
- **Living language** = constantly growing corpus

### 3. Pedagogical Advantages
- **Relevant content**: Learn through texts you want to read (news, sports, novels)
- **Modern usage**: Contemporary grammatical patterns
- **Practical application**: Immediate use in conversation/reading
- **Aspect pairs**: B/C/S has perfective/imperfective verbs (pedagogically interesting)

## Architecture: Language-Agnostic Design

### Current System (Latin)
```
Text → Parser (CLTK/Stanza) → JSONL (morphology) → Trainer → Progress tracking
                                                   ↓
                                            Exercise generator
                                            (declension templates)
```

### Adaptable Components

**Universal (no changes needed)**:
1. **JSONL format**: `{text, lemma, pos, case, gender, number, ...}`
2. **Trainer keyboard interface**: Navigate, input, check answers
3. **Progress tracking**: Attempts file, mistake analysis
4. **Vocabulary extraction**: Build glossary from corpus
5. **Exercise progression**: Track completed exercises, smart randomization

**Language-specific (swap templates)**:
1. **Declension templates** (`declension_templates.json`):
   - Define case endings per declension class
   - Mark ambiguous forms
   - B/C/S: Add 7th case (locative), instrumental patterns

2. **Parser integration** (`latin-parse`):
   - Change Stanza language model: `stanza.Pipeline('hr')` or `stanza.Pipeline('sr')`
   - Map morphological features to exercise format
   - Extract aspect for verbs (perfective/imperfective)

3. **Keyboard mappings** (`latin-train`):
   - Add `l` (locative), `i` (instrumental) keys
   - Otherwise identical: case input, navigation, vocab lookup

4. **Vocabulary display**:
   - B/C/S format: "nominative, genitive (gender)" (same as Latin)
   - Example: "kuća, kuće (f)" vs "puella, puellae (f)"

## Vocabulary Progression: The 80-20 Rule

### Principle
Texts should contain **~80% known vocabulary** and **~20% new vocabulary** for optimal learning (Krashen's i+1: comprehensible input just beyond current level).

### Implementation Strategy

**1. Vocabulary Tracking**
- User progress file already tracks: `{exercise, sentence, attempts, accuracy}`
- Extract **seen lemmas** across all completed exercises
- Build **known vocabulary set** per user

**2. Text Difficulty Scoring**
```python
def calculate_vocabulary_overlap(text_lemmas, known_lemmas):
    """
    Returns overlap percentage: known_lemmas ∩ text_lemmas / text_lemmas

    Example:
    - Text has 100 unique lemmas
    - User knows 82 of them
    - Overlap = 82% → Good match for 80-20 rule
    """
    overlap = len(set(text_lemmas) & set(known_lemmas))
    return overlap / len(text_lemmas)
```

**3. Corpus Matching Pipeline**
```
User known vocabulary → Score all corpus texts → Filter 75-85% overlap → Present options
```

**4. Glossary Generation**
- For each text, identify **new lemmas** (in the 20%)
- Auto-generate glossary entries from parser output
- Display in vocabulary modal (`?` key) during training

**5. Adaptive Progression**
```
Beginner (0-500 words):     High-frequency word lists → Graded readers
Intermediate (500-2000):    News articles (filtered by overlap)
Advanced (2000+):           Literature, technical texts, domains of interest
```

### Corpus Organization by Difficulty

**Level 1 (Foundation)**:
- Generated exercises using high-frequency nouns (top 100)
- Controlled vocabulary, systematic declension introduction
- **Example**: Days of week, family members, common objects

**Level 2 (Graded Readers)**:
- Short texts with 300-500 word vocabulary
- Folk tales, simple news, dialogues
- **Overlap target**: 85-90% (very accessible)

**Level 3 (Domain-Specific)**:
- Sports articles (if user interested in sports)
- Technology news (if user is developer)
- **Overlap target**: 80-85% (20% new vocab)

**Level 4 (Literature)**:
- Short stories, novel excerpts
- Poetry (higher grammar complexity)
- **Overlap target**: 75-80% (challenging but comprehensible)

**Level 5 (Native Content)**:
- Unfiltered news, technical documentation
- Literary classics (Andrić, Krleža)
- **Overlap target**: <75% (independent reading)

### Glossary Format in Modal

When user presses `?` during training:

```
                    VOCABULARY REFERENCE
============================================================

Known Vocabulary (80%):
  grad, grada (m) - city           kuća, kuće (f) - house
  čovjek, čovjeka (m) - person     žena, žene (f) - woman

New Vocabulary (20%):
  ⭐ trgovina, trgovine (f) - store    ⭐ prozor, prozora (m) - window
  ⭐ ulica, ulice (f) - street         ⭐ zid, zida (m) - wall

              Press any key to return to exercise...
```

**Visual distinction**:
- Known words: regular formatting
- New words: ⭐ marker + English translation
- Sorted alphabetically within each category

## Implementation: Language as First-Class Parameter

### Unified Tool Interface
```bash
# Latin (current)
grammaticus-parse texts/caesar.txt --lang latin --output exercises/caesar.jsonl

# B/C/S (new)
grammaticus-parse texts/novosti.txt --lang hr --output exercises/novosti.jsonl

# Russian (future)
grammaticus-parse texts/pushkin.txt --lang ru --output exercises/pushkin.jsonl
```

### Configuration Structure
```
config/
  ├── latin/
  │   ├── declensions.json      # 5 declensions, 6 cases
  │   ├── stanza_model.txt      # "la"
  │   └── keyboard_map.json     # n/g/d/a/b/v
  ├── croatian/
  │   ├── declensions.json      # Gender-based, 7 cases
  │   ├── stanza_model.txt      # "hr"
  │   └── keyboard_map.json     # n/g/d/a/v/l/i
  └── serbian/
      ├── declensions.json
      ├── stanza_model.txt      # "sr"
      └── keyboard_map.json
```

### Exercise Generator: Language-Agnostic
```python
class ExerciseGenerator:
    def __init__(self, language_config):
        self.declensions = load_json(language_config['declensions'])
        self.cases = language_config['cases']
        self.parser_model = language_config['stanza_model']

    def generate_exercises(self, corpus_file, user_vocab):
        """
        1. Parse corpus with Stanza
        2. Calculate vocabulary overlap
        3. Generate exercises (single case, mixed, integration)
        4. Mark new vocabulary for glossary
        """
        pass
```

## Next Steps: B/C/S Implementation

See `NEXT_STEPS.md` for detailed implementation roadmap.

## Generalization: Beyond B/C/S

Once B/C/S is working, the system can be adapted to:

**Slavic languages**:
- Russian (ru): 6 cases, rich morphology, huge corpus
- Polish (pl): 7 cases, complex declensions
- Czech (cs): 7 cases, dual number remnants

**Other inflected languages**:
- Ancient Greek (grc): Complex verb system, 5 cases
- Sanskrit (sa): 8 cases, verb conjugations
- Finnish (fi): 15 cases, agglutinative
- Hungarian (hu): 18 cases, vowel harmony

**Key insight**: The harder the grammar, the more valuable this systematic training approach becomes.

## Why This Matters

**Current state**: Language learners memorize declension tables divorced from reading practice.

**This approach**: Learn grammar BY reading, with automatic exercise generation from texts you care about.

**Impact**: Makes inflected languages accessible through comprehensible input + targeted grammar drills + vocabulary progression tracking.

---

*Generated: 2025-11-20*
*Based on: Latin Grammar Trainer (research/1.140-classical-language-libraries/03-cli-utilities/)*
