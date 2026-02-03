#!/home/ivanadamin/spawn-solutions/research/1.140-classical-language-libraries/02-implementations/.venv/bin/python
"""
Test how different Latin packages handle REAL enclitics vs regular word endings

REAL Latin enclitics:
- -que (and) - "Senatus Populusque Romanus" → "Populus" + "-que"
- -ne (question) - "videsne?" → "vides" + "-ne"
- -ve (or) - "homine ve" → "homine" + "-ve"

NOT enclitics (just case endings):
- -ae (genitive/dative singular)
- -a (nominative/ablative singular)
- -s (nominative singular)
"""

import stanza

# Test with all packages
packages = ['perseus', 'proiel', 'ittb']

test_cases = [
    # REAL enclitics (should be split)
    ("Senatus Populusque Romanus", "Populusque should split into Populus + que"),
    ("videsne", "videsne should split into vides + ne"),
    ("terrave", "terrave should split into terra + ve"),

    # NOT enclitics (should NOT be split)
    ("poetae", "poetae is genitive, NOT enclitic - should stay as one word"),
    ("terra", "terra is nominative, should stay as one word"),
    ("navis", "navis is nominative, should stay as one word"),
]

print("="*80)
print("LATIN ENCLITIC HANDLING TEST")
print("="*80)
print("\nReal enclitics: -que (and), -ne (question), -ve (or)")
print("Regular endings: -ae, -a, -s (case/number markers)")
print()

for package in packages:
    print(f"\n{'='*80}")
    print(f"PACKAGE: {package.upper()}")
    print(f"{'='*80}")

    nlp = stanza.Pipeline('la', package=package, processors='tokenize,pos,lemma',
                          verbose=False, logging_level='ERROR')

    for sentence, description in test_cases:
        doc = nlp(sentence)
        words = [w.text for w in doc.sentences[0].words]
        tokens = [t.text for t in doc.sentences[0].tokens]

        print(f"\n📝 {sentence}")
        print(f"   {description}")
        print(f"   Tokens: {len(tokens)} → {tokens}")
        print(f"   Words:  {len(words)} → {words}")

        # Check for MWT
        sent = doc.sentences[0]
        if len(tokens) != len(words):
            print(f"   ⚠️  MWT: {len(tokens)} tokens → {len(words)} words")

            # Show which tokens are MWT
            for token in sent.tokens:
                if isinstance(token.id, tuple):
                    start, end = token.id
                    mwt_words = sent.words[start-1:end]
                    print(f"      '{token.text}' → {[w.text for w in mwt_words]}")

print("\n" + "="*80)
print("EXPECTED BEHAVIOR")
print("="*80)
print("""
SHOULD split (enclitics):
  - Populusque → Populus + que
  - videsne → vides + ne
  - terrave → terra + ve

SHOULD NOT split (case endings):
  - poetae → poetae (one word)
  - terra → terra (one word)
  - navis → navis (one word)
""")
