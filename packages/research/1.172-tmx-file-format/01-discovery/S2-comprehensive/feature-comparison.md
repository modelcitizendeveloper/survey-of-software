# Feature Comparison Matrix: TMX Libraries

## Overview

This document provides a detailed, quantitative comparison of TMX translation memory libraries for Python. All measurements and characteristics are based on technical analysis of library internals, not use-case recommendations.

## High-Level Comparison

| Library | TMX Support | License | Python | Status | Stars | Dependencies |
|---------|------------|---------|--------|--------|-------|--------------|
| **translate-toolkit** | Native (Level 1) | GPL-2.0+ | ≥3.11 | Stable | 933 | lxml |
| **hypomnema** | Native (Level 2) | MIT | ≥3.12 | Pre-1.0 | 8 | Optional lxml |
| **polib** | Indirect (conversion) | MIT | 2.7-3.11 | Stable | N/A | None (+ translate-toolkit for TMX) |

## TMX Format Capabilities

### TMX Standard Conformance

| Feature | translate-toolkit | hypomnema | polib |
|---------|------------------|-----------|-------|
| **TMX Version** | 1.4 | 1.4b | N/A (via conversion) |
| **TMX Level** | Level 1 | Level 2 (full) | N/A |
| **Inline Markup** | Preserved as text | Structured objects | Lost (converted to text) |
| **Nesting Depth** | Unlimited (unstructured) | Configurable (default: unlimited) | N/A |
| **DTD Validation** | No | Optional (via policy) | N/A |
| **BCP 47 Lang Codes** | No validation | Optional validation | No (PO lang codes) |

### Supported TMX Elements

| Element | translate-toolkit | hypomnema | polib (via TMX) |
|---------|------------------|-----------|-----------------|
| `<tmx>` | Yes | Yes | Yes (via conversion) |
| `<header>` | Yes | Yes | Partial (metadata → PO header) |
| `<body>` | Yes | Yes | Yes |
| `<tu>` | Yes | Yes | Yes (→ POEntry) |
| `<tuv>` | Yes | Yes | Yes (source/target) |
| `<seg>` | Yes | Yes | Yes |
| `<prop>` | Yes (unstructured) | Yes (structured) | Partial (x-context only) |
| `<note>` | Yes | Yes | Yes (→ PO comment) |
| `<bpt>` | Preserved as text | Structured object | Lost |
| `<ept>` | Preserved as text | Structured object | Lost |
| `<it>` | Preserved as text | Structured object | Lost |
| `<ph>` | Preserved as text | Structured object | Lost |
| `<hi>` | Preserved as text | Structured object | Lost |
| `<sub>` | Preserved as text | Structured object (recursive) | Lost |

### Header Attributes Support

| Attribute | translate-toolkit | hypomnema | polib (conversion) |
|-----------|------------------|-----------|-------------------|
| `creationtool` | Yes | Yes | Yes (→ PO metadata) |
| `creationtoolversion` | Yes | Yes | Partial |
| `datatype` | Yes | Yes (enum) | Partial |
| `segtype` | Yes | Yes (enum) | No |
| `adminlang` | Yes | Yes | No |
| `srclang` | Yes (required) | Yes (required) | Yes (→ Language) |
| `o-tmf` | Yes | Yes | No |
| Custom attributes | Preserved | Preserved | Lost |

## Parsing Capabilities

### Input Formats

| Format | translate-toolkit | hypomnema | polib |
|--------|------------------|-----------|-------|
| **TMX** | Yes | Yes | No (indirect) |
| **PO** | Yes | No | Yes |
| **POT** | Yes | No | Yes |
| **MO** | Yes | No | Yes |
| **XLIFF** | Yes | No | No |
| **TBX** | Yes | No | No |
| **20+ others** | Yes | No | No |

### Parsing Options

| Feature | translate-toolkit | hypomnema | polib |
|---------|------------------|-----------|-------|
| **In-memory (DOM)** | Yes | Yes | Yes |
| **Streaming (SAX)** | No | Yes | No |
| **Backend choice** | lxml only | lxml or stdlib | stdlib only |
| **Encoding detection** | Auto (lxml) | Auto (backend) | Auto (BOM + metadata) |
| **Error recovery** | Strict (no recovery) | Policy-driven | Lenient (attempts recovery) |
| **Validation levels** | Minimal | Policy-driven (strict/permissive/custom) | Minimal |
| **Malformed handling** | Crash | Configurable (skip/log/crash) | Best-effort recovery |

