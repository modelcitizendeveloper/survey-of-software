# Technical Selection Criteria: TMX Libraries

## Purpose of This Document

This document provides TECHNICAL EVALUATION CRITERIA for selecting TMX translation memory libraries, not prescriptive recommendations. It maps technical requirements to library capabilities, enabling informed decisions based on measurable characteristics.

**Not included**: Use case narratives (reserved for S3)

**Included**: Technical trade-off analysis, risk assessment, capability mapping

## Technical Requirement Categories

### 1. TMX Standard Compliance

**Requirement**: Level of TMX 1.4b conformance needed

| Level | Description | Library Support |
|-------|-------------|----------------|
| **Level 1 (Basic)** | Inline tags preserved as text, no nesting structure | translate-toolkit |
| **Level 2 (Full)** | Structured inline markup, arbitrary nesting depth | hypomnema |
| **Conversion-based** | TMX via PO format bridge, metadata loss acceptable | polib + translate-toolkit |

**Evaluation criteria**:
- Does application need to manipulate inline markup programmatically? → Level 2 required
- Is inline markup display-only (pass-through)? → Level 1 sufficient
- Is TMX export-only (from PO files)? → Conversion-based acceptable

**Technical risk**:
- **Level 1 limitation**: Cannot validate `<bpt>`/`<ept>` pairing, cannot reorder inline elements
- **Level 2 requirement**: Smaller library ecosystem, pre-1.0 stability risk
- **Conversion loss**: `tuid`, properties, flags lost in round-trip

### 2. File Size and Memory Constraints

**Requirement**: Maximum file size and available RAM

| Scenario | Memory Requirement | Library Capability |
|----------|-------------------|-------------------|
| **Small** (<10 MB, <100K units) | Any | All libraries adequate |
| **Medium** (10-100 MB, 100K-1M units) | 2-8 GB RAM | All libraries (in-memory) |
| **Large** (100 MB-1 GB, 1M-10M units) | 8-32 GB RAM | hypomnema (streaming) or external chunking |
| **Very large** (>1 GB, >10M units) | Streaming required | hypomnema (streaming API) |

**Memory overhead calculations**:
- translate-toolkit: File size × 3-5 (e.g., 100 MB → 300-500 MB RAM)
- hypomnema (in-memory): File size × 2-3 (e.g., 100 MB → 200-300 MB RAM)
- hypomnema (streaming): ~50 MB constant (file size independent)
- polib (PO): File size × 2-3 (PO files smaller than TMX)

**Evaluation criteria**:
- Available RAM < file size × 5? → Streaming required (hypomnema only)
- Batch processing multiple large files? → Streaming or multi-process (hypomnema)
- Embedded/resource-constrained? → polib (lowest overhead, pure Python)

**Technical risk**:
- **In-memory parsing**: Out-of-memory crash on files exceeding RAM budget
- **Streaming limitation**: Sequential access only, cannot modify in-place
- **External chunking**: Manual file splitting, coordination overhead

### 3. Performance Requirements

**Requirement**: Parse/write speed and throughput

| Metric | translate-toolkit | hypomnema (lxml) | hypomnema (stdlib) | polib |
|--------|------------------|-----------------|-------------------|-------|
| **Parse speed** | Medium (~5 sec/100K units) | Fast (~2 sec/100K units) | Slow (~20 sec/100K units) | Medium (~5 sec/100K units PO) |
| **Memory efficiency** | Low (3-5x overhead) | Medium (2-3x overhead) | Medium (2-3x overhead) | High (2-3x overhead, simpler format) |
| **Concurrent read** | Safe (after parse) | Safe (after parse) | Safe (after parse) | Safe (after parse) |
| **Concurrent write** | Unsafe | Unsafe | Unsafe | Unsafe |

**Evaluation criteria**:
- Parse time critical (real-time)? → hypomnema (lxml backend)
- Memory critical? → polib (if PO format acceptable) or hypomnema (streaming)
- Concurrent writes needed? → Multi-process architecture (all libraries)
- Batch processing? → hypomnema (streaming) or parallel processes

**Technical risk**:
- **lxml dependency**: C-compiled, platform-specific builds (may fail on obscure platforms)
- **stdlib backend**: 10-100x slower, but zero dependencies
- **Thread safety**: No built-in locking, must use external synchronization

### 4. Validation and Error Handling

**Requirement**: Strictness of validation, malformed file handling

