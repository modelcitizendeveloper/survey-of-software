#!/usr/bin/env python3
"""
Add fill-in-the-blank production mode task to Vikunja
"""

import sys
sys.path.insert(0, '/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src')

from vikunja_wrapper import VikunjaClient

VIKUNJA_TOKEN = "tk_0dcac3c3c8ebf9f3c8e832b7576bb59835e3ebc3"
VIKUNJA_URL = "https://app.vikunja.cloud"
LATIN_PROJECT_ID = 14229

def main():
    client = VikunjaClient(base_url=VIKUNJA_URL, token=VIKUNJA_TOKEN)

    description = """
<h2>Fill-in-the-Blank Production Mode</h2>

<p>Complement the recognition trainer with a <strong>production mode</strong> where users generate the correct form from prompts.</p>

<h3>🎯 Two Modes of Learning</h3>

<table>
<tr>
<th>Recognition Mode (Current)</th>
<th>Production Mode (New)</th>
</tr>
<tr>
<td>See "puellam" → identify "accusative"</td>
<td>See "puella, accusative singular" → type "puellam"</td>
</tr>
<tr>
<td>Passive recall (easier)</td>
<td>Active recall (harder, more effective)</td>
</tr>
<tr>
<td>Reading skill</td>
<td>Writing skill</td>
</tr>
</table>

<h3>📝 Exercise Types</h3>

<h4>1. Case Fill-in-the-Blank</h4>

<p><strong>Prompt:</strong></p>
<pre>Dictionary form: puella, -ae (f)
Needed: accusative singular

Type the correct form: ________</pre>

<p><strong>Answer:</strong> <code>puellam</code></p>

<h4>2. Verb Conjugation Fill-in-the-Blank</h4>

<p><strong>Prompt:</strong></p>
<pre>Dictionary form: amo, amare, amavi, amatus
Needed: 3rd person singular, present, indicative

Type the correct form: ________</pre>

<p><strong>Answer:</strong> <code>amat</code></p>

<h4>3. Sentence Completion</h4>

<p><strong>Prompt:</strong></p>
<pre>Puella in via ________.
          (ambulare, 3rd sg present)

Type the verb: ________</pre>

<p><strong>Answer:</strong> <code>ambulat</code></p>

<h4>4. Ending-Only Mode</h4>

<p><strong>Prompt:</strong></p>
<pre>puell_____ (accusative singular)

Type the ending: ________</pre>

<p><strong>Answer:</strong> <code>-am</code> or <code>am</code></p>

<p><em>Focuses purely on pattern recognition, not spelling</em></p>

<h3>⌨️ Keyboard Interface</h3>

<p><strong>Exercise Screen:</strong></p>
<pre>┌────────────────────────────────────────────────────┐
│ LATIN FILL-IN-THE-BLANK TRAINER                   │
├────────────────────────────────────────────────────┤
│                                                    │
│ Dictionary form: puella, -ae (f)                   │
│ Declension: 1st                                    │
│                                                    │
│ Generate: accusative singular                      │
│                                                    │
│ Your answer: [puellam____________]                 │
│                                                    │
│ Press Enter to check                               │
│ Press Tab for hint                                 │
│                                                    │
├────────────────────────────────────────────────────┤
│ Progress: 5/20 | Accuracy: 80% | Streak: 3         │
└────────────────────────────────────────────────────┘</pre>

<h3>💡 Hint System</h3>

<p>Press <code>Tab</code> for progressive hints:</p>

<ol>
<li><strong>First hint:</strong> "Think about the ending for accusative singular in 1st declension"</li>
<li><strong>Second hint:</strong> "It starts with 'puell-'"</li>
<li><strong>Third hint:</strong> "puell__ (2 letters needed)"</li>
<li><strong>Final hint:</strong> "p u e l l a m" (reveal one letter at a time)</li>
</ol>

<p>Hints reduce points earned (encourages trying without help)</p>

<h3>✅ Answer Validation</h3>

<h4>Exact Match</h4>
<ul><li>User: "puellam" → ✓ Correct!</li></ul>

<h4>Case Insensitive</h4>
<ul><li>User: "Puellam" → ✓ Correct! (auto-lowercased)</li></ul>

<h4>Macron Flexibility</h4>
<ul>
<li>User: "puellam" → ✓ Correct</li>
<li>User: "puellām" → ✓ Also correct (macrons optional)</li>
</ul>

<h4>Common Typos (Fuzzy Matching)</h4>
<ul>
<li>User: "puellm" (1 char off) → ⚠️ "Almost! Check your spelling: puellam"</li>
<li>User: "puellarm" (transposition) → ⚠️ "Close! The correct form is 'puellam'"</li>
<li>Levenshtein distance ≤ 2 → Give partial credit + correction</li>
</ul>

<h4>Wrong Case/Number</h4>
<ul>
<li>User: "puella" (nom instead of acc) → ✗ "That's the nominative. Try accusative: -am"</li>
<li>User: "puellas" (acc plural instead of sg) → ✗ "That's accusative plural. We need singular."</li>
</ul>

<h3>🎓 Practice Modes</h3>

<h4>1. Drill Mode (Single Declension)</h4>
<ul>
<li>Focus: 1st declension only</li>
<li>20 random nouns (puella, via, terra, silva...)</li>
<li>All 12 forms (6 cases × 2 numbers)</li>
<li>Target: Master one declension at a time</li>
</ul>

<h4>2. Mixed Mode (All Declensions)</h4>
<ul>
<li>Random word from any declension</li>
<li>Random case/number combination</li>
<li>Tests full knowledge</li>
</ul>

<h4>3. Verb Conjugation Drill</h4>
<ul>
<li>Focus: Present tense, 1st conjugation</li>
<li>Generate all 6 persons (1sg, 2sg, 3sg, 1pl, 2pl, 3pl)</li>
<li>Expand to all tenses once mastered</li>
</ul>

<h4>4. Timed Challenge</h4>
<ul>
<li>30 seconds per answer</li>
<li>Leaderboard for speed + accuracy</li>
<li>Gamification element</li>
</ul>

<h4>5. Weak Points Review</h4>
<ul>
<li>Focus on user's mistakes from recognition mode</li>
<li>"You confused 3rd declension genitive singular last time. Let's practice that."</li>
<li>Targeted remediation</li>
</ul>

<h3>🔄 Integration with Recognition Mode</h3>

<table>
<tr><th>Learning Stage</th><th>Mode</th></tr>
<tr><td>1. Introduction</td><td>Tutorial (passive explanation)</td></tr>
<tr><td>2. Recognition</td><td>See form → identify case (easier)</td></tr>
<tr><td>3. Production</td><td>See prompt → generate form (harder)</td></tr>
<tr><td>4. Reading</td><td>Full sentences in context (application)</td></tr>
<tr><td>5. Spaced Review</td><td>Mix of recognition + production based on SRS</td></tr>
</table>

<p><strong>Workflow:</strong></p>
<ol>
<li>Learn nominative case (tutorial)</li>
<li>Practice recognition: see "puella" → identify "nominative"</li>
<li>Practice production: prompt "nominative of puella" → type "puella"</li>
<li>Read sentences with nominative forms</li>
<li>SRS reviews both recognition and production</li>
</ol>

<h3>💾 Database Schema</h3>

<pre>CREATE TABLE production_exercises (
  id SERIAL PRIMARY KEY,
  exercise_type VARCHAR(50),
  word_lemma VARCHAR(100),
  word_type VARCHAR(20),
  target_case VARCHAR(20),
  target_number VARCHAR(20),
  target_tense VARCHAR(20),
  correct_answers JSONB,
  difficulty INT,
  INDEX idx_word_type (word_type)
);

CREATE TABLE user_production_attempts (
  id SERIAL PRIMARY KEY,
  user_id INT,
  exercise_id INT,
  user_answer VARCHAR(100),
  correct BOOLEAN,
  hints_used INT,
  time_taken_ms INT,
  attempted_at TIMESTAMP
);</pre>

<h3>📊 Scoring System</h3>

<ul>
<li><strong>Perfect answer, no hints:</strong> 100 points</li>
<li><strong>Perfect answer, 1 hint:</strong> 75 points</li>
<li><strong>Perfect answer, 2+ hints:</strong> 50 points</li>
<li><strong>Fuzzy match (typo):</strong> 80 points</li>
<li><strong>Wrong case (but correct declension):</strong> 25 points</li>
<li><strong>Completely wrong:</strong> 0 points</li>
</ul>

<p><strong>Bonus multipliers:</strong></p>
<ul>
<li>Streak bonus: +10% per consecutive correct (max 50%)</li>
<li>Speed bonus: Answer in &lt;5 seconds → +20%</li>
<li>Perfect session: 20/20 correct → +50% on all points</li>
</ul>

<h3>🎮 Gamification</h3>

<ul>
<li><strong>Badges:</strong>
<ul>
<li>"1st Declension Master" (100% accuracy on 50 exercises)</li>
<li>"Speed Demon" (average &lt;5s per answer)</li>
<li>"Perfect Streak" (50 consecutive correct)</li>
</ul>
</li>
<li><strong>Daily Goals:</strong> "Complete 20 production exercises today"</li>
<li><strong>Leaderboards:</strong> Daily high score, weekly accuracy</li>
</ul>

<h3>⏱️ Implementation Estimate</h3>

<ol>
<li><strong>Exercise generation logic:</strong> 4-6 hours</li>
<li><strong>Validation with CLTK:</strong> 3-4 hours</li>
<li><strong>Fuzzy matching/typo detection:</strong> 2-3 hours</li>
<li><strong>Hint system:</strong> 3-4 hours</li>
<li><strong>UI/keyboard input handling:</strong> 6-8 hours</li>
<li><strong>Database schema + tracking:</strong> 3-4 hours</li>
<li><strong>Scoring/gamification:</strong> 4-6 hours</li>
<li><strong>Integration with SRS:</strong> 4-6 hours</li>
</ol>

<p><strong>Total: 30-45 hours</strong></p>

<h3>🎯 Learning Science</h3>

<blockquote>
<p><strong>Active recall</strong> (production) is proven more effective than passive recognition for long-term retention.</p>

<p>Studies show that generating answers (retrieval practice) leads to better learning outcomes than simply identifying correct answers.</p>

<p>Source: <em>Make It Stick: The Science of Successful Learning</em></p>
</blockquote>

<p><strong>Best practice: 50/50 mix of recognition and production</strong></p>

<p><em>This mode completes the learning cycle!</em></p>
"""

    task = client.tasks.create(
        project_id=LATIN_PROJECT_ID,
        title='Add fill-in-the-blank production mode (generate forms from prompts)',
        description=description,
        priority=4
    )

    print(f"✓ Created task: {task.title}")
    print(f"  URL: {VIKUNJA_URL}/tasks/{task.id}")


if __name__ == "__main__":
    main()
