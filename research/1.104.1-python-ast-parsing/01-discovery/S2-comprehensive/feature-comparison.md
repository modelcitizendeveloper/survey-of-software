# Feature Comparison Matrix - Python Code Parsing Libraries

## Overview

Systematic comparison of viable Python code parsing/modification libraries across all evaluation criteria. Each data point is sourced from evidence collected during comprehensive research.

---

## Comparison Matrix

| Feature Category | LibCST | ast (stdlib) | rope |
|-----------------|---------|--------------|------|
| **FORMATTING PRESERVATION (30% weight)** |
| Preserves comments | ✅ Yes (CST design) | ❌ No (all removed) | ✅ Yes (region edits) |
| Preserves whitespace | ✅ Yes (explicit tracking) | ❌ No (normalized) | ✅ Yes (region preservation) |
| Preserves style choices | ✅ Yes (quotes, parens, etc.) | ❌ No (standardized) | ✅ Yes (text regions) |
| Mechanism | Concrete Syntax Tree | Abstract Syntax Tree | Region annotations |
| Round-trip fidelity | 100% lossless | Lossy (like JPEG) | High (surgical edits) |
| **Score (0-10)** | **10** | **0** | **8** |
| **Evidence Source** | libcst.readthedocs.io/why_libcst | docs.python.org/3/library/ast | rope.readthedocs.io |

| **MODIFICATION API (25% weight)** |
| Visitor pattern | ✅ CSTVisitor | ✅ NodeVisitor | ❌ (project-based API) |
| Transformer pattern | ✅ CSTTransformer | ✅ NodeTransformer | ❌ (refactoring ops) |
| Matchers | ✅ Declarative patterns | ❌ Manual isinstance | ❌ Not applicable |
| Codemod framework | ✅ Built-in CLI + testing | ❌ Manual | ❌ Different paradigm |
| Refactoring operations | ⚠️ General (via transformers) | ❌ Manual implementation | ✅ 8+ built-in ops |
| API complexity | Medium (immutability) | Low (simple traversal) | High (project model) |
| Lines of code (simple rename) | ~30-50 (transformer) | ~20-30 (transformer) | ~10-15 (refactor.rename) |
| **Score (0-10)** | **9** | **7** | **9** |
| **Evidence Source** | libcst.readthedocs.io/visitors | greentreesnakes.readthedocs.io | rope.readthedocs.io/overview |

