# Keyboard-Driven Latin Reading Interface

**Design Philosophy**: Vim-like keyboard workflow for rapid grammatical analysis

---

## User Experience Flow

### 1. Display Sentence in Context

```
┌────────────────────────────────────────────────────────────────┐
│ De Bello Gallico - Book 1, Chapter 1                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ Gallia est omnis divisa in partes tres, quarum unam           │
│ incolunt Belgae, aliam Aquitani, tertiam qui ipsorum          │
│ lingua Celtae, nostra Galli appellantur.                      │
│                                                                │
│ [1]      [2]    [3]     [4]      [5]  [6]     [7]             │
│ Gallia   est    omnis   divisa   in   partes  tres            │
│ ━━━━━━                                                         │
│ Selected: Word 1                                               │
│                                                                │
│ Your answers:                                                  │
│   POS:        [____]  (n=noun, v=verb, a=adj, p=prep, ...)    │
│   Declension: [____]  (1-5 for nouns)                         │
│   Case:       [____]  (n=nom, g=gen, d=dat, a=acc, b=abl)     │
│                                                                │
│ Press Enter to check | Ctrl-N for next sentence               │
└────────────────────────────────────────────────────────────────┘
```

---

## Keyboard Commands

### Navigation

| Key | Action |
|-----|--------|
| `Ctrl-1` through `Ctrl-9` | Jump to word 1-9 in sentence |
| `Ctrl-0` | Jump to word 10 |
| `j` / `k` | Next/previous word |
| `w` / `b` | Forward/backward word (vim-style) |
| `0` / `$` | First/last word in sentence |
| `Ctrl-N` | Next sentence |
| `Ctrl-P` | Previous sentence |

### Input Mode

| Key | Field | Options |
|-----|-------|---------|
| `n` | POS = NOUN | Unlocks declension field |
| `v` | POS = VERB | Unlocks tense field |
| `a` | POS = ADJECTIVE | Unlocks declension field |
| `p` | POS = PREPOSITION | - |
| `c` | POS = CONJUNCTION | - |
| `d` | POS = ADVERB | - |

**For Nouns/Adjectives** (after pressing `n` or `a`):
| Key | Declension |
|-----|------------|
| `1` | 1st declension |
| `2` | 2nd declension |
| `3` | 3rd declension |
| `4` | 4th declension |
| `5` | 5th declension |

**Case** (after declension):
| Key | Case |
|-----|------|
| `n` | Nominative |
| `g` | Genitive |
| `d` | Dative |
| `a` | Accusative |
| `b` | Ablative (from Latin 'b' for ablativus) |
| `v` | Vocative |

**For Verbs** (after pressing `v`):
| Key | Tense |
|-----|-------|
| `p` | Present |
| `i` | Imperfect |
| `f` | Future |
| `r` | Perfect (peRfect) |
| `l` | Pluperfect (pLuperfect) |
| `u` | Future perfect (futUre perfect) |

**Mood** (after tense):
| Key | Mood |
|-----|------|
| `i` | Indicative |
| `s` | Subjunctive |
| `m` | Imperative |

**Person** (after mood):
| Key | Person |
|-----|--------|
| `1` | 1st person |
| `2` | 2nd person |
| `3` | 3rd person |

### Review

| Key | Action |
|-----|--------|
| `Enter` | Check answers for current sentence |
| `Space` | Skip current word |
| `u` | Undo last input |
| `r` | Reset current word |
| `R` | Reset entire sentence |

---

## Example Workflow

**Sentence**: "Puella in via ambulat"

### User Input Sequence

```
1. Ctrl-1          # Jump to word 1 (Puella)
2. n               # POS = NOUN
3. 1               # 1st declension
4. n               # Nominative case
   → Complete: NOUN, 1st declension, nominative

5. j               # Next word (in)
6. p               # POS = PREPOSITION
   → Complete: PREPOSITION

7. j               # Next word (via)
8. n 1 b           # NOUN, 1st declension, ablative
   → Complete: NOUN, 1st declension, ablative

9. j               # Next word (ambulat)
10. v              # POS = VERB
11. p              # Present tense
12. i              # Indicative mood
13. 3              # 3rd person
   → Complete: VERB, present, indicative, 3rd person

14. Enter          # Check answers
```

**Feedback**:
```
┌────────────────────────────────────────────────────────────────┐
│ Results: 4/4 words correct! ✓                                  │
├────────────────────────────────────────────────────────────────┤
│ [1] Puella   ✓  NOUN, 1st decl, nom                           │
│ [2] in       ✓  PREP                                           │
│ [3] via      ✓  NOUN, 1st decl, abl                           │
│ [4] ambulat  ✓  VERB, present, indic, 3rd                     │
│                                                                │
│ Press Ctrl-N for next sentence or R to retry                  │
└────────────────────────────────────────────────────────────────┘
```

