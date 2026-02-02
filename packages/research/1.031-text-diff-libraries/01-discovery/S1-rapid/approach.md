# S1 Rapid Discovery: Approach

## Goal
Quickly identify 5-10 Python libraries for text differencing across different algorithm categories.

## Search Strategy

### 1. Algorithm Categories
- **Line-based diff**: Myers, patience, histogram algorithms
- **Semantic diff**: AST/tree-based diffing
- **Word/character diff**: Fine-grained text comparison
- **Structured diff**: JSON, XML, specialized formats
- **Merge/patch**: 3-way merge, conflict resolution

### 2. Library Sources
- Python Package Index (PyPI) search: "diff", "patch", "merge"
- Standard library: `difflib`
- Git ecosystem: Libraries used by git tools
- Code review tools: Libraries used by GitHub, GitLab
- Academic implementations: Papers with reference implementations

### 3. Inclusion Criteria
- Has Python API (native or bindings)
- Actively maintained OR widely used despite maintenance mode
- Implements at least one diff algorithm
- Available on PyPI or pip-installable

### 4. Exclusion Criteria
- Pure command-line tools with no Python API
- Abandoned libraries (>5 years no updates, no users)
- Language-specific diff tools for non-Python languages (unless Python bindings exist)

## Deliverables

For each library:
- Name and PyPI package name
- Primary algorithm(s) implemented
- Installation method
- Brief description (2-3 sentences)
- Status: active / maintenance mode / abandoned
- GitHub stars / PyPI downloads (rough popularity metric)
- Quick example (if trivial to demonstrate)

## Libraries to Investigate

**Line-based:**
1. `difflib` (stdlib) - SequenceMatcher, Myers-like
2. `diff-match-patch` - Google's library
3. `python-diff` - GNU diff in Python
4. `unidiff` - Unified diff parser

**Semantic/Structural:**
5. `tree-sitter` - Parse tree diffing
6. `gumtree-python` - AST diff (if bindings exist)
7. `difftastic` - Structural diff via tree-sitter (if Python accessible)

**Specialized:**
8. `deepdiff` - Python object diffing
9. `jsondiff` - JSON-specific diff
10. `xmldiff` - XML tree diff

**Merge/Patch:**
11. `python-diff3` - 3-way merge
12. `automerge-py` - CRDT-based merge (if exists)

## Time Budget
- 2-3 hours total
- ~15-20 minutes per library
- Focus on breadth, not depth (depth comes in S2)
