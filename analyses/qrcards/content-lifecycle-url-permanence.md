# QRCards Content Lifecycle & URL Permanence Strategy

**Date:** 2025-10-09
**Application:** QRCards Intelligence Platform
**Subject:** URL Permanence, Redirects, and Content Lifecycle Management
**Context:** Dynamic path generation creates infinite URLs - need permanence strategy

---

## Executive Summary

The QRCards dynamic path generation system enables **infinite navigable URLs** from trip structures. This power creates **URL permanence responsibility**: users bookmark paths, QR codes are printed on physical materials, and content gets cited in external systems.

**Core Principle:** **URLs are a promise to users.** Breaking links erodes trust.

**Strategic Solution:** **Hybrid permalink + redirect + tombstone architecture** ensuring:
- QR codes never break (permalink system)
- Bookmarked URLs redirect gracefully (path history)
- Deleted content shows helpful information (tombstone pages)
- Zero 404 errors for legitimate historical paths

---

## Problem Statement

### **Scenario: Content Lifecycle Events Break URLs**

**Slug Changes:**
```
Old: /bcbs-239-the-book/chapter-1/what-is-bcbs-239/principles
New: /bcbs-239-the-book/ch-1/bcbs-239-overview/core-principles
Impact: Bookmarks break, QR codes fail, citations invalid
```

**Content Restructuring:**
```
Old: /bcbs-239-the-book/chapter-1/intro/overview
New: /bcbs-239-the-book/chapter-2/basics/introduction
Impact: Content moved, old path returns 404
```

**Content Deletion:**
```
Old: /bcbs-239-the-book/chapter-3/deprecated-topic/old-approach
New: [Deleted - no longer relevant]
Impact: QR codes, bookmarks, citations all break
```

**Content Merging:**
```
Old: /bcbs-239/chapter-1/overview
Old: /bcbs-239/chapter-1/background
New: /bcbs-239/chapter-1/introduction (merged content)
Impact: 50% of links break
```

---

## Solution Architecture: Three-Layer Permanence System

### **Layer 1: Permalink System (QR Codes & Bookmarks)**

**Purpose:** Permanent short URLs that never break

```
Permalink:  https://qrcards.app/p/xJ3k9
            ↓
Resolves:   Activity ID 4532 (stable database ID)
            ↓
Redirects:  Current canonical path based on trip structure
```

**Database Schema:**
```sql
CREATE TABLE permalinks (
    id INTEGER PRIMARY KEY,
    short_code TEXT UNIQUE NOT NULL,           -- 'xJ3k9'
    activity_id INTEGER REFERENCES activities(id),
    source TEXT,                                -- 'qr_code', 'bookmark', 'manual'
    created_at TIMESTAMP,
    last_accessed_at TIMESTAMP,
    access_count INTEGER DEFAULT 0
);

CREATE INDEX idx_permalinks_short_code ON permalinks(short_code);
CREATE INDEX idx_permalinks_activity ON permalinks(activity_id);
```

**Implementation:**
```python
@app.route('/p/<short_code>')
def permalink_handler(short_code: str):
    """Permanent URL resolver - never breaks."""
    permalink = Permalink.query.filter_by(short_code=short_code).first_or_404()

    # Track analytics
    permalink.access_count += 1
    permalink.last_accessed_at = datetime.utcnow()
    db.session.commit()

    # Get activity (handles all statuses: active, archived, deleted)
    activity = Activity.query.get(permalink.activity_id)
    return handle_activity_by_status(activity)
```

**Use Cases:**
- **QR codes on printed materials** (business cards, posters, books)
- **Shareable short links** for social media
- **Email campaigns** with trackable links
- **API integrations** requiring stable identifiers

---

### **Layer 2: Path History System (Automatic Redirects)**

**Purpose:** Track every URL that ever existed, redirect to current location

```
Old Path:    /bcbs-239/chapter-1/old-name/principles
             ↓
Check:       path_history table
             ↓
Found:       Redirect to /bcbs-239/chapter-1/new-name/core-principles (301)
```

