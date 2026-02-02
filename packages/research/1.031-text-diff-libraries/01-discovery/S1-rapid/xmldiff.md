# xmldiff

## Overview
- **Package**: xmldiff (PyPI)
- **Status**: Active (regular updates)
- **Popularity**: ~200 GitHub stars, ~400k PyPI downloads/month
- **Scope**: XML-specific tree diff (understands XML structure)

## Algorithm
- **Core**: Tree diff algorithm optimized for XML DOM
- **Structure-aware**: Knows elements, attributes, text nodes, namespaces
- **XUpdate format**: Standard XML patch format
- **Normalization**: Handles whitespace, attribute order

## Best For
- **XML document comparison**: Config files, data exports, SOAP messages
- **XML patch generation**: Standardized update format (XUpdate)
- **Content management**: Comparing XML-based document versions
- **Configuration diff**: XML config files (Spring, Maven, etc.)
- **Testing**: Validating XML output against expected

## Trade-offs

**Strengths:**
- XML-aware (understands elements, attributes, namespaces)
- Tree-based (structural comparison, not text diff)
- XUpdate patches (standard format)
- Namespace support (handles XML namespaces correctly)
- Patch application (apply patches to XML documents)
- HTML output (formatted diff display)

**Limitations:**
- XML-only (not for JSON, text, or other formats)
- Slower than text diff (tree parsing overhead)
- Requires lxml (C extension dependency)
- Small community (less popular than JSON tools)
- Limited compared to specialized XML tools

## Ecosystem Fit
- **Dependencies**: lxml (C extension, needs build tools)
- **Platform**: All (with C compiler for lxml)
- **Python**: 3.x
- **Maintenance**: Active (regular updates)
- **Risk**: Low (stable, focused)

## Quick Verdict
**Use this for XML-specific diff** when text diff produces unhelpful output (attribute order, whitespace differences). If you're comparing XML occasionally and text diff is sufficient, stick with difflib. This is for XML-heavy workflows.
