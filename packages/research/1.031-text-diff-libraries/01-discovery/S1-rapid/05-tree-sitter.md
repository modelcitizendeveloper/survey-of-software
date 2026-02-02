# tree-sitter

## Overview
**Package:** `tree-sitter`
**Algorithm:** Parse tree construction + tree diff
**Status:** Very active
**Author:** Max Brunsfeld (GitHub)
**First Released:** 2017
**Language:** Rust with bindings for Python, JavaScript, C, etc.

## Description
A parser generator and incremental parsing library that builds concrete syntax trees for source code. While not strictly a "diff library," tree-sitter enables **structural diffing** by comparing parse trees instead of raw text. This allows semantic understanding of code changes.

**Key features:**
- **Language-agnostic parsing**: Grammar files for 100+ languages
- **Incremental parsing**: Fast re-parsing after edits
- **Concrete syntax tree**: Preserves all source information (comments, whitespace)
- **Error recovery**: Can parse incomplete/invalid code
- **Query language**: Find patterns in code (S-expressions)
- **Tree editing**: Apply edits and re-parse efficiently

## Use Cases
- **Semantic diff**: Understand code structure changes (not just text)
- **Code navigation**: Jump to definition, find references
- **Syntax highlighting**: Fast, accurate highlighting for editors
- **Code analysis**: Static analysis without full AST
- **Refactoring tools**: Detect renamed functions, moved classes
- **Code search**: Find structural patterns (e.g., all function calls)

## Structural Diff Concept
Traditional diff: "deleted 10 lines, added 12 lines"
Tree-sitter diff: "renamed function `foo` to `bar`, moved class `Baz` to new file"

By comparing parse trees, you can detect:
- **Renamed identifiers**: Same structure, different names
- **Moved code**: Same subtree, different location
- **Refactorings**: Extract method, inline variable, etc.
- **Semantic equivalence**: Different syntax, same meaning

## Installation
```bash
# Core library
pip install tree-sitter

# Language grammars (install separately)
pip install tree-sitter-python
pip install tree-sitter-javascript
# ... etc for other languages
```

## Basic Usage

### Parse Python code
```python
from tree_sitter import Language, Parser
import tree_sitter_python

# Build language
PY_LANGUAGE = Language(tree_sitter_python.language())

# Create parser
parser = Parser()
parser.set_language(PY_LANGUAGE)

# Parse code
code = b"""
def hello(name):
    print(f"Hello, {name}!")
"""

tree = parser.parse(code)
root = tree.root_node

# Print tree structure
print(root.sexp())
```

Output (simplified):
```lisp
(module
  (function_definition
    name: (identifier)
    parameters: (parameters (identifier))
    body: (block
      (expression_statement
        (call
          function: (identifier)
          arguments: (argument_list (string)))))))
```

### Find all function definitions
```python
from tree_sitter import Language, Parser
import tree_sitter_python

PY_LANGUAGE = Language(tree_sitter_python.language())
parser = Parser()
parser.set_language(PY_LANGUAGE)

code = b"""
def foo():
    pass

def bar(x, y):
    return x + y
"""

tree = parser.parse(code)

# Query for function definitions
query = PY_LANGUAGE.query("""
(function_definition
  name: (identifier) @function.name)
""")

captures = query.captures(tree.root_node)
for node, capture_name in captures:
    print(f"Found function: {node.text.decode()}")
```

Output:
```
Found function: foo
Found function: bar
```

### Structural diff (conceptual)
```python
from tree_sitter import Language, Parser
import tree_sitter_python

PY_LANGUAGE = Language(tree_sitter_python.language())
parser = Parser()
parser.set_language(PY_LANGUAGE)

code1 = b"def foo(x): return x + 1"
code2 = b"def bar(x): return x + 1"

tree1 = parser.parse(code1)
tree2 = parser.parse(code2)

# Compare trees (simplified - real implementation would be more complex)
# This is conceptual - tree-sitter doesn't have built-in tree diff
def tree_diff(node1, node2):
    if node1.type != node2.type:
        return "Node type changed"
    if node1.text != node2.text:
        return f"Text changed: {node1.text} -> {node2.text}"
    # Recursively compare children...

# Real semantic diff tools (difftastic, etc.) use tree-sitter for parsing,
# then implement custom tree diff algorithms
```

## Pros
- **Semantic understanding**: Knows what code constructs are, not just text
- **Language-agnostic**: 100+ language grammars (Python, JS, Rust, Go, etc.)
- **Incremental parsing**: Fast updates after edits
- **Error tolerant**: Can parse incomplete code
- **Query language**: Powerful pattern matching
- **Active ecosystem**: Used by GitHub, Neovim, Emacs, etc.

## Cons
- **Not a diff tool**: Provides parsing, not diffing (need to build diff on top)
- **Complexity**: Steeper learning curve than text diff
- **Grammar maintenance**: Each language needs a maintained grammar
- **Performance**: Slower than simple text diff for small changes
- **Memory usage**: Parse trees can be large for big files

## Structural Diff Tools Built on tree-sitter
- **difftastic**: Rust CLI tool for structural diff (highly recommended)
- **tree-sitter-graph**: Query language for code navigation
- **semantic-diff (GitHub)**: GitHub's internal semantic diff tool

## When to Use
- **Refactoring detection**: Identify renamed/moved code
- **Code review**: Show meaningful changes (not formatting)
- **Static analysis**: Parse code without full compiler
- **Editor features**: Syntax highlighting, code folding, navigation
- **Code search**: Find structural patterns across projects

## When NOT to Use
- **Simple text diff**: Overkill for non-code files
- **Performance-critical diff**: Slower than Myers/patience for text
- **No language grammar**: If your language isn't supported
- **Quick prototyping**: More setup than `difflib`

## Integration with Diff Tools
```python
# Conceptual workflow:
# 1. Parse both versions with tree-sitter
tree1 = parser.parse(code1)
tree2 = parser.parse(code2)

# 2. Use a tree diff algorithm (e.g., GumTree, difftastic)
# (Not built into tree-sitter - requires external tool)

# 3. Interpret diff semantically
# "function foo renamed to bar" vs "10 lines changed"
```

## Popularity
- **GitHub stars:** ~18k (tree-sitter core)
- **PyPI downloads:** ~2M/month (tree-sitter), ~200k/month (tree-sitter-python)
- **Adoption:** GitHub, Neovim, Emacs, Atom, Zed, many LSP servers

## Real-World Usage
- **GitHub Code Navigation**: Powered by tree-sitter
- **Neovim**: Syntax highlighting and code navigation
- **difftastic**: Structural diff CLI tool
- **Semgrep**: Code analysis and pattern matching

## Verdict
**Best for:** Semantic/structural diffing of code where you need to understand refactorings, not just line changes. Essential for modern editor features and code intelligence.

**Skip if:** You need simple text diff, don't want to build diff logic on top of parsing, or your language isn't supported.

**Note:** tree-sitter provides parsing, not diffing. For actual structural diff, use tools like **difftastic** (Rust CLI) or build custom logic on tree-sitter's parse trees.
