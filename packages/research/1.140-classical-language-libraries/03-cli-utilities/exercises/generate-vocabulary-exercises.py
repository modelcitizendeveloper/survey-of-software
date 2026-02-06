#!/usr/bin/env python3
"""
Generate complete 15-exercise series from vocabulary list.

Usage:
    python generate-vocabulary-exercises.py series-2-common-nouns.json
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class FormGenerator:
    """Generate declined forms from word data and declension templates."""

    def __init__(self, templates: Dict):
        self.templates = templates

    def get_stem(self, word: Dict) -> str:
        """Extract stem from lemma using declension pattern."""
        lemma = word['lemma']
        decl = word['declension']

        # Handle forms_override for irregular words
        if word.get('irregular') and 'genitive_singular' in word:
            # For 3rd declension, stem comes from genitive
            if decl == '3rd':
                gen_sg = word['genitive_singular']
                # Remove -is ending to get stem
                if gen_sg.endswith('is'):
                    return gen_sg[:-2]

        template = self.templates[decl]
        stem_rule = template['stem_rule']

        if stem_rule == 'remove_a':
            return lemma[:-1] if lemma.endswith('a') else lemma
        elif stem_rule == 'remove_us':
            return lemma[:-2] if lemma.endswith('us') else lemma
        elif stem_rule == 'remove_es':
            return lemma[:-2] if lemma.endswith('ēs') or lemma.endswith('es') else lemma
        elif stem_rule == 'from_genitive':
            # For 3rd declension, need genitive_singular
            if 'genitive_singular' in word:
                gen_sg = word['genitive_singular']
                if gen_sg.endswith('is'):
                    return gen_sg[:-2]
            # Fallback: use lemma as-is
            return lemma

        return lemma

    def generate_form(self, word: Dict, case: str, number: str) -> str:
        """Generate a specific declined form."""
        # Check for form override first (irregular forms)
        if word.get('forms_override'):
            if number in word['forms_override']:
                if case in word['forms_override'][number]:
                    return word['forms_override'][number][case]

        decl = word['declension']
        template = self.templates[decl]
        stem = self.get_stem(word)

        # Special handling for 3rd declension nominative/vocative singular
        # These use the lemma, not stem + ending, because nom sg is often irregular
        if decl == '3rd' and number == 'singular' and case in ('nominative', 'vocative'):
            return word['lemma']

        # Get ending from template
        ending = template[number][case]

        # Special handling for neuter nouns
        if word.get('neuter'):
            # Neuter: nominative = accusative = vocative
            if case in ('accusative', 'vocative'):
                # For singular, use the lemma (which is the nominative)
                if number == 'singular':
                    return word['lemma']
                # For plural, use the nominative ending
                ending = template[number]['nominative']

        return stem + ending

    def get_ambiguous_cases(self, word: Dict, case: str, number: str) -> Optional[List[str]]:
        """Check if this case/number combination is ambiguous."""
        decl = word['declension']
        template = self.templates[decl]

        if number not in template['ambiguous']:
            return None

        for pattern in template['ambiguous'][number]:
            cases = pattern.split('|')
            if case in cases:
                return cases

        return None


class ExerciseBuilder:
    """Build exercise files from vocabulary and templates."""

    def __init__(self, vocab: Dict, form_gen: FormGenerator):
        self.vocab = vocab
        self.form_gen = form_gen
        self.words = vocab['words']
        self.usage_counter = {decl: 0 for decl in ['1st', '2nd', '3rd', '4th', '5th']}

    def get_word_by_declension(self, declension: str, rotate: bool = True) -> Optional[Dict]:
        """Get a word of the specified declension."""
        candidates = [w for w in self.words if w['declension'] == declension]
        if not candidates:
            return None

        if rotate:
            # Rotate through words to ensure variety
            idx = self.usage_counter[declension] % len(candidates)
            self.usage_counter[declension] += 1
            return candidates[idx]
        else:
            return candidates[0]

    def build_word_data(self, word: Dict, case: str, number: str) -> Dict:
        """Build word data structure for JSONL output."""
        form = self.form_gen.generate_form(word, case, number)
        ambiguous = self.form_gen.get_ambiguous_cases(word, case, number)

        return {
            "text": form,
            "lemma": word['lemma'],
            "pos": "NOUN",
            "declension": word['declension'],
            "gender": word['gender'],
            "number": number,
            "case": ambiguous if ambiguous else case
        }

    def build_single_declension(self, declension: str) -> List[Dict]:
        """Build single-declension exercise (all 12 forms of one noun)."""
        word = self.get_word_by_declension(declension, rotate=False)
        if not word:
            return []

        lines = []

        # Singular: nom gen dat acc abl voc
        singular_words = []
        for case in ['nominative', 'genitive', 'dative', 'accusative', 'ablative', 'vocative']:
            singular_words.append(self.build_word_data(word, case, 'singular'))

        lines.append({
            'sentence': ' '.join(w['text'] for w in singular_words),
            'words': singular_words
        })

        # Plural: nom gen dat acc abl voc
        plural_words = []
        for case in ['nominative', 'genitive', 'dative', 'accusative', 'ablative', 'vocative']:
            plural_words.append(self.build_word_data(word, case, 'plural'))

        lines.append({
            'sentence': ' '.join(w['text'] for w in plural_words),
            'words': plural_words
        })

        return lines

    def build_single_case(self, case: str) -> List[Dict]:
        """Build single-case exercise (one case across all declensions, both numbers)."""
        lines = []

        # Singular: one word from each declension
        singular_words = []
        for decl in ['1st', '2nd', '3rd', '4th', '5th']:
            word = self.get_word_by_declension(decl, rotate=True)
            if word:
                singular_words.append(self.build_word_data(word, case, 'singular'))

        if singular_words:
            lines.append({
                'sentence': ' '.join(w['text'] for w in singular_words),
                'words': singular_words
            })

        # Plural: one word from each declension
        plural_words = []
        for decl in ['1st', '2nd', '3rd', '4th', '5th']:
            word = self.get_word_by_declension(decl, rotate=True)
            if word:
                plural_words.append(self.build_word_data(word, case, 'plural'))

        if plural_words:
            lines.append({
                'sentence': ' '.join(w['text'] for w in plural_words),
                'words': plural_words
            })

        return lines

    def build_single_number(self, number: str) -> List[Dict]:
        """Build single-number exercise (all cases, all declensions, one number)."""
        lines = []

        # For each declension, show all 6 cases
        for decl in ['1st', '2nd', '3rd', '4th', '5th']:
            word = self.get_word_by_declension(decl, rotate=True)
            if not word:
                continue

            case_words = []
            for case in ['nominative', 'genitive', 'dative', 'accusative', 'ablative', 'vocative']:
                case_words.append(self.build_word_data(word, case, number))

            lines.append({
                'sentence': ' '.join(w['text'] for w in case_words),
                'words': case_words
            })

        return lines

    def build_integration(self) -> List[Dict]:
        """Build integration exercise (mixed cases, numbers, declensions)."""
        lines = []

        # Create 5-6 sentences mixing everything
        # Each sentence uses different words in different forms
        patterns = [
            [('nominative', 'singular'), ('genitive', 'singular'), ('dative', 'singular'),
             ('accusative', 'singular'), ('ablative', 'singular')],
            [('nominative', 'plural'), ('genitive', 'plural'), ('dative', 'plural'),
             ('accusative', 'plural'), ('ablative', 'plural')],
            [('nominative', 'singular'), ('accusative', 'singular'), ('nominative', 'plural'),
             ('accusative', 'plural'), ('ablative', 'singular')],
            [('genitive', 'singular'), ('dative', 'plural'), ('accusative', 'singular'),
             ('nominative', 'plural'), ('ablative', 'plural')],
            [('nominative', 'singular'), ('genitive', 'plural'), ('dative', 'singular'),
             ('accusative', 'plural'), ('ablative', 'singular')],
            [('vocative', 'singular'), ('nominative', 'plural'), ('genitive', 'singular'),
             ('dative', 'plural'), ('accusative', 'singular')]
        ]

        for pattern in patterns:
            sentence_words = []
            for case, number in pattern:
                # Pick a random declension
                decl = ['1st', '2nd', '3rd', '4th', '5th'][len(sentence_words) % 5]
                word = self.get_word_by_declension(decl, rotate=True)
                if word:
                    sentence_words.append(self.build_word_data(word, case, number))

            if sentence_words:
                lines.append({
                    'sentence': ' '.join(w['text'] for w in sentence_words),
                    'words': sentence_words
                })

        return lines


def load_json_file(filepath: Path) -> Dict:
    """Load and parse a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_exercise_file(output_dir: Path, exercise_num: int, title: str,
                        description: str, lines: List[Dict]):
    """Write exercise data to JSONL file."""
    # Create filename from exercise number and title
    filename = f"{exercise_num:02d}-{title.lower().replace(' ', '_').replace('-', '_')}.jsonl"
    filepath = output_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        # Write metadata line
        metadata = {
            "_metadata": True,
            "title": title,
            "description": description
        }
        f.write(json.dumps(metadata) + '\n')

        # Write exercise lines
        for line in lines:
            f.write(json.dumps(line) + '\n')

    print(f"  ✅ {filename}")


