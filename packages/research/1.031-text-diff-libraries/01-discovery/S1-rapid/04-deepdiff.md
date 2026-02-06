# DeepDiff

## Overview
**Package:** `deepdiff`
**Algorithm:** Recursive tree diff
**Status:** Active (frequent updates)
**Author:** Sep Dehpour (seperman)
**First Released:** 2014
**Purpose:** Deep difference and search of Python objects

## Description
A powerful library for finding differences between Python objects (dicts, lists, sets, custom objects). Unlike text diff libraries, DeepDiff understands Python data structures and can handle nested objects, type changes, and complex comparisons.

**Key features:**
- **Deep comparison**: Recursively compare nested structures
- **Type-aware**: Detects type changes, not just value changes
- **Delta objects**: Generate serializable change sets
- **Ignore rules**: Skip certain keys, paths, or types
- **Custom operators**: Define comparison logic for custom classes
- **JSON serialization**: Export diffs as JSON
- **Search**: Find items in nested structures (DeepSearch)

## Use Cases
- **Testing**: Assert complex data structures match expected output
- **API versioning**: Detect breaking changes in JSON schemas
- **Config management**: Track configuration changes
- **Data validation**: Compare database records before/after updates
- **Debugging**: Find unexpected changes in object state

## Installation
```bash
pip install deepdiff
```

## Basic Usage

### Compare dictionaries
```python
from deepdiff import DeepDiff

t1 = {
    'name': 'Alice',
    'age': 30,
    'address': {'city': 'NYC', 'zip': '10001'}
}

t2 = {
    'name': 'Alice',
    'age': 31,
    'address': {'city': 'LA', 'zip': '90001'},
    'email': 'alice@example.com'
}

diff = DeepDiff(t1, t2)
print(diff)
```

Output:
```python
{
    'values_changed': {
        "root['age']": {'new_value': 31, 'old_value': 30},
        "root['address']['city']": {'new_value': 'LA', 'old_value': 'NYC'},
        "root['address']['zip']": {'new_value': '90001', 'old_value': '10001'}
    },
    'dictionary_item_added': {"root['email']"}
}
```

### Compare lists
```python
from deepdiff import DeepDiff

t1 = [1, 2, 3, 4]
t2 = [1, 2, 5, 4, 6]

diff = DeepDiff(t1, t2)
print(diff)
```

Output:
```python
{
    'values_changed': {"root[2]": {'new_value': 5, 'old_value': 3}},
    'iterable_item_added': {"root[4]": 6}
}
```

### Ignore order in lists
```python
from deepdiff import DeepDiff

t1 = [1, 2, 3]
t2 = [3, 2, 1]

# With order ignored
diff = DeepDiff(t1, t2, ignore_order=True)
print(diff)  # {} (no difference)

# With order enforced (default)
diff = DeepDiff(t1, t2)
print(diff)  # Shows reordering as changes
```

### Ignore certain keys
```python
from deepdiff import DeepDiff

t1 = {'name': 'Alice', 'timestamp': 1234567890}
t2 = {'name': 'Alice', 'timestamp': 9999999999}

# Ignore timestamp changes
diff = DeepDiff(t1, t2, exclude_paths=["root['timestamp']"])
print(diff)  # {} (timestamp ignored)
```

### Type changes
```python
from deepdiff import DeepDiff

t1 = {'value': 42}
t2 = {'value': '42'}

diff = DeepDiff(t1, t2)
print(diff)
```

Output:
```python
{
    'type_changes': {
        "root['value']": {
            'old_type': int,
            'new_type': str,
            'old_value': 42,
            'new_value': '42'
        }
    }
}
```

### Generate delta and apply
```python
from deepdiff import DeepDiff, Delta

t1 = {'a': 1, 'b': 2}
t2 = {'a': 1, 'b': 3, 'c': 4}

# Create delta
diff = DeepDiff(t1, t2)
delta = Delta(diff)

# Apply delta
t1_updated = t1 + delta
print(t1_updated)  # {'a': 1, 'b': 3, 'c': 4}

# Reverse delta
t2_reverted = t2 - delta
print(t2_reverted)  # {'a': 1, 'b': 2}
```

### Serialize to JSON
```python
from deepdiff import DeepDiff
import json

t1 = {'a': 1}
t2 = {'a': 2}

diff = DeepDiff(t1, t2)
diff_json = diff.to_json()
print(json.dumps(json.loads(diff_json), indent=2))
```

## Pros
- **Python-native**: Understands dicts, lists, sets, tuples, custom objects
- **Type-aware**: Detects type changes, not just value changes
- **Flexible ignore rules**: Skip keys, regex paths, types
- **Delta support**: Generate and apply change sets
- **JSON serialization**: Export diffs for storage/transmission
- **Active development**: Frequent updates, responsive maintainer
- **Rich comparison**: Handles edge cases (NaN, circular refs, etc.)

## Cons
- **Not for text diff**: Designed for objects, not line-based text
- **Performance**: Slower than text diff for large text files
- **Complexity**: More features = steeper learning curve
- **Memory usage**: Recursion can be expensive for deep structures

## When to Use
- **Testing**: Compare complex data structures in assertions
- **API testing**: Validate JSON responses
- **Config management**: Track changes in configuration files
- **Data pipelines**: Verify data transformations
- **Database testing**: Compare records before/after operations
- **Object state tracking**: Debug unexpected object mutations

## When NOT to Use
- **Text files**: Use `difflib` or `diff-match-patch`
- **Line-based diff**: Not designed for code review
- **Version control**: Use git or text diff tools
- **Performance-critical**: Slower than specialized text diff

## Related Libraries
- **DeepSearch**: Find items in nested structures (same author)
- **jsondiff**: JSON-specific diff (simpler, less features)
- **dictdiffer**: Similar but less actively maintained

## Popularity
- **GitHub stars:** ~2k
- **PyPI downloads:** ~15M/month
- **Status:** Very active, widely used in testing frameworks

## Real-World Usage
- **pytest**: Compare complex test outputs
- **API testing frameworks**: Validate responses
- **Data validation libraries**: Schema comparison
- **ETL pipelines**: Verify data transformations

## Verdict
**Best for:** Comparing Python objects (dicts, lists, custom classes) in tests, data validation, and config management. The go-to library for non-text diff needs.

**Skip if:** You need text diff, code review, or version control functionality. Use `difflib` or `diff-match-patch` instead.
