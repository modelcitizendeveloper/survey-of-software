"""
Unit tests for ExerciseBuilder class.

Tests exercise generation for all 15 exercise types.
"""

import pytest
import sys
from pathlib import Path

# Add exercises directory to path
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


@pytest.mark.unit
@pytest.mark.generator
class TestExerciseBuilder:
    """Test ExerciseBuilder functionality."""

    def test_init(self, sample_vocabulary, declension_templates):
        """Test ExerciseBuilder initialization."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        assert builder.vocab == sample_vocabulary
        assert builder.form_gen == form_gen
        assert builder.words == sample_vocabulary['words']
        assert '1st' in builder.usage_counter
        assert '5th' in builder.usage_counter

    def test_get_word_by_declension(self, sample_vocabulary, declension_templates):
        """Test getting word by declension."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        word_1st = builder.get_word_by_declension('1st', rotate=False)
        assert word_1st['lemma'] == 'puella'
        assert word_1st['declension'] == '1st'

        word_2nd = builder.get_word_by_declension('2nd', rotate=False)
        assert word_2nd['declension'] == '2nd'

    def test_get_word_by_declension_rotation(self, sample_vocabulary, declension_templates):
        """Test word rotation through multiple calls."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        # First call gets first 2nd decl word
        word1 = builder.get_word_by_declension('2nd', rotate=True)
        first_lemma = word1['lemma']

        # Second call should get different word if multiple exist
        word2 = builder.get_word_by_declension('2nd', rotate=True)

        # Both should be 2nd declension
        assert word1['declension'] == '2nd'
        assert word2['declension'] == '2nd'

        # Usage counter should increment
        assert builder.usage_counter['2nd'] == 2

    def test_build_word_data_simple(self, sample_vocabulary, declension_templates):
        """Test building word data structure."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        word = sample_vocabulary['words'][0]  # puella
        word_data = builder.build_word_data(word, 'nominative', 'singular')

        assert word_data['text'] == 'puella'
        assert word_data['lemma'] == 'puella'
        assert word_data['pos'] == 'NOUN'
        assert word_data['declension'] == '1st'
        assert word_data['gender'] == 'f'
        assert word_data['number'] == 'singular'
        assert word_data['case'] == 'nominative'

    def test_build_word_data_ambiguous(self, sample_vocabulary, declension_templates):
        """Test building word data with ambiguous case."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        word = sample_vocabulary['words'][0]  # puella
        word_data = builder.build_word_data(word, 'genitive', 'singular')

        assert word_data['text'] == 'puellae'
        assert word_data['case'] == ['genitive', 'dative']  # Ambiguous

    # Single declension tests
    def test_build_single_declension_structure(self, sample_vocabulary, declension_templates):
        """Test single declension exercise structure."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_single_declension('1st')

        assert len(lines) == 2  # Singular and plural lines
        assert 'sentence' in lines[0]
        assert 'words' in lines[0]
        assert len(lines[0]['words']) == 6  # 6 cases
        assert len(lines[1]['words']) == 6  # 6 cases

    def test_build_single_declension_all_cases(self, sample_vocabulary, declension_templates):
        """Test single declension includes all cases."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_single_declension('1st')
        cases_sg = [w['case'] for w in lines[0]['words']]
        cases_pl = [w['case'] for w in lines[1]['words']]

        # Should have all 6 cases (some may be ambiguous lists)
        expected_cases = ['nominative', 'genitive', 'dative', 'accusative', 'ablative', 'vocative']

        for expected in expected_cases:
            # Check if case appears as string or in ambiguous list
            found_sg = any(expected == c if isinstance(c, str) else expected in c for c in cases_sg)
            found_pl = any(expected == c if isinstance(c, str) else expected in c for c in cases_pl)
            assert found_sg, f"Missing {expected} in singular"
            assert found_pl, f"Missing {expected} in plural"

    def test_build_single_declension_2nd(self, sample_vocabulary, declension_templates):
        """Test 2nd declension exercise generation."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_single_declension('2nd')
        assert len(lines) == 2

        # First word should be 2nd declension
        assert lines[0]['words'][0]['declension'] == '2nd'

    # Single case tests
    def test_build_single_case_structure(self, sample_vocabulary, declension_templates):
        """Test single case exercise structure."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_single_case('nominative')

        assert len(lines) == 2  # Singular and plural
        assert len(lines[0]['words']) == 5  # 5 declensions (singular)
        assert len(lines[1]['words']) == 5  # 5 declensions (plural)

    def test_build_single_case_correct_case(self, sample_vocabulary, declension_templates):
        """Test single case exercise has correct case."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_single_case('accusative')

        # All words should be accusative (or ambiguous including accusative)
        for line in lines:
            for word in line['words']:
                case = word['case']
                if isinstance(case, list):
                    assert 'accusative' in case
                else:
                    assert case == 'accusative'

    def test_build_single_case_all_declensions(self, sample_vocabulary, declension_templates):
        """Test single case includes all declensions."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_single_case('genitive')

        # Should have words from all 5 declensions
        decls_sg = [w['declension'] for w in lines[0]['words']]
        decls_pl = [w['declension'] for w in lines[1]['words']]

        for decl in ['1st', '2nd', '3rd', '4th', '5th']:
            assert decl in decls_sg, f"Missing {decl} in singular"
            assert decl in decls_pl, f"Missing {decl} in plural"

    # Single number tests
    def test_build_single_number_structure(self, sample_vocabulary, declension_templates):
        """Test single number exercise structure."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_single_number('singular')

        # Should have 5 lines (one per declension)
        assert len(lines) == 5

        # Each line should have 6 words (6 cases)
        for line in lines:
            assert len(line['words']) == 6

    def test_build_single_number_correct_number(self, sample_vocabulary, declension_templates):
        """Test single number exercise has correct number."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_single_number('plural')

        # All words should be plural
        for line in lines:
            for word in line['words']:
                assert word['number'] == 'plural'

    def test_build_single_number_all_declensions(self, sample_vocabulary, declension_templates):
        """Test single number includes all declensions."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_single_number('singular')

        # Should have one line per declension
        declensions = [line['words'][0]['declension'] for line in lines]
        for decl in ['1st', '2nd', '3rd', '4th', '5th']:
            assert decl in declensions

    # Integration tests
    def test_build_integration_structure(self, sample_vocabulary, declension_templates):
        """Test integration exercise structure."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_integration()

        # Should have multiple sentences (5-6)
        assert len(lines) >= 5
        assert len(lines) <= 6

        # Each sentence should have 5 words
        for line in lines:
            assert len(line['words']) == 5

    def test_build_integration_mixed_cases(self, sample_vocabulary, declension_templates):
        """Test integration has mixed cases."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_integration()

        # Collect all cases used
        all_cases = []
        for line in lines:
            for word in line['words']:
                case = word['case']
                if isinstance(case, list):
                    all_cases.extend(case)
                else:
                    all_cases.append(case)

        # Should have variety of cases
        unique_cases = set(all_cases)
        assert len(unique_cases) >= 4  # At least 4 different cases

    def test_build_integration_mixed_numbers(self, sample_vocabulary, declension_templates):
        """Test integration has mixed numbers."""
        form_gen = FormGenerator(declension_templates)
        builder = ExerciseBuilder(sample_vocabulary, form_gen)

        lines = builder.build_integration()

        # Collect all numbers used
        all_numbers = []
        for line in lines:
            for word in line['words']:
                all_numbers.append(word['number'])

        # Should have both singular and plural
        assert 'singular' in all_numbers
        assert 'plural' in all_numbers
