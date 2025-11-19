#!/usr/bin/env python3
"""Compare ALL Latin packages to find the best one"""

import stanza

packages = ['ittb', 'perseus', 'proiel', 'llct']

test_sentence = "Puella rosam poetae dat"

print("=" * 80)
print(f"Testing sentence: {test_sentence}")
print("=" * 80)

for package in packages:
    print(f"\n{'='*80}")
    print(f"Package: {package.upper()}")
    print(f"{'='*80}")

    try:
        # Download if needed
        stanza.download('la', package=package, processors='tokenize,pos,lemma', verbose=False, logging_level='ERROR')

        # Load pipeline
        nlp = stanza.Pipeline('la', package=package, processors='tokenize,pos,lemma', verbose=False, logging_level='ERROR')

        # Parse
        doc = nlp(test_sentence)

        for sent in doc.sentences:
            for word in sent.words:
                status = "✓" if word.text == "poetae" and word.lemma.lower() == "poeta" and word.upos == "NOUN" else ""
                print(f"{status:2s} {word.text:12s} → lemma: {word.lemma:12s} | upos: {word.upos:8s}")

    except Exception as e:
        print(f"ERROR: {e}")

print("\n" + "=" * 80)
print("SUMMARY: Which package correctly parses 'poetae' as NOUN 'poeta'?")
print("=" * 80)