| Strategy | translate-toolkit | hypomnema | polib |
|----------|------------------|-----------|-------|
| **Validation level** | Minimal (well-formed XML only) | Policy-driven (strict/permissive/custom) | Minimal (lenient) |
| **Error recovery** | None (strict, crash on error) | Configurable (skip/log/crash) | Best-effort (attempts recovery) |
| **Schema validation** | No (no DTD/XSD) | Optional (via policy) | N/A |
| **Inline tag pairing** | No | Optional (policy-driven) | N/A |

**Evaluation criteria**:
- Messy real-world files (malformed, missing attributes)? → hypomnema (permissive policy) or polib (lenient)
- Strict conformance required (regulatory, quality)? → hypomnema (strict policy)
- Simple workflows (trusted sources)? → translate-toolkit (adequate)
- Custom validation logic needed? → hypomnema (custom policies) or subclassing

**Technical risk**:
- **Strict parsing**: Single error crashes entire parse (no partial results)
- **Lenient parsing**: Silent data corruption on malformed input
- **Policy complexity**: Configuration overhead, learning curve

### 5. Type Safety and Development Experience

**Requirement**: Static typing, IDE support, debugging

| Feature | translate-toolkit | hypomnema | polib |
|---------|------------------|-----------|-------|
| **Type annotations** | None (0% coverage) | Full (100% coverage) | None (0% coverage) |
| **IDE autocomplete** | Limited (docstrings) | Full (dataclasses) | Limited (docstrings) |
| **Static type checking** | No (mypy/pyright fail) | Yes (mypy/pyright pass) | No (mypy/pyright fail) |
| **Runtime type checking** | No | Optional (typeguard) | No |

**Evaluation criteria**:
- Type safety critical (large codebase, team)? → hypomnema (Python 3.12+)
- Python <3.12 required? → translate-toolkit or polib (no type safety)
- Rapid prototyping, small scripts? → Any library (types less critical)
- IDE-driven development? → hypomnema (best autocomplete)

**Technical risk**:
- **No type safety**: Runtime errors not caught until execution
- **Python 3.12+ requirement**: Excludes older Python versions, conservative environments
- **Learning curve**: Type-safe APIs may be less intuitive for Python 2 developers

### 6. Extensibility and Customization

**Requirement**: Custom validation, backends, policies

| Extension Point | translate-toolkit | hypomnema | polib |
|----------------|------------------|-----------|-------|
| **Custom validation** | Subclassing (limited) | Custom policies (full) | Subclassing (limited) |
| **Custom backends** | No (lxml only) | Yes (Backend interface) | No (stdlib only) |
| **Pre/post hooks** | Method override | Custom policies/backends | Method override |
| **Plugin system** | No | No | No |

**Evaluation criteria**:
- Custom XML parser needed (e.g., performance, features)? → hypomnema (custom backend)
- Custom error handling (logging, recovery, reporting)? → hypomnema (custom policies)
- Simple extensions (add metadata, validation)? → Subclassing (all libraries)
- No customization needed? → translate-toolkit (comprehensive out-of-box)

**Technical risk**:
- **Limited extensibility**: Subclassing fragile across library updates
- **Custom backend complexity**: Significant implementation effort
- **Policy design**: Over-configuration leads to complexity

### 7. Licensing and Distribution

**Requirement**: License compatibility with project

| License | translate-toolkit | hypomnema | polib |
|---------|------------------|-----------|-------|
| **License** | GPL-2.0+ (copyleft) | MIT (permissive) | MIT (permissive) |
| **Derivative works** | Must be GPL | Any license | Any license |
| **Commercial use** | Complex (copyleft) | Allowed | Allowed |
| **SaaS products** | Uncertain (GPL interpretation) | Allowed | Allowed |
| **Binary distribution** | Source required | Allowed | Allowed |

**Evaluation criteria**:
- Proprietary software? → MIT required (hypomnema or polib)
- Open source project? → GPL compatible (all libraries)
- SaaS product? → MIT preferred (licensing clarity)
- Library embedding? → MIT required (binary-only distribution allowed)

**Technical risk**:
- **GPL copyleft**: Derivative works must be GPL-licensed (legal complexity)
- **GPL interpretation**: "Linking" vs "using" ambiguity in Python
- **Commercial legal review**: May require legal counsel for GPL compliance

### 8. Python Version and Platform Support

**Requirement**: Python version, platform constraints

| Requirement | translate-toolkit | hypomnema | polib |
|-------------|------------------|-----------|-------|
| **Python version** | ≥3.11 | ≥3.12 | 2.7-3.11, PyPy |
| **Platform** | Most (lxml wheels) | All (stdlib) or most (lxml) | All (pure Python) |
| **Compilation** | lxml (C extension) | Optional lxml | None |
| **Offline install** | Wheels available | Possible (stdlib backend) | Yes (pure Python) |