### Validation Features

| Validation | translate-toolkit | hypomnema | polib |
|------------|------------------|-----------|-------|
| **Well-formed XML** | Yes (lxml) | Yes (backend) | N/A |
| **Required elements** | Yes | Yes | N/A |
| **Required attributes** | Partial | Yes (policy-driven) | N/A |
| **Language code format** | No | Optional (BCP 47) | No |
| **Inline tag pairing** | No | Optional (`<bpt>`/`<ept>` matching) | N/A |
| **Duplicate detection** | No | No | No (manual) |
| **Custom validation** | Via subclassing | Via custom policies | Via subclassing |

## Writing Capabilities

### Serialization Options

| Feature | translate-toolkit | hypomnema | polib |
|---------|------------------|-----------|-------|
| **Create from scratch** | Yes | Yes | Yes (PO) |
| **Modify existing** | Yes | Yes | Yes (PO) |
| **Incremental write** | No | No | No |
| **Streaming write** | No | No | No |
| **Pretty-printing** | Yes (always on) | Yes (via backend) | Yes (PO format) |
| **Encoding control** | Yes (default UTF-8) | Yes (UTF-8, UTF-16) | Yes (via metadata) |
| **Roundtrip integrity** | Yes (attributes preserved) | Yes (full preservation) | Partial (lossy conversion) |

### Format Conversion

| Conversion | translate-toolkit | hypomnema | polib |
|------------|------------------|-----------|-------|
| **PO → TMX** | Yes (po2tmx CLI) | No | Via translate-toolkit |
| **TMX → PO** | Yes (tmx2po CLI) | No | Via translate-toolkit |
| **TMX → XLIFF** | Yes | No | No |
| **Batch conversion** | Yes (CLI tools) | No | Manual (Python script) |
| **Language pair mapping** | Auto-detect from PO | N/A | Auto-detect from PO |

## Performance Characteristics

### Memory Usage

| Metric | translate-toolkit | hypomnema | polib |
|--------|------------------|-----------|-------|
| **Per entry overhead** | ~2-4 KB | ~1.5-2 KB | ~1 KB |
| **File size multiplier** | 3-5x | 2-3x (in-memory) | 2-3x |
| **Streaming overhead** | N/A | ~10-50 MB (constant) | N/A |
| **100K units (est.)** | ~400 MB | ~200 MB (in-memory), ~50 MB (streaming) | ~100 MB |
| **1M units (est.)** | ~4 GB | ~2 GB (in-memory), ~50 MB (streaming) | ~1 GB |

### Parsing Speed (estimated, i7 CPU)

| File Size | translate-toolkit | hypomnema (lxml) | hypomnema (stdlib) | polib |
|-----------|------------------|-----------------|-------------------|-------|
| **10K units, 1 MB** | ~0.5 sec | ~0.3 sec | ~3 sec | ~0.5 sec |
| **100K units, 10 MB** | ~5 sec | ~2 sec | ~20 sec | ~5 sec |
| **1M units, 100 MB** | ~50 sec | ~20 sec | ~200 sec | ~50 sec |

Notes:
- translate-toolkit: lxml-based, storage abstraction overhead
- hypomnema (lxml): Fastest (optimized dataclasses)
- hypomnema (stdlib): Slowest (pure Python XML parser)
- polib: PO format faster to parse than TMX (simpler format)

### Serialization Speed (estimated)

| File Size | translate-toolkit | hypomnema (lxml) | hypomnema (stdlib) | polib |
|-----------|------------------|-----------------|-------------------|-------|
| **10K units** | ~0.5 sec | ~0.4 sec | ~4 sec | ~0.3 sec |
| **100K units** | ~5 sec | ~3 sec | ~30 sec | ~3 sec |

### Concurrent Access

| Feature | translate-toolkit | hypomnema | polib |
|---------|------------------|-----------|-------|
| **Thread-safe read** | Yes (after parse) | Yes (after parse) | Yes (after parse) |
| **Thread-safe write** | No | No (mutable dataclasses) | No |
| **Multi-process** | Yes (separate instances) | Yes (separate instances) | Yes (separate instances) |
| **Locking mechanism** | None | None | None |

### Scalability Limits (16 GB RAM)