**Database Schema:**
```sql
CREATE TABLE path_history (
    id INTEGER PRIMARY KEY,
    old_path TEXT UNIQUE NOT NULL,              -- Historical URL
    current_path TEXT,                          -- NULL if deleted
    activity_id INTEGER REFERENCES activities(id),
    trip_id INTEGER,
    redirect_type TEXT,                         -- 'permanent', 'temporary', 'gone'
    reason TEXT,                                -- 'slug_changed', 'activity_moved', 'merged'
    created_at TIMESTAMP,
    deprecated_at TIMESTAMP,
    redirect_count INTEGER DEFAULT 0,
    last_redirected_at TIMESTAMP
);

CREATE INDEX idx_path_history_old_path ON path_history(old_path);
CREATE INDEX idx_path_history_activity ON path_history(activity_id);
```

**Automatic Population on Slug Changes:**
```python
def update_activity_slug(activity_id: int, new_slug: str, reason: str = "slug_updated"):
    """Safe slug update with automatic redirect creation."""
    activity = Activity.query.get(activity_id)
    old_slug = activity.url_slug

    if old_slug == new_slug:
        return  # No change needed

    # 1. Generate all old paths that will break
    old_paths = generate_all_paths_for_activity(activity)

    # 2. Update slug
    activity.url_slug = new_slug
    db.session.commit()

    # 3. Generate new canonical paths
    new_paths = generate_all_paths_for_activity(activity)

    # 4. Create redirect entries for every old path
    for old_path in old_paths:
        new_path = old_path.replace(f"/{old_slug}/", f"/{new_slug}/")

        PathHistory.create_or_update(
            old_path=old_path,
            current_path=new_path,
            activity_id=activity_id,
            trip_id=activity.trip_id,
            redirect_type='permanent',
            reason=reason
        )

    # 5. Invalidate caches
    invalidate_trip_caches(activity.trip_id, old_paths=old_paths)

    logger.info(f"Slug updated: {old_slug} → {new_slug}, created {len(old_paths)} redirects")
```

**Path Resolution with Redirect Fallback:**
```python
def resolve_path_or_redirect(url_path: str):
    """Try current path, fall back to history redirects."""

    # 1. Try resolving as current path
    try:
        result = resolve_current_path(url_path)
        return render_activity(result['activity'])

    except PathNotFound:
        # 2. Check path history for redirects
        history = get_redirect_for_path(url_path)  # Cached lookup

        if history and history.current_path:
            # Track redirect usage
            log_redirect_access(history)

            # 301 Permanent Redirect
            flash(f"This content has moved (reason: {history.reason})", "info")
            return redirect(history.current_path, code=301)

        elif history and history.redirect_type == 'gone':
            # 410 Gone (deleted content)
            activity = Activity.query.get(history.activity_id)
            return render_tombstone(activity)

        else:
            # True 404 - path never existed
            return render_404_with_search(url_path)
```

**Performance Optimization:**
```python
# Cache redirect lookups (redirects don't change often)
@cached(cache=TTLCache(maxsize=10000, ttl=3600))
def get_redirect_for_path(old_path: str):
    """Cached path history lookup."""
    return PathHistory.query.filter_by(old_path=old_path).first()
```

---

### **Layer 3: Tombstone System (Graceful Content Deletion)**

**Purpose:** Deleted content shows helpful information instead of 404 errors

```
Status:      'deleted'
             ↓
Renders:     Tombstone page explaining deletion
             ↓
Suggests:    Alternative content, trip homepage
```

**Database Schema Extension:**
```sql
ALTER TABLE activities ADD COLUMN status TEXT DEFAULT 'active';
-- Values: 'active', 'archived', 'deleted', 'merged'

ALTER TABLE activities ADD COLUMN tombstone_message TEXT;
ALTER TABLE activities ADD COLUMN redirect_to_activity_id INTEGER;
ALTER TABLE activities ADD COLUMN deleted_at TIMESTAMP;
```

