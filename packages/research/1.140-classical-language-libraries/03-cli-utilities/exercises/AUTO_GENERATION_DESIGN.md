# Auto-Generation Design for Vocabulary Exercise Series

## Overview

Generate complete 15-exercise series from a vocabulary list + declension templates.

**Input**: `vocabulary.json` (10 words with declension info)
**Output**: 15 JSONL exercise files matching model-nouns structure
**Time**: 30 seconds vs 6-8 hours manual

## Architecture

```
generate-vocabulary-exercises.py
├── Input: vocabulary.json
├── Templates: declension_templates.json
├── Generator: exercise_builder.py
└── Output: 15 JSONL files
```

## Core Components

### 1. Vocabulary Input Format

```json
{
  "series_name": "common-nouns",
  "series_title": "Common Nouns (Intermediate)",
  "series_description": "Practice with everyday vocabulary",
  "level": "intermediate",
  "words": [
    {
      "lemma": "familia",
      "declension": "1st",
      "gender": "f",
      "meaning": "family",
      "irregular": false
    },
    {
      "lemma": "amicus",
      "declension": "2nd",
      "gender": "m",
      "meaning": "friend",
      "irregular": false,
      "vocative_override": "amice"  // For -us → -e pattern
    },
    // ... 8 more words
  ]
}
```

**Key**: Don't require all forms - generate them from declension patterns!

### 2. Declension Templates

Store canonical endings for each declension:

```json
{
  "1st": {
    "singular": {
      "nominative": "",
      "genitive": "e",
      "dative": "e",
      "accusative": "m",
      "ablative": "ā",
      "vocative": ""
    },
    "plural": {
      "nominative": "e",
      "genitive": "ārum",
      "dative": "īs",
      "accusative": "ās",
      "ablative": "īs",
      "vocative": "e"
    },
    "stem_rule": "remove_a",  // familia → famili
    "ambiguous": {
      "singular": ["genitive|dative"],
      "plural": ["dative|ablative"]
    }
  },
  "2nd": {
    "singular": {
      "nominative": "us",
      "genitive": "ī",
      "dative": "ō",
      "accusative": "um",
      "ablative": "ō",
      "vocative": "e"  // Special rule: -us → -e
    },
    // ... etc
  }
  // ... 3rd, 4th, 5th declensions
}
```

### 3. Form Generator

```python
class FormGenerator:
    def __init__(self, templates):
        self.templates = templates

    def generate_form(self, word, case, number):
        """Generate a specific form from word + declension template"""
        decl = self.templates[word['declension']]

        # Get stem (e.g., familia → famili)
        stem = self.get_stem(word['lemma'], decl['stem_rule'])

        # Get ending for case/number
        ending = decl[number][case]

        # Handle special cases (vocative override, etc.)
        if case == 'vocative' and 'vocative_override' in word:
            return word['vocative_override']

        return stem + ending

    def is_ambiguous(self, word, case, number):
        """Check if this form is ambiguous"""
        decl = self.templates[word['declension']]
        ambiguous_key = f"{case}|..."

        if number in decl['ambiguous']:
            for pattern in decl['ambiguous'][number]:
                if case in pattern.split('|'):
                    return pattern.split('|')
        return None
```

### 4. Exercise Templates

Define structure for each exercise type:

```python
EXERCISE_TEMPLATES = {
    "01": {
        "type": "single_declension",
        "declension": "1st",
        "title": "{lemma} ({meaning})",
        "description": "Learn all 12 forms of 1st declension nouns",
        "structure": [
            # Line 1: singular forms in order
            ["nom", "gen", "gen", "acc", "abl", "voc"],  # singular
            # Line 2: plural forms in order
            ["nom", "gen", "dat", "acc", "dat", "voc"]   # plural
        ]
    },
    "06": {
        "type": "single_case",
        "case": "nominative",
        "title": "Nominative Case - All Declensions",
        "description": "Practice nominative (subject) across all declensions",
        "structure": [
            # One word from each declension, singular
            {"1st": "nom-sg", "2nd": "nom-sg", "3rd": "nom-sg", "4th": "nom-sg", "5th": "nom-sg"},
            # One word from each declension, plural
            {"1st": "nom-pl", "2nd": "nom-pl", "3rd": "nom-pl", "4th": "nom-pl", "5th": "nom-pl"}
        ]
    },
    // ... templates for all 15 exercise types
}
```

### 5. Exercise Builder

