# S1: Rapid Search - Python QR Code Generation Libraries

**Experiment**: 1.080.1 - QR Code Generation Libraries
**Methodology**: S1 - Rapid Search (Focus on popular solutions & ecosystem)
**Date**: 2025-10-13
**Time Spent**: ~20 minutes

## Popular Libraries Found

### 1. qrcode (python-qrcode)

**PyPI Package**: `qrcode`
**GitHub**: lincolnloop/python-qrcode
**Stars**: 4,800
**Downloads/Month**: 6,087,537
**Latest Version**: 8.2
**Last Update**: May 1, 2025

**Description**: Pure Python QR Code generator with extensive customization options. Supports multiple output formats (PNG, SVG, console), styled QR codes with colors and embedded images, and all error correction levels.

**Primary Use Case**: General-purpose QR code generation with emphasis on customization and visual styling. Great for applications requiring branded or artistic QR codes.

---

### 2. segno

**PyPI Package**: `segno`
**GitHub**: heuer/segno
**Stars**: 716
**Downloads/Month**: 561,296
**Latest Version**: 1.6.6
**Last Update**: Mar 12, 2025

**Description**: Pure Python QR Code and Micro QR Code encoder with zero dependencies. Implements ISO/IEC 18004:2015(E) standard. Fastest pure Python implementation with 1500+ test cases and >98% coverage.

**Primary Use Case**: Standards-compliant QR code generation where dependencies are a concern. Best for Micro QR codes, performance-critical applications, and environments requiring strict ISO compliance.

---

### 3. PyQRCode

**PyPI Package**: `PyQRCode`
**GitHub**: mnooner256/pyqrcode
**Stars**: 77
**Downloads/Month**: 374,335
**Latest Version**: 1.2.1
**Last Update**: Jun 20, 2016

**Description**: Pure Python QR code generator with SVG, EPS, PNG, and terminal output. Simple two-line API for basic QR code generation.

**Primary Use Case**: Simple, straightforward QR code generation with minimal configuration. Best for basic use cases requiring SVG or terminal output.

**Note**: Last updated in 2016 - maintenance status unclear.

---

### 4. qrcodegen (Nayuki)

**PyPI Package**: `qrcodegen`
**GitHub**: nayuki/QR-Code-generator
**Stars**: 6,200 (entire repo, multi-language)
**Downloads/Month**: 9,950
**Latest Version**: 1.8.0
**Last Update**: Recent (active maintenance)

**Description**: High-quality QR Code generator library emphasizing correctness and clarity. Part of multi-language project (Java, TypeScript, Python, Rust, C++, C). Supports all 40 versions and all 4 error correction levels.

**Primary Use Case**: Applications requiring absolute correctness and a multi-language ecosystem. Ideal when you need consistent QR code generation across different platforms/languages.

---

## Quick Comparison Table

| Library | Downloads/Month | GitHub Stars | Last Update | Dependencies | Key Strength |
|---------|----------------|--------------|-------------|--------------|--------------|
| **qrcode** | 6,087,537 | 4,800 | May 2025 | Pillow/pypng (optional) | Customization & styling |
| **segno** | 561,296 | 716 | Mar 2025 | None | Standards compliance, performance |
| **PyQRCode** | 374,335 | 77 | Jun 2016 | pypng (optional) | Simplicity |
| **qrcodegen** | 9,950 | 6,200 | Recent | None | Multi-language, correctness |

---

## Initial Recommendation

**For typical use cases: `qrcode` (python-qrcode)**

**Rationale**:
- **Overwhelming popularity**: 10x more downloads than the next competitor, indicating strong community trust and adoption
- **Active maintenance**: Updated May 2025, showing ongoing development
- **Rich feature set**: Comprehensive customization options (colors, styling, embedded images)
- **Mature ecosystem**: Large user base means better documentation, more tutorials, and faster issue resolution
- **Flexible output**: Supports PNG, SVG, and terminal output
- **Proven in production**: Wide adoption suggests battle-tested reliability

**When to consider alternatives**:
- **segno**: If you need zero dependencies, Micro QR codes, or strict ISO/IEC 18004:2015 compliance. This is commonly chosen for production systems requiring standards compliance and no-dependency design.
- **qrcodegen**: If building multi-platform applications requiring identical QR code generation across languages, or when correctness is absolutely critical.
- **PyQRCode**: Not recommended due to 9-year maintenance gap (last update 2016).

---

## Production Use Case: Business Card Printing System

Example production deployment: A business card printing system uses `segno` for QR code generation. This choice demonstrates several advantages:

**Strengths of this approach**:
- Zero dependencies reduces deployment complexity
- Standards-compliant (ISO/IEC 18004:2015)
- Strong test coverage (>98%)
- Active maintenance (updated Mar 2025)
- Good performance for pure Python

**Trade-off considerations**:
- Advanced styling/branding features: `qrcode` offers more options
- Community size: `qrcode`'s larger community provides more resources/plugins
- Use case fit: For standard business QR codes, `segno` is typically sufficient

**Pattern observed**: For standards-compliant, dependency-free deployments, `segno` is a solid professional choice. Migration decisions should be based on specific feature requirements rather than popularity metrics alone.

---

## Methodology Notes

**Search Strategy**:
1. Web searches for "Python QR code library" + "downloads" + "comparison"
2. Checked PyPI pages for version/update info
3. Fetched pypistats.org for download statistics
4. Reviewed GitHub repositories for stars/activity
5. Cross-referenced Segno's own comparison documentation

**Data Sources**:
- pypistats.org (download statistics)
- PyPI (version/release dates)
- GitHub (stars, activity)
- Official documentation

**Limitations**:
- Download stats can include CI/CD, bots, mirrors
- GitHub stars don't always reflect production usage
- Didn't test actual code quality or performance
- Focused on popularity metrics over technical deep-dive
