"""
Integration tests for vocabulary exercise generation.

Tests the complete flow from vocabulary JSON to exercise JSONL files.
"""

import pytest
import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'exercises'))

# Now import
import importlib.util
spec = importlib.util.spec_from_file_location(
    "generate_vocabulary_exercises",
    PROJECT_ROOT / 'exercises' / 'generate-vocabulary-exercises.py'
)
gen_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen_module)
FormGenerator = gen_module.FormGenerator
ExerciseBuilder = gen_module.ExerciseBuilder
generate_series = gen_module.generate_series
load_json_file = gen_module.load_json_file


@pytest.mark.integration
@pytest.mark.generator
class TestEndToEndGeneration:
    """Test complete exercise generation workflow."""

    def test_generate_complete_series(self, sample_vocabulary, declension_templates, temp_exercise_dir):
        """Test generating a complete exercise series."""
        # Create vocab file
        vocab_file = temp_exercise_dir / "test-vocab.json"
        with open(vocab_file, 'w') as f:
            json.dump(sample_vocabulary, f)

        # Generate series
        generate_series(vocab_file, temp_exercise_dir)

        # Check series directory was created
        series_dir = temp_exercise_dir / sample_vocabulary['series_name']
        assert series_dir.exists()

        # Check metadata file
        metadata_file = series_dir / '.series-metadata.json'
        assert metadata_file.exists()

        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            assert metadata['title'] == sample_vocabulary['series_title']
            assert metadata['level'] == sample_vocabulary['level']

        # Check all 15 exercise files were created
        exercise_files = list(series_dir.glob('*.jsonl'))
        assert len(exercise_files) == 15

        # Check files are numbered correctly
        for i in range(1, 16):
            expected_file = series_dir / f"{i:02d}-*.jsonl"
            matching = list(series_dir.glob(f"{i:02d}-*.jsonl"))
            assert len(matching) == 1, f"Missing exercise {i:02d}"

    def test_generated_files_have_metadata(self, sample_vocabulary, temp_exercise_dir):
        """Test that generated files have metadata line."""
        vocab_file = temp_exercise_dir / "test-vocab.json"
        with open(vocab_file, 'w') as f:
            json.dump(sample_vocabulary, f)

        generate_series(vocab_file, temp_exercise_dir)

        series_dir = temp_exercise_dir / sample_vocabulary['series_name']
        exercise_files = list(series_dir.glob('*.jsonl'))

        for ex_file in exercise_files:
            with open(ex_file, 'r') as f:
                first_line = f.readline()
                metadata = json.loads(first_line)
                assert metadata.get('_metadata') is True
                assert 'title' in metadata
                assert 'description' in metadata

    def test_generated_exercises_have_content(self, sample_vocabulary, temp_exercise_dir):
        """Test that generated exercises have actual exercise lines."""
        vocab_file = temp_exercise_dir / "test-vocab.json"
        with open(vocab_file, 'w') as f:
            json.dump(sample_vocabulary, f)

        generate_series(vocab_file, temp_exercise_dir)

        series_dir = temp_exercise_dir / sample_vocabulary['series_name']
        exercise_files = list(series_dir.glob('*.jsonl'))

        for ex_file in exercise_files:
            with open(ex_file, 'r') as f:
                lines = f.readlines()
                assert len(lines) >= 2  # Metadata + at least 1 exercise line

                # Check first content line (after metadata)
                if len(lines) > 1:
                    exercise_line = json.loads(lines[1])
                    assert 'sentence' in exercise_line
                    assert 'words' in exercise_line
                    assert len(exercise_line['words']) > 0

    def test_single_declension_exercises_correct(self, sample_vocabulary, temp_exercise_dir):
        """Test single declension exercises (01-05) are correct."""
        vocab_file = temp_exercise_dir / "test-vocab.json"
        with open(vocab_file, 'w') as f:
            json.dump(sample_vocabulary, f)

        generate_series(vocab_file, temp_exercise_dir)

        series_dir = temp_exercise_dir / sample_vocabulary['series_name']

        # Check first exercise (1st declension)
        ex_file = list(series_dir.glob('01-*.jsonl'))[0]
        with open(ex_file, 'r') as f:
            lines = f.readlines()

            # Skip metadata
            for line in lines[1:]:
                exercise = json.loads(line)
                # All words should be 1st declension
                for word in exercise['words']:
                    assert word['declension'] == '1st'

    def test_single_case_exercises_correct(self, sample_vocabulary, temp_exercise_dir):
        """Test single case exercises (06-11) are correct."""
        vocab_file = temp_exercise_dir / "test-vocab.json"
        with open(vocab_file, 'w') as f:
            json.dump(sample_vocabulary, f)

        generate_series(vocab_file, temp_exercise_dir)

        series_dir = temp_exercise_dir / sample_vocabulary['series_name']

        # Check nominative case exercise (06)
        ex_file = list(series_dir.glob('06-*.jsonl'))[0]
        with open(ex_file, 'r') as f:
            lines = f.readlines()

            # Skip metadata
            for line in lines[1:]:
                exercise = json.loads(line)
                # All words should be nominative (or ambiguous including nominative)
                for word in exercise['words']:
                    case = word['case']
                    if isinstance(case, list):
                        assert 'nominative' in case
                    else:
                        assert case == 'nominative'

    def test_generated_words_have_required_fields(self, sample_vocabulary, temp_exercise_dir):
        """Test that all generated words have required fields."""
        vocab_file = temp_exercise_dir / "test-vocab.json"
        with open(vocab_file, 'w') as f:
            json.dump(sample_vocabulary, f)

        generate_series(vocab_file, temp_exercise_dir)

        series_dir = temp_exercise_dir / sample_vocabulary['series_name']
        exercise_files = list(series_dir.glob('*.jsonl'))

        required_fields = ['text', 'lemma', 'pos', 'declension', 'gender', 'number', 'case']

        for ex_file in exercise_files:
            with open(ex_file, 'r') as f:
                lines = f.readlines()

                for line in lines[1:]:  # Skip metadata
                    exercise = json.loads(line)
                    for word in exercise['words']:
                        for field in required_fields:
                            assert field in word, f"Missing {field} in {ex_file.name}"


