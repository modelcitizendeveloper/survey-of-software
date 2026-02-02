# Use Case: Freelance Translators

## Who Needs This

**Role**: Solo translator or small freelance collective

**Context**:
- Works independently across multiple clients and projects
- Uses commercial CAT tools (SDL Trados, memoQ, Wordfast, OmegaT)
- Manages personal translation memory built over years
- Limited budget for specialized software or infrastructure
- No dedicated IT support or programming team

**Technical background**:
- May have basic scripting knowledge (not a professional developer)
- Comfortable with command-line tools if well-documented
- Uses Windows or Mac, standard Python installation
- Focuses on translation quality, not software engineering

**Volume**:
- Personal TM: 10K-500K translation units accumulated over career
- Typical project: 1K-10K new segments
- File sizes: Usually <50 MB

## Requirements and Constraints

### Must-Have Requirements

1. **CAT tool interoperability**: Must export/import TMX files compatible with commercial CAT tools (Trados, memoQ)
   - Why: Client projects use different CAT tools, need seamless TM exchange

2. **PO ↔ TMX conversion**: Must convert between PO and TMX formats
   - Why: Many open source projects use PO files, clients expect TMX deliverables

3. **Simple command-line tools**: Must work without writing complex Python code
   - Why: Not a programmer, needs ready-to-use tools for batch operations

4. **Stable, production-ready**: Must be mature with minimal breaking changes
   - Why: No time to debug library updates, translation deadlines critical

5. **Zero-cost licensing**: Must be free to use commercially
   - Why: Freelance budget constraints, cannot afford per-project licensing fees

### Constraints

- **Python version**: Likely Python 3.11 or whatever comes with OS (no budget for infrastructure upgrades)
- **Platform**: Windows or Mac (standard consumer hardware)
- **Dependencies**: Comfortable with pip install if dependencies have pre-compiled wheels
- **Learning curve**: Limited time to learn new tools (needs good documentation and examples)
- **Licensing**: Both GPL and MIT acceptable (not distributing software, just using tools)

### Nice-to-Have Features

- Quality checks (find untranslated segments, mismatched formatting)
- Merge multiple TM files from different projects
- Extract terminology from TM for glossary building
- Search/filter TM by language pair, client, date

### Anti-Requirements

- TMX Level 2 structured inline markup (CAT tools handle this internally)
- Type safety and IDE autocomplete (not writing large codebases)
- Streaming API for large files (personal TM fits in memory)
- Custom validation policies (standard CAT tool validation sufficient)

## Current Workflow and Pain Points

### As-Is Workflow

1. Receive project from client (various CAT tool formats)
2. Import client TM into CAT tool
3. Translate in CAT tool, leveraging personal TM
4. Export updated TM as TMX for client deliverable
5. Merge translated segments into personal TM
6. Occasionally convert open source PO files to TMX for personal use

### Pain Points

1. **TM fragmentation**: Personal TM scattered across multiple CAT tool exports
   - Need: Consolidate TMs into single master file

2. **Format incompatibility**: Some clients provide PO files, CAT tools expect TMX
   - Need: Reliable PO → TMX conversion without manual editing

3. **Quality assurance**: Manual checks for untranslated segments time-consuming
   - Need: Automated QA checks before client delivery

4. **TM bloat**: Years of translations include outdated or low-quality entries
   - Need: Filter/clean TM programmatically

5. **No version control**: Single TM file, no backup or change tracking
   - Need: Integration with simple backup workflow (Dropbox, Git)

## Library Fitness Assessment

### translate-toolkit

**Fitness rating**: **Primary fit**

**Rationale**:
- **Command-line tools**: `po2tmx` and `tmx2po` CLI tools work out-of-box, no Python coding required
- **CAT tool compatibility**: Generates TMX Level 1 files compatible with all major CAT tools (Trados, memoQ, Wordfast)
- **Multi-format support**: Converts 20+ formats (PO, XLIFF, RC, etc.) to TMX, enabling broad client support
- **Quality checks**: `pofilter` tool with 40+ checks for translation quality
- **Mature and stable**: 10+ years in production, rare breaking changes
- **Documentation**: Comprehensive guides with command-line examples