---

## Rapid Input Modes

### Expert Mode (Chained Input)

For experienced users, allow chained commands:

```
Ctrl-1 n1n j p j n1b j vpi3 Enter
  │    │   │ │ │   │     │
  │    │   │ │ │   │     └─ VERB, present, indic, 3rd
  │    │   │ │ │   └─────── NOUN, 1st, abl
  │    │   │ │ └─────────── PREP
  │    │   │ └───────────── Next word
  │    │   └─────────────── NOUN, 1st, nom
  │    └───────────────────── Word 1
  └────────────────────────── Jump to word 1
```

### Auto-Advance Mode

After completing a word, automatically advance to next:

```
# Enable auto-advance
:set autoadvance

# Now just type for each word in sequence
n1n p n1b vpi3 Enter
 │   │  │    │
 └─ Word 1
     └─ Word 2
        └─ Word 3
           └─ Word 4
```

---

## Backend Integration

### Parser Response Format

```python
{
    "sentence": "Puella in via ambulat",
    "words": [
        {
            "index": 1,
            "form": "Puella",
            "lemma": "puella",
            "answer": {
                "pos": "NOUN",
                "declension": "1st",
                "case": "nominative",
                "gender": "feminine",
                "number": "singular"
            }
        },
        {
            "index": 2,
            "form": "in",
            "lemma": "in",
            "answer": {
                "pos": "PREP"
            }
        },
        {
            "index": 3,
            "form": "via",
            "lemma": "via",
            "answer": {
                "pos": "NOUN",
                "declension": "1st",
                "case": "ablative",
                "gender": "feminine",
                "number": "singular"
            }
        },
        {
            "index": 4,
            "form": "ambulat",
            "lemma": "ambulo",
            "answer": {
                "pos": "VERB",
                "tense": "present",
                "mood": "indicative",
                "person": "3rd",
                "number": "singular"
            }
        }
    ]
}
```

### Validation Logic

```python
def validate_user_answer(user_input, correct_answer):
    """
    Compare user input to parser output

    Args:
        user_input: {'pos': 'n', 'declension': '1', 'case': 'n'}
        correct_answer: {'pos': 'NOUN', 'declension': '1st', 'case': 'nominative'}

    Returns:
        {
            'correct': True/False,
            'errors': ['case: expected nominative, got accusative'],
            'score': 0.75  # Partial credit
        }
    """

    # Normalize user input
    normalized = {
        'pos': POS_MAP[user_input['pos']],  # 'n' → 'NOUN'
        'declension': user_input.get('declension'),
        'case': CASE_MAP.get(user_input.get('case')),  # 'n' → 'nominative'
    }

    # Compare fields
    errors = []
    score = 0
    total_fields = 0

    for field in correct_answer.keys():
        total_fields += 1
        if normalized.get(field) == correct_answer[field]:
            score += 1
        else:
            errors.append(f"{field}: expected {correct_answer[field]}, got {normalized.get(field)}")

    return {
        'correct': len(errors) == 0,
        'errors': errors,
        'score': score / total_fields if total_fields > 0 else 0
    }
```

---

## Implementation Options

### Option 1: Terminal UI (TUI) with `curses`

**Pros**:
- Native vim-like feel
- Fast, lightweight
- Works over SSH
- No dependencies beyond Python

**Cons**:
- Terminal-only (no web access)
- More complex UI code

**Libraries**:
- `curses` (built-in)
- `blessed` (modern curses wrapper)
- `textual` (modern TUI framework)

### Option 2: Vim Plugin

**Pros**:
- Perfect vim integration
- Existing vim users already comfortable
- Can edit Latin texts directly

**Cons**:
- Requires vim/neovim
- Steeper learning curve for non-vim users

**Implementation**:
- Python interface via `pynvim` or `vim.python3`
- CLTK parser runs in background
- Vim highlights words, accepts keyboard input
- Split window shows feedback

### Option 3: Web App with Vim Keybindings

**Pros**:
- Accessible anywhere (browser)
- Can have both keyboard and mouse input
- Rich UI possibilities (highlighting, animations)
- Mobile support (optional)

**Cons**:
- Need web backend
- More complex deployment

**Libraries**:
- Frontend: `codemirror` (vim keybindings built-in)
- Backend: FastAPI + CLTK
- Keyboard handling: JavaScript event listeners

### Option 4: Hybrid (Recommended)

