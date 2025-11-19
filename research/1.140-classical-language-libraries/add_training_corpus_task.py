#!/usr/bin/env python3
"""
Add training corpus task to Vikunja Latin project
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
sys.path.insert(0, '/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src')

from vikunja_wrapper import VikunjaClient

VIKUNJA_TOKEN = os.environ.get('VIKUNJA_API_TOKEN')
VIKUNJA_URL = "https://app.vikunja.cloud"
LATIN_PROJECT_ID = 14229

def main():
    client = VikunjaClient(base_url=VIKUNJA_URL, token=VIKUNJA_TOKEN)

    print("=" * 70)
    print("Adding Training Corpus Task")
    print("=" * 70)

    description = """
<h2>Structured Training Curriculum</h2>

<p>Create a progressive training corpus that systematically teaches Latin grammar patterns, starting from basics and building to complex constructions.</p>

<h3>🎯 Learning Progression</h3>

<h4>Phase 1: Case Training (Nouns Only)</h4>
<p>Introduce one case at a time with simple sentences:</p>

<ol>
<li><strong>Nominative Only</strong> (Subject)
<ul>
<li>"Puella est" (The girl is)</li>
<li>"Marcus ambulat" (Marcus walks)</li>
<li>"Poeta scribit" (The poet writes)</li>
<li>10-15 sentences, 1st/2nd declension only</li>
</ul>
</li>

<li><strong>Nominative + Accusative</strong> (Subject + Direct Object)
<ul>
<li>"Puella rosam amat" (The girl loves the rose)</li>
<li>"Marcus librum legit" (Marcus reads the book)</li>
<li>"Poeta carmina scribit" (The poet writes poems)</li>
<li>20-30 sentences, introduce verb transitivity</li>
</ul>
</li>

