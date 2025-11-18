# 1.140: Classical Language Libraries Discovery

**Research Code**: 1.140
**Title**: Classical Language Libraries (CLTK, pyLatinam, PyWORDS)
**Category**: Language Learning & Linguistic Libraries
**Status**: In Progress
**Started**: 2025-11-17

## Research Question

**"What is the optimal Python library for Latin declension and conjugation generation for a language learning application?"**

## Scope

Evaluate libraries for:
- **Latin morphology**: Noun declensions (1st-5th), verb conjugations (1st-4th)
- **Form generation**: Produce all inflected forms from lemma
- **Form parsing**: Analyze inflected form to identify grammatical properties
- **API usability**: Integration ease for quiz generation
- **Accuracy**: Correctness of generated forms
- **Coverage**: Handling of irregular forms and edge cases

### In Scope
- Latin language support (primary focus)
- Greek language support (secondary, if library supports)
- Morphological analysis and generation
- Dictionary lookup capabilities

### Out of Scope
- Modern Romance languages (covered by spaCy in 1.033)
- Syntax parsing and NLP tasks beyond morphology
- Historical linguistics and corpus analysis (unless directly relevant)
- Ancient Greek deep-dive (mention support but focus on Latin)

## Candidate Libraries

### Primary Candidates

1. **CLTK (Classical Language Toolkit)**
   - Version: 1.x (modern) and 0.x (legacy)
   - Focus: Classical languages (Latin, Greek, Sanskrit, etc.)
   - Key feature: CollatinusDecliner for Latin morphology
   - Docs: https://docs.cltk.org/

2. **pyLatinam**
   - Focus: Automated Latin morphology
   - Key feature: Generate full paradigms from base forms
   - PyPI: https://pypi.org/project/pyLatinam/

3. **PyWORDS**
   - Focus: Python implementation of Whitaker's WORDS
   - Key feature: Latin-English dictionary with morphology
   - GitHub: https://github.com/sjgallagher2/PyWORDS

### Secondary Candidates
- **LatMor** - Latin morphological analyzer (if found)
- **Latin dictionaries** - JMdict-style resources for Latin
- **Custom solutions** - Building on existing linguistic resources

## Use Case: Language Learning Application

**Context**: Building `~/spawn-solutions/applications/language-learning/`

**Requirements**:
- Generate quiz questions: "What is the genitive plural of 'puella'?"
- Validate user answers with fuzzy matching
- Support all 5 declensions and 4 conjugations
- Handle irregular forms (sum, possum, eo, fero, etc.)
- Fast enough for interactive quizzes (<100ms per generation)
- Seed database with declension/conjugation paradigms

**Success Criteria**:
- >95% accuracy on standard declension tables
- Covers irregular verbs (sum, possum, eo, fero, volo, nolo, malo)
- API clean enough to abstract into wrapper (experiment 1.624)
- Installation straightforward (minimal binary dependencies)

## Discovery Methodology

Following MPSE framework (S1-S4):

### S1: Rapid Discovery (Target: 1-2 hours)
- Quick install and test of each library
- Generate sample declensions (puella, dominus, rex)
- Identify obvious showstoppers or winners
- Document first impressions

### S2: Comprehensive Discovery (Target: 3-4 hours)
- Deep dive into API documentation
- Test coverage of all 5 declensions
- Test 4 conjugations + irregular verbs
- Performance benchmarking
- Error handling and edge cases

### S3: Need-Driven Discovery (Target: 2-3 hours)
- Map library capabilities to quiz generation use case
- Prototype integration with quiz engine
- Identify gaps and workarounds
- Cost/benefit analysis for each library

### S4: Strategic Discovery (Target: 2-3 hours)
- Long-term maintainability assessment
- Community activity and documentation quality
- Extensibility for Greek and other classical languages
- Build vs adapt vs hybrid approach

**Total estimated time**: 8-12 hours

## Deliverables

1. **S1-S4 Discovery Documents**: Individual methodology reports
2. **DISCOVERY_SYNTHESIS.md**: Cross-methodology analysis and recommendation
3. **Prototype code**: Working examples of each library (in 02-implementations/)
4. **Recommendation**: Primary library choice with rationale
5. **Integration plan**: Path to experiment 1.624 (CLTK wrapper)