**Soft Delete Implementation:**
```python
def delete_activity_gracefully(activity_id: int, reason: str, suggest_alternative_id: int = None):
    """Soft delete with tombstone - never hard delete."""
    activity = Activity.query.get(activity_id)

    # Mark as deleted (keep in database)
    activity.status = 'deleted'
    activity.tombstone_message = reason
    activity.deleted_at = datetime.utcnow()

    if suggest_alternative_id:
        activity.redirect_to_activity_id = suggest_alternative_id

    db.session.commit()

    # Record all paths as "gone" in history
    old_paths = generate_all_paths_for_activity(activity)
    for path in old_paths:
        PathHistory.create_or_update(
            old_path=path,
            current_path=None,
            activity_id=activity_id,
            trip_id=activity.trip_id,
            redirect_type='gone',
            reason=f"Content deleted: {reason}"
        )

    # Invalidate caches
    invalidate_trip_caches(activity.trip_id, old_paths=old_paths)

    logger.warning(f"Soft deleted activity {activity_id}: {reason}")
```

**Status-Based Rendering:**
```python
def handle_activity_by_status(activity: Activity):
    """Render activity based on lifecycle status."""

    if activity.status == 'active':
        # Normal rendering
        return render_template('activity.html', activity=activity)

    elif activity.status == 'archived':
        # Still show content with warning banner
        return render_template('activity.html',
            activity=activity,
            warning_message="This content is archived and may be outdated",
            show_archive_badge=True
        )

    elif activity.status == 'merged':
        # Redirect to merged location
        new_activity = Activity.query.get(activity.redirect_to_activity_id)
        new_path = generate_canonical_path(new_activity)

        flash(f"This content has been merged with: {new_activity.name}", "info")
        return redirect(new_path, code=301)

    elif activity.status == 'deleted':
        # Tombstone page (HTTP 410 Gone)
        return render_template('tombstone.html',
            title=activity.name,
            deletion_reason=activity.tombstone_message,
            deleted_date=activity.deleted_at,
            trip=get_trip(activity.trip_id),
            suggested_alternatives=find_similar_activities(activity),
            trip_homepage_link=generate_trip_base_path(activity.trip_id)
        ), 410  # HTTP 410 Gone (better than 404)
```

**Tombstone Template (`tombstone.html`):**
```html
<div class="tombstone-page">
    <h1>Content No Longer Available</h1>

    <div class="tombstone-info">
        <h2>{{ title }}</h2>
        <p class="deletion-date">Removed on {{ deleted_date }}</p>
        <p class="reason">{{ deletion_reason }}</p>
    </div>

    <div class="alternatives">
        <h3>You might be interested in:</h3>
        <ul>
            {% for alt in suggested_alternatives %}
                <li><a href="{{ alt.url }}">{{ alt.name }}</a></li>
            {% endfor %}
        </ul>

        <p><a href="{{ trip_homepage_link }}">Return to {{ trip.name }} homepage</a></p>
    </div>
</div>
```

---

## Content Lifecycle Workflows

### **Workflow 1: Update Slugs Safely**

**Scenario:** Rename activity from "what-is-bcbs-239" → "bcbs-239-overview"

```python
# Admin interface action
update_activity_slug(
    activity_id=4532,
    new_slug="bcbs-239-overview",
    reason="Improved clarity and SEO"
)

# Automatic actions:
# 1. Find all old paths containing "what-is-bcbs-239"
# 2. Update activity.url_slug to "bcbs-239-overview"
# 3. Create PathHistory redirects (old → new)
# 4. Invalidate L1 and L2 caches
# 5. Log change for audit trail

# Result: Old URLs automatically redirect, zero broken links
```

---

### **Workflow 2: Merge Content**

**Scenario:** Consolidate "overview" + "background" → "introduction"

