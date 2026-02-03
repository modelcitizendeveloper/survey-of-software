# Research Validation Enforcement System

## Summary

Multi-layer enforcement system to prevent incomplete research from being committed or closed.

## Enforcement Layers

### Layer 1: Pre-Commit Hook (Automatic)
**Location**: `.git/hooks/pre-commit` (installed via `scripts/install-hooks.sh`)

**Behavior**:
- Runs on every `git commit`
- Validates all staged research files in `packages/research/`
- Blocks commit if validation score < 75%
- Warns if score 75-89%
- Passes if score 90%+

**Example**:
```bash
$ git commit -m "research: Add incomplete 1.xxx"
🔍 Running pre-commit validation...
  → Validating research quality...
    ❌ Research 1.xxx scored 65% (minimum: 75% required)
       Run: python3 scripts/validate_research.py 1.xxx
       Missing components must be completed before committing

❌ Found 1 issue(s) that need to be fixed before committing.

To bypass these checks (NOT recommended):
  git commit --no-verify
```

### Layer 2: Helper Script (Manual)
**Location**: `scripts/validate-and-commit.sh`

**Usage**:
```bash
./scripts/validate-and-commit.sh 1.007 "Complete Pattern Matching research"
```

**Behavior**:
- Validates research first
- Blocks if < 75%
- Prompts for confirmation if 75-89%
- Auto-commits if 90%+
- Provides next steps after commit

**Benefits**:
- One command validates + commits
- Interactive confirmation for borderline scores
- Guides user through workflow

### Layer 3: Polecat Instructions (Documentation)
**Location**: `polecats/ace/.claude/RESEARCH-COMPLETION-REQUIREMENTS.md`

**Purpose**:
- Instructs polecats to run validation before closing beads
- Explains scoring thresholds
- Documents what to do when validation fails
- Prevents polecats from closing incomplete research

**Key Requirement**:
> You MUST validate research before closing any research bead.

## Validation Scoring

### Thresholds

| Score | Status | Action |
|-------|--------|--------|
| < 75% | ❌ FAIL | Cannot commit/close |
| 75-89% | ⚠️ ACCEPTABLE | Can commit with warning |
| 90%+ | ✅ EXCELLENT | Ideal score |

### Scoring Breakdown

**Structure (100 points)**:
- S1-S4 directories exist (25 points each)
- Required files per phase (approach, libraries, recommendation)
- DOMAIN_EXPLAINER.md exists
- metadata.yaml exists

**Content Quality (50 points)**:
- metadata.yaml completeness (30 points)
  - All required fields (id, title, status, dates, sources, libraries_evaluated, key_findings)
  - Optional fields (domain, tags, related_research, etc.)
- File size thresholds (20 points)
  - DOMAIN_EXPLAINER.md > 500 bytes
  - Each S phase files have reasonable content

### Common Issues

**1. Missing metadata.yaml** (Most common)
- **Symptom**: Score 83% (100 structure + 25 content)
- **Fix**: Create metadata.yaml with all required fields
- **Example**: See `packages/research/1.006-graph-search/metadata.yaml`

**2. Missing domain field in metadata**
- **Symptom**: Score 93% (100 structure + 40 content)
- **Fix**: Add `domain: "<domain>"` to metadata.yaml

**3. Incomplete phases**
- **Symptom**: Score < 100 structure
- **Fix**: Ensure all S1-S4 have approach.md, library files, recommendation.md

## Testing Enforcement

### Test Pre-Commit Hook

**1. Create incomplete research**:
```bash
mkdir -p packages/research/1.999-test/01-discovery/S1-rapid
touch packages/research/1.999-test/DOMAIN_EXPLAINER.md
git add packages/research/1.999-test/
```

**2. Try to commit**:
```bash
git commit -m "test: incomplete research"
# Should FAIL with validation error
```

**3. Complete the research**:
```bash
# Add all S1-S4 phases
# Add metadata.yaml
git add packages/research/1.999-test/
git commit -m "test: complete research"
# Should PASS
```

