# Latin Learning CLI Utilities

Unix-philosophy approach to Latin grammar training: small, composable command-line utilities.

## Architecture

```
┌─────────────┐
│ Raw Latin   │
│ Text        │
└──────┬──────┘
       │
       ▼ latin-parse
┌─────────────┐
│ Parsed      │
│ JSONL       │
└──────┬──────┘
       │
       ▼ latin-train
┌─────────────┐
│ Attempts    │
│ JSONL       │
└──────┬──────┘
       │
       ▼ latin-analyze
┌─────────────┐
│ Statistics  │
│ & Reports   │
└─────────────┘
```

## Three Utilities

### 1. `latin-parse` - Text Parser

Parse raw Latin text into structured JSONL format.

**Usage:**
```bash
latin-parse input.txt > parsed.jsonl
cat input.txt | latin-parse > parsed.jsonl
```

**Output:** One JSON object per line (JSONL)
```json
{
  "sentence": "Puella in via ambulat",
  "words": [
    {"text": "Puella", "lemma": "puella", "pos": "NOUN", "declension": "1st", "case": "nominative"},
    {"text": "in", "lemma": "in", "pos": "ADP"},
    {"text": "via", "lemma": "via", "pos": "NOUN", "declension": "1st", "case": "ablative"},
    {"text": "ambulat", "lemma": "ambulo", "pos": "VERB", "tense": "present"}
  ]
}
```

**Features:**
- Uses CLTK NLP pipeline with Stanza models
- Extracts POS tags, lemmas, declensions, cases, tenses
- Pre-parse entire corpus once (slow), then instant retrieval
- Output is portable, version-controllable

---

### 2. `latin-train` - Interactive Trainer

Vim-like keyboard interface for identifying grammatical forms.

**Usage:**
```bash
latin-train parsed.jsonl --output attempts.jsonl
latin-train parsed.jsonl --output attempts.jsonl --resume
latin-train parsed.jsonl --output attempts.jsonl --user ivan
```

**Keyboard Commands:**
- `j/k` - next/previous word
- `n` - NOUN
- `v` - VERB
- `a` - ADJECTIVE
- `p` - PREPOSITION
- `1-5` - declension (after noun/adj)
- `n/g/d/a/b/v` - case (nominative/genitive/dative/accusative/ablative/vocative)
- `p/i/f/r` - tense (present/imperfect/future/perfect)
- `Enter` - check answers
- `q` - quit

**Rapid Input Example:**
```
n1n p n1b vp Enter
 │   │  │   │
 └─ Word 1: NOUN, 1st declension, nominative
     └─ Word 2: PREPOSITION
        └─ Word 3: NOUN, 1st declension, ablative
           └─ Word 4: VERB, present tense
```

**Output:** Appends attempt records to JSONL file
```json
{
  "sentence_id": 0,
  "sentence": "Puella in via ambulat",
  "timestamp": "2025-01-18T10:30:00",
  "user": "ivan",
  "attempts": [
    {"word": "Puella", "expected": {"pos": "NOUN", "declension": "1st", "case": "nominative"}, "user_input": {...}, "correct": true}
  ],
  "accuracy": 0.75
}
```

**Features:**
- Reads pre-parsed sentences (instant, no parsing delay)
- Fullscreen terminal UI with immediate feedback
- Auto-advance between sentences
- Resume from last position with `--resume`
- Append-only output (never overwrites)

---

### 3. `latin-analyze` - Statistics Analyzer

Analyze training attempts and identify weakness patterns.

**Usage:**
```bash
# Overall statistics (default)
latin-analyze attempts.jsonl

# List all mistakes
latin-analyze attempts.jsonl --mistakes

# Show progress over time
latin-analyze attempts.jsonl --progress

# Export mistakes to SRS format
latin-analyze attempts.jsonl --export srs.json
```

