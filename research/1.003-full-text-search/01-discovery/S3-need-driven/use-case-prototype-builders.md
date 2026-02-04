# Use Case: Prototype & Proof-of-Concept Builders

## Who Needs This

**Persona**: Developers or tech leads building quick prototypes to validate product ideas, test feasibility, or demonstrate concepts to stakeholders.

**Context**:
- Hackathons, proof-of-concepts, MVPs, client demos
- Timeline: 2 hours to 2 weeks (not months)
- Uncertain if project will proceed beyond prototype
- No infrastructure budget for POC phase
- Using Python for rapid development
- Dataset: 1K-50K documents (test data or small production sample)

**Team size**: 1-3 developers, often solo

**Budget**: $0 (using free tier services, local development)

---

## Why They Need Full-Text Search

**Primary problem**: Prototype needs search functionality to demonstrate viability, but can't justify infrastructure investment before validation.

**Common scenarios**:
- **Hackathon**: "Build internal knowledge base search in 24 hours"
- **Client pitch**: "Demo search feature to win contract"
- **MVP validation**: "Test if users find search valuable before building full system"
- **Technical spike**: "Prove we CAN build search in-house before committing to Algolia"

**Time pressure**:
- No time to learn complex systems
- Can't spend days on deployment
- Need results fast to validate or pivot

---

## Their Requirements

### Installation Requirements (CRITICAL)
- **pip install only** - No system packages, no Docker, no Java
- **Works on laptop** - Can demo without internet or servers
- **Zero configuration** - Defaults should "just work"
- **5-minute setup** - From pip install to first search results

### Performance Requirements
- **Latency**: <100ms acceptable (prototype UX, not production)
- **Not a blocker**: Slow search OK if it works
- **Development speed >> runtime speed**

### Scale Requirements
- **Test dataset**: 1K-10K documents typical
- **Memory**: <1GB (runs on laptop)
- **Growth**: Not planning for scale at POC stage

### Feature Requirements (Minimal)
1. **Basic ranking** - Any ranking better than database LIKE
2. **Phrase search** - Nice to have, not required
3. **Filters** - If easy to add, otherwise skip
4. **Fuzzy search** - Defer to production if needed

### Must NOT Require
- ❌ Infrastructure setup (Docker, VMs, databases)
- ❌ Configuration files (YAML, JSON, environment variables)
- ❌ Reading 50-page documentation
- ❌ Debugging native code compilation

---

## Library Selection Criteria (From S1)

### Top Priority: Time-to-First-Result

**Decision rule**: From `pip install` to working search in <30 minutes.

### Evaluation Against S1 Libraries

| Library | Fits? | Why / Why Not |
|---------|-------|---------------|
| **Whoosh** | ✅ Perfect | Pure Python (zero deps), 10-line example works, in-memory mode for quick tests, BM25 ranking |
| **lunr.py** | ✅ Good | Simple API, but in-memory only (index regenerates on restart), TF-IDF (weaker ranking) |
| **Tantivy** | ⚠️ Maybe | Pre-built wheel (easy install), but less Pythonic API (Rust types), steeper learning curve |
| **Xapian** | ❌ No | System package install (`apt install python3-xapian`), breaks "pip only" constraint |
| **Pyserini** | ❌ No | Requires Java 21+, 50+ page docs, overkill for POC |

### Recommended Choice
**Primary**: **Whoosh**
- Pure Python (one `pip install whoosh`)
- Quick start code works immediately:
  ```python
  # 10 lines to working search (context, not tutorial)
  from whoosh.index import create_in
  from whoosh.fields import Schema, TEXT
  from whoosh.qparser import QueryParser

  schema = Schema(title=TEXT, content=TEXT)
  ix = create_in("indexdir", schema)
  # Add docs, search - it just works
  ```
- In-memory mode for demos (no disk I/O)
- BM25 ranking out-of-box

**Alternative**: **lunr.py** if static docs demo (no server)

---

## When to Consider Managed Services

**Generally DEFER** during POC phase:

### Why NOT Managed During POC
- **Cost validation first** - Don't pay $200/month before validating user need
- **Overkill** - Managed service features (analytics, A/B testing) unnecessary for demo
- **Commitment** - Prototype might get cancelled; monthly subscription is premature

### When to SWITCH to Managed
**Trigger**: POC validated, proceeding to production.

