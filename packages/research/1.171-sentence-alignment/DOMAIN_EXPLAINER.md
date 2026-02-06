# Sentence Alignment: Domain Explainer

## What This Solves

**The Problem**: When you have documents translated into multiple languages, the translations aren't explicitly linked at the sentence level. You have "The quick brown fox jumps" in English and "Le renard brun rapide saute" in French, but the computer doesn't know these sentences are translations of each other.

**Who Encounters This**:
- **Machine translation teams** building training data from parallel texts
- **Localization companies** creating translation memories to avoid re-translating
- **Content platforms** synchronizing documentation across 10+ languages
- **Researchers** analyzing how concepts translate across languages

**Why It Matters**: Without sentence alignment, you're stuck manually matching translations (impossibly slow) or treating each language independently (wasteful duplication). Alignment unlocks:
- **Reuse**: "We already translated this sentence in 2023, use that translation"
- **Quality**: "Compare how three translators handled this difficult passage"
- **Learning**: "Train MT systems on millions of matched sentence pairs"

## Accessible Analogies

### The Matching Game
Imagine two shuffled decks of cards where each card in deck A has a corresponding match in deck B. Sometimes one card matches one card (1-to-1). Sometimes two cards in deck A match a single card in deck B (2-to-1) because deck B's designer combined concepts. Your job: find all matching pairs without knowing the content, only by observing patterns.

**Sentence alignment is that matching game** with three strategies:

1. **Length-based** (Hunalign): "Cards that match are usually similar sizes"
2. **Meaning-based** (vecalign): "Use an expert who understands both decks to find semantic matches"
3. **Translation-based** (Bleualign): "Translate deck A to deck B's language, then match by similarity"

### The Library Reorganization
A library has the same book collection in two buildings: one organized by author (English), one by subject (French). You need to create a "this book here matches that book there" mapping.

**Length-based approach**: "Books of similar thickness probably match" (fast but imperfect—a thick anthology could match a dense philosophy tome)

**Meaning-based approach**: "Hire a bilingual librarian to read both and find matches" (accurate but requires expertise)

**Translation-based approach**: "Translate all English titles to French, then match by title similarity" (works well if translation is good)

### The Assembly Line Sync Problem
Two assembly lines produce the same product but operate at slightly different speeds. Line A might package 3 items while Line B packages 2 larger bundles. You need to match "these 3 items from Line A = these 2 bundles from Line B" to verify they're building the same thing.

**This is the core sentence alignment challenge**: Source and target languages don't always break content into the same sentence boundaries. English might say "Hello. How are you?" (2 sentences) while Japanese might combine it into one polite greeting. Alignment tools find these variable-length matches (1-to-1, 2-to-1, 1-to-2, etc.).

## When You Need This

### ✅ You Need Sentence Alignment If:

**Building Machine Translation Systems**
- You have millions of translated document pairs (UN proceedings, EU documents, movie subtitles)
- You need training data: matched sentence pairs
- Example: "Train Spanish↔English MT on 10M aligned pairs from European Parliament"

**Operating a Translation Memory System**
- Translators work on similar content repeatedly
- You want to reuse previous translations
- Example: "This sentence was translated 6 months ago; reuse it instead of paying a translator"

**Maintaining Multilingual Documentation**
- You have product docs in 15 languages
- New content added frequently
- Example: "We updated the English docs; find matching paragraphs in other languages that need updating"

**Research or Quality Assurance**
- Analyzing translation quality across vendors
- Studying how languages express concepts differently
- Example: "Compare how 5 translators handled this legal clause"

### ❌ You DON'T Need This If:

**Documents Aren't Truly Parallel**
- If source and target have different content (adapted, not translated), alignment will fail
- Example: Marketing materials "localized" with different messaging per region

**Only Working in One Language**
- Alignment is specifically for linking bilingual or multilingual content
- If you're doing monolingual NLP (sentiment analysis, summarization), this isn't relevant

**Sentences Already Aligned**
- Some parallel corpora come pre-aligned (e.g., TMX files from CAT tools)
- Check your data format first; you might already have alignment metadata

**Volume Too Small for Automation**
- For 100 sentence pairs, manual alignment might be faster than tool setup
- Break-even: ~1000+ pairs justify automation

## Trade-offs

### Speed vs Accuracy

**Fast but Less Accurate (Hunalign)**:
- Aligns 100K sentence pairs in minutes
- 85-95% accuracy on clean parallel texts
- Uses statistical length correlation + optional dictionary
- **Fails when**: Creative translation, paraphrasing, poetry

**Slow but More Accurate (vecalign)**:
- Aligns 100K pairs in 10-30 minutes (with GPU)
- 93-99% accuracy on diverse texts
- Uses deep semantic understanding (multilingual embeddings)
- **Fails when**: Very short sentences, memory limits on huge corpora

**Middle Ground (Bleualign)**:
- Requires machine translation as input (adds complexity)
- 90-98% accuracy, especially good for divergent translations
- **Fails when**: MT quality is poor (garbage in, garbage out)

**The Tradeoff**: For most use cases, "fast and good enough" (Hunalign at 90%) beats "slow and perfect" (vecalign at 98%). The extra accuracy only matters if you're building research-grade corpora or alignment errors are costly.

### Resources vs Accessibility

