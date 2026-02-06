# Terminology Extraction Libraries: Domain Explainer

**Purpose**: Help technical decision makers understand Python terminology extraction libraries and choose the right tool for translation, technical writing, and domain-specific NLP projects.

**Audience**: Product managers, technical leads, translators, technical writers without deep NLP expertise.

---

## What This Solves

### The Problem

Imagine you're a translator working on a 50-page technical manual about machine learning. You need to:
1. Identify all technical terms ("neural network," "gradient descent," "backpropagation")
2. Ensure consistent translation across the document
3. Build a glossary for future projects

**Manual approach**: Read through 50 pages, manually highlight terms, copy to spreadsheet.
**Time**: 3-4 hours of tedious work.

**Automated approach**: Run terminology extraction library, get list of 200 candidate terms in 30 seconds.
**Review time**: 30-60 minutes to validate and filter.

**This is the terminology extraction problem**: Automatically finding domain-specific technical terms in large documents.

### Who Encounters This

- **Translators**: Building glossaries for technical translations (medical, legal, engineering)
- **Technical Writers**: Maintaining terminology consistency across documentation
- **Domain NLP**: Extracting concepts for knowledge graphs, ontologies, search systems
- **Localization Teams**: Scaling terminology management across languages and projects

### Why It Matters

**Business Impact**:
- **Translation**: 60-80% time savings on glossary creation (3-4 hours → 30-60 min per 10K words)
- **Technical Writing**: Automated glossary generation ensures terminology consistency
- **Domain NLP**: Foundation for building domain-specific models (medical, legal, etc.)

**Technical Impact**:
- Identify multi-word technical terms ("natural language processing" not just "language")
- Domain-specific extraction (medical terms from medical texts, legal from legal)
- Multilingual support (Chinese, Japanese, Korean technical terminology)

---

## Accessible Analogies

### What Is Terminology Extraction?

**Analogy**: Finding Specialized Vocabulary in a Foreign Language Textbook

Imagine learning Chinese from a computer science textbook. You need to identify:
- **Technical terms**: "机器学习" (machine learning), "神经网络" (neural network)
- **General words**: "学习" (learning), "网络" (network)

A **keyword extractor** would find both (anything important-looking).
A **terminology extractor** would focus on the technical terms (domain-specific).

**Terminology extraction** is like having a smart assistant that knows the difference between "learning" (general word) and "machine learning" (technical term).

### Why Libraries Matter

**Without libraries**: You write custom code to find technical terms
- Implement statistical algorithms (C-Value, TF-IDF)
- Handle POS tagging, linguistic rules
- Build language-specific models

**Time**: Weeks to months of development

**With libraries**: `pip install pyate` or `pip install keybert`
- Pre-built algorithms (battle-tested)
- Multi-language support
- 3 lines of code to extract terms

**Time**: Minutes to hours

---

## When You Need This

### Clear Decision Criteria

**You NEED terminology extraction if**:
- ✅ Large documents with technical content (>5,000 words)
- ✅ Recurring projects in same domain (build glossary once, reuse)
- ✅ Multiple translators/writers (consistency matters)
- ✅ Tight deadlines (60-80% time savings on term prep)

**You DON'T need this if**:
- ❌ Small documents (<1,000 words) - manual extraction faster
- ❌ General content (few technical terms)
- ❌ One-off projects (no glossary reuse value)

### Concrete Use Case Examples

**Translation Glossary Creation**:
- **Problem**: Translator receives 50-page medical device manual. Manual term identification takes 3-4 hours.
- **Solution**: Run pyate (English) or KeyBERT (Chinese/Japanese/Korean), get 200 candidate terms in 30 seconds, review in 30-60 minutes.
- **ROI**: 60-80% time savings (3-4 hours → 30-60 min)

**Technical Documentation Consistency**:
- **Problem**: 10 technical writers producing 500 pages of documentation. Inconsistent terminology ("ML model" vs "machine learning model" vs "ML algorithm").
- **Solution**: Extract terminology from all 500 pages, create shared glossary, enforce consistency.
- **ROI**: Improved documentation quality, reduced customer confusion

**Multilingual Product Documentation (CJK)**:
- **Problem**: Product docs in English, Chinese, Japanese, Korean. Need consistent terminology across languages.
- **Solution**: KeyBERT with multilingual model extracts terms from all languages using single tool.
- **ROI**: Consistency across languages, simplified workflow

---

## Trade-offs

### What You're Choosing Between

#### 1. pyate vs KeyBERT: Terminology vs Keywords

**pyate (Terminology Extraction)**:
- **Pros**: High precision (70-80%) for technical terms, multi-word focus ("gradient descent optimization"), domain-specific
- **Cons**: English and Italian only (no Chinese/Japanese/Korean), requires spaCy dependency

