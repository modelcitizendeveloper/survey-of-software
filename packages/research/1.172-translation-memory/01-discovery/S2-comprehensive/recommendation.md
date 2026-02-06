# S2 Comprehensive Pass: Recommendations

## Key Technical Insights

### The Three Standards Work Together

| Standard | Purpose | Use In Workflow |
|----------|---------|----------------|
| **XLIFF** | Active translation projects | Extracting, translating, merging files |
| **TMX** | Translation memory exchange | Archiving, sharing translation assets |
| **TBX** | Terminology management | Maintaining approved vocabulary |

**Mental Model:**
- **XLIFF** = Document on the translator's desk (work in progress)
- **TMX** = Filing cabinet of completed translations (the memory)
- **TBX** = Dictionary of approved terms (the reference)

### TMX Remains Stable Despite Age

**TMX 1.4b (2005)** is 21 years old in 2026, yet:
- Still the universal standard
- No competing format has emerged
- All CAT tools support it
- No active development, but no need for updates

**Lesson:** Sometimes "good enough" standards persist because interoperability matters more than cutting-edge features.

### XLIFF Evolution is Slow

**XLIFF 2.x** was approved as ISO standard (2024), but:
- Many tools still use XLIFF 1.2
- Migration slower than expected
- Both versions coexist in 2026

**Implication:** When implementing XLIFF support, start with 1.2 for compatibility, add 2.x support later.

### Cloud is Winning for New Deployments

**Market Shift:**
- Established tools: Desktop (Trados, MemoQ on Windows)
- New entrants: Cloud-native (Smartcat, Phrase)
- Hybrid approaches: Desktop tools adding cloud features

**Why Cloud Wins:**
- No installation/updates
- Platform-agnostic (works on macOS/Linux)
- Team collaboration easier
- CI/CD integration simpler

**Why Desktop Persists:**
- Agency requirements (Trados standard)
- Data control (self-hosted)
- Offline work
- Performance (large files)

## Tool Selection Decision Tree

### Start Here: What's Your Context?

#### Context 1: Individual Translator

**Do agencies require Trados?**
- **Yes** → SDL Trados Studio (Windows required)
- **No** → Go to next question

**What's your budget?**
- **Zero** → OmegaT (desktop) or Wordfast Anywhere (cloud)
- **Moderate** → MemoQ ($44/month) if advanced features needed
- **Flexible** → Smartcat (marketplace access, modern UX)

**What's your platform?**
- **Windows** → All options available
- **macOS/Linux** → OmegaT, Smartcat, Phrase, or Wordfast Anywhere

#### Context 2: Translation Agency

**What's your vendor management model?**
- **External vendors** → SDL Trados or MemoQ (industry standard, vendors expect these)
- **Building vendor network** → Smartcat (integrated marketplace)

**How many projects per month?**
- **Low volume** → Desktop tools (Trados, MemoQ)
- **High volume with repetitive workflows** → Phrase (automation, AI-driven)

#### Context 3: Software Company

**How often do you release?**
- **Continuous deployment** → Phrase (CI/CD integration, API-first)
- **Periodic releases** → Smartcat (integrations, ease of use)
- **Occasional localization** → OmegaT (free, no ongoing costs)

**Data sovereignty requirements?**
- **Must be self-hosted** → OmegaT (only truly self-hosted option)
- **Cloud acceptable** → Smartcat or Phrase

## Implementation Patterns

### Pattern 1: Full Localization Pipeline

**For Software Companies with CI/CD:**

1. **Source Code** → Extraction tool → **XLIFF files**
2. **XLIFF** → TMS (Phrase/Smartcat) → **Translator assignment**
3. **Translators** use CAT tool with **TM (TMX)** and **Termbase (TBX)**
4. **Completed XLIFF** → Merge tool → **Localized files**
5. **Export TM** → **TMX** for archival and next project

