# Implementation Roadmap: B/C/S Grammar Trainer

## Phase 1: Parser Validation (2-4 hours)

### Goal
Verify that Stanza's Croatian/Serbian models produce sufficient morphological features for exercise generation.

### Tasks

**1.1 Install CLASSLA-Stanza B/C/S models**
```bash
cd research/1.140-classical-language-libraries/04-bcs-adaptation
uv venv
uv pip install classla

# Download Croatian and Serbian models
# Note: No dedicated Bosnian model exists, but Croatian model works excellently
# for Bosnian text (languages are mutually intelligible with identical grammar)
python -c "import classla; classla.download('hr'); classla.download('sr')"
```

**1.2 Test parser on sample sentences**
Create `test-parser.py`:
```python
import classla
import json

# Sample sentences covering different cases
# Note: Testing Croatian model with Bosnian, Croatian, and Serbian text
test_sentences = {
    'hr': [  # Croatian
        "Kuća je velika.",              # Nominative
        "Vidim kuću.",                  # Accusative
        "Dam djetetu knjigu.",          # Dative
        "Pričam o kući.",               # Locative
        "Idem s prijateljem.",          # Instrumental
    ],
    'bs': [  # Bosnian (will use 'hr' model)
        "Kuća je velika.",
        "Vidim kuću.",
        "Dajem djetetu knjigu.",
        "Pričam o kući.",
        "Idem s prijateljem.",
    ],
    'sr': [  # Serbian (Cyrillic)
        "Град је велик.",
        "Видим град.",
        "Дајем детету књигу.",
        "Причам о граду.",
        "Идем са пријатељем.",
    ]
}

# Test Croatian model on Croatian text
print("=== Croatian model on Croatian text ===")
nlp_hr = classla.Pipeline('hr', type='standard')
for sentence in test_sentences['hr']:
    doc = nlp_hr(sentence)

    for sent in doc.sentences:
        for word in sent.words:
            print(json.dumps({
                'text': word.text,
                'lemma': word.lemma,
                'upos': word.upos,
                'xpos': word.xpos,
                'feats': word.feats if word.feats else None
            }, ensure_ascii=False, indent=2))

# Test Croatian model on Bosnian text (should work identically)
print("\n=== Croatian model on Bosnian text ===")
for sentence in test_sentences['bs']:
    doc = nlp_hr(sentence)  # Using Croatian model for Bosnian

        for sent in doc.sentences:
            for word in sent.words:
                # Check what morphological features are available
                print(json.dumps({
                    'text': word.text,
                    'lemma': word.lemma,
                    'upos': word.upos,
                    'xpos': word.xpos,
                    'feats': word.feats if word.feats else None
                }, ensure_ascii=False, indent=2))
```

**Expected output** (verify these features exist):
- `Case`: Nom, Gen, Dat, Acc, Voc, Loc, Ins
- `Gender`: Masc, Fem, Neut
- `Number`: Sing, Plur
- `Animacy`: Anim, Inan (for accusative masculine)

**1.3 Create feature mapping**
Document how Stanza features map to trainer format:
```python
STANZA_TO_TRAINER = {
    'Case': {
        'Nom': 'nominative',
        'Gen': 'genitive',
        'Dat': 'dative',
        'Acc': 'accusative',
        'Voc': 'vocative',
        'Loc': 'locative',
        'Ins': 'instrumental',
    },
    'Gender': {
        'Masc': 'm',
        'Fem': 'f',
        'Neut': 'n',
    },
    # ... etc
}
```

**Deliverable**: `parser-validation-report.md` documenting:
- Which morphological features are available
- Any gaps or limitations
- Accuracy on test sentences
- Recommendations for ambiguity handling

---

## Phase 2: Declension Templates (4-8 hours)

### Goal
Create declension templates for B/C/S noun paradigms.

### Background
B/C/S declension is organized by **gender + ending type** rather than numbered declensions:

