#!/usr/bin/env python3
"""
Latin Keyboard Trainer - Vim-like interface for rapid grammatical analysis

Usage:
    python latin_keyboard_trainer.py

Keyboard commands:
    j/k         - Next/previous word
    Ctrl-1..9   - Jump to word N
    n/v/a/p     - Set POS (noun/verb/adj/prep)
    1-5         - Set declension (for nouns)
    Enter       - Check answers
    q           - Quit
"""

from blessed import Terminal
from cltk import NLP
import re

# Maps for user input → formal terms
POS_MAP = {
    'n': 'NOUN',
    'v': 'VERB',
    'a': 'ADJ',
    'p': 'ADP',  # Preposition/Adposition
    'c': 'CONJ',
    'd': 'ADV',
}

DECLENSION_MAP = {
    '1': '1st',
    '2': '2nd',
    '3': '3rd',
    '4': '4th',
    '5': '5th',
}

CASE_MAP = {
    'n': 'nominative',
    'g': 'genitive',
    'd': 'dative',
    'a': 'accusative',
    'b': 'ablative',
    'v': 'vocative',
}

TENSE_MAP = {
    'p': 'present',
    'i': 'imperfect',
    'f': 'future',
    'r': 'perfect',
}


class LatinKeyboardTrainer:
    def __init__(self):
        self.term = Terminal()
        self.nlp = NLP(language="lat", suppress_banner=True)
        self.current_word = 0
        self.user_answers = {}
        self.input_buffer = ""
        self.checked = False

    def parse_xpos(self, xpos, pos):
        """Extract grammatical info from XPOS codes"""
        result = {}

        if pos == 'NOUN':
            # Declension from first character
            decl_map = {'A': '1st', 'B': '2nd', 'C': '2nd/3rd', 'D': '4th', 'E': '5th'}
            result['declension'] = decl_map.get(xpos[0], 'unknown')

            # Case
            case_match = re.search(r'cas([A-Z])', xpos)
            if case_match:
                case_code = case_match.group(1)
                case_map_xpos = {
                    'A': 'nominative/accusative',
                    'F': 'ablative',
                    'G': 'genitive',
                    'D': 'dative',
                }
                result['case'] = case_map_xpos.get(case_code, 'unknown')

        elif pos == 'VERB':
            # Tense
            tense_match = re.search(r'tem(\d)', xpos)
            if tense_match:
                tense_code = tense_match.group(1)
                tense_map = {'1': 'present', '2': 'imperfect', '3': 'future', '4': 'perfect'}
                result['tense'] = tense_map.get(tense_code, 'unknown')

            # Person
            person_match = re.search(r'gen(\d)', xpos)
            if person_match:
                person_code = person_match.group(1)
                person_map = {'4': '1st', '5': '2nd', '6': '3rd'}
                result['person'] = person_map.get(person_code, 'unknown')

        return result

    def display(self, words, sentence):
        """Render the UI"""
        print(self.term.home + self.term.clear)

        # Title
        print(self.term.move_y(1) + self.term.center(
            self.term.bold("LATIN KEYBOARD TRAINER")
        ))

        # Sentence
        print(self.term.move_y(3) + self.term.center(
            self.term.italic(sentence)
        ))

        # Words with indices
        word_line = ""
        for i, w in enumerate(words):
            if i == self.current_word:
                word_line += self.term.bold_green(f"[{i+1}]{w.string} ")
            else:
                word_line += f"[{i+1}]{w.string} "

        print(self.term.move_y(5) + self.term.center(word_line))

        # Current word info
        current = words[self.current_word]
        print(self.term.move_y(7) + self.term.center(
            self.term.underline(f"Word {self.current_word + 1}: {current.string}")
        ))

        # User's input buffer
        if self.input_buffer:
            print(self.term.move_y(9) + self.term.center(
                f"Input: {self.term.yellow(self.input_buffer)}_"
            ))

        # User's completed answer
        if self.current_word in self.user_answers:
            ans = self.user_answers[self.current_word]
            answer_text = f"POS: {ans.get('pos', '?')}"
            if 'declension' in ans:
                answer_text += f" | Decl: {ans['declension']}"
            if 'tense' in ans:
                answer_text += f" | Tense: {ans['tense']}"

            print(self.term.move_y(11) + self.term.center(
                self.term.cyan(answer_text)
            ))

        # Results (if checked)
        if self.checked:
            self.display_results(words)

        # Instructions
        instructions = [
            "j/k: next/prev word | Ctrl-1..9: jump to word | q: quit",
            "n: noun | v: verb | a: adj | p: prep",
            "1-5: declension | Enter: check answers"
        ]

        for i, inst in enumerate(instructions):
            print(self.term.move_y(self.term.height - 4 + i) + self.term.center(
                self.term.dim(inst)
            ))

    def display_results(self, words):
        """Show validation results"""
        print(self.term.move_y(14) + self.term.center(
            self.term.bold("━" * 50)
        ))
        print(self.term.move_y(15) + self.term.center(
            self.term.bold("RESULTS")
        ))

        correct = 0
        total = 0

        for i, word in enumerate(words):
            if i not in self.user_answers:
                continue

            total += 1
            user_ans = self.user_answers[i]

            # Get correct answer
            correct_ans = {'pos': word.upos}
            if word.xpos:
                correct_ans.update(self.parse_xpos(word.xpos, word.upos))

            # Check if correct
            is_correct = user_ans.get('pos') == correct_ans.get('pos')

            if is_correct:
                correct += 1
                marker = self.term.green("✓")
            else:
                marker = self.term.red("✗")

            result_line = f"{marker} [{i+1}] {word.string}: {user_ans.get('pos', '?')}"
            if not is_correct:
                result_line += f" (expected: {correct_ans.get('pos')})"

            print(self.term.move_y(17 + i) + self.term.center(result_line))

        # Score
        if total > 0:
            score = (correct / total) * 100
            score_text = f"Score: {correct}/{total} ({score:.0f}%)"

            if score == 100:
                score_display = self.term.green_bold(score_text)
            elif score >= 75:
                score_display = self.term.yellow_bold(score_text)
            else:
                score_display = self.term.red_bold(score_text)

            print(self.term.move_y(17 + len(words) + 1) + self.term.center(score_display))

    def process_input(self, key):
        """Process user keyboard input"""

        # Navigation
        if key == 'j':
            self.current_word = min(self.current_word + 1, len(self.words) - 1)
            self.input_buffer = ""
        elif key == 'k':
            self.current_word = max(self.current_word - 1, 0)
            self.input_buffer = ""

        # POS input
        elif key in 'nvapcd':
            self.input_buffer = key
            # Auto-complete simple POS
            if key in ['p', 'c', 'd']:
                self.user_answers[self.current_word] = {
                    'pos': POS_MAP[key]
                }
                self.input_buffer = ""
                self.current_word = min(self.current_word + 1, len(self.words) - 1)

        # Declension input (after 'n' or 'a')
        elif key in '12345' and self.input_buffer in ['n', 'a']:
            self.user_answers[self.current_word] = {
                'pos': POS_MAP[self.input_buffer],
                'declension': DECLENSION_MAP[key]
            }
            self.input_buffer = ""
            self.current_word = min(self.current_word + 1, len(self.words) - 1)

        # Tense input (after 'v')
        elif key in 'pifr' and self.input_buffer == 'v':
            self.user_answers[self.current_word] = {
                'pos': POS_MAP['v'],
                'tense': TENSE_MAP[key]
            }
            self.input_buffer = ""
            self.current_word = min(self.current_word + 1, len(self.words) - 1)

        # Reset input
        elif key == 'u':
            self.input_buffer = ""
            if self.current_word in self.user_answers:
                del self.user_answers[self.current_word]

        return True

    def run(self, sentence):
        """Main training loop"""

        # Parse sentence
        doc = self.nlp.analyze(text=sentence)
        self.words = list(doc.words)

        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            while True:
                # Display UI
                self.display(self.words, sentence)

                # Get input
                key = self.term.inkey(timeout=0.1)

                if not key:
                    continue

                # Quit
                if key.lower() == 'q' and not self.input_buffer:
                    break

                # Check answers
                if key.name == 'KEY_ENTER':
                    self.checked = True
                    self.display(self.words, sentence)
                    # Wait for any key to continue
                    self.term.inkey()
                    break

                # Jump to word (Ctrl-1 through Ctrl-9)
                if key.code and 49 <= key.code <= 57:  # ASCII 1-9
                    # Check if Ctrl is pressed
                    word_num = key.code - 49  # Convert to 0-indexed
                    if word_num < len(self.words):
                        self.current_word = word_num
                        self.input_buffer = ""
                    continue

                # Process other input
                self.process_input(key)


def main():
    print("Loading CLTK Latin NLP pipeline...")
    print("(This may take a few seconds on first run)\n")

    trainer = LatinKeyboardTrainer()

    # Test sentences
    sentences = [
        "Puella in via ambulat",
        "Marcus librum legit",
        "Poeta carmina scribit",
    ]

    for sentence in sentences:
        print(f"\nTraining on: {sentence}")
        print("Press Enter to start...")
        input()  # Now it's clear you need to press Enter

        trainer.run(sentence)

        print("\nSentence complete!")
        print("Continue to next? (y/Enter): ", end="")
        response = input().lower()
        if response and response != 'y':
            break

    print("\nTraining session complete!")


if __name__ == "__main__":
    main()
