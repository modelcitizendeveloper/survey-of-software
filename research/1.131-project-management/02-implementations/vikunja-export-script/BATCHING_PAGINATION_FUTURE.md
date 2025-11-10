# Batching/Pagination - Future Consideration

**Date**: November 8, 2025
**Status**: Not needed at current scale (105 tasks, 181KB export)
**Review trigger**: When portfolio exceeds 500 tasks

---

## Current Performance Baseline

**Portfolio size (Nov 2025)**:
- 41 projects
- 105 tasks
- 17 tasks with source documents

**Export performance**:
- Full portfolio: ~5 minutes
- Single project: ~2 seconds
- Output size: 181KB JSON
- Memory usage: Normal
- API rate limits: No issues

**Conclusion**: No batching needed at current scale

---

## When Batching/Pagination Would Be Needed

### Trigger Conditions

**Consider implementing when**:
- Portfolio exceeds **500 tasks** (5x current)
- Export time exceeds **15 minutes**
- File size exceeds **5MB**
- API rate limit errors occur
- Memory constraints hit (low-memory environments)

**Definitely implement when**:
- Portfolio exceeds **1000 tasks** (10x current)
- Export fails due to timeout
- API rejects requests (rate limiting)
- Memory errors during export

---

## Implementation Approach

### Option A: Page-Based Batching

**Strategy**: Process projects in batches

```python
def export_portfolio_batched(client, batch_size=10):
    """Export portfolio in batches of projects"""
    all_projects = client.projects.list()
    results = []

    for i in range(0, len(all_projects), batch_size):
        batch = all_projects[i:i+batch_size]

        # Export batch
        for project in batch:
            project_data = export_project(client, project)
            results.append(project_data)

        # Optional: Write intermediate results
        write_checkpoint(results, f"batch_{i}.json")

        # Optional: Rate limit delay
        time.sleep(1)

    return results
```

**Pros**:
- Simple to implement
- Can resume from checkpoints
- Spreads load over time

**Cons**:
- Still loads all tasks per project
- Doesn't help with very large single projects

---

### Option B: Cursor-Based Pagination

**Strategy**: Use API pagination if available

```python
def export_tasks_paginated(client, project_id, page_size=50):
    """Export tasks using cursor pagination"""
    tasks = []
    page = 1

    while True:
        # Assuming Vikunja API supports pagination
        response = client._request(
            "GET",
            f"/api/v1/projects/{project_id}/tasks",
            params={"page": page, "per_page": page_size}
        )

        if not response or len(response) == 0:
            break

        tasks.extend(response)
        page += 1

        # Rate limit protection
        if page % 10 == 0:
            time.sleep(1)

    return tasks
```

**Pros**:
- Official API pattern (if supported)
- Efficient memory usage
- Handles unlimited task counts

**Cons**:
- Requires API pagination support (check Vikunja docs)
- More complex error handling

---

### Option C: Streaming JSON Output

**Strategy**: Write results as they're fetched (avoid loading all in memory)

```python
def export_portfolio_streaming(client, output_file):
    """Stream export directly to file"""
    with open(output_file, 'w') as f:
        f.write('{"projects": [')

        projects = client.projects.list()
        for i, project in enumerate(projects):
            if i > 0:
                f.write(',')

            # Export project
            project_data = export_project(client, project)
            json.dump(project_data, f)

            # Memory freed immediately

        f.write('], "exported_at": "..."}')
```

**Pros**:
- Minimal memory footprint
- Works for any portfolio size
- Can monitor progress during export

**Cons**:
- Can't easily resume from failure
- Harder to validate mid-export

---

### Option D: Parallel Batching (Advanced)

**Strategy**: Export multiple projects concurrently

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def export_portfolio_parallel(client, max_workers=5):
    """Export projects in parallel batches"""
    projects = client.projects.list()
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(export_project, client, p): p
            for p in projects
        }

        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Failed to export {futures[future]}: {e}")

    return results