**Trade-offs**:
- **GPL licensing**: Acceptable for tool usage (only problematic if distributing modified software)
- **TMX Level 1 only**: Sufficient for CAT tool interoperability (Level 2 not needed)
- **Memory usage**: May struggle with very large personal TMs (>500K units), but most freelancers below this threshold

**Why it fits**: Designed for localization practitioners who need reliable format conversion and quality checks without programming expertise.

### hypomnema

**Fitness rating**: **Poor fit**

**Rationale**:
- **No CLI tools**: Requires Python coding, not suitable for non-programmers
- **Python 3.12+ requirement**: Likely not available on freelancer's system without infrastructure upgrade
- **TMX Level 2**: Over-engineered for CAT tool interoperability (Level 1 sufficient)
- **Pre-1.0 status**: Breaking changes risk workflow disruption during busy project seasons
- **Minimal documentation**: Lacks beginner-friendly tutorials and command-line examples

**Trade-offs**:
- **MIT licensing**: Licensing advantage irrelevant if tool unusable without coding
- **Streaming API**: Personal TM files small enough for in-memory processing
- **Type safety**: Unnecessary for simple one-off scripts

**Why it doesn't fit**: Designed for developers building custom TMX processing pipelines, not translators needing ready-to-use tools.

### polib + translate-toolkit

**Fitness rating**: **Acceptable fit**

**Rationale**:
- **PO-centric workflow**: If freelancer primarily works with open source projects (PO files), polib offers simpler PO manipulation
- **Conversion via translate-toolkit**: Use translate-toolkit's po2tmx for TMX export when needed
- **Simpler API**: polib easier to learn for basic scripting compared to translate-toolkit's TMX API
- **Zero dependencies**: polib pure Python, easier installation if lxml wheels problematic

**Trade-offs**:
- **Indirect TMX support**: Requires translate-toolkit dependency for TMX conversion (two libraries instead of one)
- **Conversion loss**: Round-trip PO → TMX → PO loses some metadata (tuid, custom properties)
- **No quality checks**: polib lacks translate-toolkit's pofilter tool

**Why it might fit**: If 80% of work is PO files (open source translation), with occasional TMX export for clients, polib + translate-toolkit combination offers simpler PO manipulation.

## Decision Criteria

### Use translate-toolkit if:
- Primary workflow involves TMX files from multiple CAT tools
- Need command-line tools for batch conversion (PO → TMX, XLIFF → TMX)
- Quality checks (pofilter) valuable for client deliverables
- Comfortable with GPL licensing (tool usage, not redistribution)
- Python 3.11 available (standard on most systems)

### Use polib + translate-toolkit if:
- 80%+ of projects use PO files (open source, Django/Flask projects)
- Prefer simpler PO manipulation API, only occasional TMX export
- Comfortable managing two libraries (polib for PO, translate-toolkit for TMX conversion)
- Need lxml-free installation (polib pure Python, translate-toolkit for conversion only)

### Avoid hypomnema if:
- Not comfortable writing Python code for every operation
- Python 3.12+ not available (and no budget/time for infrastructure upgrade)
- Need CLI tools, not a programming library
- Cannot afford downtime from pre-1.0 API changes during project deadlines

## Migration Considerations

### Migrating from Manual CAT Tool Workflow

**Scenario**: Currently export/import TMX manually via CAT tool GUI

**With translate-toolkit**:
- Learn basic command-line usage (batch scripts replace GUI clicks)
- Automate TM consolidation: merge multiple TMX exports into master TM
- Integrate quality checks before client delivery
- Version control: commit TM to Git, track changes over time

