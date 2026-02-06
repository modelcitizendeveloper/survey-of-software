# hypomnema

## Overview

Modern, type-safe Python library focused exclusively on TMX (Translation Memory eXchange) format. Built for Python 3.12+ with full type hints, streaming API, and TMX 1.4b Level 2 support (nested inline markup).

**Package**: `hypomnema` (PyPI, formerly `python-tmx`)
**License**: MIT
**Status**: Pre-1.0 (active development)
**Python**: ≥3.12

**Note**: `python-tmx` package deprecated December 2025, superseded by `hypomnema`.

## Maintenance Status

**Active Development** (Pre-1.0)

- Current: Pre-release development phase
- History: Renamed from python-tmx (Dec 2025)
- GitHub: 8 stars (small community)
- Maintainer: Single-author project (Enzo Agosta)
- Breaking changes expected until 1.0 release

## Key Capabilities

### TMX Conformance
- **Level**: Full TMX 1.4b Level 2 support
- **Parsing**: Structured inline markup (`<bpt>`, `<ept>`, `<it>`, `<ph>`, `<hi>`)
- **Writing**: Roundtrip integrity with nested elements
- **Validation**: Policy-driven (strict/permissive/custom)

### Architecture Highlights
- **Type-safe**: Full Python 3.12+ type annotations
- **Dataclass-based**: Efficient memory representation (1.5-2 KB per unit)
- **Backend-agnostic**: Optional lxml (fast) or stdlib XML (portable)
- **Policy-driven**: Configure parsing strictness per use case

### Streaming API
**Unique feature**: Constant-memory streaming for large TMX files
- Parse multi-GB files without loading entire file into memory
- ~50 MB RAM regardless of file size
- Sequential access (suitable for ETL pipelines, corpus extraction)

### Validation Policies
- **Strict**: Reject malformed TMX (standards-compliant only)
- **Permissive**: Best-effort parsing (recover from real-world errors)
- **Custom**: Define error handling per field/element

## Strengths

**TMX Level 2 support**: ONLY Python library with full nested inline markup (essential for software localization with UI formatting)

**Streaming capability**: Process 1M+ translation units on laptops without memory exhaustion

**Type safety**: Full type hints enable IDE autocomplete, static analysis, early error detection

**MIT license**: Commercial-friendly, embed in proprietary software without copyleft restrictions

**Modern Python**: Built for Python 3.12+, idiomatic dataclass patterns, no legacy cruft

**Backend flexibility**: Choose lxml (2x faster) or stdlib XML (zero C dependencies)

## Limitations

**Pre-1.0 status**: API breaking changes expected, not recommended for risk-averse production

**Small community**: 8 GitHub stars, limited Stack Overflow coverage, single maintainer risk

**Python 3.12+ only**: Cannot use in codebases stuck on Python 3.11 or earlier

**TMX-only**: No multi-format support (no PO, XLIFF, TBX) - must use translate-toolkit for conversions

**Documentation**: README-based, no comprehensive tutorial or API reference site

**No CLI tools**: Python API only, requires scripting for automation (unlike translate-toolkit's `po2tmx`)

## Performance Characteristics

- **Parse speed (lxml backend)**: ~2 seconds per 100K units (fastest option)
- **Parse speed (stdlib backend)**: ~20 seconds per 100K units (portable but slower)
- **Memory overhead**: 1.5-2 KB per unit (most efficient of three libraries)
- **Streaming mode**: Constant ~50 MB RAM for any file size

## Best For

**NLP/ML pipelines**: Extract parallel corpora from TMX for machine translation training (streaming API handles large datasets)

**Software localization**: UI strings with inline markup (`<b>`, `<a>`, variables) require Level 2 support

**Commercial CAT tools**: MIT license allows embedding in proprietary translation software

**Modern Python projects**: Type-safe codebases on Python 3.12+ benefit from full annotations

**Custom validation**: Policy-driven parsing handles vendor-specific TMX extensions gracefully

## Not Ideal For

**Production-critical systems**: Pre-1.0 API instability risks breaking changes during upgrades

**Multi-format workflows**: No native PO/XLIFF support (must integrate with translate-toolkit)

**Legacy Python**: Projects on Python 3.11 or earlier cannot use hypomnema

**Risk-averse teams**: Small community means limited support, single-maintainer dependency

**Command-line automation**: No CLI tools, requires Python scripting

## Ecosystem Position

**Modern specialist**: Hypomnema is the "precision tool" - focused on TMX Level 2 excellence, streaming performance, and type safety.

**Strategic bet**: Choosing hypomnema is betting on modern Python patterns over legacy stability. High reward (best-in-class TMX Level 2 + streaming) with risk (pre-1.0, small community).

## Quick Stats

| Metric | Value |
|--------|-------|
| GitHub Stars | 8 |
| Latest Status | Pre-1.0 |
| Python Support | 3.12+ |
| License | MIT |
| TMX Level | Level 2 (full) |
| Formats Supported | TMX only |
| Dependencies | lxml (optional) |
| Memory per Unit | 1.5-2 KB |
| Parse Speed (lxml) | ~2 sec / 100K units |
| Parse Speed (stdlib) | ~20 sec / 100K units |
| Streaming | Yes (constant memory) |

## Decision Factors

**Choose hypomnema if**:
- TMX Level 2 required (nested inline markup)
- MIT license needed for commercial use
- Large files require streaming (>500 MB)
- Type safety priority (Python 3.12+)
- TMX-only focus acceptable

**Choose alternative if**:
- Production stability required (→ translate-toolkit)
- Pre-1.0 risk unacceptable (→ translate-toolkit)
- Multi-format needed (→ translate-toolkit)
- Python <3.12 required (→ translate-toolkit or polib)
- Large community desired (→ translate-toolkit)

## Pre-1.0 Risk Mitigation

If choosing hypomnema despite pre-1.0 status:
1. Pin exact version in requirements.txt
2. Monitor GitHub for breaking changes
3. Vendor the library if stability critical
4. Have migration path to translate-toolkit ready
5. Contribute to community (increase maintainer support)
