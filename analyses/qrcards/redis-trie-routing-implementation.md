# Redis Trie Routing: Implementation Specification

**Date:** 2025-10-09
**Application:** QRCards Intelligence Platform
**Subject:** Redis-based URL routing using prefix tree (trie) structure
**Status:** Reference Implementation (On Hold - Priorities: Ship Pages First)

---

## Context: Architectural Evolution (When Ready)

**Current Priority:** Get pages live, deliver value to users
**This Document:** Future reference for when URL routing becomes a bottleneck

This specification describes a **Redis trie-based routing system** as an alternative to:
- Complex SQL JOINs for path resolution
- Explicit path records in database tables
- Dynamic generation with complex caching

**When to implement this:**
- Current routing becomes measurably slow (>100ms response times)
- Trip structures grow to 100+ activities
- You're already migrating to Render (Redis infrastructure available)

**For now:** Use whatever gets pages live fastest. This is here when you need it.

---

## Executive Summary

**Problem:** URL routing is fundamentally a **tree traversal problem**, not a relational query problem.

**Solution:** Use Redis as a **prefix tree (trie)** for O(1) path lookups.

```
Traditional (SQLite):
/bcbs-239/chapter-1/principles → Complex JOIN query (20-50ms)

Redis Trie:
/bcbs-239/chapter-1/principles → Single key lookup (<1ms)
```

**Architecture:**
```
SQLite (source of truth)
  ↓ generates (when trip structure changes)
Redis Trie (materialized routing table)
  ↓ resolves (on every request)
Fast path resolution
```

**Cost:** $0-7/month (Redis free tier <25MB, or $7 for dedicated Redis on Render)

**Performance:** <1ms path resolution, 90%+ faster than SQL queries

---

## Data Structure: Trie in Redis

### **Concept: URLs as Hierarchical Keys**

```
URL: /bcbs-239-the-book/chapter-1/what-is-bcbs-239/principles

Redis Key: route:bcbs-239-the-book:chapter-1:what-is-bcbs-239:principles

Value: {"activity_id": 4532, "trip_id": 150, "breadcrumbs": [...]}
```

**Why this works:**
- Redis keys ARE the trie structure (no complex data structure needed)
- Path lookup = single `GET` operation (O(1) time complexity)
- Natural prefix matching (can query all routes under `/bcbs-239/chapter-1/*`)
- Simple to understand (key-value pairs, no graph theory required)

---

## Implementation

### **1. Generate Trie from Trip Structure (SQLite)**

```python
# scripts/generate_route_trie.py
import redis
import json
from models import Trip, ActivityGroup, Destination, Activity

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=6379,
    decode_responses=True
)

def generate_route_trie(trip_id: int):
    """
    Materialize trip structure into Redis trie.
    Run this when trip structure changes.
    """
    trip = Trip.query.get(trip_id)
    route_count = 0

    # Clear existing routes for this trip
    pattern = f"route:{trip.base_slug}:*"
    for key in redis_client.scan_iter(match=pattern):
        redis_client.delete(key)

    print(f"Generating routes for trip: {trip.name}")

    # Generate all valid paths
    for group in trip.activity_groups:
        for destination in group.destinations:
            for activity in destination.activities:

                # Build route key
                path_segments = [
                    trip.base_slug,
                    group.slug,
                    destination.slug,
                    activity.slug
                ]
                route_key = f"route:{':'.join(path_segments)}"

                # Build route data
                route_data = {
                    'activity_id': activity.id,
                    'trip_id': trip.id,
                    'breadcrumbs': [
                        {'name': trip.name, 'slug': trip.base_slug},
                        {'name': group.name, 'slug': group.slug},
                        {'name': destination.name, 'slug': destination.slug},
                        {'name': activity.name, 'slug': activity.slug}
                    ],
                    'content_path': f'/content/{trip.base_slug}/{group.slug}/{destination.slug}/{activity.slug}.md'
                }

                # Store in Redis with 24-hour TTL
                redis_client.setex(
                    route_key,
                    86400,  # 24 hours
                    json.dumps(route_data)
                )

                route_count += 1
                print(f"  ✓ {'/'.join(path_segments)}")

    # Store metadata
    redis_client.setex(
        f"trip:{trip_id}:route_count",
        86400,
        route_count
    )

    print(f"\n✅ Generated {route_count} routes for trip {trip_id}")
    return route_count


# CLI usage
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generate_route_trie.py <trip_id>")
        sys.exit(1)

    trip_id = int(sys.argv[1])
    generate_route_trie(trip_id)
```

