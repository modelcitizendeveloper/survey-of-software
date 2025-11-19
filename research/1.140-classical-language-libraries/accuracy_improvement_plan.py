#!/home/ivanadamin/spawn-solutions/research/1.140-classical-language-libraries/02-implementations/.venv/bin/python
"""
TDD Plan: Improve Latin parsing from 70% to 95%+ accuracy

Current PROIEL errors (30%):
1. Accusative -am forms → misidentified as verbs (nautam → navo)
2. Rare words not in corpus (pirata → piro)
3. Context-dependent ambiguities

Strategy:
1. Known-word database (500 common classical words)
2. Multi-parser voting (PROIEL + morphological analyzer)
3. Validation rules (catch impossible parses)
4. User feedback loop (learn from mistakes)
"""

import stanza
from cltk.morphology.lat import CollatinusDecliner

# Initialize parsers
nlp_proiel = stanza.Pipeline('la', package='proiel', processors='tokenize,pos,lemma',
                              verbose=False, logging_level='ERROR')
decliner = CollatinusDecliner()

print("="*80)
print("ACCURACY IMPROVEMENT ANALYSIS")
print("="*80)

# Analyze PROIEL errors from comprehensive test
errors = [
    ("nautam video", "nautam", "nauta", "NOUN", "navo", "VERB"),
    ("scribam video", "scribam", "scriba", "NOUN", "scribo", "VERB"),
    ("pirata navigat", "pirata", "pirata", "NOUN", "piratum", "NOUN"),
    ("piratae navis", "piratae", "pirata", "NOUN", "piror", "VERB"),
    ("piratam video", "piratam", "pirata", "NOUN", "piro", "VERB"),
    ("piratarum scelera", "piratarum", "pirata", "NOUN", "piratarus", "ADJ"),
]

print("\nCurrent PROIEL Errors (6/20 = 30%):")
print("-"*80)

for sentence, word, expected_lemma, expected_pos, actual_lemma, actual_pos in errors:
    print(f"\n❌ '{word}' in '{sentence}'")
    print(f"   Expected: {expected_lemma} ({expected_pos})")
    print(f"   Got:      {actual_lemma} ({actual_pos})")

# Categorize error types
print("\n" + "="*80)
print("ERROR PATTERN ANALYSIS")
print("="*80)

accusative_am_errors = [e for e in errors if e[1].endswith('am')]
rare_word_errors = [e for e in errors if 'pirat' in e[1]]

print(f"\n1. Accusative -am → VERB confusion: {len(accusative_am_errors)}/6 errors")
for e in accusative_am_errors:
    print(f"   - {e[1]} → {e[4]} (VERB)")

print(f"\n2. Rare words not in corpus: {len(rare_word_errors)}/6 errors")
for e in rare_word_errors:
    print(f"   - {e[1]} → {e[4]} ({e[5]})")

print("\n" + "="*80)
print("IMPROVEMENT STRATEGIES")
print("="*80)

print("""
Strategy 1: KNOWN-WORD DATABASE (easiest, biggest impact)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Manually curate 500-1000 most common classical Latin words.
For known words, override parser with correct declension.

Expected improvement: 70% → 85% (+15%)

Implementation:
- Use frequency lists from Caesar, Cicero, Virgil
- Store as JSON: {lemma: {declension, common_forms}}
- Check known words BEFORE parsing
- Fall back to PROIEL for unknown words

Example:
{
  "nauta": {
    "declension": "1st",
    "gender": "masculine",
    "forms": {
      "nauta": {"case": "nom/abl sg"},
      "nautae": {"case": "gen/dat sg, nom pl"},
      "nautam": {"case": "acc sg"},
      "nautarum": {"case": "gen pl"}
    }
  }
}
""")

print("""
Strategy 2: MORPHOLOGICAL ANALYZER VOTING (medium difficulty)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run multiple parsers and take majority vote:
- PROIEL (Stanza)
- Collatinus (CLTK morphological decliner)
- Rule-based validator

Expected improvement: 85% → 92% (+7%)

Implementation:
- Parse with PROIEL
- Validate with Collatinus (can word be declined?)
- Apply heuristic rules
- If disagreement, flag for manual review

Example:
  PROIEL:     nautam → navo (VERB)
  Collatinus: nautam → nauta (NOUN, accusative)
  Rule:       -am ending + no verb context → likely NOUN
  → Override to NOUN
""")

print("""
Strategy 3: VALIDATION RULES (easy, incremental)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Catch impossible/improbable parses:
- Two verbs in a row without conjunction
- Preposition followed by nominative
- Sentence with no verb
- -am ending identified as verb but no subject

Expected improvement: 92% → 95% (+3%)

Implementation:
- Post-process parsed sentence
- Check for structural violations
- Flag suspicious parses for review
- User can accept/reject suggestions
""")

print("""
Strategy 4: USER FEEDBACK LOOP (long-term)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Learn from user corrections:
- User marks wrong parse
- Store correction in database
- Use corrections to override future parses

Expected improvement: 95% → 99% (over time)

Implementation:
- Track all user corrections
- Build custom correction database
- Apply corrections before parsing
- Periodically review to add to known-word DB
""")

print("\n" + "="*80)
print("RECOMMENDED IMPLEMENTATION ORDER")
print("="*80)

print("""
Phase 1: KNOWN-WORD DATABASE (Week 1)
────────────────────────────────────
✓ Curate 100 most common classical words
✓ Implement lookup-before-parse
✓ Test on current 20-word corpus
✓ Target: 85% accuracy

Phase 2: MORPHOLOGICAL VALIDATION (Week 2)
───────────────────────────────────────────
✓ Integrate Collatinus decliner
✓ Implement voting mechanism
✓ Add -am accusative rule
✓ Target: 90% accuracy

Phase 3: VALIDATION RULES (Week 3)
───────────────────────────────────
✓ Implement structural validators
✓ Add confidence scoring
✓ Flag low-confidence parses
✓ Target: 95% accuracy

Phase 4: USER FEEDBACK (Ongoing)
─────────────────────────────────
✓ Add correction UI
✓ Store corrections in DB
✓ Apply corrections automatically
✓ Target: 99% accuracy (over time)
""")

print("\n" + "="*80)
print("NEXT STEPS")
print("="*80)

print("""
1. Create known_words.json with 100 common words
2. Implement KnownWordOverride class
3. Write TDD tests for known-word lookup
4. Measure accuracy improvement
5. Expand to 500 words
6. Move to Phase 2 (morphological voting)
""")
