# Requirement-Driven Selection Guide: TMX Libraries

## Purpose of This Document

This guide provides **conditional selection criteria** for TMX translation memory libraries based on requirements, constraints, and use case characteristics. Instead of prescriptive "use library X" recommendations, it offers decision trees: "If requirement A AND constraint B, then library X fits because [reason]."

**Cross-reference**: See persona files (use-case-*.md) for detailed context. This document distills common selection patterns.

## Quick Selection Decision Tree

```
START: I need a TMX library for Python

├─ Commercial product (proprietary)?
│  ├─ YES → MIT licensing required
│  │  ├─ TMX Level 2 needed (structured inline markup)?
│  │  │  ├─ YES → hypomnema (only MIT + Level 2 option)
│  │  │  └─ NO → Can you accept pre-1.0 risk?
│  │  │     ├─ YES → hypomnema (type safety, streaming)
│  │  │     └─ NO → Build custom parser or wait for hypomnema 1.0
│  │  └─ TMX via conversion only (PO primary)?
│  │     └─ polib (PO manipulation) + translate-toolkit CLI (po2tmx)
│  │
│  └─ NO → GPL acceptable
│     ├─ Multi-format needed (PO, XLIFF, TBX, etc.)?
│     │  └─ YES → translate-toolkit (20+ formats)
│     ├─ CLI tools preferred (no coding)?
│     │  └─ YES → translate-toolkit (po2tmx, tmx2po, pofilter)
│     └─ Large files (>1 GB)?
│        ├─ YES → hypomnema (streaming) or external chunking
│        └─ NO → translate-toolkit (adequate for <1 GB)
```

## Selection by Primary Requirement

### Requirement: TMX Level 2 (Structured Inline Markup)

**When needed**:
- Software localization with complex UI formatting (nested bold, links, placeholders)
- Linguistic research requiring inline tag analysis (NER, alignment patterns)
- Lossless round-trip with professional CAT tools (Trados, memoQ Level 2 workflows)

**Selection**:
- **Primary fit**: hypomnema (only library with full Level 2 support)
- **Acceptable workaround**: translate-toolkit (Level 1) + manual XPath for tag extraction (lossy, complex)
- **Not suitable**: polib (no native TMX, conversion loses inline markup)

**Trade-offs**:
- hypomnema: Pre-1.0 API instability, Python 3.12+ requirement
- translate-toolkit: GPL licensing, Level 1 only (inline tags as text, not structured objects)

**Recommendation**: If Level 2 is must-have, hypomnema is only practical option. Accept pre-1.0 risk (pin version) or wait for 1.0 release.

### Requirement: Large File Handling (>1 GB)

**When needed**:
- Enterprise TMs with 10M+ translation units
- NLP research on large parallel corpora (DGT-TM, OPUS)
- LSP consolidating client TMs into corporate memory

**Selection**:
- **Primary fit**: hypomnema (streaming API, constant ~50 MB RAM)
- **Workarounds**:
  - translate-toolkit + external chunking (split TMX into smaller files)
  - Database-backed storage (parse once, store in PostgreSQL, export on demand)
- **Not suitable**: polib (in-memory only, no streaming)

**Memory calculations** (for in-memory libraries):
- translate-toolkit: File size × 3-5 (e.g., 1 GB → 3-5 GB RAM)
- hypomnema (in-memory): File size × 2-3 (e.g., 1 GB → 2-3 GB RAM)
- hypomnema (streaming): ~50 MB constant (file size independent)

**Recommendation**: If file size > available RAM ÷ 3, use hypomnema streaming. Otherwise, in-memory adequate.

### Requirement: Type Safety (Python 3.12+)

**When needed**:
- Large codebase (10K+ lines of code)
- Team development (static checking prevents errors)
- Reproducible research (type errors caught before experiments)
- Commercial CAT tool development (production quality critical)

**Selection**:
- **Primary fit**: hypomnema (full type hints, mypy/Pylance compatible)
- **No alternatives**: translate-toolkit and polib have zero type hints

**Trade-offs**:
- hypomnema: Python 3.12+ requirement (excludes older infrastructure)
- Alternative: Add type stubs for translate-toolkit/polib (significant effort, unofficial)

**Recommendation**: If type safety critical and Python 3.12+ deployable, hypomnema only option. Otherwise, accept untyped APIs.

### Requirement: Multi-Format Support (Beyond TMX)

**When needed**:
- LSPs handling diverse client formats (PO, XLIFF, TBX, RC, Properties)
- Enterprise localization pipelines (developer PO files → translator TMX)
- Format migration projects (legacy formats → modern standards)

