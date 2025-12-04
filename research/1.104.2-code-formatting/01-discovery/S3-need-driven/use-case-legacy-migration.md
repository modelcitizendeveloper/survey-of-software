# Use Case: Legacy Codebase Migration

## Scenario Overview

Adopting automated code formatting on an existing codebase with inconsistent style, requiring gradual migration without breaking blame history or blocking development.

## Primary Requirements

### Migration Safety
- Preserve git blame/history
- Avoid massive reformatting commits
- No disruption to active development
- Rollback capability

### Incremental Adoption
- Format new code only initially
- Progressive file/module migration
- No forced "big bang" reformatting
- Clear migration progress tracking

### Team Coordination
- Minimal merge conflict creation
- Clear migration timeline
- Training and onboarding
- Consensus building

### Tool Compatibility
- Work with existing linters
- Integrate with current CI/CD
- Support existing editor workflows
- No build system changes

## Recommended Toolchain

### Primary: Ruff Format (Python) or Prettier (JavaScript)
Modern formatters with incremental adoption support

### Supporting: pre-commit
Framework for gradual hook deployment

### Version Control: git-blame-ignore-revs
Preserve meaningful blame history

**Why This Combination:**
- Strong incremental migration support
- Excellent documentation for legacy adoption
- Community-proven migration patterns
- Minimal team disruption

## Migration Strategies

### Strategy 1: Progressive File Migration (Recommended)

**Timeline:** 2-4 weeks for medium codebase

**Phase 1: Setup (Week 1)**
1. Install formatter without enforcement
2. Configure formatting rules
3. Run on sample files for validation
4. Document style decisions

**Phase 2: New Code Only (Week 2)**
5. Enable pre-commit hooks for new/modified files
6. Format files as they're touched in PRs
7. Train team on format-on-save
8. Monitor adoption metrics

**Phase 3: Module-by-Module (Week 3-4)**
9. Format complete modules in dedicated PRs
10. Update `.git-blame-ignore-revs` file
11. Communicate changes to team
12. Enable CI enforcement per module

### Strategy 2: Immediate Full Formatting

**Timeline:** 1 week

**When to Use:**
- Small codebase (< 10k lines)
- Single developer or small team
- No active feature branches
- Clean git history not critical

**Steps:**
1. Create feature branch
2. Run formatter on entire codebase
3. Commit with descriptive message
4. Update `.git-blame-ignore-revs`
5. Merge to main
6. Enable enforcement immediately

### Strategy 3: Directory-Based Rollout

**Timeline:** 3-6 weeks for large codebase

**When to Use:**
- Monorepo with clear boundaries
- Multiple teams working independently
- Need to test formatting on subset first

**Steps:**
1. Start with least-critical directory
2. Format and validate
3. Enable enforcement for that path only
4. Gather feedback
5. Expand to next directory
6. Repeat until complete

## Configuration Approach

### Formatter Configuration (Python Example)

`pyproject.toml`:
```toml
[tool.ruff]
line-length = 100  # Match existing style if possible
target-version = "py38"

[tool.ruff.format]
quote-style = "double"  # Match existing majority preference
# Use preview mode cautiously
preview = false

# Exclude during migration
extend-exclude = [
    "legacy_module_a/",
    "legacy_module_b/",
]
```

### Incremental Pre-commit Configuration

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff-format
        # Only format specific paths during migration
        files: ^(src/new_module/|src/migrated_module/)
        # Or exclude legacy paths
        exclude: ^(legacy/|vendor/)
```

### Git Blame Ignore Configuration

`.git-blame-ignore-revs`:
```
# Mass formatting with Black - 2025-01-15
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0

# Migrated auth module to Ruff - 2025-02-01
b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1

# Format frontend with Prettier - 2025-02-10
c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2
```

Configure git to use this file:
```bash
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

## Pre-commit Hook Setup

### Gradual Enforcement Approach

**Phase 1: Optional (No Hooks)**
```bash
# Developers run manually
ruff format src/
prettier --write .
```

