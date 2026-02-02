# Use Case: CAT Tool Developers

## Who Needs This

**Role**: Software engineer building Computer-Aided Translation (CAT) tools or translation management systems (TMS)

**Context**:
- Developing commercial CAT tool (desktop or SaaS) or open source translation software
- TMX is core data format (primary import/export, internal TM storage)
- Must support full TMX specification for professional translator users
- Competing with established tools (SDL Trados, memoQ, Phrase, Memsource, OmegaT)
- Quality and compatibility critical (data loss or corruption unacceptable)
- Building complex features (translation editing UI, QA checks, MT integration, TM search)

**Technical background**:
- Professional software engineers (Python, Java, C++, JavaScript)
- Building production-grade applications (not one-off scripts)
- Large codebase (10K-100K+ lines of code)
- Team development (multiple engineers, code reviews, CI/CD)
- Performance critical (real-time UI responsiveness, large TM search)
- Reliability critical (data integrity, crash recovery, no data loss)

**Volume**:
- User TMs: 1K-100M translation units (wide range, from beginners to enterprise clients)
- File sizes: 1 MB - 10 GB (must support full spectrum)
- Concurrent users: 1-10K active users (if SaaS)
- Real-time operations: TM search (<100ms), segment saving (<50ms)

## Requirements and Constraints

### Must-Have Requirements

1. **Full TMX specification support**: Must implement TMX 1.4b Level 2 (structured inline markup)
   - Why: Professional translators expect full compatibility with Trados, memoQ (no data loss on import/export)

2. **Production stability**: Must be mature, well-tested library (no data corruption, crashes)
   - Why: Single bug loses customer data → reputational damage, legal liability

3. **High performance**: Must parse/write TMX files quickly (<5 sec for 100K units)
   - Why: Users expect responsive UI (instant TM search, fast project loading)

4. **Permissive licensing**: Must be MIT/BSD/Apache (not GPL)
   - Why: Commercial software cannot be GPL-licensed (copyleft forces open source)

5. **Type safety**: Must have type hints for large codebase integration
   - Why: Untyped APIs cause runtime errors in production, costly to debug

6. **Extensibility**: Must support custom validation, backends, policies
   - Why: Commercial CAT tools have proprietary features (custom metadata, workflow extensions)

7. **Streaming API**: Must handle large files (>1 GB) without excessive memory
   - Why: Enterprise clients have TMs with 10M+ units, memory constraints on user machines

### Constraints

- **Python version**: Can target Python 3.12+ (control deployment environment)
  - Desktop apps: bundle Python runtime (PyInstaller, py2app)
  - SaaS: control server Python version (Docker, Kubernetes)

- **Licensing**: MIT required (GPL copyleft prohibits commercial use)
  - Cannot use translate-toolkit (GPL) in proprietary product

- **Dependencies**: Acceptable if reliable and well-maintained
  - Prefer optional dependencies (lxml vs stdlib) for flexibility

- **Platform**: Must support Windows, Mac, Linux (desktop CAT tools)
  - SaaS: Linux servers only (containerized)

- **API stability**: Critical (breaking changes disrupt development)
  - Prefer stable 1.0+ release, or willing to absorb pre-1.0 risk if benefits justify

### Nice-to-Have Features

- Incremental parsing (load TM progressively for faster UI startup)
- Partial write (update single TU without rewriting entire file)
- Concurrent access (multiple users editing TM simultaneously)
- Database backend (store TM in SQL instead of XML files)
- Fuzzy matching (find similar translations, not exact matches)
- MT integration (pre-translate with Google Translate, DeepL)

### Anti-Requirements

- CLI tools (building GUI application, need programmatic API)
- Multi-format support beyond TMX (handle PO, XLIFF separately if needed)
- Zero dependencies (performance > simplicity, lxml acceptable)

## Current Workflow and Pain Points

### As-Is Workflow (Building CAT Tool)

1. **TM import**: User imports TMX file from Trados, memoQ, or other CAT tools
2. **TM storage**: Parse TMX, store in database (PostgreSQL, SQLite) for fast search
3. **Translation UI**: Display source segment, show TM matches (fuzzy matching), allow editing
4. **TM update**: User saves translation, update database + in-memory cache
5. **TM export**: User exports project TM as TMX for client delivery or backup
6. **QA checks**: Validate translations (completeness, consistency, formatting)