**When**: English/Italian technical documentation, translation glossaries, domain-specific NLP

**KeyBERT (Keyword Extraction)**:
- **Pros**: Multilingual (50-109 languages including CJK), semantic understanding, simple API
- **Cons**: Extracts keywords (not pure terminology), CJK character-level tokenization, slower (BERT inference)

**When**: Chinese/Japanese/Korean content, multilingual projects, semantic keywords (not just technical terms)

**Key Difference**: pyate finds **technical terms**, KeyBERT finds **semantically important words**. Overlap exists, but goals differ.

#### 2. Automated Extraction vs Manual Curation

**Automated Extraction**:
- **Pros**: 60-80% time savings, handles large volumes (1000s of documents)
- **Cons**: 60-80% precision (20-40% false positives), requires validation

**When**: Large documents, recurring projects, tight deadlines

**Manual Curation**:
- **Pros**: 95%+ precision, full control
- **Cons**: Time-consuming (3-4 hours per 10K words)

**When**: Small documents, one-off projects, ultra-high precision required

**Recommended**: **Hybrid** - automated extraction for volume, human validation for precision.

#### 3. Integrated CAT Tools vs Python Libraries

**CAT Tool Built-in**:
- **Pros**: Integrated workflow (no export/import), convenient
- **Cons**: Less sophisticated algorithms, vendor lock-in

**When**: Existing CAT tool user, convenience > precision

**Python Libraries (pyate/KeyBERT)**:
- **Pros**: State-of-art algorithms, customizable, free/open-source
- **Cons**: Requires Python skills, manual export to CAT tool

**When**: Need best precision, willing to invest setup time, tech-savvy team

---

## Cost Considerations

### Why Cost Matters Here

Unlike commercial terminology tools ($500-5,000/year per seat), **Python libraries are free**. The cost is **time and expertise**.

### Pricing Models

**Python Libraries (Free)**:
- **Software Cost**: $0 (open-source)
- **Setup Cost**: 1-4 hours (installation, learning)
- **Ongoing Cost**: 10-20 hours/year (maintenance, updates)

**Commercial Tools (Sketch Engine, AntConc alternatives)**:
- **Software Cost**: $500-5,000/year per seat
- **Setup Cost**: Included (vendor support)
- **Ongoing Cost**: Vendor handles updates

### ROI Analysis

**Translation Glossary Creation** (10K-word document):
- **Manual**: 3-4 hours × $50/hour = **$150-200 per document**
- **Automated (pyate/KeyBERT)**: 30-60 min × $50/hour = **$25-50 per document**
- **Savings**: $100-150 per document (60-75% reduction)

**Payback**: If processing >10 documents/year, automated extraction pays for setup time in first month.

**Technical Documentation** (500 pages):
- **Manual**: 20-30 hours × $75/hour = **$1,500-2,250**
- **Automated**: 2-4 hours (extraction + review) × $75/hour = **$150-300**
- **Savings**: $1,200-2,000 (85-90% reduction)

---

## Implementation Reality

### Realistic Timeline Expectations

**Prototype** (1 week):
- Install pyate or KeyBERT
- Run on sample documents (10-20 pages)
- Validate output quality
- **Team**: 1 developer or technical translator

**Production MVP** (2-4 weeks):
- Set up batch processing pipeline
- Create validation workflow (human-in-loop)
- Export to glossary format (CSV, TBX)
- Train team on usage
- **Team**: 1 developer + 1 domain expert (translator/writer)

**Optimized Production** (2-3 months):
- Fine-tune for specific domain (if needed)
- Integrate with CAT tool or documentation system
- Automate glossary updates (CI/CD)
- **Team**: 1 developer + 1-2 domain experts

### Team Skill Requirements

**Minimum** (Using KeyBERT):
- **Python**: Basic (run scripts, install packages)
- **NLP Knowledge**: None (library handles complexity)
- **Domain Expertise**: High (validate extracted terms)
- **Training Time**: 1-2 days

**Typical** (Using pyate + spaCy):
- **Python**: Moderate (pipelines, batch processing)
- **NLP Knowledge**: Basic (understand POS tagging)
- **Domain Expertise**: High
- **Training Time**: 1-2 weeks

### Common Pitfalls

**Pitfall 1**: "Automated extraction replaces human review"
- **Reality**: Extraction is 60-80% precise. Human validation essential.
- **Fix**: Budget time for review (30-60 min per 10K words)

**Pitfall 2**: "CJK support means perfect Chinese/Japanese/Korean"
- **Reality**: KeyBERT uses character-level tokenization (may miss word boundaries)
- **Fix**: Use chinese_keybert for Chinese-only, plan for extra validation