**Masculine**:
- Type I: consonant stem (grad → grada, gradu, grad, grade, o gradu, gradom)
- Type II: soft consonant (muž → muža, mužu, muža, muže, o mužu, mužem)

**Feminine**:
- Type I: -a ending (kuća → kuće, kući, kuću, kuće, o kući, kućom)
- Type II: consonant stem (noć → noći, noći, noć, noći, o noći, noći/noćju)

**Neuter**:
- Type I: -o/-e ending (selo → sela, selu, selo, sela, o selu, selom)
- Type II: -e ending (polje → polja, polju, polje, polja, o polju, poljem)

### Tasks

**2.1 Research standard paradigms**
- Consult grammar references (Browne & Alt, Barić et al.)
- Document 6-8 declension classes with full paradigms
- Note dialectal variations (ijekavian/ekavian differences are minimal in declensions)

**2.2 Create `config/croatian/declensions.json`**
```json
{
  "masculine-consonant": {
    "singular": {
      "nominative": "",
      "genitive": "a",
      "dative": "u",
      "accusative": "",
      "vocative": "e",
      "locative": "u",
      "instrumental": "om"
    },
    "plural": {
      "nominative": "i",
      "genitive": "a",
      "dative": "ima",
      "accusative": "e",
      "vocative": "i",
      "locative": "ima",
      "instrumental": "ima"
    },
    "stem_rule": "nominative_is_stem",
    "ambiguous": {
      "singular": ["nominative|accusative"],
      "plural": ["dative|locative|instrumental"]
    }
  },
  "feminine-a": {
    "singular": {
      "nominative": "a",
      "genitive": "e",
      "dative": "i",
      "accusative": "u",
      "vocative": "o",
      "locative": "i",
      "instrumental": "om"
    },
    "plural": {
      "nominative": "e",
      "genitive": "a",
      "dative": "ama",
      "accusative": "e",
      "vocative": "e",
      "locative": "ama",
      "instrumental": "ama"
    },
    "stem_rule": "remove_a",
    "ambiguous": {
      "singular": ["dative|locative"],
      "plural": ["nominative|accusative|vocative", "dative|locative|instrumental"]
    }
  }
  // ... other paradigms
}
```

**2.3 Animacy handling**
B/C/S masculine accusative depends on animacy:
- **Animate**: accusative = genitive (vidim čovjeka)
- **Inanimate**: accusative = nominative (vidim grad)

Add animacy parameter to declension templates and parser output.

**2.4 Validation**
Test templates against textbook examples:
```python
def validate_declension(lemma, declension_type, expected_forms):
    """Generate all forms and compare to expected"""
    generator = FormGenerator(declension_templates['croatian'])
    generated = generator.generate_all_forms(lemma, declension_type)

    for case_number, expected in expected_forms.items():
        assert generated[case_number] == expected
```

**Deliverable**: `config/croatian/declensions.json` with 6-8 paradigms validated against textbook examples

---

## Phase 3: Parser Integration (6-10 hours)

### Goal
Adapt `latin-parse` to work with B/C/S Stanza models.

### Tasks

