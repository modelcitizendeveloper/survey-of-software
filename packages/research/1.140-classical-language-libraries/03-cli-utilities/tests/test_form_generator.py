"""
Unit tests for FormGenerator class.

Tests stem extraction, form generation, irregular handling, and ambiguous forms.
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


@pytest.mark.unit
@pytest.mark.generator
class TestFormGenerator:
    """Test FormGenerator functionality."""

    def test_init(self, declension_templates):
        """Test FormGenerator initialization."""
        gen = FormGenerator(declension_templates)
        assert gen.templates == declension_templates

    # Stem extraction tests
    def test_get_stem_1st_declension(self, declension_templates):
        """Test stem extraction for 1st declension (remove -a)."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "puella", "declension": "1st"}
        assert gen.get_stem(word) == "puell"

    def test_get_stem_2nd_declension(self, declension_templates):
        """Test stem extraction for 2nd declension (remove -us)."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "ventus", "declension": "2nd"}
        assert gen.get_stem(word) == "vent"

    def test_get_stem_3rd_declension_from_genitive(self, declension_templates):
        """Test stem extraction for 3rd declension from genitive."""
        gen = FormGenerator(declension_templates)
        word = {
            "lemma": "homo",
            "declension": "3rd",
            "genitive_singular": "hominis"
        }
        assert gen.get_stem(word) == "homin"

    def test_get_stem_4th_declension(self, declension_templates):
        """Test stem extraction for 4th declension (remove -us)."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "usus", "declension": "4th"}
        assert gen.get_stem(word) == "us"

    def test_get_stem_5th_declension(self, declension_templates):
        """Test stem extraction for 5th declension (remove -ēs)."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "diēs", "declension": "5th"}
        assert gen.get_stem(word) == "di"

    # Regular form generation tests
    def test_generate_1st_decl_nominative_sg(self, declension_templates):
        """Test 1st declension nominative singular."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "puella", "declension": "1st", "irregular": False}
        form = gen.generate_form(word, "nominative", "singular")
        assert form == "puella"

    def test_generate_1st_decl_genitive_sg(self, declension_templates):
        """Test 1st declension genitive singular."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "puella", "declension": "1st", "irregular": False}
        form = gen.generate_form(word, "genitive", "singular")
        assert form == "puellae"

    def test_generate_2nd_decl_accusative_pl(self, declension_templates):
        """Test 2nd declension accusative plural."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "ventus", "declension": "2nd", "irregular": False}
        form = gen.generate_form(word, "accusative", "plural")
        assert form == "ventōs"

    # Irregular form tests
    def test_generate_vir_nominative(self, declension_templates):
        """Test vir irregular nominative (no -us ending)."""
        gen = FormGenerator(declension_templates)
        word = {
            "lemma": "vir",
            "declension": "2nd",
            "irregular": True,
            "genitive_singular": "virī",
            "forms_override": {
                "singular": {
                    "nominative": "vir",
                    "vocative": "vir"
                }
            }
        }
        form = gen.generate_form(word, "nominative", "singular")
        assert form == "vir"

    def test_generate_vir_vocative(self, declension_templates):
        """Test vir irregular vocative (not -e)."""
        gen = FormGenerator(declension_templates)
        word = {
            "lemma": "vir",
            "declension": "2nd",
            "irregular": True,
            "genitive_singular": "virī",
            "forms_override": {
                "singular": {
                    "nominative": "vir",
                    "vocative": "vir"
                }
            }
        }
        form = gen.generate_form(word, "vocative", "singular")
        assert form == "vir"

    def test_generate_3rd_decl_nominative_uses_lemma(self, declension_templates):
        """Test 3rd declension nominative singular uses lemma."""
        gen = FormGenerator(declension_templates)
        word = {
            "lemma": "homo",
            "declension": "3rd",
            "genitive_singular": "hominis"
        }
        form = gen.generate_form(word, "nominative", "singular")
        assert form == "homo"  # Not "homin"

    def test_generate_3rd_decl_vocative_uses_lemma(self, declension_templates):
        """Test 3rd declension vocative singular uses lemma."""
        gen = FormGenerator(declension_templates)
        word = {
            "lemma": "homo",
            "declension": "3rd",
            "genitive_singular": "hominis"
        }
        form = gen.generate_form(word, "vocative", "singular")
        assert form == "homo"  # Not "homin"

    def test_generate_3rd_decl_accusative(self, declension_templates):
        """Test 3rd declension accusative uses stem + ending."""
        gen = FormGenerator(declension_templates)
        word = {
            "lemma": "homo",
            "declension": "3rd",
            "genitive_singular": "hominis"
        }
        form = gen.generate_form(word, "accusative", "singular")
        assert form == "hominem"

    # Neuter noun tests
    def test_generate_neuter_nominative_sg(self, declension_templates):
        """Test neuter nominative singular uses lemma."""
        gen = FormGenerator(declension_templates)
        word = {
            "lemma": "nomen",
            "declension": "3rd",
            "genitive_singular": "nominis",
            "neuter": True
        }
        form = gen.generate_form(word, "nominative", "singular")
        assert form == "nomen"

    def test_generate_neuter_accusative_sg_equals_nominative(self, declension_templates):
        """Test neuter accusative singular = nominative."""
        gen = FormGenerator(declension_templates)
        word = {
            "lemma": "nomen",
            "declension": "3rd",
            "genitive_singular": "nominis",
            "neuter": True
        }
        form = gen.generate_form(word, "accusative", "singular")
        assert form == "nomen"  # Same as nominative

    def test_generate_neuter_vocative_sg_equals_nominative(self, declension_templates):
        """Test neuter vocative singular = nominative."""
        gen = FormGenerator(declension_templates)
        word = {
            "lemma": "nomen",
            "declension": "3rd",
            "genitive_singular": "nominis",
            "neuter": True
        }
        form = gen.generate_form(word, "vocative", "singular")
        assert form == "nomen"  # Same as nominative

    # Ambiguous forms tests
    def test_ambiguous_1st_decl_gen_dat_sg(self, declension_templates):
        """Test 1st declension gen/dat singular ambiguity."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "puella", "declension": "1st"}

        ambig_gen = gen.get_ambiguous_cases(word, "genitive", "singular")
        assert ambig_gen == ["genitive", "dative"]

        ambig_dat = gen.get_ambiguous_cases(word, "dative", "singular")
        assert ambig_dat == ["genitive", "dative"]

    def test_ambiguous_1st_decl_dat_abl_pl(self, declension_templates):
        """Test 1st declension dat/abl plural ambiguity."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "puella", "declension": "1st"}

        ambig_dat = gen.get_ambiguous_cases(word, "dative", "plural")
        assert ambig_dat == ["dative", "ablative"]

        ambig_abl = gen.get_ambiguous_cases(word, "ablative", "plural")
        assert ambig_abl == ["dative", "ablative"]

    def test_ambiguous_2nd_decl_dat_abl_sg(self, declension_templates):
        """Test 2nd declension dat/abl singular ambiguity."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "ventus", "declension": "2nd"}

        ambig = gen.get_ambiguous_cases(word, "dative", "singular")
        assert ambig == ["dative", "ablative"]

    def test_ambiguous_3rd_decl_nom_acc_voc_pl(self, declension_templates):
        """Test 3rd declension nom/acc/voc plural ambiguity."""
        gen = FormGenerator(declension_templates)
        word = {
            "lemma": "homo",
            "declension": "3rd",
            "genitive_singular": "hominis"
        }

        for case in ["nominative", "accusative", "vocative"]:
            ambig = gen.get_ambiguous_cases(word, case, "plural")
            assert ambig == ["nominative", "accusative", "vocative"]

    def test_no_ambiguity_for_unique_forms(self, declension_templates):
        """Test that unique forms return None."""
        gen = FormGenerator(declension_templates)
        word = {"lemma": "puella", "declension": "1st"}

        ambig = gen.get_ambiguous_cases(word, "accusative", "singular")
        assert ambig is None