**Key Technologies:**
- XLIFF for file exchange
- TMX for translation asset building
- TBX for terminology governance
- Cloud TMS for orchestration

### Pattern 2: Agency-Driven Translation

**For Translation Agencies:**

1. **Client sends source files** (any format)
2. **Project manager** creates project in TMS
3. **Files converted** to XLIFF or tool-native format
4. **Translators assigned** (each uses their CAT tool)
5. **TM and Termbase shared** via TMX/TBX export/import
6. **QA checks** run (terminology, consistency)
7. **Completed files** delivered to client
8. **TM exported** to TMX for client deliverable

**Key Technologies:**
- TMX for TM sharing (vendor independence)
- TBX for client terminology
- XLIFF for format-agnostic workflows

### Pattern 3: Self-Hosted DIY

**For Organizations with Data Control Requirements:**

1. **OmegaT** installed on translators' machines
2. **TM files** stored on shared network drive
3. **TMX files** versioned in git
4. **Glossaries** maintained as simple text or TBX
5. **Custom scripts** for file conversion (to/from XLIFF)

**Key Technologies:**
- OmegaT (open source, self-hosted)
- TMX for TM sharing
- Git for version control
- Custom scripts (Python, etc.) for automation

## Common Pitfalls

### Pitfall 1: Ignoring Terminology Management

**Mistake:** Focus only on TM, neglect termbases
**Result:** Inconsistent terminology, failed QA checks, client complaints

**Solution:**
- Create TBX termbase early
- Import into all CAT tools
- Configure QA to enforce terminology

### Pitfall 2: Format Mismatch

**Mistake:** Assume all CAT tools handle the same formats identically
**Result:** Formatting lost, inline codes broken, manual cleanup required

**Solution:**
- Test round-trip (export → import → export) before production
- Use TMX Level 1 for plain text, Level 2 only when formatting critical
- Validate XLIFF with tool-specific validators

### Pitfall 3: Proprietary Lock-In

**Mistake:** Rely on tool-specific features without TMX/XLIFF export
**Result:** Vendor lock-in, can't switch tools, TM trapped

**Solution:**
- Regularly export TM to TMX
- Archive TMX files in version control
- Test TM portability (import into different tool annually)

### Pitfall 4: Over-Engineering for Small Projects

**Mistake:** Set up full TMS pipeline for occasional translation
**Result:** Overhead exceeds benefit, complexity slows down simple tasks

**Solution:**
- Start simple (OmegaT + TMX export)
- Add automation only when volume justifies it
- Use cloud tools for flexibility without infrastructure overhead

## Next Steps (S3 Need-Driven)

### Research Questions for S3

1. **Programmatic TMX Handling:**
   - Python libraries for TMX parsing/generation
   - Creating TM from existing translated documents (alignment)
   - TM quality metrics (scoring, cleaning, deduplication)

2. **MT + TM Hybrid Workflows:**
   - How to combine MT with TM in modern workflows
   - Post-editing vs. TM matching
   - Quality thresholds for MT vs. TM suggestions

3. **TM as a Service:**
   - APIs for TM lookup/storage
   - Cloud-based TM sharing
   - Real-time TM updates across distributed teams

4. **Alignment Tools:**
   - Creating TMX from source + translated documents
   - Sentence alignment algorithms
   - Tools: bitext alignment, LF Aligner, etc.

5. **Continuous Localization:**
   - Git integration for XLIFF files
   - Automated XLIFF extraction from code
   - CI/CD pipeline examples

### Research Questions for S4 (Strategic)

1. **Build vs. Buy for Enterprises:**
   - ROI calculations for CAT tool investments
   - Self-hosted TMS vs. cloud TMS cost comparison
   - When to build custom localization pipelines

2. **TM Governance:**
   - TM ownership (agency vs. client)
   - TM quality standards
   - TM asset valuation

3. **Strategic Tool Selection:**
   - Long-term vendor relationships
   - Avoiding lock-in
   - Migration paths between tools
