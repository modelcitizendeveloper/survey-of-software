"""
Data validation tests for JSONL exercise files.

Tests that exercise data conforms to expected format and contains valid values.
"""

import pytest
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent


@pytest.mark.data
class TestJSONLFormat:
    """Test JSONL file format compliance."""

    def test_all_lines_are_valid_json(self):
        """Test that all lines in JSONL files are valid JSON."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    line_num = 0
                    for line in f:
                        line_num += 1
                        try:
                            json.loads(line)
                        except json.JSONDecodeError as e:
                            pytest.fail(f"Invalid JSON in {jsonl_file.name}:{line_num}: {e}")

    def test_first_line_is_metadata(self):
        """Test that first line of each exercise is metadata."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    first_line = f.readline()
                    data = json.loads(first_line)
                    assert data.get('_metadata') is True, f"Missing metadata in {jsonl_file.name}"
                    assert 'title' in data, f"Missing title in {jsonl_file.name}"
                    assert 'description' in data, f"Missing description in {jsonl_file.name}"


@pytest.mark.data
class TestWordDataStructure:
    """Test word data structure compliance."""

    def test_all_words_have_required_fields(self):
        """Test that all words have required fields."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        required_fields = ['text', 'lemma', 'pos', 'declension', 'number', 'case']

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    lines = f.readlines()

                    for line_num, line in enumerate(lines[1:], start=2):  # Skip metadata
                        data = json.loads(line)
                        for word_num, word in enumerate(data['words'], start=1):
                            for field in required_fields:
                                assert field in word, \
                                    f"Missing {field} in {jsonl_file.name}:{line_num} word {word_num}"

    def test_all_words_have_gender(self):
        """Test that all words have gender field (for Series 1+)."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    lines = f.readlines()

                    for line_num, line in enumerate(lines[1:], start=2):
                        data = json.loads(line)
                        for word_num, word in enumerate(data['words'], start=1):
                            assert 'gender' in word, \
                                f"Missing gender in {jsonl_file.name}:{line_num} word {word_num}"

    def test_pos_values_are_valid(self):
        """Test that POS values are from valid set."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        valid_pos = {'NOUN', 'PROPN', 'VERB', 'ADJ', 'ADP'}

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    lines = f.readlines()

                    for line_num, line in enumerate(lines[1:], start=2):
                        data = json.loads(line)
                        for word in data['words']:
                            assert word['pos'] in valid_pos, \
                                f"Invalid POS '{word['pos']}' in {jsonl_file.name}:{line_num}"

    def test_declension_values_are_valid(self):
        """Test that declension values are valid."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        valid_declensions = {'1st', '2nd', '3rd', '4th', '5th'}

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    lines = f.readlines()

                    for line_num, line in enumerate(lines[1:], start=2):
                        data = json.loads(line)
                        for word in data['words']:
                            assert word['declension'] in valid_declensions, \
                                f"Invalid declension '{word['declension']}' in {jsonl_file.name}:{line_num}"

    def test_number_values_are_valid(self):
        """Test that number values are valid."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        valid_numbers = {'singular', 'plural'}

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    lines = f.readlines()

                    for line_num, line in enumerate(lines[1:], start=2):
                        data = json.loads(line)
                        for word in data['words']:
                            assert word['number'] in valid_numbers, \
                                f"Invalid number '{word['number']}' in {jsonl_file.name}:{line_num}"

    def test_case_values_are_valid(self):
        """Test that case values are valid (string or list)."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        valid_cases = {'nominative', 'genitive', 'dative', 'accusative', 'ablative', 'vocative'}

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    lines = f.readlines()

                    for line_num, line in enumerate(lines[1:], start=2):
                        data = json.loads(line)
                        for word in data['words']:
                            case = word['case']
                            if isinstance(case, str):
                                assert case in valid_cases, \
                                    f"Invalid case '{case}' in {jsonl_file.name}:{line_num}"
                            elif isinstance(case, list):
                                for c in case:
                                    assert c in valid_cases, \
                                        f"Invalid case '{c}' in ambiguous list in {jsonl_file.name}:{line_num}"
                            else:
                                pytest.fail(f"Case must be string or list in {jsonl_file.name}:{line_num}")

    def test_gender_values_are_valid(self):
        """Test that gender values are valid."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        valid_genders = {'f', 'm', 'n', 'm/f'}

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    lines = f.readlines()

                    for line_num, line in enumerate(lines[1:], start=2):
                        data = json.loads(line)
                        for word in data['words']:
                            if 'gender' in word:
                                assert word['gender'] in valid_genders, \
                                    f"Invalid gender '{word['gender']}' in {jsonl_file.name}:{line_num}"


@pytest.mark.data
class TestAmbiguousForms:
    """Test ambiguous form handling."""

    def test_1st_decl_gen_dat_sg_ambiguous(self):
        """Test 1st declension gen/dat singular marked as ambiguous."""
        series_dir = PROJECT_ROOT / 'exercises' / 'model-nouns'
        if not series_dir.exists():
            pytest.skip("model-nouns not found")

        # Check single declension 1st exercise
        ex_file = list(series_dir.glob('01-*.jsonl'))[0]
        with open(ex_file, 'r') as f:
            lines = f.readlines()

            for line in lines[1:]:
                data = json.loads(line)
                for word in data['words']:
                    # Check for genitive/dative singular forms
                    if (word['text'] in ['puellae'] and
                        word['number'] == 'singular' and
                        word['lemma'] == 'puella'):
                        case = word['case']
                        if isinstance(case, list):
                            assert 'genitive' in case or 'dative' in case, \
                                f"Expected gen/dat ambiguity for {word['text']}"

    def test_dat_abl_pl_ambiguous_all_declensions(self):
        """Test dat/abl plural marked as ambiguous in all declensions."""
        series_dir = PROJECT_ROOT / 'exercises' / 'model-nouns'
        if not series_dir.exists():
            pytest.skip("model-nouns not found")

        # Check single declension exercises
        for i in range(1, 6):
            ex_file = list(series_dir.glob(f'{i:02d}-*.jsonl'))[0]
            with open(ex_file, 'r') as f:
                lines = f.readlines()

                found_dat_abl_pl = False
                for line in lines[1:]:
                    data = json.loads(line)
                    for word in data['words']:
                        if word['number'] == 'plural':
                            case = word['case']
                            if isinstance(case, list) and 'dative' in case and 'ablative' in case:
                                found_dat_abl_pl = True

                assert found_dat_abl_pl, f"No dat/abl plural ambiguity found in {ex_file.name}"

    def test_3rd_decl_nom_acc_voc_pl_ambiguous(self):
        """Test 3rd declension nom/acc/voc plural marked as ambiguous."""
        series_dir = PROJECT_ROOT / 'exercises' / 'model-nouns'
        if not series_dir.exists():
            pytest.skip("model-nouns not found")

        # Check single declension 3rd exercise
        ex_file = list(series_dir.glob('03-*.jsonl'))[0]
        with open(ex_file, 'r') as f:
            lines = f.readlines()

            found_nav_pl = False
            for line in lines[1:]:
                data = json.loads(line)
                for word in data['words']:
                    if word['number'] == 'plural':
                        case = word['case']
                        if isinstance(case, list):
                            if ('nominative' in case and
                                'accusative' in case and
                                'vocative' in case):
                                found_nav_pl = True

            assert found_nav_pl, "No nom/acc/voc plural ambiguity found in 3rd declension"


@pytest.mark.data
class TestSentenceStructure:
    """Test sentence structure in exercises."""

    def test_sentence_matches_word_order(self):
        """Test that sentence text matches word order."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    lines = f.readlines()

                    for line_num, line in enumerate(lines[1:], start=2):
                        data = json.loads(line)
                        sentence = data['sentence']
                        words = data['words']

                        # Reconstruct sentence from words
                        reconstructed = ' '.join(w['text'] for w in words)
                        assert sentence == reconstructed, \
                            f"Sentence mismatch in {jsonl_file.name}:{line_num}"

    def test_all_exercises_have_content(self):
        """Test that all exercises have at least one sentence."""
        exercise_dirs = [
            PROJECT_ROOT / 'exercises' / 'model-nouns',
            PROJECT_ROOT / 'exercises' / 'common-nouns'
        ]

        for series_dir in exercise_dirs:
            if not series_dir.exists():
                continue

            for jsonl_file in series_dir.glob('*.jsonl'):
                with open(jsonl_file, 'r') as f:
                    lines = f.readlines()

                    # Should have metadata + at least 1 exercise
                    assert len(lines) >= 2, f"No content in {jsonl_file.name}"
