# Use Case: Text Editor Search (Find/Replace)

## Who

**Persona**: Application developer building text editor or IDE
**Examples**: VS Code, Sublime Text, Notepad++, IntelliJ IDEA
**Scale**: Files typically <10 MB, patterns change frequently (every keystroke)

## Why (Requirements)

### Functional Requirements
- **Interactive search**: User types pattern, sees results immediately
- **Incremental**: Update results as pattern changes
- **Multiple matches**: Highlight all occurrences in document
- **Case sensitivity**: Toggle between case-sensitive/-insensitive
- **Regex support**: Users expect wildcards, character classes, etc.

### Non-Functional Requirements
- **Latency**: <50ms response time (feels instant to user)
- **No UI blocking**: Search must not freeze editor
- **Memory efficient**: Don't double memory for search
- **Simple implementation**: Editor has many features, search shouldn't dominate codebase

## Constraints Analysis

### Pattern Characteristics
- **Short patterns**: Typically 3-30 characters (what users type)
- **Changes frequently**: Every keystroke is a new pattern
- **Unpredictable**: User might search for anything

### Text Characteristics
- **Small to medium**: Source files usually < 1 MB
- **UTF-8 common**: Must handle Unicode correctly
- **Structured**: Code has predictable structure (not random)

### Performance Constraints
- **Latency critical**: Must respond in <50ms for good UX
- **Preprocessing cost matters**: Pattern changes every keystroke
- **Multiple matches**: Must find all, not just first

## Solution: Boyer-Moore or Optimized Naive

### Primary Recommendation: Use Stdlib

**Choice**: `std::string::find()` (C++), `str.find()` (Python), similar
**Why**:
- Highly optimized (often BMH variant)
- Zero integration cost
- Handles Unicode
- Fast enough for typical files (<1 MB)

**Example**: VS Code uses Rust regex crate (DFA-based, linear time)

### Algorithm Rationale

**Why NOT sophisticated algorithms**:
- KMP: Preprocessing overhead not amortized (pattern changes constantly)
- Aho-Corasick: Overkill for single pattern, complex trie construction wasted
- Rabin-Karp: Hash computation overhead, no advantage over BM

**Why Boyer-Moore (or BMH)**:
- Sublinear average case: For 1 MB file, might check only 50K characters
- Preprocessing: O(m) where m is small (10-20 chars typical)
- Large alphabet (English text): Bad-character rule very effective
- Simple enough: BMH variant is ~100 lines

**Why Naive sometimes wins**:
- Very short patterns (<5 chars): Preprocessing overhead dominates
- Small files (<10 KB): Naive fast enough, simpler
- Modern SIMD: Can check 16-32 bytes at once, beating simple BM

### Implementation Details

**Incremental Search**:
```
Option 1: Re-search on every keystroke
- Simple: Just call search() again
- Fast enough for <1 MB files

Option 2: Update previous results
- Complex: Track matches, update incrementally
- Needed for very large files (>10 MB)
```

**Case-Insensitive**:
```
Option 1: Lowercase both pattern and text
- Simple but doubles memory

Option 2: Case-folding in comparison
- More efficient, built into many search functions
```

**Regex Support**:
```
Use regex engine (NOT pure string matching):
- Rust regex crate (VS Code)
- RE2 (Google, C++)
- Python re module

Ensure linear-time guarantee (avoid catastrophic backtracking)
```

## Alternatives

### If Files Very Large (>100 MB)

**Problem**: Even BM takes too long
**Solution**: Index-based search
- Build suffix array or inverted index
- Search index instead of raw text
- Example: Sublime Text indexes on file open

### If Many Concurrent Searches

**Problem**: Multiple users searching simultaneously (cloud IDE)
**Solution**: Thread-safe search, async execution
- Don't block UI thread
- Background worker for search
- Stream results as found

### If Need Fuzzy Matching

**Problem**: User types "functon", wants "function"
**Solution**: Approximate matching
- Edit distance (Levenshtein)
- Bitap algorithm (agrep)
- Slower but better UX for typos

