#!/home/ivanadamin/spawn-solutions/research/1.140-classical-language-libraries/02-implementations/.venv/bin/python
"""
TDD Test Suite for Perseus Package Multi-Word Token (MWT) Issues

Test-Driven Development approach:
1. Write failing tests that show current MWT problems
2. Implement fix to merge split tokens
3. Verify tests pass
4. Validate accuracy on full test corpus
"""

import stanza

# Make pytest optional for initial analysis
try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False
    print("Warning: pytest not installed, skipping test execution")

# Initialize Perseus pipeline
nlp = stanza.Pipeline('la', package='perseus', processors='tokenize,pos,lemma',
                      verbose=False, logging_level='ERROR')


class TestPerseusBasicParsing:
    """Test that Perseus correctly parses basic Latin without MWT issues"""

    def test_poetae_not_split(self):
        """poetae should be ONE word, not split into poeta + e"""
        doc = nlp("poetae")
        words = doc.sentences[0].words

        assert len(words) == 1, f"Expected 1 word, got {len(words)}: {[w.text for w in words]}"
        assert words[0].text == "poetae", f"Expected 'poetae', got '{words[0].text}'"
        assert words[0].lemma.lower() == "poeta", f"Expected lemma 'poeta', got '{words[0].lemma}'"
        assert words[0].upos == "NOUN", f"Expected NOUN, got {words[0].upos}"

    def test_puella_rosam_poetae_dat(self):
        """Full sentence should have 4 words, not more"""
        doc = nlp("Puella rosam poetae dat")
        words = doc.sentences[0].words

        expected_words = ["Puella", "rosam", "poetae", "dat"]
        actual_words = [w.text for w in words]

        assert len(words) == 4, f"Expected 4 words, got {len(words)}: {actual_words}"
        assert actual_words == expected_words, f"Word split mismatch: {actual_words}"

    def test_nautae_not_split(self):
        """nautae should be ONE word"""
        doc = nlp("nautae domus")
        words = doc.sentences[0].words

        assert words[0].text == "nautae", f"Expected 'nautae', got '{words[0].text}'"
        assert len(words) == 2, f"Expected 2 words, got {len(words)}: {[w.text for w in words]}"

    def test_agricolae_not_split(self):
        """agricolae should be ONE word"""
        doc = nlp("agricolae terra")
        words = doc.sentences[0].words

        assert words[0].text == "agricolae", f"Expected 'agricolae', got '{words[0].text}'"
        assert len(words) == 2, f"Expected 2 words, got {len(words)}: {[w.text for w in words]}"

    def test_terra_not_split(self):
        """terra should be ONE word, not terr + a"""
        doc = nlp("terra")
        words = doc.sentences[0].words

        assert len(words) == 1, f"Expected 1 word, got {len(words)}: {[w.text for w in words]}"
        assert words[0].text == "terra", f"Expected 'terra', got '{words[0].text}'"

    def test_navis_not_split(self):
        """navis should be ONE word, not navi + s"""
        doc = nlp("navis")
        words = doc.sentences[0].words

        assert len(words) == 1, f"Expected 1 word, got {len(words)}: {[w.text for w in words]}"
        assert words[0].text == "navis", f"Expected 'navis', got '{words[0].text}'"


