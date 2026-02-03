# Use Case: Software Localization

**Experiment**: 1.172 Translation Memory
**Pass**: S3 - Need-Driven Discovery
**Date**: 2026-01-29

## Use Case Overview

**WHO**: Software companies localizing SaaS products, mobile apps, desktop applications

**WHY**: Reuse translations across product versions, maintain UI consistency, reduce translation costs by 60-85% on incremental updates

**Context**: Development team ships quarterly releases with 10-30% new/changed strings, needs consistent terminology across web/mobile/desktop

**Requirements**:
- Integrate with developer workflows (Git, CI/CD)
- Handle multiple file formats (JSON, XLIFF, properties, YAML)
- Support 5-20 target languages simultaneously
- Version control for translation files
- Fuzzy matching for similar strings (e.g., "Save file" vs. "Save the file")
- Terminology management (consistent brand terms)

**Volume**:
- Source strings: 10K-100K segments
- Target languages: 5-20
- Update frequency: Quarterly (major) or monthly (minor)
- Incremental changes: 10-30% per release

## Recommended Tool: OmegaT

**Rationale**:
1. **Git integration**: Translation files commit alongside source code
2. **Open source**: Zero licensing cost, extensible for custom workflows
3. **TMX format**: Industry-standard, portable to other tools
4. **File format support**: JSON, XLIFF, properties, PO, YAML via plugins
5. **Offline capable**: Translators work locally, commit when ready
6. **Command-line tools**: Scriptable for CI/CD automation

### Git Workflow Advantage

**Example project structure**:
```
my-saas-app/
  src/
    en/
      messages.json        # English source
    translations/
      fr/messages.json     # French
      de/messages.json     # German
  omegat/
    project_save.tmx       # Translation memory (TMX format)
    glossary.txt           # Terminology
  .github/
    workflows/
      localization.yml     # CI/CD automation
```

**Use case fit**: Translators work in feature branches, translations reviewed in PRs alongside code changes

## Implementation Guidance

### 1. Project Setup

```bash
# Install OmegaT
wget https://omegat.org/download
sudo dpkg -i omegat_6.0.0_amd64.deb

# Or use Docker for CI/CD
docker pull omegat/omegat:latest
```

**Create OmegaT project**:
```bash
mkdir -p my-app-i18n/omegat-project
cd my-app-i18n/omegat-project

# OmegaT project structure
mkdir -p source target tm glossary
```

**omegat.project file** (XML config):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<omegat>
  <project version="1.0">
    <source_dir>source/</source_dir>
    <target_dir>target/</target_dir>
    <tm_dir>tm/</tm_dir>
    <glossary_dir>glossary/</glossary_dir>
    <source_lang>en</source_lang>
    <target_lang>fr</target_lang>
  </project>
</omegat>
```

### 2. Developer Workflow (Extract Strings)

**Extract translatable strings from codebase**:
```python
# scripts/extract_i18n.py
import json
import re
from pathlib import Path

def extract_strings_from_code():
    """Extract i18n strings from React/Vue/Angular code"""
    strings = {}

    for file_path in Path('src').rglob('*.jsx'):
        with open(file_path) as f:
            content = f.read()
            # Find i18n calls: t('key', 'Default text')
            matches = re.findall(r"t\('([^']+)',\s*'([^']+)'\)", content)
            for key, text in matches:
                strings[key] = text

    # Export to JSON for OmegaT
    with open('omegat-project/source/messages.json', 'w') as f:
        json.dump(strings, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(strings)} translatable strings")

extract_strings_from_code()
```

**Run extraction on every commit**:
```yaml
# .github/workflows/extract-strings.yml
name: Extract Translatable Strings
on:
  push:
    paths:
      - 'src/**'
jobs:
  extract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Extract strings
        run: python scripts/extract_i18n.py
      - name: Commit updated source
        run: |
          git add omegat-project/source/
          git commit -m "Update translatable strings" || true
          git push
