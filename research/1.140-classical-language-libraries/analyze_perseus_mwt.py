#!/home/ivanadamin/spawn-solutions/research/1.140-classical-language-libraries/02-implementations/.venv/bin/python
"""
Quick analysis of Perseus MWT (multi-word token) splitting behavior
"""

import stanza

# Initialize Perseus
nlp_perseus = stanza.Pipeline('la', package='perseus', processors='tokenize,pos,lemma',
                               verbose=False, logging_level='ERROR')

# Initialize PROIEL for comparison
nlp_proiel = stanza.Pipeline('la', package='proiel', processors='tokenize,pos,lemma',
                              verbose=False, logging_level='ERROR')

test_sentences = [
    "Puella rosam poetae dat",
    "poetae",
    "terra",
    "navis",
    "agricolae terra",
    "piratae navis"
]

print("="*80)
print("PERSEUS vs PROIEL TOKENIZATION COMPARISON")
print("="*80)

for sentence in test_sentences:
    print(f"\n📝 Sentence: '{sentence}'")
    print("-" * 80)

    # Perseus
    doc_p = nlp_perseus(sentence)
    perseus_words = [w.text for w in doc_p.sentences[0].words]

    # PROIEL
    doc_r = nlp_proiel(sentence)
    proiel_words = [w.text for w in doc_r.sentences[0].words]

    print(f"PERSEUS:  {len(perseus_words)} words → {perseus_words}")
    print(f"PROIEL:   {len(proiel_words)} words → {proiel_words}")

    if perseus_words != proiel_words:
        print(f"⚠️  MISMATCH DETECTED!")

        # Show where they differ
        max_len = max(len(perseus_words), len(proiel_words))
        for i in range(max_len):
            p_word = perseus_words[i] if i < len(perseus_words) else "—"
            r_word = proiel_words[i] if i < len(proiel_words) else "—"

            if p_word != r_word:
                print(f"  Position {i}: Perseus='{p_word}' vs PROIEL='{r_word}'")

print("\n" + "="*80)
print("ANALYSIS")
print("="*80)

# Test "poetae" in detail
sentence = "poetae"
doc = nlp_perseus(sentence)
sent = doc.sentences[0]

print(f"\nDetailed analysis of '{sentence}':")
print(f"Tokens ({len(sent.tokens)}):")
for token in sent.tokens:
    print(f"  - id={token.id}, text='{token.text}'")

print(f"\nWords ({len(sent.words)}):")
for word in sent.words:
    print(f"  - id={word.id}, text='{word.text}', lemma='{word.lemma}', upos='{word.upos}'")

# Check if this is actually MWT or just wrong tokenization
print("\nConclusion:")
if len(sent.tokens) > len(sent.words):
    print("  This appears to be MWT (multi-word token expansion)")
elif len(sent.tokens) < len(sent.words):
    print("  This appears to be token combining")
elif len(sent.tokens) == len(sent.words) and len(sent.words) > 1:
    print("  This appears to be INCORRECT TOKENIZATION (not MWT)")
    print("  Perseus is incorrectly splitting single words into multiple tokens")
