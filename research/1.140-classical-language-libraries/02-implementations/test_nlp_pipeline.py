#!/usr/bin/env python3
"""
Test CLTK's full NLP pipeline (Stanza-based) for Latin parsing

Goal: Determine if full NLP pipeline can:
1. Correctly identify POS (noun/verb/preposition/etc.)
2. Extract verb tense information
3. Provide declension/conjugation details
4. Parse real Latin sentences accurately

Use case: Word-by-word clicking exercise where user identifies:
- Declension number (1-6) for nouns
- Tense/mood/voice for verbs
"""

print("=" * 70)
print("CLTK NLP PIPELINE TEST")
print("Use Case: Full sentence parsing for reading-focused learning")
print("=" * 70)

# Test 1: Initialize NLP pipeline
print("\n" + "=" * 70)
print("TEST 1: NLP PIPELINE INITIALIZATION")
print("=" * 70)

try:
    from cltk import NLP

    print("\nInitializing CLTK NLP pipeline for Latin...")
    print("Note: This may download Stanza models (~100MB) on first run")
    print("Attempting automatic download with suppress_banner=True...")

    # Try to initialize with automatic model download
    cltk_nlp = NLP(language="lat", suppress_banner=True)

    print("✓ NLP pipeline initialized successfully!")

except Exception as e:
    print(f"✗ ERROR during initialization: {type(e).__name__}: {e}")
    print("\nThis likely means Stanza models need manual download.")
    print("Skipping full NLP pipeline tests for now.")
    print("\nTo manually download:")
    print("  from cltk.data.fetch import FetchCorpus")
    print("  corpus_downloader = FetchCorpus(language='lat')")
    print("  corpus_downloader.import_corpus('lat_models_cltk')")

    import sys
    sys.exit(0)

# Test 2: Parse simple sentence with POS tagging
print("\n" + "=" * 70)
print("TEST 2: POS TAGGING")
print("=" * 70)

test_sentence = "Puella in via ambulat"
print(f"\nSentence: '{test_sentence}'")
print("Expected POS: NOUN PREP NOUN VERB\n")

try:
    doc = cltk_nlp.analyze(text=test_sentence)

    print("Parsed tokens:")
    print("-" * 70)

    for i, word in enumerate(doc.words, 1):
        print(f"{i}. {word.string:12s} → POS: {word.upos:8s} | Lemma: {word.lemma:12s}")

    print("\n✓ POS tagging complete!")

except Exception as e:
    print(f"✗ ERROR during POS tagging: {type(e).__name__}: {e}")

# Test 3: Extract morphological features
print("\n" + "=" * 70)
print("TEST 3: MORPHOLOGICAL FEATURES")
print("=" * 70)

print("\nExtracting detailed morphological information...\n")

try:
    doc = cltk_nlp.analyze(text=test_sentence)

    print("Word-by-word morphological analysis:")
    print("-" * 70)

    for word in doc.words:
        print(f"\n{word.string}:")
        print(f"  POS:      {word.upos}")
        print(f"  Lemma:    {word.lemma}")
        print(f"  Features: {word.xpos}")  # Morphological features

        # Try to access detailed features if available
        if hasattr(word, 'feats'):
            print(f"  Details:  {word.feats}")

    print("\n✓ Morphological feature extraction complete!")

except Exception as e:
    print(f"✗ ERROR during morphological analysis: {type(e).__name__}: {e}")

# Test 4: Test on multiple sentences
print("\n" + "=" * 70)
print("TEST 4: MULTIPLE SENTENCE PARSING")
print("=" * 70)

test_sentences = [
    ("Puella rosam amat", "The girl loves the rose (nom-acc-verb)"),
    ("Marcus librum legit", "Marcus reads a book (nom-acc-verb)"),
    ("In silva ambulo", "I walk in the forest (prep-abl-verb)"),
    ("Poeta carmina scribit", "The poet writes poems (nom-acc-verb)"),
]

print("\nParsing diverse sentence structures...\n")

for sentence, description in test_sentences:
    print(f"Sentence: '{sentence}' ({description})")

    try:
        doc = cltk_nlp.analyze(text=sentence)

        # Compact output
        pos_sequence = " ".join([w.upos for w in doc.words])
        lemma_sequence = " ".join([w.lemma for w in doc.words])

        print(f"  POS:    {pos_sequence}")
        print(f"  Lemmas: {lemma_sequence}")
        print()

    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}\n")

