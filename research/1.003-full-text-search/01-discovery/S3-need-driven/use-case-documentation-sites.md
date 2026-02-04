# Use Case: Technical Writers & Documentation Site Builders

## Who Needs This

**Persona**: Technical writers, documentation engineers, or developers maintaining static documentation sites.

**Context**:
- Building documentation for open-source projects, APIs, or internal tools
- Using static site generators (MkDocs, Docusaurus, Sphinx, Hugo)
- Publishing to GitHub Pages, Netlify, or similar hosting
- No server-side processing (pure static HTML/CSS/JS)
- Dataset size: 100-5K documentation pages

**Team size**: 1-3 people, often solo maintainers

**Budget**: $0 (free hosting), no backend infrastructure

---

## Why They Need Full-Text Search

**Primary problem**: Users can't find information in documentation without search. Table of contents is insufficient for large doc sites.

**User frustration scenario**:
> "I know this library supports rate limiting, but where is it documented? I've clicked through 20 pages and can't find it."

**Business impact**:
- Poor docs search = support tickets
- Good search = self-service = less support load
- Fast search = better developer experience = library adoption

**Why NOT Google Custom Search or Algolia DocSearch**:
- **Google CSE**: Indexes entire site (includes navigation, footers), low relevance, ads on free tier
- **Algolia DocSearch**: Great but limited to open-source projects, requires application approval
- **Control**: Want to own the search experience, no external dependencies

---

## Their Requirements

### Deployment Constraints (CRITICAL)
- **Static hosting only** - No backend server, no Python/Node runtime
- **Client-side search** - JavaScript runs search in browser
- **Index generation** - Build search index at docs build time, serve as static JSON
- **File size** - Search index must be <5MB (download penalty)

### Performance Requirements
- **Initial load**: <1 second to download + parse index
- **Query latency**: <100ms (client-side, acceptable for docs)
- **Indexing time**: Negligible (happens at build time, not user-facing)

### Scale Requirements
- **Page count**: 100-5K pages typical
- **Index size**: <5MB for fast download
- **Growth**: Slow (docs grow incrementally)

### Feature Requirements
- **Basic ranking** - TF-IDF acceptable (BM25 nice-to-have)
- **Phrase search** - Match exact terms
- **Highlighting** - Show matching snippets
- **Multi-field** - Search titles, headings, body text

### Must NOT Require
- ❌ Server-side runtime (Python, Node)
- ❌ Database or persistent storage
- ❌ Docker containers or VMs
- ❌ Monthly hosting costs

---

## Library Selection Criteria (From S1)

### Top Priority: Static Site Compatibility

**Decision rule**: Library must support **pre-built index** that loads in browser.

### Evaluation Against S1 Libraries

| Library | Fits? | Why / Why Not |
|---------|-------|---------------|
| **lunr.py** | ✅ Perfect | Designed for static sites, Lunr.js interop, builds JSON index, <1MB typical |
| **Whoosh** | ❌ No | Requires Python runtime, can't run in browser |
| **Tantivy** | ❌ No | Native binary format, can't run in browser, overkill |
| **Xapian** | ❌ No | C++ library, requires server-side processing |
| **Pyserini** | ❌ No | JVM required, way too heavy for static sites |

### Recommended Choice
**Primary**: **lunr.py**
- Builds static JSON index at docs generation time
- JavaScript version (Lunr.js) runs search in browser
- Interop: Python builds index, JS searches it
- Typical index size: 500KB-1MB for 1K pages

**No fallback**: If static hosting is non-negotiable, lunr.py is the only option from S1 libraries.

---

## When to Consider Managed Services

**Trigger points for Path 3 (Algolia DocSearch, Typesense Cloud)**:

### Scale Triggers
- **>5K pages** - lunr.py index size grows linearly, >5MB = slow page load
- **Fast-changing docs** - Need instant index updates without rebuilding entire site
- **Multi-version docs** - Search across v1.x, v2.x, v3.x simultaneously

