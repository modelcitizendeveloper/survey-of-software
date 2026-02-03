# Research Integration Scripts

Automation tools for the research workflow.

## integrate_research.py

Identifies research pieces that have been converted but not yet integrated into the site.

**Usage:**
```bash
python3 scripts/integrate_research.py          # Run integration
python3 scripts/integrate_research.py --dry-run  # Preview changes
```

**What it does:**
- Scans `docs/survey/*.md` for converted research
- Checks `docs/survey/index.md` for linked entries
- Checks `sidebars.ts` for sidebar entries
- Reports missing or stub entries

**Current limitations:**
- Does not automatically modify files (reports only)
- User must manually update index.md and sidebars.ts
- Future: Add automatic file modification with TDD tests

**Manual steps after running script:**

1. **Update docs/survey/index.md:**
   - Replace stub entries (no checkmark/link) with full linked entries
   - Format: `- ✅ [**1.XXX** Title](/survey/1-xxx) - description`

2. **Update sidebars.ts:**
   - Add missing entries in numerical order
   - Format: `{type: "doc", id: "survey/1-xxx"}`

3. **Update section counts:**
   - Count completed research in each section
   - Update "**Completed: X/Y**" headers

## tests/

Test suite for integration automation (TDD approach).

Run tests:
```bash
pytest scripts/tests/
```
