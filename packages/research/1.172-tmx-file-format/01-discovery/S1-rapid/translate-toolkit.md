# translate-toolkit

## Overview

Production-ready localization toolkit with comprehensive TMX (Translation Memory eXchange) support. Part of Translate House's ecosystem, widely used by major open-source localization platforms.

**Package**: `translate-toolkit` (PyPI)
**License**: GPL-2.0-or-later
**Status**: Production/Stable
**Python**: ≥3.11

## Maintenance Status

**Actively Maintained** (January 2026)

- Latest version: 3.18.1 (Jan 14, 2026)
- Regular releases: Monthly cadence (3.17.0-3.18.1 in Nov 2025-Jan 2026)
- GitHub: 933 stars, 328 forks, 263 open issues
- Community: Active development, used by Weblate and Pootle
- History: 15+ years of continuous development

## Key Capabilities

### TMX Conformance
- **Level**: TMX 1.4 Level 1 conformance
- **Parsing**: Reads TMX translation memory files
- **Writing**: Generates TMX from translation data
- **Markup**: Preserves inline formatting (does NOT strip markup)

### Format Ecosystem
TMX is one of **20+ supported formats**:
- Primary: PO, XLIFF, TMX, TBX
- Development: Properties, RC, RESX, DTD
- Office: OpenOffice.org GSI/SDF
- Other: Qt .ts, CSV, WordFast, subtitles

### Command-Line Tools
- `po2tmx` / `tmx2po`: Format conversion
- `pofilter`: 40+ translation quality checks
- `pocount`: Word count and analysis
- `pretranslate`: Apply translation memory
- `poterminology`: Extract terminology

### Python API
- Storage abstraction layer (unified API across formats)
- Programmatic TMX manipulation
- Batch processing capabilities
- Translation unit iteration and filtering

## Strengths

**Comprehensive toolkit**: Multi-format support means one tool for entire localization workflow (PO ↔ TMX ↔ XLIFF conversions)

**Production-proven**: Used by major platforms (Weblate, Pootle), 15+ years in production, extensive real-world validation

**Command-line automation**: Ready-to-use CLI tools for CI/CD pipelines, no Python knowledge required for basic operations

**Quality assurance**: Built-in 40+ translation checks (variables, punctuation, consistency) integrated with TMX workflows

**Active maintenance**: Monthly releases, responsive to issues, security-conscious (signed commits)

## Limitations

**GPL licensing**: Copyleft license requires derivative works to be GPL (may restrict commercial use in proprietary software)

**TMX Level 1 only**: Does NOT support TMX Level 2 nested inline markup (e.g., `<bpt>`, `<ept>` tags for complex formatting)

**Memory usage**: Loads entire TMX into memory (5x file size multiplier) - 10 MB file = 50 MB RAM

**Python 3.11+ only**: Dropped support for Python 3.10 and earlier (as of late 2025)

**lxml dependency**: Requires C-compiled lxml library (not pure Python)

## Performance Characteristics

- **Parse speed**: ~5 seconds per 100K translation units (adequate for most workflows)
- **Memory overhead**: 2-4 KB per translation unit (lxml DOM + wrapper objects)
- **Scalability**: Suitable for files up to 500 MB; larger files require splitting or batch processing

## Best For

**Multi-format localization workflows**: Teams working with PO, XLIFF, and TMX need unified conversion pipeline

**Open-source projects**: GPL license aligns with open-source ecosystems (Django, GNOME, KDE)

**Enterprise localization platforms**: Production stability and comprehensive tooling justify GPL restrictions

**CLI automation**: DevOps teams prefer command-line tools over Python API

**Weblate/Pootle integration**: Native support in these platforms

## Not Ideal For

**Commercial proprietary software**: GPL licensing complicates embedding in closed-source products (workaround: use CLI tools without importing library)

**TMX Level 2 requirements**: Software localization with nested inline markup needs hypomnema instead

**Large file streaming**: Files >500 MB need constant-memory streaming (hypomnema offers this)

**Pure Python environments**: lxml C dependency may complicate deployment in restricted environments

**Modern type-safe codebases**: Limited type hints compared to newer libraries

## Ecosystem Position

**De facto standard** for Python-based localization automation. Translate-toolkit is the "Swiss Army Knife" - if you need TMX + 20 other formats + QA tools + CLI automation, this is the proven choice.

**Strategic dependency**: Weblate (20K+ stars) and Pootle depend on translate-toolkit, ensuring long-term viability.

## Quick Stats

| Metric | Value |
|--------|-------|
| GitHub Stars | 933 |
| Latest Release | 3.18.1 (Jan 2026) |
| Python Support | 3.11+ |
| License | GPL-2.0-or-later |
| TMX Level | Level 1 |
| Formats Supported | 20+ |
| Dependencies | lxml (required) |
| Memory per Unit | 2-4 KB |
| Parse Speed | ~5 sec / 100K units |

## Decision Factors

**Choose translate-toolkit if**:
- Production stability is priority
- Multi-format support needed (PO, XLIFF, TMX)
- Command-line automation required
- GPL licensing acceptable
- Weblate/Pootle integration planned

**Choose alternative if**:
- MIT license required (→ hypomnema, polib)
- TMX Level 2 needed (→ hypomnema)
- Streaming large files (→ hypomnema)
- Pure Python required (→ polib for PO, convert to TMX)
