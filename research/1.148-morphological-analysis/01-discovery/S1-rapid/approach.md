# S1: Rapid Discovery - Approach

**Methodology**: Rapid Library Search (speed-focused)
**Time Box**: 90-120 minutes maximum
**Goal**: Identify viable libraries for Japanese, Russian, Czech morphological analysis

## Core Philosophy

Quickly map the solution space for each language:
- What libraries exist?
- Which are popular/actively maintained?
- Can they produce JSONL output (latin-parse pattern)?
- Is there a unified solution (spaCy) or per-language specialists?

## Discovery Process

### 1. Japanese Libraries (25 min)
- **MeCab**: Classic Japanese morphological analyzer (2003)
- **fugashi**: Modern Python wrapper for MeCab
- **SudachiPy**: Modern Japanese tokenizer (2017)
- **spaCy**: General NLP with Japanese model

Check:
- PyPI downloads, GitHub stars
- Installation complexity (system dependencies?)
- Output format (can we get lemma + POS + reading?)

### 2. Russian Libraries (25 min)
- **pymorphy2**: Morphology specialist for Russian
- **spaCy**: General NLP with Russian model
- **UDPipe**: Universal Dependencies parser

Check:
- Accuracy for case + aspect identification
- Performance (<100ms per sentence?)
- API usability

### 3. Czech Libraries (25 min)
- **UDPipe**: Universal Dependencies (best Czech support)
- **spaCy**: Experimental Czech model
- **MorphoDiTa**: Czech-specific morphological analyzer

Check:
- 7 cases correctly identified?
- Installation ease
- Active maintenance

### 4. Unified vs Specialist Decision (15 min)
- **Option A**: spaCy for all three (unified API)
- **Option B**: Per-language specialists (MeCab, pymorphy2, UDPipe)
- **Option C**: Hybrid (spaCy where good, specialists where needed)

Trade-offs:
- API consistency vs accuracy
- Installation complexity vs performance
- Maintenance burden vs optimal results

### 5. Quick Recommendation (10 min)
- Default library per language
- Confidence level
- When to reconsider (S2/S3 signals)

## Evaluation Criteria

**Primary**:
- Popularity (PyPI downloads, GitHub stars)
- Active maintenance (last commit, open issues)
- Installation ease (pip install vs binary deps)

**Secondary**:
- Accuracy (if easily testable)
- Performance (if documented)
- Documentation quality

**Tertiary**:
- API consistency across languages
- Community size

## Output Files

- `approach.md` (this file)
- `japanese-libraries.md` - MeCab vs SudachiPy vs spaCy
- `russian-libraries.md` - pymorphy2 vs spaCy vs UDPipe
- `czech-libraries.md` - UDPipe vs spaCy vs MorphoDiTa
- `recommendation.md` - Per-language recommendations + unified decision

## Success Criteria

- Found 2-3 viable options per language
- Clear popularity leader identified (or not)
- Can answer: "What should I use for each language?"
- Total time: <120 minutes

## Note for S2/S3

S1 identifies viable options. If no clear winner per language:
- **S2**: Deep-dive accuracy testing, API comparison
- **S3**: Validate against real Japanese/Russian/Czech texts

This research likely needs more than S1 (3 languages, complex trade-offs).
