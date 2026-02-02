# tree-sitter

## Overview
- **Package**: tree-sitter (PyPI), py-tree-sitter (Python bindings)
- **Status**: Very active (frequent releases, growing ecosystem)
- **Popularity**: ~18k GitHub stars, ~2M PyPI downloads/month
- **Scope**: Parsing library (provides infrastructure for semantic diff, not diff itself)

## Algorithm
- **Core**: Incremental GLR parser (not a diff algorithm)
- **Tree-based**: Parses code into AST (abstract syntax tree)
- **Semantic understanding**: Knows functions, classes, variables (not just text)
- **Incremental**: Re-parses only changed regions (fast updates)
- **Error recovery**: Handles incomplete/invalid code gracefully

## Best For
- **Semantic code diff**: Understanding what changed structurally (function renamed, class moved)
- **Refactoring detection**: Identifying renames, extractions, moved blocks
- **Code search**: Finding patterns in syntax trees (not text)
- **Language-aware tools**: Building linters, formatters, code analysis
- **Multi-language support**: 100+ language grammars available

## Trade-offs

**Strengths:**
- Understands code structure (not just character sequences)
- 100+ languages supported (Python, JS, Rust, Go, C++, etc.)
- Incremental parsing (efficient for real-time editing)
- Error recovery (works with incomplete code)
- Query language (S-expressions for pattern matching)
- Very active ecosystem (growing, well-maintained)

**Limitations:**
- NOT a diff library (parsing only - you build diff on top)
- Steep learning curve (parsing concepts, query language)
- Slow for large files (parsing overhead)
- High memory usage (stores full parse tree)
- Requires language grammars (per-language setup)
- Complex integration (not drop-in replacement for difflib)

## Ecosystem Fit
- **Dependencies**: Rust toolchain (for grammar compilation), language grammars
- **Platform**: All (with build tools)
- **Python**: 3.6+
- **Maintenance**: Very active (core project + grammars)
- **Risk**: Low (used by GitHub, major IDEs)

## Quick Verdict
**NOT a simple diff replacement** - this is for building semantic code analysis tools. Choose this if you need to understand code structure changes (renames, moves, refactorings), not just text differences. Requires significant investment to use effectively.