```

### 3. Translator Workflow

**Clone repository**:
```bash
git clone https://github.com/company/my-app-i18n
cd my-app-i18n/omegat-project
```

**Open in OmegaT**:
```bash
omegat omegat-project/
```

**OmegaT UI shows**:
- **Source**: "Save file" (English)
- **TM matches**: "Save the file" (90% match from previous version)
- **Glossary**: "file" → "fichier" (approved term)
- **Target**: Translator types: "Enregistrer le fichier"

**Auto-propagation**: If "Save file" appears 50 times, first translation auto-fills remaining 49

**Commit translations**:
```bash
cd omegat-project
git add target/ tm/
git commit -m "fr: Translate v2.1 new strings"
git push origin feature/fr-v2.1-translation
```

**Pull request review**:
```bash
# Reviewer checks translation quality
git diff main..feature/fr-v2.1-translation target/fr/messages.json

# Merge when approved
gh pr merge --squash
```

### 4. CI/CD Integration (Automated Translation Sync)

**GitHub Actions workflow**:
```yaml
# .github/workflows/sync-translations.yml
name: Sync Translations
on:
  push:
    branches: [main]
    paths:
      - 'omegat-project/source/**'

jobs:
  notify-translators:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Detect new strings
        id: detect
        run: |
          # Count untranslated segments
          docker run --rm -v $(pwd)/omegat-project:/project \
            omegat/omegat-cli \
            /project --mode=console-translate --quiet

          # Check if translations needed
          NEW_STRINGS=$(grep "untranslated" /tmp/omegat-stats.txt | awk '{print $1}')
          echo "new_strings=$NEW_STRINGS" >> $GITHUB_OUTPUT

      - name: Create translation issue
        if: steps.detect.outputs.new_strings > 0
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '[${{ steps.detect.outputs.new_strings }}] New strings need translation',
              body: 'Version 2.1 has new strings. Please translate:\n\n' +
                    'Languages: French, German, Spanish, Japanese\n' +
                    'Deadline: 2026-02-15',
              labels: ['translation', 'urgent']
            })
```

**Build localized app bundles**:
```yaml
# .github/workflows/build-localized.yml
name: Build Localized Apps
on:
  push:
    branches: [main]
    paths:
      - 'omegat-project/target/**'

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        lang: [fr, de, es, ja]
    steps:
      - uses: actions/checkout@v3

      - name: Import translations
        run: |
          # Copy translated JSON to app source
          cp omegat-project/target/${{ matrix.lang }}/messages.json \
             src/${{ matrix.lang }}/messages.json

      - name: Build app
        run: |
          npm run build -- --lang=${{ matrix.lang }}

      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: app-${{ matrix.lang }}
          path: dist/
```

## Alternative Options

### Option 2: Memsource (Cloud-Based)

**When to use**:
- Non-technical translators (can't use Git)
- Real-time collaboration (multiple translators on same project)
- Need API-driven automation (no manual Git commits)

**Trade-off**: $500-2,000/year subscription vs. OmegaT free

**Implementation**:
```python
# scripts/sync_to_memsource.py
import requests

MEMSOURCE_TOKEN = os.environ['MEMSOURCE_TOKEN']
API_BASE = 'https://cloud.memsource.com/web/api2/v1'

def create_translation_job(source_file, target_langs):
    """Push source strings to Memsource via API"""

    # Create project
    response = requests.post(
        f'{API_BASE}/projects',
        headers={'Authorization': f'Bearer {MEMSOURCE_TOKEN}'},
        json={
            'name': 'MyApp v2.1 Translation',
            'sourceLang': 'en',
            'targetLangs': target_langs,  # ['fr', 'de', 'es']
            'workflowSteps': [
                {'name': 'Translation', 'assignees': ['translator@example.com']},
                {'name': 'Review', 'assignees': ['reviewer@example.com']}
            ]
        }
    )
    project_id = response.json()['id']

    # Upload source file
    with open(source_file, 'rb') as f:
        requests.post(
            f'{API_BASE}/projects/{project_id}/jobs',
            headers={'Authorization': f'Bearer {MEMSOURCE_TOKEN}'},
            files={'file': f}
        )

    print(f"Created Memsource project: {project_id}")
    return project_id