**Decision flow**:
1. **POC phase**: Use Whoosh (free, fast setup)
2. **Validation**: Users find search valuable → green light for production
3. **Production decision**:
   - If scale <1M docs + technical team → **Tantivy** (DIY production-ready)
   - If scale >1M docs OR non-technical team → **Algolia/Typesense** (managed)

**Key insight**: Whoosh gets you to validation fast. Don't over-invest before validation.

---

## Real-World Examples

**Hackathon projects**:
- "Search 10K Stack Overflow questions" - Whoosh, 2 hours
- "Internal wiki search" - lunr.py, static site, 4 hours
- "Product catalog search" - Whoosh, 8 hours

**MVPs that validated and scaled**:
- POC: Whoosh (1K products, solo developer, 1 week)
- Production v1: Tantivy (50K products, scaled to 10K users)
- Production v2: Algolia (500K products, 100K users, international)

**POCs that got cancelled**:
- "We built search in 3 days, tested with 10 users, they didn't use it"
- **Cost of failure**: 3 days developer time, $0 infrastructure
- **Validation**: Search not valuable for this user base; pivot to different feature

---

## Success Metrics for Prototypes

How prototype builders know their library choice worked:

✅ **Good fit indicators**:
- Got search working in <1 day
- Demo impressed stakeholders
- Able to pivot quickly when requirements changed
- No infrastructure costs during POC phase
- Validated user need before investing in production

⚠️ **When prototype becomes production** (warning signs):
- Demo is "good enough" → deployed to real users
- 10 users became 1000 users
- 64ms latency (Whoosh) now causing complaints
- Dataset grew from 10K to 100K documents

**Danger**: Prototype code in production = technical debt. Plan migration to Tantivy or managed service.

---

## The "Prototype to Production" Trap

**Common mistake**: Deploying Whoosh prototype to production without refactoring.

**Why it's tempting**:
- "It works fine in the demo!"
- Pressure to ship fast
- "We'll refactor later" (never happens)

**Why it causes problems**:
- Whoosh aging codebase (2020), Python 3.12 warnings
- 64ms latency degrades to 200ms+ under load
- No support for scale (1M doc ceiling)
- Technical debt compounds over time

**Correct approach**:
1. POC with Whoosh (1 week)
2. Validate with users (1-2 weeks)
3. **Refactor to Tantivy BEFORE production** (1 week)
4. Ship production-ready system

**Time saved by correct approach**: 2 weeks upfront vs 3+ months fixing production issues later.

---

## Integration Complexity: POC vs Production

**POC integration** (Whoosh):
- 50-100 lines of Python
- In-memory index (no persistence complexity)
- No error handling (demo code)
- No monitoring, logging, alerting

**Production integration** (Tantivy or managed):
- 300-500 lines (error handling, retries, monitoring)
- Persistent storage (disk or cloud)
- Index update pipeline (background workers)
- Monitoring, alerting, logging
- User-facing error messages
- A/B testing, analytics

**Gap**: 5× complexity increase from POC to production. Plan accordingly.

---

## Validation Against S1 Findings

S1 noted:
- **Whoosh** = pure Python, easy install, 10K-1M docs, aging codebase
- **Rating**: ⭐⭐⭐⭐ (4/5) - "Best for: Prototypes, Python-only environments"

**S3 validation**: Prototype builders are Whoosh's PERFECT use case:
- Need fast setup (✅ pip install, 10-line example)
- Small scale (✅ POC uses 1K-10K test docs)
- Zero budget (✅ No infrastructure costs)
- Uncertain future (✅ Don't over-invest before validation)

**Alignment**: S1's "prototypes" recommendation validated by S3 persona analysis.

**Gap identified**: S1 didn't emphasize "don't deploy Whoosh to production." S3 clarifies: Whoosh for POC, Tantivy for production.

---

## Recommendation: Two-Phase Approach

**Phase 1: Validation (Week 1-2)**
- Library: **Whoosh**
- Goal: Prove search is valuable to users
- Cost: $0
- Risk: Low (can discard if not valuable)

**Phase 2: Production (Week 3-4)**
- If validated → Refactor to **Tantivy** (or **managed service**)
- If not validated → Cancel project, saved $1000s by not building production system

**Key insight**: Whoosh is a validation tool, not a production tool. Use it to learn, then upgrade.