class TestPerseusAccuracy:
    """Test that Perseus achieves expected accuracy on key forms"""

    def test_poeta_all_forms(self):
        """All forms of poeta should parse correctly"""
        test_cases = [
            ("poeta scribit", "poeta", "NOUN"),
            ("poetae domus", "poeta", "NOUN"),
            ("poetam video", "poeta", "NOUN"),
            ("poetarum carmina", "poeta", "NOUN"),
        ]

        for sentence, expected_lemma, expected_pos in test_cases:
            doc = nlp(sentence)
            first_word = doc.sentences[0].words[0]

            assert first_word.lemma.lower() == expected_lemma, \
                f"{sentence}: Expected lemma '{expected_lemma}', got '{first_word.lemma}'"
            assert first_word.upos == expected_pos, \
                f"{sentence}: Expected {expected_pos}, got {first_word.upos}"

    def test_nauta_all_forms(self):
        """All forms of nauta should parse correctly"""
        test_cases = [
            ("nauta navigat", "nauta", "NOUN"),
            ("nautae domus", "nauta", "NOUN"),
            ("nautam video", "nauta", "NOUN"),
            ("nautarum naves", "nauta", "NOUN"),
        ]

        for sentence, expected_lemma, expected_pos in test_cases:
            doc = nlp(sentence)
            first_word = doc.sentences[0].words[0]

            assert first_word.lemma.lower() == expected_lemma, \
                f"{sentence}: Expected lemma '{expected_lemma}', got '{first_word.lemma}'"
            assert first_word.upos == expected_pos, \
                f"{sentence}: Expected {expected_pos}, got {first_word.upos}"

    def test_agricola_all_forms(self):
        """All forms of agricola should parse correctly"""
        test_cases = [
            ("agricola laborat", "agricola", "NOUN"),
            ("agricolae terra", "agricola", "NOUN"),
            ("agricolam video", "agricola", "NOUN"),
            ("agricolarum agri", "agricola", "NOUN"),
        ]

        for sentence, expected_lemma, expected_pos in test_cases:
            doc = nlp(sentence)
            first_word = doc.sentences[0].words[0]

            assert first_word.lemma.lower() == expected_lemma, \
                f"{sentence}: Expected lemma '{expected_lemma}', got '{first_word.lemma}'"
            assert first_word.upos == expected_pos, \
                f"{sentence}: Expected {expected_pos}, got {first_word.upos}"


class TestMWTDetection:
    """Test that we can detect when MWT splitting has occurred"""

    def test_detect_mwt_in_doc(self):
        """Identify if a document contains MWT splits"""
        doc = nlp("poetae navis terra")

        # Check if any sentence has MWT
        for sent in doc.sentences:
            # In Stanza, MWT is when a token has multiple words
            # token.id is a tuple (start, end) for MWT
            mwt_count = sum(1 for token in sent.tokens if isinstance(token.id, tuple))

        print(f"\nMWT tokens found: {mwt_count}")
        print(f"Total tokens: {len(doc.sentences[0].tokens)}")
        print(f"Total words: {len(doc.sentences[0].words)}")

        # If there's MWT, tokens < words
        if len(doc.sentences[0].words) > len(doc.sentences[0].tokens):
            print("MWT detected: More words than tokens")
            for token in doc.sentences[0].tokens:
                if isinstance(token.id, tuple):
                    print(f"  MWT: {token.text} → {token.id}")


def analyze_mwt_patterns():
    """Analyze MWT patterns to understand the issue"""
    print("\n" + "="*80)
    print("MWT PATTERN ANALYSIS")
    print("="*80)

    test_words = [
        "poetae",
        "terra",
        "navis",
        "agricolae",
        "nautae",
        "rosam",
        "carmina",
        "puella"
    ]

    for word in test_words:
        doc = nlp(word)
        sent = doc.sentences[0]

        print(f"\n'{word}':")
        print(f"  Tokens: {len(sent.tokens)} → {[t.text for t in sent.tokens]}")
        print(f"  Words:  {len(sent.words)} → {[w.text for w in sent.words]}")

        # Check for MWT (multi-word tokens have tuple IDs like (1, 2))
        for i, token in enumerate(sent.tokens):
            if isinstance(token.id, tuple):
                start, end = token.id
                words_in_mwt = sent.words[start-1:end]
                print(f"  ⚠ MWT DETECTED: '{token.text}' → {[w.text for w in words_in_mwt]}")


if __name__ == '__main__':
    print("Running TDD tests for Perseus MWT issues...")
    print("Expected: Most tests will FAIL initially")
    print("Goal: Fix MWT issues until all tests pass")
    print()

    # First, analyze the patterns
    analyze_mwt_patterns()

    # Then run the tests
    if HAS_PYTEST:
        print("\n" + "="*80)
        print("RUNNING TESTS")
        print("="*80)
        pytest.main([__file__, '-v'])
    else:
        print("\n" + "="*80)
        print("pytest not installed - install with: uv pip install pytest")
        print("="*80)
