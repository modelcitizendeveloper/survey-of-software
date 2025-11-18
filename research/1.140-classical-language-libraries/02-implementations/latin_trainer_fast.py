#!/usr/bin/env python3
"""
Latin Keyboard Trainer - FAST VERSION

Optimizations:
- Pre-parse sentences at startup (once)
- Minimal screen redraws (no flicker)
- Use ADP → PREP for clarity
"""

from blessed import Terminal
from cltk import NLP
import re
import time

# Maps for user input → formal terms
POS_MAP = {
    'n': 'NOUN',
    'v': 'VERB',
    'a': 'ADJ',
    'p': 'PREP',  # Changed from ADP
}

# Reverse map for display
POS_DISPLAY = {
    'NOUN': 'NOUN',
    'VERB': 'VERB',
    'ADJ': 'ADJ',
    'ADP': 'PREP',  # Show PREP instead of ADP
    'PROPN': 'NOUN',  # Proper nouns count as nouns for learning
    'CONJ': 'CONJ',
    'ADV': 'ADV',
}


class LatinKeyboardTrainer:
    def __init__(self):
        self.term = Terminal()
        self.current_word = 0
        self.user_answers = {}
        self.input_buffer = ""
        self.checked = False
        self.last_display = None  # Cache last display to reduce flicker

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
        """Render the UI (with caching to reduce flicker)"""

        # Create display state
        state = (self.current_word, str(self.user_answers), self.input_buffer, self.checked)

        # Only redraw if state changed
        if state == self.last_display:
            return

        self.last_display = state

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
            correct_pos = POS_DISPLAY.get(word.upos, word.upos)  # Convert ADP → PREP
            correct_ans = {'pos': correct_pos}
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
            elif word.upos == 'PROPN':
                # Show that proper nouns are accepted as nouns
                result_line += " (proper noun)"

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

    def run(self, all_sentences):
        """Main training loop - handles all sentences in one fullscreen session"""

        sentence_idx = 0

        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            while sentence_idx < len(all_sentences):
                sentence, words = all_sentences[sentence_idx]
                self.words = words

                # Reset state for new sentence
                self.current_word = 0
                self.user_answers = {}
                self.input_buffer = ""
                self.checked = False
                self.last_display = None

                while True:
                    # Display UI
                    self.display(self.words, sentence)

                    # Get input (longer timeout to reduce CPU)
                    key = self.term.inkey(timeout=0.05)

                    if not key:
                        continue

                    # Quit
                    if key.lower() == 'q' and not self.input_buffer:
                        return  # Exit completely

                    # Check answers
                    if key.name == 'KEY_ENTER':
                        self.checked = True
                        self.last_display = None  # Force redraw
                        self.display(self.words, sentence)
                        # Wait for any key to continue
                        self.term.inkey()
                        # Move to next sentence (seamlessly)
                        sentence_idx += 1
                        break  # Break inner loop to load next sentence

                    # Process other input
                    self.process_input(key)


if __name__ == "__main__":
    print("=" * 70)
    print("LATIN KEYBOARD TRAINER (FAST VERSION)")
    print("=" * 70)
    print("\nLoading CLTK Latin NLP pipeline...")

    # Initialize NLP once
    nlp = NLP(language="lat", suppress_banner=True)

    # Pre-parse all sentences at startup
    sentences = [
        "Puella in via ambulat",
        "Marcus librum legit",
        "Poeta carmina scribit",
    ]

    print("Pre-parsing sentences (this happens once)...\n")

    parsed_sentences = []
    for i, sentence in enumerate(sentences, 1):
        print(f"  [{i}/{len(sentences)}] Parsing: {sentence}...")
        start = time.time()
        doc = nlp.analyze(text=sentence)
        elapsed = time.time() - start
        print(f"      → Done in {elapsed:.2f}s")
        parsed_sentences.append((sentence, list(doc.words)))

    print("\n✓ All sentences pre-parsed!")
    print("=" * 70)
    print("\nStarting trainer in 2 seconds...\n")
    time.sleep(2)

    trainer = LatinKeyboardTrainer()

    # Run all sentences in one seamless session
    trainer.run(parsed_sentences)

    print("\n" + "=" * 70)
    print("Training complete!")
    print("=" * 70)