### Test Helper Script

```bash
# Should fail (incomplete)
./scripts/validate-and-commit.sh 1.999 "Test commit"

# Should prompt (acceptable but not excellent)
# Complete research to 80%
./scripts/validate-and-commit.sh 1.999 "Test commit"

# Should auto-commit (excellent)
# Complete research to 95%
./scripts/validate-and-commit.sh 1.999 "Test commit"
```

### Test Polecat Instructions

1. Assign research bead to polecat
2. Polecat creates research
3. Before closing bead, polecat should run validation
4. If < 75%, polecat should fix issues and re-validate
5. Only close bead after validation passes

## Bypassing Enforcement (Not Recommended)

### Bypass Pre-Commit Hook

```bash
git commit --no-verify -m "bypass validation"
```

**When to use**:
- Emergency fixes
- Non-research changes that trigger false positives
- You're absolutely certain the research is complete

**WARNING**: This defeats the purpose of validation enforcement. Use sparingly.

### Why Enforcement Matters

**Before enforcement**:
- ❌ Polecats closed beads without validation
- ❌ Incomplete research (83%) was committed as "complete"
- ❌ Missing metadata.yaml discovered only after integration
- ❌ Manual intervention required to fix

**After enforcement**:
- ✅ Pre-commit hook catches incomplete research
- ✅ Polecats instructed to validate before closing
- ✅ Helper script streamlines workflow
- ✅ Quality standards enforced automatically

## Maintenance

### Updating Validation Requirements

**1. Update validation script**:
- Edit `scripts/validate_research.py`
- Adjust scoring thresholds or add new checks

**2. Update pre-commit hook**:
- Edit `scripts/pre-commit-hook.sh`
- Update minimum score threshold (currently 75%)
- Reinstall: `bash scripts/install-hooks.sh`

**3. Update documentation**:
- Edit `RESEARCH-COMPLETION-REQUIREMENTS.md`
- Update `VALIDATION-ENFORCEMENT.md` (this file)
- Update `scripts/AUTOMATION-GUIDE.md`

### Monitoring Effectiveness

**Check validation scores in commits**:
```bash
git log --grep="validation score" --oneline
```

**Find research that bypassed validation**:
```bash
git log --all --grep="--no-verify" --oneline
```

**Audit research completeness**:
```bash
for dir in packages/research/*/; do
  code=$(basename "$dir" | cut -d'-' -f1)
  echo -n "$code: "
  python3 scripts/validate_research.py "$code" 2>&1 | grep "Overall Score"
done
```

## Success Metrics

**Research #100 (Pattern Matching)**:
- ✅ Polecat created comprehensive 4PS research
- ✅ Initially closed at 83% (missing metadata.yaml)
- ✅ Reopened, completed metadata.yaml
- ✅ Final score: 93% (EXCELLENT)
- ✅ Pre-commit hook validated on commit
- ✅ Enforcement prevented incomplete submission

**Lessons learned**:
1. Validation must run before closing beads
2. Multiple enforcement layers catch different failure modes
3. Clear documentation helps polecats follow requirements
4. Automated hooks prevent human error

## Future Enhancements

**Potential improvements**:
1. **Beads validation gate**: Prevent status=closed if validation fails
2. **CI validation**: Run validation in GitHub Actions
3. **Score trending**: Track validation scores over time
4. **Auto-fix**: Automatically create minimal metadata.yaml
5. **Severity levels**: Different thresholds for different research tiers

## See Also

- `scripts/validate_research.py` - Validation script
- `scripts/pre-commit-hook.sh` - Pre-commit hook source
- `scripts/validate-and-commit.sh` - Helper script
- `polecats/ace/.claude/RESEARCH-COMPLETION-REQUIREMENTS.md` - Polecat instructions
- `scripts/AUTOMATION-GUIDE.md` - Overall automation documentation