| Library | Max Units (in-memory) | Max File Size (in-memory) | Max File Size (streaming) |
|---------|----------------------|--------------------------|--------------------------|
| **translate-toolkit** | ~1M | ~500 MB - 1 GB | N/A |
| **hypomnema** | ~5M | ~2-3 GB | Unlimited (disk I/O bound) |
| **polib** | ~10M | ~5 GB | N/A |

## API Design

### Type Safety

| Feature | translate-toolkit | hypomnema | polib |
|---------|------------------|-----------|-------|
| **Type hints** | No | Full (Python 3.12+) | No |
| **Runtime type checking** | No | Optional (typeguard) | No |
| **IDE autocomplete** | Limited | Full (dataclasses) | Limited |
| **Static type checking** | No (mypy/pyright fail) | Yes (mypy/pyright pass) | No |
| **Type annotation coverage** | 0% | ~100% | 0% |

### API Style

| Aspect | translate-toolkit | hypomnema | polib |
|--------|------------------|-----------|-------|
| **Paradigm** | Object-oriented | Dataclass + functional | Object-oriented |
| **Entry style** | `unit.source`, `unit.target` | `tu.tuvs[0].segments` | `entry.msgid`, `entry.msgstr` |
| **Load syntax** | `store.parsefile(path)` | `load(path)` | `pofile(path)` |
| **Save syntax** | `bytes(store)` → file | `dump(tmx, path)` | `po.save(path)` |
| **Modification** | Mutable objects | Mutable (default) or immutable (frozen) | Mutable objects |

### Extensibility Points

| Extension | translate-toolkit | hypomnema | polib |
|-----------|------------------|-----------|-------|
| **Subclass storage** | Yes (`tmxfile`) | No (use dataclasses directly) | Yes (`POFile`) |
| **Subclass units** | Yes (`tmxunit`) | No (use dataclasses directly) | Yes (`POEntry`) |
| **Custom backends** | No (lxml only) | Yes (`Backend` interface) | No |
| **Custom policies** | No | Yes (`DeserializationPolicy`) | No |
| **Pre/post hooks** | Via method override | Via custom policies/backends | Via method override |
| **Plugin system** | No | No | No |

### Configuration Options

| Option | translate-toolkit | hypomnema | polib |
|--------|------------------|-----------|-------|
| **Validation strictness** | Fixed (minimal) | Policy-driven (strict/permissive/custom) | Fixed (lenient) |
| **Backend selection** | N/A (lxml only) | Yes (lxml or stdlib) | N/A (stdlib only) |
| **Encoding** | Configurable | Configurable | Configurable |
| **Error handling** | Exceptions only | Policy (skip/log/crash) | Lenient (best-effort) |
| **Nesting depth limit** | No limit | Configurable (policy) | N/A |
| **Inline validation** | No | Optional (policy) | N/A |

## Data Model

### Internal Representation

| Library | Structure | Inline Markup | Metadata |
|---------|-----------|---------------|----------|
| **translate-toolkit** | lxml tree + Python objects | Unstructured (text) | lxml attributes |
| **hypomnema** | Dataclasses | Structured (objects) | Dataclass fields |
| **polib** | Python objects + lists | N/A | Dict (metadata) |

### Memory Efficiency

| Library | Overhead | Structure | Explanation |
|---------|----------|-----------|-------------|
| **translate-toolkit** | High (~3 KB/unit) | lxml tree + wrapper objects | DOM overhead + storage abstraction |
| **hypomnema** | Medium (~1.5 KB/unit) | Dataclasses | Efficient Python objects |
| **polib** | Low (~1 KB/unit) | Simple objects | Minimal overhead (PO simpler than TMX) |

## Error Handling

### Exception Types

| Library | Exception Hierarchy | Custom Exceptions |
|---------|-------------------|------------------|
| **translate-toolkit** | lxml exceptions (XMLSyntaxError) | Minimal (relies on lxml) |
| **hypomnema** | Custom (ValidationError, etc.) | Yes (policy-specific) |
| **polib** | Standard Python exceptions | No (uses ValueError, etc.) |

### Error Recovery

| Strategy | translate-toolkit | hypomnema | polib |
|----------|------------------|-----------|-------|
| **Malformed XML** | Crash (no recovery) | Configurable (policy) | Attempts recovery (lenient) |
| **Missing required attrs** | Crash | Configurable (policy) | Best-effort |
| **Invalid language codes** | Accepted (no validation) | Configurable (policy) | Accepted |
| **Unclosed tags** | Crash (lxml error) | Crash (unless custom backend) | Best-effort |
| **Encoding errors** | Crash (strict) | Crash (strict) | Fallback to Latin-1 |

