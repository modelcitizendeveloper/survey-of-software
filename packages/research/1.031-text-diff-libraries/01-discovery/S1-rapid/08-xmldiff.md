# xmldiff

## Overview
**Package:** `xmldiff`
**Algorithm:** Tree diff with XML-specific optimizations
**Status:** Active (regular updates)
**Author:** Lennart Regebro
**First Released:** 2002 (rewritten in 2017)
**Purpose:** Diff and patch XML documents

## Description
A library for finding differences between XML documents at the tree level. It understands XML structure (elements, attributes, text nodes) and produces diffs that respect XML semantics, not just text changes.

**Key features:**
- **Tree-based diff**: Compares XML DOM trees, not text
- **XML-aware**: Handles attributes, namespaces, CDATA
- **Patch support**: Generate and apply patches to XML
- **Multiple output formats**: XUpdate, diff format, HTML
- **Normalization**: Ignores insignificant whitespace
- **Fast algorithm**: Optimized tree diff

## Use Cases
- **Configuration management**: Track XML config changes
- **API versioning**: Compare XML schemas (XSD, WSDL)
- **Document processing**: Track changes in XML documents
- **Testing**: Compare expected vs actual XML output
- **CMS systems**: Version control for XML content

## Installation
```bash
pip install xmldiff
```

## Basic Usage

### Compare two XML strings
```python
from xmldiff import main, formatting

xml1 = """
<root>
    <person id="1">
        <name>Alice</name>
        <age>30</age>
    </person>
</root>
"""

xml2 = """
<root>
    <person id="1">
        <name>Alice</name>
        <age>31</age>
    </person>
    <person id="2">
        <name>Bob</name>
        <age>25</age>
    </person>
</root>
"""

diff = main.diff_texts(xml1, xml2)
print(diff)
```

Output (simplified):
```
[UpdateTextIn('/root/person[1]/age', '31'),
 InsertNode('/root', 'person', 1)]
```

### Formatted diff output
```python
from xmldiff import main

xml1 = "<root><a>1</a></root>"
xml2 = "<root><a>2</a></root>"

# Human-readable diff
formatter = formatting.DiffFormatter()
diff = main.diff_texts(xml1, xml2, formatter=formatter)
print(diff)
```

Output:
```
[update] /root/a: 1 → 2
```

### Apply patch
```python
from xmldiff import main
from lxml import etree

xml1 = "<root><a>1</a></root>"
xml2 = "<root><a>2</a></root>"

# Generate diff
diff = main.diff_texts(xml1, xml2)

# Parse original XML
tree = etree.fromstring(xml1.encode())

# Apply patch
main.patch_tree(tree, diff)

# Result matches xml2
result = etree.tostring(tree, encoding='unicode')
print(result)  # <root><a>2</a></root>
```

### Ignore whitespace
```python
from xmldiff import main

xml1 = "<root>\n  <a>value</a>\n</root>"
xml2 = "<root><a>value</a></root>"

# With normalization (default), whitespace is ignored
diff = main.diff_texts(xml1, xml2)
print(diff)  # [] (no difference)
```

### Compare XML files
```python
from xmldiff import main

diff = main.diff_files('file1.xml', 'file2.xml')
print(diff)
```

### HTML diff output
```python
from xmldiff import main

xml1 = "<root><a>old</a></root>"
xml2 = "<root><a>new</a></root>"

html = main.diff_texts(xml1, xml2,
                       formatter=main.formatting.HTMLFormatter())
# Returns HTML with highlighted changes
```

## Output Formats

### XUpdate (default)
Standard XML diff/patch format
```python
diff = main.diff_texts(xml1, xml2)
# Returns list of edit operations
```

### Text formatter
```python
from xmldiff.formatting import DiffFormatter
diff = main.diff_texts(xml1, xml2, formatter=DiffFormatter())
# Returns human-readable text
```

### HTML formatter
```python
from xmldiff.formatting import HTMLFormatter
html = main.diff_texts(xml1, xml2, formatter=HTMLFormatter())
# Returns HTML with visual diff
```

### XML formatter
```python
from xmldiff.formatting import XMLFormatter
xml = main.diff_texts(xml1, xml2, formatter=XMLFormatter())
# Returns diff as XML document
```

## Algorithm
Uses an **ordered tree diff algorithm** that:
1. Matches nodes by identity (attributes, position)
2. Computes minimum edit distance on trees
3. Handles moves, inserts, deletes, updates
4. Respects XML semantics (element order matters)

**Complexity:** O(n * m) where n and m are tree sizes, but optimized for typical XML structures.

## Pros
- **XML-aware**: Understands elements, attributes, namespaces
- **Tree-based**: Not fooled by formatting/whitespace changes
- **Patch support**: Can apply diffs to documents
- **Multiple formats**: XUpdate, HTML, text
- **Normalization**: Ignores insignificant differences
- **Active maintenance**: Regular updates

## Cons
- **XML-only**: Can't diff other formats
- **Complexity**: More complex than text diff
- **Performance**: Slower than text diff for large documents
- **Learning curve**: XML and XPath knowledge helpful

## When to Use
- **XML configuration**: Track changes in config files
- **Schema versioning**: Compare XSD, WSDL, SOAP
- **Document management**: Version control for XML content
- **API contracts**: Detect breaking changes in XML APIs
- **Testing**: Validate XML output matches expected

## When NOT to Use
- **Non-XML data**: Use appropriate diff tool (JSON, YAML, etc.)
- **Large documents**: May be slow (consider text diff)
- **HTML**: Use specialized HTML diff tools
- **Simple text**: Overkill for basic text diff

## Comparison with Text Diff

| Feature | xmldiff | Text Diff |
|---------|---------|-----------|
| **Structural understanding** | ✓ | ✗ |
| **Attribute changes** | ✓ | Limited |
| **Namespace handling** | ✓ | ✗ |
| **Whitespace normalization** | ✓ | Manual |
| **Performance** | Slower | Faster |

## Popularity
- **GitHub stars:** ~200
- **PyPI downloads:** ~400k/month
- **Status:** Active, well-maintained

## Real-World Usage
- **Configuration management tools**: XML config versioning
- **SOAP API testing**: Compare WSDL/SOAP responses
- **Document management systems**: Track XML document changes
- **Build systems**: Validate XML transformations (XSLT, etc.)

## Related Libraries
- **lxml**: XML parsing (xmldiff dependency)
- **jsondiff**: JSON-specific diff
- **deepdiff**: General Python object diff

## Verdict
**Best for:** XML document comparison where you need to understand structural changes, not just text differences. Essential for XML-heavy workflows (configuration, schemas, SOAP).

**Skip if:** You're not working with XML, or simple text diff is sufficient. For other formats, use specialized tools (jsondiff for JSON, etc.).
