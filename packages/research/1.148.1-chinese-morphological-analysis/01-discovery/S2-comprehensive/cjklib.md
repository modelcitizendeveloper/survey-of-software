# cjklib - Comprehensive Assessment

## Python 3 Compatibility Status

**Original cjklib:** Python 2 only. No Python 3 support in the main [cburgmer/cjklib](https://github.com/cburgmer/cjklib) repository.

**cjklib3 Fork:** Python 3.7+ compatible fork available at [free-utils-python/cjklib3](https://github.com/free-utils-python/cjklib3). Requires 2to3 conversion during installation:

```bash
conda create -n py37 python=3.7
conda activate py37
git clone https://github.com/free-utils-python/cjklib3
cd cjklib3
pip install 2to3
2to3 -w .
# Build database, install dictionaries
```

**Verdict:** Python 3 is possible but requires fork and manual setup. Not pip-installable for Python 3.

## Character Decomposition Capabilities

### IDS Support
- **Full IDS (Ideographic Description Sequences)** implementation
- Stores decompositions using Unicode IDS operators (⿰, ⿱, ⿲, etc.)
- Example: 好 = ⿰女子 (left-right: woman + child)

### API Features
From [characterlookup module](https://cjklib.readthedocs.io/en/0.3.2/library/cjklib.characterlookup.html):
- `getDecompositionEntries()` - Get all decomposition trees
- `getRadicalForms()` - Get radical variants
- `getStrokeCount()` - Character stroke counts
- `getCharacterVariants()` - Traditional/simplified variants

### Data Quality
- Comprehensive coverage of CJK Unified Ideographs
- Multiple decomposition paths for characters with variant structures
- Kangxi radical mappings
- Component-to-stroke mappings for analysis

## Limitations

### Maintenance Concerns
- Original project: Last PyPI release unclear
- Documentation references Python 2
- Open [issue #11](https://github.com/cburgmer/cjklib/issues/11) requesting Python 3 support from 2017
- [Snyk analysis](https://snyk.io/advisor/python/cjklib) shows no recent releases

### Installation Complexity
- Not simple pip install for Python 3
- Requires building database from source
- Dictionary installation separate step
- Fork-based solution not ideal for production

## Alternative: Data Sources Only

Instead of using cjklib as a library, consider using its data sources:
- CJKVI-IDS database: [cjkvi/cjkvi-ids](https://github.com/cjkvi/cjkvi-ids)
- Parse IDS strings directly
- Simpler integration, modern Python code

## Compound Word Analysis

**None** - cjklib operates at character level only. No word segmentation or compound analysis features.

## Production Readiness

**Moderate Risk:**
- ✅ Proven character decomposition algorithms
- ✅ Comprehensive data coverage
- ❌ Python 2 legacy code
- ❌ Requires fork for Python 3
- ❌ Setup complexity
- ❌ Unclear maintenance status

**Recommendation:** Use cjklib3 fork for prototyping, but investigate migrating to IDS database parsing with modern Python for production.

---

Sources:
- [cjklib Documentation](https://cjklib.readthedocs.io/en/latest/)
- [cjklib3 Python 3 Fork](https://github.com/free-utils-python/cjklib3)
- [Original cjklib GitHub](https://github.com/cburgmer/cjklib)
- [Python 3 Support Issue](https://github.com/cburgmer/cjklib/issues/11)
- [CJKVI-IDS Database](https://github.com/cjkvi/cjkvi-ids)