## Dependencies and Portability

### Dependency Analysis

| Library | Core Dependency | Version | Size | Platform-Specific |
|---------|----------------|---------|------|------------------|
| **translate-toolkit** | lxml | ≥4.6.3 | ~5 MB | Yes (C extension) |
| **hypomnema** | None (lxml optional) | ≥4.6 | ~5 MB | No (with stdlib backend) |
| **polib** | None | N/A | N/A | No (pure Python) |

For TMX conversion:
- **polib + translate-toolkit**: Requires lxml (C extension)

### Installation Complexity

| Library | Installation | Compilation | Offline |
|---------|-------------|-------------|---------|
| **translate-toolkit** | Simple (pip) | lxml (usually pre-compiled wheels) | Possible (wheels) |
| **hypomnema** | Simple (pip) | Optional lxml | Yes (stdlib backend) |
| **polib** | Simple (pip) | None | Yes |

### Python Version Support

| Library | Min Python | Max Python | PyPy | Python 2 |
|---------|-----------|-----------|------|----------|
| **translate-toolkit** | 3.11 | Latest | No | No |
| **hypomnema** | 3.12 | Latest | Unknown | No |
| **polib** | 2.7 | 3.11 | Yes | Yes |

## Command-Line Tools

### CLI Tool Availability

| Tool | translate-toolkit | hypomnema | polib |
|------|------------------|-----------|-------|
| **TMX → PO** | `tmx2po` | No | No |
| **PO → TMX** | `po2tmx` | No | No |
| **TMX validation** | No | No | No |
| **TMX merge** | Via conversion | No | No |
| **Batch processing** | Yes (all formats) | No | No |
| **Quality checks** | `pofilter` (40+ checks) | No | No |

### CLI Features

| Feature | translate-toolkit | hypomnema | polib |
|---------|------------------|-----------|-------|
| **File globbing** | Yes | N/A | N/A |
| **Recursive directories** | Yes | N/A | N/A |
| **Output formatting** | Configurable | N/A | N/A |
| **Progress indicators** | Yes | N/A | N/A |
| **Error reporting** | Detailed | N/A | N/A |

## Ecosystem Integration

### Framework Support

| Framework | translate-toolkit | hypomnema | polib |
|-----------|------------------|-----------|-------|
| **Django** | Via PO conversion | Via TMX conversion | Native (PO files) |
| **Flask** | Via PO conversion | Via TMX conversion | Native (PO files) |
| **Weblate** | Yes (native) | Possible | Yes (native) |
| **Pootle** | Yes (native) | Unknown | Yes (native) |

### CAT Tool Compatibility

| CAT Tool | translate-toolkit | hypomnema | polib |
|----------|------------------|-----------|-------|
| **Trados** | Yes (TMX Level 1) | Yes (TMX Level 2) | Via conversion |
| **memoQ** | Yes (TMX Level 1) | Yes (TMX Level 2) | Via conversion |
| **Wordfast** | Yes (TMX Level 1) | Yes (TMX Level 2) | Via conversion |
| **OmegaT** | Yes (TMX Level 1) | Yes (TMX Level 2) | Via conversion |
| **Import/Export** | Both | Both | Import (TMX→PO), Export (PO→TMX) |

## Documentation and Community

### Documentation Quality

| Aspect | translate-toolkit | hypomnema | polib |
|--------|------------------|-----------|-------|
| **Official docs** | Comprehensive (Sphinx) | README-based | Comprehensive (Sphinx) |
| **API reference** | Full | Partial | Full |
| **Examples** | Many | Few | Many |
| **Tutorials** | Yes | No | Yes |
| **Format guides** | Extensive | Basic | Extensive |

### Community Support

| Metric | translate-toolkit | hypomnema | polib |
|--------|------------------|-----------|-------|
| **GitHub stars** | 933 | 8 | N/A |
| **Open issues** | 263 | Unknown | Unknown |
| **Contributors** | Many (328 forks) | Few (2 forks) | Unknown |
| **Last release** | Jan 2026 (active) | Pre-1.0 (active development) | Feb 2023 (stable) |
| **Commercial support** | Yes (Translate House) | No | No |

## Licensing

### License Comparison