def generate_series(vocab_file: Path, output_base: Path):
    """Generate complete 15-exercise series from vocabulary file."""

    print(f"\n📚 Generating exercise series from {vocab_file.name}...")

    # Load inputs
    vocab = load_json_file(vocab_file)
    templates = load_json_file(Path(__file__).parent / 'declension_templates.json')

    # Create series directory
    series_dir = output_base / vocab['series_name']
    series_dir.mkdir(parents=True, exist_ok=True)

    print(f"📁 Output directory: {series_dir}")
    print()

    # Write series metadata
    metadata = {
        "title": vocab['series_title'],
        "description": vocab['series_description'],
        "vocabulary": [f"{w['lemma']} ({w['meaning']})" for w in vocab['words']],
        "level": vocab['level']
    }

    metadata_file = series_dir / '.series-metadata.json'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"✅ .series-metadata.json")

    # Initialize components
    form_gen = FormGenerator(templates)
    builder = ExerciseBuilder(vocab, form_gen)

    # Exercise definitions
    exercises = [
        # Single declension (01-05)
        (1, "1st Declension", "Learn all 12 forms of 1st declension nouns",
         lambda: builder.build_single_declension('1st')),
        (2, "2nd Declension", "Learn all 12 forms of 2nd declension nouns",
         lambda: builder.build_single_declension('2nd')),
        (3, "3rd Declension", "Learn all 12 forms of 3rd declension nouns",
         lambda: builder.build_single_declension('3rd')),
        (4, "4th Declension", "Learn all 12 forms of 4th declension nouns",
         lambda: builder.build_single_declension('4th')),
        (5, "5th Declension", "Learn all 12 forms of 5th declension nouns",
         lambda: builder.build_single_declension('5th')),

        # Single case (06-11)
        (6, "Nominative Case", "Practice nominative (subject) across all declensions",
         lambda: builder.build_single_case('nominative')),
        (7, "Genitive Case", "Practice genitive (possession) across all declensions",
         lambda: builder.build_single_case('genitive')),
        (8, "Dative Case", "Practice dative (indirect object) across all declensions",
         lambda: builder.build_single_case('dative')),
        (9, "Accusative Case", "Practice accusative (direct object) across all declensions",
         lambda: builder.build_single_case('accusative')),
        (10, "Ablative Case", "Practice ablative (by/with/from) across all declensions",
         lambda: builder.build_single_case('ablative')),
        (11, "Vocative Case", "Practice vocative (direct address) across all declensions",
         lambda: builder.build_single_case('vocative')),

        # Single number (12-13)
        (12, "Singular Forms", "Practice all singular forms across declensions",
         lambda: builder.build_single_number('singular')),
        (13, "Plural Forms", "Practice all plural forms across declensions",
         lambda: builder.build_single_number('plural')),

        # Integration (14-15)
        (14, "Integration Practice", "Mixed forms for comprehensive practice",
         lambda: builder.build_integration()),
        (15, "Advanced Integration", "Advanced mixed forms drill",
         lambda: builder.build_integration())
    ]

    # Generate all exercises
    for num, title, description, build_func in exercises:
        lines = build_func()
        if lines:
            write_exercise_file(series_dir, num, title, description, lines)

    print()
    print(f"✅ Generated {series_dir.name} with 15 exercises")
    print(f"📊 Vocabulary: {len(vocab['words'])} words")
    print()


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate-vocabulary-exercises.py <vocabulary-file.json>")
        print()
        print("Example:")
        print("  python generate-vocabulary-exercises.py series-2-common-nouns.json")
        sys.exit(1)

    vocab_file = Path(sys.argv[1])

    if not vocab_file.exists():
        print(f"❌ Error: File not found: {vocab_file}")
        sys.exit(1)

    # Output to exercises/ directory
    output_base = Path(__file__).parent

    generate_series(vocab_file, output_base)


if __name__ == '__main__':
    main()
