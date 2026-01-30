# Continuous Localization and CI/CD Integration

## What is Continuous Localization?

**Definition:** Automated localization integrated with CI/CD processes, ensuring every code update triggers immediate translation tasks.

**Goal:** Eliminate delays between development and localization. Global releases happen simultaneously.

**Source:** [Continuous Localization: Key Concepts and Best Practices – Accelingo](https://www.accelingo.com/continuous-localization/)

## Traditional vs. Continuous Localization

| Traditional | Continuous |
|-------------|------------|
| Translate after development complete | Translate as development happens |
| Manual file handoffs | Automated extraction/delivery |
| Weeks/months for localized release | Hours/days for localized release |
| Waterfall process | Agile/CI-CD integrated |

## How It Works

### Step 1: Developer Pushes Code

```bash
# Developer commits new strings
git add src/locales/en-US.json
git commit -m "Add new feature strings"
git push origin main
```

### Step 2: CI/CD Detects Changes

**GitHub Actions Example:**

```yaml
name: Continuous Localization

on:
  push:
    paths:
      - 'src/locales/en-US.json'

jobs:
  extract-and-upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Extract strings to XLIFF
        run: |
          npm run extract-xliff

      - name: Upload to TMS
        run: |
          curl -X POST https://tms.example.com/api/upload \
            -H "Authorization: Bearer ${{ secrets.TMS_TOKEN }}" \
            -F "file=@locales/strings.xliff"
```

**Source:** [How to continuously localize using GitHub Actions - Lokalise](https://lokalise.com/blog/how-to-continuously-localize-your-front-end-resource-files-using-github-actions/)

### Step 3: TMS Notifies Translators

**Automatic Workflow:**
1. TMS receives XLIFF file
2. Checks TM for existing translations
3. Sends new/changed segments to MT or translator
4. Translator receives notification

**Source:** [Streamline Your Workflow with AI-Driven Continuous Localization - Transifex](https://www.transifex.com/blog/2024/ai-continuous-localization)

### Step 4: Translations Pushed Back

**Automatic Merge:**

```yaml
name: Import Translations

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  import-translations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Download from TMS
        run: |
          curl https://tms.example.com/api/download \
            -H "Authorization: Bearer ${{ secrets.TMS_TOKEN }}" \
            -o locales/strings_fr-FR.xliff

      - name: Merge XLIFF into resources
        run: |
          npm run merge-xliff

      - name: Commit and push
        run: |
          git config user.name "Localization Bot"
          git config user.email "bot@example.com"
          git add src/locales/
          git commit -m "chore: update translations"
          git push
```

## XLIFF in CI/CD

### Automatic XLIFF Generation (.NET Example)

**MSBuild Integration:**

```xml
<Project>
  <PropertyGroup>
    <!-- Update XLIFF files automatically on build -->
    <UpdateXlfOnBuild>true</UpdateXlfOnBuild>
  </PropertyGroup>
</Project>
```

**Behavior:**
- Developer builds project locally
- XLIFF files auto-update with new strings
- Developer commits updated XLIFF files
- CI build **fails** if XLIFF changes not committed (keeps files in sync)

**Source:** [GitHub - dotnet/xliff-tasks](https://github.com/dotnet/xliff-tasks)

**Best Practice:**
- `UpdateXlfOnBuild=true` for local builds
- `UpdateXlfOnBuild=false` for CI (enforces commit discipline)

### Git Workflow

```
main
 ├─ feature/new-strings
 │   ├─ Add new strings to en-US.json
 │   ├─ npm run extract-xliff (generates strings.xliff)
 │   ├─ Commit both en-US.json and strings.xliff
 │   └─ Push to GitHub
 │
 ├─ CI detects changes to strings.xliff
 ├─ Uploads to TMS
 │
 ├─ Translator completes translation
 ├─ TMS creates PR with updated fr-FR.xliff
 │
 └─ Merge PR → Localized release
```

## Platforms Supporting Continuous Localization

### Transifex

**Features:**
- GitHub/GitLab/Bitbucket integration
- Automatic string detection
- Live preview for translators
- AI translation + human review

**Source:** [Streamline Your Workflow with AI-Driven Continuous Localization - Transifex](https://www.transifex.com/blog/2024/ai-continuous-localization)

### Lokalise

**Features:**
- CLI for automation
- GitHub Actions integration
- Webhook notifications
- OTA (Over-The-Air) delivery for mobile

**Source:** [Automate Your Localization Workflows with Lokalise](https://lokalise.com/product/localization-workflow-management/)

### Smartcat/Phrase

Both support API-driven continuous localization with CI/CD integration.

### SimpleLocalize

**Features:**
- Lightweight CLI
- CI/CD integration examples
- Open-source friendly

**Source:** [CI/CD integration | SimpleLocalize](https://simplelocalize.io/docs/cli/ci-cd-integration/)

## Implementation Patterns

### Pattern 1: Fully Automated

```
Code Change → Auto-Extract → Auto-Translate (MT) → Auto-Merge → Deploy
```

**Use Case:** High-velocity products where speed > perfection (internal tools, support docs)

### Pattern 2: Human-in-Loop

```
Code Change → Auto-Extract → Human Translate → Manual Review → Auto-Merge → Deploy
```

**Use Case:** Customer-facing products where quality critical

### Pattern 3: Hybrid

```
Code Change → Auto-Extract → TM Check:
  ├─ 100% match → Auto-Merge
  ├─ 80-99% match → Human Review → Auto-Merge
  └─ <80% match → MT → Human Post-Edit → Auto-Merge → Deploy
```

**Use Case:** Balance speed and quality (most common in 2026)

## Monitoring and Metrics

**Key Metrics:**
- **Time from code change to translated:** Hours (vs. weeks in traditional)
- **TM match rate:** % of segments matched from TM
- **Post-edit distance:** How much MT output is edited
- **Translation velocity:** Segments per day

**Dashboards:**
- TMS platforms provide analytics
- Track coverage % by language
- Monitor translator workload

## Challenges

### 1. Context Loss

**Problem:** Translators see individual strings, not full UI

**Solution:**
- Provide screenshots in XLIFF `<note>` elements
- Live preview environments
- Context comments in source code → extracted to XLIFF

### 2. String Freeze Discipline

**Problem:** Continuous changes frustrate translators

**Solution:**
- Feature flags for new strings (don't expose until translated)
- String freeze periods before major releases
- Communicate with localization team

### 3. Git Conflicts

**Problem:** Translation bot and developers editing same files

**Solution:**
- Separate branches for translation updates
- Merge bot changes during off-peak hours
- Use XLIFF (separate from source code files)

## Best Practices

1. **Use XLIFF:** Separates translatable content from code
2. **Automate Extract/Merge:** Don't rely on manual file uploads
3. **Leverage TM:** Maximize reuse, minimize translation cost
4. **Integrate MT:** For speed, with human review for quality
5. **Monitor Metrics:** Track time-to-localization, match rates
6. **Communicate:** Keep translators informed of release schedule

## Example: Full GitHub Actions Workflow

```yaml
name: Continuous Localization

on:
  push:
    branches: [main]
    paths:
      - 'src/locales/**'

jobs:
  sync-to-tms:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install CLI
        run: npm install -g @lokalise/cli

      - name: Push strings to Lokalise
        run: |
          lokalise2 file upload \
            --token=${{ secrets.LOKALISE_TOKEN }} \
            --project-id=${{ secrets.LOKALISE_PROJECT }} \
            --file=src/locales/en-US.json \
            --lang-iso=en

  pull-translations:
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule'
    steps:
      - uses: actions/checkout@v2

      - name: Download translations
        run: |
          lokalise2 file download \
            --token=${{ secrets.LOKALISE_TOKEN }} \
            --project-id=${{ secrets.LOKALISE_PROJECT }} \
            --format=json \
            --dest=src/locales/

      - name: Create PR
        uses: peter-evans/create-pull-request@v4
        with:
          commit-message: "chore: update translations"
          title: "Update translations from Lokalise"
          branch: "translations-update"
```

## Sources

- [How to continuously localize using GitHub Actions - Lokalise](https://lokalise.com/blog/how-to-continuously-localize-your-front-end-resource-files-using-github-actions/)
- [Continuous Localization: Key Concepts and Best Practices – Accelingo](https://www.accelingo.com/continuous-localization/)
- [Streamline Your Workflow with AI-Driven Continuous Localization - Transifex](https://www.transifex.com/blog/2024/ai-continuous-localization)
- [GitHub - dotnet/xliff-tasks](https://github.com/dotnet/xliff-tasks)
- [Continuous localization: the missing step in CI/CD workflows - RWS](https://www.rws.com/blog/continuous-localization-missing-step/)
- [Continuous localization and translation 101 - Lokalise](https://lokalise.com/blog/continuous-localization-101/)
- [Automate Your Localization Workflows with Lokalise](https://lokalise.com/product/localization-workflow-management/)
- [CI/CD integration | SimpleLocalize](https://simplelocalize.io/docs/cli/ci-cd-integration/)
