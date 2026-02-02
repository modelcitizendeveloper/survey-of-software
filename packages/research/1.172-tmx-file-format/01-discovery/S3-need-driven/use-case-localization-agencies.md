# Use Case: Localization Agencies (LSPs)

## Who Needs This

**Role**: Language Service Provider (LSP) managing translation workflows for multiple clients

**Context**:
- Commercial translation agency with 10-100 translators
- Handles projects for diverse clients across industries (software, legal, medical, marketing)
- Manages multiple CAT tools based on client requirements (Trados, memoQ, Phrase, Memsource)
- Processes 100K-10M translation units monthly
- Quality assurance critical (regulatory compliance, brand consistency)
- IT team available but focused on core business systems, not custom development

**Technical background**:
- Project managers: CAT tool power users, basic scripting
- IT team: Can deploy Python applications, manage servers, configure automation
- Translation team: Uses CAT tools exclusively, no programming
- DevOps: CI/CD experience with Jenkins/GitLab, comfortable with API integration

**Volume**:
- Corporate TM databases: 1M-100M translation units
- Typical project: 10K-500K segments
- File sizes: 10 MB - 1 GB TMX files
- Concurrent projects: 50-200 active translation jobs

## Requirements and Constraints

### Must-Have Requirements

1. **Multi-client TM isolation**: Must maintain separate TMs per client with strict access control
   - Why: Confidentiality agreements prohibit sharing client A's translations with client B

2. **CAT tool interoperability**: Must import/export TMX for multiple CAT tool platforms
   - Why: Different clients mandate specific tools (Trados Studio, memoQ Server, Phrase TMS)

3. **Batch processing performance**: Must process large TM files (100 MB+) efficiently
   - Why: Project deadlines require fast TM preparation, merging, and delivery

4. **Quality assurance automation**: Must validate TM consistency, completeness, format compliance
   - Why: Manual QA infeasible at scale, regulatory industries require audit trails

5. **Multi-format pipeline**: Must convert between TMX, PO, XLIFF, TBX for diverse client requirements
   - Why: Clients deliver/expect different formats (software → PO, enterprise → TMX, technical docs → XLIFF)

6. **Automation integration**: Must integrate with project management systems (APIs, scripting, CI/CD)
   - Why: Manual TM handling bottlenecks workflow, need automated TM distribution to translators

### Constraints

- **Licensing**: GPL problematic if embedding in proprietary TMS (Translation Management System)
  - Commercial SaaS product may require MIT licensing to avoid copyleft obligations

- **Python version**: Can deploy Python 3.11+ on servers, but legacy systems may limit translator workstations
  - Server-side processing flexible, client-side tools must support older Python

- **Platform**: Primarily Linux servers for automation, Windows workstations for translators
  - Must support both platforms (server-side batch processing, client-side GUI/CLI tools)

- **Dependencies**: Can manage C extensions (lxml) on servers, prefer pure Python for translator workstations
  - Deployment complexity acceptable for servers, minimize for translator tools

- **Learning curve**: IT team can learn library APIs, translators need zero-code tools
  - Developer-friendly API acceptable for IT automation, must provide CLI tools for project managers

### Nice-to-Have Features

- TM deduplication and consolidation (merge overlapping client TMs without duplication)
- Terminology extraction from TMs to build glossaries
- Translation reuse analytics (measure leverage across projects)
- TM versioning and rollback (track changes over time)
- Client-specific QA rules (e.g., medical client forbids certain terms)

### Anti-Requirements

- TMX Level 2 for typical workflows (Level 1 sufficient for most CAT tool exchange)
  - Exception: Software localization clients with complex UI formatting may need Level 2

- Type safety for one-off scripts (not building large codebase, rapid prototyping valued)
- Zero dependencies (IT can manage lxml, performance > simplicity)

## Current Workflow and Pain Points

### As-Is Workflow

1. **Project intake**: Client sends source files + TM (various formats)
2. **TM preparation**: IT team converts TM to format compatible with assigned CAT tool
3. **Distribution**: Project manager distributes TM to translators via CAT tool server
4. **Translation**: Translators work in CAT tool, leveraging client TM + corporate TM
5. **QA**: Project manager runs QA checks (completeness, consistency, format validation)
6. **Delivery**: Export translated TM + target files for client
7. **TM update**: Merge new translations into client's master TM

### Pain Points