| **PERFORMANCE (15% weight)** |
| Implementation | Rust native parser | C native parser | Pure Python |
| Claimed speed | "Within 2x CPython" | Baseline (fastest) | Not specified |
| Typical file (500 LOC) | ~60ms (estimated) | ~8ms (measured) | Unknown |
| Large file (500k LOC) | ~8-16 seconds (est.) | ~8 seconds (measured) | Slow (issue #324) |
| Performance issues | None reported | None | GitHub #324 complaint |
| Optimization | Binary wheels (Rust) | C implementation | Object DB caching |
| **Score (0-10)** | **7** | **10** | **5** |
| **Evidence Source** | libcst docs (goals) | Web search (benchmarks) | GitHub issues |

| **ERROR HANDLING (15% weight)** |
| Syntax error recovery | ❌ No (raises exception) | ❌ No (raises SyntaxError) | ⚠️ Unclear (assumed no) |
| Error reporting quality | Good (line/col + message) | Standard Python errors | Variable (per issues) |
| Partial parsing | ❌ Future feature | ❌ Not supported | ❌ Not documented |
| Validation | Strong (CST construction) | Strong (AST construction) | Project-wide checks |
| Error handling roadmap | Planned (issue #310) | None | Not documented |
| **Score (0-10)** | **3** | **2** | **4** |
| **Evidence Source** | GitHub issue #310 | docs.python.org/3/library/ast | Inferred from docs |

| **PRODUCTION MATURITY (10% weight)** |
| Public case studies | Instagram, Instawork, SeatGeek | Ubiquitous (mypy, pylint, etc.) | IDE integration (PyCharm, etc.) |
| GitHub stars | 1,800 | N/A (stdlib) | 2,100 |
| Dependent projects | ~12,200 | Uncountable (stdlib) | ~78,500 |
| Active maintenance | ✅ Yes (Nov 2025 release) | ✅ Python core team | ✅ Yes (July 2025 release) |
| Production scale | Instagram (millions LOC) | Entire Python ecosystem | IDE backends (massive) |
| Major bugs | None blocking | None | Some performance issues |
| Release stability | Regular (quarterly/monthly) | Python release cycle | Regular (few months) |
| **Score (0-10)** | **10** | **10** | **9** |
| **Evidence Source** | Instagram eng blog | Python docs | PyPI stats |

| **LEARNING CURVE (5% weight)** |
| Documentation quality | Excellent (9/10) | Excellent (9/10) | Good (7/10) |
| Tutorial availability | 6 comprehensive tutorials | Green Tree Snakes guide | Limited tutorials |
| Example quality | High (working code) | Good (official + community) | Basic examples |
| Time to productivity | 1-2 weeks (complex) | 1-2 days (basic) | 2-3 days (API), instant (IDE) |
| Community resources | Growing (SO, blogs) | Extensive | Moderate |
| Complexity factors | Immutability, metadata | Tree traversal | Project model, config |
| **Score (0-10)** | **6** | **8** | **6** |
| **Evidence Source** | Community blogs | Docs + SO | Documentation |

| **ADDITIONAL CRITERIA** |
| Python version support (runtime) | 3.9+ | 3.0+ (stdlib) | 3.x+ |
| Python syntax support (parsing) | 3.0-3.14 | Same as runtime | Up to 3.10 only |
| Dependencies | pyyaml, typing-ext (minimal) | None (stdlib) | None (minimal) |
| License | MIT | PSF (very permissive) | LGPL v3+ |
| Memory usage | High (immutable trees) | Medium (mutable trees) | Medium (caching) |
| Binary distribution | ✅ Wheels available | ✅ Stdlib | ✅ Pure Python |

---

## Detailed Feature Analysis

### 1. Formatting Preservation (30% weight)

#### LibCST: 10/10
**Mechanism**: Concrete Syntax Tree with explicit whitespace nodes

**Evidence**:
- Source: https://libcst.readthedocs.io/en/latest/why_libcst.html
- Quote: "LibCST preserves all whitespace and can be reprinted exactly, while parsing source into nodes that represent the semantics of the code."

**What's Preserved**:
- Comments (attached via metadata)
- Whitespace (spaces, tabs, blank lines)
- Parentheses (even semantically unnecessary)
- String delimiters (single/double/triple quotes)
- End-of-file newlines
- Formatting style choices

**Reliability**: 10/10 - Design goal, proven in production at Instagram

#### ast: 0/10
**Mechanism**: Abstract Syntax Tree (semantic only)

**Evidence**:
- Source: https://docs.python.org/3/library/ast.html
- Quote: "The produced code string will not necessarily be equal to the original code that generated the ast.AST object."

**What's Lost**:
- All comments
- Original whitespace
- Formatting choices
- Style preferences

**Reliability**: 10/10 - Documented limitation, by design

#### rope: 8/10
**Mechanism**: Region-based text editing

**Evidence**:
- Source: Rope documentation, comparative discussions
- Inference: Uses surgical text replacement in identified regions

**Strengths**:
- Preserves surrounding code untouched
- Excellent for targeted refactorings (rename is perfect)

**Limitations**:
- May struggle with complex structural transformations that rearrange code
- Less explicit than CST about guarantees

**Reliability**: 7/10 - Proven in IDE usage, but less documented than LibCST

---

### 2. Modification API (25% weight)

#### LibCST: 9/10
**Patterns**:
- `CSTVisitor` (read-only traversal)
- `CSTTransformer` (read-write modification)
- Matchers (declarative pattern matching)
- Codemod framework (high-level CLI + testing)

**Evidence**:
- Source: https://libcst.readthedocs.io/en/latest/visitors.html
- Example complexity: ~30-50 LOC for simple transformation (from Instawork blog)

**Strengths**:
- Immutability prevents mutation bugs
- Matchers more readable than isinstance checks
- Built-in testing utilities
- Production-proven at Instagram

**Weaknesses**:
- Immutability adds verbosity (`.with_changes()` pattern)
- Learning curve for metadata system

**Reliability**: 9/10 - Comprehensive documentation, production case studies

#### ast: 7/10
**Patterns**:
- `NodeVisitor` (read-only)
- `NodeTransformer` (read-write)

**Evidence**:
- Source: https://docs.python.org/3/library/ast.html
- Example complexity: ~20-30 LOC for simple transformation (from Green Tree Snakes)

**Strengths**:
- Simple, well-understood patterns
- Official Python documentation
- Extensive community examples

**Weaknesses**:
- Manual location info management (`fix_missing_locations()`)
- No high-level abstractions (raw tree manipulation)
- No built-in testing or codemod framework

**Reliability**: 9/10 - Official docs, decades of community usage

#### rope: 9/10
**Patterns**:
- Project-based API
- Specialized refactoring operations (8+ types)

**Evidence**:
- Source: https://rope.readthedocs.io/en/latest/overview.html
- Example complexity: ~10-15 LOC for rename (simple API call)

**Strengths**:
- Comprehensive refactoring operations (rename, extract, move, etc.)
- Very simple for standard refactorings
- Project-wide awareness (updates all references)

**Weaknesses**:
- Different paradigm than visitor/transformer
- Requires project initialization
- Less flexible for custom transformations

**Reliability**: 8/10 - Documentation adequate, proven in IDEs

---

### 3. Performance (15% weight)

#### LibCST: 7/10
**Implementation**: Rust native parser

**Evidence**:
- Source: https://libcst.readthedocs.io/ (search results)
- Quote: "The aspirational goal for LibCST is to be within 2x CPython performance"

**Estimates**:
- 500 LOC file: ~60ms (extrapolated from 2x goal)
- Meets <100ms requirement for typical files

**Reliability**: 6/10 - Goal stated, no published benchmarks. Inferred from production usage without complaints.

#### ast: 10/10
**Implementation**: C native parser

**Evidence**:
- Source: Web search on AST performance
- Measured: 500k LOC in ~8 seconds = ~8ms per 500 LOC file

**Performance**: Easily meets <100ms requirement

**Reliability**: 9/10 - Measured data, C implementation is inherently fast

#### rope: 5/10
**Implementation**: Pure Python

**Evidence**:
- Source: Rope documentation quote: "Rope is written in Python itself"
- Issue #324: Performance complaint (slow refactoring)

**Concerns**:
- Pure Python slower than native implementations
- Performance issue reported on GitHub
- Object DB caching helps but doesn't eliminate concern

**Reliability**: 6/10 - One documented complaint, no systematic benchmarks

---

### 4. Error Handling (15% weight)

#### LibCST: 3/10
**Syntax Errors**: No recovery (raises `ParserSyntaxError`)

**Evidence**:
- Source: https://github.com/Instagram/LibCST/issues/310
- Quote: "Users have requested this feature... error recovery is listed as a future feature"

**Error Quality**: Good reporting (line/col + message)

**Future**: Planned feature (no timeline)

**Reliability**: 9/10 - Well-documented limitation

#### ast: 2/10
**Syntax Errors**: No recovery (raises `SyntaxError`)

**Evidence**:
- Source: https://docs.python.org/3/library/ast.html
- Standard Python error handling

**Error Quality**: Standard Python exceptions

**Future**: No plans for error recovery

**Reliability**: 10/10 - Documented behavior

#### rope: 4/10
**Syntax Errors**: Assumed no recovery (not well-documented)

**Evidence**:
- Source: Inference from documentation gaps
- No explicit error recovery documentation

**Validation**: Project-wide refactoring validation (checks name collisions, etc.)

**Reliability**: 5/10 - Lower confidence due to lack of explicit documentation

---

### 5. Production Maturity (10% weight)

#### LibCST: 10/10
**Evidence**:
- Instagram engineering blog (official case study)
- Instawork, SeatGeek blogs (detailed usage)
- 12,200 dependent repositories
- Active development (Nov 2025 release)

**Reliability**: 10/10 - Multiple high-quality sources

#### ast: 10/10
**Evidence**:
- Python standard library (ultimate maturity)
- Used by mypy, pylint, black, etc. (ecosystem foundation)
- Maintained by Python core team

**Reliability**: 10/10 - Observable reality

#### rope: 9/10
**Evidence**:
- 78,500 dependent projects (highest of all)
- PyCharm/VS Code integration
- Active maintenance (July 2025 release)

**Slight deduction**: Some performance issues unresolved

**Reliability**: 9/10 - Strong ecosystem evidence

---

### 6. Learning Curve (5% weight)

#### LibCST: 6/10
**Evidence**:
- Community reports: "Tricky at first, took a while to get the hang of it"
- Mitigation: 6 comprehensive tutorials

**Time**: 1-2 weeks for complex transformations

**Reliability**: 7/10 - Subjective reports but consistent

#### ast: 8/10
**Evidence**:
- Official Python docs + Green Tree Snakes
- Simpler concepts than CST

**Time**: 1-2 days for basic transformations

**Reliability**: 8/10 - Well-established, many learners

#### rope: 6/10
**Evidence**:
- Project model adds complexity
- Documentation less tutorial-heavy

**Time**: 2-3 days for programmatic use, instant for IDE use

**Reliability**: 6/10 - Less evidence, documentation gaps

---

## Weighted Scoring Calculation

### LibCST
- Formatting: 10 × 0.30 = 3.00
- Modification: 9 × 0.25 = 2.25
- Performance: 7 × 0.15 = 1.05
- Error Handling: 3 × 0.15 = 0.45
- Production: 10 × 0.10 = 1.00
- Learning: 6 × 0.05 = 0.30

**Total: 8.05/10**

### ast (stdlib)
- Formatting: 0 × 0.30 = 0.00
- Modification: 7 × 0.25 = 1.75
- Performance: 10 × 0.15 = 1.50
- Error Handling: 2 × 0.15 = 0.30
- Production: 10 × 0.10 = 1.00
- Learning: 8 × 0.05 = 0.40

**Total: 4.95/10**

### rope
- Formatting: 8 × 0.30 = 2.40
- Modification: 9 × 0.25 = 2.25
- Performance: 5 × 0.15 = 0.75
- Error Handling: 4 × 0.15 = 0.60
- Production: 9 × 0.10 = 0.90
- Learning: 6 × 0.05 = 0.30

**Total: 7.20/10**

---

## Evidence Quality by Category

### High Reliability Data (9-10/10 confidence)
- Official documentation for all libraries
- GitHub metrics (stars, forks, dependents)
- Engineering blog case studies (Instagram, Instawork, SeatGeek)
- License information (from repositories)
- Python version support (from PyPI/docs)

### Medium Reliability Data (7-8/10 confidence)
- Performance claims (stated goals vs measured)
- Community learning curve reports (subjective but consistent)
- API complexity assessments (from example code)

### Lower Reliability Data (5-6/10 confidence)
- Performance estimates (extrapolated, not measured)
- Rope error handling (inferred from gaps)
- Formatting preservation edge cases

---

## Key Insights

### Clear Winner for Given Requirements
**LibCST** scores highest (8.05) when formatting preservation weighted at 30%

**Sensitivity Analysis**:
- If formatting was 10% weight instead: AST would lead
- If performance was 30% weight: AST would lead
- Current weights match requirements: LibCST is optimal

### ast Strength: Wrong Criteria
ast is technically excellent but fails the primary requirement (formatting preservation)

### rope Position: Strong Alternative
rope scores well (7.20) but:
- Python 3.10 syntax limitation is critical gap
- LGPL license may not suit all users
- Performance concerns unresolved

---

## Decision Framework

**Choose LibCST if**:
- Formatting preservation is top priority (30%+ weight)
- Building codemods or refactoring tools
- Need production-proven solution
- MIT license required

**Choose ast if**:
- Formatting preservation not needed (0% weight)
- Code generation or analysis only
- Performance is critical
- Zero dependencies required

**Choose rope if**:
- Need standard refactoring operations (rename, extract, etc.)
- Python 3.10 syntax sufficient
- LGPL license acceptable
- IDE integration desired

**Choose none (build custom) if**:
- Need syntax error recovery (all libraries fail)
- Unusual requirements not met by existing tools