**3.1 Create `bcs-parse` script** (copy from `latin-parse`)
```python
#!/usr/bin/env python3
"""
bcs-parse - Parse B/C/S text and extract morphology

Usage:
    bcs-parse input.txt --lang hr --output parsed.jsonl
    bcs-parse input.txt --lang sr --output parsed.jsonl
"""

import stanza
import json
import argparse

def parse_bcs(text, language='hr'):
    """
    Parse B/C/S text using Stanza

    Args:
        text: Input text
        language: 'hr' (Croatian) or 'sr' (Serbian)

    Returns:
        List of sentence dicts with morphological annotations
    """
    nlp = stanza.Pipeline(language, processors='tokenize,pos,lemma')
    doc = nlp(text)

    sentences = []
    for sent in doc.sentences:
        words = []
        for word in sent.words:
            # Extract morphological features
            feats = parse_features(word.feats) if word.feats else {}

            word_data = {
                'text': word.text,
                'lemma': word.lemma,
                'pos': map_pos(word.upos),
                'case': feats.get('case'),
                'gender': feats.get('gender'),
                'number': feats.get('number'),
                'animacy': feats.get('animacy'),  # Important for B/C/S!
            }

            # Only include nouns/adjectives for grammar training
            if word_data['pos'] in ['NOUN', 'ADJ']:
                words.append(word_data)

        if words:  # Only include sentences with trainable words
            sentences.append({
                'sentence': sent.text,
                'words': words
            })

    return sentences

def parse_features(feats_str):
    """Parse Stanza feature string: 'Case=Nom|Gender=Masc|Number=Sing'"""
    feats = {}
    for feat in feats_str.split('|'):
        key, value = feat.split('=')
        if key == 'Case':
            feats['case'] = CASE_MAP[value]
        elif key == 'Gender':
            feats['gender'] = GENDER_MAP[value]
        elif key == 'Number':
            feats['number'] = NUMBER_MAP[value]
        elif key == 'Animacy':
            feats['animacy'] = ANIMACY_MAP[value]
    return feats

CASE_MAP = {
    'Nom': 'nominative',
    'Gen': 'genitive',
    'Dat': 'dative',
    'Acc': 'accusative',
    'Voc': 'vocative',
    'Loc': 'locative',
    'Ins': 'instrumental',
}

# ... etc
```

**3.2 Test on real texts**
```bash
# Croatian news article
curl https://www.jutarnji.hr/... > test_hr.txt
./bcs-parse test_hr.txt --lang hr --output test_hr.jsonl

# Serbian news article
curl https://www.politika.rs/... > test_sr.txt
./bcs-parse test_sr.txt --lang sr --output test_sr.jsonl
```

