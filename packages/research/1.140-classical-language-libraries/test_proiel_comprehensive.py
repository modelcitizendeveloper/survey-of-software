#!/usr/bin/env python3
"""Comprehensive test of PROIEL package with all 1st declension masculine nouns"""

import stanza

# Use PROIEL package
print("Loading PROIEL package...")
nlp = stanza.Pipeline('la', package='proiel', processors='tokenize,pos,lemma', verbose=False, logging_level='ERROR')

# Test all problematic cases from before
test_cases = [
    # poeta
    ("poeta carmina scribit", "poeta", "NOUN"),
    ("poetae domus", "poeta", "NOUN"),
    ("poetam video", "poeta", "NOUN"),
    ("poetarum carmina", "poeta", "NOUN"),

    # nauta
    ("nauta ambulat", "nauta", "NOUN"),
    ("nautae domus", "nauta", "NOUN"),
    ("nautam video", "nauta", "NOUN"),
    ("nautarum naves", "nauta", "NOUN"),

    # agricola
    ("agricola laborat", "agricola", "NOUN"),
    ("agricolae terra", "agricola", "NOUN"),
    ("agricolam video", "agricola", "NOUN"),
    ("agricolarum agri", "agricola", "NOUN"),

    # scriba
    ("scriba scribit", "scriba", "NOUN"),
    ("scribae liber", "scriba", "NOUN"),
    ("scribam video", "scriba", "NOUN"),
    ("scribarum tabulae", "scriba", "NOUN"),

    # pirata
    ("pirata navigat", "pirata", "NOUN"),
    ("piratae navis", "pirata", "NOUN"),
    ("piratam video", "pirata", "NOUN"),
    ("piratarum scelera", "pirata", "NOUN"),
]

print("\n" + "=" * 80)
print("TESTING PROIEL PACKAGE - 1st DECLENSION MASCULINE NOUNS")
print("=" * 80)

errors = []
correct = []

for sentence, expected_lemma, expected_pos in test_cases:
    doc = nlp(sentence)

    # Get the first word (the noun we're testing)
    word = doc.sentences[0].words[0]

    # Check if it matches expectations
    is_correct = (word.lemma.lower() == expected_lemma.lower() and word.upos == expected_pos)

    status = "✓" if is_correct else "✗"

    print(f"{status} {word.text:15s} → lemma: {word.lemma:15s} | "
          f"upos: {word.upos:8s} | expected: {expected_lemma}/{expected_pos}")

    if is_correct:
        correct.append((word.text, word.lemma, word.upos))
    else:
        errors.append({
            'word': word.text,
            'actual_lemma': word.lemma,
            'actual_pos': word.upos,
            'expected_lemma': expected_lemma,
            'expected_pos': expected_pos,
            'sentence': sentence
        })

# Summary
print("\n" + "=" * 80)
print("SUMMARY - PROIEL vs ITTB (default)")
print("=" * 80)
print(f"Total tests: {len(test_cases)}")
print(f"Correct: {len(correct)} ({len(correct)/len(test_cases)*100:.1f}%)")
print(f"Errors: {len(errors)} ({len(errors)/len(test_cases)*100:.1f}%)")
print(f"\nCompare to ITTB: 9/20 correct (45%)")
print(f"PROIEL: {len(correct)}/20 correct ({len(correct)/len(test_cases)*100:.1f}%)")

if errors:
    print("\n" + "=" * 80)
    print("REMAINING ERRORS WITH PROIEL")
    print("=" * 80)

    for error in errors:
        print(f"\n✗ {error['word']}")
        print(f"  Expected: {error['expected_lemma']} ({error['expected_pos']})")
        print(f"  Got:      {error['actual_lemma']} ({error['actual_pos']})")
