# S3 Need-Driven Discovery - Recommendation

## Use Case → Library Quick Reference

| Who You Are | What You Need | Primary Library | Alternative |
|-------------|---------------|-----------------|-------------|
| **Testing Engineer** | Compare test outputs | difflib + DeepDiff | jsondiff (JSON) |
| **Code Review Builder** | Analyze git diffs | GitPython + unidiff | - |
| **Data Engineer** | Compare structured data | DeepDiff | jsondiff, xmldiff |
| **Developer Tool Creator** | Semantic code analysis | tree-sitter | GitPython (simpler) |
| **Text Processing Dev** | Fuzzy matching | python-Levenshtein | difflib (simple cases) |

## Key Insights from Use Cases

### Pattern 1: Layered Complexity
Start simple, upgrade when needed:
1. **Level 1:** difflib (stdlib, zero deps)
2. **Level 2:** Specialized libraries (DeepDiff, python-Levenshtein)
3. **Level 3:** Complex infrastructure (tree-sitter, GitPython)

**Rule:** Don't skip levels. Try simpler solution first, profile, then upgrade.

### Pattern 2: Domain Specificity Matters
Don't use general-purpose tools for specialized domains:
- ❌ difflib for Python objects → ✅ DeepDiff
- ❌ text diff for JSON → ✅ jsondiff or DeepDiff
- ❌ line diff for semantic changes → ✅ tree-sitter

### Pattern 3: Performance vs Simplicity Trade-off
**Stdlib (difflib) trade-off:**
- ✅ Zero dependencies, simple API
- ❌ Slower, fewer features

**C extensions (python-Levenshtein) trade-off:**
- ✅ 10-100x faster
- ❌ Build dependency, more complex

**Infrastructure (tree-sitter) trade-off:**
- ✅ Semantic understanding
- ❌ Steep learning curve, complex integration

## Common Anti-Patterns Across Use Cases

**❌ Anti-Pattern: Using GitPython outside git contexts**
- Testing: Don't use GitPython to compare test outputs (use difflib/DeepDiff)
- Data: Don't use GitPython for database comparisons (use DeepDiff)
- Rule: GitPython only for git repositories

**❌ Anti-Pattern: Using difflib for structured data**
- Loses structure (converts to text)
- Can't ignore specific fields
- Not type-aware
- Rule: Use DeepDiff for objects/JSON, xmldiff for XML

**❌ Anti-Pattern: Using tree-sitter for simple text diff**
- Massive overkill
- Slow, complex setup
- Rule: tree-sitter only when semantic understanding required

**❌ Anti-Pattern: Using python-Levenshtein for full diff**
- Edit distance only (no context)
- Character-level only
- Rule: Use for fuzzy matching, not code review

## Validation Framework

### Questions to Ask Before Choosing

**1. What am I comparing?**
- Text/code? → difflib, diff-match-patch, GitPython
- Python objects? → DeepDiff
- JSON? → DeepDiff or jsondiff
- XML? → xmldiff
- Code structure? → tree-sitter

**2. What's my performance requirement?**
- <10ms (real-time)? → python-Levenshtein, unidiff
- <1s (interactive)? → difflib, DeepDiff, GitPython
- Batch (no time limit)? → Any library

**3. What's my dependency budget?**
- Zero deps? → difflib
- Minimal? → diff-match-patch, DeepDiff, jsondiff
- OK with git? → GitPython
- OK with complex setup? → tree-sitter

**4. What's my team's expertise?**
- Junior devs? → difflib (simplest)
- Experienced? → DeepDiff, GitPython
- Specialists? → tree-sitter (requires investment)

**5. What's the long-term commitment?**
- One-off script? → difflib (quick and done)
- Production tool? → diff-match-patch, DeepDiff, GitPython
- Core feature? → tree-sitter (if semantic understanding needed)

## Decision Trees by Domain

### For Testing
```
Comparing...
├─ Text files?
│  └─ difflib ✓
├─ Python objects?
│  └─ DeepDiff ✓
├─ JSON API responses?
│  ├─ DeepDiff ✓ (more features)
│  └─ jsondiff (RFC 6902 standard)
└─ XML?
   ├─ xmldiff (structure matters)
   └─ difflib (text sufficient)
```

### For Code Review / CI/CD
```
Working with...
├─ Git repos?
│  ├─ Need parsing? → GitPython + unidiff ✓
│  └─ Just diff? → GitPython ✓
└─ Standalone files?
   └─ diff-match-patch ✓
```

### For Data Engineering
```
Comparing...
├─ JSON?
│  ├─ DeepDiff ✓ (type-aware, ignore rules)
│  └─ jsondiff (standards-focused)
├─ XML?
│  └─ xmldiff ✓
├─ CSV?
│  ├─ pandas (DataFrame API)
│  └─ DeepDiff (after loading to dicts)
└─ Database records?
   └─ DeepDiff ✓ (load as dicts)
```

### For Semantic Code Analysis
```
Need...
├─ Semantic understanding?
│  └─ tree-sitter ✓ (AST-aware)
├─ Line-based sufficient?
│  ├─ Git repos? → GitPython (patience diff) ✓
│  └─ Standalone? → diff-match-patch ✓
└─ Just text? → difflib ✓
```

### For Fuzzy Matching
```
Performance...
├─ Critical (real-time)?
│  └─ python-Levenshtein ✓ (C extension)
├─ Acceptable (batch)?
│  ├─ python-Levenshtein ✓ (fastest)
│  └─ difflib (stdlib, good enough)
└─ Simple case (low volume)?
   └─ difflib.get_close_matches ✓
```

## Success Metrics by Use Case

### Testing (difflib + DeepDiff)
- ✅ Test failures show exact differences
- ✅ <5% overhead from diff computation
- ✅ Developers debug from diff output alone

### Code Review (GitPython + unidiff)
- ✅ Patience diff shows moved blocks correctly
- ✅ Can filter/analyze diffs programmatically
- ✅ Fast enough for CI/CD (seconds per PR)

### Data Engineering (DeepDiff)
- ✅ Detects type changes (int vs str)
- ✅ Ignores irrelevant fields (timestamps)
- ✅ Diffs are serializable (audit trail)

### Developer Tools (tree-sitter)
- ✅ Detects renames (not delete + add)
- ✅ Parses multiple languages
- ✅ Incremental updates work

### Text Processing (python-Levenshtein)
- ✅ <10ms per comparison (real-time)
- ✅ Finds similar strings (tolerates typos)
- ✅ Similarity scores make sense

## Final Recommendations

**Most Common Pattern: Start with stdlib, specialize as needed**
```
1. Start: difflib (built-in, quick to try)
2. Profile: Is it fast enough? Are diffs good?
3. Specialize:
   - Objects? → DeepDiff
   - Git? → GitPython
   - Fuzzy? → python-Levenshtein
   - Semantic? → tree-sitter
```

**Safety Net: Combination Approach**
Don't limit yourself to one library - use the right tool per use case:
- Testing: difflib + DeepDiff
- CI/CD: GitPython + unidiff
- Data: DeepDiff + jsondiff
- Tools: tree-sitter + GitPython
- Text: python-Levenshtein + difflib

**When in Doubt:**
1. Read S1 (quick comparison)
2. Match your use case to S3 examples
3. Check S4 for long-term concerns
4. Start simple (difflib), upgrade if needed
