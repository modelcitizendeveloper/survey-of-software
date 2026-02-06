# Use Case: Developer Tool Creators

## Who Needs This

**Persona:** IDE plugin developers, refactoring tool builders, code intelligence platform developers

**Context:**
- Building semantic code analysis tools (refactoring detectors, API migration tools)
- Creating language-aware diff viewers (show function renames, not text changes)
- Developing code intelligence features (find all references, rename symbols)
- Building custom linters, formatters, code transformation tools

**Scale:**
- Analyzing 1000s of files per repository
- Real-time analysis (as developers type)
- Multiple programming languages (Python, JavaScript, TypeScript, Rust, etc.)
- Incremental updates (re-analyze only changed regions)

**Constraints:**
- Must understand code structure (not just text)
- Performance critical (real-time or near-real-time)
- Multi-language support (not Python-only)
- Incremental parsing (don't re-parse entire file on each edit)
- Error resilience (code often incomplete while editing)

## Why They Need It

**Problem:** Text diff tools show character/line changes, not semantic changes:
- Text diff: "10 lines deleted, 10 lines added"
- Semantic diff: "Function `foo` renamed to `bar`"

**Use cases:**
- Refactoring detection: identify renames, extractions, moves
- API migration: find deprecated API calls across codebase
- Code review: show structural changes (class hierarchy, imports)
- Incremental compilation: re-compile only changed functions
- Smart diff viewing: collapse whitespace-only changes, highlight logic changes

**Requirements:**
- **MUST**: Understand code structure (AST-aware)
- **MUST**: Multi-language support (10+ languages minimum)
- **MUST**: Incremental parsing (fast re-parsing after edits)
- **MUST**: Error recovery (handle incomplete/invalid code)
- **SHOULD**: Query language (find patterns in code)
- **SHOULD**: Good performance (real-time or <1s for large files)

**Anti-Requirements:**
- Not for comparing test outputs (use difflib/DeepDiff)
- Not for data comparison (use DeepDiff for JSON/objects)
- Not for simple text diff (use difflib if structure doesn't matter)

## Library Fit Analysis

### Recommended Solution

→ **tree-sitter**

**Strengths:**
- ✅ 100+ language grammars (Python, JS, Rust, Go, C++, etc.)
- ✅ Incremental parsing (re-parse only changed regions)
- ✅ Error recovery (parses incomplete code)
- ✅ Query language (S-expressions for pattern matching)
- ✅ Fast (Rust core, C bindings)
- ✅ Very active (18k stars, 2M downloads/month)
- ✅ Used by GitHub, major IDEs (production-proven)

**Limitations:**
- ⚠️ NOT a diff tool (provides parsing infrastructure only)
- ⚠️ Steep learning curve (parsing concepts, query language)
- ⚠️ Complex integration (need to build diff logic on top)
- ⚠️ Parsing overhead (slower than text diff for large files)

**What you get:**
- Parse code into AST (abstract syntax tree)
- Query for patterns (find all functions, classes, imports)
- Incremental re-parsing (efficient for real-time editing)

**What you must build:**
- Diff algorithm for comparing trees (tree-sitter doesn't provide this)
- Logic to detect renames, moves, extractions
- Integration with your tool's workflow

### Alternative: Build on GitPython

**When GitPython is sufficient:**
- Only need line-based diff (not semantic)
- Working with git repositories (code review, CI/CD)
- Patience diff is good enough for moved blocks

**When to upgrade to tree-sitter:**
- Need true semantic understanding (renames, not just moves)
- Building IDE features (go-to-definition, find-references)
- Multi-language support required

### Anti-Patterns

**❌ DON'T use difflib/diff-match-patch:**
- No code understanding (text-only)
- Can't detect renames (sees as delete + add)
- No multi-language support

**❌ DON'T use DeepDiff:**
- For Python objects, not code parsing
- No syntax understanding

**❌ DON'T use tree-sitter for simple text diff:**
- Massive overkill if structure doesn't matter
- Slower, more complex than difflib

### Decision Factors

**Choose tree-sitter when:**
- Building semantic code analysis tools
- Need to understand code structure
- Multi-language support required
- Incremental parsing valuable (real-time tools)

**Choose GitPython when:**
- Line-based diff is sufficient
- Working with git repositories
- Don't need semantic analysis

**Choose difflib when:**
- Simple text comparison
- No code structure understanding needed
- Want minimal complexity

## Validation Criteria

**You picked the right library if:**
- ✅ Can detect renames (not just delete + add)
- ✅ Parses multiple languages (not language-specific)
- ✅ Fast enough for your use case (real-time or batch)
- ✅ Handles incomplete code (developers often save invalid syntax)
- ✅ Incremental updates work (don't re-parse entire file)

**Red flags (wrong choice):**
- ❌ Shows "100 lines changed" for simple rename
- ❌ Can't parse language you need
- ❌ Too slow for real-time (>1s for 1000-line file)
- ❌ Crashes on incomplete code (no error recovery)
- ❌ Re-parses entire file on every edit (no incremental support)

## Common Patterns

**Pattern: Semantic diff**
```
# Parse both versions
tree_old = parser.parse(code_old)
tree_new = parser.parse(code_new)

# Custom diff logic on ASTs
changed_functions = find_changed_functions(tree_old, tree_new)
renamed_classes = detect_renames(tree_old, tree_new)
```

**Pattern: Incremental parsing**
```
# Initial parse
tree = parser.parse(code)

# User edits line 50
tree.edit(start_byte, old_end_byte, new_end_byte)
tree = parser.parse(new_code, tree)  # Re-parse only affected region
```

**Pattern: Pattern matching**
```
# Find all deprecated API calls
query = """
(call_expression
  function: (identifier) @func
  (#eq? @func "deprecated_api"))
"""
matches = query.captures(tree.root_node)
```

## Real-World Example

**Scenario:** Building a refactoring tool that detects function renames across a codebase

**Requirements:**
- Analyze 1000s of Python files
- Detect when function `foo` renamed to `bar`
- Find all call sites that need updating
- Show semantic diff (rename, not delete + add)
- Fast enough for interactive use (<10s for large repo)

**Solution:** tree-sitter with custom diff logic
1. Parse all Python files with tree-sitter
2. Build symbol table (functions, classes, variables)
3. Compare ASTs to detect renames (function node changed name but body similar)
4. Query for all call sites of renamed function
5. Generate refactoring patch

**Why not difflib:** Can't detect renames, sees as delete + add

**Why not GitPython:** Line-based diff can't understand "function renamed"

**Why tree-sitter:** AST-aware, can identify symbol renames vs complete rewrites

## Learning Curve Warning

**tree-sitter is NOT plug-and-play:**
- Requires understanding parsing concepts (AST, CST, incremental parsing)
- Query language is powerful but has learning curve (S-expressions)
- Need to build diff logic yourself (tree-sitter doesn't diff trees)
- Setup complexity (grammars, build process)

**Estimate: 2-4 weeks to become productive** (vs 1-2 hours for difflib)

**Worth it if:**
- Building semantic code tools (long-term investment)
- Need multi-language support
- Performance matters (incremental parsing pays off)

**Not worth it if:**
- One-off analysis (use GitPython or difflib)
- Single language (language-specific parser might be simpler)
- Don't need semantic understanding (line diff is sufficient)