# Test 5: Can we identify declension number?
print("\n" + "=" * 70)
print("TEST 5: DECLENSION NUMBER IDENTIFICATION")
print("=" * 70)

print("\nQuestion: Can NLP pipeline tell us declension number (1st/2nd/3rd/etc.)?")
print("-" * 70)

test_nouns = [
    ("puella", "1st declension", "puella, -ae (f)"),
    ("dominus", "2nd declension masculine", "dominus, -i (m)"),
    ("templum", "2nd declension neuter", "templum, -i (n)"),
    ("rex", "3rd declension", "rex, regis (m)"),
    ("manus", "4th declension", "manus, -us (f)"),
    ("res", "5th declension", "res, rei (f)"),
]

for noun, declension, full_form in test_nouns:
    sentence = f"{noun.capitalize()} est"  # Simple sentence: "X is"

    try:
        doc = cltk_nlp.analyze(text=sentence)
        word = doc.words[0]  # First word

        print(f"\n{noun:12s} ({declension})")
        print(f"  POS:      {word.upos}")
        print(f"  Lemma:    {word.lemma}")
        print(f"  XPOS:     {word.xpos}")

        # Check if morphological features contain declension info
        if hasattr(word, 'feats'):
            print(f"  Features: {word.feats}")

        # Check if there's any declension indicator
        has_declension_info = False
        if hasattr(word, 'feats') and word.feats:
            if any('Decl' in str(f) for f in str(word.feats)):
                has_declension_info = True
                print(f"  ✓ Contains declension information!")

        if not has_declension_info:
            print(f"  ✗ No declension number in features")

    except Exception as e:
        print(f"\n{noun}: ERROR - {type(e).__name__}: {e}")

# Test 6: Verb tense identification
print("\n" + "=" * 70)
print("TEST 6: VERB TENSE IDENTIFICATION")
print("=" * 70)

print("\nQuestion: Can NLP pipeline identify verb tense/mood/voice?")
print("-" * 70)

test_verbs = [
    ("amo", "1st person singular present", "I love"),
    ("amat", "3rd person singular present", "he/she loves"),
    ("amabat", "3rd person singular imperfect", "he/she was loving"),
    ("amavit", "3rd person singular perfect", "he/she loved"),
    ("amabit", "3rd person singular future", "he/she will love"),
]

for verb, description, translation in test_verbs:
    sentence = verb  # Just the verb alone

    try:
        doc = cltk_nlp.analyze(text=sentence)
        word = doc.words[0]

        print(f"\n{verb:12s} ({description})")
        print(f"  Translation: {translation}")
        print(f"  POS:         {word.upos}")
        print(f"  Lemma:       {word.lemma}")
        print(f"  XPOS:        {word.xpos}")

        if hasattr(word, 'feats') and word.feats:
            print(f"  Features:    {word.feats}")

            # Check for tense information
            tense_found = False
            if any('Tense' in str(f) for f in str(word.feats)):
                tense_found = True
                print(f"  ✓ Contains tense information!")

            if not tense_found:
                print(f"  ✗ No tense information in features")
        else:
            print(f"  Features:    None")
            print(f"  ✗ No morphological features available")

    except Exception as e:
        print(f"\n{verb}: ERROR - {type(e).__name__}: {e}")

# Summary
print("\n" + "=" * 70)
print("NLP PIPELINE ASSESSMENT")
print("=" * 70)

print("""
Key Questions for Reading Exercise:

1. Can identify POS (noun vs verb)?
   → Check TEST 2 results

2. Can identify declension number (1-6)?
   → Check TEST 5 results

3. Can identify verb tense?
   → Check TEST 6 results

4. Can identify case/number for nouns?
   → Check TEST 3 results (morphological features)

For the word-by-word clicking exercise to work, we need:
- User clicks 1-6 to identify declension → Need declension # from parser
- User clicks tense for verbs → Need tense from parser

If NLP pipeline provides this info → Use CLTK NLP
If not → Need to build custom parser using lemmatizer + decliner

Next steps:
1. Review test output above
2. Check if XPOS or feats contain needed information
3. Research Stanza's Latin model capabilities
4. Consider hybrid approach (NLP for POS, decliner for forms)
""")