<li><strong>Add Genitive</strong> (Possession)
<ul>
<li>"Puella rosam poetae amat" (The girl loves the poet's rose)</li>
<li>"Liber Marci magnus est" (Marcus's book is large)</li>
<li>15-20 sentences, genitive case patterns</li>
</ul>
</li>

<li><strong>Add Dative</strong> (Indirect Object)
<ul>
<li>"Puella poetae rosam dat" (The girl gives a rose to the poet)</li>
<li>"Marcus amico librum mittit" (Marcus sends a book to his friend)</li>
<li>15-20 sentences, dative verbs (do, mitto, etc.)</li>
</ul>
</li>

<li><strong>Add Ablative</strong> (Instrumental, Locative)
<ul>
<li>"Puella in via ambulat" (The girl walks in the street)</li>
<li>"Marcus gladio pugnat" (Marcus fights with a sword)</li>
<li>20-25 sentences, ablative uses</li>
</ul>
</li>

<li><strong>Add Vocative</strong> (Direct Address)
<ul>
<li>"Ave, Marce!" (Hello, Marcus!)</li>
<li>"Salve, amice!" (Greetings, friend!)</li>
<li>5-10 sentences, vocative patterns</li>
</ul>
</li>
</ol>

<h4>Phase 2: Verb Tense Training</h4>
<p>Introduce tenses progressively with previously learned cases:</p>

<ol>
<li><strong>Present Tense Only</strong>
<ul>
<li>All 1st conjugation: amo, porto, laboro</li>
<li>30-40 sentences reinforcing case knowledge</li>
</ul>
</li>

<li><strong>Add Imperfect</strong>
<ul>
<li>"Puella ambulabat" (The girl was walking)</li>
<li>"Marcus legebat" (Marcus was reading)</li>
<li>20-30 sentences, past continuous actions</li>
</ul>
</li>

<li><strong>Add Future</strong>
<ul>
<li>"Puella ambulabit" (The girl will walk)</li>
<li>"Marcus leget" (Marcus will read)</li>
<li>20-30 sentences, future actions</li>
</ul>
</li>

<li><strong>Add Perfect</strong>
<ul>
<li>"Puella ambulavit" (The girl walked)</li>
<li>"Marcus legit" (Marcus read)</li>
<li>25-35 sentences, completed actions</li>
</ul>
</li>

<li><strong>Add Pluperfect</strong>
<ul>
<li>"Puella ambulaverat" (The girl had walked)</li>
<li>15-20 sentences, past perfect</li>
</ul>
</li>

<li><strong>Add Future Perfect</strong>
<ul>
<li>"Puella ambulaverit" (The girl will have walked)</li>
<li>10-15 sentences, future perfect</li>
</ul>
</li>
</ol>

<h4>Phase 3: Preposition Patterns</h4>
<p>Systematically teach preposition + case combinations:</p>

<ul>
<li><strong>+ Accusative Only</strong>
<ul>
<li><code>ad</code> (to, toward): "Marcus ad urbem ambulat"</li>
<li><code>per</code> (through): "Puella per viam ambulat"</li>
<li><code>trans</code> (across): "Marcus trans flumen natat"</li>
<li><code>ante</code> (before): "Stat ante portam"</li>
<li><code>post</code> (after): "Post bellum venit"</li>
<li>15 sentences per preposition = 75 sentences</li>
</ul>
</li>

<li><strong>+ Ablative Only</strong>
<ul>
<li><code>a/ab</code> (from, by): "Ab urbe venit"</li>
<li><code>cum</code> (with): "Cum amico ambulat"</li>
<li><code>de</code> (about, from): "De bello scribit"</li>
<li><code>e/ex</code> (out of): "Ex silva exit"</li>
<li><code>sine</code> (without): "Sine gladio pugnat"</li>
<li>15 sentences per preposition = 75 sentences</li>
</ul>
</li>

<li><strong>+ Accusative OR Ablative (Motion vs Location)</strong>
<ul>
<li><code>in</code> + acc (into): "In urbem ambulat" (motion toward)</li>
<li><code>in</code> + abl (in): "In urbe est" (location)</li>
<li><code>sub</code> + acc (under - motion): "Sub aquam cadit"</li>
<li><code>sub</code> + abl (under - location): "Sub arbore sedet"</li>
<li>20 sentences each = 40 sentences</li>
</ul>
</li>
</ul>

<h4>Phase 4: Declension-Specific Training</h4>

<ol>
<li><strong>1st Declension Mastery</strong>
<ul>
<li>50 sentences using common 1st declension nouns</li>
<li>puella, via, terra, aqua, silva, porta, villa</li>
<li>All six cases in various contexts</li>
</ul>
</li>

<li><strong>2nd Declension (Masculine)</strong>
<ul>
<li>50 sentences: dominus, filius, amicus, servus, populus</li>
<li>Focus on -us nominative, -i genitive pattern</li>
</ul>
</li>

<li><strong>2nd Declension (Neuter)</strong>
<ul>
<li>40 sentences: templum, bellum, oppidum, regnum</li>
<li>Emphasize nom/acc same form</li>
</ul>
</li>

<li><strong>3rd Declension (Consonant Stems)</strong>
<ul>
<li>60 sentences: rex, miles, dux, pater, homo, nomen</li>
<li>Various stem types (x, t, n endings)</li>
<li>Hardest declension - more practice needed</li>
</ul>
</li>

<li><strong>3rd Declension (i-stems)</strong>
<ul>
<li>40 sentences: civis, hostis, navis, mare</li>
<li>Distinguish i-stem patterns from consonant stems</li>
</ul>
</li>

<li><strong>4th Declension</strong>
<ul>
<li>30 sentences: manus, cornu, exercitus, domus (irregular)</li>
<li>Less common - fewer sentences needed</li>
</ul>
</li>

<li><strong>5th Declension</strong>
<ul>
<li>25 sentences: res, dies, spes</li>
<li>Rare declension - focus on most common words</li>
</ul>
</li>
</ol>

<h4>Phase 5: Adjective Agreement</h4>

<ul>
<li><strong>1st/2nd Declension Adjectives</strong>
<ul>
<li>"Puella bona est" (The good girl)</li>
<li>"Magnus liber" (The large book)</li>
<li>30 sentences, adjective-noun agreement</li>
</ul>
</li>

<li><strong>3rd Declension Adjectives</strong>
<ul>
<li>"Fortis miles" (The brave soldier)</li>
<li>"Omnes puellae" (All the girls)</li>
<li>30 sentences, 3-termination, 2-termination, 1-termination</li>
</ul>
</li>

<li><strong>Agreement Challenges</strong>
<ul>
<li>Mixed declensions: "Puella bona librum magnum legit"</li>
<li>20 sentences deliberately testing agreement rules</li>
</ul>
</li>
</ul>

<h4>Phase 6: Conjugation Practice</h4>

<ol>
<li><strong>1st Conjugation</strong>: amo, porto, laboro (40 sentences)</li>
<li><strong>2nd Conjugation</strong>: moneo, video,habeo (40 sentences)</li>
<li><strong>3rd Conjugation</strong>: mitto, duco, scribo (50 sentences - irregular)</li>
<li><strong>3rd -io Conjugation</strong>: capio, facio (30 sentences)</li>
<li><strong>4th Conjugation</strong>: audio, venio (30 sentences)</li>
</ol>

<h4>Phase 7: Irregular Verbs</h4>

<ul>
<li><code>sum, esse</code> (to be): 30 sentences, all tenses</li>
<li><code>possum, posse</code> (to be able): 25 sentences</li>
<li><code>eo, ire</code> (to go): 25 sentences</li>
<li><code>fero, ferre</code> (to carry): 20 sentences</li>
<li><code>volo, velle</code> (to want): 20 sentences</li>
<li><code>nolo, nolle</code> (to not want): 15 sentences</li>
<li><code>malo, malle</code> (to prefer): 15 sentences</li>
</ul>

<h3>📊 Corpus Statistics</h3>

<table>
<tr><th>Phase</th><th>Sentences</th><th>Cumulative</th></tr>
<tr><td>1. Case Training</td><td>~100</td><td>100</td></tr>
<tr><td>2. Verb Tenses</td><td>~150</td><td>250</td></tr>
<tr><td>3. Prepositions</td><td>~190</td><td>440</td></tr>
<tr><td>4. Declensions</td><td>~295</td><td>735</td></tr>
<tr><td>5. Adjectives</td><td>~80</td><td>815</td></tr>
<tr><td>6. Conjugations</td><td>~190</td><td>1005</td></tr>
<tr><td>7. Irregulars</td><td>~150</td><td>1155</td></tr>
</table>

<p><strong>Total Training Corpus: ~1,200 sentences</strong></p>

<h3>🔧 Implementation</h3>

<h4>1. Database Schema</h4>
<pre>
CREATE TABLE training_sentences (
  id SERIAL PRIMARY KEY,
  phase VARCHAR(50),      -- 'case_training', 'verb_tenses', etc.
  level INT,              -- 1-7 within phase
  sentence TEXT,
  translation TEXT,
  focus VARCHAR(100),     -- 'nominative', 'in+abl', '3rd_decl', etc.
  difficulty INT,         -- 1-5
  parsed_words JSONB,     -- Pre-parsed CLTK data
  position INT            -- Order within level
);
</pre>

<h4>2. Progress Tracking</h4>
<pre>
CREATE TABLE user_training_progress (
  user_id INT,
  phase VARCHAR(50),
  level INT,
  sentences_completed INT,
  sentences_total INT,
  accuracy_rate FLOAT,
  last_practiced TIMESTAMP,
  PRIMARY KEY (user_id, phase, level)
);
</pre>

<h4>3. UI Flow</h4>
<ul>
<li>User starts trainer</li>
<li>Choose: "Training Mode" or "Free Reading"</li>
<li>Training Mode shows current phase/level</li>
<li>Progress bar: "Case Training - Nominative Only (5/15)"</li>
<li>Unlock next level after 80% accuracy</li>
<li>Can replay any completed level</li>
</ul>

<h4>4. Sentence Generation</h4>
<ul>
<li><strong>Manual curation</strong>: Write sentences by hand (best quality)</li>
<li><strong>Template-based</strong>: "NOUN(nom) VERB NOUN(acc)" → fill with vocabulary</li>
<li><strong>Hybrid</strong>: Templates + manual review for naturalness</li>
</ul>

<h4>5. Vocabulary Control</h4>
<ul>
<li>Use only DCC Core 300 words for first 500 sentences</li>
<li>Gradually expand to Core 1000</li>
<li>Avoid rare/archaic words in training mode</li>
<li>Ensure high-frequency, useful vocabulary</li>
</ul>

<h3>✅ Deliverables</h3>

<ol>
<li>1,200 training sentences in YAML/JSON format</li>
<li>Database schema and migration scripts</li>
<li>Training mode UI in keyboard trainer</li>
<li>Progress tracking and level unlock logic</li>
<li>Admin interface to add/edit training sentences</li>
<li>Export to Anki/flashcard format (bonus)</li>
</ol>

<h3>🎓 Pedagogical Benefits</h3>

<ul>
<li><strong>Progressive difficulty</strong>: Never overwhelmed</li>
<li><strong>Systematic coverage</strong>: No grammar gaps</li>
<li><strong>Immediate application</strong>: Learn-by-doing</li>
<li><strong>Spaced repetition</strong>: Built into level structure</li>
<li><strong>Confidence building</strong>: Early wins with simple patterns</li>
<li><strong>Natural transition</strong>: Training mode → real texts</li>
</ul>

<h3>📚 Reference Materials</h3>

<ul>
<li><strong>Wheelock's Latin</strong>: Chapter progression model</li>
<li><strong>Lingua Latina</strong>: Natural method sentences</li>
<li><strong>DCC Core Vocabulary</strong>: Word frequency data</li>
<li><strong>Cambridge Latin Course</strong>: Graded reader approach</li>
</ul>

<h3>⏱️ Estimated Time</h3>

<ul>
<li>Sentence writing: 40-60 hours (1-2 min per sentence)</li>
<li>CLTK parsing: 30 min (automated)</li>
<li>Database setup: 2-3 hours</li>
<li>UI integration: 4-6 hours</li>
<li><strong>Total: ~50-70 hours</strong></li>
</ul>

<p><em>This becomes the foundation for the entire learning experience!</em></p>
"""

    task = client.tasks.create(
        project_id=LATIN_PROJECT_ID,
        title="Create progressive training corpus (1200+ sentences)",
        description=description,
        priority=5  # Highest priority - foundational
    )

    print(f"\n✓ Created task: {task.title}")
    print(f"  Priority: {task.priority}")
    print(f"  Project: Latin ({LATIN_PROJECT_ID})")
    print(f"  URL: {VIKUNJA_URL}/tasks/{task.id}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
