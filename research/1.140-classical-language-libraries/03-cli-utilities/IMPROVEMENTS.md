# UI/UX Improvements to latin-train

**Date:** 2025-01-18

## Changes Made

### 1. ✅ Backspace Support
**Problem:** If you mistype during identification, you had to use j/k to navigate away and back.

**Solution:** Added backspace/delete key support to clear current word's input instantly.

**Usage:** Press Backspace to clear the current word and start over.

---

### 2. ✅ Improved Visual Layout
**Problem:** Interface looked cluttered, hard to see what you're working on.

**Solution:** Redesigned layout to match the cleaner original interface:
- **Word indices**: Shows `[1] Puella [2] in [3] via` with current word highlighted in green
- **Italic sentence**: Sentence displayed in italic at top for visual separation
- **Current word focus**: Shows "Word 1: Puella" underlined below sentence
- **Better spacing**: Positioned elements with `term.move_y()` for consistent layout
- **Checkmarks**: Shows ✓ for correct, ✗ for incorrect with expected answer

**Before:**
```
→ Puella         NOUN 1st nominative
  in             PREP
  via
```

**After:**
```
          Puella in via ambulat (italic, centered)

     [1]Puella [2]in [3]via [4]ambulat (current word in green)

          Word 1: Puella (underlined)

  → [1] Puella        ✓ NOUN 1st nominative
    [2] in            ✓ PREP
    [3] via           ✗ NOUN 1st accusative → NOUN 1st ablative
    [4] ambulat
```

---

### 3. ✅ Ctrl-Number Navigation
**Problem:** Had to press j/k multiple times to reach later words.

**Solution:** Added Ctrl-1 through Ctrl-9 to jump directly to words.

**Usage:**
- Ctrl-1 → jump to word [1]
- Ctrl-2 → jump to word [2]
- etc.

---

### 4. ✅ Grammar Options Display
**Problem:** Users had to remember verb tense keys ([p]resent vs [i]mperfect).

**Solution:** Added grammar help line showing all options:

```
NOUN/ADJ: 1-5 decl, then n/g/d/a/b/v case | VERB: [p]resent [i]mperfect [f]uture pe[r]fect
```

Now users can see:
- **For nouns/adjectives:** Type declension (1-5), then case (n/g/d/a/b/v)
- **For verbs:** Type tense with clear labels showing which letter to press

---

## Complete Keyboard Reference

### Navigation
- `j` / `k` - Next/previous word
- `Ctrl-1` to `Ctrl-9` - Jump to word [1], [2], etc.
- `Backspace` - Clear current word's input

### POS (Part of Speech)
- `n` - NOUN
- `v` - VERB
- `a` - ADJECTIVE
- `p` - PREPOSITION

### Declension (after noun/adj)
- `1` - 1st declension
- `2` - 2nd declension
- `3` - 2nd/3rd declension
- `4` - 4th declension
- `5` - 5th declension

### Case (after declension)
- `n` - nominative
- `g` - genitive
- `d` - dative
- `a` - accusative
- `b` - ablative
- `v` - vocative

### Tense (after verb)
- `p` - present
- `i` - imperfect
- `f` - future
- `r` - perfect

### Actions
- `Enter` - Check answers (first press), advance to next sentence (second press)
- `q` - Quit

---

## Example Workflow

### Sentence: "Puella in via ambulat"

**Word [1] - Puella** (girl, nominative):
```
Type: n 1 n
      │ │ │
      │ │ └─ nominative
      │ └─── 1st declension
      └───── NOUN
```

**Word [2] - in** (in, preposition):
```
Type: p
      │
      └───── PREPOSITION (auto-advances)
```

**Word [3] - via** (street, ablative):
```
Type: n 1 b
      │ │ │
      │ │ └─ ablative
      │ └─── 1st declension
      └───── NOUN
```

**Word [4] - ambulat** (walks, present):
```
Type: v p
      │ │
      │ └─ present
      └─── VERB (auto-advances)
```

**Check answers:**
```
Press Enter
```

**Advance to next sentence:**
```
Press any key (or Enter)
```

---

## Rapid Input Example

For experienced users, the entire sentence can be done rapidly:

```
n1n  p  n1b  vp  Enter  Enter
 │    │   │    │    │      │
 │    │   │    │    │      └─ Next sentence
 │    │   │    │    └──────── Check
 │    │   │    └──────────── ambulat: VERB present
 │    │   └────────────────── via: NOUN 1st ablative
 │    └────────────────────── in: PREP
 └─────────────────────────── Puella: NOUN 1st nominative
```

Completes entire sentence in ~5 seconds!

---

## Testing the Improvements

Run the trainer:
```bash
./TEST_TRAINER.sh
```

Or directly:
```bash
bin/latin-train corpus/sample_parsed.jsonl --output progress/my_attempts.jsonl
```

Then analyze your results:
```bash
bin/latin-analyze progress/my_attempts.jsonl
```

---

## Technical Details

**Files Modified:**
- `bin/latin-train` (~330 lines)

**Key Changes:**
- Added `term.move_y()` positioning for cleaner layout
- Added backspace handler in `handle_input()` method
- Added Ctrl-number detection for jumping to words
- Enhanced display with word indices `[1], [2], [3]`
- Added grammar help line showing all options
- Added italic styling for sentence
- Added bold-green highlighting for current word
- Added ✓/✗ symbols for correct/incorrect answers

**Dependencies:**
- `blessed` - Terminal UI library (already installed)

---

## Future Enhancements

- **Undo last word** (Ctrl-Z)
- **Skip word** (Space bar)
- **Hint system** (? key shows expected answer for current word)
- **Timer display** (show time taken per word)
- **Streak counter** (show consecutive correct answers)
- **Sound effects** (optional beep on correct/incorrect)
