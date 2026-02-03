"""
Unit tests for LatinTrainer class.

Tests interpretation checking, vocabulary extraction, and scoring.
"""

import pytest
import sys
from pathlib import Path

# Add bin directory to path
PROJECT_ROOT = Path(__file__).parent.parent
BIN_DIR = PROJECT_ROOT / 'bin'
sys.path.insert(0, str(BIN_DIR))

# Import after path setup
import importlib.util
latin_train_path = BIN_DIR / "latin-train"
if not latin_train_path.exists():
    pytest.skip(f"latin-train not found at {latin_train_path}")

spec = importlib.util.spec_from_file_location("latin_train", latin_train_path)
if spec is None:
    pytest.skip("Could not load latin-train spec")

latin_train = importlib.util.module_from_spec(spec)


@pytest.mark.unit
@pytest.mark.trainer
class TestLatinTrainer:
    """Test LatinTrainer functionality."""

    def test_check_interpretation_correct_simple(self):
        """Test check_interpretation with correct simple answer."""
        # This will import the module
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        user_ans = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': 'nominative'
        }

        interpretation = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': 'nominative'
        }

        assert trainer.check_interpretation(user_ans, interpretation)

    def test_check_interpretation_wrong_case(self):
        """Test check_interpretation with wrong case."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        user_ans = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': 'accusative'
        }

        interpretation = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': 'nominative'
        }

        assert not trainer.check_interpretation(user_ans, interpretation)

    def test_check_interpretation_ambiguous_case_correct(self):
        """Test check_interpretation with ambiguous case (correct)."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        user_ans = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': 'genitive'
        }

        interpretation = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': ['genitive', 'dative']
        }

        assert trainer.check_interpretation(user_ans, interpretation)

    def test_check_interpretation_ambiguous_case_other_valid(self):
        """Test check_interpretation with ambiguous case (other valid option)."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        user_ans = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': 'dative'
        }

        interpretation = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': ['genitive', 'dative']
        }

        assert trainer.check_interpretation(user_ans, interpretation)

    def test_check_interpretation_ambiguous_case_wrong(self):
        """Test check_interpretation with ambiguous case (wrong)."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        user_ans = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': 'accusative'
        }

        interpretation = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': ['genitive', 'dative']
        }

        assert not trainer.check_interpretation(user_ans, interpretation)

    def test_check_interpretation_ambiguous_number(self):
        """Test check_interpretation with ambiguous number."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        user_ans = {
            'pos': 'NOUN',
            'declension': '3rd',
            'number': 'plural',
            'case': 'nominative'
        }

        interpretation = {
            'pos': 'NOUN',
            'declension': '3rd',
            'number': ['singular', 'plural'],
            'case': ['nominative', 'accusative', 'vocative']
        }

        assert trainer.check_interpretation(user_ans, interpretation)

    def test_check_interpretation_wrong_pos(self):
        """Test check_interpretation with wrong POS."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        user_ans = {
            'pos': 'VERB',
            'tense': 'present'
        }

        interpretation = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': 'nominative'
        }

        assert not trainer.check_interpretation(user_ans, interpretation)

    def test_check_interpretation_wrong_declension(self):
        """Test check_interpretation with wrong declension."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        user_ans = {
            'pos': 'NOUN',
            'declension': '2nd',
            'number': 'singular',
            'case': 'nominative'
        }

        interpretation = {
            'pos': 'NOUN',
            'declension': '1st',
            'number': 'singular',
            'case': 'nominative'
        }

        assert not trainer.check_interpretation(user_ans, interpretation)


@pytest.mark.unit
@pytest.mark.trainer
class TestVocabularyExtraction:
    """Test vocabulary extraction functionality."""

    def test_extract_vocabulary_single_word(self, sample_exercise_line):
        """Test extracting vocabulary from a single exercise line."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        sentences = [sample_exercise_line]
        vocab = trainer.extract_vocabulary(sentences)

        assert 'puella' in vocab
        assert vocab['puella']['genitive'] == 'puellae'
        assert vocab['puella']['gender'] == 'f'

    def test_extract_vocabulary_multiple_words(self, model_nouns_vocab):
        """Test extracting vocabulary from multiple words."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        # Create sentences with multiple words
        sentences = [
            {
                "sentence": "puella ventī",
                "words": [
                    {
                        "text": "puella",
                        "lemma": "puella",
                        "pos": "NOUN",
                        "declension": "1st",
                        "gender": "f",
                        "number": "singular",
                        "case": "nominative"
                    },
                    {
                        "text": "ventī",
                        "lemma": "ventus",
                        "pos": "NOUN",
                        "declension": "2nd",
                        "gender": "m",
                        "number": "singular",
                        "case": "genitive"
                    }
                ]
            },
            {
                "sentence": "puellae ventus",
                "words": [
                    {
                        "text": "puellae",
                        "lemma": "puella",
                        "pos": "NOUN",
                        "declension": "1st",
                        "gender": "f",
                        "number": "singular",
                        "case": ["genitive", "dative"]
                    },
                    {
                        "text": "ventus",
                        "lemma": "ventus",
                        "pos": "NOUN",
                        "declension": "2nd",
                        "gender": "m",
                        "number": "singular",
                        "case": "nominative"
                    }
                ]
            }
        ]

        vocab = trainer.extract_vocabulary(sentences)

        assert len(vocab) == 2
        assert 'puella' in vocab
        assert 'ventus' in vocab
        assert vocab['puella']['genitive'] == 'puellae'
        assert vocab['ventus']['genitive'] == 'ventī'

    def test_extract_vocabulary_no_duplicates(self):
        """Test that vocabulary extraction doesn't duplicate lemmas."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        # Same word in multiple sentences
        sentences = [
            {
                "sentence": "puella",
                "words": [{
                    "text": "puella",
                    "lemma": "puella",
                    "pos": "NOUN",
                    "declension": "1st",
                    "gender": "f",
                    "number": "singular",
                    "case": "nominative"
                }]
            },
            {
                "sentence": "puellae",
                "words": [{
                    "text": "puellae",
                    "lemma": "puella",
                    "pos": "NOUN",
                    "declension": "1st",
                    "gender": "f",
                    "number": "singular",
                    "case": ["genitive", "dative"]
                }]
            }
        ]

        vocab = trainer.extract_vocabulary(sentences)

        assert len(vocab) == 1
        assert 'puella' in vocab

    def test_extract_vocabulary_ambiguous_genitive(self):
        """Test extracting genitive from ambiguous case."""
        spec.loader.exec_module(latin_train)
        trainer = latin_train.LatinTrainer('test.jsonl', 'test_user')

        sentences = [
            {
                "sentence": "puella puellae",
                "words": [
                    {
                        "text": "puella",
                        "lemma": "puella",
                        "pos": "NOUN",
                        "declension": "1st",
                        "gender": "f",
                        "number": "singular",
                        "case": "nominative"
                    },
                    {
                        "text": "puellae",
                        "lemma": "puella",
                        "pos": "NOUN",
                        "declension": "1st",
                        "gender": "f",
                        "number": "singular",
                        "case": ["genitive", "dative"]
                    }
                ]
            }
        ]

        vocab = trainer.extract_vocabulary(sentences)

        # Should still extract genitive even though it's ambiguous
        assert 'puella' in vocab
        assert vocab['puella']['genitive'] == 'puellae'
