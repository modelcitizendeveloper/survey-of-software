# CJKVI (CJK Variation & Interchange)

**Source:** cjkvi.org, ISO/IEC 10646 Ideographic Variation Database
**Format:** XML (IVD), text files
**License:** Open source / ISO standard
**Size:** ~10MB (variant mappings)
**Last Updated:** 2025-01 (quarterly updates)

## Quick Assessment

- **Adoption:** 🟡 Medium - Used by font vendors, publishing systems
- **Maintenance:** 🟢 Active - Regular updates via Unicode/ISO
- **Documentation:** 🟢 Good - IVD specification, practical examples
- **Standards Compliance:** ✅ ISO/Unicode official (IVD registered variants)

## What It Provides

**Core Data:**
- **Variant mappings:** Simplified ↔ Traditional, regional glyphs
- **Cross-language equivalence:** Same character, different preferred forms (China/Japan/Korea)
- **IVD (Ideographic Variation Database):** Official variant sequences
- **Glyph interchange:** Safe character substitution rules
- **Font selection guidance:** Which glyph to render per locale

**Key Mappings:**
- Simplified Chinese ↔ Traditional Chinese
- Japanese kanji variants (新字体 vs 旧字体)
- Korean hanja variants
- Hong Kong variants (HKSCS)
- Taiwan variants (Big5)

## Pros

- **Locale-aware:** Handles regional character preferences
- **Font-agnostic:** Defines variants independent of rendering
- **Standard-based:** ISO/Unicode official variant registry
- **Practical focus:** Solves real-world interchange problems
- **Compact:** Small dataset, easy integration
- **Clear scope:** Focused on variants, not general character properties

## Cons

- **Limited to variants:** Doesn't provide definitions, pronunciations, or structure
- **Incomplete mappings:** Not all characters have documented variants
- **Locale complexity:** China/Taiwan/Hong Kong differences can be subtle
- **Not bidirectional:** Some mappings are one-way (multiple simplified → one traditional)
- **Requires context:** Must know user's locale to apply correctly

## Quick Take

**The variant normalizer.** CJKVI solves the specific problem of character variants across locales - essential for search, content deduplication, and multi-market applications. Use alongside Unihan (backbone) and IDS (structure) for complete coverage.

**Integration complexity:** Low. Simple mappings, straightforward lookup tables. Main challenge is deciding WHEN to normalize (search time vs index time).

## Rapid Validation Checks

✅ **Official:** ISO/IEC 10646 IVD registry
✅ **Current:** Updated January 2025
✅ **Accessible:** Public download from Unicode IVD site
✅ **Documented:** IVD specification, practical guides
✅ **Proven:** Used by Adobe, Google Fonts, Microsoft Office

## Popularity Signals

- **Standard adoption:** All major font vendors implement IVD
- **GitHub mentions:** 30+ CJKVI/IVD processing libraries
- **Production use:** Adobe Source Han fonts, Google Noto CJK
- **Ecosystem integration:** Built into HarfBuzz text shaping engine

## Speed Score: 7.5/10

**Why 7.5?** Solves a critical problem (variants) efficiently, but narrow scope. High value for multi-locale applications, less relevant for single-market products.

## Use Case Fit (Rapid Assessment)

**Strong fit:**
- Multi-market e-commerce (CN/TW/HK/JP search normalization)
- Publishing systems (locale-appropriate glyph selection)
- Content deduplication (recognize simplified/traditional as "same")
- Font rendering (pick correct glyph per locale)

**Weak fit:**
- Single-locale applications (less critical)
- Semantic analysis (CHISE better)
- Structural decomposition (IDS better)

## Relationship to Other Databases

**CJKVI complements Unihan:** Unihan provides `kSimplifiedVariant`/`kTraditionalVariant` fields, but CJKVI adds deeper regional variant handling (HK/TW differences, Japanese old/new forms).

**CJKVI ≠ IDS:** IDS describes structure, CJKVI describes equivalence. Different problems.

**CJKVI ⊂ Unicode IVD:** The broader Ideographic Variation Database includes CJKVI data plus vendor-specific variants (Adobe Japan1, Hanyo-Denshi).

## Real-World Example

**Problem:** User searches "学習" (Japanese) but content has "學習" (traditional form). Without CJKVI variant mapping, search fails.

**Solution:** Normalize search queries using CJKVI mappings:
- 学 → 學 (simplified → traditional)
- 習 → 習 (same in both)

Result: Successful cross-locale search.

## Integration Pattern (Rapid)

```
User input (any locale)
  ↓
CJKVI normalization
  ↓
Canonical form (e.g., traditional)
  ↓
Index lookup (variant-aware)
  ↓
Results (all relevant forms)
```

Simple lookup table, low overhead, high value for multi-market apps.