**Phase 2: Pre-commit Warning**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff-format
        verbose: true
        # Don't block commits yet
        stages: [manual]
```

**Phase 3: Automatic Formatting**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff-format
        # Auto-format on commit
        stages: [commit]
```

**Phase 4: Full Enforcement**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff-format
        args: [--check]  # Fail if unformatted
```

## CI/CD Integration

### Progressive CI Enforcement

**Stage 1: Warning Only**
```yaml
- name: Check formatting (informational)
  run: ruff format --check src/
  continue-on-error: true
```

**Stage 2: Fail on New Code**
```yaml
- name: Check formatting on changed files
  run: |
    FILES=$(git diff --name-only origin/main...HEAD | grep '\.py$')
    if [ -n "$FILES" ]; then
      ruff format --check $FILES
    fi
```

**Stage 3: Full Enforcement**
```yaml
- name: Check formatting
  run: ruff format --check .
```

## Common Pitfalls

### Pitfall 1: Big Bang Reformatting During Active Development
**Problem:** Reformatting entire codebase causes merge conflicts for all open branches

**Solution:**
- Announce reformatting 1 week in advance
- Coordinate with team to merge/pause feature work
- Provide rebase instructions
- Consider quiet period (Friday afternoon)

### Pitfall 2: Inconsistent Configuration Across Tools
**Problem:** Existing linter (Flake8) conflicts with new formatter (Black)

**Solution:**
- Update Flake8 configuration to ignore formatting rules:
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, E501, W503
```
- Or migrate to unified tool (Ruff)

### Pitfall 3: Lost Git Blame
**Problem:** Formatting commits hide actual code authors

**Solution:**
- Always use `.git-blame-ignore-revs`
- Document formatting commit hashes
- Educate team on `git blame --ignore-revs-file`
- Consider GitHub's automatic ignore support

### Pitfall 4: Mixed Formatting in Single File
**Problem:** Partially formatted files look inconsistent

**Solution:**
- Format complete files, not individual functions
- Use clear exclusion patterns during migration
- Document which modules are formatted
- Track migration progress visibly

### Pitfall 5: Reverting After Resistance
**Problem:** Team pushback causes abandonment of formatting effort

**Solution:**
- Build consensus before starting
- Run pilot on small module first
- Demonstrate productivity gains
- Address specific concerns individually
- Consider gradual "new code only" approach if needed

## Communication Strategy

### Before Migration
- **Announcement:** Share formatting decision and rationale
- **Timeline:** Publish migration schedule
- **Training:** Offer editor setup sessions
- **Feedback:** Collect concerns and address

### During Migration
- **Progress Updates:** Weekly status on formatted modules
- **Support:** Dedicated Slack channel or help desk
- **Documentation:** Keep migration guide updated
- **Flexibility:** Adjust timeline based on feedback

### After Migration
- **Retrospective:** Review what worked and what didn't
- **Maintenance:** Document ongoing formatting processes
- **Metrics:** Share productivity improvements
- **Standards Update:** Update contributing guidelines

## Example Migration Timeline

### Week 1: Preparation
- Install formatters and configure
- Run on test module and validate
- Set up CI warning (non-blocking)
- Document decisions in CONTRIBUTING.md

### Week 2: Pilot
- Format 1-2 modules in separate PRs
- Enable pre-commit hooks (optional)
- Gather team feedback
- Refine configuration if needed

### Week 3: Gradual Rollout
- Format 3-5 modules per day
- Update `.git-blame-ignore-revs` daily
- Enable pre-commit hooks (auto-fix)
- Monitor merge conflict frequency

### Week 4: Completion
- Format remaining modules
- Enable CI enforcement
- Make pre-commit hooks mandatory
- Celebrate and document wins

## Success Metrics

- Migration completed without major merge conflicts
- < 5% of team needs formatting help after Week 2
- Git blame remains useful via `.git-blame-ignore-revs`
- Zero formatting debates in PRs post-migration
- Development velocity maintained or improved

## Date Compiled
December 4, 2025