**Low Resources (Hunalign)**:
- Runs on any computer (CPU-only)
- Needs bilingual dictionary for best results
- **Challenge**: Finding good dictionaries for rare language pairs

**High Resources (vecalign)**:
- Requires GPU for reasonable performance (10x faster than CPU)
- Works for 93 languages out-of-the-box (no dictionaries needed)
- **Challenge**: GPU access (cloud costs ~$1-3/hour, or buy hardware)

**The Tradeoff**: If you have GPU access, vecalign is amazing for low-resource languages. If you don't, Hunalign with a dictionary can match its quality for high-resource pairs (English, Spanish, French, German, Chinese, etc.).

### Build vs Buy

**Open Source (Hunalign, vecalign, Bleualign)**:
- Free, full control, customize anything
- Requires setup: Docker, Python dependencies, models
- Ongoing maintenance: updates, bug fixes, monitoring
- **Best for**: >1M sentence pairs/year, in-house ML team

**SaaS APIs (ModernMT, Google Cloud Translation)**:
- Pay per use (~$0.08-0.10 per 1K alignments)
- Zero setup, instant start
- Limited customization, vendor lock-in risk
- **Best for**: <1M pairs/year, small teams, fast time-to-market

**The Tradeoff**: SaaS is cheaper upfront but expensive at scale. Open source has high setup cost but low marginal cost. Break-even: ~5-10M pairs/year.

## Implementation Reality

### First 90 Days: What to Expect

**Weeks 1-2: Tool Selection and Setup**
- Download and test all three tools on a 10K sample
- Manually validate 100 pairs from each to measure accuracy
- Choose tool based on your accuracy/speed requirements
- Set up Docker container or cloud environment
- **Reality check**: Setup takes 1-3 days, not "5 minutes" (especially vecalign with GPU dependencies)

**Weeks 3-6: Integration and Pipeline**
- Build preprocessing: sentence segmentation, text cleaning
- Integrate alignment tool into your workflow (batch processing or API)
- Set up quality monitoring (sample and validate 1% of output)
- **Reality check**: Integration uncovers edge cases (encoding issues, memory limits, timeout handling)

**Weeks 7-12: Production Hardening**
- Scale testing: run on full corpus, measure performance
- Cost optimization: caching, spot instances, parallelization
- Monitoring and alerting: track alignment quality over time
- **Reality check**: 10-20% of sentences won't align perfectly; decide how to handle

### Team Skill Requirements

**Minimum Viable Team**:
- 1 engineer with Python + NLP basics
- Comfortable with command-line tools
- Can read documentation and debug errors
- **Estimated effort**: 0.25 FTE (part-time) for maintenance

**Ideal Team (Production at Scale)**:
- 1 senior ML/NLP engineer (algorithm selection, tuning)
- 1 DevOps/SRE (deployment, monitoring, scaling)
- **Estimated effort**: 0.5-1 FTE total

**Reality**: You don't need PhDs. Sentence alignment is well-understood, and tools are mature. Biggest challenge is operational (infrastructure, monitoring), not algorithmic.

### Common Pitfalls

**Pitfall 1: Assuming Perfect Alignment is Possible**
- Even the best tools get 95-98% accuracy, not 100%
- Literary translation, idioms, cultural adaptations will misalign
- **Solution**: Accept imperfection, filter low-confidence pairs, sample and validate

**Pitfall 2: Ignoring Preprocessing**
- Tools expect clean, sentence-segmented text
- Feeding raw HTML or unsegmented paragraphs causes garbage output
- **Solution**: Invest in preprocessing pipeline (sentence splitters, cleaning)

**Pitfall 3: Not Validating Quality**
- "It ran without errors" ≠ "It produced good results"
- **Solution**: Always manually check 100-1000 random samples before trusting at scale

**Pitfall 4: Over-Engineering for Small Data**
- Don't set up Kubernetes for 10K pairs
- **Solution**: Start simple (Docker on laptop), scale when needed (>1M pairs)

### First 90 Days Timeline (Realistic)

| Week | Milestone | Effort |
|------|-----------|--------|
| 1-2 | Tool evaluation, sample testing | 2-3 days |
| 3-4 | Setup (Docker, dependencies, GPU) | 3-5 days |
| 5-6 | Preprocessing pipeline | 3-5 days |
| 7-8 | Integration with existing workflow | 5-7 days |
| 9-10 | Scale testing, optimization | 3-5 days |
| 11-12 | Monitoring, documentation | 2-3 days |
| **Total** | **Production-ready system** | **20-30 days** |

*Assumes 1 engineer working part-time (50% capacity)*

### Success Metrics

**After 90 Days, You Should Have**:
- ✅ Alignment pipeline processing your corpus end-to-end
- ✅ Quality validation on 1000+ sample pairs (>90% accuracy)
- ✅ Documented workflow for future runs
- ✅ Basic monitoring (track # pairs aligned, errors, runtime)
- ✅ Decision framework for when to re-align vs reuse

## References

- [Hunalign GitHub](https://github.com/danielvarga/hunalign) - Fast length-based alignment
- [vecalign GitHub](https://github.com/thompsonb/vecalign) - Multilingual embedding alignment
- [Bleualign GitHub](https://github.com/rsennrich/Bleualign) - BLEU-based alignment
- [Full Technical Research](01-discovery/DISCOVERY_TOC.md) - Deep dive into all tools and use cases