```python
class ExerciseBuilder:
    def __init__(self, vocab, form_gen, templates):
        self.vocab = vocab
        self.form_gen = form_gen
        self.templates = templates

    def build_exercise(self, exercise_num):
        """Build one complete exercise file"""
        template = self.templates[exercise_num]

        # Select words based on exercise type
        if template['type'] == 'single_declension':
            words = [w for w in self.vocab if w['declension'] == template['declension']]
            word = words[0]  # Use first word of this declension
        elif template['type'] == 'single_case':
            words = self.select_one_per_declension()
        # ... other exercise types

        # Build sentences according to structure
        lines = []
        for structure_line in template['structure']:
            sentence_words = []
            for spec in structure_line:
                # spec = "nom-sg" or {"1st": "nom-sg", ...}
                form = self.form_gen.generate_form(word, case, number)
                ambiguous = self.form_gen.is_ambiguous(word, case, number)

                sentence_words.append({
                    "text": form,
                    "lemma": word['lemma'],
                    "pos": "NOUN",
                    "declension": word['declension'],
                    "number": number,
                    "case": ambiguous if ambiguous else case
                })

            lines.append({
                "sentence": " ".join(w["text"] for w in sentence_words),
                "words": sentence_words
            })

        return lines

    def write_exercise_file(self, exercise_num, lines):
        """Write JSONL file with metadata + exercise lines"""
        filepath = f"{exercise_num:02d}-{template['filename']}.jsonl"

        with open(filepath, 'w') as f:
            # Write metadata line
            metadata = {
                "_metadata": true,
                "title": template['title'],
                "description": template['description']
            }
            f.write(json.dumps(metadata) + '\n')

            # Write exercise lines
            for line in lines:
                f.write(json.dumps(line) + '\n')
```

### 6. Main Generator

```python
def generate_series(vocab_file):
    """Generate complete 15-exercise series from vocabulary file"""

    # Load inputs
    vocab = load_vocabulary(vocab_file)
    declension_templates = load_declension_templates()
    exercise_templates = load_exercise_templates()

    # Initialize components
    form_gen = FormGenerator(declension_templates)
    builder = ExerciseBuilder(vocab, form_gen, exercise_templates)

    # Create series directory
    series_dir = f"exercises/{vocab['series_name']}"
    os.makedirs(series_dir, exist_ok=True)

    # Write series metadata
    write_series_metadata(series_dir, vocab)

    # Generate all 15 exercises
    for num in range(1, 16):
        exercise_num = f"{num:02d}"
        lines = builder.build_exercise(exercise_num)
        builder.write_exercise_file(os.path.join(series_dir, exercise_num), lines)

    print(f"✅ Generated {series_dir} with 15 exercises")
```

## Usage

```bash
# 1. Create vocabulary file
cat > my-vocab.json << EOF
{
  "series_name": "common-nouns",
  "series_title": "Common Nouns",
  ...
}
EOF

# 2. Generate series
python generate-vocabulary-exercises.py my-vocab.json

# 3. Output
# exercises/common-nouns/
#   ├── .series-metadata.json
#   ├── 01-single_declension_1st.jsonl
#   ├── 02-single_declension_2nd.jsonl
#   ...
#   └── 15-ambiguous_forms_drill.jsonl
```

## Advanced Features

### Handling Irregular Forms

```json
{
  "lemma": "vir",
  "declension": "2nd",
  "irregular": true,
  "forms_override": {
    "singular": {
      "nominative": "vir",  // Not "virus"
      "vocative": "vir"     // Not "vire"
    }
  }
}
```

### Smart Word Selection

For exercises requiring multiple words (like single-case drills):

```python
def select_one_per_declension(self):
    """Pick one word from each declension, avoiding repetition"""
    selected = {}
    for decl in ['1st', '2nd', '3rd', '4th', '5th']:
        candidates = [w for w in self.vocab if w['declension'] == decl]
        # Rotate through words to ensure variety across exercises
        selected[decl] = candidates[self.usage_counter[decl] % len(candidates)]
        self.usage_counter[decl] += 1
    return selected
```

### Meaningful Sentences (Integration Exercises)

For exercises 14-15 (integration), generate simple meaningful sentences:

```python
SENTENCE_PATTERNS = [
    "{nom_sg} {gen_sg} {dat_sg}",  # "The girl of the family to the friend"
    "{nom_pl} {acc_pl} {abl_pl}",  # "Friends with families by the wind"
]

def generate_meaningful_sentence(words):
    """Use sentence patterns to create more natural word order"""
    pattern = random.choice(SENTENCE_PATTERNS)
    # Fill pattern with appropriate words/forms
    ...
```

## Implementation Priority

### Phase 1: MVP (2-3 hours)
- ✅ Basic form generation from templates
- ✅ Single declension exercises (01-05)
- ✅ Single case exercises (06-11)

### Phase 2: Complete (2-3 hours)
- ✅ Single number exercises (12-13)
- ✅ Integration exercises (14-15)
- ✅ Ambiguous form marking

### Phase 3: Polish (1-2 hours)
- ✅ Irregular form support
- ✅ Smart word rotation
- ✅ Meaningful sentence patterns
- ✅ Validation/testing

**Total: 5-8 hours to build, saves 6-8 hours per series**

## Benefits

1. **Consistency**: All series follow exact same structure
2. **Speed**: 30 seconds vs 6-8 hours per series
3. **Scalability**: Can generate dozens of series from vocab lists
4. **Maintainability**: Fix bug once, regenerate all series
5. **Flexibility**: Easy to add new exercise types

## Future Extensions

- **Adjective support**: Add adjective declensions
- **Verb conjugations**: Extend to verb drills
- **Mixed exercises**: Nouns + adjectives + verbs
- **AI-generated sentences**: Use LLM for natural sentences
- **Difficulty scaling**: Adjust based on learner level
