# S1 Rapid Discovery: Recommendation

## Quick Decision Guide

For rapid selection of TMX translation memory libraries in Python:

### Default Choice: translate-toolkit
**Use when**: You need production-ready TMX support and don't have specific constraints

**Rationale**:
- Battle-tested in enterprise localization workflows
- Active maintenance (v3.18.1, Jan 2026)
- Comprehensive format support (TMX + 20 other formats)
- Command-line tools for automation
- 933 GitHub stars, used by Weblate, Pootle

**Trade-off**: GPL-2.0+ license may restrict commercial use

### Modern Alternative: hypomnema
**Use when**: You need full TMX 1.4b Level 2 support or MIT licensing

**Rationale**:
- Full TMX Level 2 (nested inline markup)
- Type-safe Python 3.12+ with full type hints
- Streaming API for large files (constant memory)
- MIT license (commercial-friendly)
- Modern architecture, policy-driven validation

**Trade-off**: Pre-1.0 status means breaking API changes possible

### PO Workflow Bridge: polib
**Use when**: Your primary format is gettext PO, TMX is secondary

**Rationale**:
- Mature PO/POT/MO library (v1.2.0)
- MIT license
- Zero dependencies
- Convert PO↔TMX via translate-toolkit
- Wide Python version support (2.7-3.11)

**Trade-off**: Not native TMX support, requires translate-toolkit for conversion

## Quick Comparison

| Aspect | translate-toolkit | hypomnema | polib |
|--------|------------------|-----------|-------|
| **Status** | Production | Pre-1.0 | Mature |
| **TMX Native** | Yes (Level 1) | Yes (Level 2) | No (conversion) |
| **License** | GPL-2.0+ | MIT | MIT |
| **Python** | ≥3.11 | ≥3.12 | 2.7-3.11 |
| **Stars** | 933 | 8 | N/A |
| **Streaming** | No | Yes | No |

## Decision Tree

```
Need TMX support?
├─ Yes
│  ├─ Need Level 2 inline markup?
│  │  ├─ Yes → hypomnema (only option)
│  │  └─ No
│  │     ├─ GPL acceptable? → translate-toolkit (production-ready)
│  │     └─ Need MIT license? → hypomnema (modern) or polib+conversion (mature)
│  │
│  └─ Commercial product?
│     ├─ Yes → hypomnema or polib (MIT license)
│     └─ No → translate-toolkit (comprehensive)
│
└─ No, working with PO files?
   └─ Yes → polib (mature, purpose-built)
```

## Use Case Recommendations

### Enterprise Localization Pipeline
**Choice**: translate-toolkit

**Reason**: Production stability, multi-format support (TMX/PO/XLIFF), CLI tools for CI/CD, QA checks

### NLP/Machine Translation Data Extraction
**Choice**: hypomnema

**Reason**: Streaming API for large corpora, policy-driven parsing for messy real-world TMX, Level 2 support for inline markup

### Django/Flask Internationalization
**Choice**: polib (+ translate-toolkit for TMX)

**Reason**: Native framework integration, PO-friendly version control, convert to TMX when needed

### Custom CAT Tool Development
**Choice**: hypomnema

**Reason**: Full Level 2 support, type-safe API, MIT license for commercial distribution

### Cross-Format Translation Management
**Choice**: translate-toolkit

**Reason**: Handles 20+ formats, unified API, format conversion tools

## Key Insights from S1

1. **Only 2-3 libraries exist** for TMX translation memory in Python (small ecosystem)
2. **Name collision**: "tmxlib" is for game tile maps, NOT translation memory
3. **Level 2 support rare**: Only hypomnema supports full TMX 1.4b Level 2 (nested inline markup)
4. **Licensing matters**: GPL (translate-toolkit) vs MIT (hypomnema, polib) affects commercial use
5. **PO ecosystem mature**: polib + translate-toolkit enables PO↔TMX workflows

## Next Steps

After choosing a library:

1. **Validate with your data**: Test parsing/writing with actual TMX files
2. **Check Level requirements**: Verify if Level 1 or Level 2 features needed
3. **License review**: Ensure GPL or MIT aligns with project requirements
4. **Integration test**: Confirm compatibility with existing tools (CAT tools, CI/CD)
5. **Performance baseline**: Measure memory/speed with representative file sizes

## When to Reconsider

**Upgrade from translate-toolkit to hypomnema if**:
- TMX Level 2 features become required
- GPL licensing creates legal issues
- Large file processing needs streaming API

**Downgrade from hypomnema to translate-toolkit if**:
- Pre-1.0 API instability causes production issues
- Need multi-format support (PO, XLIFF, TBX)
- Require mature ecosystem and commercial support

**Add polib to workflow if**:
- Developers prefer PO format for version control
- Framework integration (Django/Flask) beneficial
- Git-friendly text format preferred over XML

## Resources

- **translate-toolkit**: https://docs.translatehouse.org/projects/translate-toolkit/
- **hypomnema**: https://github.com/EnzoAgosta/hypomnema
- **polib**: http://polib.readthedocs.org/
- **TMX Spec**: https://www.gala-global.org/tmx-14b
