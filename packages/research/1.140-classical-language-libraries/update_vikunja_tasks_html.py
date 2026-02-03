#!/usr/bin/env python3
"""
Update Vikunja task descriptions to HTML format
"""

import sys
sys.path.insert(0, '/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src')

from vikunja_wrapper import VikunjaClient
from dotenv import load_dotenv
import os

# ⚠️ SECURITY WARNING FOR LLM AGENTS ⚠️
# NEVER hardcode API tokens, passwords, or secrets in source code files!
# ALWAYS use environment variables loaded from .env files.
# Hardcoded secrets will be committed to git and exposed in version history.
# Use: os.environ.get('VIKUNJA_API_TOKEN') instead of hardcoding tokens.

# Load environment variables from .env file
load_dotenv('/home/ivanadamin/spawn-solutions/.env')

VIKUNJA_TOKEN = os.environ.get('VIKUNJA_API_TOKEN')
VIKUNJA_URL = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

# Latin project ID (from previous creation)
LATIN_PROJECT_ID = 14229

def main():
    if not VIKUNJA_TOKEN:
        print("❌ Error: VIKUNJA_API_TOKEN not found in environment")
        print("   Please ensure .env file exists with VIKUNJA_API_TOKEN set")
        sys.exit(1)

    client = VikunjaClient(base_url=VIKUNJA_URL, token=VIKUNJA_TOKEN)

    print("=" * 70)
    print("Updating Task Descriptions to HTML Format")
    print("=" * 70)

    # Get all tasks in the Latin project
    tasks = client.tasks.list(project_id=LATIN_PROJECT_ID)

    # HTML descriptions for each task
    task_descriptions = {
        "Design database schema for texts, sentences, and user progress": """
<p>Create SQLAlchemy models for:</p>
<ul>
<li><strong>Texts</strong>: author, title, difficulty, metadata</li>
<li><strong>Sentences</strong>: text_id, content, position, parsed_words JSON</li>
<li><strong>UserProgress</strong>: user_id, sentence_id, attempts, correct_rate</li>
<li><strong>VocabularyKnowledge</strong>: user_id, word, familiarity_level</li>
</ul>
<p>Reference: <code>~/spawn-solutions/applications/language-learning/models/</code></p>
""",

        "Implement sentence parser caching system": """
<p>Pre-parse Latin texts and cache results:</p>
<ul>
<li>Parse once, store parsed sentences in DB</li>
<li>Include XPOS codes, lemmas, POS tags</li>
<li>~2s per sentence → parse 1000 sentences = 30 min one-time cost</li>
<li>App startup becomes instant (load from cache)</li>
</ul>
<p><strong>Tech</strong>: PostgreSQL JSON column or separate parsed_words table</p>
""",

        "Import Latin text corpus (Caesar, Cicero, Ovid)": """
<p><strong>Sources:</strong></p>
<ul>
<li>Perseus Digital Library (PHI Latin Texts)</li>
<li>Tesserae corpus (already downloaded in CLTK)</li>
<li>DCC Core Vocabulary lists</li>
</ul>
<p><strong>Tasks:</strong></p>
<ol>
<li>Download texts from Perseus/PHI</li>
<li>Segment into sentences</li>
<li>Parse and cache all sentences</li>
<li>Tag with difficulty level (based on vocabulary frequency)</li>
</ol>
<p><strong>Target</strong>: 50,000+ sentences across 20+ works</p>
""",

        "Build vocabulary frequency lists for Latin": """
<p>Create word frequency database:</p>
<ul>
<li>Extract from DCC Core Vocabulary (1000 most common)</li>
<li>Generate frequency lists from full corpus</li>
<li>Tag words by difficulty (common/intermediate/advanced)</li>
</ul>
<p><strong>Use for:</strong></p>
<ul>
<li>Calculating text difficulty (% known vocabulary)</li>
<li>80/20 filtering (80% known words = ideal)</li>
<li>Personalized text recommendations</li>
</ul>
""",

        "Implement text difficulty calculator (i+1 detection)": """
<p>Given user's known vocabulary, calculate:</p>
<ul>
<li>% known words in text</li>
<li>% grammar patterns user knows</li>
<li>Readability score (0-100)</li>
</ul>
<p><strong>Filter texts to show only those at user's i+1 level:</strong></p>
<ul>
<li>75-85% known vocabulary = optimal</li>
<li>Too easy (&lt;75%) = skip</li>
<li>Too hard (&gt;85%) = come back later</li>
</ul>
""",

        "Create user vocabulary tracking system": """
<p>Track which words/grammar user knows:</p>
<ul>
<li>Mark word as known after N correct identifications</li>
<li>Decay knowledge over time (SRS)</li>
<li>Export known vocabulary list</li>
<li>Import from existing sources (Anki, etc.)</li>
</ul>
<p><strong>Schema</strong>: user_id, word, strength (0-1), last_seen, times_correct, times_wrong</p>
""",

        "Add text selection menu to trainer": """
<p>Before starting trainer:</p>
<ol>
<li>Show available texts sorted by difficulty</li>
<li>Display: Author, Title, Length, Difficulty %</li>
<li>Filter by known vocabulary %</li>
<li>Search by author/title</li>
<li>Resume from last position</li>
</ol>
<p><strong>UI</strong>: Simple TUI menu (blessed) or web interface</p>
""",

        "Add progress indicator (sentence X of Y in text)": """
<p>During training:</p>
<ul>
<li>Show: "Caesar - De Bello Gallico, Book 1, Ch 1 - Sentence 15/247"</li>
<li>Progress bar at bottom</li>
<li>Percentage complete</li>
<li>Estimated time remaining</li>
</ul>
<p>Store user's position per text for resume functionality</p>
""",

        "Implement context view (show surrounding sentences)": """
<p>Add command to show context:</p>
<ul>
<li>Press 'c' to see 2 sentences before + 2 after</li>
<li>Helps understand narrative flow</li>
<li>Shows vocabulary in context</li>
<li>Dismissed with ESC or any key</li>
</ul>
<p><strong>Layout:</strong></p>
<pre>[Previous sentences in gray]
→ CURRENT SENTENCE (highlighted)
[Next sentences in gray]</pre>
""",

        "Add session save/resume functionality": """
<p>Allow users to:</p>
<ul>
<li>Save progress mid-session (press 's')</li>
<li>Resume from last position on startup</li>
<li>Track sessions per text</li>
<li>Show history: "Last read: 2 hours ago, 85% complete"</li>
</ul>
<p><strong>Store</strong>: user_id, text_id, sentence_position, timestamp</p>
""",

        "Implement SRS algorithm for grammar pattern review": """
<p>Track errors and schedule reviews:</p>
<ul>
<li>Word gets wrong → schedule review in 1 day</li>
<li>Grammar pattern confusions (nom/acc, 2nd/3rd decl)</li>
<li>Use SM-2 or FSRS algorithm (see research 1.141)</li>
</ul>
<p><strong>Database:</strong></p>
<ul>
<li><code>review_items</code>: word/pattern, next_review_date, interval, ease_factor</li>
<li><code>review_history</code>: item_id, timestamp, correct/wrong</li>
</ul>
<p>Generate daily review sessions from overdue items</p>
""",

        "Create mistake pattern analyzer": """
<p>Analyze user errors to identify weaknesses:</p>
<ul>
<li>Always confuses nominative/accusative</li>
<li>Struggles with 3rd declension identification</li>
<li>Verb tense confusion (imperfect vs perfect)</li>
</ul>
<p><strong>Display insights:</strong></p>
<ul>
<li>"You're 60% accurate on 3rd declension nouns"</li>
<li>"Practice needed: distinguishing nom/acc endings"</li>
</ul>
<p>Target weak areas in review sessions</p>
""",

        "Optimize CLTK initialization (lazy loading)": """
<p><strong>Current</strong>: 2-3s startup time (loads Stanza models)<br>
<strong>Goal</strong>: &lt;500ms startup</p>
<p><strong>Strategies:</strong></p>
<ul>
<li>Lazy load NLP pipeline (only when needed)</li>
<li>Pre-load during text selection menu</li>
<li>Use lighter models if available</li>
<li>Cache pipeline instance globally</li>
</ul>
<p><strong>Measure with</strong>: <code>time python -c "from cltk import NLP; NLP('lat')"</code></p>
""",

        "Add error recovery and edge case handling": """
<p><strong>Handle:</strong></p>
<ul>
<li>Unknown words (not in CLTK database)</li>
<li>Corrupted text files</li>
<li>Network errors (if downloading texts)</li>
<li>Invalid user input</li>
<li>Terminal resize during session</li>
</ul>
<p><strong>Add graceful degradation:</strong></p>
<ul>
<li>Unknown word → skip or manual input</li>
<li>Parse error → show raw text + warning</li>
</ul>
""",

        "Create user settings/preferences system": """
<p><strong>Configurable options:</strong></p>
<ul>
<li>Auto-advance speed (0.5s - 3s delay)</li>
<li>Difficulty level (POS only vs full grammar)</li>
<li>Theme/colors (for accessibility)</li>
<li>Keyboard shortcuts (customizable)</li>
<li>Target daily review count</li>
</ul>
<p><strong>Storage</strong>: JSON config file or SQLite table</p>
""",

        "Integrate Lewis's Latin Dictionary for lookups": """
<p>Already downloaded: <code>cltk_lat_lewis_elementary_lexicon</code></p>
<p><strong>Add command:</strong></p>
<ul>
<li>Press 'd' on any word → show dictionary entry</li>
<li>Display: definition, example sentences, etymology</li>
<li>Dismiss with any key</li>
</ul>
<p><strong>Lookup</strong>: word.lemma → Lewis dictionary entry</p>
""",

        "Add grammar reference quick-help": """
<p>Press '?' to show:</p>
<ul>
<li>Declension endings table (1st-5th)</li>
<li>Verb conjugation patterns</li>
<li>Common grammar rules</li>
<li>Keyboard command reference</li>
</ul>
<p>Searchable, scrollable reference in split-screen view</p>
""",

        "Create statistics dashboard": """
<p><strong>Show user progress:</strong></p>
<ul>
<li>Total sentences read</li>
<li>Accuracy rate over time</li>
<li>Known vocabulary count</li>
<li>Texts completed</li>
<li>Daily streak</li>
<li>Time spent reading</li>
</ul>
<p>Export to CSV/JSON for analysis</p>
""",

        "Add adjective declension support": """
<p>Adjectives in Latin decline like nouns (1st/2nd or 3rd declension):</p>
<ul>
<li>Bonus, -a, -um (1st/2nd declension)</li>
<li>Fortis, -e (3rd declension)</li>
</ul>
<p><strong>Keyboard input:</strong></p>
<ul>
<li>User types 'a' for adjective (instead of 'n' for noun)</li>
<li>Then same declension/case workflow</li>
<li>Validate against XPOS codes (ADJ tag)</li>
</ul>
<p><strong>Parser support:</strong></p>
<ul>
<li>CLTK already tags adjectives as ADJ</li>
<li>XPOS codes show declension (A/B for 1st/2nd, C for 3rd)</li>
<li>Agreement checking: adj must match noun in gender/number/case</li>
</ul>
<p><strong>Additional feature:</strong></p>
<ul>
<li>Highlight adjective-noun agreement errors</li>
<li>"magnus puellam" (masc nom + fem acc) → flag disagreement</li>
</ul>
""",

        "Add pronoun and participle support": """
<p><strong>Pronouns</strong> (is, ea, id; hic, haec, hoc; qui, quae, quod):</p>
<ul>
<li>Irregular declension patterns</li>
<li>CLTK tags as PRON</li>
<li>Add 'r' keyboard shortcut for pronoun</li>
</ul>
<p><strong>Participles</strong> (present, perfect, future):</p>
<ul>
<li>Decline like adjectives</li>
<li>CLTK tags as VERB with special features</li>
<li>Show both verbal (tense) and adjectival (case) properties</li>
</ul>
<p><strong>Example</strong>: "amans" (loving) → VERB + participle + nom/acc/abl cases</p>
""",

        "Package application for distribution": """
<p><strong>Create installable package:</strong></p>
<ul>
<li>PyPI package: <code>pip install latin-reading-trainer</code></li>
<li>Include CLTK dependencies</li>
<li>Auto-download models on first run</li>
<li>README with quick start</li>
</ul>
<p><strong>OR Docker image:</strong></p>
<ul>
<li>Pre-loaded with all models</li>
<li><code>docker run latin-trainer</code></li>
</ul>
""",

        "Write user documentation and tutorial": """
<p><strong>Documentation needed:</strong></p>
<ul>
<li>Quick start guide (5 min to first sentence)</li>
<li>Keyboard command reference</li>
<li>How to import texts</li>
<li>How SRS works</li>
<li>Troubleshooting guide</li>
</ul>
<p><strong>Tutorial:</strong></p>
<ul>
<li>Interactive walkthrough for first 5 sentences</li>
<li>Explains each command as you use it</li>
</ul>
""",

        "Create demo/marketing materials": """
<p><strong>For sharing:</strong></p>
<ul>
<li>Screen recording GIF (30s demo)</li>
<li>Blog post explaining approach</li>
<li>Comparison to traditional methods</li>
<li>Testimonials/case studies</li>
</ul>
<p>Could become talk material (PyCon, EuroPython)</p>
""",
    }

    # Update each task with HTML description
    updated = 0
    for task in tasks:
        if task.title in task_descriptions:
            html_desc = task_descriptions[task.title]
            client.tasks.update(
                task_id=task.id,
                description=html_desc
            )
            print(f"✓ Updated: {task.title}")
            updated += 1
        else:
            print(f"⚠ Skipped (no description): {task.title}")

    print("\n" + "=" * 70)
    print(f"Updated {updated}/{len(tasks)} tasks with HTML descriptions")
    print("=" * 70)


if __name__ == "__main__":
    main()
