"""
Pytest fixtures and configuration for Latin training tests.
"""

import json
import pytest
import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'exercises'))


@pytest.fixture
def declension_templates():
    """Load declension templates for testing."""
    templates_path = PROJECT_ROOT / 'exercises' / 'declension_templates.json'
    with open(templates_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def sample_vocabulary():
    """Sample vocabulary data for testing."""
    return {
        "series_name": "test-series",
        "series_title": "Test Series",
        "series_description": "Test description",
        "level": "beginner",
        "words": [
            {
                "lemma": "puella",
                "declension": "1st",
                "gender": "f",
                "meaning": "girl",
                "irregular": False
            },
            {
                "lemma": "ventus",
                "declension": "2nd",
                "gender": "m",
                "meaning": "wind",
                "irregular": False
            },
            {
                "lemma": "vir",
                "declension": "2nd",
                "gender": "m",
                "meaning": "man",
                "irregular": True,
                "genitive_singular": "virī",
                "forms_override": {
                    "singular": {
                        "nominative": "vir",
                        "vocative": "vir"
                    }
                }
            },
            {
                "lemma": "homo",
                "declension": "3rd",
                "gender": "m",
                "meaning": "human",
                "irregular": False,
                "genitive_singular": "hominis"
            },
            {
                "lemma": "nomen",
                "declension": "3rd",
                "gender": "n",
                "meaning": "name",
                "irregular": True,
                "genitive_singular": "nominis",
                "neuter": True
            },
            {
                "lemma": "manus",
                "declension": "4th",
                "gender": "f",
                "meaning": "hand",
                "irregular": True,
                "genitive_singular": "manūs"
            },
            {
                "lemma": "dies",
                "declension": "5th",
                "gender": "m/f",
                "meaning": "day",
                "irregular": True,
                "genitive_singular": "diēī"
            }
        ]
    }


@pytest.fixture
def sample_exercise_line():
    """Sample exercise line in JSONL format."""
    return {
        "sentence": "puella puellae puellae puellam puellā puella",
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
            },
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
                "text": "puellam",
                "lemma": "puella",
                "pos": "NOUN",
                "declension": "1st",
                "gender": "f",
                "number": "singular",
                "case": "accusative"
            },
            {
                "text": "puellā",
                "lemma": "puella",
                "pos": "NOUN",
                "declension": "1st",
                "gender": "f",
                "number": "singular",
                "case": "ablative"
            },
            {
                "text": "puella",
                "lemma": "puella",
                "pos": "NOUN",
                "declension": "1st",
                "gender": "f",
                "number": "singular",
                "case": "vocative"
            }
        ]
    }


@pytest.fixture
def model_nouns_vocab():
    """Vocabulary for model nouns series."""
    return {
        'puella': {'genitive': 'puellae', 'gender': 'f'},
        'ventus': {'genitive': 'ventī', 'gender': 'm'},
        'miles': {'genitive': 'militis', 'gender': 'm'},
        'usus': {'genitive': 'usūs', 'gender': 'm'},
        'res': {'genitive': 'reī', 'gender': 'f'}
    }


@pytest.fixture
def temp_exercise_dir(tmp_path):
    """Create a temporary directory for exercise files."""
    exercise_dir = tmp_path / "exercises"
    exercise_dir.mkdir()
    return exercise_dir
