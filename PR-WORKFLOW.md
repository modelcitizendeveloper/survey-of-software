# Pull Request Workflow for Research

## Overview

All research submissions use a **feature branch + PR workflow** with automated CI validation and integration.

## Complete Workflow

### 1. Create Research Branch

```bash
# Naming convention: research/1.xxx-topic-name
git checkout -b research/1.013-string-algorithms
```

### 2. Create Research (Polecat or Human)

```bash
# Research goes in packages/research/
packages/research/1.013-string-algorithms/
├── DOMAIN_EXPLAINER.md
├── metadata.yaml
└── 01-discovery/
    ├── S1-rapid/
    ├── S2-comprehensive/
    ├── S3-need-driven/
    └── S4-strategic/
```

### 3. Validate Locally

```bash
python3 scripts/validate_research.py 1.013
# Must score 75%+ (90%+ recommended)
```

### 4. Commit to Feature Branch

```bash
git add packages/research/1.013-*
git commit -m "research: Complete 1.013 String Algorithms (96% score)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### 5. Push Branch

```bash
git push -u origin research/1.013-string-algorithms
```

### 6. Create Pull Request

```bash
gh pr create --title "Research 1.013: String Algorithms" --body "$(cat <<'EOF'
## Research Details
- **Code**: 1.013
- **Topic**: String Algorithms
- **Validation Score**: 96% (EXCELLENT)
- **Methodology**: 4PS (S1-S4 complete)

## Structure
- ✅ DOMAIN_EXPLAINER.md (18KB)
- ✅ S1: Rapid Discovery (5 files)
- ✅ S2: Comprehensive Discovery (6 files)
- ✅ S3: Need-Driven Discovery (4 files)
- ✅ S4: Strategic Discovery (3 files)
- ✅ metadata.yaml with complete sourcing

## Validation Results
\`\`\`
$ python3 scripts/validate_research.py 1.013

Research Validation Report: 1.013
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

🤖 Created by Polecat Ace
EOF
)"
```

Or from the GitHub UI: Click "Compare & pull request" button

### 7. CI Validation (Automatic)

**What CI checks**:
- ✅ Extracts research codes from PR
- ✅ Runs `validate_research.py` for each code
- ✅ Blocks PR if any research < 75%
- ✅ Comments validation results on PR

**Example CI comment**:
```
## ✅ Research Validation Passed

- **1.013**: 96% - ✅ EXCELLENT

All research meets quality standards (75%+).
```

### 8. Human Review

**Reviewer checks**:
- Content accuracy and completeness
- 4PS methodology followed
- Sources properly cited
- No problematic content

```bash
# Review locally
gh pr checkout 123
python3 scripts/validate_research.py 1.013
cat packages/research/1.013-*/metadata.yaml

# Approve
gh pr review 123 --approve --body "Excellent research! LGTM 🚀"
```

### 9. Merge PR

```bash
# Squash merge (cleaner history)
gh pr merge 123 --squash --delete-branch

# Or from GitHub UI
```

### 10. Auto-Integration (Automatic on Merge)

**What happens automatically**:
1. ✅ CI detects new research in `packages/research/`
2. ✅ Runs `convert_research.py` → generates `docs/survey/1-013.md`
3. ✅ Runs `integrate_research.py` → updates index.md and sidebars.ts
4. ✅ Commits integration changes to main
5. ✅ Triggers deployment to GitHub Pages
6. ✅ Research live on site in ~5 minutes

**CI commit message**:
```
docs: Auto-integrate research 1.013

Automated conversion and integration:
- Converted packages/research/ to docs/survey/
- Updated survey index with new entries
- Updated sidebar navigation

Research codes: 1.013

Co-Authored-By: github-actions[bot]
```

## Branch Protection (Recommended)

Configure on GitHub Settings → Branches → main:

```yaml
Protection rules:
- ✅ Require pull request before merging
- ✅ Require status checks (validate-research-pr)
- ✅ Require conversation resolution
- ✅ Delete head branches automatically
```

## For Polecats

**Updated instructions**: See `polecats/ace/.claude/RESEARCH-COMPLETION-REQUIREMENTS.md`

**Key points**:
- Create feature branch: `research/1.xxx-topic-name`
- Validate before pushing (75%+)
- Create PR with detailed description
- **DO NOT merge** - human will review and merge
- Close bead after PR is created (not after merge)

## For Multiple Contributors

**This workflow scales for**:
- Multiple polecats working in parallel
- Human contributors submitting research
- External contributors (if repo is public)
- Cross-team collaboration

**Parallel work example**:
```
research/1.013-string-algorithms    (Polecat Ace)
research/1.014-graph-traversal      (Polecat Beta)
research/1.015-sorting-networks     (Human contributor)
```

All can work simultaneously without conflicts. Merge order doesn't matter - integration is idempotent.

## Troubleshooting

### PR blocked by CI validation

**Symptom**: CI fails with "Research validation failed"

**Fix**:
```bash
# Check validation locally
python3 scripts/validate_research.py 1.xxx

# Fix issues (add missing files, improve metadata, etc.)
git add packages/research/1.xxx-*
git commit -m "fix: Improve research 1.xxx (now XX% score)"
git push

# CI will re-run automatically
```

### Auto-integration not triggered

**Symptom**: PR merged but no integration commit

**Possible causes**:
1. PR didn't change `packages/research/` (check PR diff)
2. CI workflow disabled (check Actions tab)
3. GitHub token permissions (check workflow logs)

**Manual integration**:
```bash
git pull origin main
python3 scripts/convert_research.py
python3 scripts/integrate_research.py
git add docs/survey/ sidebars.ts
git commit -m "docs: Manual integration of research 1.xxx"
git push
```

### Merge conflicts

**Rare but possible if**:
- Multiple PRs modify same research code
- Integration conflicts (index.md, sidebars.ts)

**Resolution**:
```bash
git checkout research/1.xxx-topic
git fetch origin
git merge origin/main
# Resolve conflicts
git add .
git commit -m "fix: Resolve merge conflicts"
git push
```

## Benefits

✅ **Quality gate**: CI validates before merge
✅ **Review process**: Human oversight for all research
✅ **Audit trail**: Full PR history with discussions
✅ **Automation**: Zero manual integration steps
✅ **Scalability**: Parallel work without conflicts
✅ **Rollback**: Easy revert if issues found
✅ **Collaboration**: Standard Git workflow familiar to contributors

## Next Steps

1. **Test workflow**: Create a test PR for research 1.013
2. **Monitor CI**: Verify validation and integration work
3. **Document learnings**: Update this doc with any issues
4. **Scale up**: Enable for all future research

---

**The PR workflow is now production-ready!** 🚀