```python
def merge_activities(source_ids: list, target_id: int, reason: str):
    """Merge multiple activities into one."""
    target = Activity.query.get(target_id)
    target_path = generate_canonical_path(target)

    for source_id in source_ids:
        source = Activity.query.get(source_id)
        source_paths = generate_all_paths_for_activity(source)

        # Mark as merged
        source.status = 'merged'
        source.redirect_to_activity_id = target_id
        source.tombstone_message = reason

        # Create redirects
        for old_path in source_paths:
            PathHistory.create_or_update(
                old_path=old_path,
                current_path=target_path,
                activity_id=source_id,
                trip_id=source.trip_id,
                redirect_type='permanent',
                reason=f"Merged into: {target.name}"
            )

    db.session.commit()
    invalidate_trip_caches(target.trip_id)

# Usage
merge_activities(
    source_ids=[4530, 4531],  # overview, background
    target_id=4532,           # introduction
    reason="Consolidated introductory content for clarity"
)
```

---

### **Workflow 3: Archive Outdated Content**

**Scenario:** Mark content as archived (still accessible but outdated)

```python
def archive_activity(activity_id: int, reason: str):
    """Mark activity as archived - still accessible with warning."""
    activity = Activity.query.get(activity_id)

    activity.status = 'archived'
    activity.tombstone_message = reason
    db.session.commit()

    # No redirects needed - content still at same URL
    # Just shows with "archived" warning banner

    logger.info(f"Archived activity {activity_id}: {reason}")

# Usage
archive_activity(
    activity_id=4533,
    reason="This content was written in 2023 and may not reflect current best practices"
)
```

---

### **Workflow 4: Delete Content Gracefully**

**Scenario:** Remove content that's no longer relevant

```python
# Admin interface action
delete_activity_gracefully(
    activity_id=4534,
    reason="Content superseded by updated regulatory framework",
    suggest_alternative_id=4535  # Point to replacement content
)

# Automatic actions:
# 1. Mark activity.status = 'deleted'
# 2. Set tombstone_message and deleted_at
# 3. Create PathHistory entries (redirect_type='gone')
# 4. Invalidate caches
# 5. Keep activity in database (soft delete)

# Result:
# - Old URLs show tombstone page (HTTP 410 Gone)
# - Suggest alternative content
# - QR codes still resolve (show tombstone)
# - Can be "undeleted" if needed (just change status)
```

---

## QR Code Best Practices

### **Rule: Always Use Permalinks for QR Codes**

```python
def generate_qr_code_for_activity(activity_id: int):
    """Generate QR code with permanent URL."""

    # Create or get existing permalink
    permalink = Permalink.query.filter_by(
        activity_id=activity_id,
        source='qr_code'
    ).first()

    if not permalink:
        short_code = generate_short_code(activity_id)
        permalink = Permalink.create(
            short_code=short_code,
            activity_id=activity_id,
            source='qr_code'
        )

    # QR code always points to permalink (never changes)
    permanent_url = f"https://qrcards.app/p/{permalink.short_code}"

    return {
        'qr_image': generate_qr_image(permanent_url),
        'permalink_url': permanent_url,
        'short_code': permalink.short_code
    }
```

**Why Permalinks for QR Codes:**
- QR codes on **printed materials** can't be updated
- Content structure may change (slugs renamed, activities moved)
- Permalink always resolves to activity (even if deleted → tombstone)
- Track QR code usage via access_count

---

## Monitoring & Analytics

### **Redirect Usage Dashboard**

```python
def get_redirect_stats(days: int = 30):
    """Monitor which old URLs are still being accessed."""
    cutoff = datetime.utcnow() - timedelta(days=days)

    return PathHistory.query.filter(
        PathHistory.last_redirected_at >= cutoff
    ).order_by(
        PathHistory.redirect_count.desc()
    ).limit(100).all()
```

**Admin Dashboard:**
```
Recent Redirects (Last 30 Days)
--------------------------------
/bcbs-239/old-chapter-1/principles → /bcbs-239/chapter-1/core-principles
  └─ 47 redirects (likely QR code or bookmarked link)

/intelligence/reports/project-alpha → [DELETED - Tombstone]
  └─ 12 visits (consider adding redirect to similar content)

/bcbs-239/chapter-2/deprecated → /bcbs-239/chapter-3/updated-approach
  └─ 3 redirects (low traffic, redirect working as expected)
```

### **Permalink Analytics**

```python
def get_permalink_stats():
    """Track QR code and short link usage."""
    return Permalink.query.order_by(
        Permalink.access_count.desc()
    ).limit(100).all()
```