**Usage:**
```bash
# When trip structure changes, regenerate routes
python scripts/generate_route_trie.py 150

# Output:
# Generating routes for trip: BCBS-239: The Book
#   ✓ bcbs-239-the-book/chapter-1/what-is-bcbs-239/principles
#   ✓ bcbs-239-the-book/chapter-1/what-is-bcbs-239/history
#   ✓ bcbs-239-the-book/chapter-1/getting-started/overview
#   ...
# ✅ Generated 47 routes for trip 150
```

---

### **2. Path Resolution (Flask)**

```python
# app.py
import redis
import json
from flask import Flask, render_template, redirect, flash

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=6379,
    decode_responses=True
)


@app.route('/<path:url_path>')
def universal_handler(url_path: str):
    """
    Universal URL handler using Redis trie.
    """
    # Convert URL to route key
    path_clean = url_path.strip('/')
    route_key = f"route:{path_clean.replace('/', ':')}"

    # Try Redis trie lookup
    cached = redis_client.get(route_key)

    if cached:
        # Fast path: Redis hit
        route_data = json.loads(cached)
        activity = Activity.query.get(route_data['activity_id'])

        return render_template('activity.html',
            activity=activity,
            breadcrumbs=route_data['breadcrumbs'],
            content_path=route_data['content_path']
        )

    # Check for redirect
    redirect_key = f"redirect:{path_clean.replace('/', ':')}"
    redirect_target = redis_client.get(redirect_key)

    if redirect_target:
        # Redirect found
        new_path = redirect_target.replace(':', '/')
        flash("This content has moved", "info")
        return redirect(f"/{new_path}", code=301)

    # Slow path: Trie miss (fallback to database)
    try:
        result = resolve_from_database_fallback(url_path)
        return render_activity(result)
    except PathNotFound:
        return render_404(url_path)


def resolve_from_database_fallback(url_path: str):
    """
    Fallback: Resolve path using SQLite queries.
    Used when Redis trie not yet generated.
    """
    segments = url_path.strip('/').split('/')

    # Find trip
    trip = Trip.query.filter_by(base_slug=segments[0]).first_or_404()

    # Traverse hierarchy (complex JOINs)
    group = ActivityGroup.query.filter_by(
        trip_id=trip.id,
        slug=segments[1]
    ).first_or_404()

    destination = Destination.query.filter_by(
        activity_group_id=group.id,
        slug=segments[2]
    ).first_or_404()

    activity = Activity.query.filter_by(
        destination_id=destination.id,
        slug=segments[3]
    ).first_or_404()

    return {
        'activity': activity,
        'trip_id': trip.id
    }
```

**Performance:**
- **Redis hit:** <1ms (single GET operation)
- **Redis miss:** 20-50ms (fallback to SQLite)
- **Expected hit ratio:** >95% (routes generated daily)

---

### **3. Redirects (When Slugs Change)**

```python
# models.py or admin actions
def update_activity_slug(activity_id: int, new_slug: str):
    """
    Update activity slug and create Redis redirects.
    """
    activity = Activity.query.get(activity_id)
    old_slug = activity.slug

    if old_slug == new_slug:
        return  # No change

    # Find all paths containing this activity
    old_paths = find_all_paths_for_activity(activity_id)

    # Update SQLite
    activity.slug = new_slug
    db.session.commit()

    # Regenerate trie for this trip (creates new paths)
    generate_route_trie(activity.trip_id)

    # Create redirect keys for old paths
    for old_path in old_paths:
        new_path = old_path.replace(f"/{old_slug}", f"/{new_slug}")

        redirect_key = f"redirect:{old_path.replace('/', ':')}"
        new_path_key = new_path.replace('/', ':')

        # Store redirect with 30-day TTL
        redis_client.setex(
            redirect_key,
            2592000,  # 30 days
            new_path_key
        )

        print(f"  Redirect: {old_path} → {new_path}")

    print(f"✅ Updated slug: {old_slug} → {new_slug}")
    print(f"✅ Created {len(old_paths)} redirects")


def find_all_paths_for_activity(activity_id: int):
    """
    Find all URL paths that resolve to this activity.
    """
    activity = Activity.query.get(activity_id)
    destination = activity.destination
    group = destination.activity_group
    trip = group.trip

    # This activity may be in multiple trips/groups (if reused)
    # For simplicity, assuming single path
    path = f"{trip.base_slug}/{group.slug}/{destination.slug}/{activity.slug}"
    return [path]
```

