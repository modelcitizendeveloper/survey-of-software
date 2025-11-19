#!/usr/bin/env python3
"""Test 1st declension masculine nouns to identify parsing bugs"""

import stanza

# Initialize Stanza directly
print("Loading Stanza Latin model...")
nlp = stanza.Pipeline('la', processors='tokenize,pos,lemma', verbose=False)

# Test all 1st declension masculine nouns
test_cases = [
    # nauta (sailor)
    ("nauta ambulat", "nauta", "NOUN"),
    ("nautae domus", "nauta", "NOUN"),  # genitive
    ("nautae do", "nauta", "NOUN"),     # dative
    ("nautam video", "nauta", "NOUN"),  # accusative
    ("nautarum naves", "nauta", "NOUN"), # genitive plural

    # agricola (farmer)
    ("agricola laborat", "agricola", "NOUN"),
    ("agricolae terra", "agricola", "NOUN"),  # genitive
    ("agricolae do", "agricola", "NOUN"),     # dative
    ("agricolam video", "agricola", "NOUN"),  # accusative
    ("agricolarum agri", "agricola", "NOUN"), # genitive plural

    # scriba (scribe)
    ("scriba scribit", "scriba", "NOUN"),
    ("scribae liber", "scriba", "NOUN"),      # genitive
    ("scribae do", "scriba", "NOUN"),         # dative
    ("scribam video", "scriba", "NOUN"),      # accusative
    ("scribarum tabulae", "scriba", "NOUN"),  # genitive plural

    # pirata (pirate)
    ("pirata navigat", "pirata", "NOUN"),
    ("piratae navis", "pirata", "NOUN"),      # genitive
    ("piratae do", "pirata", "NOUN"),         # dative
    ("piratam video", "pirata", "NOUN"),      # accusative
    ("piratarum scelera", "pirata", "NOUN"),  # genitive plural
]

print("\n" + "=" * 80)
print("TESTING 1st DECLENSION MASCULINE NOUNS")
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
print("SUMMARY")
print("=" * 80)
print(f"Total tests: {len(test_cases)}")
print(f"Correct: {len(correct)} ({len(correct)/len(test_cases)*100:.1f}%)")
print(f"Errors: {len(errors)} ({len(errors)/len(test_cases)*100:.1f}%)")

if errors:
    print("\n" + "=" * 80)
    print("DETAILED ERROR REPORT")
    print("=" * 80)

    for error in errors:
        print(f"\nWord: {error['word']}")
        print(f"  Sentence: {error['sentence']}")
        print(f"  Expected: {error['expected_lemma']} ({error['expected_pos']})")
        print(f"  Got:      {error['actual_lemma']} ({error['actual_pos']})")

    # Group errors by lemma misidentification
    print("\n" + "=" * 80)
    print("ERROR PATTERNS")
    print("=" * 80)

    from collections import defaultdict
    patterns = defaultdict(list)

    for error in errors:
        key = f"{error['expected_lemma']} → {error['actual_lemma']}"
        patterns[key].append(error['word'])

    for pattern, words in patterns.items():
        print(f"\n{pattern}")
        print(f"  Affected forms: {', '.join(words)}")
        print(f"  Count: {len(words)}")

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

if len(errors) == 0:
    print("✓ All 1st declension masculine nouns parsed correctly!")
else:
    print(f"✗ Found {len(errors)} parsing errors across 1st declension masculine nouns")
    print("  This suggests a systematic issue with the Latin model's handling")
    print("  of 1st declension masculine nouns in genitive/dative forms.")
