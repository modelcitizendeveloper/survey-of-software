# Eliminated Libraries - Evidence-Based Exclusions

## Overview

This document explains why certain Python AST/parsing libraries were eliminated from consideration during S2 comprehensive analysis. Each elimination is supported by verifiable evidence from authoritative sources.

---

## 1. RedBaron - ELIMINATED

**Repository**: https://github.com/pycqa/redbaron
**PyPI**: https://pypi.org/project/redbaron/
**Status**: Effectively Abandoned

### Elimination Rationale

**Primary Reason**: Limited Python version support (Python 3.7 maximum)

### Evidence

**Source**: https://pypi.org/project/redbaron/

**Quote**: "RedBaron supports Python 2 and up to Python 3.7 grammar."

**Analysis**:
- Python 3.7 reached end-of-life on June 27, 2023
- Current Python versions (3.9-3.13) introduce significant syntax changes:
  - Python 3.8: Walrus operator (`:=`), positional-only parameters
  - Python 3.9: Type hinting improvements, dictionary union operator
  - Python 3.10: Pattern matching (`match`/`case`), parenthesized context managers
  - Python 3.11: Exception groups, improved error messages
  - Python 3.12: Type parameter syntax (PEP 695), f-string improvements
  - Python 3.13: Additional syntax enhancements

**Implication**: RedBaron cannot parse any modern Python code using post-3.7 syntax features.

### Maintenance Status

**Source**: https://github.com/pycqa/redbaron, https://opencollective.com/redbaron

**Development History**: "Until the end of 2018, the development has been a full volunteer work mostly done by Bram."

**Funding Attempts**: Project sought financial support through OpenCollective to continue development.

**Last Significant Update**: Development appears to have stalled around 2018-2019 based on version support.

**Assessment**: While not formally deprecated, the project has not kept pace with Python language evolution.

### Why Not Suitable

1. **Syntax Support Gap**: Cannot parse Python 3.8+ code (5+ years of Python evolution missed)
2. **No Active Development**: No evidence of ongoing work to add modern syntax support
3. **Unclear Maintenance**: No clear path to Python 3.11+ support
4. **Better Alternatives Exist**: LibCST provides similar Full Syntax Tree benefits with active maintenance

### Confidence in Elimination

**Confidence Level**: 10/10 - Very High

**Evidence Quality**: Official PyPI documentation clearly states version limits. No ambiguity.

**Reversibility**: Could only be reconsidered if:
- Project added Python 3.10+ syntax support
- Active maintenance resumed
- Both are unlikely given 5+ years of stagnation

---

## 2. Bowler - ELIMINATED

**Repository**: https://github.com/facebookincubator/Bowler
**PyPI**: https://pypi.org/project/bowler/
**Status**: Officially Archived

### Elimination Rationale

**Primary Reason**: Repository archived on August 8, 2025 - read-only, no future development

### Evidence

**Source**: https://github.com/facebookincubator/Bowler

**Archive Status**: "The repository was archived on August 8, 2025, and is now read-only."

**Stars**: 1,600 (shows historical interest)

**Official Deprecation Notice**:

**Quote**: "Bowler 0.x is based on fissix (a fork of lib2to3) which was never intended to be a stable api" and "we have reached the limit of being able to add new language features."

**Explicit Recommendation from Maintainers**:

**Quote**: "If you need to do codemods today, we recommend looking at LibCST codemods which are a bit more verbose, but work well on modern python grammars."

**Future Plans**: Maintainers indicated "a future Bowler 2.x built on libcst's parser is planned but unlikely to release during 2021 (noting this was written in 2021)."

**Current Date**: November 2025 - Bowler 2.x never materialized, repository now archived.

### Technical Limitations

