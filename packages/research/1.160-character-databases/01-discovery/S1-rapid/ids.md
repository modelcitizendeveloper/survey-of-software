# IDS (Ideographic Description Sequences)

**Source:** cjkvi.org, Unicode IDS files
**Format:** Text (IDS notation), integrated into Unihan
**License:** Public domain / Unicode License
**Size:** ~5MB (IDS data only)
**Last Updated:** 2025-03 (maintained by CJK-VI group)

## Quick Assessment

- **Adoption:** 🟡 Medium - Standard notation, used by IMEs and handwriting recognition
- **Maintenance:** 🟢 Active - Updates via CJK-VI and Unicode
- **Documentation:** 🟡 Good - Unicode TR37, examples in Unihan
- **Standards Compliance:** ✅ Official Unicode notation (TR37)

## What It Provides

**Core Data:**
- **Structural decomposition:** Break characters into components
- **IDS sequences:** Standard notation for character structure (e.g., 好 = ⿰女子)
- **Component search:** Find characters containing specific radicals/parts
- **Handwriting input support:** Enables stroke-order and structure-based IMEs

**IDS Operators (12 total):**
- `⿰` Left-right (好 = ⿰女子, woman + child)
- `⿱` Top-bottom (字 = ⿱宀子, roof + child)
- `⿴` Surround (国 = ⿴囗玉, enclosure + jade)
- `⿵` Surround-bottom (同 = ⿵冂一, frame + horizontal)
- [8 more operators for complex structures]

## Pros

- **Standard notation:** Unicode-official, widely supported
- **Precise structure:** Unambiguous component breakdown
- **Handwriting-friendly:** Enables structure-based character input
- **Compact:** Efficient representation (5MB for 98K+ characters)
- **Integrated:** Available in Unihan `kIDS` field
- **Machine-readable:** Easy parsing for algorithmic use

## Cons

- **Ambiguity in variants:** Same character may have multiple valid IDS
- **Component identification:** Requires radical/component knowledge
- **Not phonetic:** Only handles visual structure, not pronunciation
- **Limited semantics:** Structural decomposition ≠ semantic relationships
- **Coverage gaps:** Some rare characters lack IDS data

## Quick Take

**Essential for input methods.** IDS is the standard for describing character structure, critical for handwriting recognition, component-based search, and IME development. Simpler than CHISE (focused only on structure, not semantics) but less comprehensive than full ontology.

**Integration complexity:** Low-Medium. IDS notation is straightforward, but building search indexes requires some parsing logic.

## Rapid Validation Checks

✅ **Official:** Unicode Technical Report 37
✅ **Current:** Updated March 2025
✅ **Accessible:** Included in Unihan `kIDS` field
✅ **Documented:** TR37 specification, examples
✅ **Proven:** Powers handwriting input on Android/iOS CJK keyboards

## Popularity Signals

- **Standard adoption:** All major CJK IMEs use IDS notation
- **GitHub implementations:** 50+ IDS parsing libraries
- **Stack Overflow:** IDS mentioned in 100+ CJK input questions
- **Production use:** Google Pinyin, Microsoft IME, Apple Handwriting

## Speed Score: 7.0/10

**Why 7.0?** Focused scope (structure only), good integration with Unihan, but requires supplementary data for semantics. Excellent for specific use cases (IMEs, handwriting), less critical for text rendering alone.

## Use Case Fit (Rapid Assessment)

**Strong fit:**
- Handwriting recognition systems
- Component-based character search
- IME development
- Character learning apps (structure visualization)

**Weak fit:**
- Pure text rendering (Unihan sufficient)
- Semantic search (CHISE better)
- Variant normalization (CJKVI focused)

## Relationship to Other Databases

**IDS ⊂ CHISE:** CHISE includes IDS data plus semantics/etymology
**IDS ⊂ Unihan:** Unihan `kIDS` field contains IDS sequences
**IDS ≠ Variants:** IDS describes structure, CJKVI describes variant relationships

**Recommendation:** Use IDS via Unihan's `kIDS` field unless you need CHISE's full ontology.