1. **Format fragmentation**: Clients deliver TMs in incompatible formats (TMX 1.4, TMX 1.1, XLIFF 1.2, proprietary)
   - Need: Reliable multi-format conversion without manual editing

2. **TM bloat**: Corporate TMs accumulate redundant/outdated translations over years
   - Need: Deduplication and quality-based filtering (prioritize recent, client-approved translations)

3. **Manual QA bottleneck**: Project managers manually check for untranslated segments, formatting errors
   - Need: Automated QA integrated into delivery pipeline

4. **TM versioning chaos**: Single TM file modified by multiple projects, no change tracking
   - Need: Git-based version control for TMs, branching per project

5. **Slow TM processing**: Large TMs (500 MB+) take minutes to open in CAT tools
   - Need: Pre-process/filter TMs to extract relevant segments only (e.g., filter by domain, date, client)

6. **Licensing uncertainty**: Unsure if GPL libraries compatible with commercial TMS product
   - Need: MIT-licensed tools to avoid legal review overhead

## Library Fitness Assessment

### translate-toolkit

**Fitness rating**: **Primary fit for multi-format workflows**

**Rationale**:
- **Multi-format support**: 20+ formats (TMX, PO, XLIFF, TBX, RC, etc.) critical for diverse client base
- **Command-line tools**: IT team can automate conversions via CLI (po2tmx, tmx2po, xliff2tmx)
- **Quality checks**: pofilter with 40+ checks automates QA for common issues (untranslated, mismatched tags)
- **Mature and stable**: 10+ years in production across LSPs, rare breaking changes
- **Python 3.11+ compatible**: Deployable on modern Linux servers

**Trade-offs**:
- **GPL licensing**: Problematic if embedding in proprietary TMS
  - Mitigation: Use as external CLI tool called via subprocess (linking vs usage legal gray area)
  - Risk: May require legal review if distributing TMS to clients

- **TMX Level 1 only**: Sufficient for 90% of workflows
  - Gap: Software localization projects with complex UI formatting may need Level 2

- **Memory usage**: Struggles with very large TMs (>1 GB)
  - Mitigation: Pre-filter TMs by date range, client, language pair before processing

- **No streaming API**: Must load entire TM into memory
  - Impact: Server RAM requirements scale with TM size (500 MB file → ~2 GB RAM)

**Why it fits**: Designed for localization practitioners managing diverse format requirements, established track record in LSP workflows.

### hypomnema

**Fitness rating**: **Acceptable fit for streaming-heavy workflows**

**Rationale**:
- **Streaming API**: Handles very large TMs (>1 GB) efficiently on memory-constrained servers
- **TMX Level 2**: Critical for software localization clients with complex inline markup
- **MIT licensing**: Avoids GPL copyleft, safe for proprietary TMS integration
- **Type safety**: Valuable if building custom TMS integrations (large codebase)
- **Policy-driven validation**: Custom QA rules per client (strict for medical, lenient for marketing)

**Trade-offs**:
- **Python 3.12+ requirement**: May require server infrastructure upgrade
  - Cost: Migration effort, testing, potential compatibility issues with other tools

- **Pre-1.0 status**: API instability risk during production workflows
  - Risk: Breaking changes could disrupt client deliveries during busy seasons
  - Mitigation: Pin version, allocate developer time for updates

- **No CLI tools**: Requires Python scripting for every operation
  - Impact: IT team must build wrapper scripts for project managers (more development effort)

- **Small community**: Limited third-party resources, slower issue resolution
  - Risk: Critical bugs may delay projects, commercial support unavailable

- **TMX-only**: Requires additional libraries for PO, XLIFF, TBX conversion
  - Impact: Multi-library integration complexity vs translate-toolkit's unified approach

**Why it might fit**: If LSP primarily handles software localization (Level 2 required), processes very large TMs (streaming critical), and can deploy Python 3.12+ infrastructure, hypomnema's MIT licensing and streaming capabilities offset pre-1.0 risk.

### polib + translate-toolkit

**Fitness rating**: **Poor fit**

**Rationale**:
- **PO-centric workflow**: LSPs handle diverse formats (TMX, XLIFF, TBX), not just PO
- **Indirect TMX support**: Requires translate-toolkit for TMX conversion (no advantage over direct use)
- **Conversion overhead**: PO → TMX → PO round-trip loses metadata (tuid, custom properties)
- **No quality checks**: Lacks translate-toolkit's pofilter, requiring separate QA tooling