**Usage:**
```python
# Admin interface action
update_activity_slug(
    activity_id=4532,
    new_slug="core-principles"
)

# Output:
#   Redirect: bcbs-239-the-book/chapter-1/what-is-bcbs-239/principles → bcbs-239-the-book/chapter-1/what-is-bcbs-239/core-principles
# ✅ Updated slug: principles → core-principles
# ✅ Created 1 redirect
```

---

## Deployment on Render

### **Option 1: Use Render's Free Redis (Recommended for Start)**

Render provides **Redis free tier** (25MB limit):

```yaml
# render.yaml
services:
  - type: web
    name: qrcards
    env: python
    plan: starter  # $7/month
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: REDIS_URL
        value: redis://localhost:6379  # Built-in Redis (free)
```

**Cost:** $0/month (included in web service)
**Limit:** 25MB (sufficient for ~50,000 routes)

---

### **Option 2: Dedicated Redis Service (If You Need More)**

```yaml
# render.yaml
services:
  - type: web
    name: qrcards
    env: python
    plan: starter  # $7/month
    envVars:
      - key: REDIS_URL
        fromService:
          name: qrcards-redis
          property: connectionString

  - type: redis
    name: qrcards-redis
    plan: starter  # $7/month (256MB, persistent)
    maxmemoryPolicy: allkeys-lru  # Evict oldest keys when full
```

**Cost:** $7/month additional
**Limit:** 256MB (sufficient for ~500,000 routes)

---

## Monitoring & Maintenance

### **Route Generation Automation**

```python
# scripts/cron_regenerate_routes.py
"""
Cron job: Regenerate all trip routes daily.
Ensures Redis trie stays in sync with SQLite.
"""
from models import Trip
from generate_route_trie import generate_route_trie

def regenerate_all_routes():
    """Regenerate routes for all active trips."""
    trips = Trip.query.filter_by(status='active').all()

    total_routes = 0
    for trip in trips:
        count = generate_route_trie(trip.id)
        total_routes += count

    print(f"✅ Regenerated {total_routes} routes for {len(trips)} trips")

if __name__ == '__main__':
    regenerate_all_routes()
```

**Render Cron Job:**
```yaml
# render.yaml
services:
  - type: cron
    name: regenerate-routes
    env: python
    schedule: "0 2 * * *"  # Daily at 2am
    buildCommand: pip install -r requirements.txt
    startCommand: python scripts/cron_regenerate_routes.py
```

**Cost:** $0 (cron jobs free on Render)

---

### **Cache Hit Ratio Monitoring**

```python
# app.py
import statsd

# Track cache hits/misses
metrics = statsd.StatsClient('localhost', 8125)

@app.route('/<path:url_path>')
def universal_handler(url_path: str):
    route_key = f"route:{url_path.replace('/', ':')}"
    cached = redis_client.get(route_key)

    if cached:
        metrics.incr('route.cache.hit')
        # ... render activity
    else:
        metrics.incr('route.cache.miss')
        # ... fallback to database
```

**Expected Metrics:**
- Cache hit ratio: >95%
- Average response time (hit): <5ms
- Average response time (miss): 20-50ms

---

## Migration Path (When Ready)

### **Phase 1: Add Redis to Existing System (No Breaking Changes)**

```python
# Add Redis lookup BEFORE existing logic
@app.route('/<path:url_path>')
def universal_handler(url_path: str):
    # NEW: Try Redis first
    route_key = f"route:{url_path.replace('/', ':')}"
    cached = redis_client.get(route_key)

    if cached:
        return render_from_redis(cached)

    # EXISTING: Fallback to current routing logic
    return existing_path_resolution(url_path)
```

**Benefit:** Redis trie runs in parallel with existing system (zero risk)

---

### **Phase 2: Generate Routes for One Trip (Test)**

```bash
# Generate routes for single trip
python scripts/generate_route_trie.py 150

# Monitor cache hit ratio
# If successful, continue to Phase 3
```

