# BucketsManager Update for View-Based Endpoints

## Summary

Update BucketsManager methods to use view-based endpoints discovered through TDD research:
- Old: `/api/v1/projects/{project_id}/buckets` (returns 404)
- New: `/api/v1/projects/{project_id}/views/{view_id}/buckets` (works!)

## Changes Required

### 1. Update `create()` method signature and endpoint

**OLD:**
```python
def create(self, project_id: int, title: str, position: int = 0, limit: int = 0) -> Bucket:
    # ...
    response = self.client._request("PUT", f"/api/v1/projects/{project_id}/buckets", json=data)
```

**NEW:**
```python
def create(self, project_id: int, view_id: int, title: str, position: int = 0, limit: int = 0) -> Bucket:
    """
    Create a new bucket in a view (typically Kanban view).

    Args:
        project_id: ID of the project
        view_id: ID of the view (get from ViewsManager.get_kanban_view())
        title: Bucket title
        position: Sort position (default 0)
        limit: WIP limit, 0 = no limit (default 0)
    """
    # ...
    response = self.client._request("PUT", f"/api/v1/projects/{project_id}/views/{view_id}/buckets", json=data)
```

### 2. Update `list()` method

**OLD:**
```python
def list(self, project_id: int) -> List[Bucket]:
    # ...
    response = self.client._request("GET", f"/api/v1/projects/{project_id}/buckets")
```

**NEW:**
```python
def list(self, project_id: int, view_id: int) -> List[Bucket]:
    """
    List all buckets in a view.

    Args:
        project_id: ID of the project
        view_id: ID of the view (get from ViewsManager.get_kanban_view())
    """
    # ...
    response = self.client._request("GET", f"/api/v1/projects/{project_id}/views/{view_id}/buckets")
```

### 3. Update `update()` method

**OLD:**
```python
def update(self, project_id: int, bucket_id: int, title: str = None, position: int = None, limit: int = None) -> Bucket:
    # ...
    response = self.client._request("POST", f"/api/v1/projects/{project_id}/buckets/{bucket_id}", json=data)
```

**NEW:**
```python
def update(self, project_id: int, view_id: int, bucket_id: int, title: str = None, position: int = None, limit: int = None) -> Bucket:
    """
    Update a bucket.

    Args:
        project_id: ID of the project
        view_id: ID of the view
        bucket_id: ID of the bucket
        title: New title (optional)
        position: New position (optional)
        limit: New WIP limit (optional)
    """
    # ...
    response = self.client._request("POST", f"/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}", json=data)
```

### 4. Update `delete()` method

**OLD:**
```python
def delete(self, project_id: int, bucket_id: int) -> None:
    # ...
    self.client._request("DELETE", f"/api/v1/projects/{project_id}/buckets/{bucket_id}")
```

**NEW:**
```python
def delete(self, project_id: int, view_id: int, bucket_id: int) -> None:
    """
    Delete a bucket.

    Args:
        project_id: ID of the project
        view_id: ID of the view
        bucket_id: ID of the bucket
    """
    # ...
    self.client._request("DELETE", f"/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}")
```

## Test Status

- ✅ ViewsManager implemented and tested (test_views_and_buckets.py::TestViewsList - 2/2 passed)
- ⏳ BucketsManager updates pending
- ⏳ Bucket tests pending (test_views_and_buckets.py::TestBucketsInView)

## Next Steps

1. Apply these changes to vikunja_wrapper.py BucketsManager class
2. Run bucket tests: `pytest test_views_and_buckets.py::TestBucketsInView -v`
3. Update populate script to use view-aware bucket creation
4. Re-run accounting setup with auto-created buckets