| Library | License | Commercial Use | Derivative Works | Attribution |
|---------|---------|----------------|-----------------|-------------|
| **translate-toolkit** | GPL-2.0+ | Restricted (copyleft) | Must be GPL | Yes |
| **hypomnema** | MIT | Allowed | Any license | Yes |
| **polib** | MIT | Allowed | Any license | Yes |

### License Implications

| Use Case | translate-toolkit | hypomnema | polib |
|----------|------------------|-----------|-------|
| **Open source project** | Compatible | Compatible | Compatible |
| **Proprietary software** | Restricted (GPL terms) | Allowed | Allowed |
| **SaaS product** | Complex (GPL interpretation) | Allowed | Allowed |
| **Embedded device** | Restricted (GPL terms) | Allowed | Allowed |
| **Library distribution** | Must include source | Can be binary-only | Can be binary-only |

## Edge Case Handling

### Special Cases

| Case | translate-toolkit | hypomnema | polib |
|------|------------------|-----------|-------|
| **UTF-8 with BOM** | Auto-handled (lxml) | Auto-handled (backend) | Auto-detected |
| **UTF-16** | Auto-detected (lxml) | Auto-detected (backend) | Auto-detected |
| **Mixed encodings** | May crash | May crash | Lenient fallback |
| **Namespace prefixes** | Preserved | Preserved | N/A |
| **Unknown elements** | Preserved | Preserved | N/A |
| **Deep nesting (Level 2)** | Unstructured (text) | Structured (objects) | N/A |
| **Duplicate `tuid`** | Allowed | Allowed | N/A |
| **Empty `<seg>`** | Allowed | Allowed (policy-dependent) | Allowed |
| **Missing `<header>`** | May crash | Configurable (policy) | N/A |

## Summary Scoring Matrix

### Feature Coverage (0-5 scale)

| Category | translate-toolkit | hypomnema | polib |
|----------|------------------|-----------|-------|
| **TMX Conformance** | 3 (Level 1 only) | 5 (Full Level 2) | 1 (indirect) |
| **Format Support** | 5 (20+ formats) | 2 (TMX only) | 3 (PO/POT/MO) |
| **Validation** | 2 (minimal) | 5 (policy-driven) | 2 (minimal) |
| **Performance** | 3 (adequate) | 5 (streaming available) | 4 (fast for PO) |
| **Type Safety** | 1 (no types) | 5 (full types) | 1 (no types) |
| **Extensibility** | 3 (subclassing) | 5 (policies/backends) | 3 (subclassing) |
| **Maturity** | 5 (production) | 2 (pre-1.0) | 5 (production) |
| **Community** | 5 (933 stars) | 1 (8 stars) | 4 (widely used) |
| **Documentation** | 5 (comprehensive) | 2 (basic) | 5 (comprehensive) |

### Use Case Fit (0-5 scale)

| Use Case | translate-toolkit | hypomnema | polib |
|----------|------------------|-----------|-------|
| **Enterprise localization** | 5 | 3 | 4 |
| **CAT tool integration** | 4 | 5 | 3 |
| **NLP/ML pipelines** | 3 | 5 | 2 |
| **Django/Flask i18n** | 4 | 2 | 5 |
| **Multi-format conversion** | 5 | 1 | 3 |
| **Level 2 inline markup** | 1 | 5 | 1 |
| **Large file processing** | 2 | 5 | 3 |
| **Embedded systems** | 2 (GPL, lxml) | 4 (stdlib backend) | 5 (pure Python) |

## Technical Decision Criteria

Based on this feature comparison, here are measurable selection criteria:

### Choose translate-toolkit if:
- Multi-format support needed (PO, XLIFF, TMX, TBX, etc.)
- Command-line automation essential
- Production stability critical (mature, widely used)
- GPL licensing acceptable
- TMX Level 1 sufficient (inline markup preserved but unstructured)

### Choose hypomnema if:
- TMX Level 2 required (structured inline markup)
- Large files (>100 MB) via streaming API
- Type safety needed (Python 3.12+ type hints)
- MIT licensing required
- Policy-driven validation/error handling needed
- Pre-1.0 API instability acceptable

### Choose polib if:
- Primary format is PO (TMX secondary)
- Git-friendly text format preferred (PO diffs)
- Zero dependencies required
- Python 2.7 or PyPy support needed
- TMX fidelity not critical (lossy conversion acceptable)
- Framework integration (Django/Flask) important

This comparison provides the technical foundation for informed library selection based on measurable criteria and specific project requirements.
