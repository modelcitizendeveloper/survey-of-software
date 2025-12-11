# QRCards Trie Routing: Recommendation for In-Memory Implementation

**Application**: QRCards
**Date**: 2025-10-10
**Purpose**: Technical recommendation for URL routing using in-memory trie data structure
**Status**: Enables weekend implementation project

---

## Executive Summary

**Recommendation**: Use **pygtrie in-memory** for QRCards URL routing, NOT Redis.

**Why**: Your scale (50-50k routes, <1000 requests/day) doesn't justify Redis complexity. An in-memory Python trie is:
- **Faster**: <1ms vs 1-5ms Redis network latency
- **Simpler**: Zero external dependencies, no deployment complexity
- **Sufficient**: 5MB memory footprint for 50k routes
- **Easier to debug**: Pure Python, no distributed state

**Migration Path**: Start with pygtrie → only move to Redis if traffic exceeds 10k requests/day OR you need multi-server deployment.

---

## Problem Statement

**Current State** (from routing-architecture-memo.md):
- QRCards generates dynamic URLs from database records
- One activity record → infinite navigable paths (e.g., `/seattle/capitol-hill/coffee-shops/vivace`)
- Current routing: Hardcoded patterns or database lookups per request
- Performance target: <50ms response time

**Original Proposal** (from redis-trie-routing-implementation.md):
- Use Redis to store trie structure
- Populate Redis keys with path prefixes
- O(1) lookups via Redis GET commands

**Why Redis is Over-Engineered**:
1. **Scale mismatch**: Redis designed for 10k+ req/sec, you have <1000 req/day
2. **Latency cost**: Network round-trip to Redis (1-5ms) > in-memory lookup (<0.1ms)
3. **Deployment complexity**: Need Redis hosting, connection management, error handling
4. **Cost**: $0-7/month for Redis vs $0 for in-memory
5. **Debugging**: Distributed state harder to inspect than local memory

---

## Recommended Solution: In-Memory Pygtrie

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Flask Application Startup                                    │
│                                                               │
│  1. Load SQLite database                                     │
│  2. Build pygtrie.StringTrie in memory                       │
│  3. Populate trie with all path → activity_id mappings       │
│  4. Ready to serve requests                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Request Handling (per request)                               │
│                                                               │
│  1. Extract URL path from request                            │
│  2. Lookup path in trie → activity_id (O(path_length))       │
│  3. If found: Load activity from SQLite, render template     │
│  4. If not found: 404                                        │
└─────────────────────────────────────────────────────────────┘
```

**Key Insight**: Build trie once at startup, use for all requests. No rebuilding needed until app restarts or data changes.

---

## Implementation

### Step 1: Install pygtrie

```bash
pip install pygtrie
```

**Why pygtrie?** (from 1.042-trie-libraries discovery):
- Pure Python (no C compilation)
- Google-backed (stable, well-maintained)
- 100k-500k operations/sec (sufficient for <1000 req/day)
- 100-300 bytes per key (5MB for 50k routes)

---

### Step 2: Build Trie at Startup

```python
# app.py or __init__.py
from flask import Flask, render_template, abort
import pygtrie
from models import db, Activity, Destination, Group, Trip

app = Flask(__name__)

# Global trie (built once at startup)
route_trie = None

@app.before_first_request
def build_route_trie():
    """
    Build in-memory trie from database.
    Runs once when first request arrives.
    """
    global route_trie

    print("Building route trie from database...")
    route_trie = pygtrie.StringTrie(separator='/')

    # Query all activities with their full path context
    activities = db.session.query(
        Activity.id,
        Activity.slug.label('activity_slug'),
        Destination.slug.label('destination_slug'),
        Group.slug.label('group_slug'),
        Trip.slug.label('trip_slug')
    ).join(
        Destination, Activity.destination_id == Destination.id
    ).join(
        Group, Destination.group_id == Group.id
    ).join(
        Trip, Group.trip_id == Trip.id
    ).all()

    # Populate trie with all paths
    for activity in activities:
        # Build full path
        path = f"{activity.trip_slug}/{activity.group_slug}/{activity.destination_slug}/{activity.activity_slug}"

        # Store activity ID in trie
        route_trie[path] = activity.id

    print(f"Route trie built: {len(route_trie)} paths indexed")
    print(f"Memory usage: ~{len(route_trie) * 200} bytes (~{len(route_trie) * 200 / 1024 / 1024:.2f} MB)")
```

---

### Step 3: Universal Route Handler

```python
@app.route('/<path:url_path>')
def universal_handler(url_path):
    """
    Universal route handler using trie lookup.

    Handles all dynamic paths:
    - /seattle/capitol-hill/coffee-shops/vivace
    - /portland/pearl-district/restaurants/le-pigeon
    - etc.
    """
    # Lookup path in trie
    activity_id = route_trie.get(url_path)

    if activity_id is None:
        # Path not found → 404
        abort(404)

    # Load activity from database
    activity = Activity.query.get(activity_id)

    if activity is None:
        # Stale trie entry (activity deleted) → 404
        abort(404)

    # Render activity page
    return render_template('activity.html', activity=activity)
