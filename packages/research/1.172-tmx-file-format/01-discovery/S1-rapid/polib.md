# polib

## Overview

Mature Python library for manipulating gettext PO/POT/MO files. **Does NOT natively parse TMX**, but enables PO↔TMX workflows via translate-toolkit conversion. Widely used in Django, Flask, and other Python web frameworks.

**Package**: `polib` (PyPI)
**License**: MIT
**Status**: Stable/Maintenance mode
**Python**: 2.7-3.11 (wide compatibility)

## Maintenance Status

**Stable/Maintenance** (Mature)

- Latest version: 1.2.0 (Feb 1, 2023)
- History: 10+ years of development
- GitHub: Established user base
- Release cadence: Infrequent (stable, feature-complete)
- Community: Used by Django, Flask localization ecosystems

## Key Capabilities

### Native Format Support
- **PO files**: Gettext Portable Object (human-readable translation format)
- **POT files**: Gettext template files
- **MO files**: Compiled binary translation files
- **TMX**: NOT natively supported (requires translate-toolkit for conversion)

### Core Operations
- Read/write/edit PO/POT/MO files
- Merge translations
- Detect encoding
- Handle plural forms
- Preserve comments and metadata

### TMX Integration Pattern
polib itself does NOT handle TMX. To work with TMX:
1. Use polib for PO file manipulation
2. Use translate-toolkit's `po2tmx` / `tmx2po` for conversion
3. Result: PO-centric workflow with occasional TMX export/import

## Strengths

**Zero dependencies**: Pure Python with no external requirements (no lxml, no C extensions)

**Wide Python support**: Works on Python 2.7-3.11 (broadest compatibility of three libraries)

**Framework integration**: Native support in Django (`makemessages`, `compilemessages`) and Flask-Babel

**Git-friendly format**: PO files are line-based text (easy diffs, merge conflicts, code review)

**Developer-centric**: PO format designed for developers (comments, source code references, fuzzy flags)

**Mature and stable**: 10+ years in production, feature-complete, rare breaking changes

**MIT license**: Commercial-friendly, no copyleft restrictions

## Limitations

**NO native TMX support**: Cannot parse or write TMX directly (must use translate-toolkit as intermediary)

**Format conversion overhead**: PO→TMX→PO round-trip may lose PO-specific metadata (fuzzy flags, comments, locations)

**Python 3.12+ unknown**: No explicit Python 3.12+ testing/support claims

**Minimal type hints**: Limited type annotations compared to modern libraries

**Not for TMX-only workflows**: If project uses TMX as primary format, polib adds unnecessary complexity

## Performance Characteristics

- **Parse speed**: ~5 seconds per 100K entries (PO format, not TMX)
- **Memory overhead**: ~1 KB per entry (PO simpler than TMX XML)
- **TMX conversion**: Additional overhead via translate-toolkit (not measured)

## Best For

**Django/Flask internationalization**: Native framework integration, PO is standard format for these ecosystems

**Developer-centric workflows**: Developers prefer PO (text-based, git-friendly) over TMX (XML-based)

**Version control**: PO files merge better than TMX in git (line-based vs XML)

**Python 2.7 compatibility**: Only option if stuck on Python 2.7 (translate-toolkit and hypomnema require 3.11+/3.12+)

**Zero dependency requirements**: Environments where lxml or C extensions prohibited

## Not Ideal For

**TMX-native workflows**: If CAT tools and translators use TMX as primary format, polib adds conversion step

**Direct TMX manipulation**: No API for TMX parsing/writing (must shell out to translate-toolkit CLI)

**Software localization**: UI strings with inline markup need TMX Level 2 (polib + translate-toolkit only supports Level 1)

**Large-scale translation memories**: PO format not designed for million-unit translation memories (TMX is)

## Ecosystem Position

**PO format specialist**: polib is THE library for gettext PO files in Python. If your workflow is PO-centric, polib is mandatory. TMX support is a bonus via translate-toolkit integration.

**Complementary tool**: Use polib for PO manipulation + translate-toolkit for PO↔TMX conversion = best of both worlds (git-friendly PO for development, TMX for translator exchange)

## Quick Stats

| Metric | Value |
|--------|-------|
| GitHub Community | Established |
| Latest Release | 1.2.0 (Feb 2023) |
| Python Support | 2.7, 3.6-3.11 |
| License | MIT |
| TMX Support | Via conversion only |
| Native Formats | PO, POT, MO |
| Dependencies | None (pure Python) |
| Memory per Entry | ~1 KB |
| Parse Speed (PO) | ~5 sec / 100K entries |

## Decision Factors

**Choose polib if**:
- PO/POT/MO is primary format
- Django/Flask framework used
- Git-friendly format preferred
- Zero dependencies required
- Python 2.7-3.11 compatibility needed
- TMX is secondary (occasional export/import)

**Choose alternative if**:
- TMX is primary format (→ translate-toolkit or hypomnema)
- Need native TMX parsing (→ translate-toolkit or hypomnema)
- Python 3.12+ required (→ translate-toolkit or hypomnema)
- TMX Level 2 needed (→ hypomnema)

## TMX Workflow Pattern

**Typical polib + TMX integration**:

1. **Development**: Use polib to manage PO files (git-friendly, developer workflow)
2. **Export for translators**: Use translate-toolkit `po2tmx` to create TMX for CAT tools
3. **Import from translators**: Use translate-toolkit `tmx2po` to update PO files
4. **Result**: Developers work in PO, translators work in TMX, translate-toolkit bridges the gap

**This pattern works when**:
- Development team uses gettext (Django, Flask, GNU tools)
- Translation team uses CAT tools (Trados, memoQ, OmegaT)
- Both sides benefit from their preferred format

**This pattern fails when**:
- Frequent bidirectional sync required (conversion overhead adds latency)
- TMX Level 2 inline markup needed (conversion loses fidelity)
- Translation memory is primary asset (PO format not ideal for large TM databases)
