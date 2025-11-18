#!/usr/bin/env python3
"""
Latin Keyboard Trainer - Simple Direct Launch

Just run and it starts immediately on first sentence.
"""

from blessed import Terminal
from cltk import NLP
import re

# Maps for user input → formal terms
POS_MAP = {
    'n': 'NOUN',
    'v': 'VERB',
    'a': 'ADJ',
    'p': 'ADP',
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
            decl_map = {'A': '1st', 'B': '2nd', 'C': '2nd/3rd', 'D': '4th', 'E': '5th'}
            result['declension'] = decl_map.get(xpos[0], 'unknown')

        elif pos == 'VERB':
            tense_match = re.search(r'tem(\d)', xpos)
            if tense_match:
                tense_code = tense_match.group(1)
                tense_map = {'1': 'present', '2': 'imperfect', '3': 'future', '4': 'perfect'}
                result['tense'] = tense_map.get(tense_code, 'unknown')

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
            "j/k: next/prev word | q: quit",
            "n: noun | v: verb | p: prep",
            "After n: 1-5 for declension | After v: p/i/f/r for tense",
            "Enter: check answers"
        ]

        for i, inst in enumerate(instructions):
            print(self.term.move_y(self.term.height - 5 + i) + self.term.center(inst))

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

            # Check if correct (just POS for now)
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

        print(self.term.move_y(self.term.height - 2) + self.term.center(
            "Press any key to exit..."
        ))

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
        elif key in 'nvap':
            self.input_buffer = key
            # Auto-complete simple POS
            if key == 'p':
                self.user_answers[self.current_word] = {
                    'pos': POS_MAP[key]
                }
                self.input_buffer = ""
                self.current_word = min(self.current_word + 1, len(self.words) - 1)

        # Declension input (after 'n')
        elif key in '12345' and self.input_buffer == 'n':
            self.user_answers[self.current_word] = {
                'pos': POS_MAP['n'],
                'declension': ['1st', '2nd', '3rd', '4th', '5th'][int(key)-1]
            }
            self.input_buffer = ""
            self.current_word = min(self.current_word + 1, len(self.words) - 1)

        # Tense input (after 'v')
        elif key in 'pifr' and self.input_buffer == 'v':
            tense_map = {'p': 'present', 'i': 'imperfect', 'f': 'future', 'r': 'perfect'}
            self.user_answers[self.current_word] = {
                'pos': POS_MAP['v'],
                'tense': tense_map[key]
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
        print("Parsing sentence...")
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

                # Process other input
                self.process_input(key)


if __name__ == "__main__":
    print("=" * 70)
    print("LATIN KEYBOARD TRAINER")
    print("=" * 70)
    print("\nLoading CLTK Latin NLP pipeline...")
    print("(This may take a few seconds)\n")

    trainer = LatinKeyboardTrainer()

    # Start with first sentence immediately
    sentence = "Puella in via ambulat"
    print(f"Sentence: {sentence}\n")

    trainer.run(sentence)

    print("\n" + "=" * 70)
    print("Training complete!")
    print("=" * 70)