```

---

### Step 4: Handle Trie Invalidation (Optional)

If you add/update/delete activities, you need to rebuild the trie:

```python
def rebuild_route_trie():
    """
    Rebuild trie after database changes.
    Call this after admin actions that modify routes.
    """
    global route_trie

    # Clear existing trie
    route_trie.clear()

    # Rebuild (same logic as build_route_trie)
    activities = db.session.query(...).all()
    for activity in activities:
        path = f"{activity.trip_slug}/{activity.group_slug}/{activity.destination_slug}/{activity.activity_slug}"
        route_trie[path] = activity.id

    print(f"Route trie rebuilt: {len(route_trie)} paths")

# Call after admin actions
@app.route('/admin/activities/create', methods=['POST'])
def create_activity():
    # ... create activity logic ...
    db.session.commit()

    # Rebuild trie to include new activity
    rebuild_route_trie()

    return redirect('/admin/activities')
```

**Alternative**: Restart app after database changes (acceptable for <1000 req/day).

---

## Performance Analysis

### Benchmark Expectations (from 1.042 discovery)

| Metric | pygtrie (In-Memory) | Redis (Managed) |
|--------|---------------------|-----------------|
| **Lookup latency** | <0.1ms | 1-5ms (network) |
| **Throughput** | 100k-500k ops/sec | 10k-50k ops/sec (network limited) |
| **Memory per route** | 100-300 bytes | 50-100 bytes |
| **Total memory (50k routes)** | 5-15 MB | 2.5-5 MB |
| **Build time (50k routes)** | <100ms | 200-500ms (network) |

**For your scale (<1000 req/day)**:
- pygtrie can handle **100× your traffic** without breaking a sweat
- Lookup latency <1ms meets your <50ms target with 50× headroom
- Memory footprint (5-15MB) is negligible for modern Python apps

---

## Migration Path to Redis (If Needed)

**When to migrate**:
- ✅ Traffic exceeds 10,000 requests/day (13 req/min sustained)
- ✅ Multi-server deployment needed (trie state must be shared)
- ✅ Routes change frequently (>10 updates/hour)
- ❌ Otherwise, stick with in-memory

**How to migrate** (from 2.033 discovery):
1. Start with **Render Redis free tier** (25MB, $0/month)
2. Replace `pygtrie` with Redis `GET` commands
3. Populate Redis on deployment (not per-request)
4. Keep in-memory trie as L1 cache, Redis as L2 (optional)

**Cost**: $0/month (free tier) → $7/month (Render Starter) if >10k routes

---

## Comparison to Original Redis Proposal

| Aspect | Original (Redis Trie) | Recommended (pygtrie In-Memory) |
|--------|----------------------|-------------------------------|
| **Complexity** | High (Redis hosting, connections, error handling) | Low (pure Python, no dependencies) |
| **Latency** | 1-5ms (network) | <0.1ms (memory) |
| **Cost** | $0-7/month | $0 |
| **Deployment** | Need Redis service | Just deploy Flask app |
| **Debugging** | Inspect Redis keys (external tool) | Print trie in debugger |
| **Scalability** | Supports distributed (multi-server) | Single-server only |
| **When to use** | >10k req/day OR multi-server | <10k req/day AND single-server |

**Verdict**: Redis is a premature optimization for QRCards' current scale.

---

## Unlocking Weekend Project

**From routing-architecture-memo.md**: "Recommendation: DEFER routing optimization. Ship pages first."

**Counter-argument**: pygtrie in-memory is SO simple that it doesn't count as "premature optimization":
- 30 lines of code (vs 200+ for Redis)
- <1 hour implementation time
- Zero operational complexity
- Zero cost

**Recommendation**: Implement pygtrie routing NOW if:
1. You have dynamic path generation working
2. You want cleaner URL structure
3. You can spare 1-2 hours over the weekend

**Don't implement if**:
- Dynamic paths not yet designed
- You have higher-priority features (e.g., content templates, user accounts)
- You're still validating product-market fit

---

## Implementation Checklist

**Weekend Project Scope**:

- [ ] **Install pygtrie**: `pip install pygtrie` (1 min)
- [ ] **Write build_route_trie()**: Copy code from Step 2 above (15 min)
- [ ] **Write universal_handler()**: Copy code from Step 3 above (10 min)
- [ ] **Test with sample data**: Create 10-50 test routes (20 min)
- [ ] **Benchmark**: Measure lookup latency (10 min)
- [ ] **Deploy**: Push to PythonAnywhere or Render (15 min)
- [ ] **Monitor**: Check memory usage, response times (10 min)

**Total time**: 1.5 hours

---

## Strategic Assessment

**Why This Unlocks Progress** (vs waiting per routing-architecture-memo.md):

1. **Low risk**: If it doesn't work, revert in 5 minutes (just remove route handler)
2. **High learning**: Understand trie performance in production
3. **Enables A/B testing**: Compare hardcoded routes vs dynamic routes
4. **Unblocks content team**: Can design URL structure knowing it's performant

**Risks of Waiting**:
- Harder to change URL structure after shipping hardcoded routes
- Team momentum lost (architecture paralysis)
- Missed opportunity to validate performance assumptions

**Recommendation**: Ship pygtrie routing this weekend, gather metrics for 1-2 weeks, then decide if optimization needed.

---

## References

**Spawn Solutions Experiments**:
- **1.042-trie-libraries**: Comprehensive analysis of pygtrie, datrie, marisa-trie
  - `experiments/1.042-trie-libraries/01-discovery/SYNTHESIS.md`: "Use pygtrie for MVP, datrie for production"
  - `experiments/1.042-trie-libraries/01-discovery/S2_COMPREHENSIVE_DISCOVERY.md`: Performance benchmarks (100k-500k ops/sec)

- **2.033-redis-hosting**: Redis hosting services evaluation
  - `experiments/2.033-redis-hosting/01-discovery/DISCOVERY_SYNTHESIS.md`: "Render free tier (25MB, $0) perfect for trie routing (5MB)"
  - `experiments/2.033-redis-hosting/01-discovery/S3_NEED_DRIVEN_DISCOVERY.md`: When to use Redis vs in-memory

**QRCards Documents**:
- `qrcards/project/features/intelligence-content-templates/2025-10-09-1708-caching-strategy-dynamic-paths.md`: Multi-tier caching proposal (L1 + L2)
- `qrcards/project/features/intelligence-content-templates/2025-10-09-1803-routing-architecture-memo.md`: Routing options analysis (defer recommendation)
- `applications/qrcards/redis-trie-routing-implementation.md`: Original Redis trie proposal (superseded by this document)

---

## Next Steps

### Immediate (This Weekend)
1. Implement pygtrie routing (1.5 hours)
2. Deploy to staging environment
3. Test with 50-100 sample routes

### Short Term (Week 1-2)
1. Monitor memory usage (expect 5-15MB)
2. Measure P50/P95/P99 latency (expect <1ms)
3. Gather user feedback on URL structure

### Medium Term (Month 1-3)
1. If traffic >1000 req/day: Consider caching layer (cachetools)
2. If traffic >10k req/day: Re-evaluate Redis migration
3. If multi-server deployment: Implement Redis (Render free tier)

### Long Term (Month 6+)
1. Benchmark against datrie (if memory becomes issue)
2. Consider marisa-trie if >100k routes (5-10× memory reduction)
3. Re-run 2.033 analysis if Redis becomes justified

---

## Conclusion

**Verdict**: Use pygtrie in-memory for QRCards URL routing.

**Why**: Simpler, faster, cheaper, and sufficient for your scale. Redis is a solution looking for a problem.

**Impact**: Unlocks weekend implementation project without operational complexity or cost.

**Validation**: Cross-referenced against 1.042 (trie libraries) and 2.033 (Redis hosting) discoveries. Both confirm in-memory is appropriate for <10k req/day.

---

**Status**: Ready for implementation
**Confidence**: High (validated by two MPSE experiments)
**Risk**: Low (1.5 hour implementation, zero cost, easy rollback)
**Recommendation**: Ship it this weekend 🚀

---

## Appendix: Code Reference

**Full implementation** (copy-paste ready):

```python
# app.py
from flask import Flask, render_template, abort
import pygtrie
from models import db, Activity, Destination, Group, Trip

app = Flask(__name__)
route_trie = None

@app.before_first_request
def build_route_trie():
    global route_trie
    route_trie = pygtrie.StringTrie(separator='/')

    activities = db.session.query(
        Activity.id,
        Activity.slug.label('activity_slug'),
        Destination.slug.label('destination_slug'),
        Group.slug.label('group_slug'),
        Trip.slug.label('trip_slug')
    ).join(Destination).join(Group).join(Trip).all()

    for activity in activities:
        path = f"{activity.trip_slug}/{activity.group_slug}/{activity.destination_slug}/{activity.activity_slug}"
        route_trie[path] = activity.id

    print(f"Route trie built: {len(route_trie)} paths")

@app.route('/<path:url_path>')
def universal_handler(url_path):
    activity_id = route_trie.get(url_path)
    if activity_id is None:
        abort(404)

    activity = Activity.query.get(activity_id)
    if activity is None:
        abort(404)

    return render_template('activity.html', activity=activity)
```

**That's it.** 30 lines of code, 1.5 hours of work, weekend project unlocked.
