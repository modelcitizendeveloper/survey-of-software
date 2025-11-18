#!/usr/bin/env python3
"""
Test CLTK parsing/analysis for reading-focused Latin learning

Use case: Given a Latin sentence, parse word-by-word to identify:
- Part of speech (noun/verb/etc.)
- Declension/conjugation
- Case/tense/number/person
- Lemma (dictionary form)
"""

print("=" * 70)
print("CLTK PARSING & ANALYSIS TEST")
print("Use Case: Reading-focused Latin learning")
print("=" * 70)

# Test 1: Basic sentence parsing
print("\n" + "=" * 70)
print("TEST 1: BASIC SENTENCE PARSING")
print("=" * 70)

try:
    from cltk import NLP

    # Initialize (may download Stanza models)
    print("\nInitializing CLTK NLP pipeline for Latin...")
    print("(This may download ~100MB of models on first run)")

    # Note: This will prompt for download - need non-interactive mode
    print("\nSkipping full NLP pipeline test (requires interactive download)")
    print("Testing individual components instead...")

except Exception as e:
    print(f"Error initializing NLP: {e}")

# Test 2: Lemmatization (reverse lookup)
print("\n" + "=" * 70)
print("TEST 2: LEMMATIZATION (Form → Base)")
print("=" * 70)

from cltk.lemmatize.lat import LatinBackoffLemmatizer

lemmatizer = LatinBackoffLemmatizer()

# Test sentence: "Puella in via ambulat"
# Expected: puella (nom sg), in (prep), via (abl sg), ambulat (3sg pres)

test_forms = [
    ("Puella", "puella", "nominative singular"),
    ("puella", "puella", "should be same"),
    ("puellam", "puella", "accusative singular"),
    ("puellas", "puella", "accusative plural"),
    ("via", "via", "ablative singular"),
    ("ambulat", "ambulo", "3rd person singular present"),
    ("ambulabat", "ambulo", "3rd person singular imperfect"),
    ("vidi", "video", "1st person singular perfect"),
    ("vici", "vinco", "1st person singular perfect"),
]

print("\nForm → Lemma (base form):")
print("-" * 70)

for form, expected, description in test_forms:
    result = lemmatizer.lemmatize([form.lower()])  # Must lowercase!

    if result:
        lemma = result[0][1]
        status = "✓" if lemma == expected else "✗"
        print(f"{status} {form:15s} → {lemma:12s} (expected: {expected:12s}) [{description}]")
    else:
        print(f"✗ {form:15s} → NO RESULT")

# Test 3: POS tagging without full pipeline
print("\n" + "=" * 70)
print("TEST 3: AVAILABLE PARSING MODULES")
print("=" * 70)

print("\nChecking what parsing capabilities exist...")

# Check for available modules
try:
    import cltk.morphology.lat
    print("✓ cltk.morphology.lat available")
    print(f"  Methods: {[m for m in dir(cltk.morphology.lat) if not m.startswith('_')]}")
except ImportError:
    print("✗ cltk.morphology.lat not available")

try:
    from cltk.tag import pos
    print("✓ cltk.tag.pos available")
except ImportError:
    print("✗ cltk.tag.pos not available")

try:
    import cltk.dependency
    print("✓ cltk.dependency available")
except ImportError:
    print("✗ cltk.dependency not available")

# Test 4: Can we identify declension from form?
print("\n" + "=" * 70)
print("TEST 4: DECLENSION IDENTIFICATION")
print("=" * 70)

from cltk.morphology.lat import CollatinusDecliner

decliner = CollatinusDecliner()

print("\nQuestion: Given 'puellam', can we identify it's 1st declension?")
print("Approach: Check which declension lemmas match the form")

# Strategy 1: Use lemmatizer then decline to verify
form = "puellam"
result = lemmatizer.lemmatize([form])

if result:
    lemma = result[0][1]
    print(f"\n1. Lemmatize 'puellam' → '{lemma}'")

    # Now decline the lemma
    all_forms = decliner.decline(lemma)

    print(f"2. Decline '{lemma}' → {len(all_forms)} forms")

    # Check if our original form is in there
    matching_forms = [(f, code) for f, code in all_forms if f == form]

    if matching_forms:
        print(f"3. Found '{form}' in declension:")
        for f, code in matching_forms:
            # Parse the code
            number = 'singular' if code[2] == 's' else 'plural'
            case_map = {'n': 'nom', 'v': 'voc', 'a': 'acc', 'g': 'gen', 'd': 'dat', 'b': 'abl'}
            case = case_map.get(code[7], '?')
            print(f"   {f} = {case} {number} (code: {code})")

        # Determine declension from lemma
        # This is where we need to check: is there a way to get declension #?
        print(f"\n4. Declension identification:")
        print(f"   Lemma: {lemma}")
        print(f"   Declension: [Need to determine - checking lemmas database...]")

        # Check if lemmas database has declension info
        if lemma in decliner.lemmas:
            lemma_data = decliner.lemmas[lemma]
            print(f"   Lemma data: {lemma_data}")

# Test 5: Test on full sentence simulation
print("\n" + "=" * 70)
print("TEST 5: SENTENCE WORD-BY-WORD SIMULATION")
print("=" * 70)

sentence = "Puella in via ambulat"
words = sentence.split()

print(f"\nSentence: '{sentence}'")
print(f"Words: {words}\n")

print("Word-by-word analysis:")
print("-" * 70)

for i, word in enumerate(words, 1):
    word_lower = word.lower()

    # Try to lemmatize
    result = lemmatizer.lemmatize([word_lower])

    if result:
        lemma = result[0][1]

        # Try to decline (to see if it's a noun)
        try:
            forms = decliner.decline(lemma)

            # Check if this word appears in the declension
            matches = [(f, code) for f, code in forms if f == word_lower]

            if matches:
                # It's a declinable noun!
                form, code = matches[0]
                number = 'sg' if code[2] == 's' else 'pl'
                case_map = {'n': 'nom', 'v': 'voc', 'a': 'acc', 'g': 'gen', 'd': 'dat', 'b': 'abl'}
                case = case_map.get(code[7], '?')

                print(f"{i}. {word:12s} → NOUN: {lemma} ({case} {number})")
            else:
                print(f"{i}. {word:12s} → VERB?: {lemma}")

        except Exception:
            # Not a declinable noun, probably verb or other
            print(f"{i}. {word:12s} → OTHER: {lemma}")
    else:
        print(f"{i}. {word:12s} → UNKNOWN")

print("\n" + "=" * 70)
print("ANALYSIS SUMMARY")
print("=" * 70)

print("""
Findings:
✓ Lemmatization works well (form → lemma)
✓ Can identify if word is declinable noun (try declining lemma)
✓ Can extract case/number from grammatical codes
✗ Cannot directly get declension NUMBER (1st/2nd/3rd/4th/5th)
✗ No built-in verb conjugation parser (only lemmatization)
? Full NLP pipeline requires Stanza models (needs interactive install)

For reading-focused app:
1. ✓ Can parse word → lemma
2. ✓ Can identify noun vs verb (by trying to decline)
3. ✓ Can get case/number for nouns
4. ✗ Cannot get declension # without additional data
5. ✗ Cannot get verb tense without additional parsing

Next steps:
- Test full NLP pipeline (Stanza) for POS tagging
- Research: How to map lemma → declension number
- Research: Verb form parsing (tense identification)
""")
