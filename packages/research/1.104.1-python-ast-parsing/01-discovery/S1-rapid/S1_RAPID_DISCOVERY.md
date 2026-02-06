# S1 Rapid Discovery: Python AST & Code Parsing Libraries

**Research ID**: 1.104.1 - Python AST/Code Parsing Libraries
**Phase**: S1 Rapid Discovery
**Date**: November 7, 2025
**Status**: Complete

## Executive Summary

After comprehensive research into 6 Python AST/code parsing libraries, **LibCST emerges as the clear frontrunner** for code modification use cases requiring formatting preservation, followed by Python's stdlib ast module and Rope as viable alternatives.

### Top 3 Candidates Identified:

1. **LibCST** (Instagram/Meta) - Industry-standard CST with formatting preservation, actively maintained, production-proven
2. **ast** (Python stdlib) - Built-in, zero-dependency, fast, but lacks formatting preservation (critical limitation)
3. **Rope** (python-rope) - Mature refactoring library with extensive APIs, but higher complexity/learning curve

### Key Decision Factors:
- **Formatting Preservation** (30% weight): Only LibCST, RedBaron, and Bowler fully preserve formatting; ast fails this critical requirement
- **Active Maintenance**: LibCST, ast, and Rope are actively maintained; RedBaron and Bowler are dead/archived
- **Production Readiness**: LibCST used by Instagram, Instawork, SeatGeek; Rope used in PyCharm, VS Code

---

## Library Profiles

### 1. ast (Python Standard Library)

#### Maintenance Status
- **Status**: Actively maintained (part of CPython)
- **Last Update**: Continuous (Python 3.14 support in 2025)
- **Python Version Support**: All Python versions (built-in)
- **License**: Python Software Foundation License (PSF)

#### GitHub/Community Metrics
- **Stars**: N/A (stdlib)
- **Contributors**: CPython core team
- **Activity**: Continuous integration with Python releases
- **Documentation**: Official Python docs + Green Tree Snakes external guide

#### Key Capabilities

**Formatting Preservation**: **NO - CRITICAL LIMITATION**
- Discards comments completely
- Discards whitespace (reduced to INDENT/DEDENT tokens)
- Cannot round-trip: `ast.unparse()` treats indent as exactly 4 spaces
- "Like a JPEG, the Abstract Syntax Tree is lossy"

**Modification APIs**: **YES** (25% weight)
- `ast.NodeTransformer` - Base class for tree transformations
- `ast.NodeVisitor` - Base class for visiting nodes
- `ast.parse()` / `ast.unparse()` (Python 3.9+) - Parse/generate code
- `ast.literal_eval()` - Safe evaluation of literals

**Performance**:
- Extremely fast (native C implementation)
- No benchmarks needed - built into interpreter
- Used by Python itself for compilation

**Error Handling**:
- Raises `SyntaxError` for invalid Python
- No error recovery - fails on first syntax error
- `ast.literal_eval()` limited to simple expressions

#### Documentation Quality
- **Official Docs**: Excellent (docs.python.org/3/library/ast.html)
- **Tutorial Quality**: Good - Green Tree Snakes provides comprehensive external guide
- **API Reference**: Complete and authoritative
- **Code Examples**: Abundant (Stack Overflow, tutorials, books)

#### "Hello World" Assessment

**Basic Usage Complexity**: LOW
```python
import ast

# Parse a file
with open('models.py', 'r') as f:
    tree = ast.parse(f.read())

# Find class definitions
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        print(f"Found class: {node.name}")

# Modify tree
class AddLogging(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Insert logging at start of function
        log_stmt = ast.Expr(value=ast.Call(
            func=ast.Name(id='print', ctx=ast.Load()),
            args=[ast.Constant(value=f"Entering {node.name}")],
            keywords=[]
        ))
        node.body.insert(0, log_stmt)
        return node

# Generate code (Python 3.9+)
new_code = ast.unparse(tree)
```

**Ease of Finding Class Definition**: EASY
- Simple tree walking with `ast.walk()`
- Direct `isinstance(node, ast.ClassDef)` checks
- Well-documented node types

#### Pros
- Zero dependencies (stdlib)
- Extremely fast (native implementation)
- Battle-tested and stable
- Excellent documentation
- Simple, well-understood API
- Universal availability

#### Cons
- **CRITICAL**: Cannot preserve formatting or comments
- No error recovery (fails on syntax errors)
- No round-trip guarantee for whitespace
- `ast.unparse()` only available in Python 3.9+
- Not designed for source-to-source transformations

