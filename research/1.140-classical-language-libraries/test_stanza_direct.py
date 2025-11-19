#!/usr/bin/env python3
"""Test Stanza directly (bypassing CLTK) to isolate the bug"""

import stanza

# Download Latin model if needed
# stanza.download('la')  # Uncomment if needed

# Initialize Stanza directly
print("Loading Stanza Latin model...")
nlp = stanza.Pipeline('la', processors='tokenize,pos,lemma', verbose=False)

# Test sentences
test_sentences = [
    "Poeta carmina scribit.",
    "Puella rosam poetae dat.",
    "carmen poetae",
    "poetam video",
    "poetarum carmina"
]

for sentence in test_sentences:
    print(f"\n{'='*60}")
    print(f"Sentence: {sentence}")
    print(f"{'='*60}")

    doc = nlp(sentence)

    for sent in doc.sentences:
        for word in sent.words:
            print(f"{word.text:12s} → "
                  f"lemma: {word.lemma:12s} | "
                  f"upos: {word.upos:8s} | "
                  f"xpos: {word.xpos}")
