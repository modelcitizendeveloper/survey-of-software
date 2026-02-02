# unidiff

## Overview
**Package:** `unidiff`
**Algorithm:** N/A (parser, not diff generator)
**Status:** Active (regular updates)
**Author:** Matias Bordese
**First Released:** 2012
**Purpose:** Parse and manipulate unified diff format

## Description
A parser for unified and context diff formats (the output of `diff -u` and `git diff`). It doesn't generate diffs - instead, it parses existing diff output into Python objects for programmatic analysis and modification.

**Key features:**
- **Parse unified diff**: Read diff output from git, patch files, etc.
- **Patch manipulation**: Add, remove, or modify hunks programmatically
- **Multi-file support**: Handle diffs across multiple files
- **Metadata extraction**: Extract added/removed lines, file paths, line numbers
- **Pretty printing**: Convert back to diff format

## Use Cases
- **Code review tools**: Parse `git diff` output for analysis
- **CI/CD pipelines**: Analyze what changed in a commit
- **Patch automation**: Modify diffs before applying
- **Diff statistics**: Count lines added/removed per file
- **Conflict detection**: Find overlapping changes

## Installation
```bash
pip install unidiff
```

## Basic Usage

### Parse a diff string
```python
from unidiff import PatchSet

diff_text = """
--- a/file.txt
+++ b/file.txt
@@ -1,3 +1,4 @@
 Line 1
-Line 2
+Line 2 modified
 Line 3
+Line 4
"""

patch = PatchSet(diff_text)

# Iterate over files
for patched_file in patch:
    print(f"File: {patched_file.path}")

    # Iterate over hunks
    for hunk in patched_file:
        print(f"  Hunk: {hunk}")

        # Iterate over lines
        for line in hunk:
            if line.is_added:
                print(f"    + {line.value}")
            elif line.is_removed:
                print(f"    - {line.value}")
            else:
                print(f"      {line.value}")
```

### Parse git diff output
```python
import subprocess
from unidiff import PatchSet

# Get diff from git
result = subprocess.run(
    ['git', 'diff', 'HEAD~1', 'HEAD'],
    capture_output=True,
    text=True
)

patch = PatchSet(result.stdout)

# Statistics
added_lines = sum(f.added for f in patch)
removed_lines = sum(f.removed for f in patch)
print(f"Added: {added_lines}, Removed: {removed_lines}")

# File-level changes
for file in patch:
    print(f"{file.path}: +{file.added} -{file.removed}")
```

### Filter and modify diffs
```python
from unidiff import PatchSet

patch = PatchSet(diff_text)

# Keep only changes to .py files
python_files = [f for f in patch if f.path.endswith('.py')]

# Filter out whitespace-only changes
for file in patch:
    for hunk in file:
        hunk.source_lines = [
            line for line in hunk.source_lines
            if not line.value.strip() == ''
        ]
```

### Get line-level details
```python
from unidiff import PatchSet

patch = PatchSet(diff_text)

for file in patch:
    for hunk in file:
        for line in hunk:
            print(f"Line {line.source_line_no or line.target_line_no}: "
                  f"{'ADD' if line.is_added else 'DEL' if line.is_removed else 'CTX'} "
                  f"{repr(line.value)}")
```

## Pros
- **Parse existing diffs**: Work with output from git, diff, etc.
- **Programmatic access**: Extract metadata, filter, modify diffs
- **Multi-file support**: Handle patch files with many files
- **Active maintenance**: Regular updates and bug fixes
- **Clean API**: Intuitive object model (PatchSet → PatchedFile → Hunk → Line)

## Cons
- **Not a diff generator**: Can't create diffs, only parse them
- **Limited to unified/context format**: Can't parse other diff formats
- **No semantic understanding**: Treats diffs as text, not code structure
- **Dependency**: Needs `git` or external diff tool to generate diffs

## When to Use
- **Parsing git diffs**: Analyze commits, pull requests
- **Code review automation**: Extract changed files/lines
- **CI/CD diff analysis**: Detect risky changes (e.g., migrations, config)
- **Patch manipulation**: Modify diffs before applying
- **Diff statistics**: Generate reports on code changes

## When NOT to Use
- **Generating diffs**: Use `difflib`, `diff-match-patch`, or `git`
- **Semantic analysis**: Use tree-sitter or AST-based tools
- **Non-unified formats**: Won't parse other diff formats

## Complementary Libraries
Often used with:
- **GitPython**: Generate diffs using git
- **difflib**: Generate diffs in Python
- **subprocess**: Call `git diff` or `diff` command

## Popularity
- **GitHub stars:** ~400
- **PyPI downloads:** ~3M/month (widely used in CI/CD tools)
- **Status:** Active, well-maintained

## Real-World Usage
- **Code review tools**: Parse GitHub PR diffs
- **Static analysis**: Check what changed in a commit
- **Automated testing**: Verify expected diff output
- **Release tools**: Generate changelogs from diffs

## Verdict
**Best for:** Parsing and analyzing unified diff output from git or other tools. Essential for CI/CD pipelines, code review automation, and diff-based workflows.

**Skip if:** You need to generate diffs (use `difflib` or `diff-match-patch` instead). This library is strictly a parser.
