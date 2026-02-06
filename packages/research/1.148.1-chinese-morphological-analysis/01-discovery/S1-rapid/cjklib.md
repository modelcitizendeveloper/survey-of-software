# cjklib - Rapid Assessment

## Overview

Han character library for CJKV languages (Chinese, Japanese, Korean, Vietnamese). Provides character-level routines including pronunciations, radicals, glyph components, stroke decomposition, and variant information.

**Repository:** [GitHub - cburgmer/cjklib](https://github.com/cburgmer/cjklib)

**Documentation:** [cjklib 0.3.2 docs](https://cjklib.readthedocs.io/en/latest/)

## Character Decomposition Capabilities

**Strengths:**
- **Explicit character decomposition** using Ideographic Description Sequences (IDS)
- Binary operators (e.g., ⿰ for left-right: 好 = ⿰女子)
- Trinary operators for three-component decomposition
- Radical analysis (Kangxi radicals)
- Stroke information derivable from component data
- Character variant mapping

**Example Use Cases:**
- Character lookup by components
- Font design pattern analysis
- Character study and etymology
- Stroke order/count deduction

## Morphological Analysis (Word Level)

**None** - cjklib operates at character level, not word level. No word segmentation or compound word analysis.

## Maturity

**Moderate concerns:**
- Last documented version: 0.3.2
- Documentation references Python 2.x
- No 2026 updates found in search
- Available on PyPI: [cjklib package](https://pypi.org/project/cjklib/)

**Maintenance status unclear** - GitHub repository exists but update frequency unknown from initial search.

## Quick Verdict

**Good for:** Character decomposition, radical analysis, IDS manipulation, character structure study
**Limitations:** Python 2 legacy, maintenance unclear, no word-level morphology

cjklib is the **only library reviewed that explicitly handles character decomposition**. It directly addresses our character structure needs but may require Python 3 compatibility verification.

## Complementary Option

[makemeahanzi](https://github.com/skishore/makemeahanzi) - Free, open-source Chinese character data with decomposition information (mentioned in search results as related project).

---

Sources:
- [cjklib GitHub Repository](https://github.com/cburgmer/cjklib)
- [cjklib Documentation](https://cjklib.readthedocs.io/en/0.3.2/)
- [CharacterLookup Module](https://cjklib.readthedocs.io/en/0.3.2/library/cjklib.characterlookup.html)
- [makemeahanzi Alternative](https://github.com/skishore/makemeahanzi)
