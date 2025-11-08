# Validation Plan: LibCST for Schema Evolution Framework

**Source**: Extracted from S1 Rapid Discovery (application-specific content)
**Purpose**: Hands-on testing plan for validating LibCST in schema evolution use case
**Date**: November 7, 2025

---

## Overview

This validation plan is **application-specific** for the schema evolution framework. The generic library research lives in `01-discovery/`. This plan describes how to validate LibCST for our specific use case.

---

## Primary Focus: LibCST

### Testing Areas

1. **Hands-On Modification Testing**
   - Parse a real `models.py` file from a Django/SQLAlchemy project
   - Locate a specific class definition (e.g., `class User(BaseModel)`)
   - Insert a new field with proper indentation
   - Modify an existing field (e.g., change type, add validator)
   - Verify formatting preservation (comments, blank lines, indentation)
   - Measure performance (parse + modify + unparse time)

2. **API Learning Curve Assessment**
   - Time how long it takes to write first working codemod
   - Document pain points and "gotchas"
   - Test pattern matching capabilities (finding specific code patterns)
   - Evaluate metadata wrappers (scope analysis) for import resolution

3. **Edge Cases**
   - Multi-line strings
   - Complex decorators
   - Nested classes
   - Type hints and annotations
   - Comments in unusual positions

4. **Integration Testing**
   - Test with our schema evolution use case specifically:
     - Parse `models.py`
     - Find migration point (specific class/function)
     - Insert new code
     - Write back to file
   - Test batch processing (multiple files)
   - Test error handling (malformed Python)

5. **Performance Benchmarking**
   - Small file (100 lines): parse/modify/unparse time
   - Medium file (1000 lines): parse/modify/unparse time
   - Large file (5000+ lines): parse/modify/unparse time
   - Compare with ast module (read-only parsing)

---

## Secondary Focus: ast (Fallback)

### Testing Areas

1. **Confirm Formatting Loss**
   - Parse file, unparse immediately (no modifications)
   - Document exactly what changes (indentation, comments, blank lines)
   - Test if auto-formatter (Black) can compensate

2. **Evaluate as Read-Only Tool**
   - If we use LibCST for writing, can we use ast for faster read-only analysis?
   - Performance comparison: ast vs LibCST for read-only operations

---

## Tertiary Focus: Rope (If Time Permits)

### Testing Areas

1. **Evaluate Complexity Trade-Off**
   - Set up a Project
   - Perform simple rename
   - Document overhead vs. LibCST

2. **Python 3.10 Syntax Limitation**
   - Test with Python 3.11+ syntax (match/case, improved type hints)
   - Confirm limitation and impact

---

## Questions to Answer in Validation

1. **LibCST Learning Curve**: How long does it take to become productive?
2. **LibCST Performance**: Is it fast enough for interactive use in our framework?
3. **LibCST Edge Cases**: Are there formatting scenarios where it fails?
4. **ast Viability**: Can we use auto-formatters to compensate for formatting loss?
5. **Rope Worth Complexity**: Does rope offer anything LibCST doesn't for our use case?

---

## Success Criteria

**LibCST Proves Viable If**:
- ✅ Can successfully modify a real-world `models.py` file
- ✅ Preserves formatting in 95%+ of cases
- ✅ Performance is acceptable (<1s for typical file)
- ✅ Learning curve is reasonable (productive within 2-4 hours)
- ✅ API supports our schema evolution use cases

**Fallback to ast If**:
- ❌ LibCST has critical bugs or edge cases
- ❌ Performance is unacceptable
- ❌ Learning curve is too steep
- ✅ We're willing to reformat modified files with Black

**Consider Rope If**:
- ✅ We need cross-file refactoring (unlikely based on requirements)
- ✅ LGPL license is acceptable
- ❌ Python 3.10 syntax limitation is acceptable

---

## Deliverables

1. **Hands-on tutorial**: Complete walkthrough of LibCST for our exact use case
2. **Performance benchmarks**: Actual timing data for realistic files
3. **Code samples**: Working examples for each modification type we need
4. **Edge case documentation**: What works, what doesn't, workarounds
5. **Final recommendation**: LibCST vs ast vs Rope with detailed justification

---

## Timeline

**Estimated**: 1-2 days for hands-on testing and proof-of-concept development

---

**Note**: This is application-specific validation work. Generic library capabilities research is in `01-discovery/S1-S4/`.
