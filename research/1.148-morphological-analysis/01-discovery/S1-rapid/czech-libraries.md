# Czech Morphological Analysis Libraries

## Winner: **UDPipe**

**PyPI Package**: `ufal-udpipe`
**Downloads**: 52,308/month
**Latest Update**: June 2024 (improved Czech support)
**Maintenance**: Active (Charles University)
**Python Requirement**: 3.x

### Best Czech Support
- Academic backing (Charles University Prague)
- **June 2024 improvements**: 50% error reduction in lemmatization, 58% in POS tagging
- Universal Dependencies format
- 7 cases correctly identified

### Key Features
- Morphological dictionary-supplemented deep learning
- Lemmatization, POS tagging, dependency parsing
- Trained on PDT-C 1.0 (Prague Dependency Treebank)
- Web service + Python client

### Installation
```bash
pip install ufal-udpipe
```

---

## Alternative: spaCy Czech

**Models**: Experimental Czech support
**Maintenance**: Active (spaCy ecosystem)

### Why Consider
- ✅ Unified API (same as other languages)
- ✅ spaCy ecosystem familiarity

### Why Not Winner
- ⚠️ **Experimental** (not mature)
- ⚠️ UDPipe has better Czech accuracy (50-58% error reduction)
- ⚠️ UDPipe is Czech-specialist

---

## Alternative: MorphoDiTa

**Source**: Czech-specific morphological analyzer
**Maintenance**: Academic

### Why Consider
- ✅ Czech-specific tool
- ✅ Academic backing

### Why Not Winner
- ⚠️ Harder to find Python bindings
- ⚠️ UDPipe supersedes it (June 2024 paper shows improvements)
- ⚠️ Less popular in Python ecosystem

---

## Recommendation

**Use UDPipe** for czech-parse implementation.

**Rationale**:
1. Best Czech support (June 2024 improvements)
2. 50% lemmatization error reduction vs alternatives
3. 7 cases correctly handled
4. Python client available
5. Universal Dependencies format (standard)

**Caveat**:
- Lower adoption (52K downloads/month vs 585K for Russian, 1.9M for Japanese)
- But this reflects Czech being smaller language community
- Still viable and actively maintained

**Confidence**: MEDIUM-HIGH (7/10)
- High confidence in quality (academic backing, recent improvements)
- Medium confidence in ecosystem (lower adoption than Japanese/Russian)

## Sources
- [UDPipe PyPI](https://pypi.org/project/ufal-udpipe/)
- [UDPipe Web Service](https://lindat.mff.cuni.cz/services/udpipe/)
- [June 2024 Paper](https://arxiv.org/abs/2406.12422) - Improved Czech support
- [UDPipe 2](https://ufal.mff.cuni.cz/udpipe/2)
- [spaCy Czech](https://spacy.io/models) - Experimental
