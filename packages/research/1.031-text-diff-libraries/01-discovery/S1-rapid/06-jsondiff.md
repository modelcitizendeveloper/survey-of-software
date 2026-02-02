# jsondiff

## Overview
**Package:** `jsondiff`
**Algorithm:** Recursive tree diff with JSON-specific optimizations
**Status:** Maintenance mode (stable, infrequent updates)
**Author:** Zbigniew Jędrzejewski-Szmek (zbyszek)
**First Released:** 2013
**Purpose:** Diff and patch JSON documents

## Description
A specialized library for comparing JSON documents. It understands JSON structure (objects, arrays) and produces compact, JSON-serializable diffs. Unlike generic object diff libraries, jsondiff is optimized for JSON's specific data model.

**Key features:**
- **JSON-native**: Designed specifically for JSON documents
- **Compact diffs**: Minimal representation of changes
- **Multiple output formats**: JSON Patch (RFC 6902), compact format, unified format
- **Patch application**: Apply diffs to JSON documents
- **Configurable**: Control how arrays and objects are compared
- **Command-line tool**: `jsondiff` CLI for quick comparisons

## Use Cases
- **API versioning**: Detect changes in JSON schemas
- **Configuration management**: Track JSON config changes
- **Testing**: Compare API responses
- **Data validation**: Verify JSON transformations
- **Audit logs**: Track document modifications

## Installation
```bash
pip install jsondiff
```

## Basic Usage

### Simple diff
```python
from jsondiff import diff

left = {
    "name": "Alice",
    "age": 30,
    "city": "NYC"
}

right = {
    "name": "Alice",
    "age": 31,
    "city": "LA",
    "email": "alice@example.com"
}

result = diff(left, right)
print(result)
```

Output:
```python
{
    'age': 31,
    'city': 'LA',
    'email': 'alice@example.com'
}
```

### Full diff with metadata
```python
from jsondiff import diff

left = {"a": 1, "b": 2}
right = {"a": 1, "b": 3, "c": 4}

result = diff(left, right, syntax='explicit')
print(result)
```

Output:
```python
{
    '$update': {
        'b': 3
    },
    '$insert': {
        'c': 4
    }
}
```

### Array diff
```python
from jsondiff import diff

left = [1, 2, 3, 4]
right = [1, 2, 5, 4, 6]

result = diff(left, right)
print(result)
```

Output:
```python
{
    2: 5,
    '$insert': [6]
}
```

### JSON Patch format (RFC 6902)
```python
from jsondiff import diff

left = {"name": "Alice", "age": 30}
right = {"name": "Bob", "age": 30}

result = diff(left, right, syntax='jsonpatch')
print(result)
```

Output:
```python
[
    {'op': 'replace', 'path': '/name', 'value': 'Bob'}
]
```

### Patch application
```python
from jsondiff import diff, patch

original = {"a": 1, "b": 2}
modified = {"a": 1, "b": 3, "c": 4}

# Create diff
diff_result = diff(original, modified)

# Apply patch
patched = patch(diff_result, original)
print(patched)  # {'a': 1, 'b': 3, 'c': 4}
```

### Command-line usage
```bash
# Compare two JSON files
jsondiff file1.json file2.json

# Output as JSON Patch
jsondiff --syntax jsonpatch file1.json file2.json

# Compare JSON strings
echo '{"a": 1}' | jsondiff - '{"a": 2}'
```

## Output Formats

### Compact (default)
```python
diff({"a": 1}, {"a": 2})
# Output: {'a': 2}
```

### Explicit
```python
diff({"a": 1}, {"a": 2}, syntax='explicit')
# Output: {'$update': {'a': 2}}
```

### Symmetric
```python
diff({"a": 1}, {"a": 2}, syntax='symmetric')
# Output: {'a': [1, 2]}
```

### JSON Patch (RFC 6902)
```python
diff({"a": 1}, {"a": 2}, syntax='jsonpatch')
# Output: [{'op': 'replace', 'path': '/a', 'value': 2}]
```

## Pros
- **JSON-specific**: Optimized for JSON's data model
- **Multiple formats**: Compact, explicit, JSON Patch support
- **Patch support**: Can apply diffs to documents
- **CLI tool**: Quick command-line comparisons
- **Compact output**: Minimal representation of changes
- **Configurable**: Control array comparison, object ordering

## Cons
- **Maintenance mode**: Infrequent updates
- **Limited to JSON**: Can't diff other data formats
- **Less feature-rich than DeepDiff**: Fewer comparison options
- **No semantic understanding**: Treats JSON as data, not structure

## When to Use
- **API testing**: Compare JSON responses
- **Schema validation**: Detect API changes
- **Config management**: Track JSON config changes
- **JSON Patch workflows**: Need RFC 6902 compliance
- **Audit logs**: Track document modifications

## When NOT to Use
- **Non-JSON data**: Use DeepDiff for general Python objects
- **Complex comparison logic**: DeepDiff has more features
- **Code diffing**: Use text diff or tree-sitter
- **Need active maintenance**: Library is stable but not actively developed

## Comparison with DeepDiff

| Feature | jsondiff | DeepDiff |
|---------|----------|----------|
| **Purpose** | JSON-specific | General Python objects |
| **JSON Patch** | ✓ (RFC 6902) | ✗ |
| **Ignore rules** | Limited | Extensive |
| **Custom operators** | ✗ | ✓ |
| **Maintenance** | Stable | Active |
| **Performance** | Fast (focused) | Slower (feature-rich) |

**Rule of thumb:**
- JSON documents → jsondiff (simpler, focused)
- Python objects → DeepDiff (more powerful)

## Popularity
- **GitHub stars:** ~400
- **PyPI downloads:** ~1.5M/month
- **Status:** Stable but not actively developed

## Real-World Usage
- **API testing frameworks**: JSON response validation
- **Config management tools**: Track JSON config changes
- **Data pipelines**: Validate JSON transformations
- **REST API clients**: Compare expected vs actual responses

## Related Libraries
- **DeepDiff**: More powerful, general-purpose object diff
- **jsonpatch**: JSON Patch implementation (RFC 6902/6901)
- **json-delta**: Alternative JSON diff library

## Verdict
**Best for:** JSON-specific diff operations, especially when you need JSON Patch (RFC 6902) format or a focused, lightweight tool for API testing.

**Skip if:** You need advanced comparison features (use DeepDiff), or you're diffing non-JSON Python objects.