### Pain Points

1. **TMX Level 1 limitation**: Existing libraries (translate-toolkit) don't preserve structured inline markup
   - Need: Level 2 support for lossless round-trip with Trados, memoQ

2. **No type hints**: Untyped TMX libraries cause runtime errors in complex codebase
   - Need: Type-safe API for IDE autocomplete, static checking (mypy, Pylance)

3. **GPL licensing**: translate-toolkit GPL-licensed, cannot embed in commercial product
   - Need: MIT-licensed library for proprietary CAT tool

4. **Memory constraints**: Parsing large TMs (>1 GB) into memory crashes on user machines
   - Need: Streaming API to import large TMs without memory exhaustion

5. **No extensibility**: Cannot customize validation, backends, error handling
   - Need: Policy-driven architecture for custom business logic (proprietary QA rules, workflow extensions)

6. **Performance bottlenecks**: Slow parsing blocks UI (users wait 30+ seconds for TM import)
   - Need: Fast parsing (lxml backend, optimized dataclasses) for responsive UI

7. **No incremental parsing**: Must parse entire file before showing UI (poor UX for large TMs)
   - Need: Streaming API to display TM segments progressively (show first 1000 units immediately, load rest in background)

## Library Fitness Assessment

### hypomnema

**Fitness rating**: **Primary fit**

**Rationale**:
- **TMX Level 2 support**: Full structured inline markup (bpt/ept pairing, nesting) enables lossless round-trip with Trados, memoQ
- **MIT licensing**: Safe for commercial CAT tool (no GPL copyleft concerns)
- **Type safety**: Full type hints (Python 3.12+) integrate into large codebase (mypy/Pylance static checking)
- **Streaming API**: Handles large TMs (>1 GB) with constant ~50 MB RAM, critical for user machines
- **Policy-driven validation**: Custom policies for proprietary QA rules, error handling
- **Extensible backends**: Can implement custom XML backend (e.g., database-backed, incremental parsing)
- **High performance**: lxml backend + optimized dataclasses for fast parsing (~2 sec for 100K units)

**Trade-offs**:
- **Pre-1.0 status**: API instability risk during CAT tool development
  - Mitigation: Pin version, allocate engineer time for updates, contribute fixes upstream
  - Risk: Breaking changes may require refactoring during development (acceptable for greenfield project, problematic for mature product)

- **Small community**: Limited third-party examples, slower issue resolution
  - Mitigation: Read source code (well-typed, readable), fork if necessary, contribute improvements
  - Risk: Critical bugs may delay product release, no commercial support SLA

- **Python 3.12+ requirement**: Limits deployment to modern Python versions
  - Impact: Must bundle Python 3.12+ runtime in desktop apps (PyInstaller, py2app handle this)
  - Non-issue for SaaS (control server Python version)

- **TMX-only**: No PO, XLIFF support (must use separate libraries)
  - Impact: If CAT tool supports multiple formats, need additional libraries
  - Mitigation: Use format-specific libraries (polib for PO, lxml for XLIFF), hypomnema for TMX

**Why it fits**: Designed for programmatic TMX processing with type safety and extensibility, exactly matching CAT tool development requirements (Level 2, MIT licensing, streaming, type hints).

### translate-toolkit

**Fitness rating**: **Not suitable**

**Rationale**:
- **GPL licensing**: Copyleft prohibits embedding in commercial CAT tool
  - Deal-breaker: Cannot distribute proprietary software with GPL dependency

**Other limitations (even if licensing acceptable)**:
- **TMX Level 1 only**: Cannot preserve structured inline markup (data loss on round-trip)
- **No type hints**: Untyped API problematic for large codebase (runtime errors in production)
- **No streaming API**: Memory exhaustion on large TMs (>1 GB)
- **Limited extensibility**: Subclassing only, no policy-driven architecture

**Why it doesn't fit**: GPL licensing eliminates from consideration for commercial products. Even if licensing acceptable, Level 1 limitation and lack of type safety reduce value compared to hypomnema.

### polib

**Fitness rating**: **Not suitable**

**Rationale**:
- **No native TMX support**: Requires conversion via translate-toolkit (GPL dependency)
  - Impact: Cannot use translate-toolkit due to GPL, rendering polib unsuitable for TMX

