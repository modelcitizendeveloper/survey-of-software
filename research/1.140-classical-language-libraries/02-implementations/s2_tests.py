#!/usr/bin/env python3
"""
S2 Comprehensive Discovery - CLTK Deep Testing
Run all tests for research 1.140 S2
"""

import time
from cltk.morphology.lat import CollatinusDecliner
from cltk.lemmatize.lat import LatinBackoffLemmatizer

def test_api_parameters():
    """Test 1: API parameter exploration"""
    print("=" * 70)
    print("TEST 1: API PARAMETERS")
    print("=" * 70)

    decliner = CollatinusDecliner()

    # Test flatten parameter
    print("\n--- Testing flatten parameter ---")
    forms_default = decliner.decline("puella")
    forms_flat = decliner.decline("puella", flatten=True)

    print(f"flatten=False (default):")
    print(f"  Type: {type(forms_default)}")
    print(f"  Length: {len(forms_default)}")
    print(f"  First 2: {forms_default[:2]}")

    print(f"\nflatten=True:")
    print(f"  Type: {type(forms_flat)}")
    if isinstance(forms_flat, list):
        print(f"  Length: {len(forms_flat)}")
        print(f"  First 2: {forms_flat[:2] if len(forms_flat) >= 2 else forms_flat}")
    else:
        print(f"  Value: {forms_flat}")

    # Test collatinus_dict parameter
    print("\n--- Testing collatinus_dict parameter ---")
    forms_standard = decliner.decline("puella", collatinus_dict=False)
    forms_collatinus = decliner.decline("puella", collatinus_dict=True)

    print(f"collatinus_dict=False:")
    print(f"  First 2: {forms_standard[:2]}")

    print(f"collatinus_dict=True:")
    if isinstance(forms_collatinus, dict):
        print(f"  Type: dict")
        print(f"  Keys: {list(forms_collatinus.keys())[:5]}")
        print(f"  Sample: {list(forms_collatinus.items())[:2]}")
    else:
        print(f"  First 2: {forms_collatinus[:2]}")

    # Test lemmas attribute
    print("\n--- Testing lemmas attribute ---")
    print(f"decliner.lemmas type: {type(decliner.lemmas)}")
    if hasattr(decliner.lemmas, '__len__'):
        print(f"Number of lemmas: {len(decliner.lemmas)}")
    print(f"Lemmas attributes: {[a for a in dir(decliner.lemmas) if not a.startswith('_')][:10]}")


def test_grammatical_codes():
    """Test 2: Decode grammatical code format"""
    print("\n" + "=" * 70)
    print("TEST 2: GRAMMATICAL CODE ANALYSIS")
    print("=" * 70)

    decliner = CollatinusDecliner()

    # Test different genders
    print("\nComparing codes across genders:")

    masculine = decliner.decline("dominus")  # 2nd masc
    feminine = decliner.decline("puella")     # 1st fem
    neuter = decliner.decline("templum")      # 2nd neut

    print("\nMasculine (dominus) codes:")
    for form, code in masculine[:6]:
        print(f"  {form:12s} {code}")

    print("\nFeminine (puella) codes:")
    for form, code in feminine[:6]:
        print(f"  {form:12s} {code}")

    print("\nNeuter (templum) codes:")
    for form, code in neuter[:6]:
        print(f"  {form:12s} {code}")

    # Analyze pattern
    print("\n--- Code Pattern Analysis ---")
    all_codes = [code for _, code in masculine + feminine + neuter]
    unique_codes = set(all_codes)
    print(f"Total unique codes: {len(unique_codes)}")
    print(f"Sample codes: {list(unique_codes)[:5]}")