**QR Code Performance Report:**
```
Top QR Codes (All Time)
-----------------------
/p/xJ3k9 → BCBS-239 Chapter 1 Principles
  └─ 1,247 scans, last accessed 2 hours ago

/p/mP2n4 → Intelligence Reports Overview
  └─ 823 scans, last accessed 1 day ago

/p/qR5t7 → [DELETED CONTENT - Tombstone]
  └─ 156 scans, last accessed 3 days ago
  └─ ACTION: Consider redirecting to alternative content
```

---

## Cache Integration

### **Cache Invalidation on Lifecycle Changes**

```python
def invalidate_trip_caches(trip_id: int, old_paths: list = None):
    """Comprehensive cache invalidation for content changes."""

    # L1 Cache (cachetools): Trip structure
    if trip_id in trip_structure_cache:
        del trip_structure_cache[trip_id]

    # L2 Cache (Redis): Trip structure + all path resolutions
    redis_client.delete(f"trip:{trip_id}:structure")

    # Pattern delete: All cached path resolutions for this trip
    pattern = f"trip:{trip_id}:path:*"
    for key in redis_client.scan_iter(match=pattern):
        redis_client.delete(key)

    # Cache redirect hints for old paths (avoid DB lookup)
    if old_paths:
        for old_path in old_paths:
            path_hash = hashlib.md5(old_path.encode()).hexdigest()[:16]
            redis_client.setex(
                f"redirect:{path_hash}",
                86400,  # 24 hour TTL
                json.dumps({'check_history': True})
            )

    logger.info(f"Invalidated caches for trip {trip_id}, {len(old_paths or [])} old paths marked")
```

### **Caching Redirect Lookups**

```python
# Path history lookups are cached (redirects don't change often)
@cached(cache=TTLCache(maxsize=10000, ttl=3600))
def get_redirect_for_path(old_path: str):
    """Cached path history lookup - 1 hour TTL."""
    return PathHistory.query.filter_by(old_path=old_path).first()
```