**Benefits**:
- Time savings on repetitive batch operations
- Consistent quality checks reduce client revisions
- TM backup via Git eliminates catastrophic loss risk

**Costs**:
- Initial learning curve (command-line tools, batch scripting)
- May need to learn basic shell scripting (bash/PowerShell)

### Compatibility with Existing TM

**CAT tool compatibility**:
- translate-toolkit: Generates TMX 1.4 compatible with Trados, memoQ, Wordfast, OmegaT
- Round-trip fidelity: TM exported from CAT tool → processed with translate-toolkit → re-imported retains structure

**Data preservation**:
- Translation units preserved
- Language pairs retained
- Inline formatting preserved as text (sufficient for CAT tool rendering)
- Metadata (creation date, author) preserved

**Risk mitigation**:
- Test workflow with small TM subset before processing master TM
- Keep backup of original CAT tool TM before automation
- Validate processed TMX by importing into CAT tool and spot-checking

## Recommended Workflow Pattern

### Initial Setup (One-Time)

1. Install Python 3.11+ (if not already available)
2. Install translate-toolkit: `pip install translate-toolkit`
3. Verify installation: `tmx2po --help`
4. Export master TM from primary CAT tool as TMX

### Daily Operations

**PO → TMX conversion for client deliverable**:
```
po2tmx --duplicates=merge client-project.po client-project.tmx
```

**TMX → PO conversion for open source work**:
```
tmx2po --duplicates=merge client-tm.tmx extracted-tm.po
```

**Quality check before client delivery**:
```
pofilter --test=untranslated,xmltags translated.po qa-report.po
```

**Merge new translations into master TM**:
```
# Export new translations from CAT tool as new-project.tmx
# Combine with master TM using CAT tool merge feature or custom script
```

### Backup and Version Control

**Simple Dropbox backup** (no Git knowledge):
- Store master TM in Dropbox folder
- Automatic versioning via Dropbox history

**Git version control** (if comfortable with basics):
```
git add master-tm.tmx
git commit -m "Added translations from Project ABC (500 new units)"
git push
```

## Alternative Considerations

### When Commercial Tools May Be Better

translate-toolkit is ideal for automation, but commercial solutions may fit better if:
- **No scripting interest**: Prefer GUI-only workflow, no desire to learn command-line
- **Budget available**: Commercial TM management software (SDL TM Server, Déjà Vu) offers integrated GUI
- **Team collaboration**: Multiple freelancers sharing TM, commercial server solutions offer conflict resolution

### When to Escalate to Developer Help

Hire a developer if:
- Custom quality checks beyond pofilter's 40+ tests
- Complex TM merging logic (e.g., prioritize client-specific translations over personal TM)
- Integration with invoicing/project management software
- Web-based TM search interface for quick lookups

Developer can build custom scripts using translate-toolkit's Python API, while freelancer uses resulting CLI tools.

## Summary: Freelance Translator Recommendation

**Primary recommendation**: translate-toolkit

**Why**: Command-line tools (po2tmx, tmx2po, pofilter) enable automation without programming, mature/stable library reduces disruption risk, multi-format support handles diverse client requirements, GPL licensing acceptable for tool usage.

**Key requirement match**:
- ✅ CAT tool interoperability (TMX Level 1 compatible with all major tools)
- ✅ PO ↔ TMX conversion (po2tmx / tmx2po CLI tools)
- ✅ Simple command-line tools (no Python coding required)
- ✅ Stable production-ready (10+ years, rare breaking changes)
- ✅ Zero-cost licensing (GPL acceptable for tool usage)

**When to consider alternatives**:
- If PO-centric workflow (80%+ open source projects): polib + translate-toolkit
- If no scripting interest: Commercial TM management software instead
- If need custom workflows: Hire developer to build translate-toolkit-based automation

This persona prioritizes ready-to-use tools over programming flexibility, stability over cutting-edge features, and cost-effectiveness over enterprise scalability.