**Selection**:
- **Primary fit**: translate-toolkit (20+ formats: PO, XLIFF, TBX, RC, etc.)
- **Hybrid approach**: Format-specific libraries (polib for PO, lxml for XLIFF) + hypomnema for TMX
- **Not suitable**: hypomnema (TMX-only)

**Trade-offs**:
- translate-toolkit: GPL licensing, no type hints, TMX Level 1 only
- Hybrid approach: Manage multiple libraries (complexity)

**Recommendation**: If multi-format critical, translate-toolkit simplifies pipeline vs managing multiple libraries. If GPL problematic, use hybrid (MIT-licensed per-format libraries).

### Requirement: CLI Tools (No Coding)

**When needed**:
- Freelance translators (batch PO → TMX conversion)
- Project managers (automated QA checks)
- DevOps (CI/CD pipeline automation via shell scripts)

**Selection**:
- **Primary fit**: translate-toolkit (po2tmx, tmx2po, pofilter CLIs)
- **No alternatives**: hypomnema and polib are library-only (require Python scripting)

**Recommendation**: If CLI tools required, translate-toolkit only option. Build wrapper scripts around hypomnema only if GPL licensing unacceptable.

### Requirement: MIT Licensing (Commercial Products)

**When needed**:
- Proprietary CAT tools
- Commercial localization SaaS platforms
- Embedded devices (binary-only distribution)
- Open-source projects requiring permissive licensing

**Selection**:
- **Primary fit**: hypomnema (MIT)
- **Alternative**: polib (MIT, but PO-only, TMX via translate-toolkit GPL dependency)
- **Not suitable**: translate-toolkit (GPL copyleft)

**GPL copyleft implications**:
- Derivative works must be GPL-licensed
- Binary distribution must include source code
- SaaS products: unclear if AGPL applies (legal gray area)

**Recommendation**: If commercial product, hypomnema required for native TMX. polib only if PO primary format (TMX secondary via conversion).

### Requirement: Production Stability (No Breaking Changes)

**When needed**:
- Mission-critical translation workflows
- Long-term maintenance (5+ years)
- Conservative IT environments (avoid frequent updates)

**Selection**:
- **Primary fit**: translate-toolkit (10+ years production, rare breaking changes) or polib (stable)
- **Not suitable**: hypomnema (pre-1.0, API changes expected)

**Risk mitigation for hypomnema**:
- Pin version in requirements.txt (control updates)
- Allocate time for updates (2-5 days per major version)
- Acceptable for greenfield projects (not mature products)

**Recommendation**: If stability critical, wait for hypomnema 1.0 or use translate-toolkit (if GPL acceptable). If cutting-edge features justify risk, pin hypomnema version.

## Selection by Persona

### Freelance Translators

**Requirements**: PO ↔ TMX conversion, CLI tools, simple workflows, stable, free

**Recommendation**: translate-toolkit
- CLI tools (po2tmx, tmx2po) no coding required
- Quality checks (pofilter) automate QA
- Stable (10+ years), GPL acceptable (tool usage, not redistribution)

**Alternative**: polib + translate-toolkit (if PO-centric, occasional TMX export)

### Localization Agencies (LSPs)

**Requirements**: Multi-format, batch processing, CAT tool interoperability, automation

**Recommendation**: translate-toolkit (primary) + hypomnema (optional for software localization)
- translate-toolkit: Multi-format (20+ formats), CLI automation, pofilter QA
- hypomnema: TMX Level 2 for software localization clients, streaming for large TMs

**Licensing consideration**: If embedding in proprietary TMS, hypomnema (MIT) required

### NLP Researchers

**Requirements**: TMX Level 2, large corpora, streaming, type safety, programmatic API

**Recommendation**: hypomnema
- Level 2 (structured inline markup for linguistic analysis)
- Streaming (multi-GB corpora on memory-constrained GPU servers)
- Type safety (reproducible research, static checking)
- MIT licensing (open-source preprocessing code)

**Alternative**: translate-toolkit (if corpus <100 MB, Level 1 sufficient, GPL acceptable)

### Enterprise Localization Teams

**Requirements**: CI/CD integration, multi-format, version control, quality gates, automation

**Recommendation**: translate-toolkit (CI/CD automation) + commercial platform (PM/translator UI)
- translate-toolkit: Multi-format conversion, pofilter QA in CI, CLI scriptable
- Hybrid: Commercial platform (Phrase, Smartling) for PM/translator + translate-toolkit for Git integration

**Alternative**: hypomnema (if building proprietary localization platform, MIT required)

### CAT Tool Developers

**Requirements**: TMX Level 2, MIT licensing, type safety, extensibility, production quality