@pytest.mark.integration
@pytest.mark.slow
class TestRealSeriesValidation:
    """Validate existing generated series."""

    def test_model_nouns_series_structure(self):
        """Test model-nouns series has correct structure."""
        series_dir = PROJECT_ROOT / 'exercises' / 'model-nouns'

        if not series_dir.exists():
            pytest.skip("model-nouns series not found")

        # Check metadata
        metadata_file = series_dir / '.series-metadata.json'
        assert metadata_file.exists()

        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            assert metadata['title'] == "Model Nouns (Foundation)"
            assert metadata['level'] == "beginner"

        # Check 15 exercises exist
        exercise_files = list(series_dir.glob('*.jsonl'))
        assert len(exercise_files) == 15

    def test_common_nouns_series_structure(self):
        """Test common-nouns series has correct structure."""
        series_dir = PROJECT_ROOT / 'exercises' / 'common-nouns'

        if not series_dir.exists():
            pytest.skip("common-nouns series not found")

        # Check metadata
        metadata_file = series_dir / '.series-metadata.json'
        assert metadata_file.exists()

        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            assert metadata['title'] == "Common Nouns (Intermediate)"
            assert metadata['level'] == "intermediate"

        # Check 15 exercises exist
        exercise_files = list(series_dir.glob('*.jsonl'))
        assert len(exercise_files) == 15

    def test_irregular_nouns_in_common_series(self):
        """Test that common-nouns series includes irregular nouns."""
        series_dir = PROJECT_ROOT / 'exercises' / 'common-nouns'

        if not series_dir.exists():
            pytest.skip("common-nouns series not found")

        # Look for vir, filius, nomen, etc. in exercises
        found_irregulars = set()

        for ex_file in series_dir.glob('*.jsonl'):
            with open(ex_file, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    if data.get('_metadata'):
                        continue

                    for word in data['words']:
                        lemma = word.get('lemma')
                        if lemma in ['vir', 'filius', 'nomen', 'manus', 'domus', 'dies']:
                            found_irregulars.add(lemma)

        # Should have at least some irregular nouns
        assert len(found_irregulars) >= 3, f"Only found {found_irregulars}"
