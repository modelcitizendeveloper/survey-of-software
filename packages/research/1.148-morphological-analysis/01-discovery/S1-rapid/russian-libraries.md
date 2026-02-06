# Russian Morphological Analysis Libraries

## Clear Winner: **pymorphy3**

**PyPI Package**: `pymorphy3`
**Downloads**: 584,844/month
**Latest Version**: 2.0.4
**Maintenance**: Active (successor to pymorphy2)
**Python Requirement**: 3.9-3.14

### Morphology Specialist
- **Dedicated Russian morphology** (not general NLP)
- Successor to pymorphy2 (original is unmaintained)
- 585K downloads/month = strong adoption

### Key Features
- Case identification (6 cases: nominative, genitive, dative, accusative, instrumental, prepositional)
- Aspect analysis (perfective/imperfective)
- Gender, number, tense, person
- Inflection engine (generate forms from lemma)

### Installation
```bash
pip install pymorphy3
```

---

## Alternative: spaCy Russian (ru_core)

**Models**: ru_core_news_sm/md/lg
**Components**: morphologizer, lemmatizer, parser
**Maintenance**: Active

### Why Consider
- ✅ Unified API (same as other languages)
- ✅ Full NLP pipeline (NER, dependency parsing)
- ✅ Token.morph for morphological features

### Why Not Winner
- ⚠️ General NLP (not morphology specialist)
- ⚠️ pymorphy3 has deeper morphology analysis
- ⚠️ Trained on Nerus dataset (good but not specialized)

---

## Alternative: UDPipe

**PyPI Package**: `ufal-udpipe`
**Downloads**: 52,308/month
**Maintenance**: Active (v1 and v2)

### Why Consider
- ✅ Universal Dependencies format
- ✅ Multi-language support
- ✅ Academic backing (Charles University)

### Why Not Winner
- ⚠️ 11× fewer downloads than pymorphy3
- ⚠️ Czech is its strength, not Russian
- ⚠️ More complex setup than pymorphy3

---

## Recommendation

**Use pymorphy3** for russian-parse implementation.

**Rationale**:
1. Morphology specialist (not general NLP)
2. Strong adoption (585K downloads/month)
3. Actively maintained (successor to pymorphy2)
4. Excellent case + aspect analysis (critical for Russian)
5. Simple API for morphological parsing

**When to consider spaCy**:
- If building unified multi-language parser with same API
- If need full NLP pipeline (NER, dependency parsing)

**Confidence**: HIGH (8/10)

## Sources
- [pymorphy3 PyPI](https://pypi.org/project/pymorphy3/)
- [pymorphy2 GitHub](https://github.com/pymorphy2/pymorphy2) - original (unmaintained)
- [spaCy Russian Models](https://spacy.io/models/ru)
- [UDPipe](https://ufal.mff.cuni.cz/udpipe)
