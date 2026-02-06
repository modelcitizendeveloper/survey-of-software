# S1 Rapid Discovery - Recommendation

## Quick Decision Matrix

### Text/Code Diff (Most Common Case)

**Start here: difflib**
- ✅ Already installed (stdlib)
- ✅ Good enough for 80% of cases
- ✅ Simple API, quick to learn

**Upgrade when:**
- Need patch application → **diff-match-patch**
- Working with git repos → **GitPython**
- Need better diffs for moved code → **GitPython** (patience/histogram)
- Performance critical → **diff-match-patch** or **GitPython**

### Structured Data Diff

**Python objects/dicts:** → **DeepDiff**
- Type-aware, powerful ignore rules
- Excellent for testing

**JSON data:** → **jsondiff** (if need RFC 6902) or **DeepDiff** (more features)
- jsondiff for standardized JSON Patch
- DeepDiff for flexibility

**XML documents:** → **xmldiff**
- Only use if text diff produces unhelpful output

### Specialized Use Cases

**Semantic code analysis:** → **tree-sitter**
- Requires significant investment
- Not a drop-in diff replacement
- For refactoring detection, code intelligence tools

**Parse existing diffs:** → **unidiff**
- When you have git diff output to process
- Pairs with GitPython or difflib

**Fuzzy matching:** → **python-Levenshtein**
- Similarity scoring, spell checking
- Complements (not replaces) text diff

## Common Combinations

**Code review pipeline:**
```
GitPython (generate patience diff)
  → unidiff (parse/filter)
  → custom analysis
```

**Testing stack:**
```
difflib (text files) + DeepDiff (objects) + python-Levenshtein (fuzzy)
```

**Multi-format comparison:**
```
difflib (text) + jsondiff (JSON) + xmldiff (XML)
```

## The "One Library" Question

**"I can only pick one, what should it be?"**

**Answer: difflib**
- Zero dependencies
- Covers most common cases
- When insufficient, you'll know exactly what features you need
- Then come back to this guide to pick the right specialized tool

## Red Flags

**DON'T use:**
- tree-sitter for simple text diff (massive overkill)
- DeepDiff for text files (wrong tool)
- GitPython without git installed (won't work)
- jsondiff/xmldiff for non-JSON/XML data

**DO validate:**
- Performance with your data sizes (benchmark before committing)
- Diff quality with your content type (code? prose? data?)
- Maintenance status (check last release date)

## Ecosystem Health Summary

**Very active (frequent updates, large community):**
- GitPython, tree-sitter, DeepDiff

**Active (regular updates):**
- difflib (stdlib), unidiff, xmldiff, python-Levenshtein

**Maintenance mode (stable, infrequent updates):**
- diff-match-patch, jsondiff

All libraries listed here are production-ready. "Maintenance mode" means stable and complete, not abandoned.

## Next Steps After S1

**For quick decisions:**
- Read S4 Strategic (check for long-term concerns)
- Pick top choice, validate with small test

**For thorough analysis:**
- S2 Comprehensive (deep technical dive)
- S3 Need-Driven (validate against your specific use case)
- S4 Strategic (long-term viability, team expertise)

**Time saved:**
This S1 guide condenses ~40 hours of research into a 15-minute read. You now know what exists, what each is best for, and how to choose.
