# MT + TM Hybrid Workflows

## The Convergence (2026)

**Trend:** Translation memories, glossaries, and post-edit data directly influence AI systems. MT and TM are no longer separate—they work together.

**Source:** [6 AI translation trends to watch in 2026 - POEditor](https://poeditor.com/blog/ai-translation-trends-2026/)

## Hybrid Approach

**Strategy:** Combine TM matches (human-generated) with MT output to minimize editing effort and maximize quality.

**Workflow:**
1. **Pre-editing:** Prepare source text
2. **TM Matching:** Check for existing translations
3. **Route by Match Quality:**
   - **100% context match** → Use TM, no MT
   - **90-99% fuzzy match** → Use TM, human edits
   - **75-89% fuzzy match** → Show TM + MT, translator chooses
   - **0-74% match** → Use MT, human post-edits

**Source:** [Integration of Machine Translation and Translation Memory](https://aclanthology.org/2021.triton-1.18.pdf)

## TM Match Insertion in MT

**Feature:** Automatically insert high-quality TM matches, bypassing MT

**Example (Smartling):**
- Configure MT profile with TM match threshold (e.g., 95%)
- When content goes through MT workflow:
  - Segments with ≥95% TM match **skip MT entirely**
  - Lower matches use MT as usual
- Result: Best of both worlds (human quality where available, MT for new content)

**Source:** [Insert Translation Memory Matches In Machine Translation – Smartling](https://help.smartling.com/hc/en-us/articles/19345269134107-Insert-Translation-Memory-Matches-In-Machine-Translation)

## MTPE (Machine Translation Post-Editing)

### What is MTPE?

**Definition:** Human editing of machine-translated content

**Levels:**
- **Light Post-Editing:** Minimal edits (make comprehensible, fix critical errors)
- **Full Post-Editing:** Edit to human quality standards

### When to Use MTPE vs. Pure TM

| Content Type | Recommendation |
|--------------|----------------|
| Marketing copy | **TM or human** (brand voice critical) |
| Technical docs (repetitive) | **TM** (consistency matters) |
| Support tickets | **MT + light PE** (volume high, perfection not critical) |
| Software UI | **TM** (terminology consistency required) |
| User-generated content | **MT + light PE** (acceptable quality, high volume) |

**Source:** [Machine Translation vs. Machine Translation Post-editing - memoQ](https://blog.memoq.com/machine-translation-vs.-machine-translation-post-editing-which-one-to-use-and-when)

### The MTPE Workflow

1. **Source Text** → Machine Translation → **Raw MT Output**
2. **Raw MT Output** → Post-Editor (human) → **Edited Translation**
3. **Edited Translation** → **Stored in TM** for future reuse

**Key Insight:** Post-edited MT becomes TM for next project, improving quality over time.

**Source:** [The Machine Translation Post-Editing Workflow](https://www.linkedin.com/pulse/post-editing-workflow-viveta-gene-intertranslations-greece-)

## Human Role Evolution (2026)

**Shift:** Linguists becoming quality supervisors and domain experts rather than word-by-word translators.

**New Responsibilities:**
- **Evaluate AI output** at a higher level
- **Provide feedback** that improves model behavior
- **Maintain termbases** for consistent AI training
- **Domain expertise** for specialized content

**Not Eliminated:** AI won't replace human linguists, but changes their role.

**Source:** [A hybrid translation approach: Machine Translation Post Editing (MTPE)](https://www.smartling.com/blog/a-hybrid-translation-approach-machine-translation-post-editing-mtpe)

## Practical Implementation

### Decision Logic

```python
def choose_translation_source(segment, tm_lookup, mt_engine):
    """Decide whether to use TM or MT for a segment"""

    # Look up TM match
    tm_match = tm_lookup(segment)

    if tm_match and tm_match['score'] >= 100:
        # Perfect match - use TM
        return {
            'source': 'TM',
            'translation': tm_match['target'],
            'requires_review': tm_match['context_match']  # Context match = no review
        }

    elif tm_match and tm_match['score'] >= 85:
        # High fuzzy match - use TM with review
        return {
            'source': 'TM_FUZZY',
            'translation': tm_match['target'],
            'requires_review': True,
            'match_score': tm_match['score']
        }

    elif tm_match and tm_match['score'] >= 70:
        # Moderate match - show both TM and MT
        mt_output = mt_engine.translate(segment)
        return {
            'source': 'HYBRID',
            'tm_suggestion': tm_match['target'],
            'mt_suggestion': mt_output,
            'requires_review': True,
            'match_score': tm_match['score']
        }

    else:
        # No useful TM match - use MT
        mt_output = mt_engine.translate(segment)
        return {
            'source': 'MT',
            'translation': mt_output,
            'requires_review': True,
            'post_edit_required': True
        }
```

### Storing Post-Edited MT in TM

After post-editing, add to TM:

```python
from pythontmx import TmxFile, TranslationUnit, TranslationUnitVariant

# Load existing TM
tmx = TmxFile.read("memory.tmx")

# After post-editing
source_segment = "Hello world"
mt_output = "Bonjour le monde"  # Raw MT
post_edited = "Bonjour tout le monde"  # Human-edited

# Create TU with post-edited version
tu = TranslationUnit()
tu.add_variant(TranslationUnitVariant(lang="en-US", segment=source_segment))
tu.add_variant(TranslationUnitVariant(lang="fr-FR", segment=post_edited))

# Add metadata indicating origin
tu.add_property("origin", "MT_POST_EDITED")

tmx.body.add_translation_unit(tu)
tmx.write("memory.tmx")
```

**Key:** Post-edited MT enriches TM for future projects.

## Cost Optimization

**Pricing Model:**
- **100% TM match:** 0-10% of full human rate
- **Fuzzy match (90-99%):** 20-50% of full rate
- **MT + light PE:** 30-50% of full rate
- **MT + full PE:** 50-70% of full rate
- **Human from scratch:** 100% rate

**Strategy:** Maximize TM matches to minimize cost. Use MT+PE for new content.

## Quality Thresholds

**Decision Matrix:**

| Match Quality | Action | Review Level |
|---------------|--------|--------------|
| 100% context | Use TM | None (auto-confirm) |
| 100% exact | Use TM | Light review |
| 95-99% fuzzy | Use TM | Full review |
| 85-94% fuzzy | TM or MT | Full review |
| 70-84% fuzzy | MT preferred | Post-edit |
| <70% | MT only | Post-edit |

**Adjust thresholds** based on content criticality (marketing = higher thresholds, support tickets = lower).

## Sources

- [A hybrid translation approach: Machine Translation Post Editing (MTPE)](https://www.smartling.com/blog/a-hybrid-translation-approach-machine-translation-post-editing-mtpe)
- [Machine Translation in the Translation Memory – Smartling](https://help.smartling.com/hc/en-us/articles/10212608375963-Machine-Translation-in-the-Translation-Memory)
- [Insert Translation Memory Matches In Machine Translation – Smartling](https://help.smartling.com/hc/en-us/articles/19345269134107-Insert-Translation-Memory-Matches-In-Machine-Translation)
- [Integration of Machine Translation and Translation Memory](https://aclanthology.org/2021.triton-1.18.pdf)
- [Machine Translation vs. Machine Translation Post-editing - memoQ](https://blog.memoq.com/machine-translation-vs.-machine-translation-post-editing-which-one-to-use-and-when)
- [6 AI translation trends to watch in 2026 - POEditor](https://poeditor.com/blog/ai-translation-trends-2026/)
- [The Machine Translation Post-Editing Workflow](https://www.linkedin.com/pulse/post-editing-workflow-viveta-gene-intertranslations-greece-)
