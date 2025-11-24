
# S1 Rapid Discovery - Recommendation

**Time Spent**: ~100 minutes
**Confidence Level**: HIGH (Japanese, Russian), MEDIUM-HIGH (Czech)

## Per-Language Winners

| Language | Winner | Downloads/Month | Rationale |
|----------|--------|-----------------|-----------|
| **Japanese** | **SudachiPy** | 1,936,812 | Clear popularity leader (2.7× vs fugashi), modern, multi-granular |
| **Russian** | **pymorphy3** | 584,844 | Morphology specialist, active maintenance, excellent case/aspect analysis |
| **Czech** | **UDPipe** | 52,308 | Best Czech support, June 2024 improvements (50-58% error reduction) |

## Installation

```bash
# Japanese
pip install SudachiPy

# Russian
pip install pymorphy3

# Czech
pip install ufal-udpipe
```

## Key Findings

### Pattern 1: No Unified Solution
Unlike 1.141 (FSRS) and 1.142 (genanki) where one library wins across the board, morphological analysis requires **per-language specialists**:
- **SudachiPy**: Japanese-specific
- **pymorphy3**: Russian-specific (+ Ukrainian)
- **UDPipe**: Multi-language but strongest for Czech

**spaCy could provide unified API** but uses these specialists internally anyway (e.g., spaCy ja_core uses SudachiPy).

### Pattern 2: Popularity Varies by Language Community
- **Japanese**: 1.9M downloads/month (large community, active NLP)
- **Russian**: 585K downloads/month (strong community)
- **Czech**: 52K downloads/month (smaller language community)

Lower Czech adoption reflects language community size, not tool quality.

### Pattern 3: Morphology Specialists Win
All three winners are **morphology-focused** (not general NLP):
- SudachiPy: Japanese morphology + tokenization
- pymorphy3: Russian morphology + inflection
- UDPipe: Multi-language morphology (Universal Dependencies)

**Takeaway**: Don't use general NLP if you need deep morphological analysis.

---

## Implementation Path

### Next Steps (Experiments)

**1.950-japanese-text-parser**:
- Use SudachiPy for tokenization + morphology
- Output JSONL (latin-parse pattern)
- Extract: lemma, POS, reading, particles

**1.951-russian-text-parser**:
- Use pymorphy3 for morphology
- Output JSONL (latin-parse pattern)
- Extract: lemma, POS, case, aspect, gender

**1.952-czech-text-parser**:
- Use UDPipe for morphology
- Output JSONL (latin-parse pattern)
- Extract: lemma, POS, case (7 cases), number, gender

### Application Implementation

**applications/language-learning/**:
- `src/japanese/japanese_train.py` - Interactive trainer (latin-train pattern)
- `src/russian/russian_train.py` - Interactive trainer
- `src/czech/czech_train.py` - Interactive trainer

---

## Trade-offs Accepted

### Unified API vs Accuracy
**Decision**: Choose accuracy (per-language specialists)
**Trade-off**: 3 different APIs instead of unified spaCy API
**Rationale**: Morphology quality critical for language learning

### Installation Complexity
**Decision**: 3 separate packages
**Trade-off**: pip install × 3 vs pip install spacy + models
**Rationale**: Simpler individual installs than managing spaCy models

### Maintenance Burden
**Decision**: Track 3 libraries instead of 1
**Trade-off**: Monitor 3 release cycles
**Rationale**: All actively maintained (2024-2025 releases)

---

## Confidence Assessment

### Japanese: HIGH (9/10)
✅ Clear popularity leader (1.9M downloads/month)
✅ Active development (Jan 2025 release)
✅ Modern technology (Sudachi.rs)
✅ Multi-granular tokenization

### Russian: HIGH (8/10)
✅ Morphology specialist (not general NLP)
✅ Strong adoption (585K downloads/month)
✅ Actively maintained (successor to pymorphy2)
✅ Excellent case + aspect analysis

Only risk: pymorphy3 is newer (2.0.4) vs pymorphy2 (0.9.1 unmaintained)

### Czech: MEDIUM-HIGH (7/10)
✅ Best Czech accuracy (June 2024 improvements)
✅ Academic backing (Charles University)
✅ Universal Dependencies standard
⚠️ Lower adoption (52K downloads/month)
⚠️ Smaller language community

Risk: Lower community = fewer Stack Overflow answers, examples

---

## When to Revisit This Decision

**Reconsider Japanese (SudachiPy)**:
- If SudachiPy development stalls (check GitHub activity)
- If spaCy ja_core significantly improves (check benchmarks)

**Reconsider Russian (pymorphy3)**:
- If pymorphy3 becomes unmaintained (fork like pymorphy2?)
- If spaCy ru_core morphology matches pymorphy3 quality

**Reconsider Czech (UDPipe)**:
- If spaCy Czech model matures (currently experimental)
- If Czech-specific library emerges with better adoption

**General reconsideration signal**:
- Unified spaCy API becomes compelling (if building 10+ languages)
- Per-language specialists become unmaintained

---

## S2/S3 Not Required Because...

**S1 answered key questions**:
1. ✅ Which libraries exist? (SudachiPy, pymorphy3, UDPipe)
2. ✅ Which are popular? (Clear download numbers)
3. ✅ Which are maintained? (All have 2024-2025 releases)
4. ✅ Is there unified solution? (No - per-language specialists win)

**S2 would add** (not needed):
- Detailed API comparison (all have morphology APIs)
- Accuracy benchmarks (pymorphy3/UDPipe papers already show this)
- Performance testing (<100ms/sentence likely for all)

**S3 would add** (not needed):
- Real text validation (popularity suggests they work)
- Integration prototypes (defer to experiments 1.950-1.952)

**Decision**: S1 sufficient - clear winners, high confidence

---

## Hardware Store Philosophy

**"In Stock Now"** (1.148 base):
- Japanese: SudachiPy ✅
- Russian: pymorphy3 ✅
- Czech: UDPipe ✅

**"Catalog Entries"** (1.148.X - LANGUAGE_FAMILIES_ROADMAP.md):
- Arabic, Chinese, Hebrew, ASL, Korean, Turkish, etc.
- Mapped but not researched
- Research when needed (user demand signal)

**Pattern validated**: Per-language specialists > unified general NLP for morphology-intensive tasks

---

## Sources

### Japanese
- [SudachiPy PyPI Stats](https://pypistats.org/packages/sudachipy) - 1.9M downloads/month
- [fugashi PyPI Stats](https://pypistats.org/packages/fugashi) - 720K downloads/month
- [spaCy Japanese Models](https://spacy.io/models/ja)

### Russian
- [pymorphy3 PyPI Stats](https://pypistats.org/packages/pymorphy3) - 585K downloads/month
- [pymorphy2 GitHub](https://github.com/pymorphy2/pymorphy2) - unmaintained
- [spaCy Russian Models](https://spacy.io/models/ru)

### Czech
- [UDPipe PyPI Stats](https://pypistats.org/packages/ufal-udpipe) - 52K downloads/month
- [June 2024 Paper](https://arxiv.org/abs/2406.12422) - Czech improvements
- [UDPipe Web Service](https://lindat.mff.cuni.cz/services/udpipe/)