**Trade-offs**:
- **Zero dependencies**: Irrelevant for server environments where lxml installation trivial
- **MIT licensing**: Shared with translate-toolkit (via po2tmx/tmx2po CLI), but limited to PO workflows

**Why it doesn't fit**: LSPs need comprehensive multi-format support, not PO-specific optimization. Using polib + translate-toolkit offers no advantage over translate-toolkit alone.

## Decision Criteria

### Use translate-toolkit if:
- Multi-format pipeline (TMX, PO, XLIFF, TBX, RC, etc.) critical for client diversity
- Need ready-to-use CLI tools for project managers (no custom development budget)
- TMX Level 1 sufficient (90% of projects, excluding complex software localization)
- Quality checks (pofilter) valuable for automated QA
- GPL licensing acceptable (external CLI tool, not embedded in proprietary TMS)
- Python 3.11 infrastructure available

### Use hypomnema if:
- Software localization primary business (TMX Level 2 required for inline markup)
- Very large TMs (>1 GB) common (streaming API critical)
- Building proprietary TMS (MIT licensing required to avoid GPL copyleft)
- IT team can develop wrapper scripts (no ready-to-use CLI tools)
- Python 3.12+ infrastructure available or planned
- Can absorb pre-1.0 API instability risk (pin version, allocate update time)

### Use hybrid approach (translate-toolkit + hypomnema) if:
- Diverse client base: general localization (translate-toolkit) + software localization (hypomnema)
- Large TM processing (hypomnema streaming) + multi-format conversion (translate-toolkit)
- Willing to manage two libraries (increased complexity for broader capability)

### Avoid polib if:
- Multi-format support needed (TMX, XLIFF, TBX beyond PO)
- Indirect TMX conversion via translate-toolkit offers no advantage

## Migration Considerations

### Migrating from Manual CAT Tool Workflow

**Scenario**: Currently export/import TMs manually via CAT tool server GUI

**With translate-toolkit**:
- Automate format conversions in CI/CD pipeline (GitLab CI, Jenkins)
- Pre-filter TMs before distribution (extract client-specific, date-range, domain)
- Integrate QA checks into delivery workflow (block if pofilter errors exceed threshold)
- Version control TMs in Git (branch per project, merge on completion)

**With hypomnema**:
- Build custom TMS integration (API calls for TM upload/download)
- Stream large TMs during processing (reduce server RAM requirements)
- Implement client-specific validation policies (medical → strict, marketing → lenient)

**Benefits**:
- Reduced manual QA effort (automated checks catch 80% of errors)
- Faster project turnaround (batch TM processing vs manual CAT tool operations)
- TM versioning prevents accidental overwrites, enables rollback

**Costs**:
- IT team learning curve (Python library APIs, CI/CD integration)
- Infrastructure upgrades (Python 3.12 for hypomnema, Git LFS for large TM versioning)
- Initial development time (build automation scripts, integrate with PM systems)

### Compatibility with Existing CAT Tools

**CAT tool integration**:
- translate-toolkit: TMX Level 1 compatible with Trados, memoQ, Phrase, Memsource, XTM
- hypomnema: TMX Level 2 compatible with all above + preserves complex inline markup

**TM server integration**:
- Both libraries: Export TMX → upload to CAT tool server via API (memoQ Server API, Trados GroupShare API)
- translate-toolkit: CLI tools scriptable via cron jobs, GitLab CI runners
- hypomnema: Python API callable from custom TMS integrations

**Data preservation**:
- translate-toolkit: Level 1 preserves all standard metadata (creation date, tuid, language pairs)
- hypomnema: Level 2 preserves structured inline markup (bpt/ept pairing, nesting)

**Risk mitigation**:
- Test workflow with non-critical project before production rollout
- Parallel run (manual + automated) during transition period
- Train project managers on CLI tools / custom TMS interfaces
- Rollback plan if automation causes delivery delays

## Recommended Workflow Patterns

### Pattern 1: Automated TM Preparation Pipeline (translate-toolkit)

**Scenario**: Client delivers PO files, translators use memoQ (requires TMX)

**Workflow**:
1. Client uploads PO files to project portal
2. GitLab CI triggered on upload:
   - Converts PO → TMX via `po2tmx`
   - Filters by date range (last 5 years only, reduces TM size)
   - Runs QA checks via `pofilter`
   - If QA passed: uploads TMX to memoQ Server API