def test_performance():
    """Test 3: Performance benchmarking"""
    print("\n" + "=" * 70)
    print("TEST 3: PERFORMANCE BENCHMARKING")
    print("=" * 70)

    decliner = CollatinusDecliner()
    lemmatizer = LatinBackoffLemmatizer()

    test_words = ["puella", "dominus", "templum", "rex", "manus", "res"]

    # Benchmark 1: Single declension
    print("\n--- Single Declension ---")
    decliner.decline("puella")  # Warm-up

    start = time.perf_counter()
    forms = decliner.decline("puella")
    elapsed = time.perf_counter() - start

    print(f"Time: {elapsed*1000:.2f} ms")
    print(f"Forms: {len(forms)}")

    # Benchmark 2: Batch of 12
    print("\n--- Batch Declension (12 words) ---")
    batch_12 = test_words * 2

    start = time.perf_counter()
    for word in batch_12:
        forms = decliner.decline(word)
    elapsed = time.perf_counter() - start

    print(f"Total: {elapsed*1000:.2f} ms")
    print(f"Average: {elapsed*1000/len(batch_12):.2f} ms/word")

    # Benchmark 3: Batch of 100
    print("\n--- Batch Declension (100 words) ---")
    batch_100 = test_words * 17

    start = time.perf_counter()
    for word in batch_100:
        forms = decliner.decline(word)
    elapsed = time.perf_counter() - start

    print(f"Total: {elapsed*1000:.2f} ms")
    print(f"Average: {elapsed*1000/len(batch_100):.2f} ms/word")
    print(f"Throughput: {len(batch_100)/elapsed:.0f} words/second")

    # Benchmark 4: Initialization
    print("\n--- Initialization Time ---")
    start = time.perf_counter()
    new_decliner = CollatinusDecliner()
    init_time = time.perf_counter() - start

    print(f"Time: {init_time*1000:.2f} ms")

    # Benchmark 5: Lemmatization
    print("\n--- Lemmatization (80 words) ---")
    verb_forms = ['amo', 'amas', 'amat', 'amabam', 'amavi', 'veni', 'vidi', 'vici']
    batch_80 = verb_forms * 10

    start = time.perf_counter()
    for form in batch_80:
        lemma = lemmatizer.lemmatize([form])
    elapsed = time.perf_counter() - start

    print(f"Total: {elapsed*1000:.2f} ms")
    print(f"Average: {elapsed*1000/len(batch_80):.2f} ms/word")


def test_edge_cases():
    """Test 4: Edge cases and error handling"""
    print("\n" + "=" * 70)
    print("TEST 4: EDGE CASES & ERROR HANDLING")
    print("=" * 70)

    decliner = CollatinusDecliner()
    lemmatizer = LatinBackoffLemmatizer()

    # Test unknown words
    print("\n--- Unknown Words ---")
    unknown = ["foobar", "computer", "pizza"]
    for word in unknown:
        try:
            forms = decliner.decline(word)
            print(f"{word:15s} → {len(forms)} forms")
            if forms:
                print(f"  Sample: {forms[0]}")
        except Exception as e:
            print(f"{word:15s} → ERROR: {type(e).__name__}")

    # Test misspelled/case variations
    print("\n--- Case Sensitivity ---")
    variations = ["puella", "Puella", "PUELLA", "puella ", " puella"]
    for word in variations:
        try:
            forms = decliner.decline(word)
            print(f"'{word:10s}' → {len(forms)} forms")
        except Exception as e:
            print(f"'{word:10s}' → ERROR: {type(e).__name__}")

    # Test invalid input
    print("\n--- Invalid Input ---")
    invalid = ["", " ", "123", "puella123", "puel-la"]
    for word in invalid:
        try:
            forms = decliner.decline(word)
            print(f"'{word:12s}' → {len(forms)} forms")
        except Exception as e:
            print(f"'{word:12s}' → ERROR: {type(e).__name__}")

    # Test lemmatization edge cases
    print("\n--- Lemmatization Edge Cases ---")
    edge_cases = ["foobar", "sum", "est", "AMAT", ""]
    for word in edge_cases:
        try:
            lemma = lemmatizer.lemmatize([word]) if word else []
            result = lemma[0][1] if lemma else "NO RESULT"
            print(f"'{word:10s}' → {result}")
        except Exception as e:
            print(f"'{word:10s}' → ERROR: {type(e).__name__}")


def test_coverage():
    """Test 5: Coverage of irregular/special cases"""
    print("\n" + "=" * 70)
    print("TEST 5: COVERAGE TESTING")
    print("=" * 70)

    decliner = CollatinusDecliner()

    # Test irregular nouns
    print("\n--- Irregular/Special Nouns ---")
    irregular = ["vis", "bos", "domus", "os", "corpus"]
    for noun in irregular:
        try:
            forms = decliner.decline(noun)
            print(f"\n{noun}: {len(forms)} forms")
            for form, code in forms[:4]:
                print(f"  {code} {form}")
        except Exception as e:
            print(f"{noun}: ERROR - {e}")

    # Test Greek loanwords
    print("\n--- Greek Loanwords ---")
    greek = ["basis", "crisis", "poesis"]
    for word in greek:
        forms = decliner.decline(word)
        print(f"{word:12s} → {len(forms)} forms")
        if forms:
            print(f"  Sample: {forms[0]}")


if __name__ == "__main__":
    print("CLTK S2 COMPREHENSIVE TESTING")
    print("=" * 70)
    print()

    test_api_parameters()
    test_grammatical_codes()
    test_performance()
    test_edge_cases()
    test_coverage()

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETE")
    print("=" * 70)
