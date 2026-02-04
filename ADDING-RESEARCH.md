# Adding New Research: Complete Guide

**Target audience**: New contributors, polecats, and anyone adding research to Survey of Software.

**Outcome**: You can add complete, validated research from scratch without help.

---

## Table of Contents

1. [Quick Start (Happy Path)](#quick-start-happy-path)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Workflow](#step-by-step-workflow)
4. [Validation](#validation)
5. [Common Failure Modes](#common-failure-modes)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [Testing Locally](#testing-locally)
8. [Automation Scripts](#automation-scripts)
9. [Complete vs Incomplete Examples](#complete-vs-incomplete-examples)
10. [Polecat Workflow](#polecat-workflow)
11. [Checklist Template](#checklist-template)

---

## Quick Start (Happy Path)

**For the impatient**: One-command workflow using automation:

```bash
# 1. Navigate to crew/ivan
cd ~/gt/research/crew/ivan

# 2. Create your research following 4PS methodology
# (See "Step-by-Step Workflow" below for details)

# 3. Run complete workflow (validates, commits, pushes, creates PR, closes bead)
python3 scripts/research_lifecycle.py complete 1.XXX research-BEAD-ID \
  --message "Complete research on <topic>"

# Done! PR created, ready for review and merge.
```

**For everyone else**: Read on for the full workflow and understanding.

---

## Prerequisites

### Required Knowledge

1. **4PS Methodology** - Read `docs/about.md` section "The Four-Pass Discovery Framework"
   - S1 (Rapid): WHAT tools/libraries exist? Library comparison for decisions.
   - S2 (Comprehensive): HOW do they work? Technical deep-dive.
   - S3 (Need-Driven): WHO needs this + WHY? Use cases and personas.
   - S4 (Strategic): WHICH to choose? Long-term viability and trade-offs.

2. **Scope** - Research LIBRARIES (pip/npm installable), NOT applications
   - ✅ Good: pandas, transformers, lodash, jieba
   - ❌ Bad: OmegaT, Photoshop, language learning apps
   - **Test**: Does a developer `import` or `require` this in code? If NO → out of scope.

3. **Templates**
   - `4PS_ORDER_TEMPLATE.md` - Bead description template with requirements
   - `DOMAIN_EXPLAINER_TEMPLATE.md` - Universal analogies template

### Required Tools

```bash
# Check you have the tools installed
python3 --version  # Python 3.x
node --version     # Node.js (for testing build)
git --version      # Git

# Check you're in the right directory
pwd
# Should output: /home/ivanadamin/gt/research/crew/ivan
```

---

## Step-by-Step Workflow

### Step 0: Verify Workspace (MANDATORY)

**Why**: Working in the wrong directory causes files to be created in the wrong location.

```bash
# Run this FIRST
pwd

# Expected output: /home/ivanadamin/gt/research/crew/ivan
# If wrong, navigate there:
cd ~/gt/research/crew/ivan
pwd  # Verify again
```

### Step 1: Create Feature Branch

**Why**: All research uses PR workflow for review and CI validation.

```bash
# Branch naming: research/1.xxx-topic-name
git checkout -b research/1.116-data-viz-libraries

# Verify you're on the new branch
git branch --show-current
# Should show: research/1.116-data-viz-libraries
```

### Step 2: Create Research Structure

**Directory structure** (REQUIRED):

```
packages/research/1.116-data-viz-libraries/
├── DOMAIN_EXPLAINER.md              # Universal analogies (see template)
├── metadata.yaml                    # Research metadata (see Step 6)
└── 01-discovery/
    ├── DISCOVERY_TOC.md             # Optional: Table of contents
    ├── S1-rapid/
    │   ├── approach.md              # How S1 was executed
    │   ├── library1.md              # Per-library comparison (NOT tutorial!)
    │   ├── library2.md
    │   └── recommendation.md        # S1 verdict: which libraries to explore
    ├── S2-comprehensive/
    │   ├── approach.md
    │   ├── library1.md              # Technical deep-dive per library
    │   ├── library2.md
    │   ├── feature-comparison.md    # Optional: Feature matrix
    │   └── recommendation.md        # S2 verdict: how they differ
    ├── S3-need-driven/
    │   ├── approach.md
    │   ├── use-case-persona1.md     # WHO + WHY (NOT how to implement!)
    │   ├── use-case-persona2.md
    │   ├── use-case-persona3.md     # Minimum 3 use cases
    │   └── recommendation.md        # S3 verdict: who should use what
    └── S4-strategic/
        ├── approach.md
        ├── library1-viability.md    # Long-term viability analysis
        ├── library2-viability.md
        └── recommendation.md        # S4 verdict: strategic paths
```

**Create directories**:

```bash
CODE="1.116-data-viz-libraries"
mkdir -p packages/research/$CODE/01-discovery/{S1-rapid,S2-comprehensive,S3-need-driven,S4-strategic}
```

### Step 3: Write S1 (Rapid Discovery)

**Goal**: WHAT tools exist? Library comparison for decision-making.

**Critical requirements**:
- ✅ Features, speed, maturity, ecosystem stats, trade-offs
- ✅ "Library X: 10K stars, F1 95%, best for domain Y"
- ❌ FORBIDDEN: Installation guides (`pip install`, `npm install`)
- ❌ FORBIDDEN: Code samples (import statements, usage examples)
- ❌ FORBIDDEN: "How to use" tutorials
- ❌ FORBIDDEN: Method explanations ("Research Method", "S1 Distinguishing Characteristics")

**Think**: "WHICH library?" not "HOW to install?" - S1 is a shopping comparison, not a manual.

**Files to create**:
1. `S1-rapid/approach.md` - How you executed S1 (sources, criteria)
2. `S1-rapid/<library>.md` - One file per library (comparison data)
3. `S1-rapid/recommendation.md` - Which libraries merit S2 exploration

### Step 4: Write S2 (Comprehensive Discovery)

**Goal**: HOW do libraries work? Technical deep-dive.

**Allowed**:
- ✅ Architecture, algorithms, performance benchmarks
- ✅ API design patterns
- ✅ Minimal code samples showing API patterns (illustrative only)

**Forbidden**:
- ❌ Method preambles explaining what S2 is
- ❌ Installation tutorials

**Files to create**:
1. `S2-comprehensive/approach.md`
2. `S2-comprehensive/<library>.md` - Technical analysis per library
3. `S2-comprehensive/feature-comparison.md` - Optional feature matrix
4. `S2-comprehensive/recommendation.md` - How libraries differ technically

### Step 5: Write S3 (Need-Driven Discovery)

**Goal**: WHO needs this + WHY? (NOT how to implement!)

**MOST COMMON MISTAKE**: Focusing on implementation instead of personas.

**Critical requirements**:
- ✅ Each file MUST start with "## Who Needs This" or "## User Persona"
- ✅ Files named: `use-case-<persona>.md` (e.g., `use-case-freelance-translators.md`)
- ✅ Minimum 3 use cases, ideally 4-5
- ❌ FORBIDDEN: `implementation-*.md` files
- ❌ FORBIDDEN: Code examples, CI/CD workflows
- ❌ FORBIDDEN: "How to implement X" content

**Example GOOD S3**:
```markdown
## Who Needs This
Freelance medical translators building a career-long translation memory.

## Why They Need It
Medical terminology is highly specialized and consistent. Reusing translations
ensures accuracy and speeds up work. A personal TM is a competitive advantage.

## Requirements
- Import/export TMX format (portability)
- Fuzzy matching (find similar segments)
- Terminology management (glossaries)
```

**Example BAD S3**:
```markdown
## How to Implement Continuous Localization

1. Set up GitHub Actions workflow
2. Install translation SDK
3. Configure API keys
```

**Files to create**:
1. `S3-need-driven/approach.md`
2. `S3-need-driven/use-case-<persona>.md` (3-5 files)
3. `S3-need-driven/recommendation.md` - Who should use what

### Step 6: Write S4 (Strategic Discovery)

**Goal**: WHICH to choose? Long-term viability and trade-offs.

**Focus**:
- Long-term viability (5-10 years)
- Ecosystem trends
- Organizational risk tolerance
- Strategic paths (Conservative, Performance-First, Adaptive)

**Files to create**:
1. `S4-strategic/approach.md`
2. `S4-strategic/<library>-viability.md` - Per-library viability analysis
3. `S4-strategic/recommendation.md` - Strategic paths and trade-offs

### Step 7: Write DOMAIN_EXPLAINER.md

**Goal**: Explain the domain using universal analogies (hardware store test).

**See**: `DOMAIN_EXPLAINER_TEMPLATE.md` for structure.

**Example**:
```markdown
# What is Data Visualization?

If software libraries were tools in a hardware store, data visualization libraries
would be in the "Display & Presentation" aisle - tools for showing information
visually.

## The Problem

You have data (numbers, measurements, events) but humans struggle to understand
long lists of numbers. A chart or graph makes patterns obvious.

## The Solution

Data visualization libraries convert raw data into charts, graphs, maps, and
interactive dashboards. Like how a hammer makes nails easier to drive, these
libraries make data easier to understand.
```

### Step 8: Write metadata.yaml

**Goal**: Provide structured metadata for automation and discovery.

**Template** (see `packages/research/1.007-pattern-matching/metadata.yaml` for complete example):

```yaml
code: '1.116'
title: Data Visualization Libraries
subtitle: "d3.js, matplotlib, plotly, chart.js, bokeh"  # 3-8 key libraries
tier: 1
category: Library/Package Discovery
domain: data-visualization
status: completed
completion_date: '2026-02-03'

description: |
  Comprehensive analysis of data visualization libraries across web and Python
  ecosystems. Covers charting, interactive dashboards, and custom visualizations.

research_output:
  total_documents: 25
  total_lines: 5000
  stages_completed: [S1-rapid, S2-comprehensive, S3-need-driven, S4-strategic]

libraries_analyzed:
  - name: d3.js
    implementation: DOM manipulation + SVG
    performance: Client-side, scales to 100K points
    best_for: Custom interactive visualizations

  - name: matplotlib
    implementation: Python plotting, MATLAB-like
    performance: 1M points reasonable
    best_for: Scientific publications, static plots

key_findings:
  - finding: "d3.js provides maximum flexibility but steeper learning curve"
    impact: "Custom visualizations possible, but 10x development time vs chart.js"

  - finding: "Plotly enables interactive dashboards with minimal code"
    impact: "80% of use cases covered with 20% of d3.js effort"

recommendations:
  default: "Use Plotly for dashboards, matplotlib for scientific papers"

  by_use_case:
    scientific_papers: "matplotlib - publication quality, LaTeX integration"
    business_dashboards: "Plotly or Tableau - interactive, low code"
    custom_viz: "d3.js - full control, high effort"

sources:
  academic_papers:
    - "Citation for relevant research"

  libraries:
    - "d3.js documentation"
    - "matplotlib documentation"

  production_systems:
    - "Company X uses library Y for use case Z"
```

**Required fields**:
- `code`, `title`, `subtitle`
- `tier`, `category`, `domain`
- `status`, `completion_date`
- `description`
- `sources` (must include actual sources with URLs/citations)
- `libraries_analyzed` (or `libraries_evaluated`)
- `key_findings`
- `recommendations`

**Validation scoring**:
- Complete metadata.yaml: 30 points
- All required fields: 30 points
- Optional fields (related_research, etc.): bonus points

### Step 9: Validate Research

**CRITICAL**: Validation must pass before committing, creating PR, or closing bead.

```bash
# Run validation (replace 1.116 with your code)
python3 scripts/validate_research.py 1.116
```

**Expected output**:
```
Research Validation Report: 1.116
============================================================
Overall Score: 96% - EXCELLENT

Structure Validation: 100/100
  ✓ S1-rapid directory exists
  ✓ S2-comprehensive directory exists
  ✓ S3-need-driven directory exists
  ✓ S4-strategic directory exists
  ✓ DOMAIN_EXPLAINER.md exists
  ✓ metadata.yaml exists

Content Quality: 45/50
  ✓ metadata.yaml is complete (30/30)
  ✓ File sizes meet thresholds (15/20)

============================================================
Status: EXCELLENT (90%+) - Ready to commit!
```

**Score thresholds**:
- **< 75%**: ❌ FAIL - Cannot commit/close bead (fix issues first)
- **75-89%**: ⚠️ ACCEPTABLE - Can commit but document missing components
- **90%+**: ✅ EXCELLENT - Ideal score

**If validation fails**: See [Common Failure Modes](#common-failure-modes) and [Troubleshooting Guide](#troubleshooting-guide).

### Step 10: Test Local Build

**Why**: Catch conversion and MDX syntax errors before pushing.

```bash
# Convert research to Docusaurus MDX
python3 scripts/convert_research.py

# Check conversion succeeded
ls -lh docs/survey/1-116.md
# Should show file size > 50KB for comprehensive research

# Quick check for placeholder content (bad)
grep -c "^# S1-rapid$" docs/survey/1-116.md
# Should output: 0 (no placeholder headers)

# Optional: Build the site locally
npm run build

# If build succeeds, your research is ready
```

**Common build errors**:
- MDX syntax errors (unescaped `{`, `<`, `>`)
- Invalid frontmatter
- Broken internal links

See [Troubleshooting Guide](#troubleshooting-guide) for fixes.

### Step 11: Commit to Feature Branch

```bash
# Stage research files
git add packages/research/1.116-*

# Commit with validation score in message
git commit -m "research: Complete 1.116 Data Visualization Libraries (96% score)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Pre-commit hook will run validation
# If it fails, fix issues and try again
```

**Pre-commit hook behavior**:
- Validates all staged research in `packages/research/`
- Blocks commit if score < 75%
- Warns if score 75-89%
- Passes if score 90%+

**To bypass hook** (not recommended):
```bash
git commit --no-verify -m "bypass validation (emergency only)"
```

### Step 12: Push Branch

```bash
git push -u origin research/1.116-data-viz-libraries
```

### Step 13: Create Pull Request

**Option A: Using gh CLI** (recommended):

```bash
gh pr create --title "Research 1.116: Data Visualization Libraries" --body "$(cat <<'EOF'
## Research Details
- **Code**: 1.116
- **Topic**: Data Visualization Libraries
- **Validation Score**: 96% (EXCELLENT)
- **Methodology**: 4PS (S1-S4 complete)

## Structure
- ✅ DOMAIN_EXPLAINER.md (8KB)
- ✅ S1: Rapid Discovery (6 files)
- ✅ S2: Comprehensive Discovery (7 files)
- ✅ S3: Need-Driven Discovery (5 use cases)
- ✅ S4: Strategic Discovery (4 files)
- ✅ metadata.yaml with complete sourcing

## Validation Results
\`\`\`
$ python3 scripts/validate_research.py 1.116

Research Validation Report: 1.116
============================================================
Overall Score: 96% - EXCELLENT

Structure Validation: 100/100
Content Quality: 45/50
\`\`\`

## Review Checklist
- [ ] Research follows 4PS methodology
- [ ] Validation score ≥ 75%
- [ ] Metadata includes proper sources
- [ ] Content is hardware-store appropriate
- [ ] No sensitive/private information

🤖 Created by Polecat / Contributor
EOF
)"
```

**Option B: Using GitHub UI**:
1. Go to your GitHub repository
2. Click "Compare & pull request" button
3. Fill in title and description (use template above)
4. Create pull request

### Step 14: Wait for CI Validation

**What happens automatically**:
1. CI extracts research codes from PR files
2. Runs `validate_research.py` for each code
3. Comments validation results on PR
4. Blocks PR merge if any research < 75%

**Example CI comment**:
```
## ✅ Research Validation Passed

- **1.116**: 96% - ✅ EXCELLENT

All research meets quality standards (75%+).
```

**If CI fails**: See [Troubleshooting Guide](#troubleshooting-guide).

### Step 15: Human Review

**Reviewer checks**:
- Content accuracy and completeness
- 4PS methodology followed correctly
- Sources properly cited
- No problematic content

**As contributor**: Respond to review feedback, make requested changes:

```bash
# Make changes
vim packages/research/1.116-*/...

# Validate again
python3 scripts/validate_research.py 1.116

# Commit and push
git add packages/research/1.116-*
git commit -m "fix: Address review feedback"
git push

# CI will re-run automatically
```

### Step 16: PR Merged (Human Action)

**DO NOT merge your own PR** - human reviewer will merge after approval.

**What happens on merge** (automatic):
1. CI detects new research in `packages/research/`
2. Runs `convert_research.py` → generates `docs/survey/1-116.md`
3. Runs `integrate_research.py` → updates `docs/survey/index.md` and `sidebars.ts`
4. Commits integration changes to main
5. Triggers deployment to GitHub Pages
6. Research live on site in ~5 minutes

**CI commit message**:
```
docs: Auto-integrate research 1.116

Automated conversion and integration:
- Converted packages/research/ to docs/survey/
- Updated survey index with new entries
- Updated sidebar navigation

Research codes: 1.116

Co-Authored-By: github-actions[bot]
```

### Step 17: Close Bead (If Using Beads)

**Only after PR is created** (not after merge):

```bash
bd update research-XYZ --status=closed
```

**Note**: Beads are closed when work is done (PR created), not when it's merged. The human reviewer merges the PR.

---

## Validation

### Running Validation

```bash
# Basic validation
python3 scripts/validate_research.py 1.116

# Validate multiple research codes
python3 scripts/validate_research.py 1.001 1.002 1.003

# Validate all research in directory
for dir in packages/research/*/; do
  code=$(basename "$dir" | cut -d'-' -f1)
  python3 scripts/validate_research.py "$code"
done
```

### Understanding Validation Scores

**Structure (100 points)**:
- S1-S4 directories exist (25 points each = 100)
- Required files per phase (approach, libraries, recommendation)
- DOMAIN_EXPLAINER.md exists
- metadata.yaml exists

**Content Quality (50 points)**:
- metadata.yaml completeness (30 points)
  - All required fields present
  - Sources properly documented
- File size thresholds (20 points)
  - DOMAIN_EXPLAINER.md > 500 bytes
  - Each S phase has reasonable content

**Total**: 150 points → percentage score

### Score Interpretation

| Score | Status | Can Commit? | Can Close Bead? | Action |
|-------|--------|-------------|-----------------|--------|
| < 75% | ❌ FAIL | No | No | Fix issues first |
| 75-89% | ⚠️ ACCEPTABLE | Yes (with warning) | Yes (document gaps) | Consider improving |
| 90%+ | ✅ EXCELLENT | Yes | Yes | Ideal quality |

---

## Common Failure Modes

### 1. Missing metadata.yaml (Most Common)

**Symptom**: Validation score 83% (100 structure + 25 content)

**Cause**: Forgot to create `metadata.yaml`

**Fix**:
```bash
# Create metadata.yaml using template
CODE="1.116"
cat > packages/research/$CODE/metadata.yaml <<'EOF'
code: '1.116'
title: Data Visualization Libraries
subtitle: "d3.js, matplotlib, plotly"
# ... (see Step 8 for complete template)
EOF

# Re-validate
python3 scripts/validate_research.py $CODE
```

**Prevention**: Add metadata.yaml to checklist (see [Checklist Template](#checklist-template))

### 2. Incomplete metadata.yaml

**Symptom**: Validation score 93% (100 structure + 40 content)

**Cause**: Missing required fields in metadata.yaml (often `domain` or `sources`)

**Fix**:
```bash
# Check what's missing
python3 scripts/validate_research.py 1.116 | grep metadata

# Add missing fields
vim packages/research/1.116-*/metadata.yaml

# Re-validate
python3 scripts/validate_research.py 1.116
```

**Common missing fields**:
- `domain` - e.g., "data-visualization", "string-algorithms"
- `sources` - Must include actual URLs/citations
- `libraries_analyzed` - Must list libraries with details
- `key_findings` - Must include meaningful findings

### 3. S3 Files Are Implementation Guides

**Symptom**: S3 files named `implementation-*.md` or contain "How to implement X"

**Cause**: Misunderstanding S3 purpose (WHO + WHY, not HOW)

**Fix**:
```bash
# Rename files
cd packages/research/1.116-*/01-discovery/S3-need-driven/
mv implementation-ci-cd.md use-case-devops-teams.md

# Rewrite content to focus on WHO + WHY
vim use-case-devops-teams.md
```

**Rewrite example**:

**Before** (wrong):
```markdown
## How to Implement Continuous Localization

1. Set up GitHub Actions
2. Install translation SDK
3. Configure API keys
```

**After** (correct):
```markdown
## Who Needs This
DevOps teams managing multi-language products with frequent releases.

## Why They Need It
Manual translation creates bottlenecks. Every release waits for translators.
Continuous localization automates translation in the CI/CD pipeline, enabling
daily releases in 20+ languages.

## Requirements
- API-based translation (integrate with CI/CD)
- Translation memory (avoid re-translating)
- Quality thresholds (block releases if quality drops)
```

### 4. S1 Contains Installation Tutorials

**Symptom**: S1 files have "pip install" or code examples

**Cause**: Misunderstanding S1 purpose (decision guide, not tutorial)

**Fix**:
```bash
# Edit S1 files to remove installation/code
vim packages/research/1.116-*/01-discovery/S1-rapid/*.md
```

**Remove**:
- `pip install <library>`
- `npm install <library>`
- Import statements (`from X import Y`)
- Code usage examples
- "How to use" tutorials

**Keep**:
- Features ("supports 50+ chart types")
- Performance ("renders 1M points in 200ms")
- Maturity ("10K stars, 5 years old, active maintenance")
- Ecosystem ("works with React, Vue, Angular")
- Trade-offs ("faster but less flexible than d3.js")

### 5. Working in Wrong Directory

**Symptom**: Files created but validation can't find them

**Cause**: `pwd` shows wrong directory (e.g., `/home/ivanadamin/gt/research` instead of `/home/ivanadamin/gt/research/crew/ivan`)

**Fix**:
```bash
# Navigate to correct directory
cd ~/gt/research/crew/ivan

# Verify
pwd
# Should show: /home/ivanadamin/gt/research/crew/ivan

# Move misplaced files if needed
mv ~/gt/research/packages/research/1.116-* ~/gt/research/crew/ivan/packages/research/
```

**Prevention**: Always run `pwd` as Step 0 (see workflow above)

### 6. Placeholder Content in Converted Doc

**Symptom**: `docs/survey/1-116.md` contains "# S1-rapid" or "# S2-comprehensive" headers

**Cause**: `approach.md` or `recommendation.md` files are empty or contain only headers

**Fix**:
```bash
# Find placeholder headers
grep "^# S[1-4]-" docs/survey/1-116.md

# Edit source files to add content
vim packages/research/1.116-*/01-discovery/S1-rapid/approach.md

# Re-convert
python3 scripts/convert_research.py

# Verify placeholders are gone
grep "^# S[1-4]-" docs/survey/1-116.md
# Should return nothing
```

### 7. Pre-Commit Hook Blocks Commit

**Symptom**: `git commit` fails with validation error

**Cause**: Research score < 75%

**Fix**:
```bash
# Check what's wrong
python3 scripts/validate_research.py 1.116

# Fix issues (see failure modes above)
# ...

# Stage fixes
git add packages/research/1.116-*

# Try commit again
git commit -m "research: Complete 1.116 (96% score)"
```

**Emergency bypass** (not recommended):
```bash
git commit --no-verify -m "bypass validation"
```

### 8. CI Validation Fails on PR

**Symptom**: PR shows red X, CI comments "Research validation failed"

**Cause**: Research passed local validation but fails in CI (rare)

**Possible reasons**:
- Pushed before validating
- Different Python version in CI
- File encoding issues

**Fix**:
```bash
# Validate locally first
python3 scripts/validate_research.py 1.116

# If local validation passes but CI fails, check CI logs
gh pr checks

# Make fixes
# ...

# Push again
git add packages/research/1.116-*
git commit -m "fix: Address CI validation issues"
git push
```

### 9. Build Fails with MDX Syntax Error

**Symptom**: `npm run build` fails with "Unexpected token" or similar

**Cause**: Unescaped MDX special characters in research content

**Common culprits**:
- `{` and `}` in prose (use `\{` and `\}`)
- `<` and `>` in comparisons (use `&lt;` and `&gt;`)
- Unescaped HTML tags

**Fix**:
```bash
# Use fix-mdx-brackets.py to auto-fix
python3 scripts/fix-mdx-brackets.py docs/survey/1-116.md

# Or manually edit
vim docs/survey/1-116.md

# Test build again
npm run build
```

### 10. Bead Closed Before PR Created

**Symptom**: Bead marked closed but PR not created yet

**Cause**: Confusion about when to close bead

**Correct timing**:
- Close bead AFTER creating PR
- NOT after PR is merged (human reviewer merges)

**Why**: Closing bead signals "my work is done (PR created and awaiting review)"

---

## Troubleshooting Guide

### Error: "Research code not found"

**Full error**:
```
Error: Research directory not found: packages/research/1.116-data-viz-libraries
```

**Causes**:
1. Wrong directory (`pwd` not `/home/ivanadamin/gt/research/crew/ivan`)
2. Typo in research code
3. Directory not created yet

**Fixes**:
```bash
# Fix 1: Navigate to correct directory
cd ~/gt/research/crew/ivan

# Fix 2: Check spelling
ls packages/research/ | grep 1.116

# Fix 3: Create directory if missing
mkdir -p packages/research/1.116-data-viz-libraries
```

### Error: "metadata.yaml: No such file"

**Full error**:
```
Warning: metadata.yaml not found
Content score: 25/50 (missing metadata)
Overall score: 83%
```

**Cause**: `metadata.yaml` not created

**Fix**:
```bash
CODE="1.116"
cat > packages/research/$CODE/metadata.yaml <<'EOF'
# See Step 8 for template
EOF
```

### Error: "S3 files missing 'Who Needs This' section"

**Full error**:
```
Warning: S3 file does not start with WHO section: use-case-*.md
```

**Cause**: S3 files don't follow required format

**Fix**:
```bash
# Edit S3 files to start with WHO section
for f in packages/research/1.116-*/01-discovery/S3-need-driven/use-case-*.md; do
  # Add WHO section at top if missing
  if ! grep -q "## Who" "$f"; then
    echo -e "## Who Needs This\n\n[Add persona description]\n\n$(cat $f)" > "$f"
  fi
done
```

### Error: "Build failed: Unexpected token {"

**Full error**:
```
Error: Unexpected token { in MDX
File: docs/survey/1-116.md:234
```

**Cause**: Unescaped `{` or `}` in text

**Fix**:
```bash
# Auto-fix with script
python3 scripts/fix-mdx-brackets.py docs/survey/1-116.md

# Or manually escape
vim docs/survey/1-116.md
# Find line 234, replace { with \{ and } with \}
```

### Error: "Pre-commit hook failed"

**Full error**:
```
🔍 Running pre-commit validation...
  → Validating research quality...
    ❌ Research 1.116 scored 65% (minimum: 75% required)

❌ Found 1 issue(s) that need to be fixed before committing.
```

**Cause**: Research quality < 75%

**Fix**:
```bash
# Check what's wrong
python3 scripts/validate_research.py 1.116

# Fix issues (see failure modes)
# ...

# Stage and commit again
git add packages/research/1.116-*
git commit -m "research: Complete 1.116 (96% score)"
```

### Error: "CI validation failed on PR"

**Full error** (in PR comment):
```
## ❌ Research Validation Failed

- **1.116**: 72% - ❌ FAIL (minimum: 75% required)

Research must score 75%+ to merge.
```

**Cause**: PR created before research was complete

**Fix**:
```bash
# Complete the research
# ...

# Validate
python3 scripts/validate_research.py 1.116

# Push update
git add packages/research/1.116-*
git commit -m "fix: Complete validation requirements (96% score)"
git push

# CI will re-run automatically
```

### Error: "Conversion generated empty file"

**Symptom**: `docs/survey/1-116.md` is 0 bytes or < 10KB

**Cause**: Missing content in source files

**Fix**:
```bash
# Check which files are empty
find packages/research/1.116-* -type f -size 0

# Add content to empty files
# ...

# Re-convert
python3 scripts/convert_research.py

# Check size
ls -lh docs/survey/1-116.md
# Should be > 50KB for comprehensive research
```

### Error: "GitHub API rate limit"

**Full error**:
```
gh: API rate limit exceeded
```

**Cause**: Too many GitHub API calls

**Fix**:
```bash
# Wait an hour, or use web UI to create PR
# Go to: https://github.com/<username>/<repo>/compare/research/1.116-data-viz-libraries
```

---

## Testing Locally

### Test 1: Validation

**What it tests**: Research structure and content quality

```bash
python3 scripts/validate_research.py 1.116

# Expected: 90%+ (EXCELLENT)
# Minimum: 75% (ACCEPTABLE)
```

### Test 2: Conversion

**What it tests**: 4PS → Docusaurus MDX conversion

```bash
python3 scripts/convert_research.py

# Check output
ls -lh docs/survey/1-116.md
# Should show size > 50KB

# Check for placeholders (should find none)
grep "^# S[1-4]-" docs/survey/1-116.md
# Should return nothing
```

### Test 3: Local Build

**What it tests**: MDX syntax, frontmatter, internal links

```bash
npm run build

# If successful, build/ directory created
ls -lh build/

# If failed, check error message (usually MDX syntax)
```

### Test 4: Local Development Server

**What it tests**: Full site with your research

```bash
npm start
# OR
sos launch 1

# Open browser: http://localhost:3000
# Navigate to your research in sidebar
```

**Check**:
- Research appears in sidebar
- Content renders correctly
- No broken links
- Images display (if any)
- Code blocks format correctly

### Test 5: S3 Format Validation

**What it tests**: S3 files follow WHO + WHY format (not HOW)

```bash
# Check all S3 files start with WHO section
for f in packages/research/1.116-*/01-discovery/S3-need-driven/use-case-*.md; do
  echo "Checking: $(basename $f)"
  head -5 "$f" | grep -E "(## Who|## User Persona)" || echo "  ❌ Missing WHO section"
done

# Should show ✓ for all files
```

### Test 6: S1 Tutorial-Free Check

**What it tests**: S1 has no installation guides or code examples

```bash
# Check for forbidden content
grep -r "pip install\|npm install\|import \|require(" \
  packages/research/1.116-*/01-discovery/S1-rapid/

# Should return nothing (no matches)
```

---

## Automation Scripts

All scripts located in `~/gt/research/crew/ivan/scripts/`

### research_lifecycle.py

**Purpose**: One-command workflow for research completion

**Usage**:
```bash
# Complete workflow: validate + commit + push + PR + close bead
python3 scripts/research_lifecycle.py complete 1.116 research-ABC \
  --message "Complete research on data visualization"

# Just validate
python3 scripts/research_lifecycle.py validate 1.116

# Just commit and push (skip validation - not recommended)
python3 scripts/research_lifecycle.py push 1.116 \
  --message "WIP: data viz research"

# Just close bead
python3 scripts/research_lifecycle.py close-bead research-ABC
```

**What `complete` does**:
1. Validates research (fails if < 75%)
2. Commits to current branch
3. Pushes to origin
4. Creates PR
5. Closes bead (if provided)

**Flags**:
- `--message, -m` - Commit message
- `--no-validate` - Skip validation (not recommended)
- `--no-pr` - Skip PR creation
- `--pr-title` - Custom PR title
- `--pr-body` - Custom PR body

### validate_research.py

**Purpose**: Validate research structure and content quality

**Usage**:
```bash
# Validate single research
python3 scripts/validate_research.py 1.116

# Validate multiple
python3 scripts/validate_research.py 1.001 1.002 1.003

# Verbose output
python3 scripts/validate_research.py 1.116 --verbose
```

**Output**:
- Structure validation (100 points)
- Content quality (50 points)
- Overall score (percentage)
- Specific missing components

### convert_research.py

**Purpose**: Convert 4PS research to Docusaurus MDX

**Usage**:
```bash
# Convert all research
python3 scripts/convert_research.py

# Convert specific codes (not directly supported, use filter below)

# Check conversion for specific research
python3 scripts/convert_research.py | grep "1-116"
```

**Output**:
- Generates `docs/survey/1-XXX.md` from `packages/research/1.XXX-*/`
- Flattens 4PS structure into single MDX file
- Adds frontmatter for Docusaurus
- Fixes common MDX issues

### integrate_research.py

**Purpose**: Update index and sidebar after conversion

**Usage**:
```bash
# Integrate all research
python3 scripts/integrate_research.py

# Updates:
# - docs/survey/index.md (research catalog)
# - sidebars.ts (navigation)
```

**Run after**: `convert_research.py`

### validate-and-commit.sh

**Purpose**: Streamlined validation + commit workflow

**Usage**:
```bash
# Validate and commit if score >= 75%
./scripts/validate-and-commit.sh 1.116 "Complete data viz research"

# Prompts for confirmation if score 75-89%
# Auto-commits if score 90%+
```

**Behavior**:
- Validates first
- Blocks if < 75%
- Interactive confirmation if 75-89%
- Auto-commit if 90%+

### install-hooks.sh

**Purpose**: Install pre-commit validation hook

**Usage**:
```bash
bash scripts/install-hooks.sh

# Installs .git/hooks/pre-commit
# Validates research on every commit
```

**What the hook does**:
- Runs on `git commit`
- Validates staged research files
- Blocks commit if score < 75%
- Can be bypassed with `git commit --no-verify`

### pre-commit-hook.sh

**Purpose**: Source for pre-commit hook (don't run directly)

**Location**: `scripts/pre-commit-hook.sh`

**Installed by**: `install-hooks.sh` → `.git/hooks/pre-commit`

### fix-mdx-brackets.py

**Purpose**: Auto-fix unescaped `{` and `}` in MDX files

**Usage**:
```bash
# Fix single file
python3 scripts/fix-mdx-brackets.py docs/survey/1-116.md

# Fix multiple files
python3 scripts/fix-mdx-brackets.py docs/survey/1-*.md
```

**What it fixes**:
- Unescaped `{` → `\{`
- Unescaped `}` → `\}`
- Preserves code blocks and frontmatter

---

## Complete vs Incomplete Examples

### Complete Example: 1.007 Pattern Matching

**Validation score**: 96% (EXCELLENT)

**Structure**:
```
packages/research/1.007-pattern-matching/
├── DOMAIN_EXPLAINER.md (18KB)
├── metadata.yaml (complete with sources, findings, recommendations)
└── 01-discovery/
    ├── DISCOVERY_TOC.md
    ├── S1-rapid/
    │   ├── approach.md
    │   ├── c-cpp-libraries.md
    │   ├── python-libraries.md
    │   ├── rust-go-libraries.md
    │   ├── java-jvm-libraries.md
    │   ├── specialized-libraries.md
    │   └── recommendation.md
    ├── S2-comprehensive/
    │   ├── approach.md
    │   ├── knuth-morris-pratt.md
    │   ├── boyer-moore.md
    │   ├── aho-corasick.md
    │   ├── rabin-karp.md
    │   ├── feature-comparison.md
    │   └── recommendation.md
    ├── S3-need-driven/
    │   ├── approach.md
    │   ├── text-editor-search.md     # WHO: editor users
    │   ├── network-ids.md            # WHO: security engineers
    │   ├── bioinformatics.md         # WHO: researchers
    │   ├── log-analysis.md           # WHO: DevOps
    │   └── recommendation.md
    └── S4-strategic/
        ├── approach.md
        ├── stdlib-viability.md
        ├── hyperscan-viability.md
        └── recommendation.md
```

**Why it's complete**:
- ✅ All S1-S4 phases present
- ✅ Each phase has approach + recommendation
- ✅ S1 focuses on library comparison (no installation guides)
- ✅ S3 files follow WHO + WHY format
- ✅ Complete metadata.yaml with sources
- ✅ DOMAIN_EXPLAINER.md with hardware store analogies
- ✅ Converted to 173KB Docusaurus doc

**Converted output**: `docs/survey/1-007.md` (173KB)

### Incomplete Example: Hypothetical 1.999

**Validation score**: 65% (FAIL)

**Structure**:
```
packages/research/1.999-incomplete/
├── DOMAIN_EXPLAINER.md (200 bytes - too short)
├── (missing metadata.yaml)
└── 01-discovery/
    ├── S1-rapid/
    │   ├── approach.md
    │   └── (missing library files)
    ├── S2-comprehensive/
    │   └── (empty directory)
    ├── S3-need-driven/
    │   ├── approach.md
    │   ├── implementation-ci-cd.md   # WRONG: should be use-case-*.md
    │   └── (missing recommendation.md)
    └── S4-strategic/
        └── (missing entirely)
```

**Why it fails**:
- ❌ Missing metadata.yaml (biggest issue)
- ❌ DOMAIN_EXPLAINER.md too short (< 500 bytes)
- ❌ S1 missing library files
- ❌ S2 empty (no content)
- ❌ S3 has implementation guide instead of WHO + WHY
- ❌ S3 missing recommendation.md
- ❌ S4 missing entirely

**Validation output**:
```
Research Validation Report: 1.999
============================================================
Overall Score: 65% - FAIL

Structure Validation: 40/100
  ✓ S1-rapid directory exists
  ✗ S1 missing library files
  ✓ S2-comprehensive directory exists
  ✗ S2 missing required files
  ✓ S3-need-driven directory exists
  ✗ S3 has wrong file format
  ✗ S4-strategic missing
  ✗ DOMAIN_EXPLAINER.md too short
  ✗ metadata.yaml missing

Content Quality: 0/50
  ✗ metadata.yaml not found

============================================================
Status: FAIL - Research incomplete. Fix issues before committing.
```

**How to fix**: Complete all missing phases, create metadata.yaml, rewrite S3 files.

---

## Polecat Workflow

### How Polecats Should Work (Ideal)

**Role**: Autonomous research completion using 4PS methodology

**Workflow**:
1. **Receive bead** assignment (research-XYZ)
2. **Read bead description** for topic, code, requirements
3. **Read methodology** (`docs/about.md` - 4PS framework)
4. **Create feature branch** (`research/1.XXX-topic-name`)
5. **Execute 4PS**:
   - S1: Library comparison (decision guide, NOT tutorial)
   - S2: Technical deep-dive (architecture, algorithms)
   - S3: WHO + WHY use cases (NOT implementation guides)
   - S4: Strategic viability (long-term, trade-offs)
6. **Create DOMAIN_EXPLAINER.md** (hardware store analogies)
7. **Create metadata.yaml** (sources, findings, recommendations)
8. **Validate** (`python3 scripts/validate_research.py 1.XXX`)
9. **Fix issues** if validation < 75%
10. **Re-validate** until 90%+
11. **Test local build** (`npm run build`)
12. **Commit to branch** with validation score in message
13. **Push branch** to origin
14. **Create PR** with detailed description
15. **Close bead** (work done, awaiting review)
16. **DO NOT merge PR** (human reviewer merges)

**Automation option**:
```bash
# One command does steps 8-15
python3 scripts/research_lifecycle.py complete 1.XXX research-BEAD-ID \
  --message "Complete research on <topic>"
```

### How Polecats Currently Work (Reality)

**Common issues**:

1. **Wrong directory** - Work in `/home/ivanadamin/gt/research/polecats/ace/` instead of `crew/ivan/`
   - Fix: Always `cd ~/gt/research/crew/ivan` first

2. **Skip validation** - Close bead without running `validate_research.py`
   - Result: 83% research committed as "complete"
   - Fix: Mandate validation before close (see RESEARCH-COMPLETION-REQUIREMENTS.md)

3. **S3 implementation guides** - Create "How to implement X" instead of WHO + WHY
   - Fix: Re-read 4PS methodology, focus on personas

4. **S1 installation tutorials** - Add "pip install" and code samples
   - Fix: Remove tutorials, keep only comparison data

5. **Missing metadata.yaml** - Forget to create metadata
   - Result: 83% score (100 structure + 25 content)
   - Fix: Add to checklist

6. **Incomplete metadata** - Create metadata but miss required fields
   - Result: 93% score (missing domain or sources)
   - Fix: Use template from existing research

7. **Wrong branch** - Commit to main instead of feature branch
   - Fix: Create feature branch first (`git checkout -b research/1.XXX-topic`)

8. **Merge own PR** - Try to merge instead of waiting for human review
   - Fix: Only create PR, don't merge

### Polecat Checklist

**Before starting**:
- [ ] Read bead description
- [ ] Read 4PS methodology (`docs/about.md`)
- [ ] Understand topic and scope
- [ ] Create feature branch (`research/1.XXX-topic-name`)

**During research**:
- [ ] Execute S1 (library comparison, NO installation guides)
- [ ] Execute S2 (technical deep-dive)
- [ ] Execute S3 (WHO + WHY, NO implementation guides)
- [ ] Execute S4 (strategic viability)
- [ ] Create DOMAIN_EXPLAINER.md (hardware store analogies)
- [ ] Create metadata.yaml (use template)

**Before commit**:
- [ ] Validate (`python3 scripts/validate_research.py 1.XXX`)
- [ ] Fix issues if < 75%
- [ ] Re-validate until 90%+
- [ ] Test conversion (`python3 scripts/convert_research.py`)
- [ ] Check for placeholders (`grep "^# S[1-4]-" docs/survey/1-XXX.md`)
- [ ] Test build (`npm run build`)

**Git workflow**:
- [ ] Stage research (`git add packages/research/1.XXX-*`)
- [ ] Commit with score (`git commit -m "research: Complete 1.XXX (96% score)"`)
- [ ] Push branch (`git push -u origin research/1.XXX-topic-name`)
- [ ] Create PR (use template from Step 13)
- [ ] Close bead (work done, awaiting review)
- [ ] DO NOT merge PR (human reviewer merges)

**Automation shortcut**:
```bash
# One command does validation → commit → push → PR → close bead
python3 scripts/research_lifecycle.py complete 1.XXX research-BEAD-ID \
  --message "Complete research on <topic>"
```

### Polecat Instructions Location

**File**: `~/gt/research/polecats/ace/.claude/RESEARCH-COMPLETION-REQUIREMENTS.md`

**Key points**:
- Validation MANDATORY before closing bead
- Feature branch workflow (not direct to main)
- PR creation (not merging)
- Score thresholds (< 75% = FAIL, 75-89% = ACCEPTABLE, 90%+ = EXCELLENT)

---

## Checklist Template

**Copy this checklist for each new research piece:**

```markdown
# Research 1.XXX: <Topic Name>

## Pre-Start
- [ ] Read 4PS methodology (docs/about.md)
- [ ] Understand topic scope (libraries, not applications)
- [ ] Create feature branch: `research/1.XXX-topic-name`
- [ ] Verify workspace: `pwd` = `/home/ivanadamin/gt/research/crew/ivan`

## Research Structure
- [ ] Create directory: `packages/research/1.XXX-topic-name/`
- [ ] Create S1-S4 subdirectories
- [ ] Create DOMAIN_EXPLAINER.md (hardware store analogies)

## S1: Rapid Discovery (Library Comparison)
- [ ] S1/approach.md (how S1 was executed)
- [ ] S1/<library1>.md (comparison data, NO installation guide)
- [ ] S1/<library2>.md
- [ ] S1/<library3>.md (minimum 3 libraries)
- [ ] S1/recommendation.md (which to explore in S2)
- [ ] Verify: No "pip install" or code samples

## S2: Comprehensive Discovery (Technical Deep-Dive)
- [ ] S2/approach.md
- [ ] S2/<library1>.md (architecture, algorithms, API)
- [ ] S2/<library2>.md
- [ ] S2/<library3>.md
- [ ] S2/feature-comparison.md (optional)
- [ ] S2/recommendation.md (how they differ)
- [ ] Verify: No installation tutorials

## S3: Need-Driven Discovery (WHO + WHY)
- [ ] S3/approach.md
- [ ] S3/use-case-<persona1>.md (WHO + WHY, NOT HOW)
- [ ] S3/use-case-<persona2>.md
- [ ] S3/use-case-<persona3>.md (minimum 3 use cases)
- [ ] S3/recommendation.md (who should use what)
- [ ] Verify: Each file starts with "## Who Needs This"
- [ ] Verify: No implementation guides

## S4: Strategic Discovery (Long-Term Viability)
- [ ] S4/approach.md
- [ ] S4/<library1>-viability.md (5-10 year outlook)
- [ ] S4/<library2>-viability.md
- [ ] S4/recommendation.md (strategic paths)

## Metadata
- [ ] Create metadata.yaml (use template from Step 8)
- [ ] Add: code, title, subtitle
- [ ] Add: tier, category, domain
- [ ] Add: status, completion_date
- [ ] Add: description
- [ ] Add: sources (with URLs/citations)
- [ ] Add: libraries_analyzed (with details)
- [ ] Add: key_findings (meaningful insights)
- [ ] Add: recommendations (actionable guidance)

## Validation
- [ ] Run: `python3 scripts/validate_research.py 1.XXX`
- [ ] Score ≥ 90% (EXCELLENT)? If not, fix issues.
- [ ] All S1-S4 directories exist?
- [ ] All required files present?
- [ ] DOMAIN_EXPLAINER.md ≥ 500 bytes?
- [ ] metadata.yaml complete?

## Testing
- [ ] Test conversion: `python3 scripts/convert_research.py`
- [ ] Check size: `ls -lh docs/survey/1-XXX.md` (should be > 50KB)
- [ ] Check placeholders: `grep "^# S[1-4]-" docs/survey/1-XXX.md` (should be none)
- [ ] Test build: `npm run build` (should succeed)
- [ ] Test local: `npm start` (check sidebar and content)

## Git Workflow
- [ ] Stage: `git add packages/research/1.XXX-*`
- [ ] Commit: `git commit -m "research: Complete 1.XXX <Topic> (XX% score)"`
- [ ] Push: `git push -u origin research/1.XXX-topic-name`
- [ ] Create PR (use template from Step 13)
- [ ] Wait for CI validation (should pass)
- [ ] Wait for human review
- [ ] DO NOT merge (human reviewer merges)

## Bead Management (If Using Beads)
- [ ] Close bead AFTER PR created: `bd update research-XYZ --status=closed`
- [ ] NOT after PR merged (human merges)

## Post-Merge (Human Action)
- [ ] CI auto-converts research
- [ ] CI auto-integrates (index, sidebar)
- [ ] Site deploys to production
- [ ] Research live in ~5 minutes
```

---

## Additional Resources

### Documentation
- `4PS_ORDER_TEMPLATE.md` - Bead description template
- `DOMAIN_EXPLAINER_TEMPLATE.md` - Universal analogies template
- `DEVELOPMENT.md` - Research rig development guide
- `DEPLOYMENT.md` - Deployment workflow and troubleshooting
- `PR-WORKFLOW.md` - Complete PR workflow guide
- `VALIDATION-ENFORCEMENT.md` - Quality enforcement system
- `RESEARCH-AUTOMATION-COMPLETE.md` - Automation system overview
- `RIG-STRUCTURE.md` - Directory organization
- `docs/about.md` - 4PS methodology explanation

### Scripts
- `scripts/research_lifecycle.py` - One-command workflow automation
- `scripts/validate_research.py` - Research quality validation
- `scripts/convert_research.py` - 4PS → Docusaurus conversion
- `scripts/integrate_research.py` - Index/sidebar updates
- `scripts/validate-and-commit.sh` - Streamlined validation + commit
- `scripts/install-hooks.sh` - Pre-commit hook installation
- `scripts/fix-mdx-brackets.py` - MDX syntax auto-fix

### Examples
- `packages/research/1.007-pattern-matching/` - Complete research (96% score)
- `packages/research/1.007-pattern-matching/metadata.yaml` - Complete metadata example

### GitHub Workflows
- `.github/workflows/validate-research-pr.yml` - PR validation gate
- `.github/workflows/integrate-research.yml` - Auto-integration on merge
- `.github/workflows/deploy.yml` - Site deployment

### Polecat Instructions
- `polecats/ace/.claude/RESEARCH-COMPLETION-REQUIREMENTS.md` - Validation requirements

---

## Quick Reference Card

**Validate**:
```bash
python3 scripts/validate_research.py 1.XXX
```

**Complete workflow** (one command):
```bash
python3 scripts/research_lifecycle.py complete 1.XXX research-BEAD \
  --message "Complete research on <topic>"
```

**Manual workflow**:
```bash
# 1. Create branch
git checkout -b research/1.XXX-topic-name

# 2. Create research (following 4PS)
# ...

# 3. Validate
python3 scripts/validate_research.py 1.XXX

# 4. Test
python3 scripts/convert_research.py
npm run build

# 5. Commit
git add packages/research/1.XXX-*
git commit -m "research: Complete 1.XXX Topic (96% score)"

# 6. Push
git push -u origin research/1.XXX-topic-name

# 7. Create PR
gh pr create --title "Research 1.XXX: Topic" --body "..."

# 8. Close bead (if using beads)
bd update research-XYZ --status=closed
```

**Score thresholds**:
- < 75%: ❌ FAIL (fix required)
- 75-89%: ⚠️ ACCEPTABLE (can ship)
- 90%+: ✅ EXCELLENT (ideal)

**Common fixes**:
- Missing metadata: Create `metadata.yaml` (see Step 8)
- Low score: Add domain/sources to metadata
- S3 wrong format: Rename to `use-case-*.md`, start with "## Who"
- S1 has tutorials: Remove installation guides and code
- Build fails: Run `python3 scripts/fix-mdx-brackets.py docs/survey/1-XXX.md`

**Get help**:
- Documentation: This file
- Examples: `packages/research/1.007-pattern-matching/`
- Troubleshooting: See sections above

---

**Last updated**: 2026-02-03
**Maintainer**: Survey of Software Team