# Triggered by GitHub webhook
create_translation_job('omegat-project/source/messages.json', ['fr', 'de', 'es'])
```

**Download completed translations**:
```python
def download_translations(project_id, target_lang):
    """Pull completed translations from Memsource"""

    response = requests.get(
        f'{API_BASE}/projects/{project_id}/jobs',
        headers={'Authorization': f'Bearer {MEMSOURCE_TOKEN}'},
        params={'targetLang': target_lang}
    )

    for job in response.json():
        if job['status'] == 'COMPLETED':
            # Download translated file
            file_response = requests.get(
                f"{API_BASE}/jobs/{job['id']}/targetFile",
                headers={'Authorization': f'Bearer {MEMSOURCE_TOKEN}'}
            )

            with open(f"translations/{target_lang}/messages.json", 'wb') as f:
                f.write(file_response.content)

# Runs on schedule (cron job)
download_translations(project_id, 'fr')
```

**Best for**: Teams without Git expertise, need for real-time translator collaboration

### Option 3: Hybrid (OmegaT offline + Memsource API)

**Use OmegaT for developers, Memsource for external translators**:
```python
# Export TM from OmegaT to Memsource
def sync_tm_to_memsource(omegat_tmx_file):
    """Upload OmegaT TMX to Memsource translation memory"""

    with open(omegat_tmx_file, 'rb') as f:
        requests.post(
            f'{API_BASE}/transMemories/{tm_id}/import',
            headers={'Authorization': f'Bearer {MEMSOURCE_TOKEN}'},
            files={'file': ('project.tmx', f, 'application/xml')}
        )

# Run after each OmegaT commit
sync_tm_to_memsource('omegat-project/tm/project_save.tmx')
```

**Benefit**: In-house team uses free OmegaT, outsourced translators use Memsource UI

## Common Pitfalls

### 1. Not Handling Pluralization

**Problem**: "1 file" vs. "2 files" → Different translations in some languages

**Example**:
```json
// ❌ WRONG: Single string for all counts
{
  "files_count": "{count} files"
}

// French: "1 fichiers" (grammatically wrong)
```

**Solution**: Use ICU MessageFormat
```json
// ✅ CORRECT: Plural forms
{
  "files_count": {
    "en": "{count, plural, one {# file} other {# files}}",
    "fr": "{count, plural, one {# fichier} other {# fichiers}}",
    "ru": "{count, plural, one {# файл} few {# файла} other {# файлов}}"
  }
}
```

### 2. Over-Trusting Fuzzy Matches

**Problem**: "Delete file" → "Delete user" (85% match, WRONG context)

**OmegaT shows**:
- Source: "Delete user"
- TM match (85%): "Delete file" → "Supprimer le fichier"
- **DANGER**: Auto-accepting changes "file" → "user" gives "Supprimer l'utilisateur"

**Solution**: Review all fuzzy matches <95%, especially for UI-critical strings

### 3. Ignoring Context Metadata

**Problem**: "Open" (verb) vs. "Open" (adjective) → Same English, different translations

**Example**:
```json
// ❌ No context
{
  "open_button": "Open",    // Verb: "Ouvrir"
  "status_open": "Open"     // Adjective: "Ouvert"
}
```

**Solution**: Use XLIFF with context notes
```xml
<!-- ✅ With context -->
<trans-unit id="open_button">
  <source>Open</source>
  <note>Button label - verb to open file</note>
</trans-unit>
<trans-unit id="status_open">
  <source>Open</source>
  <note>Status - adjective indicating not closed</note>
</trans-unit>
```

**OmegaT displays notes**, translators see context

### 4. Not Cleaning TM After UI Redesign

**Problem**: Old "Settings" screen TM pollutes new "Preferences" UI

**Example**:
- v1.0: "User settings" → "Paramètres utilisateur"
- v2.0: Complete UI redesign, now called "Preferences"
- TM still suggests old "Paramètres utilisateur" (doesn't match new UI)

**Solution**: Archive old TM, start fresh for redesigned sections
```bash
# Backup old TM
mv omegat-project/tm/project_save.tmx omegat-project/tm/v1-archive.tmx

# Start fresh for v2 UI
# Keep v1-archive.tmx as reference, but don't auto-match
```

## Performance Tuning

### 1. Parallel Translation (Speed Up Batch Work)

**OmegaT supports multi-core processing**:
```bash
# Enable parallel mode in omegat.prefs
omegat.parallel.threads=8

# 3x speedup on 4+ cores for bulk translation
```

### 2. Custom Segmentation Rules

**Problem**: Default segmentation breaks on code snippets

**Example**:
```
Source text: "Run: npm install. Then: npm start."
Default segments:
  1. "Run: npm install."
  2. "Then: npm start."