**Performance Impact:**
- First redirect check: ~5-10ms (database query)
- Cached redirect check: <0.1ms (cachetools)
- Cache hit ratio: ~99% (historical paths don't change)

---

## Database Migration Plan

### **Migration 1: Add Permalinks Table**

```python
# migrations/001_add_permalinks.py
def upgrade():
    op.create_table(
        'permalinks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('short_code', sa.String(20), unique=True, nullable=False),
        sa.Column('activity_id', sa.Integer(), sa.ForeignKey('activities.id')),
        sa.Column('source', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('last_accessed_at', sa.DateTime()),
        sa.Column('access_count', sa.Integer(), default=0)
    )
    op.create_index('idx_permalinks_short_code', 'permalinks', ['short_code'])
    op.create_index('idx_permalinks_activity', 'permalinks', ['activity_id'])
```

### **Migration 2: Add Path History Table**

```python
# migrations/002_add_path_history.py
def upgrade():
    op.create_table(
        'path_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('old_path', sa.Text(), unique=True, nullable=False),
        sa.Column('current_path', sa.Text()),
        sa.Column('activity_id', sa.Integer(), sa.ForeignKey('activities.id')),
        sa.Column('trip_id', sa.Integer(), sa.ForeignKey('trips.id')),
        sa.Column('redirect_type', sa.String(50)),
        sa.Column('reason', sa.Text()),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('deprecated_at', sa.DateTime()),
        sa.Column('redirect_count', sa.Integer(), default=0),
        sa.Column('last_redirected_at', sa.DateTime())
    )
    op.create_index('idx_path_history_old_path', 'path_history', ['old_path'])
    op.create_index('idx_path_history_activity', 'path_history', ['activity_id'])
```

### **Migration 3: Add Activity Lifecycle Fields**

```python
# migrations/003_add_activity_lifecycle.py
def upgrade():
    op.add_column('activities', sa.Column('status', sa.String(20), default='active'))
    op.add_column('activities', sa.Column('tombstone_message', sa.Text()))
    op.add_column('activities', sa.Column('redirect_to_activity_id', sa.Integer()))
    op.add_column('activities', sa.Column('deleted_at', sa.DateTime()))

    # Update existing activities to 'active'
    op.execute("UPDATE activities SET status = 'active' WHERE status IS NULL")
```

---

## Success Metrics

### **URL Permanence KPIs**

| Metric | Target | Measurement |
|--------|--------|-------------|
| **True 404 rate** | <1% | Only paths that never existed |
| **Redirect success rate** | >99% | Historical paths resolve correctly |
| **QR code reliability** | 100% | Permalinks never return 404 |
| **Tombstone clarity** | >90% user satisfaction | Survey deleted content pages |
| **Redirect cache hit ratio** | >98% | Cached redirect lookups |

### **Content Lifecycle Metrics**

| Metric | Current | Target |
|--------|---------|--------|
| **Hard deletes per month** | Unknown | 0 (always soft delete) |
| **Redirects created per slug change** | 0 (no system) | Automatic |
| **Broken link reports** | Unknown | <5 per month |
| **QR code printed materials** | Unknown | Track all permalinks |

---

## Implementation Roadmap

### **Phase 1: Permalink System (Week 1)**
- Create `permalinks` table
- Implement `/p/<short_code>` route handler
- Generate permalinks for all existing activities
- Update QR code generation to use permalinks

**Success Criteria:**
- All QR codes use permalink URLs
- Permalink resolution working
- Analytics tracking implemented

### **Phase 2: Path History System (Week 2)**
- Create `path_history` table
- Implement redirect fallback in path resolution
- Add automatic redirect creation to slug update workflows
- Cache redirect lookups

**Success Criteria:**
- Slug changes automatically create redirects
- 301 redirects working for historical paths
- Redirect dashboard showing usage

### **Phase 3: Tombstone System (Week 3)**
- Add lifecycle fields to `activities` table
- Implement status-based rendering
- Create tombstone template
- Update admin delete workflow to soft delete

**Success Criteria:**
- Deleted content shows tombstone page
- Merged content redirects correctly
- Archived content shows warning banner
- Zero hard deletes in production

### **Phase 4: Monitoring & Optimization (Week 4+)**
- Build redirect analytics dashboard
- Implement permalink usage tracking
- Optimize redirect cache strategy
- Document content lifecycle policies

**Success Criteria:**
- Admin can monitor redirect usage
- QR code analytics available
- Redirect cache hit ratio >98%
- Content lifecycle policy documented

---

## Best Practices for Content Editors

### **Do's:**
- ✅ Update slugs confidently (redirects created automatically)
- ✅ Use permalinks for all QR codes (never canonical paths)
- ✅ Soft delete content (provides context to users)
- ✅ Suggest alternatives when deleting content
- ✅ Archive outdated content instead of deleting when possible

### **Don'ts:**
- ❌ Never hard delete activities (always soft delete)
- ❌ Don't use canonical URLs in QR codes (use permalinks)
- ❌ Don't change slugs without testing redirects
- ❌ Don't delete content without adding tombstone message
- ❌ Don't ignore redirect analytics (shows user pain points)

---

## Conclusion

The **permalink + redirect + tombstone architecture** ensures QRCards maintains **URL permanence** as a core platform value. This approach:

- **Respects users** by honoring bookmarks and citations
- **Protects QR codes** printed on physical materials
- **Enables confident content management** without fear of breaking links
- **Provides transparency** when content changes or is removed
- **Maintains SEO value** through proper 301 redirects

**Strategic Value:** URL permanence is a **competitive advantage** - users trust platforms that don't break links. This system enables aggressive content iteration while maintaining that trust.

---

**References:**
- `caching-strategy-dynamic-paths.md` - Cache integration patterns
- `specialist-agent-prompts.md` - Database and Flask implementation guidance
- experiments/1.047-caching-libraries - Validated caching solutions

**Next Steps:**
1. Review implementation roadmap with team
2. Begin Phase 1 (permalink system)
3. Update specialist agent prompts to include lifecycle workflows
4. Create admin interface mockups for content lifecycle management
