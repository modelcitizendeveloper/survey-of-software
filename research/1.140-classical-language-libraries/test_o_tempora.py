#!/home/ivanadamin/spawn-solutions/research/1.140-classical-language-libraries/02-implementations/.venv/bin/python
"""
Test Case: Cicero's "O tempora, o mores!"

Famous quote from Cicero's First Oration Against Catiline
Translation: "Oh the times! Oh the customs!"

Let's see how our parser handles it.
"""

import stanza
from test_known_words_tdd import KnownWordDatabase

# Initialize parsers
nlp_proiel = stanza.Pipeline('la', package='proiel', processors='tokenize,pos,lemma',
                              verbose=False, logging_level='ERROR')
nlp_ittb = stanza.Pipeline('la', package='ittb', processors='tokenize,pos,lemma',
                            verbose=False, logging_level='ERROR')

# Known words DB
db = KnownWordDatabase()

# The famous quote (corrected spelling)
cicero_quote = "O tempora, o mores!"

print("="*80)
print("PARSING CICERO: 'O tempora, o mores!'")
print("="*80)

print("\nContext: First Oration Against Catiline (63 BC)")
print("Translation: 'Oh the times! Oh the customs!'")
print()

# Test with PROIEL
print("="*80)
print("PROIEL PARSER")
print("="*80)

doc = nlp_proiel(cicero_quote)
print(f"\nTokenized: {[w.text for w in doc.sentences[0].words]}")
print()

for word in doc.sentences[0].words:
    print(f"{word.text:12s} → {word.lemma:12s} ({word.upos:8s}) xpos: {word.xpos}")

# Test with ITTB for comparison
print("\n" + "="*80)
print("ITTB PARSER (for comparison)")
print("="*80)

doc = nlp_ittb(cicero_quote)
print(f"\nTokenized: {[w.text for w in doc.sentences[0].words]}")
print()

for word in doc.sentences[0].words:
    print(f"{word.text:12s} → {word.lemma:12s} ({word.upos:8s})")

# Check known-word DB
print("\n" + "="*80)
print("KNOWN-WORD DATABASE CHECK")
print("="*80)

words_to_check = ["tempora", "mores"]
for word in words_to_check:
    result = db.lookup(word)
    if result:
        print(f"✓ {word} → {result['lemma']} ({result['pos']}) [IN DATABASE]")
    else:
        print(f"✗ {word} → NOT in database")

# Expected correct parse
print("\n" + "="*80)
print("EXPECTED CORRECT PARSE")
print("="*80)

expected = [
    ("O", "o", "INTJ", "Interjection - exclamation"),
    ("tempora", "tempus", "NOUN", "Accusative plural of tempus (time)"),
    ("o", "o", "INTJ", "Interjection - exclamation"),
    ("mores", "mos", "NOUN", "Accusative plural of mos (custom/manner)"),
]

print()
for text, lemma, pos, note in expected:
    print(f"{text:12s} → {lemma:12s} ({pos:8s}) - {note}")

# Analysis
print("\n" + "="*80)
print("ANALYSIS")
print("="*80)

doc = nlp_proiel(cicero_quote)

errors = []
for word, (expected_text, expected_lemma, expected_pos, _) in zip(doc.sentences[0].words, expected):
    if word.text.lower() != expected_text.lower():
        continue  # Skip punctuation differences

    if word.lemma.lower() != expected_lemma.lower() or word.upos != expected_pos:
        errors.append({
            'word': word.text,
            'got_lemma': word.lemma,
            'got_pos': word.upos,
            'expected_lemma': expected_lemma,
            'expected_pos': expected_pos
        })

if errors:
    print(f"\n✗ Found {len(errors)} error(s):")
    for error in errors:
        print(f"  - {error['word']}: got {error['got_lemma']} ({error['got_pos']}), "
              f"expected {error['expected_lemma']} ({error['expected_pos']})")
else:
    print("\n✓ All words parsed correctly!")

print("\n" + "="*80)
print("HOW TO IMPROVE")
print("="*80)

print("""
To get this right, add to known_words.json:

{
  "tempus": {
    "lemma": "tempus",
    "declension": "3rd",
    "gender": "neuter",
    "pos": "NOUN",
    "forms": {
      "tempus": {"case": "nominative", "number": "singular"},
      "temporis": {"case": "genitive", "number": "singular"},
      "tempori": {"case": "dative", "number": "singular"},
      "tempus": {"case": "accusative", "number": "singular"},
      "tempore": {"case": "ablative", "number": "singular"},
      "tempora": {"case": "nominative", "number": "plural"},
      "tempora": {"case": "accusative", "number": "plural"},
      "temporum": {"case": "genitive", "number": "plural"},
      "temporibus": {"case": "dative", "number": "plural"}
    }
  },
  "mos": {
    "lemma": "mos",
    "declension": "3rd",
    "gender": "masculine",
    "pos": "NOUN",
    "forms": {
      "mos": {"case": "nominative", "number": "singular"},
      "moris": {"case": "genitive", "number": "singular"},
      "mori": {"case": "dative", "number": "singular"},
      "morem": {"case": "accusative", "number": "singular"},
      "more": {"case": "ablative", "number": "singular"},
      "mores": {"case": "nominative", "number": "plural"},
      "mores": {"case": "accusative", "number": "plural"},
      "morum": {"case": "genitive", "number": "plural"},
      "moribus": {"case": "dative", "number": "plural"}
    }
  }
}

These are VERY common words - should definitely be in the top 500.
""")