- **PO-centric**: Designed for gettext workflows, not CAT tool TMX processing

**Why it doesn't fit**: CAT tools require native TMX support, not PO-centric library with indirect TMX conversion.

## Decision Criteria

### Use hypomnema if:
- Building commercial CAT tool (MIT licensing required)
- TMX Level 2 required (structured inline markup, lossless round-trip)
- Large codebase (type safety critical for production quality)
- Must support large TMs (>1 GB, streaming API needed)
- Willing to absorb pre-1.0 risk (pin version, allocate update time)
- Python 3.12+ deployable (control runtime environment)

### Avoid translate-toolkit if:
- Commercial product (GPL copyleft prohibits proprietary use)
- TMX Level 2 required (translate-toolkit Level 1 only)
- Type safety needed (no type hints)

### Avoid polib if:
- TMX is primary format (polib TMX support via translate-toolkit, GPL dependency)

### Alternative: Custom lxml-based TMX parser if:
- Extreme performance requirements (hand-tuned parsing faster than libraries)
- Proprietary TMX extensions (non-standard attributes, elements)
- Full control over error handling, validation logic
- Engineering team can maintain custom TMX parser (ongoing development cost)

Trade-off: Custom parser = flexibility + performance, but high development/maintenance cost vs hypomnema's ready-to-use API.

## Migration Considerations

### Migrating from Custom lxml-based Parser

**Scenario**: Currently using lxml + manual XPath for TMX parsing

**With hypomnema**:
- Replace XPath queries with dataclass property access (`tu.tuvs[0].segments`)
- Add type hints to codebase (mypy catches errors before production)
- Use streaming API for large TM import (reduce memory usage 5-10x)
- Leverage policy-driven validation (replace custom validation logic)

**Benefits**:
- Type safety prevents production bugs (static checking before release)
- Streaming enables larger TMs without memory upgrades
- Reduced maintenance (upstream library fixes vs in-house parser)
- Cleaner code (dataclasses vs lxml ElementTree navigation)

**Costs**:
- Refactor existing codebase (replace custom parser with hypomnema API)
- Learning curve (new API, though well-typed and documented)
- Dependency on third-party library (pre-1.0 risk, but MIT allows forking)

### Integrating into Existing CAT Tool

**Integration points**:
- **TM import**: User selects TMX file → hypomnema parses → insert into PostgreSQL
- **TM search**: Query PostgreSQL for matches → hypomnema-based TU objects for UI display
- **TM export**: Query PostgreSQL → hypomnema writes TMX → user downloads
- **QA checks**: Custom validation policies (brand-specific terminology, client-specific rules)

**Data model mapping**:
- **hypomnema TU** → **Database row** (tuid, source text, target text, metadata JSON)
- **hypomnema TUV** → **Normalized table** (TU_id, language, segments, inline markup JSON)
- **Inline markup** → **Separate table** (for linguistic analysis, search by tag type)

**Performance optimization**:
- Use hypomnema streaming for import (avoid memory exhaustion)
- Cache parsed TUs in memory (avoid re-parsing for search)
- Index database on source text hash (fast fuzzy matching)
- Lazy-load inline markup (only parse when user expands segment)

## Recommended Workflow Patterns

### Pattern 1: Streaming TM Import with Progress UI

**Scenario**: User imports 500 MB TMX file, CAT tool shows progress bar

**Workflow**:
1. User selects TMX file in import dialog
2. CAT tool starts background thread:
   - Use hypomnema streaming API to iterate over TUs
   - Insert each TU into PostgreSQL (batched inserts for performance)
   - Update progress bar (% of file processed)
3. Display imported segments in UI as database fills
4. Enable search/editing once import completes

**Benefits**: Responsive UI (progress feedback), constant memory usage (~50 MB), background import doesn't block UI

### Pattern 2: Incremental TM Export

**Scenario**: User edits 100 segments in 1M-unit TM, export only changes

**Workflow**:
1. Track modified TUs in memory (dirty flag)
2. On export: query database for modified TUs only
3. Use hypomnema to write modified TUs to new TMX file
4. Optionally: merge with original TMX (full TM) or export changes only (incremental update)

**Benefits**: Fast export (seconds vs minutes for full TM), reduced file size for client delivery

### Pattern 3: Custom Validation Policy for QA