**Pitfall 3**: "Keywords = Terminology"
- **Reality**: KeyBERT extracts semantically important words, not always technical terms
- **Fix**: Use pyate for pure terminology (if language supported), KeyBERT + filtering otherwise

**Pitfall 4**: "One library solves everything"
- **Reality**: pyate best for English/Italian terminology, KeyBERT best for CJK
- **Fix**: Use both (per-language optimization) or abstract interface (swap backends)

---

## Key Takeaways for Decision Makers

### Top 3 Decisions to Make

**Decision 1**: Terminology Extraction vs Keyword Extraction
- **Rule**: Need technical terms (glossaries, translation)? → pyate (if English/Italian) or KeyBERT + filtering (if CJK)
- **Rule**: Need semantic keywords (content tagging)? → KeyBERT

**Decision 2**: Language Support
- **Rule**: English or Italian only? → pyate (highest precision)
- **Rule**: Chinese, Japanese, Korean, or multilingual? → KeyBERT (only viable option)

**Decision 3**: Integration Approach
- **Rule**: CAT tool built-in available? → Use it (convenience)
- **Rule**: Need best precision or CJK support? → Python libraries (setup effort justified)

### Budget Guidance

**Setup** (One-Time):
- Developer time: 1-4 weeks × $5K/week = **$5K-20K**
- Infrastructure: $0 (runs on standard hardware)
- **Total**: **$5K-20K**

**Ongoing** (Per Year):
- Maintenance: 10-20 hours × $100/hour = **$1K-2K**
- **Total**: **$1K-2K/year**

**ROI**:
- Translation: $100-150 savings per 10K-word document
- Technical Docs: $1,200-2,000 savings per 500-page manual
- **Payback**: Typically 1-3 months for active translation/writing teams

### Questions to Ask Vendors/Consultants

**Technical Questions**:
1. "Which library do you recommend: pyate or KeyBERT? Why?" (Tests understanding of terminology vs keyword trade-off)
2. "How does it handle Chinese/Japanese/Korean?" (Tests CJK knowledge)
3. "What's the expected precision for our domain?" (Tests realistic expectations - should be 60-80%, not 95%)

**Business Questions**:
1. "What's the time savings vs manual extraction?" (Should quote 60-80%, not 90-95%)
2. "How much human validation is needed?" (Should acknowledge 20-40% false positives)
3. "Can it integrate with our CAT tool?" (Most likely no - manual export/import)

**Red Flags**:
- ❌ Claims 90-95% precision without human review (unrealistic)
- ❌ Recommends same library for all languages (no understanding of pyate/KeyBERT trade-offs)
- ❌ Doesn't mention CJK challenges (character-level tokenization)

**Green Flags**:
- ✅ Recommends pyate for English, KeyBERT for CJK (shows nuanced understanding)
- ✅ Acknowledges 60-80% precision, plans for human validation
- ✅ Discusses integration challenges (export/import to CAT tool)

---

## Glossary

**Terminology Extraction**: Automatically finding domain-specific technical terms (multi-word expressions like "machine learning model")

**Keyword Extraction**: Finding semantically important words in a document (may include general words if important)

**CJK**: Chinese, Japanese, Korean languages (share some NLP challenges like lack of spaces between words)

**CAT Tool**: Computer-Assisted Translation tool (SDL Trados, MemoQ, Smartcat) - software translators use

**Glossary/Termbase**: Database of technical terms and their translations

**pyate**: Python library for terminology extraction (C-Value, Combo Basic algorithms). Best for English/Italian.

**KeyBERT**: Python library for keyword extraction using BERT embeddings. Best for multilingual/CJK.

**spaCy**: Industrial-strength NLP library (POS tagging, parsing). Required by pyate.

**BERT**: Transformer-based language model. Provides semantic understanding for KeyBERT.

**Precision**: How many extracted terms are actually technical terms (70-80% typical)

**Recall**: How many actual technical terms were found (harder to measure, less critical)

---

## Further Reading

**Non-Technical**:
- "Nine Terminology Extraction Tools for Translators" (LinguaGreca) - Practical translator perspective
- "Translation Glossary Creation Guide" (Smartcat) - Workflow and best practices

**Technical**:
- pyate documentation: https://kevinlu1248.github.io/pyate/
- KeyBERT documentation: https://maartengr.github.io/KeyBERT/
- Astrakhantsev 2016 (ATR4S benchmark) - Academic validation of algorithms

**Community**:
- spaCy Universe: https://spacy.io/universe (pyate and ecosystem)
- sentence-transformers: https://www.sbert.net/ (KeyBERT backend)

**Tools**:
- CAT Tools: SDL Trados, MemoQ, Smartcat (commercial translation tools)
- Alternative Python: YAKE, RAKE-NLTK (simpler keyword extraction)
