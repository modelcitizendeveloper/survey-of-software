# Research Site Integration Guide

## Post-Polecat Integration Checklist

When integrating converted research from polecats into the public site:

### 1. Run Conversion
```bash
python3 convert_research.py
```
This converts `packages/research/*` to `docs/survey/*.md`

### 2. Update Survey Catalog (`docs/survey/index.md`)

**Add new entries in numerical order:**

For sub-topics (e.g., 1.035.1):
```markdown
- **1.035** Tokenization - Wordpiece, BPE, SentencePiece
  - ✅ [**1.035.1** Chinese Tokenization](/survey/1-035-1) - jieba, pkuseg, word segmentation
```

For main topics (e.g., 1.173):
```markdown
- ✅ [**1.173** Terminology Extraction](/survey/1-173) - KeyBERT, PyATE, YAKE, spaCy
```

**Update section counts:**
```markdown
## 1.030-039: String & Text Algorithms
**Completed: 8/10**  ← Increment this
```

**Update total counts at bottom:**
```markdown
**Total Defined**: 189 research slots
**Completed**: 51 pieces (27%)  ← Update both numbers
**Remaining**: 138 pieces
```

### 3. Update Homepage (`docs/index.md`) - If Needed

Only update if this is a significant addition worth highlighting in "Recent Additions":

```markdown
## 🔍 Recent Additions

**2. Language-Specific Variants** (1.xxx.n)
- 1.035.1: Chinese Tokenization Strategies (jieba, pkuseg, word segmentation)
- 1.154.1: Chinese Text Simplification (MCTS dataset, neural approaches)
```

### 4. Update Sidebar (`sidebars.ts`)

Add entries in numerical order:
```typescript
{type: "doc", id: "survey/1-035-1"},
{type: "doc", id: "survey/1-154-1"},
{type: "doc", id: "survey/1-166"},
{type: "doc", id: "survey/1-173"},
```

### 5. Verify Locally

```bash
npm start
# Check http://localhost:3000/survey
# Verify new topics appear in sidebar AND catalog page
```

### 6. Commit & Push

```bash
git status
git add docs/survey/*.md docs/index.md docs/survey/index.md sidebars.ts
git commit -m "docs: Integrate <topic-name> research

- Add 1.xxx.y to survey catalog
- Update sidebar and counts
- <any other changes>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
git push
```

## Common Mistakes

❌ **Only updating homepage** - Survey catalog page won't show new topics
❌ **Forgetting section counts** - "Completed: X/10" gets stale
❌ **Wrong sidebar format** - Use `survey/1-035-1` not `1-035-1`
❌ **Not testing locally** - Dev server caches aggressively, do hard refresh

## Two Index Files

The site has **TWO index pages** that need updating:

1. **`docs/index.md`** - Homepage (/) - Optional, only for significant updates
2. **`docs/survey/index.md`** - Survey catalog (/survey) - **ALWAYS update this**

Users typically browse `/survey` to see all research, so that's the critical one.