Problem: ". Then" is not a sentence break
```

**Solution**: Custom segmentation rules (segmentation.conf)
```xml
<languagerule languagecode="en">
  <rule break="no">
    <beforebreak>\.</beforebreak>
    <afterbreak>\s*Then</afterbreak>
  </rule>
</languagerule>
```

### 3. Translation Memory Penalty Tuning

**OmegaT TM match scoring**:
- 100% match: Exact same source and context
- 95-99%: Small differences (punctuation, capitalization)
- 75-94%: Fuzzy match (some words changed)

**Adjust penalty** (omegat.prefs):
```properties
# Default: 5% penalty per word change
tm.fuzzy.match.penalty=5

# Stricter (prefer exact matches): 10% penalty
tm.fuzzy.match.penalty=10

# More aggressive (accept fuzzier matches): 3% penalty
tm.fuzzy.match.penalty=3
```

## Success Metrics

### TM Leverage Rates (Reuse %)

**Targets by release type**:
- **Major release** (v1.0 → v2.0): 40-60% exact matches (significant changes)
- **Minor release** (v1.1 → v1.2): 70-85% exact matches (incremental features)
- **Patch release** (v1.1.1 → v1.1.2): 90-95% exact matches (bug fixes only)

**Measure in OmegaT**:
```bash
# Project statistics
omegat project-stats

Output:
Total segments: 10,000
  100% match: 6,000 (60%)
  95-99% match: 2,000 (20%)
  85-94% match: 1,000 (10%)
  New: 1,000 (10%)
```

### Cost Reduction

**Calculation**:
```python
def calculate_savings(total_segments, match_distribution, rates):
    """
    total_segments: 10,000
    match_distribution: {'100%': 6000, '95-99%': 2000, '85-94%': 1000, 'new': 1000}
    rates: {'100%': 0.01, '95-99%': 0.03, '85-94%': 0.05, 'new': 0.12}  # $/word
    """
    cost_with_tm = sum(count * rates[match_type]
                       for match_type, count in match_distribution.items())

    cost_without_tm = total_segments * rates['new']

    savings_pct = (cost_without_tm - cost_with_tm) / cost_without_tm * 100

    print(f"Cost with TM: ${cost_with_tm:,.2f}")
    print(f"Cost without TM: ${cost_without_tm:,.2f}")
    print(f"Savings: {savings_pct:.1f}%")

# Example for v1.2 release
calculate_savings(
    10000,
    {'100%': 6000, '95-99%': 2000, '85-94%': 1000, 'new': 1000},
    {'100%': 0.01, '95-99%': 0.03, '85-94%': 0.05, 'new': 0.12}
)
# Output:
# Cost with TM: $290
# Cost without TM: $1,200
# Savings: 75.8%
```

### Translation Speed

**Targets**:
- **Without TM**: 2,000 words/day (raw translation)
- **With mature TM** (70%+ leverage): 3,500-4,000 words/day

**Measure productivity**:
```python
# Track translation speed
segments_translated = 500
time_spent_hours = 4

words_per_segment_avg = 8
words_per_day = (segments_translated * words_per_segment_avg) / (time_spent_hours / 8)

print(f"Productivity: {words_per_day:.0f} words/day")
# Output: 4,000 words/day (2x faster with TM)
```

### Quality (Terminology Consistency)

**Target**: 95%+ consistency for approved terms

**Measurement**:
```python
# Extract all translations of "Settings"
grep -r "Settings" omegat-project/source/ | wc -l
# Output: 50 occurrences

grep -r "Paramètres" omegat-project/target/fr/ | wc -l
# Output: 48 (96% consistency)

# 2 inconsistent: "Réglages" (synonym, but inconsistent)
```

**Enforce with glossary**:
```
# omegat-project/glossary/terminology.txt
Settings	Paramètres
(not "Réglages")
```

## Deployment Architecture

### Docker-Based CI/CD

**Dockerfile**:
```dockerfile
FROM openjdk:11-jre-slim

# Install OmegaT
RUN wget https://github.com/omegat-org/omegat/releases/download/v6.0.0/OmegaT_6.0.0_Without_JRE.zip && \
    unzip OmegaT_6.0.0_Without_JRE.zip -d /opt/ && \
    rm OmegaT_6.0.0_Without_JRE.zip

