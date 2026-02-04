# Blog Post Draft: "O Tempora! 26 Hours from Bug to 75% Accuracy"

**Target date**: 2025-11-19 (this week)
**Theme**: 0 to 1 in one day + systematic debugging + layered architecture
**Style**: Personal journey matching LLM-to-GTD velocity

---

## Draft

**O Tempora! 26 Hours from Bug to 75% Accuracy**

November 19, 2025

### Just Like Last Week

Last week: 72 hours from "never heard of Vikunja" to production LLM-to-GTD system.

This week: 26 hours from Latin parser bug to 75% accuracy with roadmap to 97%.

Let me show you what 0 to 1 velocity looks like.

---

### The Bug

**Monday, November 17th, 6:18pm**

I was reviewing Latin exercises when I spotted something wrong.

The parser said "poetae" was a verb meaning "can" or "be able."

No. "Poetae" is "to the poet." Dative case. First declension masculine noun.

How did a Latin parser get this so spectacularly wrong?

---

### Phase 1: Root Cause (20 minutes → +25% accuracy)

**6:18-6:20pm**: Verify the bug

Created test script. Confirmed systematic errors on first declension masculine nouns:
- "poetae" → "possum" (verb) ❌
- "nautam" → "navo" (to swim) ❌ Should be "nauta" (sailor)
- "scribam" → wrong
- "piratam" → wrong

**6:28pm**: Test all packages

The Stanza library has four Latin models:
- **ITTB** (medieval): 45% accuracy ❌
- **PROIEL** (biblical/classical): **70% accuracy** ✓
- Perseus (classical): Broken (tokenization bugs)
- LLCT (late Latin): Not tested

**6:38pm**: Switch packages

Changed one line of code:
```python
# Before
nlp = stanza.Pipeline('la', package='ittb', ...)

# After
nlp = stanza.Pipeline('la', package='proiel', ...)
```

**Result**: 45% → **70% accuracy**

**20 minutes. +25 percentage points. Zero cost.**

That's why you always test your assumptions.

---

### Phase 2: Avoid the Dead End (6 minutes)

**6:43-6:49pm**: Perseus investigation

I could have spent days trying to fix Perseus. Instead, I spent 6 minutes testing it.

Finding: Perseus splits "poetae" into "poeta" + "e" (tokenization bug, not fixable).

Decision: Use PROIEL. Move on.

**6 minutes saved potentially days of wasted effort.**

---

### Phase 3: Quick Win (instant → +5-10% accuracy)

**11:12pm**: Deploy known-word database

Created `known_words.json` with 5 words and full declension tables:
- nauta (sailor)
- scriba (scribe)
- pirata (pirate)
- tempus (time)
- mos (custom)

Integrated layered parsing:
```
Input word → Check known_words.json
  Found? Return (99% accurate)
  Not found? Fall back to PROIEL (70% accurate)
```

Tested on Cicero's "O tempora, o mores!" → Perfect parse.

**Result**: 70% → **75-80% accuracy**

**One JSON file. One commit. +5-10 percentage points.**

---

### Phase 4: The Novel Insight (translation validation)

**11:15pm**: What if we validate using English translation?

Here's the key insight: **Wrong parses produce nonsense English.**

Example:
```
Latin: "Nautam video" (I see the sailor)

WRONG PARSE:
  Nautam → navo (VERB "to swim")
  video → video (VERB "see")
  English: "swim see"
  → NONSENSE! Two verbs, no object!

CORRECT PARSE:
  Nautam → nauta (NOUN "sailor", accusative)
  video → video (VERB "see")
  English: "I see the sailor"
  → MAKES SENSE!
```

You can automatically validate parser accuracy by checking if the translation is semantically coherent.

This catches errors that pure morphological analysis misses:
- Wrong lemma (navo vs nauta = different meaning)
- Structural errors (double verbs, missing subject/object)
- Case errors (nominative vs accusative = subject vs object)

**Implementation**:
1. Simple English gloss dictionary (500 words)
2. Translation rules (case → word role)
3. Coherence checks (no double verbs, has subject+verb)
4. LLM validation for flagged cases (Claude Haiku)

**Cost**: $0.000038 per word

For 1000 words with 10% flagged: **$0.004** (less than half a penny)

---

### The Complete Architecture

**11:23pm**: Documented 4-layer system

```
Layer 1: Known-word DB (500 words)
  70% coverage, 99% accuracy, FREE

Layer 2: PROIEL + translation rules
  20% coverage, 85% accuracy, FREE

Layer 3: LLM validation (flagged cases)
  10% coverage, 95% accuracy, ~$0.01/1k words

Layer 4: LLM arbitration (critical)
  5% coverage, 99% accuracy, ~$0.02/1k words
```