```

**Pros**:
- Fastest export time
- Utilizes concurrent API requests

**Cons**:
- Risk of hitting rate limits
- More complex error handling
- Requires thread-safe operations

---

## Recommended Implementation (When Needed)

**Phase 1: Simple batching (500-1000 tasks)**
- Implement Option A (page-based batching)
- Batch size: 10-20 projects at a time
- Add progress indicators
- Write checkpoints every 5 batches

**Phase 2: Streaming output (1000+ tasks)**
- Add Option C (streaming JSON)
- Reduces memory footprint
- Essential for very large portfolios

**Phase 3: Optimization (if still slow)**
- Consider Option D (parallel processing)
- Test carefully for rate limits
- Add retry logic and backoff

---

## Current Code to Modify

**File**: `src/export_vikunja.py`

**Function to update**: `export_portfolio()`

**Current structure** (simplified):
```python
def export_portfolio(client, project_ids=None):
    # Get all projects
    projects = client.projects.list()

    # Filter if requested
    if project_ids:
        projects = [p for p in projects if p.id in project_ids]

    # Export all at once
    results = []
    for project in projects:
        project_data = export_project_with_tasks(client, project)
        results.append(project_data)

    return results
```

**Batched version** (add when needed):
```python
def export_portfolio(client, project_ids=None, batch_size=None):
    # Get all projects
    projects = client.projects.list()

    # Filter if requested
    if project_ids:
        projects = [p for p in projects if p.id in project_ids]

    # Export with optional batching
    results = []

    if batch_size:
        # Batched export
        for i in range(0, len(projects), batch_size):
            batch = projects[i:i+batch_size]
            for project in batch:
                project_data = export_project_with_tasks(client, project)
                results.append(project_data)

            # Checkpoint
            if (i + batch_size) < len(projects):
                write_checkpoint(results, f"checkpoint_{i}.json")

            time.sleep(1)  # Rate limit protection
    else:
        # Original behavior (current)
        for project in projects:
            project_data = export_project_with_tasks(client, project)
            results.append(project_data)

    return results
```

---

## Testing Plan (When Implementing)

**Unit tests**:
- Test batching with various sizes (1, 10, 100 projects)
- Test checkpoint writing and resuming
- Test rate limit delays

**Integration tests**:
- Export real portfolio with batching enabled
- Compare output to non-batched version (should be identical)
- Measure performance improvement

**Performance benchmarks**:
- Time comparison: batched vs non-batched
- Memory usage comparison
- API request count

---

## Monitoring

**Add metrics to track** (before implementing):
1. **Portfolio growth rate**: Tasks added per month
2. **Export duration trend**: Track over time
3. **File size trend**: Monitor JSON growth
4. **API errors**: Count rate limit hits

**Dashboard query** (example):
```sql
-- Track portfolio growth
SELECT
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as tasks_created
FROM tasks
GROUP BY month
ORDER BY month DESC;
```

**Set alerts**:
- Export time > 10 minutes → Review batching
- Portfolio size > 400 tasks → Plan for batching
- Rate limit errors > 0 → Implement delays

---

## Decision Matrix

| Portfolio Size | Export Time | File Size | Action |
|----------------|-------------|-----------|--------|
| < 200 tasks | < 10 min | < 1MB | ✅ Current approach fine |
| 200-500 tasks | 10-15 min | 1-3MB | ⚠️ Monitor, consider batching |
| 500-1000 tasks | 15-30 min | 3-10MB | 🔶 Implement simple batching |
| 1000-5000 tasks | 30+ min | 10-50MB | 🔴 Implement streaming + batching |
| > 5000 tasks | Hours | > 50MB | 🚨 Implement parallel + streaming |

**Current status (Nov 2025)**: 105 tasks → ✅ No action needed

---

## References

**Vikunja API docs**: https://vikunja.io/docs/api/
- Check for pagination support in tasks endpoint
- Review rate limiting policies
- Understand API timeouts

**Related files**:
- `src/export_vikunja.py` - Main export script
- `src/test_export_vikunja.py` - Test suite to extend
- `EXPORT_COMPLETE.md` - Current implementation summary

**External resources**:
- Streaming JSON in Python: https://docs.python.org/3/library/json.html
- ThreadPoolExecutor: https://docs.python.org/3/library/concurrent.futures.html

---

## Revision History

| Date | Portfolio Size | Action |
|------|----------------|--------|
| 2025-11-08 | 105 tasks | Documented batching approach, not implemented |
| Future | 500+ tasks | Implement simple batching (Option A) |
| Future | 1000+ tasks | Add streaming output (Option C) |

---

**Status**: DOCUMENTED - Implementation deferred until portfolio scale requires it
**Next review**: When portfolio exceeds 400 tasks or export time exceeds 10 minutes
**Owner**: Future maintainer who encounters performance issues
