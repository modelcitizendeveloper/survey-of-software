# Use Case: Enterprise Localization Teams

## Who Needs This

**Role**: Software company with continuous localization pipeline (DevOps-integrated translation workflow)

**Context**:
- Technology company shipping localized software (web apps, mobile apps, SaaS products)
- Engineering-led localization (developers, not dedicated localization team)
- Continuous deployment (CI/CD pipelines, automated releases)
- Version control integration (Git workflows, pull request reviews)
- Infrastructure as code (Docker, Kubernetes, Terraform)
- Multiple products/repositories requiring translation

**Technical background**:
- Engineering team: Professional developers (Python, JavaScript, Go, etc.)
- DevOps team: CI/CD expertise (GitHub Actions, GitLab CI, Jenkins)
- Product managers: Minimal technical background, use web UIs
- Translators: External vendors or crowdsourced, submit via web portals
- Infrastructure: Cloud-native (AWS, GCP, Azure), containerized deployments

**Volume**:
- Strings per product: 1K-100K translatable segments
- Languages: 10-50 language pairs
- Release cadence: Weekly to daily deployments
- File sizes: 1 MB - 100 MB per language (all strings combined)
- Translation updates: Continuous (new features, bug fixes, copy changes)

## Requirements and Constraints

### Must-Have Requirements

1. **CI/CD integration**: Must automate TM extraction, translation import, validation in deployment pipeline
   - Why: Manual translation workflows block releases, need zero-touch automation

2. **Version control friendly**: Must generate diff-friendly files for code review
   - Why: Translation changes reviewed like code (Git pull requests, diff approval)

3. **Developer workflow integration**: Must fit existing i18n frameworks (React Intl, Django, Rails i18n)
   - Why: Developers use PO/JSON/YAML, TMX for external translators only

4. **Quality checks in CI**: Must validate translations before deployment (completeness, format consistency)
   - Why: Broken translations in production damage user experience, need pre-deployment checks

5. **Automated TM updates**: Must update translation memory from completed translations without manual intervention
   - Why: Manual TM maintenance bottlenecks rapid release cycles

6. **Format conversion pipeline**: Must convert between developer formats (PO, JSON) and translator formats (TMX)
   - Why: Developers commit PO, translators work in CAT tools (TMX), need bidirectional conversion

### Constraints

- **Licensing**: MIT required for proprietary software products
  - GPL copyleft problematic if embedding in commercial SaaS (legal uncertainty)

- **Python version**: CI/CD runners support Python 3.11+ (Docker images controllable)
  - Can adopt Python 3.12+ if benefits justify Dockerfile updates

- **Platform**: Linux CI runners (GitHub Actions, GitLab CI, Jenkins)
  - Windows/Mac compatibility unnecessary (automation server-side)

- **Dependencies**: Acceptable if Dockerizable (lxml, C extensions OK)
  - CI runner images pre-built, dependency installation one-time cost

- **Learning curve**: Engineering team can learn Python APIs, product managers need CLIs
  - Developer-friendly documentation critical, GUI optional (web portals exist)

### Nice-to-Have Features

- Translation memory analytics (coverage, reuse rate across products)
- Terminology extraction (build glossaries from TM automatically)
- Machine translation integration (pre-translate with MT, human post-edit)
- Translation suggestions in developer IDEs (VS Code extension showing TM matches)
- Internationalization linting (detect hard-coded strings in code)

### Anti-Requirements

- CAT tool server hosting (use external translation vendors, not in-house CAT tools)
- Complex TM management (prefer simple files in Git over database solutions)
- Multi-tenancy (single company, not LSP managing multiple clients)
- TMX Level 2 for typical workflows (UI strings rarely have complex inline markup)

## Current Workflow and Pain Points

### As-Is Workflow

1. **Development**: Engineers write code with i18n framework (React Intl, Django gettext)
2. **Extraction**: Extract translatable strings to PO files via CLI (django-admin makemessages, formatjs extract)
3. **Commit**: Commit updated PO files to Git (new strings, changed copy)
4. **Translation**: Export PO → TMX, send to translation vendor
5. **Import**: Vendor returns translated TMX, convert TMX → PO
6. **Validation**: Manual review of translated PO files (completeness, format)
7. **Deployment**: Compile PO → MO, deploy to production

### Pain Points

1. **Manual format conversion**: Engineers manually run `po2tmx`, email TMX to vendors, reverse on return
   - Need: CI/CD pipeline automates conversion, vendor portal integration

2. **Git conflicts on PO files**: Multiple developers add strings simultaneously, merge conflicts on line numbers
   - Need: Better merge strategies, or alternative format (JSON, YAML) with less conflict