**3.3 Handle edge cases**
- **Enclitics**: je, li, sam, etc. - Should these be parsed separately or ignored?
- **Compound words**: očeva (father's) - possessive adjectives
- **Diminutives**: kućica (little house) - declensions still apply

**Deliverable**: `bin/bcs-parse` script that outputs same JSONL format as `latin-parse`

---

## Phase 4: Vocabulary Tracking & 80-20 Matching (8-12 hours)

### Goal
Implement vocabulary progression system with corpus matching.

### Tasks

**4.1 Extract user's known vocabulary**
```python
class VocabularyTracker:
    def __init__(self, progress_file):
        self.progress_file = progress_file

    def get_known_lemmas(self, min_exposure=3):
        """
        Extract lemmas user has seen at least N times

        Args:
            min_exposure: Minimum times seen to count as "known"

        Returns:
            Set of known lemmas
        """
        lemma_counts = defaultdict(int)

        with open(self.progress_file, 'r') as f:
            for line in f:
                attempt = json.loads(line)
                for word_attempt in attempt['attempts']:
                    lemma = word_attempt.get('lemma', word_attempt['word'])
                    lemma_counts[lemma] += 1

        # Only count lemmas seen multiple times as "known"
        return {lemma for lemma, count in lemma_counts.items()
                if count >= min_exposure}

    def get_proficiency_level(self):
        """Estimate user's vocabulary size"""
        known = self.get_known_lemmas()

        if len(known) < 100:
            return 'beginner'
        elif len(known) < 500:
            return 'elementary'
        elif len(known) < 1500:
            return 'intermediate'
        elif len(known) < 3000:
            return 'advanced'
        else:
            return 'proficient'
```

**4.2 Implement corpus text scoring**
```python
class CorpusMatcher:
    def __init__(self, corpus_dir):
        self.corpus_dir = Path(corpus_dir)

    def score_text(self, text_file, known_lemmas):
        """
        Calculate vocabulary overlap for a text

        Returns:
            {
                'file': text_file,
                'total_lemmas': int,
                'known_lemmas': int,
                'new_lemmas': list,
                'overlap_pct': float,
                'difficulty': str
            }
        """
        # Parse text to extract lemmas
        text_lemmas = self.extract_lemmas(text_file)

        known_in_text = set(text_lemmas) & known_lemmas
        new_in_text = set(text_lemmas) - known_lemmas

        overlap = len(known_in_text) / len(text_lemmas)

        # Classify difficulty
        if overlap >= 0.95:
            difficulty = 'too_easy'
        elif 0.75 <= overlap < 0.95:
            difficulty = 'optimal'  # 80-20 rule range
        elif 0.50 <= overlap < 0.75:
            difficulty = 'challenging'
        else:
            difficulty = 'too_hard'

        return {
            'file': text_file,
            'total_lemmas': len(text_lemmas),
            'known_lemmas': len(known_in_text),
            'new_lemmas': sorted(new_in_text),
            'overlap_pct': overlap * 100,
            'difficulty': difficulty,
        }

    def find_matching_texts(self, known_lemmas, target_overlap=(0.75, 0.85), limit=10):
        """
        Find corpus texts matching vocabulary level

        Returns top N texts with vocabulary overlap in target range
        """
        scores = []

        for text_file in self.corpus_dir.glob('**/*.txt'):
            score = self.score_text(text_file, known_lemmas)

            if score['difficulty'] == 'optimal':
                scores.append(score)

        # Sort by how close to ideal 80% overlap
        scores.sort(key=lambda s: abs(s['overlap_pct'] - 80.0))

        return scores[:limit]
```

**4.3 Enhance exercise generator with glossary**
```python
class ExerciseBuilder:
    def build_exercise(self, text_file, known_lemmas):
        """
        Generate exercise with vocabulary metadata

        Returns JSONL with:
        1. Metadata line (title, description, vocab stats)
        2. Exercise lines (sentences with morphology)
        3. Glossary line (new lemmas with definitions)
        """
        sentences = parse_text(text_file)

        # Identify new vocabulary
        all_lemmas = extract_all_lemmas(sentences)
        new_lemmas = set(all_lemmas) - known_lemmas

        # Build glossary entries
        glossary = {}
        for lemma in new_lemmas:
            # Look up lemma in dictionary (or use parser's base form)
            glossary[lemma] = {
                'lemma': lemma,
                'genitive': self.get_genitive_form(lemma),
                'gender': self.get_gender(lemma),
                'translation': self.get_translation(lemma),  # From dictionary API
                'is_new': True
            }

        # Add known vocabulary to glossary (no translation needed)
        for lemma in (set(all_lemmas) & known_lemmas):
            glossary[lemma] = {
                'lemma': lemma,
                'genitive': self.get_genitive_form(lemma),
                'gender': self.get_gender(lemma),
                'is_new': False
            }

        # Write JSONL with metadata
        output = []

        # Line 1: Metadata
        output.append({
            '_metadata': True,
            'title': extract_title(text_file),
            'description': extract_description(text_file),
            'total_lemmas': len(all_lemmas),
            'new_lemmas': len(new_lemmas),
            'overlap_pct': len(known_lemmas & set(all_lemmas)) / len(all_lemmas) * 100
        })

        # Lines 2-N: Exercise sentences
        for sentence in sentences:
            output.append(sentence)

        # Last line: Glossary
        output.append({
            '_glossary': True,
            'vocabulary': glossary
        })

        return output
```

**4.4 Update trainer to show new vocabulary**
Modify `show_vocabulary_modal()` to distinguish new vs known:
```python
def show_vocabulary_modal(self):
    """Display vocabulary with new words highlighted"""
    # ... existing code ...

    # Split into known and new
    known_words = []
    new_words = []

    for lemma in sorted(self.vocabulary.keys()):
        v = self.vocabulary[lemma]
        entry = f"{lemma}, {v['genitive']} ({v['gender']})"

        if v.get('is_new'):
            # Add translation for new words
            if 'translation' in v:
                entry += f" - {v['translation']}"
            new_words.append(entry)
        else:
            known_words.append(entry)

    # Display with visual distinction
    if known_words:
        print(self.term.move_y(start_line) + self.term.bold("Known Vocabulary:"))
        start_line += 1
        for word in known_words:
            print(self.term.move_y(start_line) + f"  {word}")
            start_line += 1
        start_line += 1

    if new_words:
        print(self.term.move_y(start_line) + self.term.bold("New Vocabulary:"))
        start_line += 1
        for word in new_words:
            print(self.term.move_y(start_line) + f"  ⭐ {word}")
            start_line += 1
```

**Deliverable**:
- `tools/vocabulary_tracker.py`
- `tools/corpus_matcher.py`
- Updated exercise generator with glossary support
- Updated trainer with known/new vocabulary distinction

---

## Phase 5: Corpus Acquisition & Organization (4-8 hours)

### Goal
Build graded corpus library organized by difficulty.

### Tasks

**5.1 Source acquisition**
```bash
corpus/
├── 01-foundation/           # Generated exercises (high-frequency vocab)
│   ├── common-nouns.jsonl
│   ├── family-terms.jsonl
│   └── daily-objects.jsonl
├── 02-graded-readers/       # Controlled vocabulary texts
│   ├── folk-tales/
│   ├── simple-news/
│   └── dialogues/
├── 03-news/                 # Real news articles
│   ├── sports/
│   ├── technology/
│   ├── politics/
│   └── culture/
├── 04-literature/           # Short stories and excerpts
│   ├── contemporary/
│   └── classic/
└── metadata.json            # Difficulty ratings, topics, word counts
```

**Croatian sources**:
- **News**: Jutarnji list, Večernji list, Index.hr (scrape recent articles)
- **Literature**: Project Gutenberg (Croatian section), Digital Library of Croatia
- **Graded readers**: Find existing B/C/S learning materials

**Serbian sources**:
- **News**: Politika, Blic, B92
- **Literature**:Project Gutenberg (Serbian section), Serbian Digital Library
- **Both scripts**: Collect Cyrillic and Latin versions

**5.2 Metadata generation**
For each text file, create companion `.meta.json`:
```json
{
  "title": "Novi most u Beogradu",
  "source": "Politika",
  "date": "2024-01-15",
  "language": "sr",
  "script": "Cyrillic",
  "domain": "news/infrastructure",
  "word_count": 342,
  "unique_lemmas": 187,
  "difficulty_estimate": "intermediate"
}
```

**5.3 Automatic difficulty estimation**
```python
def estimate_difficulty(text_file):
    """
    Heuristic difficulty estimation based on:
    - Lexical diversity (unique lemmas / total words)
    - Sentence complexity (avg sentence length)
    - Rare word frequency (not in top 1000 word list)
    """
    lemmas = extract_lemmas(text_file)
    sentences = parse_sentences(text_file)

    diversity = len(set(lemmas)) / len(lemmas)
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
    rare_words = count_rare_words(lemmas, frequency_list='top1000.txt')

    difficulty_score = (diversity * 0.3 +
                       (avg_sentence_length / 20) * 0.3 +
                       (rare_words / len(lemmas)) * 0.4)

    if difficulty_score < 0.3:
        return 'beginner'
    elif difficulty_score < 0.5:
        return 'intermediate'
    else:
        return 'advanced'
```

**5.4 Build frequency lists**
Create top-N word lists for B/C/S:
```python
def build_frequency_list(corpus_dir, output_file, top_n=5000):
    """
    Count lemma frequencies across entire corpus
    Output sorted list of most common lemmas
    """
    lemma_counts = Counter()

    for text_file in corpus_dir.glob('**/*.txt'):
        lemmas = extract_lemmas(text_file)
        lemma_counts.update(lemmas)

    with open(output_file, 'w') as f:
        for lemma, count in lemma_counts.most_common(top_n):
            f.write(f"{lemma}\t{count}\n")
```

Use this for:
- **Foundation exercises**: Generate exercises using top 100-500 words
- **Difficulty estimation**: Compare text vocabulary to frequency list
- **Vocabulary milestones**: Track user progress (e.g., "You know 800/5000 common words")

**Deliverable**:
- `corpus/` directory with 50-100 texts across difficulty levels
- Metadata for all texts
- Frequency lists (`frequency-lists/croatian-top5000.txt`, etc.)

---

## Phase 6: Launcher Integration (4-6 hours)

### Goal
Add B/C/S to the project launcher with corpus matching.

### Tasks

**6.1 Add to `completed-projects.yaml`**
```yaml
- id: bcs-trainer
  name: "B/C/S Grammar Trainer"
  description: "Learn Croatian/Serbian grammar through reading with automatic exercise generation and 80-20 vocabulary matching"
  location: research/1.140-classical-language-libraries/04-bcs-adaptation/
  research_basis:
    - 1.140-classical-language-libraries (Latin toolkit)
    - Stanza NLP (Croatian/Serbian models)
  tech_stack:
    - Stanza (parser)
    - Python blessed (terminal UI)
    - JSONL format (exercises)
  status: complete
  features:
    - Parse Croatian/Serbian texts
    - 7-case declension training
    - Vocabulary progression tracking (80-20 rule)
    - Corpus matching by vocabulary overlap
    - Smart randomization (standard first time, random on repeat)
    - Animated/inanimate accusative distinction
  how_to_run:
    setup: |
      cd research/1.140-classical-language-libraries/04-bcs-adaptation
      uv venv
      uv pip install -r requirements.txt
      python -c "import stanza; stanza.download('hr'); stanza.download('sr')"
    run_commands:
      - name: "Parse Croatian text"
        command: "bin/bcs-parse {input_file} --lang hr --output exercises/{exercise_name}.jsonl"
        parameters:
          input_file:
            type: string
            prompt: "Path to Croatian text file:"
          exercise_name:
            type: string
            prompt: "Exercise name:"

      - name: "Parse Serbian text"
        command: "bin/bcs-parse {input_file} --lang sr --output exercises/{exercise_name}.jsonl"
        parameters:
          input_file:
            type: string
            prompt: "Path to Serbian text file:"
          exercise_name:
            type: string
            prompt: "Exercise name:"

      - name: "Find matching texts (Croatian)"
        command: "bin/match-corpus --lang hr --user {username} --show {limit}"
        parameters:
          username:
            type: string
            prompt: "Your name:"
            default: "ivan"
          limit:
            type: string
            prompt: "Number of matches:"
            default: "10"

      - name: "Interactive trainer (Croatian)"
        command: "bin/bcs-train {exercise} --output progress/{username}_attempts.jsonl --user {username}"
        repeat: true
        parameters:
          exercise:
            type: file_select
            pattern: "exercises/hr/*.jsonl"
            display: basename
            prompt: "Select Croatian exercise:"
            supports_randomize: true
          username:
            type: string
            prompt: "Your name:"
            default: "ivan"

      - name: "Interactive trainer (Serbian)"
        command: "bin/bcs-train {exercise} --output progress/{username}_attempts.jsonl --user {username}"
        repeat: true
        parameters:
          exercise:
            type: file_select
            pattern: "exercises/sr/*.jsonl"
            display: basename
            prompt: "Select Serbian exercise:"
            supports_randomize: true
          username:
            type: string
            prompt: "Your name:"
            default: "ivan"
```

**6.2 Create `bin/match-corpus` utility**
```python
#!/usr/bin/env python3
"""
match-corpus - Find texts matching user's vocabulary level

Usage:
    match-corpus --lang hr --user ivan --show 10
    match-corpus --lang sr --user ivan --target-overlap 80 --show 5
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', choices=['hr', 'sr'], required=True)
    parser.add_argument('--user', required=True)
    parser.add_argument('--target-overlap', type=float, default=80.0)
    parser.add_argument('--show', type=int, default=10)
    args = parser.parse_args()

    # Load user's known vocabulary
    progress_file = f"progress/{args.user}_attempts.jsonl"
    tracker = VocabularyTracker(progress_file)
    known_lemmas = tracker.get_known_lemmas()

    print(f"Your vocabulary: {len(known_lemmas)} known lemmas")
    print(f"Proficiency level: {tracker.get_proficiency_level()}")
    print()

    # Find matching texts
    corpus_dir = f"corpus/{args.lang}"
    matcher = CorpusMatcher(corpus_dir)
    matches = matcher.find_matching_texts(
        known_lemmas,
        target_overlap=(args.target_overlap - 5, args.target_overlap + 5),
        limit=args.show
    )

    # Display results
    print(f"Top {len(matches)} matching texts (target: {args.target_overlap}% overlap):")
    print("=" * 70)

    for i, match in enumerate(matches, 1):
        print(f"{i}. {match['file'].name}")
        print(f"   Overlap: {match['overlap_pct']:.1f}% | New words: {len(match['new_lemmas'])}")
        print(f"   Difficulty: {match['difficulty']}")
        print()

    # Offer to generate exercises
    choice = input("Generate exercises for any? (enter number or 'q'): ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(matches):
            text_file = matches[idx]['file']
            # Generate exercise...
            print(f"Generating exercise from {text_file.name}...")
```

**Deliverable**: Full launcher integration with corpus matching workflow

---

## Phase 7: Testing & Validation (8-12 hours)

### Goal
Validate end-to-end workflow with real users.

### Tasks

**7.1 Unit tests**
```python
# Test declension generation
def test_croatian_declensions():
    gen = FormGenerator(declension_templates['croatian'])

    # Test masculine consonant stem
    forms = gen.generate_all_forms('grad', 'masculine-consonant')
    assert forms['singular']['genitive'] == 'grada'
    assert forms['singular']['locative'] == 'gradu'

    # Test feminine -a stem
    forms = gen.generate_all_forms('kuća', 'feminine-a')
    assert forms['singular']['genitive'] == 'kuće'
    assert forms['plural']['instrumental'] == 'kućama'

# Test parser
def test_stanza_parser():
    parser = BCParser('hr')
    result = parser.parse_sentence("Vidim veliku kuću.")

    assert result['words'][0]['text'] == 'Vidim'
    assert result['words'][1]['lemma'] == 'velik'
    assert result['words'][1]['case'] == 'accusative'
    assert result['words'][2]['lemma'] == 'kuća'
    assert result['words'][2]['case'] == 'accusative'

# Test vocabulary matching
def test_corpus_matching():
    known = {'kuća', 'grad', 'čovjek', 'vidim', 'velika'}  # 5 known lemmas

    matcher = CorpusMatcher('corpus/hr')
    score = matcher.score_text('test_text.txt', known)

    assert 0.75 <= score['overlap_pct'] / 100 <= 0.85  # Should be in 80-20 range
```

**7.2 Integration tests**
```bash
# Full workflow test
cd research/1.140-classical-language-libraries/04-bcs-adaptation

# 1. Parse sample text
bin/bcs-parse corpus/hr/sample_news.txt --lang hr --output exercises/hr/test.jsonl

# 2. Train on parsed text
bin/bcs-train exercises/hr/test.jsonl --output progress/testuser_attempts.jsonl --user testuser

# 3. Check vocabulary tracking
bin/match-corpus --lang hr --user testuser --show 5

# 4. Validate progress file has correct format
python -c "
import json
with open('progress/testuser_attempts.jsonl') as f:
    for line in f:
        data = json.loads(line)
        assert 'exercise' in data
        assert 'attempts' in data
        for attempt in data['attempts']:
            assert 'lemma' in attempt or 'word' in attempt
"
```

**7.3 User acceptance testing**
- Recruit 3-5 B/C/S learners (different proficiency levels)
- Have them complete:
  1. 3 generated exercises (different difficulty)
  2. 1 corpus-matched text
  3. Vocabulary progression check
- Collect feedback on:
  - Parser accuracy (did it correctly identify cases?)
  - Exercise difficulty (was 80-20 rule effective?)
  - UI/UX (keyboard shortcuts, vocabulary modal)
  - Vocabulary progression (did recommendations improve over time?)

**Deliverable**:
- Test suite (`tests/`) with 80%+ coverage
- User testing report with feedback
- Bug fixes based on testing

---

## Phase 8: Documentation & Polish (4-6 hours)

### Goal
Production-ready documentation and user guides.

### Tasks

**8.1 User guide**
```markdown
# B/C/S Grammar Trainer - User Guide

## Quick Start

1. Install dependencies
2. Parse your first text
3. Start training
4. Track your progress

## Workflow: The 80-20 Rule

[Explain vocabulary progression strategy]

## Advanced Features

- Custom corpus organization
- Vocabulary milestone tracking
- Exporting progress data

## Keyboard Reference

[Full keyboard map with 7 cases]
```

**8.2 Technical documentation**
```markdown
# Developer Guide: Adapting to New Languages

This system works for any inflected language. Here's how to adapt it:

1. Check Stanza support (https://stanfordnlp.github.io/stanza/)
2. Create declension templates
3. Map morphological features
4. Add keyboard shortcuts
5. Test and validate

See: Latin (6 cases) and B/C/S (7 cases) as reference implementations.
```

**8.3 Corpus curation guide**
```markdown
# Building Your Corpus Library

## Sourcing texts
- News websites
- Digital libraries
- Public domain literature
- User-contributed texts

## Quality criteria
- Grammatically correct
- Domain diversity
- Difficulty spread (beginner → advanced)
- Cultural relevance

## Metadata standards
[Template for .meta.json files]
```

**Deliverable**:
- README.md for 04-bcs-adaptation/
- USER_GUIDE.md
- DEVELOPER_GUIDE.md
- CORPUS_CURATION.md

---

## Success Metrics

### Phase 1-3 (Parser & Templates)
- [ ] Stanza parser achieves >90% accuracy on test sentences
- [ ] Declension templates validated against textbook examples
- [ ] `bcs-parse` outputs valid JSONL

### Phase 4-5 (Vocabulary & Corpus)
- [ ] Vocabulary tracker correctly identifies known lemmas
- [ ] Corpus matcher finds texts with 75-85% overlap
- [ ] 50+ texts across difficulty levels

### Phase 6-7 (Integration & Testing)
- [ ] Launcher workflow: parse → train → match → progress
- [ ] Test suite passes (>80% coverage)
- [ ] User testing shows improved comprehension after 10 exercises

### Phase 8 (Documentation)
- [ ] Documentation complete and clear
- [ ] New users can complete workflow independently

---

## Timeline Estimate

**Minimum viable product (MVP)**: 40-60 hours
- Phases 1-4: Core functionality (20-30 hours)
- Phase 5: Basic corpus (10-15 hours)
- Phase 6-7: Integration + testing (10-15 hours)

**Production release**: 60-80 hours
- Add Phase 8: Documentation (4-6 hours)
- Additional corpus curation (10-15 hours)
- User testing iterations (6-10 hours)

**Per language adaptation (after B/C/S)**: 15-25 hours
- Most code is reusable
- Main work: declension templates, testing, corpus

---

## Priority Order

### Must Have (MVP)
1. Parser working (Phase 1-3)
2. Basic vocabulary tracking (Phase 4)
3. 20-30 corpus texts (Phase 5 - subset)
4. Launcher integration (Phase 6)

### Should Have (Production)
5. Full corpus library (Phase 5 - complete)
6. Comprehensive testing (Phase 7)
7. Documentation (Phase 8)

### Nice to Have (Future)
- Dictionary API integration (automatic translations in glossary)
- Spaced repetition algorithm (optimize review schedule)
- Web interface (browser-based trainer)
- Mobile app (iOS/Android)
- Anki deck export (integrate with existing flashcard workflows)

---

*Generated: 2025-11-20*
*Estimated total effort: 60-80 hours for production-ready B/C/S trainer*