**Evaluation criteria**:
- Python 2.7 or PyPy required? → polib only
- Python 3.11 required? → translate-toolkit or polib
- Python 3.12+ available? → hypomnema (best type safety)
- Obscure platform (no lxml wheels)? → polib or hypomnema (stdlib backend)
- Air-gapped environment? → polib (zero dependencies) or hypomnema (stdlib)

**Technical risk**:
- **lxml compilation**: May fail on platforms without libxml2/libxslt
- **Python version lock-in**: Upgrading library may require Python upgrade
- **PyPy performance**: polib only option, but PyPy may be slower for this workload

### 9. Multi-Format Support

**Requirement**: Support for formats beyond TMX

| Format Support | translate-toolkit | hypomnema | polib |
|---------------|------------------|-----------|-------|
| **TMX** | Yes (Level 1) | Yes (Level 2) | Indirect (conversion) |
| **PO/POT/MO** | Yes | No | Yes (native) |
| **XLIFF** | Yes | No | No |
| **TBX, RC, Properties, etc.** | Yes (20+ formats) | No | No |

**Evaluation criteria**:
- TMX-only workflow? → hypomnema (specialized, efficient)
- PO primary, TMX secondary? → polib + translate-toolkit (conversion)
- Multi-format localization pipeline? → translate-toolkit (comprehensive)
- Format migration (PO → TMX, XLIFF → TMX)? → translate-toolkit (converters)

**Technical risk**:
- **Single-format lock-in**: Future format changes require library migration
- **Conversion overhead**: External tool dependency, lossy conversions
- **Comprehensive toolkit weight**: Large dependency for TMX-only use

### 10. Maturity and Community Support

**Requirement**: Production stability, commercial backing

| Aspect | translate-toolkit | hypomnema | polib |
|--------|------------------|-----------|-------|
| **Status** | Stable (10+ years) | Pre-1.0 (active dev) | Stable (10+ years) |
| **Breaking changes** | Rare | Expected (pre-1.0) | Rare |
| **GitHub stars** | 933 | 8 | N/A |
| **Commercial support** | Yes (Translate House) | No | No |
| **Community** | Large | Small | Medium |

**Evaluation criteria**:
- Production critical system? → translate-toolkit or polib (stable)
- Greenfield project, bleeding edge? → hypomnema (modern features)
- Commercial support required? → translate-toolkit only
- Breaking changes acceptable? → hypomnema (pre-1.0 caveat)
- Long-term maintenance (10+ years)? → translate-toolkit or polib (proven longevity)

**Technical risk**:
- **Pre-1.0 instability**: API changes may require code updates
- **Small community**: Fewer third-party resources, slower issue resolution
- **No commercial backing**: Maintenance dependent on single developer (hypomnema)
- **Mature library stagnation**: Slower to adopt new features (translate-toolkit, polib)

## Technical Trade-Off Analysis

### Memory vs Speed

**Trade-off**: Faster parsing often requires more memory

| Library | Memory (100K units) | Parse Time (100K units) |
|---------|-------------------|------------------------|
| **translate-toolkit** | ~400 MB | ~5 sec |
| **hypomnema (in-memory, lxml)** | ~200 MB | ~2 sec |
| **hypomnema (streaming, lxml)** | ~50 MB | ~2 sec |
| **polib** | ~100 MB (PO format) | ~5 sec |

**Decision criteria**:
- Memory constrained, speed flexible? → Streaming (hypomnema)
- Speed critical, memory abundant? → In-memory with lxml (hypomnema or translate-toolkit)
- Both constrained? → polib (if PO format acceptable)

### Type Safety vs Compatibility

**Trade-off**: Type safety (Python 3.12+) vs broad Python support (2.7+)

| Requirement | Type Safety | Python Compatibility |
|-------------|-------------|---------------------|
| **Modern codebase (3.12+)** | hypomnema (full types) | N/A |
| **Mixed versions (3.11)** | No types available | translate-toolkit or polib |
| **Legacy (2.7, PyPy)** | No types available | polib only |

**Decision criteria**:
- Type safety > compatibility? → hypomnema (Python 3.12+ required)
- Compatibility > type safety? → translate-toolkit or polib
- Both needed? → Impossible (choose priority)

### Strictness vs Leniency

**Trade-off**: Strict validation (catch errors early) vs lenient (handle messy data)

