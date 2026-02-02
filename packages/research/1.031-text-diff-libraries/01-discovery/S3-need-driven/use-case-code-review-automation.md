# Use Case: Code Review Automation Builders

## Who Needs This

**Persona:** DevOps engineers, CI/CD platform developers, code review tool builders

**Context:**
- Building automated code review tools (linters, security scanners, custom checks)
- Analyzing pull requests in CI/CD pipelines
- Generating diff-based insights (what changed, security impact, test coverage)
- Integrating with git workflows (GitHub, GitLab, Bitbucket)

**Scale:**
- 10s-100s of PRs per day
- Diffs range from single-line to 1000s of lines
- Multiple repositories, languages, teams
- Must handle merge commits, rebases, moved files

**Constraints:**
- Git integration required (already using git repos)
- Must support multiple diff algorithms (Myers, patience, histogram)
- Fast enough for CI/CD (seconds per PR, not minutes)
- Parse output programmatically (not for human viewing only)
- Reliable (production CI/CD depends on this)

## Why They Need It

**Problem:** Building tools that analyze code changes requires:
1. Generating diffs (what changed)
2. Parsing diffs (programmatic access to hunks, files, lines)
3. Advanced algorithms (patience diff for moved code, histogram for large refactorings)
4. Integration with git history (commits, branches, merge bases)

**Requirements:**
- **MUST**: Git integration (read from repositories)
- **MUST**: Multiple algorithms (Myers + patience + histogram)
- **MUST**: Programmatic parsing (not just text output)
- **MUST**: Production-ready (used in CI/CD, can't be flaky)
- **SHOULD**: Handle large repos (Linux kernel, Chromium scale)
- **SHOULD**: Three-way merge (for merge commit analysis)

**Anti-Requirements:**
- Not for comparing test outputs (use difflib/DeepDiff for that)
- Not for semantic code analysis (use tree-sitter if need AST)
- Not for standalone text files (use diff-match-patch)

## Library Fit Analysis

### Recommended Solution

→ **GitPython + unidiff**

**GitPython** (diff generation):
- ✅ Full git integration (repos, commits, branches)
- ✅ Multiple algorithms (Myers, patience, histogram via flags)
- ✅ Three-way merge support (merge commit analysis)
- ✅ Very active, widely used (50M downloads/month)
- ✅ Handles large repos well (delegates to git binary)

**unidiff** (diff parsing):
- ✅ Fast parsing (no LCS computation)
- ✅ Clean API (PatchSet, PatchedFile, Hunk objects)
- ✅ Programmatic access (filter files, iterate changes)
- ✅ Lightweight (3M downloads/month, stable)

**Why this combination:**
- GitPython generates diffs with advanced algorithms
- unidiff parses output into structured objects
- Clean separation (generation vs parsing)
- Both production-ready, widely used

### Alternative: GitPython alone

**If you only need:**
- Diff generation (not parsing)
- Simple text output (display to users)
- Git operations beyond diff (commits, branches)

**Skip unidiff if:**
- You're using git's built-in parser (language bindings)
- Don't need programmatic hunk/line access

### Anti-Patterns

**❌ DON'T use difflib:**
- No git integration (can't read repos)
- No patience/histogram algorithms
- Poor performance on large files

**❌ DON'T use diff-match-patch:**
- No git integration
- No patience/histogram
- Myers only (inferior for moved code)

**❌ DON'T use tree-sitter:**
- Not a diff tool (parsing library)
- Overkill unless you need semantic analysis
- Slow, complex setup

### Decision Factors

**Choose GitPython when:**
- Working with git repositories (the common case)
- Need advanced algorithms (patience, histogram)
- Building production CI/CD tools
- Need full git functionality (commits, branches, history)

**Add unidiff when:**
- Need to analyze diffs programmatically (filter hunks, count changes)
- Want structured access to diff components
- Building complex diff-based logic

**Skip GitPython if:**
- Not working with git (use diff-match-patch for standalone files)
- Can't install git binary (constrained environments)

## Validation Criteria

**You picked the right library if:**
- ✅ Can generate diffs for any commit in git repos
- ✅ Patience diff shows moved code blocks correctly
- ✅ Can parse diff output to filter/analyze changes
- ✅ Fast enough for CI/CD (seconds per PR)
- ✅ Production-stable (doesn't break on weird diffs)

**Red flags (wrong choice):**
- ❌ Poor diffs for refactorings (use patience, not Myers)
- ❌ Can't parse diff output easily (add unidiff)
- ❌ Hangs on large diffs (GitPython delegates to git, should handle)
- ❌ Can't access git history (need GitPython, not standalone diff)

## Common Patterns

**Pattern: Full pipeline**
```
GitPython.repo.head.commit.diff()  # Generate diff
  → unidiff.PatchSet(diff_output)  # Parse into objects
  → filter/analyze hunks           # Custom logic
  → generate insights               # Security, coverage, etc.
```

**Pattern: Algorithm selection**
```
# Default: Myers (fast, works for most cases)
diff = repo.git.diff('HEAD~1')

# Refactoring detection: patience (better for moved blocks)
diff = repo.git.diff('HEAD~1', patience=True)

# Large changes: histogram (best for massive refactorings)
diff = repo.git.diff('HEAD~1', histogram=True)
```

**Pattern: Merge analysis**
```
# Three-way diff for merge commits
merge_base = repo.merge_base(branch_a, branch_b)
diff = repo.git.diff(merge_base, branch_a)
```

## Real-World Example

**Scenario:** Building a security scanner that checks if PRs modify auth code

**Requirements:**
- Analyze every PR in CI/CD
- Find files matching `*/auth/*` or `*/security/*`
- Check if sensitive functions were changed
- Report which lines changed in those files
- Use patience diff (auth code often refactored, moved)

**Solution:** GitPython + unidiff
1. GitPython generates patience diff for PR
2. unidiff parses diff into PatchedFile objects
3. Filter files matching `*/auth/*` paths
4. Iterate hunks to find changed functions
5. Generate security review report

**Why not difflib:** No git integration, can't read PR diffs

**Why not tree-sitter:** Overkill for path-based filtering, slower
