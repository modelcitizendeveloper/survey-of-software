# Japanese Morphological Analysis Libraries

## Clear Winner: **SudachiPy**

**PyPI Package**: `SudachiPy`
**Downloads**: 1,936,812/month
**Latest Version**: 0.6.10 (Jan 2025)
**Maintenance**: Active (Nov 2024 release)
**Python Requirement**: 3.x

### Popularity Winner
- **2.7× more downloads** than fugashi (1.9M vs 720K/month)
- Modern development (0.6+ uses Sudachi.rs)
- Multi-granular tokenization (A/B/C split modes)

### Key Features
- Morpheme information (dictionary forms, readings, POS)
- Built-in dictionaries (sudachidict_small/core/full)
- Active development by Works Applications

### Installation
```bash
pip install SudachiPy
# Dictionary included by default (sudachidict_core)
```

---

## Alternative: fugashi (MeCab wrapper)

**PyPI Package**: `fugashi`
**Downloads**: 720,141/month
**Latest Version**: 1.5.2
**Maintenance**: Active

### Why Consider
- ✅ Pythonic MeCab wrapper (Cython-based)
- ✅ Classic MeCab reliability (2003+)
- ✅ UniDic dictionary support

### Why Not Winner
- ⚠️ 2.7× fewer downloads than SudachiPy
- ⚠️ Requires dictionary installation (unidic-lite or unidic)
- ⚠️ MeCab is older technology (SudachiPy more modern)

---

## Alternative: spaCy Japanese (ja_core)

**Models**: ja_core_news_sm/md/lg
**Maintenance**: Active (spaCy ecosystem)

### Why Consider
- ✅ Unified API (same as other languages)
- ✅ Full NLP pipeline (not just morphology)

### Why Not Winner
- ⚠️ **Uses SudachiPy internally** for tokenization
- ⚠️ Heavier (full NLP vs morphology specialist)
- ⚠️ Morphology = subset of what SudachiPy provides

---

## Recommendation

**Use SudachiPy** for japanese-parse implementation.

**Rationale**:
1. Clear popularity leader (1.9M downloads/month)
2. Modern, actively maintained (2024-2025 releases)
3. Multi-granular tokenization (flexible parsing)
4. spaCy uses it internally anyway

**Confidence**: HIGH (9/10)

## Sources
- [SudachiPy PyPI](https://pypi.org/project/SudachiPy/)
- [SudachiPy GitHub](https://github.com/WorksApplications/SudachiPy)
- [fugashi PyPI](https://pypi.org/project/fugashi/)
- [spaCy Japanese Models](https://spacy.io/models/ja)