**Recommendation**: hypomnema
- Level 2 (lossless round-trip with Trados, memoQ)
- MIT licensing (commercial product)
- Type safety (large codebase quality)
- Streaming (enterprise-scale TMs)
- Extensibility (custom policies, backends)

**Risk mitigation**: Pin version (pre-1.0 caveat), allocate update time, fork if necessary

## Selection by Constraint

### Constraint: Python 2.7 or PyPy Required

**Selection**: polib (only library supporting Python 2.7 and PyPy)
- translate-toolkit: Python 3.11+ only
- hypomnema: Python 3.12+ only

**Recommendation**: If cannot upgrade Python, polib only option. For TMX, use translate-toolkit CLI tools (po2tmx) externally.

### Constraint: No lxml (Pure Python Only)

**Selection**: polib (pure Python, zero dependencies) or hypomnema (stdlib backend)
- translate-toolkit: Requires lxml (C extension)
- hypomnema: Optional lxml (stdlib backend 10x slower, but zero dependencies)

**Recommendation**: If deployment environment lacks compilers (embedded systems, air-gapped servers), polib or hypomnema (stdlib backend).

### Constraint: Python 3.11 (Cannot Upgrade to 3.12)

**Selection**: translate-toolkit or polib
- hypomnema: Requires Python 3.12+ (excluded)

**Recommendation**: If infrastructure frozen at Python 3.11, use translate-toolkit (multi-format) or polib (PO-only). Reconsider when Python 3.12+ available.

### Constraint: Memory <1 GB (Embedded Systems)

**Selection**: hypomnema (streaming API) or polib (lowest overhead)
- translate-toolkit: High memory overhead (3-5x file size)
- hypomnema (streaming): Constant ~50 MB RAM
- polib: Low overhead (2-3x file size, but PO simpler than TMX)

**Recommendation**: For large TMX files on embedded systems, hypomnema streaming only option. For small files, polib lower overhead.

## Selection by Use Case Workflow

### Use Case: One-Time TMX → PO Conversion

**Recommendation**: translate-toolkit CLI
- Single command: `tmx2po input.tmx output.po`
- No coding required
- GPL acceptable (one-time tool usage)

### Use Case: Research Corpus Extraction (Multi-GB TMX)

**Recommendation**: hypomnema
- Streaming API (constant RAM usage)
- Type safety (reproducible pipelines)
- Level 2 (structured inline markup for linguistic analysis)

### Use Case: CI/CD Automated Translation Pipeline

**Recommendation**: translate-toolkit (CLI automation) or hypomnema (Python API)
- translate-toolkit: Shell-scriptable CLI tools, multi-format
- hypomnema: Python API integration (if MIT licensing required)

### Use Case: Building Commercial CAT Tool

**Recommendation**: hypomnema
- MIT licensing (commercial product)
- Level 2 (professional compatibility)
- Type safety (production quality)
- Extensibility (custom features)

### Use Case: Django/Flask i18n Workflow (PO Primary)

**Recommendation**: polib (PO manipulation) + translate-toolkit CLI (occasional TMX export)
- polib: Native PO support, simple API
- translate-toolkit: TMX export via po2tmx CLI when needed

## Decision Matrix Template

Use this matrix to score libraries against your requirements (weight 1-5):

| Requirement | Weight | translate-toolkit | hypomnema | polib |
|-------------|--------|------------------|-----------|-------|
| TMX Level 2 | ___ | 1 | 5 | 1 |
| Large files (>1 GB) | ___ | 1 | 5 | 2 |
| Type safety | ___ | 1 | 5 | 1 |
| MIT licensing | ___ | 1 | 5 | 5 |
| Multi-format support | ___ | 5 | 1 | 3 |
| CLI tools | ___ | 5 | 1 | 1 |
| Production stability | ___ | 5 | 2 | 5 |
| Python 2.7 / PyPy | ___ | 1 | 1 | 5 |
| Zero dependencies | ___ | 1 | 3 | 5 |
| Quality checks (pofilter) | ___ | 5 | 1 | 1 |

**Instructions**:
1. Assign weight (1-5) based on importance
2. Multiply requirement score × weight
3. Sum weighted scores
4. Highest score = best fit

**Example**:
- Commercial CAT tool: MIT licensing (weight 5), Level 2 (weight 5), type safety (weight 4) → hypomnema wins
- Freelance translator: CLI tools (weight 5), multi-format (weight 4), stability (weight 4) → translate-toolkit wins

## Common Selection Patterns

### Pattern: "I need X AND Y"

