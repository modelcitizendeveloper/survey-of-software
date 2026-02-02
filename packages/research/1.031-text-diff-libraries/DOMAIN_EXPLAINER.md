# Text Diff Libraries: Domain Explainer

## What Are Text Diff Libraries?

Text diff libraries compute the differences between two sequences of text (or lines, or tokens). They power version control systems, code review tools, merge conflict resolution, and collaborative editing.

The core problem: given two text strings A and B, find the **minimum set of operations** (insertions, deletions, modifications) that transforms A into B.

## Why This Matters

Every software developer uses diff tools daily:
- **Version control**: `git diff` shows what changed between commits
- **Code review**: GitHub/GitLab show side-by-side diffs
- **Merge conflicts**: 3-way merge algorithms resolve conflicting changes
- **Collaborative editing**: Google Docs, CRDTs track simultaneous edits
- **Testing**: Test frameworks compare expected vs actual output
- **Documentation**: Track changes to specifications, contracts, schemas

Poor diff algorithms create noise:
- Irrelevant whitespace changes clutter reviews
- Large refactorings appear as "delete everything, add everything"
- Merge conflicts become unsolvable when algorithm misidentifies common ancestors
- Test failures show unhelpful diffs

## The Problem Space

### 1. Classic Line-Based Diff (Myers Algorithm)
The standard Unix `diff` command uses the **Myers diff algorithm** (1986), which finds the shortest edit script between two sequences. It's based on the **Longest Common Subsequence (LCS)** problem.

**Pros:**
- Mathematically optimal for minimizing edit distance
- Fast for most real-world inputs (O(ND) where D is edit distance)
- Well-studied, proven correct

**Cons:**
- Can produce unintuitive diffs when multiple equally-short edits exist
- Treats all lines equally - doesn't understand code structure
- Sensitive to line reordering (e.g., sorting imports)

**Use case:** General-purpose diffing where minimizing edit distance is the goal.

### 2. Patience Diff
Developed by Bram Cohen (BitTorrent creator) as an alternative to Myers. The key insight: **unique lines are reliable anchors**.

**Algorithm:**
1. Find lines that appear exactly once in both files
2. Use these as anchors to recursively divide the problem
3. Fall back to Myers for regions without unique lines

**Pros:**
- More intuitive diffs for code (preserves function boundaries)
- Better at handling moved blocks
- Reduces "diff noise" from indentation changes

**Cons:**
- Slower than Myers in worst case
- Not always minimal (trades edit distance for readability)

**Use case:** Code reviews, where human readability matters more than mathematical optimality.

### 3. Histogram Diff
A variant of patience diff that uses occurrence counts instead of strict uniqueness.

**Pros:**
- Similar intuition to patience diff
- Faster than patience in some cases

**Use case:** Git's `--histogram` option for code diffs.

### 4. Semantic Diff
Goes beyond line-based comparison to understand **code structure**:
- Parse code into Abstract Syntax Trees (ASTs)
- Diff at the AST level (functions, classes, expressions)
- Map changes to semantic units ("renamed function X" vs "deleted 50 lines, added 50 lines")

**Pros:**
- Understands refactorings (rename, extract method, move class)
- Ignores irrelevant formatting changes
- Can detect equivalent but syntactically different code

**Cons:**
- Language-specific (needs parser for each language)
- Computationally expensive
- Harder to present to users (can't just show line diffs)

**Use case:** Refactoring-heavy codebases, API compatibility checking, security audits.

### 5. Word/Character-Level Diff
Instead of diffing lines, diff at word or character granularity.

**Pros:**
- Shows inline changes ("changed `foo` to `bar`" instead of "deleted line, added line")
- Better for prose (markdown, documentation)
- Reduces visual noise in code reviews

**Cons:**
- Slower for large files
- Can be overwhelming (too much detail)

**Use case:** Git's `--word-diff`, prose editing, fine-grained change tracking.

### 6. Three-Way Merge
Special case of diffing: given a **base version** and two **divergent versions**, automatically merge changes.

**Algorithm:**
1. Compute diff(base, left) and diff(base, right)
2. Apply non-conflicting changes from both sides
3. Mark conflicts where both sides changed the same region

**Conflict resolution strategies:**
- Myers-based: minimize edit distance
- Patience-based: preserve unique lines as anchors
- Semantic: understand code structure to resolve conflicts

**Use case:** Git merge, collaborative editing, CRDT replication.

## Key Libraries in Python

Based on algorithm support:

| Library | Myers | Patience | Histogram | Semantic | 3-Way Merge |
|---------|-------|----------|-----------|----------|-------------|
| `difflib` (stdlib) | ✓ | ✗ | ✗ | ✗ | ✗ |
| `diff-match-patch` | ✓ | ✗ | ✗ | ✗ | ✗ |
| `libdiff` | ? | ? | ? | ? | ? |
| `Tree-sitter` | ✗ | ✗ | ✗ | ✓ | ✗ |
| `GumTree` | ✗ | ✗ | ✗ | ✓ | ✗ |
| `difftastic` | ✗ | ✗ | ✗ | ✓ | ✗ |

(We'll fill in the `?` during discovery.)

## The Landscape Shift

**1980s-1990s:** Myers algorithm dominates (Unix diff, RCS, CVS)
**2000s:** Git popularizes patience diff and histogram diff for code
**2010s:** Semantic diff emerges for refactoring detection (e.g., GitHub's "renamed" detection)
**2020s:** Tree-sitter and structural diffing gain traction for code intelligence

## Business Context

When do you need a diff library?

1. **Version control tools**: Building a custom VCS or git-like tool
2. **Code review platforms**: Custom diffs for internal code hosting
3. **Testing frameworks**: Compare expected vs actual output
4. **Data pipelines**: Detect schema changes, data drift
5. **Document collaboration**: Track changes in structured documents
6. **API versioning**: Detect breaking changes in OpenAPI specs
7. **Infrastructure as Code**: Terraform plan, Kubernetes diff

## What We'll Discover

In the S1-S4 discovery phases, we'll answer:

**S1 (Rapid):** What libraries exist? What algorithms do they support?
**S2 (Comprehensive):** Performance benchmarks, accuracy, edge cases
**S3 (Need-Driven):** Which library for version control? Testing? Merge conflicts?
**S4 (Strategic):** Longevity, ecosystem, maintenance, future-proofing

By the end, you'll know **which diff library to choose for your use case**.
