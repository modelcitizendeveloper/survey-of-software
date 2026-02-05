# Survey of Software - Research Library

**Live Site:** https://research.modelcitizendeveloper.com/

A curated collection of research pieces covering software libraries, algorithms, and development tools across 199 domains

## About

This research library helps developers make informed decisions about software libraries and tools. Each research piece provides:

- **Concept explanations** - Clear explanations for beginners
- **Library comparisons** - Side-by-side analysis of alternatives
- **Production readiness** - Assessment of stability and maturity
- **Long-term viability** - Evaluation of maintenance and community health

**Current Progress:** 111 completed pieces (56%)

## Categories

Research is organized into 13 major categories:

- **1.001-009** Sorting & Searching Algorithms
- **1.010-019** Graph & Network Algorithms
- **1.020-029** Mathematical & Statistical Algorithms
- **1.030-039** String & Text Algorithms
- **1.040-049** Data Structure Libraries
- **1.050-059** Compression & Encoding
- **1.060-069** Cryptographic & Hashing
- **1.070-079** Machine Learning Algorithms
- **1.080-089** Geometric & Spatial Algorithms
- **1.100-109** Text & Document Processing
- **1.110-119** User Interface & Frontend
- **1.200-209** LLM & AI Stack
- **1.300-309** Public Finance & Civic Data

Browse the full catalog at https://research.modelcitizendeveloper.com/survey/

## Building Locally

```bash
# Install Hugo extended v0.155.2+
# macOS: brew install hugo
# Linux: https://github.com/gohugoio/hugo/releases

# Clone and build
git clone https://github.com/modelcitizendeveloper/survey-of-software-site.git
cd survey-of-software-site
git submodule update --init --recursive
hugo server -D

# View at http://localhost:1313/
```

## Technical Details

- **Generator:** Hugo v0.155.2 (extended)
- **Theme:** [hugo-book](https://github.com/alex-shpak/hugo-book)
- **Deployment:** GitHub Pages via GitHub Actions
- **Custom Domain:** research.modelcitizendeveloper.com

## Directory Structure

```
survey-of-software-site/
├── content/
│   ├── _index.md           # Homepage
│   ├── about.md            # About page
│   ├── vision.md           # Vision page
│   └── survey/             # Research content
│       ├── _index.md       # Survey index
│       ├── 1-001.md        # Individual research pieces
│       └── ...             # 199 research slots
├── themes/hugo-book/       # Hugo Book theme (submodule)
├── .github/workflows/      # Deployment automation
└── hugo.toml               # Hugo configuration
```

## Critical Hugo Gotchas

### ⚠️ Section Index Files MUST be Named `_index.md`

**IMPORTANT**: Hugo requires section index files to be named `_index.md` (with underscore), not `index.md`.

- ✅ `content/survey/_index.md` - Correct (section index)
- ❌ `content/survey/index.md` - Wrong (will cause Hugo to skip building individual pages)

**What happens if both exist?**
- Hugo gets confused and only builds the section index page
- Individual research pages (1-001.md, 1-002.md, etc.) won't be generated
- Deployed site will show 404s for all research pages

**If you see only 1 page built instead of 147+:**
1. Check for duplicate index files: `ls content/survey/*index.md`
2. Delete `index.md` if it exists: `rm content/survey/index.md`
3. Keep only `_index.md`

### Front Matter Format

Hugo Book theme requires specific front matter:

```yaml
---
title: "Page Title"
weight: 1                    # Sort order (lower = earlier)
bookFlatSection: false       # Flatten hierarchy
bookCollapseSection: false   # Auto-collapse in sidebar
---
```

**Not Docusaurus format:**
```yaml
---
sidebar_position: 0  # Wrong - this is Docusaurus
slug: /survey        # Wrong - this is Docusaurus
---
```

## Deployment Workflow

The site auto-deploys via GitHub Actions when changes are pushed to `main`:

1. **Trigger**: Push to `main` with changes in `research-site-hugo/**` or `.github/workflows/deploy-hugo.yml`
2. **Build**: GitHub Actions runs `hugo --minify` to generate static files
3. **Upload**: Artifact uploaded to GitHub Pages
4. **Deploy**: Automatic deployment to https://research.modelcitizendeveloper.com/

**Workflow file**: `.github/workflows/deploy-hugo.yml`

### Testing Before Push

Always test locally before pushing:

```bash
cd research-site-hugo
hugo               # Build (check page count)
hugo server -D     # Test locally at localhost:1313
```

Expected output:
```
Pages            │ 147+    # Should be 147 or more, not just 1-2
```

If you see only 1-2 pages, check for the `_index.md` vs `index.md` issue.

## Adding New Research Content

1. Create markdown file: `content/survey/1-XXX.md`
2. Add proper front matter (see above)
3. Update `content/survey/_index.md` to reference the new piece
4. Test locally: `hugo server -D`
5. Commit and push

## Build Artifacts (Gitignored)

These directories are auto-generated and should NOT be committed:

- `public/` - Generated static site
- `resources/_gen/` - Processed assets (images, CSS, etc.)
- `.hugo_build.lock` - Hugo build lock file

All are in `.gitignore` at the repo root.

## Troubleshooting

### Site shows 404 for individual pages

1. Check build output page count: `hugo` → should show 147+ pages
2. Check for duplicate index files: `ls content/survey/*index.md`
3. Verify only `_index.md` exists (delete `index.md` if present)
4. Check workflow logs for artifact contents

### Hugo version mismatch

The workflow uses Hugo v0.155.2 extended. Match this locally to avoid build differences:

```bash
hugo version
# Should show: hugo v0.155.2+extended
```

### Theme issues

The theme is a git submodule. If missing:

```bash
git submodule update --init --recursive
```

## Theme

Using [hugo-book](https://github.com/alex-shpak/hugo-book) theme for clean documentation layout.

Theme is included as a git submodule in `themes/hugo-book/`.