| Library | Strictness | Error Handling |
|---------|-----------|----------------|
| **translate-toolkit** | Minimal (crashes on XML errors) | Strict (no recovery) |
| **hypomnema** | Configurable (policy-driven) | Configurable (skip/log/crash) |
| **polib** | Minimal (lenient) | Best-effort (attempts recovery) |

**Decision criteria**:
- Trusted sources, quality control? → Strict (translate-toolkit default or hypomnema strict policy)
- Real-world messy data? → Lenient (polib or hypomnema permissive policy)
- Custom needs (log errors, skip units)? → Configurable (hypomnema)

### Specialization vs Generalization

**Trade-off**: TMX-only library vs multi-format toolkit

| Library | Specialization | Formats Supported |
|---------|---------------|-------------------|
| **translate-toolkit** | Generalized | TMX + 20+ formats |
| **hypomnema** | Specialized | TMX only (Level 2) |
| **polib** | Specialized | PO/POT/MO (TMX via conversion) |

**Decision criteria**:
- TMX-only workflow? → Specialized (hypomnema: simpler, smaller)
- Multi-format pipeline? → Generalized (translate-toolkit: one tool)
- PO-centric, TMX secondary? → Specialized (polib + conversion)

### Stability vs Features

**Trade-off**: Production-stable API vs cutting-edge features

| Aspect | Stable (translate-toolkit, polib) | Cutting-edge (hypomnema) |
|--------|----------------------------------|--------------------------|
| **API stability** | High (rare breaking changes) | Low (pre-1.0, changes expected) |
| **Features** | Adequate (Level 1, no streaming) | Advanced (Level 2, streaming) |
| **Risk** | Low (proven in production) | Medium (newer, smaller community) |

**Decision criteria**:
- Production critical? → Stable (translate-toolkit or polib)
- Level 2 required? → Accept risk (hypomnema only option)
- Experimental, R&D? → Cutting-edge (hypomnema features)

## Risk Assessment Framework

### Technical Risks (Probability × Impact)

| Risk | translate-toolkit | hypomnema | polib |
|------|------------------|-----------|-------|
| **Out of memory (large files)** | High × High | Low × Low (streaming) | Medium × Medium |
| **Performance bottleneck** | Low × Medium | Very Low × Medium | Low × Medium |
| **Breaking API changes** | Very Low × High | High × Medium (pre-1.0) | Very Low × High |
| **Dependency failures (lxml)** | Low × High | Low × Medium (stdlib fallback) | Very Low × Low |
| **License compliance issues** | Medium × High (GPL) | Very Low × Low (MIT) | Very Low × Low (MIT) |
| **Unsupported platform** | Low × Medium (lxml) | Very Low × Low (stdlib) | Very Low × Low |
| **Level 2 inadequacy** | High × High (Level 1 only) | Very Low × Medium | High × Medium (conversion) |
| **Community abandonment** | Very Low × High | Medium × High (small community) | Low × Medium |

### Risk Mitigation Strategies

**For translate-toolkit**:
- Large file risk → External chunking, database-backed TM
- GPL risk → Legal review, consider alternative for proprietary use
- Level 1 limitation → Accept (if Level 2 not needed) or migrate to hypomnema

**For hypomnema**:
- Pre-1.0 risk → Pin version, monitor releases, allocate update time
- Small community → Vendor code (fork if necessary), contribute fixes
- Python 3.12+ requirement → Ensure infrastructure supports before commitment

**For polib**:
- Indirect TMX → Accept conversion losses or use native TMX library
- No streaming → Batch process, multi-process architecture
- Infrequent updates → Fork if critical bug found, contribute patch

## Capability Mapping Table

### Requirement → Library Mapping

| Technical Requirement | Best Fit | Alternative | Not Suitable |
|----------------------|----------|-------------|--------------|
| **TMX Level 2 (structured inline)** | hypomnema | - | translate-toolkit, polib |
| **Large files (>1 GB)** | hypomnema (streaming) | External chunking | translate-toolkit, polib (in-memory) |
| **Type safety (Python 3.12+)** | hypomnema | - | translate-toolkit, polib |
| **Production stability** | translate-toolkit, polib | - | hypomnema (pre-1.0) |
| **Multi-format support** | translate-toolkit | - | hypomnema, polib |
| **PO-centric workflow** | polib | translate-toolkit | hypomnema |
| **Zero dependencies** | polib | hypomnema (stdlib) | translate-toolkit (lxml) |
| **Python 2.7 / PyPy** | polib | - | translate-toolkit, hypomnema |
| **MIT licensing** | hypomnema, polib | - | translate-toolkit (GPL) |
| **Command-line tools** | translate-toolkit | - | hypomnema, polib |
| **Custom validation logic** | hypomnema (policies) | Subclassing (all) | - |
| **Streaming API** | hypomnema | - | translate-toolkit, polib |

