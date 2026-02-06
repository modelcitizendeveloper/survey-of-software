#!/home/ivanadamin/spawn-solutions/research/1.140-classical-language-libraries/02-implementations/.venv/bin/python
"""
TDD: Known-Word Database Override System

Test-first approach:
1. Write tests showing what we want
2. Tests fail (no implementation yet)
3. Implement KnownWordDatabase class
4. Tests pass
5. Measure accuracy improvement
"""

import json
from pathlib import Path

# Test data: words we know are wrong in PROIEL
KNOWN_WORDS = {
    "nauta": {
        "lemma": "nauta",
        "declension": "1st",
        "gender": "masculine",
        "pos": "NOUN",
        "forms": {
            "nauta": {"case": "nominative", "number": "singular"},
            "nautae": {"case": "genitive", "number": "singular"},
            "nautae": {"case": "dative", "number": "singular"},
            "nautam": {"case": "accusative", "number": "singular"},
            "nauta": {"case": "ablative", "number": "singular"},
            "nautae": {"case": "nominative", "number": "plural"},
            "nautarum": {"case": "genitive", "number": "plural"},
            "nautis": {"case": "dative", "number": "plural"},
            "nautas": {"case": "accusative", "number": "plural"},
            "nautis": {"case": "ablative", "number": "plural"},
        }
    },
    "scriba": {
        "lemma": "scriba",
        "declension": "1st",
        "gender": "masculine",
        "pos": "NOUN",
        "forms": {
            "scriba": {"case": "nominative", "number": "singular"},
            "scribae": {"case": "genitive", "number": "singular"},
            "scribam": {"case": "accusative", "number": "singular"},
            "scribarum": {"case": "genitive", "number": "plural"},
        }
    },
    "pirata": {
        "lemma": "pirata",
        "declension": "1st",
        "gender": "masculine",
        "pos": "NOUN",
        "forms": {
            "pirata": {"case": "nominative", "number": "singular"},
            "piratae": {"case": "genitive", "number": "singular"},
            "piratam": {"case": "accusative", "number": "singular"},
            "piratarum": {"case": "genitive", "number": "plural"},
        }
    }
}


class KnownWordDatabase:
    """
    Override parser with known-correct word forms

    Strategy:
    1. Check if word form exists in known words
    2. If yes, return known lemma + POS
    3. If no, fall back to parser
    """

    def __init__(self, known_words_path=None):
        if known_words_path and Path(known_words_path).exists():
            with open(known_words_path, 'r') as f:
                self.known_words = json.load(f)
        else:
            self.known_words = KNOWN_WORDS

    def lookup(self, word_form):
        """
        Look up a word form in the known-word database

        Returns:
            dict with {lemma, pos, case, number} if found
            None if not found
        """
        word_lower = word_form.lower()

        # Search all known lemmas
        for lemma, word_data in self.known_words.items():
            if word_lower in word_data.get("forms", {}):
                form_info = word_data["forms"][word_lower]
                return {
                    "lemma": word_data["lemma"],
                    "pos": word_data["pos"],
                    "declension": word_data.get("declension"),
                    "case": form_info.get("case"),
                    "number": form_info.get("number"),
                    "source": "known_words"
                }

        return None

    def save(self, filepath):
        """Save known words to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.known_words, f, indent=2)


# ============================================================================
# TDD TESTS
# ============================================================================

def test_lookup_nautam():
    """nautam should be recognized as accusative of nauta"""
    db = KnownWordDatabase()
    result = db.lookup("nautam")

    assert result is not None, "nautam should be in database"
    assert result["lemma"] == "nauta", f"Expected lemma 'nauta', got '{result['lemma']}'"
    assert result["pos"] == "NOUN", f"Expected NOUN, got '{result['pos']}'"
    assert result["case"] == "accusative", f"Expected accusative, got '{result['case']}'"
    print("✓ test_lookup_nautam PASSED")


def test_lookup_scribam():
    """scribam should be recognized as accusative of scriba"""
    db = KnownWordDatabase()
    result = db.lookup("scribam")

    assert result is not None, "scribam should be in database"
    assert result["lemma"] == "scriba"
    assert result["pos"] == "NOUN"
    assert result["case"] == "accusative"
    print("✓ test_lookup_scribam PASSED")


def test_lookup_pirata():
    """pirata should be recognized as nominative of pirata"""
    db = KnownWordDatabase()
    result = db.lookup("pirata")

    assert result is not None
    assert result["lemma"] == "pirata"
    assert result["pos"] == "NOUN"
    assert result["case"] == "nominative"
    print("✓ test_lookup_pirata PASSED")


def test_lookup_unknown_word():
    """Unknown words should return None"""
    db = KnownWordDatabase()
    result = db.lookup("xyzabc")

    assert result is None, "Unknown word should return None"
    print("✓ test_lookup_unknown_word PASSED")


def test_save_and_load():
    """Test saving and loading known words"""
    db = KnownWordDatabase()
    test_file = "/tmp/test_known_words.json"

    db.save(test_file)
    db2 = KnownWordDatabase(test_file)

    # Should have same data
    result = db2.lookup("nautam")
    assert result is not None
    assert result["lemma"] == "nauta"
    print("✓ test_save_and_load PASSED")


# ============================================================================
# INTEGRATION TEST WITH PROIEL
# ============================================================================

def test_integration_with_proiel():
    """Test that known words override PROIEL errors"""
    import stanza

    nlp = stanza.Pipeline('la', package='proiel', processors='tokenize,pos,lemma',
                          verbose=False, logging_level='ERROR')
    db = KnownWordDatabase()

    # Test cases where PROIEL is wrong
    test_cases = [
        ("nautam", "nauta", "NOUN"),   # PROIEL says "navo" VERB
        ("scribam", "scriba", "NOUN"),  # PROIEL says "scribo" VERB
        ("piratam", "pirata", "NOUN"),  # PROIEL says "piro" VERB
    ]

    print("\n" + "="*70)
    print("INTEGRATION TEST: Known Words vs PROIEL")
    print("="*70)

    for word_form, expected_lemma, expected_pos in test_cases:
        # Get PROIEL parse
        doc = nlp(word_form)
        proiel_result = doc.sentences[0].words[0]

        # Get known-word override
        known_result = db.lookup(word_form)

        print(f"\n'{word_form}':")
        print(f"  PROIEL:  {proiel_result.lemma} ({proiel_result.upos})")

        if known_result:
            print(f"  KNOWN:   {known_result['lemma']} ({known_result['pos']}) ✓ OVERRIDE")
            assert known_result['lemma'] == expected_lemma
            assert known_result['pos'] == expected_pos
        else:
            print(f"  KNOWN:   Not found - would use PROIEL")


if __name__ == '__main__':
    print("="*70)
    print("TDD: KNOWN-WORD DATABASE TESTS")
    print("="*70)

    # Run unit tests
    print("\nUnit Tests:")
    print("-"*70)
    test_lookup_nautam()
    test_lookup_scribam()
    test_lookup_pirata()
    test_lookup_unknown_word()
    test_save_and_load()

    # Run integration test
    test_integration_with_proiel()

    print("\n" + "="*70)
    print("ALL TESTS PASSED ✓")
    print("="*70)

    print("""
Next steps:
1. Expand known_words to 100 common words
2. Integrate into latin-parse script
3. Measure accuracy on 20-word test corpus
4. Expected: 14/20 (70%) → 17/20 (85%)
""")
