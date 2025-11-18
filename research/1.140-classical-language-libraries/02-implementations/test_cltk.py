#!/usr/bin/env python3
"""
Quick test script for CLTK (Classical Language Toolkit)

Usage:
    cd ~/spawn-solutions/research/1.140-classical-language-libraries/02-implementations
    uv venv
    source .venv/bin/activate
    uv pip install cltk
    python test_cltk.py
"""

from cltk.morphology.lat import CollatinusDecliner


def test_declension(decliner, word, declension_num, description):
    """Test declension of a Latin noun."""
    print("=" * 70)
    print(f"{description}")
    print("=" * 70)

    try:
        # CLTK v1 API: decline(lemma, flatten=False, collatinus_dict=False)
        # Returns list of tuples: [(form, grammatical_info), ...]
        forms = decliner.decline(word)

        if isinstance(forms, list):
            for form, grammar in forms:
                print(f"{grammar:30s} {form}")
        elif isinstance(forms, dict):
            for case_label, form in forms.items():
                print(f"{case_label:30s} {form}")
        else:
            print(f"Unexpected output type: {type(forms)}")
            print(forms)

        print(f"\nTotal forms: {len(forms)}")
        return True

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run CLTK tests."""
    print("\n" + "=" * 70)
    print("CLTK (Classical Language Toolkit) - Latin Declension Test")
    print("=" * 70)

    # Initialize decliner
    try:
        decliner = CollatinusDecliner()
        print("✓ CollatinusDecliner initialized successfully\n")
    except Exception as e:
        print(f"✗ Failed to initialize CollatinusDecliner: {e}")
        return

    # Test each declension
    test_cases = [
        ("puella", 1, "1st Declension: puella, puellae (f) - girl"),
        ("dominus", 2, "2nd Declension (masculine): dominus, domini (m) - lord"),
        ("templum", 2, "2nd Declension (neuter): templum, templi (n) - temple"),
        ("rex", 3, "3rd Declension: rex, regis (m) - king"),
        ("manus", 4, "4th Declension: manus, manus (f) - hand"),
        ("res", 5, "5th Declension: res, rei (f) - thing"),
    ]

    results = []
    for word, decl_num, description in test_cases:
        success = test_declension(decliner, word, decl_num, description)
        results.append((description, success))
        print()

    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for description, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {description}")

    # Check for verb conjugation
    print("\n" + "=" * 70)
    print("VERB CONJUGATION TEST")
    print("=" * 70)

    try:
        # Try different possible conjugation classes
        from cltk.morphology.lat import CollatinusConjugator
        conjugator = CollatinusConjugator()
        print("✓ CollatinusConjugator found!")

        # Test conjugation
        print("\n1st Conjugation: amo, amare - to love")
        print("-" * 70)
        forms = conjugator.conjugate("amo")
        print(forms)

    except ImportError:
        print("✗ No CollatinusConjugator found in CLTK")
        print("  (Verb conjugation may not be available)")

    except AttributeError as e:
        print(f"✗ Conjugation method not found: {e}")

    except Exception as e:
        print(f"✗ Error testing conjugation: {type(e).__name__}: {e}")

    # API exploration
    print("\n" + "=" * 70)
    print("API EXPLORATION")
    print("=" * 70)

    print("\nCollatinusDecliner available methods:")
    methods = [m for m in dir(decliner) if not m.startswith('_')]
    for method in methods:
        print(f"  - {method}")

    print("\nCollatinusDecliner type:")
    print(f"  {type(decliner)}")

    # Check decline method signature
    import inspect

    print("\ndecline() signature:")
    try:
        sig = inspect.signature(decliner.decline)
        print(f"  {sig}")
    except Exception as e:
        print(f"  Could not get signature: {e}")


if __name__ == "__main__":
    main()