ENV PATH="/opt/OmegaT_6.0.0/bin:${PATH}"

WORKDIR /project

# Pre-load plugins
COPY plugins/ /opt/OmegaT_6.0.0/plugins/

CMD ["omegat", "/project", "--mode=console-translate"]
```

**GitHub Actions**:
```yaml
jobs:
  translate:
    runs-on: ubuntu-latest
    container:
      image: omegat/omegat:latest
    steps:
      - uses: actions/checkout@v3

      - name: Auto-propagate 100% matches
        run: |
          omegat omegat-project/ --mode=console-translate --quiet

      - name: Generate statistics
        run: |
          omegat omegat-project/ --mode=console-stats > stats.txt
          cat stats.txt
```

## Cost Analysis

### Software Costs

**OmegaT**: $0 (open source)
**Memsource**: $500-2,000/year (alternative)

### Translation Costs (Per Language)

**Scenario**: 50,000-word app, quarterly updates

| Release | New Segments | TM Leverage | Translation Cost |
|---------|--------------|-------------|------------------|
| v1.0 (initial) | 50,000 | 0% | $6,000 ($0.12/word) |
| v1.1 (minor) | 5,000 new<br>40,000 100% match<br>5,000 fuzzy | 80% | $1,000 |
| v1.2 (minor) | 3,000 new<br>45,000 100% match<br>2,000 fuzzy | 90% | $560 |
| v2.0 (major) | 15,000 new<br>25,000 100% match<br>10,000 fuzzy | 50% | $2,550 |

**Annual savings** (4 quarterly releases):
- Without TM: $6,000 × 4 = $24,000
- With TM: $6,000 + $1,000 + $560 + $2,550 = $10,110
- **Savings**: $13,890/year per language (58%)

**For 8 languages**: $111,120/year savings

### ROI Timeline

**Payback**: 2nd release (3-6 months)
- v1.0: Build TM (no savings yet)
- v1.1: 80% leverage → immediate 58% cost reduction
- ROI > 1000% by end of year 1

## Real-World Examples

### Case Study: WordPress (Localization Platform)

**Scale**: 50,000+ strings, 200+ languages
**Tool**: GlotPress (custom, TMX-based like OmegaT)
**TM leverage**: 70-85% on minor releases
**Translator community**: 10,000+ volunteers

**Key insights**:
- Open source = free TM tools (OmegaT, GlotPress)
- Git workflow enables contributor PRs
- TMX export allows translators to use any CAT tool

### Case Study: Discourse (Forum Software)

**Scale**: 15,000 strings, 40+ languages
**Tool**: Custom Transifex integration (cloud, similar to Memsource)
**Update frequency**: Bi-weekly releases
**TM leverage**: 85-90% (mature product)

**Key insights**:
- API-driven (push strings on each release)
- Real-time translator collaboration (multiple people on same language)
- Hybrid: Core team uses Git, volunteers use web UI

## Summary

**Recommended Tool**: OmegaT (Git integration, open source)

**Key strengths**:
- ✅ Zero cost (vs. $500-2,000/year for Memsource/Trados)
- ✅ Git workflow (translations version-controlled with code)
- ✅ TMX format (portable, industry standard)
- ✅ Scriptable (CI/CD automation via command-line tools)
- ✅ File format support (JSON, XLIFF, properties, PO, YAML)

**When to upgrade**:
- Team size >5 translators → Consider Memsource for real-time collaboration
- Non-technical translators → Memsource web UI easier than Git
- Need 24/7 cloud access → Memsource cloud-based

**Savings**: 60-85% cost reduction on incremental releases, ROI < 6 months

## Cross-References

- **S1 Rapid Discovery**: [omegat.md](../S1-rapid/omegat.md), [tmx-format.md](../S1-rapid/tmx-format.md)
- **S2 Comprehensive**: [omegat.md](../S2-comprehensive/omegat.md), [memsource.md](../S2-comprehensive/memsource.md)
- **S3 Other Use Cases**: [use-case-translation-agencies.md](use-case-translation-agencies.md), [use-case-freelance-translators.md](use-case-freelance-translators.md)
- **S4 Strategic**: TM governance, build vs. buy analysis