**Scenario**: Medical translation client forbids certain terms, requires strict formatting

**Workflow**:
1. Implement custom hypomnema DeserializationPolicy:
   - Validate terminology (reject TUs containing forbidden terms)
   - Validate inline tags (enforce medical formatting guidelines)
   - Log violations for QA report
2. Apply policy during TM import and editing
3. Block TM export if QA violations exceed threshold

**Benefits**: Client-specific QA rules without hardcoding in application, policy reusable across projects

### Pattern 4: Database-Backed TMX Storage

**Scenario**: Store TM in PostgreSQL for fast search, export TMX on demand

**Workflow**:
1. Import TMX with hypomnema streaming → insert into PostgreSQL
2. Translation workflow: all operations on database (search, edit, save)
3. Export TMX: query database → hypomnema writes TMX file
4. Round-trip fidelity: preserve original TMX metadata (tuid, creation date) in database

**Benefits**: Fast fuzzy matching (PostgreSQL full-text search), concurrent user editing, TMX export on demand

## Alternative Considerations

### When to Build Custom TMX Parser

Custom parser may fit better than hypomnema if:
- **Proprietary TMX extensions**: Non-standard attributes, elements not in TMX spec
- **Extreme performance requirements**: Hand-tuned parsing 10x faster for specific use case
- **Full control**: Proprietary validation, error handling, recovery logic
- **No Python 3.12**: Cannot deploy Python 3.12+ (e.g., legacy desktop app)

Trade-off: Custom parser = maximum control + performance, but high development/maintenance cost (10-100x engineer hours vs using library).

### When to Use Existing CAT Tool as Base

Instead of building from scratch, consider:
- **OmegaT (GPL)**: Open source CAT tool, fork and extend (must remain GPL)
- **Okapi Framework (Apache)**: Localization toolkit with TMX support (permissive licensing)
- **Commercial white-label**: License existing CAT tool, rebrand (no development, but high licensing cost)

Building custom CAT tool justified if:
- Proprietary workflow not supported by existing tools (e.g., real-time collaborative editing, ML-powered QA)
- CAT tool integrated into broader platform (CMS, e-commerce, customer support)
- Licensing costs exceed in-house development (Python engineer cheaper than per-seat licensing at scale)

## Summary: CAT Tool Developer Recommendation

**Primary recommendation**: hypomnema

**Why**: TMX Level 2 (structured inline markup) enables lossless round-trip with professional CAT tools (Trados, memoQ), MIT licensing safe for commercial products, type safety (Python 3.12+) critical for large codebase quality, streaming API handles enterprise-scale TMs (>1 GB), policy-driven validation enables custom QA rules, extensible backends allow proprietary features (database storage, incremental parsing).

**When to avoid hypomnema**:
- Cannot deploy Python 3.12+ (legacy desktop app): Build custom lxml parser or wait for hypomnema 1.0 (may support older Python)
- Cannot accept pre-1.0 risk (mission-critical product): Wait for hypomnema 1.0 or build custom parser
- Extreme performance requirements: Hand-tuned custom parser may be faster (but 10-100x development cost)

**Not recommended**:
- translate-toolkit: GPL licensing prohibits commercial use
- polib: No native TMX support, PO-centric

**Key requirement match**:
- ✅ Full TMX specification support (Level 2, structured inline markup)
- ✅ Production stability (well-tested, though pre-1.0 caveat)
- ✅ High performance (lxml backend, ~2 sec for 100K units)
- ✅ Permissive licensing (MIT, safe for commercial products)
- ✅ Type safety (full type hints, mypy/Pylance compatible)
- ✅ Extensibility (custom policies, backends)
- ✅ Streaming API (handles large TMs without memory exhaustion)

**Risk mitigation for pre-1.0**:
- Pin hypomnema version in requirements.txt (control updates)
- Allocate engineer time for API updates (budget 2-5 days per major version)
- Contribute fixes upstream (build relationship with maintainer)
- Fork if necessary (MIT licensing allows proprietary fork)
- Consider commercial support contract (if available in future)

This persona prioritizes TMX Level 2 compliance and MIT licensing (commercial product requirements), type safety for large codebase quality, and extensibility for proprietary features. Pre-1.0 risk acceptable if benefits justify (modern type-safe API vs mature untyped alternatives).