3. **No pre-deployment validation**: Broken translations (missing placeholders, wrong variables) reach production
   - Need: Automated QA checks in CI before merging pull requests

4. **TM fragmentation**: Translation memory scattered across vendor emails, no central repository
   - Need: Git-based TM versioning, single source of truth

5. **Slow translation turnaround**: Manual vendor communication delays releases
   - Need: Vendor portal integration (API-driven TM upload/download)

6. **No translation reuse tracking**: Unknown how many strings reused vs new translations (budget planning difficult)
   - Need: TM analytics (coverage, reuse rate) per release

## Library Fitness Assessment

### translate-toolkit

**Fitness rating**: **Primary fit for multi-format CI/CD pipelines**

**Rationale**:
- **Multi-format support**: Converts PO, JSON, YAML, XLIFF → TMX for vendor delivery, TMX → PO for developer import
- **Command-line tools**: `po2tmx`, `tmx2po`, `pofilter` scriptable in CI/CD (GitHub Actions, GitLab CI)
- **Quality checks**: `pofilter` with 40+ checks (untranslated, mismatched variables, XML tag errors) integrates into CI
- **Mature and stable**: 10+ years in production, rare breaking changes (low maintenance burden)
- **Python 3.11 compatible**: Works on standard CI runners (no infrastructure upgrades)

**Trade-offs**:
- **GPL licensing**: Problematic if embedding in SaaS product
  - Mitigation: Use as external CLI tool (subprocess calls), not library import
  - Risk: Legal gray area (linking vs usage), may require legal review

- **TMX Level 1 only**: Sufficient for most UI strings
  - Gap: Complex software UI with nested formatting may need Level 2 (rare)

- **No native JSON/YAML support**: Requires custom converters
  - Mitigation: Use existing tools (i18next-conv, yaml2po) then po2tmx

- **PO-centric**: Git merge conflicts on line numbers remain (not solved by library)
  - Mitigation: Use `msgcat --use-first` for automated conflict resolution

**Why it fits**: Designed for localization automation, established CI/CD integration patterns, comprehensive format support for diverse developer frameworks.

### hypomnema

**Fitness rating**: **Acceptable fit for modern Python 3.12+ stacks**

**Rationale**:
- **MIT licensing**: Safe for proprietary SaaS products, no GPL copyleft concerns
- **Type safety**: Full type hints enable robust CI/CD pipelines (mypy catches errors before deployment)
- **Streaming API**: Efficient for large monorepo TMs (100+ MB, millions of strings)
- **TMX Level 2**: Handles complex UI formatting (if needed)
- **Policy-driven validation**: Custom QA rules (e.g., brand-specific terminology checks)

**Trade-offs**:
- **Python 3.12+ requirement**: Requires CI runner Dockerfile updates
  - Cost: One-time Dockerfile change, but delays adoption if infrastructure frozen

- **No CLI tools**: Requires custom Python scripts for every operation
  - Impact: Engineering team must build wrapper scripts (po → TMX, TMX → po, QA checks)

- **TMX-only**: No PO/JSON/YAML conversion built-in
  - Impact: Must use separate tools (i18next-conv, polib) then hypomnema for TMX only

- **Pre-1.0 status**: API changes may break CI pipelines
  - Risk: Deployment blocked if library update requires code changes
  - Mitigation: Pin version in Dockerfile, allocate engineer time for updates

- **Small community**: Limited CI/CD integration examples, slower issue resolution
  - Impact: Team must read source code, contribute fixes if bugs found

**Why it might fit**: If building proprietary localization platform (MIT required), Python 3.12+ stack, and engineering team can build custom tooling, hypomnema's type safety and flexibility justify development effort. Otherwise, translate-toolkit's ready-to-use CLI tools superior.

### polib

**Fitness rating**: **Acceptable fit for PO-only workflows**

**Rationale**:
- **Zero dependencies**: Pure Python, simplifies CI Docker images
- **MIT licensing**: Safe for proprietary products
- **PO-native**: Direct manipulation of Django/Flask/gettext PO files
- **Simple API**: Easy for engineers to script (lower learning curve than translate-toolkit)

**Trade-offs**:
- **No native TMX**: Requires translate-toolkit for TMX conversion (defeats zero-dependency advantage)
- **No quality checks**: Must build custom QA or use translate-toolkit's pofilter
- **PO-only**: If developers adopt JSON/YAML i18n, polib irrelevant
- **No CLI tools**: Requires scripting for every operation

**Why it might fit**: If developers exclusively use PO (Django, Rails gettext), rarely export TMX (vendors work directly in PO), and need simple PO manipulation, polib offers lightweight solution. However, most enterprises need TMX for external vendors, requiring translate-toolkit anyway.