## Decision Matrix Template

Use this matrix to score libraries against your requirements:

| Requirement | Weight (1-5) | translate-toolkit | hypomnema | polib |
|-------------|-------------|------------------|-----------|-------|
| TMX Level 2 support | ___ | 1 | 5 | 1 |
| Large file handling (>1 GB) | ___ | 1 | 5 | 2 |
| Production stability | ___ | 5 | 2 | 5 |
| Type safety | ___ | 1 | 5 | 1 |
| MIT licensing | ___ | 1 | 5 | 5 |
| Multi-format support | ___ | 5 | 1 | 3 |
| Python 2.7 support | ___ | 1 | 1 | 5 |
| Memory efficiency | ___ | 2 | 4 | 5 |
| Parse speed | ___ | 3 | 5 | 3 |
| Community size | ___ | 5 | 1 | 4 |
| **Total (weighted sum)** | | ___ | ___ | ___ |

**Instructions**:
1. Assign weight (1-5) to each requirement based on project priority
2. Multiply requirement score × weight for each library
3. Sum weighted scores
4. Highest score = best technical fit

**Note**: This is a starting point. Add/remove requirements based on specific needs.

## Quantitative Selection Criteria

### Hard Requirements (Go/No-Go)

These are binary criteria. If not met, library is eliminated:

- [ ] Python version available (e.g., must support 3.11)
- [ ] License compatible (e.g., must be MIT, not GPL)
- [ ] Platform supported (e.g., must work on ARM64)
- [ ] TMX Level required (e.g., must support Level 2)
- [ ] Memory constraint (e.g., must handle 10 GB file in 8 GB RAM)

### Measurable Criteria (Numeric Thresholds)

Set thresholds based on requirements:

- Parse speed: ___ seconds for ___ units (e.g., <10 sec for 100K units)
- Memory usage: ___ MB for ___ units (e.g., <500 MB for 100K units)
- Community size: ___ GitHub stars minimum (e.g., >100 stars)
- Release frequency: Last release within ___ months (e.g., 12 months)

### Qualitative Criteria (Ranked Preferences)

Order by importance (1 = most important):

1. ___
2. ___
3. ___

(e.g., 1. Type safety, 2. Streaming API, 3. Documentation quality)

## Technical Evaluation Checklist

Before selecting a library, verify:

**Functional requirements**:
- [ ] Parses required TMX files (test with sample data)
- [ ] Writes valid TMX files (validate with CAT tool import)
- [ ] Handles expected file sizes (benchmark with realistic data)
- [ ] Supports required inline markup level (Level 1 vs 2)
- [ ] Validation level adequate (strict, permissive, custom)

**Non-functional requirements**:
- [ ] Performance acceptable (parse/write speed benchmarked)
- [ ] Memory usage within limits (profiled with realistic data)
- [ ] License compatible (legal review if necessary)
- [ ] Python version available (infrastructure support confirmed)
- [ ] Platform supported (test on target platform)

**Operational requirements**:
- [ ] Installation tested (pip install, dependencies resolved)
- [ ] Documentation adequate (API reference, examples available)
- [ ] Community support acceptable (issue tracker active)
- [ ] Maintenance status confirmed (recent releases, active development)

**Integration requirements**:
- [ ] API ergonomics acceptable (test with prototype code)
- [ ] Error handling adequate (test with malformed files)
- [ ] Extensibility sufficient (custom validation, backends tested if needed)
- [ ] Framework compatibility (Django, Flask, etc. if applicable)

## Summary: Technical Decision Framework

This document provides:
1. **Requirement categories**: 10 technical dimensions for evaluation
2. **Trade-off analysis**: Explicit costs/benefits of each choice
3. **Risk assessment**: Probability × impact for each library
4. **Capability mapping**: Requirement → best-fit library lookup
5. **Decision matrix**: Quantitative scoring template
6. **Evaluation checklist**: Pre-selection verification steps

**Next steps** (not in this document, reserved for S3):
- Use case narratives
- Integration examples
- Workflow patterns
- Migration guides

This S2 analysis provides the technical foundation for informed library selection based on measurable characteristics and explicit trade-offs.
