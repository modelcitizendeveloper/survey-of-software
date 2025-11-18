#!/usr/bin/env python3
"""
XPOS Code Decoder for CLTK/Stanza Latin POS tags

Based on test_nlp_pipeline.py results, the XPOS field contains:
- Declension number (for nouns)
- Verb tense (for verbs)
- Case information
- Gender/person information

Format examples:
- Nouns:  A1|grn1|casA|gen2  (1st decl, nom/acc, feminine)
- Verbs:  J3|modA|tem1|gen6  (present tense, 3rd person)
"""

def decode_noun_xpos(xpos):
    """
    Decode XPOS for nouns

    Example: 'A1|grn1|casA|gen2' → 1st declension, nominative, feminine
    """
    parts = xpos.split('|')

    # First character indicates declension
    declension_map = {
        'A': '1st',  # puella
        'B': '2nd (neuter)',  # templum
        'C': '2nd/3rd',  # dominus OR rex (need more data)
        'D': '4th',  # manus
        'E': '5th',  # res
    }

    declension_letter = parts[0][0]
    declension = declension_map.get(declension_letter, 'unknown')

    # Case (casX)
    case_part = [p for p in parts if p.startswith('cas')]
    if case_part:
        case_code = case_part[0].replace('cas', '')
        case_map = {
            'A': 'nominative/accusative',  # Need to disambiguate
            'F': 'ablative',
            'G': 'genitive',  # Hypothesis
            'D': 'dative',    # Hypothesis
            'B': 'ablative',  # Alternative code?
        }
        case = case_map.get(case_code, f'case_{case_code}')
    else:
        case = 'unknown'

    # Gender (genX)
    gender_part = [p for p in parts if p.startswith('gen')]
    if gender_part:
        gender_code = gender_part[0].replace('gen', '')
        gender_map = {
            '1': 'masculine',
            '2': 'feminine',
            '3': 'neuter',
        }
        gender = gender_map.get(gender_code, f'gender_{gender_code}')
    else:
        gender = 'unknown'

    return {
        'declension': declension,
        'case': case,
        'gender': gender,
        'raw_xpos': xpos
    }


def decode_verb_xpos(xpos):
    """
    Decode XPOS for verbs

    Example: 'J3|modA|tem1|gen6' → present tense, 3rd person, indicative
    """
    parts = xpos.split('|')

    # Tense (temX)
    tense_part = [p for p in parts if p.startswith('tem')]
    if tense_part:
        tense_code = tense_part[0].replace('tem', '')
        tense_map = {
            '1': 'present',
            '2': 'imperfect',
            '3': 'future',
            '4': 'perfect',
            '5': 'pluperfect',  # Hypothesis
            '6': 'future perfect',  # Hypothesis
        }
        tense = tense_map.get(tense_code, f'tense_{tense_code}')
    else:
        tense = 'unknown'

    # Mood (modX)
    mood_part = [p for p in parts if p.startswith('mod')]
    if mood_part:
        mood_code = mood_part[0].replace('mod', '')
        mood_map = {
            'A': 'indicative',
            'B': 'subjunctive',  # Hypothesis
            'C': 'imperative',   # Hypothesis
            'D': 'infinitive',   # Hypothesis
        }
        mood = mood_map.get(mood_code, f'mood_{mood_code}')
    else:
        mood = 'unknown'

    # Person (genX for verbs means person!)
    person_part = [p for p in parts if p.startswith('gen')]
    if person_part:
        person_code = person_part[0].replace('gen', '')
        person_map = {
            '4': '1st person',
            '5': '2nd person',  # Hypothesis
            '6': '3rd person',
        }
        person = person_map.get(person_code, f'person_{person_code}')
    else:
        person = 'unknown'

    return {
        'tense': tense,
        'mood': mood,
        'person': person,
        'raw_xpos': xpos
    }


# Test the decoder
if __name__ == "__main__":
    print("=" * 70)
    print("XPOS DECODER TEST")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("NOUN EXAMPLES")
    print("=" * 70)

    noun_examples = [
        ("Puella", "A1|grn1|casA|gen2", "1st declension, nominative, feminine"),
        ("via", "A1|grn1|casF|gen2", "1st declension, ablative, feminine"),
        ("dominus", "C1|grn1|casA|gen1", "2nd declension, nominative, masculine"),
        ("templum", "B1|grn1|casA|gen3", "2nd declension, nominative, neuter"),
        ("rex", "C1|grn1|casA|gen1", "3rd declension, nominative, masculine"),
        ("manus", "D1|grn1|casA|gen2", "4th declension, nominative, feminine"),
        ("res", "E1|grn1|casA|gen2", "5th declension, nominative, feminine"),
    ]

    for word, xpos, expected in noun_examples:
        decoded = decode_noun_xpos(xpos)
        print(f"\n{word:12s} ({expected})")
        print(f"  XPOS: {xpos}")
        print(f"  → Declension: {decoded['declension']}")
        print(f"  → Case: {decoded['case']}")
        print(f"  → Gender: {decoded['gender']}")

    print("\n" + "=" * 70)
    print("VERB EXAMPLES")
    print("=" * 70)

    verb_examples = [
        ("amo", "N3|modA|tem1|gen4", "1st person singular present"),
        ("amat", "J3|modA|tem1|gen6", "3rd person singular present"),
        ("amabat", "J3|modA|tem2|gen6", "3rd person singular imperfect"),
        ("amavit", "J3|modA|tem4|gen6", "3rd person singular perfect"),
        ("amabit", "J3|modA|tem3|gen6", "3rd person singular future"),
    ]

    for word, xpos, expected in verb_examples:
        decoded = decode_verb_xpos(xpos)
        print(f"\n{word:12s} ({expected})")
        print(f"  XPOS: {xpos}")
        print(f"  → Tense: {decoded['tense']}")
        print(f"  → Mood: {decoded['mood']}")
        print(f"  → Person: {decoded['person']}")

    print("\n" + "=" * 70)
    print("KEY FINDINGS")
    print("=" * 70)

    print("""
For the word-by-word clicking exercise:

✓ CAN identify declension number!
  - A = 1st declension
  - B = 2nd declension (neuter)
  - C = 2nd/3rd declension (need to disambiguate)
  - D = 4th declension
  - E = 5th declension

✓ CAN identify verb tense!
  - tem1 = present
  - tem2 = imperfect
  - tem3 = future
  - tem4 = perfect

✓ CAN identify case (casX)
  - casA = nominative/accusative
  - casF = ablative
  - (Need to test other cases)

✓ CAN identify gender/person (genX)
  - For nouns: gen1=masc, gen2=fem, gen3=neut
  - For verbs: gen4=1st person, gen6=3rd person

Next steps:
1. Test more cases (genitive, dative, vocative)
2. Disambiguate 'C' code (2nd vs 3rd declension)
3. Test subjunctive, imperative moods
4. Build complete XPOS → human-readable decoder
""")