---

### **Phase 3: Generate Routes for All Trips**

```bash
# Regenerate all trips
python scripts/cron_regenerate_routes.py

# Set up daily cron job (Render YAML)
```

---

### **Phase 4: Remove Database Fallback (Optional)**

Once Redis trie proves stable:

```python
@app.route('/<path:url_path>')
def universal_handler(url_path: str):
    route_key = f"route:{url_path.replace('/', ':')}"
    cached = redis_client.get(route_key)

    if cached:
        return render_from_redis(cached)

    # No fallback - 404 if not in trie
    return render_404(url_path)
```

**Benefit:** Removes complex SQL queries entirely

---

## Performance Benchmarks

### **Theoretical Performance:**

| Operation | Time |
|-----------|------|
| Redis GET | <1ms |
| JSON parse | <0.1ms |
| SQLite query (activity) | 2-5ms |
| **Total (cache hit)** | **<6ms** |

### **Compared to Alternatives:**

| Approach | Response Time | Memory |
|----------|---------------|--------|
| **Redis Trie** | **<6ms** | **5MB** (10k routes) |
| SQLite JOINs | 20-50ms | 0MB (database queries) |
| Path records | 5-10ms | 500KB (table rows) |
| Neo4j | 2-5ms | 512MB+ (graph database) |

---

## Cost Analysis

### **Development Cost (One-Time):**
- Write trie generation script: 2-4 hours
- Integrate Redis into Flask: 1-2 hours
- Test and debug: 2-4 hours
- **Total: 5-10 hours**

### **Operating Cost (Monthly):**
- **Render Free Redis:** $0/month (25MB limit)
- **Render Paid Redis:** $7/month (256MB, persistent)
- Cron job (daily regeneration): $0/month (included)

**Compared to:**
- Neo4j: $24-31/month (service + disk)
- Explicit path records: $0/month (SQLite)

---

## Limitations & Trade-offs

### **Limitations:**

1. **Memory Constraint:** Redis trie size grows with number of routes
   - 10,000 routes ≈ 5MB
   - 100,000 routes ≈ 50MB
   - Free tier limit: 25MB (~50,000 routes)

2. **TTL Management:** Routes expire after 24 hours
   - Must regenerate daily via cron job
   - Cold start = cache miss until regenerated

3. **Eventual Consistency:** Trie may be stale if trip structure changes
   - Mitigation: Regenerate trie immediately on structure changes
   - Or accept 24-hour staleness

### **Trade-offs:**

**Pros:**
- ✅ 10x faster than SQL queries
- ✅ Simple to understand (key-value pairs)
- ✅ Low operational complexity
- ✅ Portable (Redis everywhere)

**Cons:**
- ⚠️ Requires Redis infrastructure
- ⚠️ Eventual consistency (trie may lag database)
- ⚠️ Memory usage (5MB per 10k routes)

---

## When NOT to Use Redis Trie

**Don't use this if:**

1. **You have <10 trips with <20 activities each**
   - SQLite queries fast enough (<10ms)
   - Not worth the complexity

2. **Trip structures change hourly**
   - Constant regeneration overhead
   - Eventual consistency problem

3. **You need complex graph queries**
   - Use Neo4j instead (better for relationships)

4. **You don't have Redis infrastructure**
   - Don't add Redis just for routing
   - Use explicit path records instead

---

## Conclusion

**Redis Trie Routing is:**
- **Simple:** Key-value lookups, no complex data structures
- **Fast:** <1ms path resolution (10x faster than SQL)
- **Cheap:** $0-7/month on Render
- **Portable:** Works anywhere Redis runs

**Best for:**
- High-traffic applications (>1000 requests/day)
- Large trip structures (50+ activities)
- Static or slowly-changing content

**Not for:**
- Hobby projects with <10 trips (overkill)
- Frequently changing structures (regeneration overhead)
- Complex relationship queries (use Neo4j)

---

**Status:** Reference implementation, ready when needed

**Priority:** Ship pages first, optimize routing later

**Next Steps (When Ready):**
1. Deploy to Render with Redis support
2. Implement `generate_route_trie.py` script
3. Add Redis lookup to Flask routing
4. Monitor cache hit ratios
5. Automate daily regeneration

This document will be here when routing becomes a bottleneck. For now: ship features, deliver value.
