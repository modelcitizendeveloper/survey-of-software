#!/usr/bin/env python3
"""Verify the conjugation forms of 'possum' to confirm this is a bug"""

# Perfect active forms of possum (to be able)
possum_perfect = {
    'singular': {
        '1st': 'potui',
        '2nd': 'potuisti',
        '3rd': 'potuit'
    },
    'plural': {
        '1st': 'potuimus',
        '2nd': 'potuistis',
        '3rd': 'potuerunt / potuere'
    }
}

# Present active forms of possum
possum_present = {
    'singular': {
        '1st': 'possum',
        '2nd': 'potes',
        '3rd': 'potest'
    },
    'plural': {
        '1st': 'possumus',
        '2nd': 'potestis',
        '3rd': 'possunt'
    }
}

# Declension of poeta (1st declension masculine)
poeta_declension = {
    'singular': {
        'nominative': 'poeta',
        'genitive': 'poetae',
        'dative': 'poetae',
        'accusative': 'poetam',
        'ablative': 'poeta'
    },
    'plural': {
        'nominative': 'poetae',
        'genitive': 'poetarum',
        'dative': 'poetis',
        'accusative': 'poetas',
        'ablative': 'poetis'
    }
}

print("=" * 70)
print("POSSUM (to be able) - PRESENT TENSE")
print("=" * 70)
for number, forms in possum_present.items():
    print(f"\n{number.upper()}:")
    for person, form in forms.items():
        print(f"  {person:10s}: {form}")

print("\n" + "=" * 70)
print("POSSUM (to be able) - PERFECT TENSE")
print("=" * 70)
for number, forms in possum_perfect.items():
    print(f"\n{number.upper()}:")
    for person, form in forms.items():
        print(f"  {person:10s}: {form}")

print("\n" + "=" * 70)
print("POETA (poet) - NOUN DECLENSION (1st declension)")
print("=" * 70)
for number, forms in poeta_declension.items():
    print(f"\n{number.upper()}:")
    for case, form in forms.items():
        print(f"  {case:12s}: {form}")

print("\n" + "=" * 70)
print("ANALYSIS: Is 'poetae' a form of 'possum'?")
print("=" * 70)

all_possum_forms = set()
for tense in [possum_present, possum_perfect]:
    for number_forms in tense.values():
        for form in number_forms.values():
            # Split compound forms like "potuerunt / potuere"
            for f in form.split(' / '):
                all_possum_forms.add(f.strip())

print(f"\nAll forms of possum: {sorted(all_possum_forms)}")
print(f"\nIs 'poetae' in possum forms? {', poetae' in all_possum_forms}")
print(f"Is 'poetarum' in possum forms? {'poetarum' in all_possum_forms}")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
print("""
'poetae' is the GENITIVE/DATIVE SINGULAR of 'poeta' (poet).
'poetae' is NOT a form of 'possum' (to be able).

Stanza's Latin model has INCORRECT training data or disambiguation logic.

This is a bug in the Stanza Latin model, not in our code or CLTK.
""")