| Requirements | Best Fit | Rationale |
|--------------|----------|-----------|
| Level 2 AND MIT licensing | hypomnema | Only option with both |
| Multi-format AND CLI tools | translate-toolkit | Comprehensive toolkit (if GPL acceptable) |
| Type safety AND streaming | hypomnema | Only typed library with streaming |
| PO-centric AND zero dependencies | polib | Pure Python, native PO |
| Large files AND MIT licensing | hypomnema | Streaming + MIT |

### Pattern: "I cannot use X"

| Cannot Use | Avoid | Use Instead |
|------------|-------|-------------|
| GPL licensing | translate-toolkit | hypomnema (MIT) or polib (MIT) |
| Python 3.12+ | hypomnema | translate-toolkit (3.11+) or polib (2.7+) |
| C extensions | translate-toolkit | polib or hypomnema (stdlib backend) |
| Pre-1.0 APIs | hypomnema | translate-toolkit or polib |

### Pattern: "X is must-have"

| Must-Have | Only Option | Alternative (Trade-off) |
|-----------|-------------|------------------------|
| TMX Level 2 | hypomnema | Build custom parser (high effort) |
| Streaming API | hypomnema | External chunking (complexity) |
| CLI tools | translate-toolkit | Build wrappers (development effort) |
| Python 2.7 | polib | Upgrade Python (infrastructure cost) |
| MIT + Level 2 | hypomnema | None (unique combination) |

## Summary: When to Use Each Library

### Use translate-toolkit when:
- ✅ Multi-format support critical (PO, XLIFF, TBX, etc.)
- ✅ CLI tools preferred (no coding)
- ✅ Production stability critical
- ✅ Quality checks needed (pofilter)
- ✅ GPL licensing acceptable
- ✅ TMX Level 1 sufficient
- ❌ Avoid if: Commercial product (GPL), Level 2 required, large files (>1 GB)

### Use hypomnema when:
- ✅ TMX Level 2 required (structured inline markup)
- ✅ MIT licensing required (commercial products)
- ✅ Type safety needed (large codebase)
- ✅ Large files (>1 GB, streaming API)
- ✅ Extensibility valued (custom policies, backends)
- ✅ Python 3.12+ available
- ❌ Avoid if: Production stability critical (pre-1.0), Python <3.12, need CLI tools

### Use polib when:
- ✅ PO primary format (Django, Flask, gettext)
- ✅ Zero dependencies required (pure Python)
- ✅ Python 2.7 or PyPy needed
- ✅ MIT licensing required
- ✅ Simple PO manipulation (not comprehensive TMX processing)
- ❌ Avoid if: Native TMX needed (use translate-toolkit or hypomnema)

## Hybrid Approaches

### translate-toolkit + hypomnema
- **Use case**: LSPs with diverse clients (general localization + software localization)
- **Pattern**: translate-toolkit for multi-format conversion, hypomnema for Level 2 workflows
- **Trade-off**: Manage two libraries vs single-library simplicity

### polib + translate-toolkit CLI
- **Use case**: Django/Flask i18n with occasional TMX export
- **Pattern**: polib for PO manipulation, translate-toolkit po2tmx CLI for vendor delivery
- **Trade-off**: Simple PO workflows, indirect TMX support (lossy conversion)

### hypomnema + custom backends
- **Use case**: CAT tool with database-backed TM storage
- **Pattern**: hypomnema for TMX I/O, custom backend for PostgreSQL integration
- **Trade-off**: Development effort vs off-the-shelf file-based storage

## Final Recommendation Process

1. **Identify must-have requirements** (deal-breakers):
   - TMX Level 2? → hypomnema (or custom parser)
   - MIT licensing? → hypomnema or polib (not translate-toolkit)
   - CLI tools? → translate-toolkit (or build wrappers)
   - Python 2.7? → polib (or upgrade Python)

2. **Evaluate constraints** (environmental limitations):
   - Python version available?
   - Memory constraints (file size vs RAM)?
   - Licensing restrictions?
   - Platform requirements (Windows, Mac, Linux)?

3. **Score nice-to-haves** (use decision matrix):
   - Weight requirements by importance
   - Calculate weighted scores
   - Highest score = best fit

4. **Validate with prototype** (test with real data):
   - Parse sample TMX files
   - Measure performance (speed, memory)
   - Test round-trip fidelity (TMX → process → TMX)
   - Verify CAT tool compatibility (import into Trados, memoQ)

5. **Make decision** (document rationale):
   - Document why chosen library fits requirements
   - Acknowledge trade-offs (what you're sacrificing)
   - Define success criteria (how to measure if decision correct)

This requirement-driven approach ensures library selection aligns with business needs, technical constraints, and long-term maintainability.
