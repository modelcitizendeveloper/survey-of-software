# Vocabulary Exercise Series Template

## Creating a New Series Manually

### 1. Create Series Directory

```bash
cd exercises/
mkdir my-series-name/
```

### 2. Create Series Metadata

Create `my-series-name/.series-metadata.json`:

```json
{
  "title": "Common Nouns (Intermediate)",
  "description": "Practice with everyday vocabulary",
  "vocabulary": [
    "familia (family) - 1st",
    "amicus (friend) - 2nd",
    "corpus (body) - 3rd",
    "manus (hand) - 4th",
    "dies (day) - 5th"
  ],
  "level": "intermediate"
}
```

### 3. Define Your Vocabulary List

Create `my-series-name/vocabulary.json`:

```json
{
  "words": [
    {
      "lemma": "familia",
      "declension": "1st",
      "gender": "f",
      "meaning": "family",
      "forms": {
        "singular": {
          "nominative": "familia",
          "genitive": "familiae",
          "dative": "familiae",
          "accusative": "familiam",
          "ablative": "familiā",
          "vocative": "familia"
        },
        "plural": {
          "nominative": "familiae",
          "genitive": "familiārum",
          "dative": "familiīs",
          "accusative": "familiās",
          "ablative": "familiīs",
          "vocative": "familiae"
        }
      }
    },
    {
      "lemma": "amicus",
      "declension": "2nd",
      "gender": "m",
      "meaning": "friend",
      "forms": {
        "singular": {
          "nominative": "amicus",
          "genitive": "amicī",
          "dative": "amicō",
          "accusative": "amicum",
          "ablative": "amicō",
          "vocative": "amice"
        },
        "plural": {
          "nominative": "amicī",
          "genitive": "amicōrum",
          "dative": "amicīs",
          "accusative": "amicōs",
          "ablative": "amicīs",
          "vocative": "amicī"
        }
      }
    }
    // ... 8 more words (10 total recommended - 2 per declension)
  ]
}
```

### 4. Create Exercises Manually

For each of the 15 exercise types, create a JSONL file following the model-nouns pattern:

**Example: `01-single_declension_1st.jsonl`**

```jsonl
{"_metadata": true, "title": "1st Declension - familia (family)", "description": "Learn all 12 forms of 1st declension nouns"}
{"sentence": "familia familiae familiae familiam familiā familia", "words": [{"text": "familia", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "singular", "case": "nominative"}, {"text": "familiae", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "singular", "case": ["genitive", "dative"]}, {"text": "familiae", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "singular", "case": ["genitive", "dative"]}, {"text": "familiam", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "singular", "case": "accusative"}, {"text": "familiā", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "singular", "case": "ablative"}, {"text": "familia", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "singular", "case": "vocative"}]}
{"sentence": "familiae familiārum familiīs familiās familiīs familiae", "words": [{"text": "familiae", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "plural", "case": "nominative"}, {"text": "familiārum", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "plural", "case": "genitive"}, {"text": "familiīs", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "plural", "case": ["dative", "ablative"]}, {"text": "familiās", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "plural", "case": "accusative"}, {"text": "familiīs", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "plural", "case": ["dative", "ablative"]}, {"text": "familiae", "lemma": "familia", "pos": "NOUN", "declension": "1st", "number": "plural", "case": "vocative"}]}
```

### 5. Repeat for All 15 Exercises

Use the same structure as model-nouns series:
- 01-05: Single declension (one declension, 12 forms)
- 06-11: Single case (one case, 10 forms across 5 declensions)
- 12-13: Single number (one number, 30 forms)
- 14-15: Integration (all mixed)

### 6. Test Your Series

```bash
./launch-project
# Select "Interactive trainer (exercises)"
# You should see series menu with your new series
```

## Recommended Vocabulary Sets

### Intermediate (Common Nouns)
- 1st: familia, vita, terra, aqua
- 2nd: amicus, animus, filius, bellum
- 3rd: corpus, tempus, homo, pars
- 4th: manus, domus
- 5th: dies, spes

### Advanced (Historical/Literary)
- 1st: fortūna, patria, memoria
- 2nd: populus, ager, verbum
- 3rd: urbs, civitas, lex, rex
- 4th: exercitus, senātus
- 5th: rēs pūblica, fidēs

### Thematic Sets
- **Nature**: terra, aqua, caelum, mare, silva, mons
- **People**: homo, vir, mulier, puer, puella, māter, pater
- **War**: bellum, pāx, arma, exercitus, miles, dux
- **State**: civitas, urbs, lex, senātus, populus, rēx

## Tips for Manual Creation

1. **Use 2 words per declension** for variety (10 total)
2. **Each word appears ~3 times** across all 15 exercises
3. **Mark all ambiguous forms** with arrays (gen/dat sg, dat/abl pl, etc.)
4. **Include vocative differences** (2nd decl: amicus → amice)
5. **Add meaningful sentences** in integration exercises (14-15)
6. **Test each file** before moving to next one

## Estimating Time

- Define vocabulary: 1 hour
- Create 15 exercises manually: 4-6 hours
- Test and fix: 1 hour
- **Total: ~6-8 hours per series**

This is why auto-generation becomes valuable after the first manual series!