### Feature Triggers
- **Typo tolerance** - lunr.py has basic fuzzy, but not as good as Algolia
- **Analytics** - Track what users search for, identify doc gaps
- **Faceted search** - Filter by version, language, topic
- **Personalization** - Show results based on user role or history

### Community Size Triggers
- **Open-source with 10K+ stars** - Eligible for Algolia DocSearch (free)
- **Commercial docs** - Algolia or Typesense paid tier worth it for UX

### Cost Considerations
**DIY (lunr.py)**:
- Hosting: $0 (GitHub Pages, Netlify)
- Engineering: 1-2 days setup + 1 hour/month maintenance

**Managed (Algolia DocSearch)**:
- Open-source: $0 (if approved)
- Commercial: $39-149/month (starter plans)
- Engineering: 2-4 hours setup + 0 hours/month maintenance

**Break-even**: If commercial, managed services worth it at $149/month when team values UX over cost.

---

## Real-World Examples

**Who uses lunr.py or Lunr.js?**:
- **MkDocs** - Default search (lunr.js)
- **Hugo** - Static search via lunr.js
- **Small open-source projects** - Python libs, frameworks
- **Internal wikis** - Markdown docs + static hosting

**Who uses Algolia DocSearch?**:
- **Large OSS projects** - React, Vue, Bootstrap, Django
- **API docs** - Stripe, Twilio (commercial, paid Algolia)

---

## Implementation Pattern (Not S3 Scope, But Context)

For context on WHY lunr.py is suitable (not HOW to implement):

**Build time** (Python):
1. Docs generator (MkDocs, Sphinx) builds HTML pages
2. lunr.py indexes content, generates `search-index.json` (~500KB)
3. Static site includes Lunr.js library + index JSON

**User's browser** (JavaScript):
1. Page loads, downloads `search-index.json`
2. Lunr.js parses index into memory (~50ms)
3. User types query, Lunr.js searches in-memory index (<100ms)
4. Results rendered instantly (no backend API call)

**Key insight**: Entire search stack runs in user's browser. Zero server cost.

---

## Success Metrics

How documentation maintainers know lunr.py is working:

✅ **Good fit indicators**:
- Index size <2MB (fast page load)
- Search returns relevant results for common queries
- No user complaints about slow/broken search
- Build time <30 seconds for search index generation

⚠️ **Warning signs to reconsider**:
- Index size >5MB (page load penalty)
- Users report irrelevant results
- Feature requests: "Why no fuzzy search?", "Can we search code examples?"
- Doc site >5K pages

---

## Special Considerations

### Multi-Language Documentation
lunr.py supports 16 languages via stemming plugins:
- English, Spanish, French, German, Italian, Portuguese, Russian, Turkish, etc.
- CJK languages: Japanese (tokenization plugin), Chinese/Korean limited

**Trade-off**: For CJK-heavy docs, might need different solution (or accept lower relevance).

### Code Search in Docs
**Problem**: Users want to search code examples, not just prose.

**lunr.py limitation**: Treats code as text, no syntax awareness.

**Workaround**: Index code blocks separately with `language: python` metadata, boost relevance for code-focused queries.

---

## Validation Against S1 Findings

S1 noted:
- **lunr.py** = lightweight, in-memory, static sites, 1K-10K docs
- **Rating**: ⭐⭐⭐ (3/5) - "Best for: Static site search, 1K-10K docs"

**S3 validation**: Documentation site builders are lunr.py's PRIMARY use case:
- Need static hosting (✅ lunr.py = only static-compatible option from S1)
- Small scale (✅ 100-5K pages typical, lunr.py handles <10K)
- Zero budget (✅ No server costs)
- Technical maintainers (✅ Can integrate lunr.py into build pipeline)

**Alignment**: lunr.py was designed for this exact persona. Perfect fit.

**Gap identified**: For large doc sites (>5K pages) or advanced features, S1 libraries insufficient → Path 3 (Algolia DocSearch) becomes necessary.
