#!/usr/bin/env python3
"""Test with Perseus (classical Latin) package instead of ITTB (medieval)"""

import stanza

# Download perseus package if needed
print("Downloading Perseus (classical Latin) package...")
stanza.download('la', package='perseus', processors='tokenize,pos,lemma')

# Initialize with Perseus package
print("\nLoading Perseus pipeline...")
nlp = stanza.Pipeline('la', package='perseus', processors='tokenize,pos,lemma', verbose=False)

# Test the problematic cases
test_cases = [
    "Puella rosam poetae dat",
    "Poeta carmina scribit",
    "carmen poetae",
    "poetam video",
    "poetarum carmina",
    "nauta ambulat",
    "nautae domus",
    "agricola laborat",
    "agricolae terra",
    "scriba scribit",
    "scribae liber",
    "pirata navigat",
    "piratae navis"
]

print("\n" + "=" * 80)
print("TESTING WITH PERSEUS (CLASSICAL LATIN) PACKAGE")
print("=" * 80)

for sentence in test_cases:
    doc = nlp(sentence)
    print(f"\n{sentence}")
    for sent in doc.sentences:
        for word in sent.words:
            print(f"  {word.text:12s} → {word.lemma:12s} ({word.upos})")