**TUI for power users + Web for accessibility**

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  CLTK Parser Backend (Python + FastAPI)        │
│  ├── Latin sentence parsing                    │
│  ├── Answer validation                         │
│  └── SRS scheduling                            │
│                                                 │
└─────────┬───────────────────────────┬───────────┘
          │                           │
    ┌─────▼──────┐            ┌───────▼────────┐
    │            │            │                │
    │  TUI App   │            │  Web App       │
    │  (curses)  │            │  (FastAPI +    │
    │            │            │   htmx/Alpine) │
    │  Vim-like  │            │  Vim bindings  │
    │  keyboard  │            │  optional      │
    │            │            │                │
    └────────────┘            └────────────────┘
```

---

## Minimal Viable Interface (MVP)

### TUI Prototype with `blessed`

```python
from blessed import Terminal
from cltk import NLP

class LatinKeyboardTrainer:
    def __init__(self):
        self.term = Terminal()
        self.nlp = NLP(language="lat", suppress_banner=True)
        self.current_word = 0
        self.user_answers = {}

    def run(self, sentence):
        """Main training loop"""

        # Parse sentence
        doc = self.nlp.analyze(text=sentence)
        words = list(doc.words)

        with self.term.fullscreen(), self.term.cbreak():
            while True:
                # Display UI
                self.display(words, sentence)

                # Get input
                key = self.term.inkey()

                # Navigation
                if key.name == 'KEY_ESCAPE':
                    break
                elif key == 'j':
                    self.current_word = min(self.current_word + 1, len(words) - 1)
                elif key == 'k':
                    self.current_word = max(self.current_word - 1, 0)
                elif key.startswith('\x00'):  # Ctrl key
                    num = int(key[1]) if key[1].isdigit() else None
                    if num is not None:
                        self.current_word = min(num - 1, len(words) - 1)

                # Input
                elif key in 'nvapcd':  # POS tags
                    self.record_pos(self.current_word, key)
                elif key in '12345':  # Declensions
                    self.record_declension(self.current_word, key)

                # Check answers
                elif key.name == 'KEY_ENTER':
                    self.check_answers(words)
                    break

    def display(self, words, sentence):
        """Render UI"""
        print(self.term.clear())
        print(self.term.move_y(2) + self.term.center(sentence))

        # Display words with indices
        word_display = " ".join([f"[{i+1}]{w.string}" for i, w in enumerate(words)])
        print(self.term.move_y(4) + self.term.center(word_display))

        # Highlight current word
        current = words[self.current_word]
        print(self.term.move_y(6) + self.term.center(
            self.term.bold_underline(f"Word {self.current_word + 1}: {current.string}")
        ))

        # Show user's answer so far
        if self.current_word in self.user_answers:
            ans = self.user_answers[self.current_word]
            print(self.term.move_y(8) + self.term.center(f"Your answer: {ans}"))

        # Instructions
        print(self.term.move_y(self.term.height - 3) + self.term.center(
            "j/k: next/prev | n/v/a/p: POS | 1-5: declension | Enter: check"
        ))
```

---

## Progressive Difficulty

### Level 1: POS Only
```
Just identify: n (noun), v (verb), a (adj), p (prep)
```

### Level 2: POS + Declension/Tense
```
Nouns: n + declension (1-5)
Verbs: v + tense (p/i/f/r)
```

### Level 3: Full Analysis
```
Nouns: n + decl + case (n/g/d/a/b/v)
Verbs: v + tense + mood + person
```

### Level 4: Speed Mode
```
Timed - complete sentence in <30 seconds
Accuracy must be >80%
```

---

## SRS Integration

After each sentence, track:
- Which words user got wrong
- Time taken per word
- Confusion patterns (e.g., always mixing nominative/accusative)

Schedule review:
```python
from datetime import datetime, timedelta

def schedule_review(word, correct, time_taken):
    """
    SM-2 algorithm for spaced repetition

    If correct:
        - Interval increases (1 day → 3 days → 1 week → 2 weeks)
    If wrong:
        - Reset to 1 day
    """

    if correct:
        return {
            'next_review': datetime.now() + timedelta(days=calculate_interval()),
            'difficulty': decrease_difficulty()
        }
    else:
        return {
            'next_review': datetime.now() + timedelta(days=1),
            'difficulty': increase_difficulty()
        }
```

---

## Next Steps

1. **Prototype TUI** with `blessed` (1-2 hours)
2. **Test keyboard workflow** with real sentences (1 hour)
3. **Integrate CLTK parser** backend (30 min)
4. **Add answer validation** (1 hour)
5. **Test with user** and refine keybindings

**Estimated MVP time**: 4-5 hours of coding

Ready to build prototype?
