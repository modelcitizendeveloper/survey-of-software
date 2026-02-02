# Use Case: Software Testing Engineers

## Who Needs This

**Persona:** QA engineers, test automation developers, software testers

**Context:**
- Writing unit tests, integration tests, end-to-end tests
- Comparing expected vs actual outputs (text, JSON, objects)
- Generating readable failure messages when tests fail
- Working in CI/CD pipelines (fast execution required)

**Scale:**
- 100s-1000s of test assertions per project
- Test runs multiple times per day (PR checks)
- Some tests compare large outputs (logs, API responses)

**Constraints:**
- Minimize test dependencies (prefer stdlib)
- Fast execution (tests run frequently)
- Readable failure output (developers need to debug quickly)
- Cross-platform (tests run on dev machines + CI servers)

## Why They Need It

**Problem:** Assertions like `assert actual == expected` fail with unhelpful messages:
```
AssertionError: {'user': 'alice', 'status': 'active', ...} != {'user': 'alice', 'status': 'inactive', ...}
```
Developers can't see what differs in large outputs.

**Requirements:**
- **MUST**: Show exactly what differed (not just "not equal")
- **MUST**: Work with text, objects, JSON, XML
- **MUST**: Fast execution (no 100ms overhead per assertion)
- **SHOULD**: Readable output (humans debug from this)
- **SHOULD**: Minimal dependencies (avoid dependency conflicts)

**Anti-Requirements:**
- No git integration needed (not diffing code, diffing test outputs)
- No semantic code analysis (comparing data, not parsing code)
- No patch application (just comparison for validation)

## Library Fit Analysis

### Recommended Solutions

**For text/string comparison:**
→ **difflib** (stdlib)
- ✅ Zero dependencies
- ✅ Fast enough for most cases
- ✅ Unified diff output (readable)
- ✅ Already available in test environment
- ⚠️ Limit to <100KB outputs (performance degrades)

**For Python objects/dicts:**
→ **DeepDiff**
- ✅ Type-aware (catches int vs str mistakes)
- ✅ Deep recursion (nested structures)
- ✅ Readable output (shows exact paths changed)
- ✅ Ignore rules (skip timestamps, UUIDs in comparisons)
- ⚠️ External dependency (but very popular, low risk)

**For JSON API responses:**
→ **DeepDiff** or **jsondiff**
- DeepDiff: More features, better type handling
- jsondiff: RFC 6902 standard format, CLI tool
- Both handle JSON well, pick based on preference

**For XML outputs:**
→ **xmldiff** (if structure matters) or **difflib** (if text is sufficient)
- xmldiff for when attribute order, whitespace shouldn't fail tests
- difflib for simple XML where text comparison works

### Anti-Patterns

**❌ DON'T use GitPython:**
- Overkill (spawns git process per comparison)
- Requires git installed on CI servers
- Slower than dedicated diff libraries

**❌ DON'T use tree-sitter:**
- Massive overkill for test assertions
- Slow (parsing overhead)
- Complex setup (grammars, build tools)

**❌ DON'T use python-Levenshtein alone:**
- Edit distance doesn't show what changed
- No context (just a similarity score)

### Decision Factors

**Choose difflib when:**
- Comparing text/string outputs
- Want zero dependencies
- Files <100KB

**Choose DeepDiff when:**
- Comparing Python objects, dicts, lists
- Need type awareness (int vs str matters)
- Want ignore rules (skip dynamic fields)

**Choose jsondiff when:**
- Comparing JSON and want RFC 6902 format
- Using CLI tools alongside Python tests

**Choose xmldiff when:**
- Comparing XML and text diff is too noisy
- Structural equivalence matters (attribute order doesn't)

## Validation Criteria

**You picked the right library if:**
- ✅ Test failures show exactly what changed (no detective work)
- ✅ Tests run fast (<5% overhead from diff computation)
- ✅ No dependency conflicts in CI/CD
- ✅ Developers can debug from diff output alone

**Red flags (wrong choice):**
- ❌ Tests time out on large outputs (difflib on huge files)
- ❌ Diff output harder to read than raw dumps
- ❌ Can't install in test environment (too many dependencies)
- ❌ False failures from irrelevant differences (attribute order in XML)

## Common Patterns

**Pattern: Hybrid approach**
```
# Use different libraries for different data types
if comparing text → difflib
if comparing objects → DeepDiff
if comparing JSON → DeepDiff or jsondiff
```

**Pattern: Fallback strategy**
```
1. Try stdlib (difflib) first
2. If output unreadable or too slow → add DeepDiff
3. If still insufficient → specialized library (xmldiff, etc.)
```

## Real-World Example

**Scenario:** Testing a REST API that returns JSON

**Requirements:**
- Compare response against expected JSON
- Ignore timestamp fields (always different)
- Detect type changes (number vs string)
- Show which nested field changed

**Solution:** DeepDiff with ignore rules
- Handles JSON natively (Python dict)
- `exclude_paths` to skip timestamps
- Type-aware comparison
- Shows exact path to changed field

**Why not difflib:** Converts JSON to text, loses structure, can't ignore specific fields easily

**Why not jsondiff:** Less flexible ignore rules than DeepDiff
