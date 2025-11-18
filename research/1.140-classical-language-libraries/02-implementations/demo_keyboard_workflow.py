#!/usr/bin/env python3
"""
Demo: Show how keyboard workflow would work

This simulates the user interaction for "Puella in via ambulat"
"""

from cltk import NLP

print("=" * 70)
print("LATIN KEYBOARD TRAINER - WORKFLOW DEMO")
print("=" * 70)

# Parse sentence
sentence = "Puella in via ambulat"
print(f"\nSentence: {sentence}")
print("(The girl walks in the street)")

nlp = NLP(language="lat", suppress_banner=True)
doc = nlp.analyze(text=sentence)

# Show what parser gives us
print("\n" + "=" * 70)
print("PARSER OUTPUT (What we validate against)")
print("=" * 70)

for i, word in enumerate(doc.words, 1):
    print(f"\n[{i}] {word.string}")
    print(f"    POS:   {word.upos}")
    print(f"    Lemma: {word.lemma}")
    print(f"    XPOS:  {word.xpos}")

# Simulate user keyboard input
print("\n" + "=" * 70)
print("USER KEYBOARD INPUT SIMULATION")
print("=" * 70)

print("""
User sees:
    [1]Puella  [2]in  [3]via  [4]ambulat
     ^^^^^^
    (word 1 highlighted)

User types:  n 1 n
    n   → POS = NOUN
    1   → Declension = 1st
    n   → Case = nominative
    ✓   → Auto-advance to word 2

    [1]Puella  [2]in  [3]via  [4]ambulat
                ^^
               (word 2 highlighted)

User types:  p
    p   → POS = PREPOSITION
    ✓   → Auto-advance to word 3

    [1]Puella  [2]in  [3]via  [4]ambulat
                       ^^^
                      (word 3 highlighted)

User types:  n 1 b
    n   → POS = NOUN
    1   → Declension = 1st
    b   → Case = ablative
    ✓   → Auto-advance to word 4

    [1]Puella  [2]in  [3]via  [4]ambulat
                                ^^^^^^
                               (word 4 highlighted)

User types:  v p i 3
    v   → POS = VERB
    p   → Tense = present
    i   → Mood = indicative
    3   → Person = 3rd
    ✓   → Complete!

User presses: Enter

RESULTS:
✓ [1] Puella   NOUN, 1st decl, nom
✓ [2] in       PREP
✓ [3] via      NOUN, 1st decl, abl
✓ [4] ambulat  VERB, present, indic, 3rd

Score: 4/4 (100%) ✓
""")

print("\n" + "=" * 70)
print("RAPID INPUT MODE (Expert)")
print("=" * 70)

print("""
Same sentence, but user types entire sequence at once:

    n1n p n1b vpi3 Enter

Breakdown:
    n1n      → Word 1: NOUN, 1st, nominative
    p        → Word 2: PREP
    n1b      → Word 3: NOUN, 1st, ablative
    vpi3     → Word 4: VERB, present, indicative, 3rd
    Enter    → Check answers

Total keypresses: 10
Time: ~3 seconds for experienced user
""")

print("\n" + "=" * 70)
print("KEYBOARD COMMAND REFERENCE")
print("=" * 70)

print("""
NAVIGATION:
    j / k           Next/previous word
    Ctrl-1 .. 9     Jump to word N
    0 / $           First/last word

POS TAGS:
    n               NOUN (→ prompts for declension)
    v               VERB (→ prompts for tense)
    a               ADJECTIVE (→ prompts for declension)
    p               PREPOSITION (auto-advance)
    c               CONJUNCTION (auto-advance)
    d               ADVERB (auto-advance)

DECLENSION (after n/a):
    1 2 3 4 5       1st through 5th declension

CASE (after declension):
    n               Nominative
    g               Genitive
    d               Dative
    a               Accusative
    b               Ablative
    v               Vocative

TENSE (after v):
    p               Present
    i               Imperfect
    f               Future
    r               Perfect
    l               Pluperfect
    u               Future perfect

ACTIONS:
    Enter           Check answers
    u               Undo current word
    r               Reset current word
    R               Reset entire sentence
    q               Quit
""")

print("\n" + "=" * 70)
print("WHY THIS INTERFACE WORKS")
print("=" * 70)

print("""
1. FAST: Expert users can analyze 4-word sentence in ~3 seconds
2. VIM-LIKE: Familiar to programmers, efficient for everyone
3. PROGRESSIVE: Start with just POS, add complexity gradually
4. IMMEDIATE FEEDBACK: See results instantly after Enter
5. SRS-READY: Track mistakes, schedule reviews automatically

Comparison to clicking:
    - Mouse clicking: ~15 seconds for same sentence
    - Keyboard: ~3 seconds (5x faster!)
    - Flow state: Stay in keyboard, never reach for mouse

Perfect for building reading fluency through rapid practice!
""")

print("=" * 70)
