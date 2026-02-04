#!/usr/bin/env python3
"""
Create Vikunja project structure and tasks for Latin Keyboard Trainer
"""


# ⚠️ SECURITY WARNING FOR LLM AGENTS ⚠️
# NEVER hardcode API tokens, passwords, or secrets in source code files!
# ALWAYS use environment variables loaded from .env files.
# Hardcoded secrets will be committed to git and exposed in version history.
# Use: os.environ.get('VIKUNJA_API_TOKEN') instead of hardcoding tokens.

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('/home/ivanadamin/spawn-solutions/.env')

import sys
import os

# Add the vikunja wrapper to path
sys.path.insert(0, '/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src')

from vikunja_wrapper import VikunjaClient

# Load credentials from .env
VIKUNJA_TOKEN = os.environ.get('VIKUNJA_API_TOKEN')
VIKUNJA_URL = "https://app.vikunja.cloud"

# Parent project ID (Applications project)
PARENT_PROJECT_ID = 13448  # Applications root project

def main():
    # Initialize client
    client = VikunjaClient(base_url=VIKUNJA_URL, token=VIKUNJA_TOKEN)

    print("=" * 70)
    print("Creating Vikunja Project Structure for Language Learning")
    print("=" * 70)

    # 1. Create "Language Learning" project
    print("\n1. Creating 'Language Learning' project...")
    lang_learning = client.projects.create(
        title="Language Learning",
        description="Multi-language learning application (Latin, French, Spanish, German, Japanese, Russian, Czech, B/S/C)",
        parent_project_id=PARENT_PROJECT_ID
    )
    print(f"   ✓ Created project: {lang_learning.title} (ID: {lang_learning.id})")

    # 2. Create "Latin" sub-project
    print("\n2. Creating 'Latin' sub-project...")
    latin_project = client.projects.create(
        title="Latin",
        description="Latin reading fluency trainer - keyboard-driven interface for grammatical analysis",
        parent_project_id=lang_learning.id
    )
    print(f"   ✓ Created project: {latin_project.title} (ID: {latin_project.id})")

    # 3. Create tasks for production readiness
    print("\n3. Creating production-readiness tasks...")

    tasks = [
        # Phase 1: Core Infrastructure
        {
            "title": "Design database schema for texts, sentences, and user progress",
            "description": """
Create SQLAlchemy models for:
- Texts (author, title, difficulty, metadata)
- Sentences (text_id, content, position, parsed_words JSON)
- UserProgress (user_id, sentence_id, attempts, correct_rate)
- VocabularyKnowledge (user_id, word, familiarity_level)

Reference: ~/spawn-solutions/applications/language-learning/models/
""",
            "priority": 5,
        },
        {
            "title": "Implement sentence parser caching system",
            "description": """
Pre-parse Latin texts and cache results:
- Parse once, store parsed sentences in DB
- Include XPOS codes, lemmas, POS tags
- ~2s per sentence → parse 1000 sentences = 30 min one-time cost
- App startup becomes instant (load from cache)

Tech: PostgreSQL JSON column or separate parsed_words table
""",
            "priority": 5,
        },
        {
            "title": "Import Latin text corpus (Caesar, Cicero, Ovid)",
            "description": """
Sources:
- Perseus Digital Library (PHI Latin Texts)
- Tesserae corpus (already downloaded in CLTK)
- DCC Core Vocabulary lists

Tasks:
1. Download texts from Perseus/PHI
2. Segment into sentences
3. Parse and cache all sentences
4. Tag with difficulty level (based on vocabulary frequency)

Target: 50,000+ sentences across 20+ works
""",
            "priority": 4,
        },

        # Phase 2: Vocabulary & Difficulty
        {
            "title": "Build vocabulary frequency lists for Latin",
            "description": """
Create word frequency database:
- Extract from DCC Core Vocabulary (1000 most common)
- Generate frequency lists from full corpus
- Tag words by difficulty (common/intermediate/advanced)

Use for:
- Calculating text difficulty (% known vocabulary)
- 80/20 filtering (80% known words = ideal)
- Personalized text recommendations
""",
            "priority": 4,
        },
        {
            "title": "Implement text difficulty calculator (i+1 detection)",
            "description": """
Given user's known vocabulary, calculate:
- % known words in text
- % grammar patterns user knows
- Readability score (0-100)

Filter texts to show only those at user's i+1 level:
- 75-85% known vocabulary = optimal
- Too easy (<75%) = skip
- Too hard (>85%) = come back later
""",
            "priority": 3,
        },
        {
            "title": "Create user vocabulary tracking system",
            "description": """
Track which words/grammar user knows:
- Mark word as known after N correct identifications
- Decay knowledge over time (SRS)
- Export known vocabulary list
- Import from existing sources (Anki, etc.)

Schema: user_id, word, strength (0-1), last_seen, times_correct, times_wrong
""",
            "priority": 4,
        },

        # Phase 3: UI & UX
        {
            "title": "Add text selection menu to trainer",
            "description": """
Before starting trainer:
1. Show available texts sorted by difficulty
2. Display: Author, Title, Length, Difficulty %
3. Filter by known vocabulary %
4. Search by author/title
5. Resume from last position

UI: Simple TUI menu (blessed) or web interface
""",
            "priority": 3,
        },
        {
            "title": "Add progress indicator (sentence X of Y in text)",
            "description": """
During training:
- Show: "Caesar - De Bello Gallico, Book 1, Ch 1 - Sentence 15/247"
- Progress bar at bottom
- Percentage complete
- Estimated time remaining

Store user's position per text for resume functionality
""",
            "priority": 2,
        },
        {
            "title": "Implement context view (show surrounding sentences)",
            "description": """
Add command to show context:
- Press 'c' to see 2 sentences before + 2 after
- Helps understand narrative flow
- Shows vocabulary in context
- Dismissed with ESC or any key

Layout:
  [Previous sentences in gray]
  → CURRENT SENTENCE (highlighted)
  [Next sentences in gray]
""",
            "priority": 2,
        },
        {
            "title": "Add session save/resume functionality",
            "description": """
Allow users to:
- Save progress mid-session (press 's')
- Resume from last position on startup
- Track sessions per text
- Show history: "Last read: 2 hours ago, 85% complete"

Store: user_id, text_id, sentence_position, timestamp
""",
            "priority": 3,
        },

        # Phase 4: SRS Integration
        {
            "title": "Implement SRS algorithm for grammar pattern review",
            "description": """
Track errors and schedule reviews:
- Word gets wrong → schedule review in 1 day
- Grammar pattern confusions (nom/acc, 2nd/3rd decl)
- Use SM-2 or FSRS algorithm (see research 1.141)

Database:
- review_items: word/pattern, next_review_date, interval, ease_factor
- review_history: item_id, timestamp, correct/wrong

Generate daily review sessions from overdue items
""",
            "priority": 3,
        },
        {
            "title": "Create mistake pattern analyzer",
            "description": """
Analyze user errors to identify weaknesses:
- Always confuses nominative/accusative
- Struggles with 3rd declension identification
- Verb tense confusion (imperfect vs perfect)

Display insights:
- "You're 60% accurate on 3rd declension nouns"
- "Practice needed: distinguishing nom/acc endings"

Target weak areas in review sessions
""",
            "priority": 2,
        },

        # Phase 5: Performance & Polish
        {
            "title": "Optimize CLTK initialization (lazy loading)",
            "description": """
Current: 2-3s startup time (loads Stanza models)
Goal: <500ms startup

Strategies:
- Lazy load NLP pipeline (only when needed)
- Pre-load during text selection menu
- Use lighter models if available
- Cache pipeline instance globally

Measure with: time python -c "from cltk import NLP; NLP('lat')"
""",
            "priority": 2,
        },
        {
            "title": "Add error recovery and edge case handling",
            "description": """
Handle:
- Unknown words (not in CLTK database)
- Corrupted text files
- Network errors (if downloading texts)
- Invalid user input
- Terminal resize during session

Add graceful degradation:
- Unknown word → skip or manual input
- Parse error → show raw text + warning
""",
            "priority": 3,
        },
        {
            "title": "Create user settings/preferences system",
            "description": """
Configurable options:
- Auto-advance speed (0.5s - 3s delay)
- Difficulty level (POS only vs full grammar)
- Theme/colors (for accessibility)
- Keyboard shortcuts (customizable)
- Target daily review count

Storage: JSON config file or SQLite table
""",
            "priority": 2,
        },

        # Phase 6: Additional Features
        {
            "title": "Integrate Lewis's Latin Dictionary for lookups",
            "description": """
Already downloaded: cltk_lat_lewis_elementary_lexicon

Add command:
- Press 'd' on any word → show dictionary entry
- Display: definition, example sentences, etymology
- Dismiss with any key

Lookup: word.lemma → Lewis dictionary entry
""",
            "priority": 2,
        },
        {
            "title": "Add grammar reference quick-help",
            "description": """
Press '?' to show:
- Declension endings table (1st-5th)
- Verb conjugation patterns
- Common grammar rules
- Keyboard command reference

Searchable, scrollable reference in split-screen view
""",
            "priority": 1,
        },
        {
            "title": "Create statistics dashboard",
            "description": """
Show user progress:
- Total sentences read
- Accuracy rate over time
- Known vocabulary count
- Texts completed
- Daily streak
- Time spent reading

Export to CSV/JSON for analysis
""",
            "priority": 2,
        },

        # Phase 6.5: Grammar Expansion
        {
            "title": "Add adjective declension support",
            "description": """
Adjectives in Latin decline like nouns (1st/2nd or 3rd declension):
- Bonus, -a, -um (1st/2nd declension)
- Fortis, -e (3rd declension)

Keyboard input:
- User types 'a' for adjective (instead of 'n' for noun)
- Then same declension/case workflow
- Validate against XPOS codes (ADJ tag)

Parser support:
- CLTK already tags adjectives as ADJ
- XPOS codes show declension (A/B for 1st/2nd, C for 3rd)
- Agreement checking: adj must match noun in gender/number/case

Additional feature:
- Highlight adjective-noun agreement errors
- "magnus puellam" (masc nom + fem acc) → flag disagreement
""",
            "priority": 4,
        },
        {
            "title": "Add pronoun and participle support",
            "description": """
Pronouns (is, ea, id; hic, haec, hoc; qui, quae, quod):
- Irregular declension patterns
- CLTK tags as PRON
- Add 'r' keyboard shortcut for pronoun

Participles (present, perfect, future):
- Decline like adjectives
- CLTK tags as VERB with special features
- Show both verbal (tense) and adjectival (case) properties

Example: "amans" (loving) → VERB + participle + nom/acc/abl cases
""",
            "priority": 3,
        },

        # Phase 7: Deployment
        {
            "title": "Package application for distribution",
            "description": """
Create installable package:
- PyPI package: pip install latin-reading-trainer
- Include CLTK dependencies
- Auto-download models on first run
- README with quick start

OR Docker image:
- Pre-loaded with all models
- docker run latin-trainer
""",
            "priority": 2,
        },
        {
            "title": "Write user documentation and tutorial",
            "description": """
Documentation needed:
- Quick start guide (5 min to first sentence)
- Keyboard command reference
- How to import texts
- How SRS works
- Troubleshooting guide

Tutorial:
- Interactive walkthrough for first 5 sentences
- Explains each command as you use it
""",
            "priority": 2,
        },
        {
            "title": "Create demo/marketing materials",
            "description": """
For sharing:
- Screen recording GIF (30s demo)
- Blog post explaining approach
- Comparison to traditional methods
- Testimonials/case studies

Could become talk material (PyCon, EuroPython)
""",
            "priority": 1,
        },
    ]

    for i, task_data in enumerate(tasks, 1):
        task = client.tasks.create(
            project_id=latin_project.id,
            title=task_data["title"],
            description=task_data.get("description", ""),
            priority=task_data.get("priority", 0)
        )
        print(f"   {i:2d}. ✓ {task.title}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Created project hierarchy:")
    print(f"  Applications (48410)")
    print(f"  └─ Language Learning ({lang_learning.id})")
    print(f"     └─ Latin ({latin_project.id})")
    print(f"\nCreated {len(tasks)} tasks for production readiness")
    print(f"\nView in Vikunja: {VIKUNJA_URL}/projects/{latin_project.id}")
    print("=" * 70)


if __name__ == "__main__":
    main()