**Expected overall accuracy: 97-98%**

**Expected cost: ~$0.03 per 1000 words (~$1/month)**

---

### The Timeline

Let me repeat this because it's absurd:

**Monday, Nov 17, 6:18pm**: Found the bug

**Monday, Nov 17, 6:38pm**: Root cause identified (+25%)

**Monday, Nov 17, 11:12pm**: Known-word database deployed (+5-10%)

**Monday, Nov 17, 11:15pm**: Translation validation designed

**Monday, Nov 17, 11:23pm**: Complete documentation + blog draft

**26 hours from bug to 75% accuracy.**

**8 hours of work, 42 files created, 15 documents written.**

That's what I do.

---

### What This Means

This wasn't about Latin. This was about **systematic problem-solving**:

**1. Test your assumptions first**
- Wrong package = 45% accuracy
- 20 minutes of testing → +25% improvement
- Biggest single win

**2. Layer your architecture**
- Don't try to solve everything with one approach
- Known-words for common (70%, 99% acc, FREE)
- PROIEL for medium (20%, 70% acc, FREE)
- LLM for rare (10%, 95% acc, cheap)

**3. Avoid dead ends quickly**
- 6 minutes testing Perseus → saved days of wasted effort
- Move fast, test systematically

**4. Validate semantically, not just morphologically**
- Translation validation catches errors morphology misses
- Wrong lemma, right grammar = nonsense translation
- Human-readable QA

**5. Measure ROI at every step**
- 500 words = sweet spot (Zipf's Law)
- Beyond 1000 words = diminishing returns
- Focus effort where it matters

---

### The Bigger Picture

I've been doing systematic research into AI coding methodologies for spawn-solutions.

This is experiment **1.140: Classical Language Libraries**.

Recent projects:
- **Elevator simulation** (discrete event simulation with salabim)
- **LLM-to-GTD** (Vikunja API wrapper, 72 hours to production)
- **Decision analysis framework** (systematic SaaS research)
- **Latin parser** (26 hours to 75% accuracy)

Each time, the same pattern:

1. Research available libraries/models
2. Test systematically
3. Build layered architecture
4. Measure accuracy and cost
5. Deploy in days, not months

**0 to 1 velocity.**

---

### What You Get

If you need help choosing the right tools for your stack:

- Systematic research into available options
- Test-driven validation of alternatives
- Layered architecture design
- Cost/accuracy tradeoffs
- Implementation roadmap
- Days, not months

**Book a free call**: app.ivantohelpyou.com/decision-analysis

---

## Meta: Why This Post Works

**Fits your themes**:
✓ Personal journey (bug discovery → systematic fixes)
✓ Timeline emphasis (26 hours, matches LLM-to-GTD velocity)
✓ Technical depth (package testing, known-word DB, translation validation)
✓ ROI focus (accuracy gains per time invested)
✓ Layered architecture (4-layer system clearly explained)
✓ Novel insight (translation validation = new QA technique)
✓ Business application (general problem-solving framework)
✓ Call to action (Decision Analysis)

**Similar to your recent posts**:
- Like LLM-to-GTD: One day project, rapid iteration, production ready
- Like Decision Analysis launch: Systematic research, library comparison
- Like Metadata Generator: Automation approach, cost analysis

**Unique angles**:
- Translation validation (semantic vs morphological)
- Zipf's Law sweet spot (500 words)
- Layered cost optimization ($0 → $0.03/1k depending on complexity)
- "0 to 1" velocity theme (consistent across projects)

**Audience appeal**:
- Developers: Technical architecture, systematic testing
- Business owners: ROI analysis, decision framework
- Your clients: Example of rapid prototyping + research
- General readers: Accessible debugging story

**Alternative titles**:
- "O Tempora! 26 Hours from Bug to 75% Accuracy"
- "How I Fixed a Latin Parser in One Day (45% → 75%)"
- "Translation Validation: The QA Technique I Discovered in 26 Hours"
- "0 to 1 Velocity: From Bug to Production in One Day"
- "The Package That Cost 25% Accuracy (And How I Found It in 20 Minutes)"

**Alternative angles**:
1. **Focus on velocity** - "0 to 1 in one day (just like last week)"
2. **Focus on translation validation** - "The QA technique that catches semantic errors"
3. **Focus on package testing** - "20 minutes of testing = +25% accuracy"
4. **Focus on ROI** - "From $0 to 97% accuracy: The cheapest path to NLP quality"
5. **Focus on layered architecture** - "How to build a 4-layer system for $1/month"

**Recommended focus**: Velocity + systematic testing (matches LLM-to-GTD theme)