## Decision Criteria

### Use translate-toolkit if:
- Multi-format conversion critical (PO, JSON, YAML, XLIFF to TMX and back)
- CLI tools preferred (minimize custom scripting, integrate via shell in CI/CD)
- Quality checks needed (pofilter's 40+ tests valuable for pre-deployment validation)
- GPL licensing acceptable (external CLI tool, not embedded library)
- Python 3.11 infrastructure (no budget for Dockerfile updates)
- Rapid adoption needed (mature library, extensive documentation, community examples)

### Use hypomnema if:
- MIT licensing required (embedding in proprietary localization SaaS)
- Type safety critical (large engineering team, mypy/Pylance in CI)
- Building custom localization platform (not just CI/CD automation)
- Python 3.12+ stack (modern infrastructure, Dockerfile updates acceptable)
- Engineering team can build wrapper scripts (no ready-to-use CLI tools)
- TMX Level 2 needed (complex UI formatting with nested inline markup)

### Use polib if:
- PO-only workflow (no TMX export to external vendors)
- Zero dependencies valued (minimal Docker images)
- Simple PO manipulation scripts (not comprehensive localization automation)
- MIT licensing required

### Use hybrid (polib + translate-toolkit) if:
- Developers use PO (polib for manipulation)
- External vendors use TMX (translate-toolkit for conversion)
- Separation of concerns (polib for dev workflows, translate-toolkit for vendor integration)

## Migration Considerations

### Migrating from Manual Workflow to CI/CD Automation

**Scenario**: Currently manual PO → TMX conversion, email to vendors, manual import

**With translate-toolkit**:
1. Add GitHub Actions workflow:
   - On commit to `main`: extract PO changes, convert to TMX via `po2tmx`, upload to vendor portal API
   - On vendor webhook: download translated TMX, convert to PO via `tmx2po`, open pull request
   - On pull request: run `pofilter` QA checks, block merge if errors exceed threshold
2. Store TM in Git LFS (large file versioning)
3. Generate TM analytics (coverage, reuse rate) via custom script

**Benefits**:
- Zero manual conversion (CI handles po2tmx/tmx2po automatically)
- Translation changes reviewable in pull requests (Git diff approval)
- QA checks prevent broken translations in production

**Costs**:
- Initial CI pipeline setup (GitHub Actions YAML, vendor API integration)
- Team training (Git-based translation workflow vs email-based)
- Vendor onboarding (API integration vs manual email)

### Compatibility with Developer Frameworks

**Framework integration**:
- **Django**: `django-admin makemessages` extracts PO → `po2tmx` converts for vendors → `tmx2po` imports back → `compilemessages` generates MO
- **React Intl**: `formatjs extract` generates JSON → custom JSON→PO converter → `po2tmx` for vendors
- **Rails i18n**: YAML files → `yaml2po` → `po2tmx` for vendors
- **iOS/Android**: XLIFF files → `xliff2tmx` (translate-toolkit) for vendors

**CI/CD integration patterns**:
- **Pre-commit hook**: Run `pofilter` before commit (catch errors early)
- **Pull request check**: Run `pofilter` on changed PO files (block merge if QA fails)
- **Deployment gate**: Run `pofilter` before production deploy (final safety check)

**Data preservation**:
- Round-trip fidelity: PO → TMX → PO preserves msgid, msgstr, comments (translator notes)
- Metadata retention: Git commit history tracks translation changes over time
- TM versioning: Git tags link TM state to software releases (rollback capability)

## Recommended Workflow Patterns

### Pattern 1: Fully Automated CI/CD Translation Pipeline

**Scenario**: React app with continuous deployment, external translation vendor with API

**Workflow**:
1. Developer adds new strings in React components (React Intl)
2. CI extracts strings on commit: `formatjs extract` → JSON → custom JSON→PO converter → PO files
3. CI detects new strings: `git diff` on PO files
4. CI converts PO → TMX: `po2tmx --duplicates=merge new-strings.po new-strings.tmx`
5. CI uploads TMX to vendor API: `curl -X POST vendor.com/api/upload -F tmx=@new-strings.tmx`
6. Vendor translates, triggers webhook on completion
7. CI downloads translated TMX: `curl vendor.com/api/download/{job_id} > translated.tmx`
8. CI converts TMX → PO: `tmx2po translated.tmx translated.po`
9. CI opens pull request with translated PO files
10. Engineer reviews translation diff, merges
11. CI compiles PO → JSON: custom PO→JSON converter → React build includes translations
12. Deploy to production

**Benefits**: Zero manual translation management, translation changes reviewed like code, deployment blocked until translations complete

### Pattern 2: Quality-Gated Deployment

**Scenario**: Django app with weekly releases, manual vendor workflow but automated QA

**Workflow**:
1. Engineer freezes features on Friday (string freeze)
2. CI extracts PO: `django-admin makemessages --all`
3. CI runs QA checks: `pofilter --test=all django.po qa-report.po`
4. If QA passed: CI converts PO → TMX, engineer emails to vendor
5. Vendor returns TMX on Tuesday
6. Engineer converts TMX → PO: `tmx2po vendor-translated.tmx django-es.po`
7. Engineer commits translated PO, opens pull request
8. CI runs QA on pull request: `pofilter django-es.po` (block merge if failures)
9. If QA passed: merge, deploy on Wednesday

**Benefits**: Automated QA prevents broken translations in production, manual steps only for vendor communication

### Pattern 3: Monorepo Translation Memory Consolidation

**Scenario**: Multiple products in monorepo, shared TM for consistency

**Workflow**:
1. Each product has `translations/` directory with PO files
2. CI consolidates TM: `find . -name "*.po" -exec po2tmx --duplicates=merge {} + > company-tm.tmx`
3. CI commits consolidated TM to `shared-tm/company-tm.tmx` (Git LFS)
4. On new project: engineers extract relevant TM subset via language pair
5. CI analytics: measure translation reuse across products (calculate leverage)

**Benefits**: Single source of truth for company TM, cross-product translation consistency, reuse analytics for budget planning

## Alternative Considerations

### When Commercial Localization Platform Better

Custom CI/CD automation ideal for engineering-led teams, but commercial platforms may fit better if:
- **Non-technical product managers**: Need GUI workflow, not Git/CI/CD
- **Complex vendor management**: Multiple vendors, bidding, quality scoring (beyond simple API integration)
- **Integrated CAT tools**: In-house translators prefer web-based CAT over external vendors
- **Enterprise budget**: Multi-million dollar contract justifies platform licensing costs

Examples: Phrase, Smartling, Crowdin, Lokalise (SaaS platforms with Git integration, CI/CD plugins)

Hybrid common: Commercial platform for PM/translator UI + translate-toolkit for CI/CD integration via platform APIs

### When to Build Custom Localization Platform

Build custom platform using hypomnema or translate-toolkit if:
- Proprietary workflow (e.g., game localization with asset management)
- Platform licensing costs exceed in-house development (Python developer + infrastructure cheaper)
- Deep integration with existing systems (CMS, customer support, product analytics)
- MIT licensing required (embedding in SaaS product sold to other companies)

## Summary: Enterprise Localization Recommendation

**Primary recommendation**: translate-toolkit for multi-format CI/CD automation

**Why**: Multi-format support (PO, JSON, XLIFF → TMX) handles diverse developer frameworks, CLI tools (`po2tmx`, `tmx2po`, `pofilter`) integrate easily into GitHub Actions/GitLab CI, mature/stable reduces CI maintenance burden, comprehensive QA checks (`pofilter`) prevent broken translations in production.

**Secondary recommendation**: hypomnema for proprietary localization platforms

**Why**: MIT licensing safe for SaaS products, type safety (Python 3.12+) enables robust CI/CD pipelines, streaming API handles large monorepo TMs, policy-driven validation enables custom QA rules. Trade-off: engineering effort to build wrapper scripts vs translate-toolkit's ready-to-use CLI tools.

**Hybrid approach**: translate-toolkit (CI/CD automation) + commercial platform (PM/translator UI)
- Use translate-toolkit for automated format conversion, QA checks in CI
- Use Phrase/Smartling/Crowdin for non-technical PM/translator workflow
- Integrate via platform APIs (translate-toolkit handles Git → platform upload, platform → Git download)

**Key requirement match**:
- ✅ CI/CD integration (translate-toolkit CLI scriptable, hypomnema Python API)
- ✅ Version control friendly (both generate TMX, PO files for Git diff)
- ✅ Developer workflow integration (translate-toolkit multi-format, hypomnema via custom scripts)
- ✅ Quality checks in CI (translate-toolkit pofilter, hypomnema custom policies)
- ✅ Automated TM updates (both enable scripted TM consolidation)
- ✅ Format conversion pipeline (translate-toolkit 20+ formats, hypomnema TMX-only)

**Licensing consideration**:
- If embedding in proprietary SaaS: hypomnema (MIT) required
- If external CLI tools: translate-toolkit (GPL) acceptable (subprocess usage, not library import)

This persona prioritizes CI/CD automation over manual workflows, version control integration for translation review, and quality gates to prevent broken translations in production.
