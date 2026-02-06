# S1 Rapid Discovery: TMX Libraries

## Critical Name Collision: TMX

**WARNING**: "TMX" refers to TWO completely different file formats:

1. **Translation Memory eXchange (TMX)** - This research
   - XML-based standard for translation memory
   - Used in CAT (Computer-Aided Translation) tools
   - Contains source/target language pairs for translation reuse
   - Industry standard: GALA (Globalization and Localization Association)

2. **Tiled Map XML (TMX)** - NOT this research
   - Game development tile map format
   - Used by Tiled Map Editor
   - Contains sprite sheets, tile layers, collision data
   - Different XML schema entirely

### Why This Matters

The research brief mentioned "tmxlib" - this is a **game tile map library**, NOT a translation memory library. PyPI search for "tmx" returns both types, creating confusion.

**Libraries excluded due to wrong TMX:**
- `tmxlib` - Tiled map editor files (game development)
- `pytmx` - Pygame tile map loader (game development)
- `python-tmx` (DEPRECATED) - Was for translation, now superseded by `hypomnema`

## Libraries Identified

### Native TMX Translation Memory Libraries:

1. **translate-toolkit** (production-ready)
   - Part of comprehensive localization toolkit
   - TMX 1.4 Level 1 support
   - GPL-2.0+ license
   - 933 GitHub stars
   - Latest: v3.18.1 (Jan 2026)

2. **hypomnema** (modern, focused)
   - Full TMX 1.4b Level 2 support (nested inline markup)
   - Type-safe Python 3.12+
   - MIT license
   - 8 GitHub stars
   - Pre-1.0 active development
   - **Note**: Formerly called "python-tmx" (deprecated Dec 2025)

### Indirect TMX Support:

3. **polib** (gettext library with TMX conversion)
   - Mature PO/POT/MO file library
   - **Does NOT natively parse TMX**
   - Enables PO↔TMX via translate-toolkit conversion
   - MIT license
   - Latest: v1.2.0 (Feb 2023)

## Initial Categorization

### By Format Support:
- **Native TMX**: translate-toolkit, hypomnema
- **TMX via conversion**: polib (using translate-toolkit)

### By Maturity:
- **Production-stable**: translate-toolkit, polib
- **Pre-1.0**: hypomnema (active development, breaking changes expected)

### By License:
- **GPL-2.0+**: translate-toolkit (copyleft, requires derivative works to be GPL)
- **MIT**: hypomnema, polib (permissive, commercial-friendly)

## Focus for S1

Analyze all three libraries:
- **translate-toolkit**: The industry standard
- **hypomnema**: The modern alternative
- **polib**: The gettext ecosystem bridge

Document their TMX capabilities, use cases, and when to choose each.
