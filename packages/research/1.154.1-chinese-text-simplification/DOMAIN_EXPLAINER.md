# Chinese Text Simplification Libraries

## What This Solves

Imagine you're running a Chinese learning app with thousands of authentic news articles, but your HSK 3 learners keep hitting walls of vocabulary they don't know. You could manually rewrite articles (expensive, slow), or you could automatically simplify them—replacing difficult words with easier synonyms, shortening complex sentences, and removing advanced grammar patterns.

Chinese Text Simplification (CTS) solves this fundamental problem: **automatically converting complex Chinese text into simpler versions that match a target proficiency level**. It takes any Chinese text and rewrites it to be comprehensible at HSK 2, 3, 4, etc.

This differs from **readability analysis** (which just measures difficulty) by actually *transforming* the text. It's the difference between a thermometer (analysis) and an air conditioner (simplification).

This matters to three groups:

1. **Language learning platforms** need to offer graded content at scale (can't hire editors to simplify thousands of articles)
2. **Accessibility services** need to make government documents, healthcare info, and public services readable for lower-literacy Chinese readers
3. **Content creators** need tools to adapt writing for different audience proficiency levels (textbooks, news sites, technical documentation)

Without automated simplification, these groups resort to manual rewriting (expensive, inconsistent) or avoid complex content entirely (limiting educational value).

## Accessible Analogies

Think of Chinese text simplification like a **recipe adapter**:

- **Original recipe** (advanced): "Julienne the carrots, create a mirepoix base, deglaze with Shaoxing wine"
- **Simplified recipe** (beginner): "Cut the carrots into thin strips, cook onions and carrots together, add rice wine to the pan"

The recipe adapter:
1. Replaces fancy cooking terms with simple descriptions
2. Breaks complex steps into smaller ones
3. Uses common ingredients instead of specialized ones
4. Keeps the same end result (dish is the same, instructions are clearer)

Chinese text simplification does the same:
1. Replaces advanced vocabulary with HSK-level equivalents
2. Splits long compound sentences into shorter ones
3. Removes or replaces idioms (成语) with plain explanations
4. Keeps the same meaning (content is preserved, expression is simplified)

**Another angle**: Like a translation app, but instead of translating between languages, it "translates" from advanced Chinese to beginner Chinese. Both preserve meaning while changing form.

**The challenge**: Unlike English where you can often just swap "utilize" → "use", Chinese has:
- No spaces between words (need segmentation first)
- Multiple ways to express the same concept with different difficulty levels
- Idioms that can't be translated word-for-word
- Sentence structures that require complete restructuring, not just word replacement

This is why off-the-shelf NLP libraries don't work—you need specialized Chinese text simplification tools.

## When You Need This

**You definitely need this if:**

- You run a language learning platform and want to offer graded readers automatically ("here's today's news at HSK 3 level")
- You're building accessibility tools for government or public services (simplified documents for low-literacy readers)
- You create educational materials and need to generate multiple difficulty versions of the same content
- You manage a news site offering "Easy Chinese" versions and want to automate the simplification pipeline

**You probably need this if:**

- You're building AI tutoring systems that need to adjust explanation complexity to learner level
- You're researching second-language acquisition and need controlled text difficulty
- You're developing translation tools with simplification as a post-processing step

**You DON'T need this if:**

- You only need to *measure* readability (use HSK-Character-Profiler or similar instead)
- You only need Traditional/Simplified conversion (use OpenCC instead)
- You're working with native speakers who don't need simplification
- You have manual editorial resources and small volume (< 100 texts/month)

**The decision hinges on**: Are you transforming complex text to simpler versions at scale? If yes, you need simplification. If you just need to know "is this HSK 3?", use analysis tools instead.

## Trade-offs

### Rule-Based vs Neural Network

**Rule-based simplification** (word replacement + sentence splitting):
- ✅ Fast (milliseconds per text)
- ✅ Predictable output (same input always gives same result)
- ✅ Easy to debug (you can see which rules fired)
- ✅ Requires no training data
- ❌ Limited to vocabulary substitution (can't restructure complex sentences well)
- ❌ Struggles with idioms, metaphors, context-dependent meaning
- ❌ Needs manually curated synonym dictionaries at each HSK level

**Neural network approach** (seq2seq, transformer models):
- ✅ Can restructure sentences creatively (not just word swaps)
- ✅ Handles idioms and context better
- ✅ Improves with more training data
- ❌ Slower (seconds per text on CPU)
- ❌ Unpredictable (might generate fluent but incorrect simplifications)
- ❌ Requires large parallel corpora (complex ↔ simple sentence pairs)
- ❌ Hard to control output level (can't guarantee "exactly HSK 3")

**Current reality**: Most production systems use rule-based as foundation + neural for specific hard cases. Pure neural is still research-grade.

### Character-Level vs Word-Level

**Character-level substitution**:
- ✅ Simpler implementation (no word segmentation needed)
- ✅ Aligns with HSK character lists
- ❌ Breaks compound words (replacing 研 in 研究 changes meaning)
- ❌ Misses multi-word expressions that need to be replaced as units

**Word-level substitution**:
- ✅ Preserves compound word integrity
- ✅ Can handle multi-word idioms
- ❌ Requires accurate segmentation (jieba is ~95% accurate, errors cascade)
- ❌ More complex to implement

**Hybrid approach** (recommended): Segment into words, simplify at word level, validate at character level.

### Build vs Dataset

**Build from scratch** (your own rules + dictionaries):
- ✅ Full control over simplification strategy
- ✅ Can customize for your domain (medical, legal, etc.)
- ❌ Requires linguistic expertise
- ❌ Months of development time
- ❌ Need native speaker validation

**Use research datasets** (MCTS, parallel corpora):
- ✅ Training data already exists (691K+ sentence pairs)
- ✅ Can train neural models if you have ML expertise
- ❌ Datasets are academic (news text, not your domain)
- ❌ Still need to build the actual simplification pipeline
- ❌ No turnkey solution (MCTS is data, not a library)

**Use existing libraries** (currently limited options):
- ✅ Fastest time to value (if they exist)
- ❌ **Reality check**: There are very few production-ready pip-installable CTS libraries as of 2026
- ❌ Most published work is research code, not maintained libraries

## Cost Considerations

**Research approach** (use MCTS dataset + train your own model):
- Dataset: Free (open source)
- Model training: $100-500 in GPU time (if using cloud)
- Development: $20K-$50K (2-4 months, requires ML expertise)
- Hosting: $50-200/month for inference
- Year 1 total: ~$25K-$60K
- Only makes sense for large-scale platforms (> 10K texts/month)

**Rule-based DIY**:
- Development: $10K-$30K (1-3 months, requires NLP + Chinese expertise)
- Hosting: $20-50/month (runs in your app)
- HSK vocabulary lists: Free (open source)
- Synonym dictionaries: Build manually or scrape ($2K-$5K)
- Year 1 total: ~$12K-$35K
- Sweet spot for mid-sized platforms (1K-10K texts/month)

**Hybrid approach** (jieba + OpenCC + HSK-Character-Profiler + custom rules):
- Integration: $5K-$15K (2-4 weeks)
- Use existing libraries for segmentation, conversion, analysis
- Build custom simplification logic on top
- Year 1 total: ~$7K-$18K
- **Most practical option for MVP**

**Commercial API** (if they existed):
- Would cost ~$5-20 per 1K simplifications
- None currently available as of 2026 for Chinese
- English has services (Rewordify, TextCompactor), Chinese market is nascent

**Manual editing** (baseline comparison):
- Professional editor: $0.10-$0.30 per sentence
- At 1,000 texts/month (avg 20 sentences): $2K-$6K/month
- Year 1: $24K-$72K
- Break-even: Automation pays off at > 100 texts/month

## Implementation Reality

### First 30 Days

Week 1: Set up infrastructure with existing libraries:
- Install jieba for segmentation
- Install OpenCC for Traditional/Simplified handling
- Install HSK-Character-Profiler for difficulty measurement
- Build simple word replacement pipeline with HSK vocabulary lists

Weeks 2-4: Build and test simplification rules:
- Create synonym dictionaries at each HSK level
- Implement sentence splitting for long sentences (> 20 characters)
- Test on sample texts, measure with human evaluators
- Deploy basic API endpoint

You'll have a working prototype that can simplify ~70% of sentences (the easy cases).

### What Actually Takes Time

1. **Synonym dictionary curation**: Finding "simple equivalents" for 2,500+ HSK 6 words takes weeks of linguistic work
2. **Context handling**: "银行" means "bank" (financial) or "riverbank" depending on context—rules alone won't catch this
3. **Idiom treatment**: 成语 (4-character idioms) need special handling (replace whole unit, not individual characters)
4. **Quality validation**: Need native speakers to verify simplifications don't change meaning
5. **Edge cases**: Names, numbers, technical terms, internet slang—each needs special rules

### Common Pitfalls

- **Over-simplifying**: Replacing every HSK 5 word breaks flow ("The very smart person" → "The very very smart person" because you replaced "intelligent")
- **Meaning drift**: Synonyms aren't perfect ("老师" (teacher) → "先生" (Mr./teacher) shifts formality)
- **Segmentation errors**: Jieba mistakes cascade (if it segments wrong, replacements break)
- **No ground truth**: Unlike translation (many references exist), Chinese simplification has limited parallel corpora for validation

### Team Skills Required

- **Rule-based MVP**: Mid-level Python dev + native Chinese speaker for validation (2 people, 1 month)
- **Production system**: Senior NLP engineer + Chinese linguist + QA (3 people, 3 months)
- **Neural approach**: ML engineer + data scientist + Chinese linguist (3 people, 6+ months)

### Realistic Expectations

You'll achieve:
- 70-80% of sentences simplified successfully (word replacements work)
- 15-20% need manual review (complex restructuring)
- 5-10% fail or degrade quality (idioms, context errors)

This is good enough for assistive tools (human reads final output). Not good enough for fully automated publishing (needs editorial review).

**The technology is nascent compared to English**: While English text simplification has commercial solutions, Chinese is still largely a research problem with limited production-ready libraries. Most organizations build custom solutions.

## Library Landscape (2026)

**Key distinction**: This research focuses on LIBRARIES (pip-installable, production-ready), not research datasets or one-off scripts.

**Current state**:
- ✅ **Analysis libraries** are mature (HSK-Character-Profiler, HanLP)
- ✅ **Utility libraries** are solid (jieba, OpenCC)
- ❌ **Actual simplification libraries** are sparse (mostly research code, not production libraries)

Most teams combine existing analysis/utility libraries with custom simplification logic.

**What you'll find in S1-rapid**: Inventory of available libraries and their actual capabilities for text simplification.