## Libraries

### C++
- **std::string::find()**: Built-in, fast, use this
- **Boost.StringAlgo**: If need advanced features
- **RE2**: For regex with linear-time guarantee

### Python
- **str.find()**: Built-in, optimized BMH variant
- **re module**: For regex (careful with backtracking)
- **pyre2**: RE2 bindings for untrusted patterns

### Rust
- **str::find()**: Built-in, well-optimized
- **memchr crate**: SIMD-optimized for byte search
- **regex crate**: Linear-time regex (used by ripgrep, VS Code)

### JavaScript/TypeScript
- **String.indexOf()**: Built-in, usually fast
- **TextEncoder/TextDecoder**: For UTF-8 handling
- **regex**: Avoid catastrophic backtracking (use RE2-based if possible)

## Pitfalls to Avoid

### 1. Catastrophic Backtracking (Regex)

**Problem**: User types pattern like `(a+)+b`, text is "aaaaaaaaaaa..."
**Result**: Exponential time, editor freezes

**Solution**: Use linear-time regex engine (RE2, Rust regex)

**Example**: VS Code switched from JavaScript regex to Rust regex to avoid this

### 2. Blocking UI Thread

**Problem**: Search runs on main thread, UI freezes during search
**Result**: Poor UX, editor feels sluggish

**Solution**: Run search in background thread/worker
- Main thread: Handle input, update UI
- Worker thread: Run search, stream results

### 3. Memory Explosion (Case-Insensitive)

**Problem**: Lowercase entire 100 MB file to search case-insensitively
**Result**: 200 MB memory usage, slow

**Solution**: Use case-folding during comparison (don't copy string)

### 4. Poor Unicode Handling

**Problem**: Byte-level search breaks on multi-byte UTF-8
**Example**: Search for "café", pattern is UTF-8, but text is Latin-1
**Result**: No match or false matches

**Solution**: Normalize encoding, use character-level search

### 5. Over-Engineering

**Problem**: Implement complex algorithm (AC, KMP with optimizations)
**Result**: Bugs, hard to maintain, no performance gain

**Solution**: Use stdlib, optimize only if proven slow

## Performance Expectations

### Typical File (100 KB, 3000 lines)

**Naive/BM**: <1ms (instant)
**Result**: Good UX, no optimization needed

### Large File (10 MB, 300K lines)

**Naive**: ~50-100ms (noticeable lag)
**Boyer-Moore**: ~10-20ms (acceptable)
**Result**: BM or index needed

### Very Large File (100 MB+)

**Any algorithm**: >100ms (poor UX)
**Solution**: Index-based search (build on file open)

## Real-World Examples

### VS Code
- **Algorithm**: Rust regex crate (DFA + bounded backtracking)
- **Why**: Linear time guarantee, Unicode support
- **Performance**: Handles 100 MB files smoothly

### Sublime Text
- **Algorithm**: Custom optimized search (likely BMH)
- **Feature**: Builds index for large files
- **Performance**: Known for speed, handles GB files

### Notepad++
- **Algorithm**: Scintilla component (likely BMH)
- **Feature**: Regex via Boost
- **Performance**: Fast for typical files

### Vim
- **Algorithm**: Custom implementation (likely BM variant)
- **Feature**: Supports very complex patterns
- **Performance**: Optimized over decades

## Key Takeaways

**Best Choice**: Use stdlib (std::string::find, str.find, etc.)
- Fast enough for 99% of use cases
- Zero integration cost
- Well-tested

**When to Optimize**:
- Files routinely >10 MB → Consider index
- Many patterns → Consider AC (rare for editor)
- Regex needed → Use RE2 or similar (linear time)

**Critical Requirement**: Don't block UI thread
- Run search async
- Stream results as found
- Cancel if user changes pattern

**Avoid**: Over-engineering
- Don't implement complex algorithm unless proven needed
- Profile first, optimize if slow
- User experience > algorithmic purity