3. Project manager assigns translators in memoQ
4. On completion: export translated TMX from memoQ
5. GitLab CI converts TMX → PO via `tmx2po` for client delivery
6. Commit updated PO + TMX to Git (versioned TM)

**Benefits**: Zero manual conversion, automated QA, version-controlled TMs

### Pattern 2: Large TM Streaming Processing (hypomnema)

**Scenario**: Corporate TM = 2 GB file (10M units), server has 8 GB RAM

**Workflow**:
1. Use hypomnema streaming API to:
   - Filter TM by client ID (extract relevant subset)
   - Filter by date (recent 3 years only)
   - Output to smaller TMX file (<100 MB)
2. Distribute filtered TMX to translators via CAT tool
3. After translation: stream new segments back into master TM
4. Commit master TM to Git LFS (large file versioning)

**Benefits**: Constant ~50 MB RAM usage regardless of file size, no TM bloat for translators

### Pattern 3: Hybrid Multi-Format + Streaming (both libraries)

**Scenario**: Diverse clients (PO, XLIFF, proprietary) + large corporate TM

**Workflow**:
1. Use translate-toolkit for multi-format conversion:
   - Client A: PO → TMX via `po2tmx`
   - Client B: XLIFF → TMX via `xliff2tmx`
   - Client C: Proprietary → TMX via custom converter + translate-toolkit
2. Use hypomnema for TM consolidation:
   - Stream multiple client TMX files → deduplicate → merge into corporate TM
   - Filter corporate TM by client for distribution
3. QA: translate-toolkit's `pofilter` for standard checks + hypomnema custom policies for client-specific rules

**Benefits**: Broad format support (translate-toolkit) + large file efficiency (hypomnema)

## Alternative Considerations

### When Commercial TMS May Be Better

Custom Python automation ideal for specific workflows, but commercial TMS may fit better if:
- **Integrated CAT tool + TM server**: All-in-one solution (Phrase, XTM Cloud, Smartling) reduces integration overhead
- **Enterprise budget**: Multi-million dollar contract justifies TMS licensing costs
- **Support SLA required**: Python library bugs may delay projects, commercial vendor provides guaranteed support
- **Project management features**: TMS includes PM tools (task assignment, invoicing, client portals) beyond TM processing

LSPs often use hybrid: commercial TMS for PM/CAT integration + Python libraries for specialized TM processing (deduplication, multi-format conversion, analytics)

### When to Build Custom TMS

Build custom TMS using hypomnema or translate-toolkit if:
- Proprietary workflow not supported by commercial TMS (e.g., legal industry confidentiality requirements)
- TMS licensing costs exceed in-house development (Python developer + server cheaper than per-seat licensing)
- Integration with existing systems critical (ERP, CRM, invoicing, proprietary client portals)
- MIT licensing required (embedding in SaaS product, distributing to clients)

## Summary: LSP Recommendation

**Primary recommendation**: translate-toolkit for multi-format workflows

**Why**: Multi-format support (20+ formats) handles diverse client base, CLI tools enable rapid automation without custom development, mature/stable reduces production risk, pofilter automates QA, established LSP track record.

**Secondary recommendation**: hypomnema for software localization + large TM workflows

**Why**: TMX Level 2 preserves complex inline markup (software UI), streaming API handles very large TMs efficiently, MIT licensing safe for proprietary TMS integration, policy-driven validation enables client-specific QA rules.

**Hybrid approach**: translate-toolkit (general localization) + hypomnema (software localization)
- Leverage translate-toolkit's multi-format conversion and CLI tools for 90% of workflows
- Use hypomnema for 10% requiring Level 2 or streaming (large software localization projects)

**Key requirement match**:
- ✅ Multi-client TM isolation (both libraries support per-client file separation)
- ✅ CAT tool interoperability (translate-toolkit Level 1, hypomnema Level 2)
- ✅ Batch processing performance (both efficient, hypomnema streaming for >1 GB files)
- ✅ Quality assurance automation (translate-toolkit pofilter, hypomnema custom policies)
- ✅ Multi-format pipeline (translate-toolkit 20+ formats, hypomnema TMX-only)
- ✅ Automation integration (both scriptable, translate-toolkit CLI, hypomnema Python API)

**Licensing consideration**:
- If embedding in proprietary TMS: hypomnema (MIT) required
- If external CLI tools: translate-toolkit (GPL) acceptable

This persona prioritizes multi-format flexibility and automation over manual workflows, production stability over cutting-edge features, and commercial SaaS compatibility if building proprietary TMS.