**Based on lib2to3**: Bowler 0.x used lib2to3 (Python's 2to3 tool internals), which:
- Was never designed as a stable public API
- Limited in supporting new Python syntax
- Deprecated by Python core team (PEP 594 area)

**New Python Grammar Support**: Cannot handle modern Python features due to lib2to3 foundation.

### Why Not Suitable

1. **Archived Repository**: No bug fixes, no security updates, no support
2. **Maintainer Recommendation**: Facebook team explicitly recommends LibCST instead
3. **Technical Dead-End**: Built on deprecated lib2to3 infrastructure
4. **No Future Development**: Bowler 2.x never released, project abandoned

### Confidence in Elimination

**Confidence Level**: 10/10 - Absolute

**Evidence Quality**: Official repository status (archived) is indisputable. Maintainer recommendation is explicit.

**Reversibility**: Zero chance unless repository is unarchived and development resumes. Facebook has moved on.

---

## 3. Parso - ELIMINATED

**Repository**: https://github.com/davidhalter/parso
**PyPI**: https://pypi.org/project/parso/
**Status**: Active Project (but not suitable for this use case)

### Elimination Rationale

**Primary Reason**: Parso is a **parser**, not a **modification tool**

### Evidence

**Source**: https://parso.readthedocs.io/, https://github.com/davidhalter/parso

**Quote**: "Parso is a Python parser that supports error recovery and round-trip parsing for different Python versions."

**Official Description**: Parso can "parse Python code and analyze syntax trees, but is primarily a **parsing tool**, not a refactoring library."

**Future Work Acknowledgement**: README notes "there will be better support for refactoring and comments" as **future work** (not current capability).

### Primary Use Case

**Source**: PyPI page

**Main Usage**: "Powering the Jedi code completion/intelligence project"

**Dependent Projects**: ~586,000 (used extensively, but as a parsing backend for other tools)

**Assessment**: Parso is infrastructure for tools like Jedi (autocomplete), not a end-user refactoring library.

### What Parso Provides vs What's Needed

**Parso Provides**:
- Syntax parsing with error recovery
- Multiple Python version support
- AST generation
- Error detection and reporting

**What's Needed** (per requirements):
- Formatting preservation ✗ (Parso is a parser)
- Easy modification API ✗ (No transformation API documented)
- Code modification capabilities ✗ (Parsing only)

### Why Not Suitable

1. **Wrong Abstraction Level**: Parso is a parsing library, not a code modification library
2. **No Transformation API**: No documented visitor/transformer patterns for modifications
3. **Not Designed for This**: README explicitly says refactoring is future work
4. **Better Alternatives**: LibCST, rope, even AST provide modification capabilities

### Could It Be Used?

**Theoretical Usage**: One could build a modification tool *on top of* Parso.

**Practical Reality**:
- Would require significant additional work
- LibCST already exists (mature modification tool)
- Reinventing the wheel

**Assessment**: Not a viable choice when better-suited libraries exist.

### Confidence in Elimination

**Confidence Level**: 9/10 - Very High

**Evidence Quality**: Official documentation clearly describes parso as a parser. Future work statement confirms modification not current capability.

**Reversibility**: Could reconsider if:
- Parso adds documented modification API
- Community builds mature modification layer on top
- Neither is likely given LibCST's existence

---

## Summary Table

| Library | Primary Reason | Evidence Source | Confidence | Status |
|---------|---------------|-----------------|------------|---------|
| **RedBaron** | Python 3.7 max support | PyPI official page | 10/10 | Stagnant |
| **Bowler** | Archived August 2025 | GitHub archive status | 10/10 | Deprecated |
| **Parso** | Parser only, not modification tool | Official docs | 9/10 | Active but wrong tool |

---

## Eliminated vs Remaining

### Why These Were Considered Initially

**Source**: Community knowledge, tool surveys

All three libraries appear in discussions about Python AST manipulation:
- RedBaron: Historical Full Syntax Tree library (predates LibCST)
- Bowler: Facebook's codemod tool (appeared in Python tooling discussions)
- Parso: Parser used by popular tools (Jedi), sometimes confused as modification tool

### Why They Don't Compete With LibCST/Rope/AST

**RedBaron**: Could have competed, but abandoned before catching up to modern Python
**Bowler**: Explicitly deprecated in favor of LibCST by its own creators
**Parso**: Different purpose (parsing backend vs modification tool)

---

## Lessons from Eliminations

### Ecosystem Insights

1. **Maintainer Recommendations Matter**: Facebook's Bowler team recommending LibCST is strong evidence
2. **Python Version Support is Critical**: RedBaron's 3.7 limit makes it unusable for modern code
3. **Purpose Alignment**: Parso shows importance of matching tool to use case (parser ≠ modifier)

### S2 Methodology Validation

Comprehensive research revealed:
- Official deprecation notices (Bowler)
- Version support limitations (RedBaron)
- Tool purpose mismatches (Parso)

Without systematic multi-source analysis, these libraries might have been incorrectly included.

---

## Evidence Quality Assessment

**High Quality Evidence** (9-10/10):
- GitHub archive status (Bowler) - directly observable
- PyPI version limits (RedBaron) - authoritative source
- Official documentation purpose (Parso) - primary source

**No Ambiguity**: All eliminations supported by unambiguous, high-quality evidence.

**Confidence in Decisions**: 9.7/10 average - very confident these eliminations are correct.

---

## Addendum: Other Libraries Not Considered

### Why Not Analyzed

**astor**: Older AST-to-source library, superseded by `ast.unparse()` in Python 3.9+
**baron**: Lower-level library underlying RedBaron, same limitations
**typed-ast**: Merged into CPython in Python 3.8, now part of stdlib `ast`

These were not analyzed because:
- Superseded by stdlib functionality, or
- Lower-level infrastructure (not end-user libraries), or
- Same limitations as analyzed libraries

**Assessment**: Comprehensive search identified all major candidates. Remaining libraries in ecosystem are either niche or superseded.