**Output:**
```
======================================================================
LATIN TRAINING ANALYSIS
======================================================================
User: ivan
Period: 2025-01-15 to 2025-01-18

Overall Accuracy: 78%
Total Sentences: 45
Total Words Analyzed: 312

======================================================================
MISTAKE PATTERNS
======================================================================

Case Confusion: 12 errors
  • nominative/accusative: 8 times
  • accusative/ablative: 4 times

Declension Confusion: 8 errors
  • 2nd/3rd/3rd: 5 times
  • 1st/2nd: 3 times

======================================================================
STRENGTHS & WEAKNESSES
======================================================================

Weaknesses (lowest accuracy):
  • Case Ablative: 67% (8/12)
  • Decl 2nd/3rd: 60% (6/10)
  • Tense Imperfect: 70% (7/10)

Strengths (highest accuracy):
  • Pos PREP: 100% (24/24)
  • Decl 1st: 95% (38/40)
  • Tense Present: 92% (23/25)
```

**Features:**
- Identifies confusion patterns (nom/acc, 1st/2nd decl, etc.)
- Shows strengths and weaknesses by category
- Progress tracking over time
- Export to SRS format for targeted review

---

## Workflow Examples

### One-time Corpus Preparation

```bash
cd 03-cli-utilities

# Parse Caesar's Gallic Wars
bin/latin-parse corpus/caesar_gallic_wars.txt > corpus/caesar_parsed.jsonl

# Parse Cicero's Orations
bin/latin-parse corpus/cicero_orations.txt > corpus/cicero_parsed.jsonl

# Parse Ovid's Metamorphoses
bin/latin-parse corpus/ovid_metamorphoses.txt > corpus/ovid_parsed.jsonl
```

### Daily Practice Session

```bash
# Practice Caesar (resumes from last position)
bin/latin-train corpus/caesar_parsed.jsonl --output progress/attempts.jsonl --resume --user ivan

# Review mistakes
bin/latin-analyze progress/attempts.jsonl --mistakes

# Check progress
bin/latin-analyze progress/attempts.jsonl --progress
```

### Advanced: Generate SRS Review Deck

```bash
# Export mistakes to SRS format
bin/latin-analyze progress/attempts.jsonl --export srs.json

# Review weak areas (future feature)
# bin/latin-drill srs.json --output progress/attempts.jsonl
```

---

## File Structure

```
03-cli-utilities/
├── bin/
│   ├── latin-parse      # Text → JSONL parser
│   ├── latin-train      # Interactive trainer
│   └── latin-analyze    # Statistics analyzer
├── corpus/
│   ├── sample.txt              # Raw Latin texts
│   ├── sample_parsed.jsonl     # Pre-parsed (read-only)
│   ├── caesar_parsed.jsonl
│   └── cicero_parsed.jsonl
├── progress/
│   └── attempts.jsonl          # Your training history (append-only)
└── README.md
```

---

## Advantages of This Approach

✅ **No database** - files are the database
✅ **Version control** - `git add progress/attempts.jsonl`
✅ **Composable** - pipe into `jq`, `grep`, other Unix tools
✅ **Fast** - pre-parsed corpus loads instantly
✅ **Portable** - copy files, practice anywhere
✅ **Testable** - easy to test with sample inputs
✅ **Extensible** - add new analyzers without changing trainer
✅ **Simple** - each tool does one thing well

---

## Testing the Sample Corpus

```bash
cd /home/ivanadamin/spawn-solutions/research/1.140-classical-language-libraries/03-cli-utilities

# Already parsed:
# bin/latin-parse corpus/sample.txt > corpus/sample_parsed.jsonl

# Try the trainer:
bin/latin-train corpus/sample_parsed.jsonl --output progress/test_attempts.jsonl

# Analyze results:
bin/latin-analyze progress/test_attempts.jsonl
```

---

## Future Enhancements

- `latin-drill` - SRS-based review from mistakes
- `latin-vocab` - Track vocabulary knowledge
- `latin-difficulty` - Calculate text difficulty (i+1)
- `latin-export` - Export to Anki format
- Integration with training corpus (1200+ progressive sentences)

---

## Technical Details

**Dependencies:**
- CLTK (Classical Language Toolkit)
- blessed (terminal UI)
- Python 3.11+

**Virtual Environment:**
Uses existing venv at: `../02-implementations/.venv`

**JSONL Format:**
- One JSON object per line
- Human-readable
- Easy to process with `jq`, `grep`, `awk`
- Git-friendly (line-based diffs)