## Related Research

- **1.033**: NLP libraries (spaCy, Transformers, NLTK) - Modern language foundation
- **1.100**: Text processing libraries - Text cleaning and validation patterns
- **1.141**: Spaced repetition algorithms - Will consume output of this research
- **1.148**: Morphological analysis - Multi-language morphology (Japanese, Slavic)

## Related Experiments

- **1.624**: CLTK wrapper (library wrapper experiment using 1.610-1.616 pattern)
- **1.850**: Vocabulary database models (store generated forms)
- **1.900**: Spaced repetition algorithm (schedule reviews of generated quizzes)

## Success Metrics

### Technical Metrics
- **Accuracy**: >95% correct forms on standard paradigms
- **Coverage**: All 5 declensions, 4 conjugations, top 20 irregular verbs
- **Performance**: <50ms to generate full declension/conjugation
- **API Quality**: Can abstract into clean wrapper in <4 hours (1.624)

### Business Metrics
- **Installation time**: <15 minutes including dependencies
- **Learning curve**: Can generate first quiz in <1 hour of reading docs
- **Maintenance**: Active development or stable/mature status
- **Cost**: Open source, no API fees

### Strategic Metrics
- **Extensibility**: Can support Greek with same library?
- **Community**: Active maintainers, responsive to issues?
- **Documentation**: Sufficient examples and API reference?
- **Future-proof**: Library likely to exist in 3-5 years?

## Next Steps

1. **S1 Rapid Discovery** (TODAY):
   - Install CLTK, test Latin declension
   - Install pyLatinam, test generation
   - Try PyWORDS (if easily installable)
   - Document in `01-discovery/S1_RAPID_DISCOVERY.md`

2. **S2-S4** (This week):
   - Complete remaining discovery methodologies
   - Benchmark performance
   - Write synthesis document

3. **Recommendation** (End of week):
   - Choose primary library
   - Document rationale
   - Plan experiment 1.624 (wrapper)

## Research Log

- **2025-11-17 15:00**: Project initialized, directory structure created
- **2025-11-17 15:30**: S1 Rapid Discovery - CLTK testing COMPLETE
  - CLTK v1.5.0 tested successfully
  - All 5 declensions working (60/60 forms correct)
  - Verb lemmatization working (12/12 forms correct)
  - 7 additional features tested (macronization, tokenization, etc.)
- **2025-11-17 16:00**: S1 Alternative libraries tested COMPLETE
  - PyWORDS: Dictionary/lookup only, not a generator ❌
  - pyLatinam: Not installable via pip ❌
  - **Decision**: CLTK is clear winner (5/5 stars)
  - See `01-discovery/S1_RESULTS.md` for full details
- **2025-11-17 16:30**: S2 Comprehensive Discovery COMPLETE
  - Performance: 129,000+ words/second ⚡
  - Coverage: 81,906 lemmas in database 📚
  - Edge cases: Handles irregulars, Greek loanwords perfectly ✅
  - API: Full parameter exploration, code format decoded
  - Integration patterns: Quiz generation workflows documented
  - See `01-discovery/S2_RESULTS.md` for full technical assessment
- **2025-11-17 22:40**: S3 Need-Driven Discovery COMPLETE ⭐
  - **CRITICAL FINDING**: User's word-by-word clicking exercise is FULLY FEASIBLE! ✅
  - NLP pipeline provides POS tagging (100% accuracy)
  - Declension identification via XPOS codes (A/B/C/D/E → 1/2/3/4/5)
  - Verb tense identification via XPOS codes (tem1/2/3/4 → present/imperfect/future/perfect)
  - Disambiguated 2nd vs 3rd declension using genitive forms
  - Downloaded: Stanza models (224MB), FastText embeddings (347MB), all Latin corpora
  - Complete parsing workflow implemented and tested
  - See `01-discovery/S3_PARSING_RESULTS.md` for full feasibility assessment
- Next: S4 Strategic Discovery (edge cases, production readiness, long-term maintainability)

---

**Status**: ✅ S1 Complete (60 min) | ✅ S2 Complete (60 min) | ✅ S3 Complete (120 min) | ⬜ S4 Pending
**Next Action**: S4 - Edge cases, poetry/medieval Latin, error handling, production deployment strategy