#### Quick Verdict
**Viable for read-only analysis, UNSUITABLE for code modification** due to formatting preservation failure. Would work if we're willing to reformat all modified files, but this violates our requirement to preserve formatting. Consider only if LibCST proves inadequate.

**Score**: 6/10 (would be 9/10 if formatting preservation wasn't required)

---

### 2. libcst (Instagram/Meta, ~1.8k stars)

#### Maintenance Status
- **Status**: ACTIVELY MAINTAINED
- **Last Update**: Continuous throughout 2025 (issues opened Oct, Aug, Jul, Jun, May, Jan 2025)
- **Recent Releases**: v1.8.6 (latest), v1.2.0, v1.1.0
- **Python Version Support**: Python 3.9+ runtime, parses Python 3.0-3.14
- **License**: MIT (with some PSF-licensed stdlib-derived files)

#### GitHub/Community Metrics
- **Stars**: 1,780 (also reported as 4.8k in some sources - verify)
- **Forks**: 220
- **Watchers**: 40
- **Contributors**: 98
- **Weekly Downloads**: 3,137,908 (PyPI)
- **Dependent Packages**: 409 packages, 214 repositories
- **Classification**: "Key ecosystem project"

#### Key Capabilities

**Formatting Preservation**: **YES - EXCELLENT** (30% weight)
- Preserves ALL formatting details: comments, whitespace, parentheses
- Concrete Syntax Tree (CST) - lossless representation
- Guarantees round-trip: `parse(code) -> modify -> unparse() == original_code` (with modifications)
- "Looks like AST, preserves like CST" - compromise design

**Modification APIs**: **YES - COMPREHENSIVE** (25% weight)
- Visitor pattern (`cst.CSTVisitor` for analysis)
- Transformer pattern (`cst.CSTTransformer` for modifications)
- Codemod framework (high-level batch transformations)
- `module.with_changes()` - Immutable tree modifications
- Metadata wrappers for scope analysis

**Performance**:
- **Native Rust parser** for speed (requires `cargo` for source builds)
- Binary wheels distributed (no build needed for installation)
- Goal: Within 2x CPython performance
- Works on `Vec<Token>` references (zero-copy where possible)
- Suitable for IDE/interactive use cases

**Error Handling**:
- Depends on parso for parsing (parso has error recovery)
- Note: Parso itself has fallen behind on Python version support (match keyword unimplemented)
- LibCST has worked around parso limitations to support Python 3.14

#### Documentation Quality
- **Official Docs**: EXCELLENT (libcst.readthedocs.io)
- **Tutorial Quality**: EXCELLENT
  - Step-by-step tutorial (parse -> display -> transform -> generate)
  - Codemods tutorial for batch transformations
  - Best practices guide
  - Interactive Jupyter notebook examples
- **API Reference**: Complete and well-organized
- **Code Examples**: Abundant
  - Official examples in repo
  - Real-world case studies (Instawork, SeatGeek blog posts)
  - Stack Overflow has growing community

#### Production Users (Documented)
- **Instagram/Meta**: Core of linting and automated refactoring tools (massive Python codebase)
- **Instawork**: Primary codemod library
- **SeatGeek**: Large-scale internal commerce service refactoring
- **bump-pydantic**: Pydantic v1→v2 migration tool
- **micropython-stubber**: Stub generation and merging

#### "Hello World" Assessment

**Basic Usage Complexity**: MEDIUM
```python
import libcst as cst

# Parse a file
with open('models.py', 'r') as f:
    source_tree = cst.parse_module(f.read())

# Find class definitions - Visitor pattern
class ClassFinder(cst.CSTVisitor):
    def visit_ClassDef(self, node):
        print(f"Found class: {node.name.value}")

source_tree.walk(ClassFinder())

# Modify code - Transformer pattern
class AddImport(cst.CSTTransformer):
    def leave_Module(self, original_node, updated_node):
        # Add import at top
        new_import = cst.SimpleStatementLine(
            body=[cst.Import(names=[cst.ImportAlias(name=cst.Attribute(...))])]
        )
        return updated_node.with_changes(
            body=[new_import] + list(updated_node.body)
        )

modified_tree = source_tree.visit(AddImport())
print(modified_tree.code)  # Preserves all original formatting
```

**Ease of Finding Class Definition**: MEDIUM
- Requires visitor pattern understanding
- More boilerplate than ast
- Node structure similar to ast (easy transition)
- Type hints help with autocomplete

#### Pros
- **Formatting preservation is perfect** (critical requirement met)
- Actively maintained by Meta/Instagram
- Production-proven at massive scale
- Excellent documentation with real-world examples
- Rust-native parser for performance
- Supports latest Python (3.14)
- MIT licensed
- Growing ecosystem (409 dependent packages)
- Codemod framework for batch operations

#### Cons
- More complex API than ast (visitor/transformer pattern required)
- Requires Python 3.9+ runtime
- Dependency on parso (though abstracted away)
- Slightly verbose for simple modifications
- Learning curve steeper than ast
- Binary dependency (Rust build tools for source installs)

#### Quick Verdict
**RECOMMENDED - Top Choice**. LibCST is the industry standard for Python code transformation with formatting preservation. Proven at scale, actively maintained, comprehensive documentation. The API complexity is justified by the power and correctness guarantees. Ideal for automated refactoring, code generation, and any source-to-source transformation requiring format preservation.

**Score**: 9.5/10

---

### 3. redbaron (PyCQA, ~1.2k stars)

#### Maintenance Status
- **Status**: INACTIVE / ABANDONED
- **Last Update**: No new PyPI versions in 12+ months
- **Python Version Support**: Python 2 + Python 3.0-3.7 only (3.7 EOL: June 2023)
- **License**: LGPL
- **Contributor Confirmation**: "This project is not actively updated"

#### GitHub/Community Metrics
- **Stars**: ~1,200
- **Activity**: No recent PRs or issue activity
- **Classification**: Snyk labels it as "Inactive project"
- **Community Sentiment**: Users migrating to LibCST

#### Key Capabilities

**Formatting Preservation**: **YES** (based on Baron FST)
- Built on Baron - lossless FST (Full Syntax Tree)
- Guarantees: `ast_to_code(code_to_ast(source)) == source`

**Modification APIs**: **YES** (designed for easy modifications)
- Simple, Pythonic API
- "As easy as possible" - original design goal
- Bottom-up refactoring approach

**Performance**: Unknown (no benchmarks found)

**Error Handling**: Limited information available

#### Documentation Quality
- **Official Docs**: ReadTheDocs (redbaron.readthedocs.io)
- **Tutorial Quality**: Basic tutorial exists
- **API Reference**: Documented but outdated
- **Code Examples**: Limited, aging

#### "Hello World" Assessment
**Basic Usage Complexity**: Likely LOW (designed for simplicity)
- Pythonic, simple API per design goals
- But: Outdated, broken parsing issues reported

#### Pros
- Simple API (if it worked)
- Designed specifically for easy code modification
- LGPL license

#### Cons
- **DEAL-BREAKER**: Abandoned / inactive maintenance
- **CRITICAL**: Only supports Python 3.7 (EOL June 2023)
- "Woefully broken and largely unmaintained"
- "Incomplete tests, PRs going months without response"
- "Basic source code parsing issues"
- No Python 3.8+ support (no async/await, walrus operator, etc.)

#### Quick Verdict
**ELIMINATED - DO NOT USE**. While RedBaron had the right idea (simple API + formatting preservation), it's abandoned and only supports Python 3.7. Migration path is LibCST.

**Score**: 2/10 (concept was good, execution and maintenance failed)

---

### 4. rope (python-rope, ~2.1k stars)

#### Maintenance Status
- **Status**: ACTIVELY MAINTAINED
- **Latest Release**: v1.14.0 (July 12, 2025)
- **Active Maintainer**: Lie Ryan (@lieryan)
- **Python Version Support**:
  - Runtime: Python 3.8, 3.9, 3.10, 3.11, 3.12
  - Syntax: Python 3.10 and below (3.11/3.12 syntax not fully supported yet)
- **License**: LGPL
- **Activity**: 170 contributors, 108 open issues, commits in past year

#### GitHub/Community Metrics
- **Stars**: ~2,100
- **Forks**: Active
- **Classification**: "World's most advanced open source Python refactoring library"
- **Integration**: Used in IDEs (PyCharm, VS Code via pylsp-rope)

#### Key Capabilities

**Formatting Preservation**: **YES** (via annotations)
- Uses "region" annotations on AST nodes
- Tracks first/last character positions for each node
- Preserves code structure during refactoring operations

**Modification APIs**: **YES - EXTENSIVE** (25% weight)
- `rope.refactor.rename` - Rename refactoring
- `rope.refactor.restructure` - Pattern-based restructuring
- `rope.refactor.introduce_factory` - Factory pattern refactoring
- `rope.refactor.introduce_parameter` - Parameter introduction
- `rope.refactor.encapsulate_field` - Getter/setter generation
- `rope.base.libutils` - Helper functions for tool building
- Project-based API (requires `rope.base.project.Project`)

**Performance**: No specific benchmarks found
- Focused on correctness over raw speed
- Project-based analysis (indexes codebases)

**Error Handling**:
- Robust refactoring validation
- Rollback capabilities
- Project state management

#### Documentation Quality
- **Official Docs**: Good (rope.readthedocs.io)
- **Tutorial Quality**: FAIR - more reference than tutorial
- **API Reference**: Complete but technical
- **Code Examples**: Available in docs and test suites
  - Restructure example: `pow(x, y)` → `x ** y`
  - Rename example provided
  - Examples found primarily in test suite

#### Production Users
- **PyCharm**: Uses rope for refactoring
- **VS Code**: Via pylsp-rope plugin
- **Emacs**: Via ropemacs
- **Vim**: Via ropevim
- Widespread IDE integration

#### "Hello World" Assessment

**Basic Usage Complexity**: MEDIUM-HIGH
```python
from rope.base.project import Project
from rope.refactor.rename import Rename
from rope.refactor import restructure

# Setup - requires Project concept
project = Project('.')

# Example 1: Renaming
change = Rename(project, resource).get_changes("new_name")
project.do(change)

# Example 2: Restructure (pattern-based transformation)
pattern = '${pow_func}(${param1}, ${param2})'
goal = '${param1} ** ${param2}'
args = {'pow_func': 'name=mod1.pow'}

restructuring = restructure.Restructure(project, pattern, goal, args)
project.do(restructuring.get_changes())

# Cleanup
project.close()
```

**Ease of Finding Class Definition**: MEDIUM
- Requires understanding project/resource model
- More abstraction layers than direct AST walking
- Focused on refactoring operations, not tree inspection

#### Pros
- Most comprehensive refactoring APIs
- Battle-tested (20+ years old)
- IDE integration proven
- Active maintenance (v1.14.0 in July 2025)
- Robust validation and safety features
- Project-aware (understands imports, scoping)

#### Cons
- **Syntax support lag**: Only Python 3.10 syntax (runs on 3.12, but doesn't parse 3.11/3.12 features)
- High complexity / learning curve
- Project-based model adds overhead
- LGPL license (more restrictive than MIT)
- Heavy-weight for simple AST operations
- Limited documentation for library usage (better for IDE integration)
- Focused on high-level refactorings, not low-level AST manipulation

#### Quick Verdict
**VIABLE - Specialized Use Case**. Rope excels at complex, project-wide refactorings (rename across files, extract method, etc.) but is overkill for simple file-level AST modifications. Consider if we need full refactoring capabilities. Otherwise, LibCST is simpler and more direct for our use case.

**Score**: 7/10 (would be 8.5/10 for complex refactoring needs)

---

### 5. parso (davidhalter, ~654 stars)

#### Maintenance Status
- **Status**: MAINTAINED (but activity unclear)
- **Last Update**: Recent maintenance detected (healthy version release cadence)
- **Python Version Support**: Parser for multiple Python versions
- **License**: MIT/Apache (dual licensed)
- **Relationship**: Originally part of Jedi, now separate; used as LibCST's parser

#### GitHub/Community Metrics
- **Stars**: 654
- **Weekly Downloads**: 11,071,121 (extremely high - dependency of many tools)
- **Classification**: "Key ecosystem project"
- **Activity**: No PR/issue activity detected in past month, but commits in 2021 included Python 3.10 fixes

#### Key Capabilities

**Formatting Preservation**: **YES** (Full Syntax Tree)
- Error-tolerant parser
- Round-trip parsing support
- Used by LibCST for parsing layer

**Modification APIs**: **LIMITED**
- Primarily a parser, not a modification library
- Provides tree structure, but limited transformation helpers
- Designed for consumption by other tools (Jedi, LibCST)

**Performance**:
- LL(1) parsing approach
- No specific benchmarks found

**Error Handling**: **EXCELLENT**
- Error recovery is a core feature
- Can list multiple syntax errors
- Continues parsing after errors (critical for IDE use)

#### Documentation Quality
- **Official Docs**: Basic (parso.readthedocs.io)
- **Tutorial Quality**: MINIMAL - primarily API reference
- **API Reference**: Basic
- **Code Examples**: Limited

#### "Hello World" Assessment
**Basic Usage Complexity**: MEDIUM
- Primarily used as a library by other tools
- Not designed for end-user tree manipulation
- Better to use Jedi or LibCST built on top

#### Pros
- Error-tolerant (great for IDE use)
- Battle-tested (via Jedi)
- High download count shows ecosystem importance
- Multi-version Python support

#### Cons
- **Parser has fallen behind**: Python 3.11+ `match` keyword unimplemented
- Limited modification APIs (parsing focus)
- Minimal documentation
- Better used via LibCST than directly
- Not designed for standalone use
- Primarily an internal library

#### Quick Verdict
**ELIMINATED - Use LibCST Instead**. Parso is the parsing engine underneath LibCST, but LibCST provides the modification APIs we need. Using parso directly would require building our own transformation layer. No advantage over LibCST.

**Score**: 5/10 (as a parser: 8/10, as a modification tool: 3/10)

---

### 6. bowler (Facebook, ~1.5k stars)

#### Maintenance Status
- **Status**: ARCHIVED / DEAD
- **Archived Date**: August 8, 2025
- **Repository**: Read-only (facebookincubator/Bowler)
- **Last Updates**: No PyPI releases in 12+ months
- **Activity**: No PR/issue activity detected
- **Classification**: "Inactive project"

#### GitHub/Community Metrics
- **Stars**: ~1,500
- **Status**: Archived by owner, read-only
- **Activity**: None (archived)

#### Key Capabilities (Historical)

**Formatting Preservation**: **YES** (via lib2to3/fissix, planned LibCST)
- Bowler 0.x: Based on fissix (lib2to3 fork)
- Bowler 2.x (never released): Planned to use LibCST

**Modification APIs**: **YES** (Fluent Query API)
- Simple command-line interface
- Fluent Query API for building refactoring scripts
- Selectors, filters, modifiers

**Note from Project**: "Look at LibCST codemods which are a bit more verbose, but work well on modern python grammars"

#### Documentation Quality
- **Official Docs**: Still accessible (pybowler.io, GitHub docs)
- **Tutorial Quality**: Good (basics-refactoring.md)
- **Note**: Documentation is frozen (archived repo)

#### "Hello World" Assessment
**Basic Usage Complexity**: LOW (was designed for simplicity)
- Fluent API was very readable
- But: Project recommends LibCST now

#### Pros (Historical)
- Simple, fluent API
- Facebook engineering pedigree
- Good documentation (while active)

#### Cons
- **DEAL-BREAKER**: Archived August 8, 2025
- Inactive for 12+ months before archival
- Based on lib2to3/fissix (deprecated)
- Project itself recommends LibCST
- No future development

#### Quick Verdict
**ELIMINATED - PROJECT DEAD**. Facebook archived Bowler and recommends LibCST. Even the Bowler team planned to rebuild on LibCST (Bowler 2.x). Clear migration path: use LibCST directly.

**Score**: 3/10 (concept was good, but deprecated in favor of LibCST)

---

## Comparison Matrix

| Library | Stars | Last Update | Formatting | Modification | Python Support | Docs | Active | Verdict |
|---------|-------|-------------|------------|--------------|----------------|------|--------|---------|
| **libcst** | 1,780 | Oct 2025 | ✅ Excellent | ✅ Comprehensive | 3.9+ runtime, 3.0-3.14 parse | ✅ Excellent | ✅ Active | **RECOMMENDED** |
| **ast** | N/A (stdlib) | Continuous | ❌ None | ✅ Good | All (stdlib) | ✅ Excellent | ✅ Active | Consider (no formatting) |
| **rope** | 2,100 | Jul 2025 | ✅ Good | ✅ Extensive | 3.8-3.12 runtime, 3.10 parse | ⚠️ Fair | ✅ Active | Viable (complex) |
| **parso** | 654 | 2024 | ✅ Good | ❌ Limited | Multi-version | ⚠️ Minimal | ⚠️ Unclear | Eliminated (use LibCST) |
| **redbaron** | 1,200 | 2023+ | ✅ Yes | ✅ Yes | 3.7 only | ⚠️ Outdated | ❌ Abandoned | **ELIMINATED** |
| **bowler** | 1,500 | Archived 2025 | ✅ Yes (lib2to3) | ✅ Yes | Legacy | ⚠️ Frozen | ❌ Archived | **ELIMINATED** |

### Scoring Breakdown (out of 10)

| Library | Formatting (30%) | Modification (25%) | Maintenance (20%) | Docs (15%) | Ease of Use (10%) | **TOTAL** |
|---------|------------------|-------------------|-------------------|------------|-------------------|-----------|
| **libcst** | 3.0 | 2.5 | 2.0 | 1.5 | 0.5 | **9.5** |
| **ast** | 0.0 | 2.0 | 2.0 | 1.5 | 1.0 | **6.5** |
| **rope** | 2.5 | 2.5 | 1.5 | 0.8 | 0.2 | **7.5** |
| **parso** | 2.5 | 0.5 | 1.0 | 0.3 | 0.5 | **4.8** |
| **redbaron** | 3.0 | 2.0 | 0.0 | 0.5 | 0.8 | **6.3** (DEAD) |
| **bowler** | 2.5 | 2.0 | 0.0 | 1.0 | 0.8 | **6.3** (ARCHIVED) |

---

## Top 3 Candidates

### 1. LibCST (Instagram/Meta) - RECOMMENDED

**Rationale**:
- **Perfect formatting preservation** - The only actively-maintained library that fully meets our critical requirement
- **Production-proven at massive scale** - Instagram's entire Python codebase, Instawork, SeatGeek
- **Excellent documentation** - Tutorials, real-world examples, best practices
- **Active development** - Continuous updates through 2025, Python 3.14 support
- **Strong ecosystem** - 409 dependent packages, growing community
- **Rust-native performance** - Fast enough for IDE/interactive use
- **Comprehensive APIs** - Visitor/Transformer patterns, Codemod framework

**Best For**:
- Source-to-source transformations with formatting preservation (our exact use case)
- Automated refactoring (codemods)
- Linting and static analysis with modifications
- Any tool that modifies Python code and needs to preserve developer intent

**Use LibCST When**:
- ✅ You need to modify Python code while preserving formatting/comments
- ✅ You're building automated refactoring tools
- ✅ You need production-grade reliability
- ✅ Python 3.9+ runtime is acceptable

### 2. ast (Python Standard Library) - FALLBACK OPTION

**Rationale**:
- **Zero dependencies** - Always available, no installation needed
- **Battle-tested** - Core Python infrastructure
- **Excellent performance** - Native C implementation
- **Simple API** - Lower learning curve than LibCST
- **Universal compatibility** - Works with all Python versions
- **Critical Limitation**: Cannot preserve formatting (30% requirement weight = automatic disqualification for primary choice)

**Best For**:
- Read-only AST analysis
- Code generation (where formatting doesn't matter)
- Quick scripts and prototypes
- Projects that auto-format with Black/autopep8 anyway

**Use ast When**:
- ✅ You only need to analyze code (not modify)
- ✅ You're generating new code (no preservation needed)
- ✅ You're okay with reformatting modified files
- ❌ You need to preserve comments/formatting (use LibCST)

### 3. Rope (python-rope) - SPECIALIZED OPTION

**Rationale**:
- **Most comprehensive refactoring APIs** - Rename, restructure, extract, encapsulate
- **Project-aware** - Understands imports, scoping across multiple files
- **IDE-proven** - Used by PyCharm, VS Code, Emacs, Vim
- **Robust validation** - Refactoring safety checks
- **Trade-offs**: High complexity, LGPL license, Python 3.10 syntax only

**Best For**:
- Complex, project-wide refactorings (rename across files, extract method)
- IDE integration
- Advanced refactoring operations beyond simple AST modifications

**Use Rope When**:
- ✅ You need cross-file refactoring (rename across project)
- ✅ You need high-level refactoring operations (extract method, introduce parameter)
- ✅ LGPL license is acceptable
- ❌ You need simple file-level modifications (use LibCST - simpler)
- ❌ You need Python 3.11+ syntax support (not yet available)

---

## Eliminated Candidates

### RedBaron
**Elimination Reason**: Abandoned project, Python 3.7 only (EOL June 2023)
- No maintenance since 2023+
- Cannot parse modern Python (no async/await improvements, walrus operator, match statements, etc.)
- "Woefully broken" according to community reports
- **Migration Path**: LibCST is the direct replacement

### Bowler
**Elimination Reason**: Archived August 8, 2025
- Repository is read-only
- Facebook recommends using LibCST instead
- Bowler 2.x was planned to rebuild on LibCST (never happened)
- **Migration Path**: LibCST (as recommended by Bowler team)

### Parso
**Elimination Reason**: Parser library, not a modification library
- Designed as a dependency for other tools (Jedi, LibCST)
- Limited modification APIs
- Better to use LibCST which builds on parso
- Python 3.11+ syntax support incomplete (match keyword missing)
- **Migration Path**: Use LibCST or Jedi (both build on parso)

---

## Key Findings & Insights

### Surprising Findings

1. **LibCST is built on parso**: Despite parso falling behind on Python version support, LibCST has worked around limitations to support Python 3.14. This shows strong engineering from Meta/Instagram team.

2. **Bowler was deprecated in favor of LibCST**: Even Facebook's own refactoring tool (Bowler) was archived with a recommendation to use LibCST. This is a strong endorsement.

3. **ast module cannot preserve formatting at all**: This is well-documented but bears repeating - the stdlib ast is fundamentally lossy and unsuitable for source-to-source transformations where formatting matters.

4. **Rope supports Python 3.12 runtime but only Python 3.10 syntax**: This creates a disconnect where you can run rope on Python 3.12, but it won't parse 3.11/3.12-specific syntax. Important limitation for modern codebases.

5. **LibCST has massive adoption**: 3.1M weekly downloads, 409 dependent packages, classified as "key ecosystem project". Far beyond what GitHub stars suggest.

6. **RedBaron's demise**: Once a popular choice, now completely abandoned. Serves as a reminder to check maintenance status.

### Key Differentiators

| Aspect | LibCST | ast | Rope |
|--------|--------|-----|------|
| **Primary Use Case** | Source transformation | AST analysis | IDE refactoring |
| **Formatting** | Perfect preservation | None | Good preservation |
| **API Complexity** | Medium (visitor/transformer) | Low (simple traversal) | High (project model) |
| **Scope** | File-level modifications | Single-file analysis | Project-wide refactoring |
| **Performance** | Fast (Rust parser) | Fastest (C native) | Moderate (project indexing) |
| **Dependencies** | parso + Rust native | None (stdlib) | Various |
| **License** | MIT | PSF | LGPL |
| **Maintenance** | Very active (Meta) | Continuous (CPython) | Active (community) |

### Critical Decision Points

**Generic Use Case Evaluation**:

1. **Formatting preservation required** (30% weight)
   - **LibCST**: ✅ Perfect (CST design)
   - **ast**: ❌ None (lossy AST)
   - **Rope**: ✅ Good (region annotations)

2. **Code modification capabilities** (25% weight)
   - **LibCST**: ✅ Comprehensive (visitor/transformer patterns)
   - **ast**: ✅ Basic (NodeTransformer)
   - **Rope**: ✅ Extensive (refactoring operations)

3. **Active maintenance** (20% weight)
   - **LibCST**: ✅ Very active (Meta/Instagram)
   - **ast**: ✅ Continuous (CPython core)
   - **Rope**: ✅ Active (community-maintained)

4. **Ease of use** (10% weight)
   - **LibCST**: ⚠️ Medium complexity
   - **ast**: ✅ Simple API
   - **Rope**: ❌ High complexity (project model)

**Result**: LibCST scores 9.5/10 for formatting-preserving code modification use cases.

---

## Conclusion

**LibCST is the clear leader** for Python code modification use cases requiring formatting preservation. It's the only actively-maintained library that perfectly preserves formatting while providing comprehensive modification APIs. Production-proven at Instagram's massive scale, excellent documentation, and active development make it a safe choice.

**ast module** remains viable for read-only analysis or use cases where reformatting is acceptable.

**Rope** is specialized for IDE-level, project-wide refactoring operations.

**Next Steps**:
1. Proceed to S2 Comprehensive Discovery (deep research on documentation, APIs, case studies)
2. S3 Need-Driven Discovery (match libraries to generic use case patterns)
3. S4 Strategic Discovery (long-term viability, Python version support roadmap)

**Application-Specific Validation**: See `02-implementations/validation-plan.md` for hands-on testing plan (application-specific, not generic research).

---

**Research Completed**: November 7, 2025
**Status**: S1 Complete - Ready for S2-S4
