# zhconv (MediaWiki-based Chinese Converter)

**Repository:** https://github.com/gumblex/zhconv
**PyPI Package:** https://pypi.org/project/zhconv/
**GitHub Stars:** 563
**Primary Language:** Python (100% pure Python)
**Contributors:** 2
**Last Activity:** October 2, 2014 (inactive)
**License:** MIT (code), GPLv2+ (conversion tables)

## Quick Assessment

- **Popularity:** ⭐⭐⭐ Medium (563 stars, 4,251 weekly PyPI downloads)
- **Maintenance:** ❌ INACTIVE (last update 2014, abandoned)
- **Documentation:** ✅ Good (clear README, regional variant support documented)
- **Language Support:** Python only

## Pros

✅ **Regional Variants** - Supports zh-cn, zh-tw, zh-hk, zh-sg, zh-hans, zh-hant
✅ **MediaWiki Tables** - Uses Wikipedia's conversion dictionaries (high quality)
✅ **Maximum Forward Matching** - Better than simple character mapping
✅ **Pure Python** - No C++ dependencies, easy installation
✅ **Decent Download Count** - 4,251 weekly downloads (still used despite age)
✅ **Clean API** - Simple, intuitive function calls

## Cons

❌ **ABANDONED** - No updates since 2014 (12 years ago!)
❌ **Security Risk** - No security patches for 12 years
❌ **Outdated Dictionaries** - Conversion tables from 2014, missing new terms
❌ **Python 2 Compatibility** - Legacy code, may have Python 3 quirks
❌ **No Maintenance** - Bug reports unanswered, no roadmap
❌ **No Modern Features** - Missing advancements from past decade

## Quick Take

**DO NOT USE THE ORIGINAL zhconv.** It's been abandoned since 2014. While it still technically works and gets downloads (inertia from old projects), using it in 2026 is a bad decision:

- Security vulnerabilities won't be patched
- Conversion tables are 12 years out of date (missing new vocabulary)
- No Python 3.10+ testing/guarantees
- No support if things break

**HOWEVER:** There's a modern Rust-based replacement called **zhconv-rs** that:
- Uses the same MediaWiki conversion tables (updated)
- Offers 10-100x better performance (Aho-Corasick algorithm)
- Has active maintenance (2020s releases)
- Provides Python bindings: `pip install zhconv-rs`

If you liked zhconv's approach (MediaWiki tables, regional variants), use **zhconv-rs** instead.

## zhconv-rs: The Modern Alternative

```bash
# Install the Rust-based version
pip install zhconv-rs
# Or with OpenCC dictionaries
pip install zhconv-rs-opencc
```

**Key improvements:**
- ⚡ **10-100x faster** (Rust + Aho-Corasick)
- 🔄 **Updated dictionaries** (recent MediaWiki exports)
- ✅ **Active maintenance** (commits in 2020s)
- 🔒 **Memory safe** (Rust prevents common bugs)

## S1 Verdict: AVOID (Use zhconv-rs Instead)

**Confidence:** High (90%)

The original zhconv gets an **AVOID** rating due to abandonment. However, its spiritual successor **zhconv-rs** is worth considering if:
- You trust MediaWiki's conversion dictionaries
- You want better performance than pure Python
- You're willing to install Rust-compiled packages

**Ranking for original zhconv:** #3 out of 3 (DO NOT USE)
**Ranking for zhconv-rs:** Worth evaluating in S2 against OpenCC

## Installation (zhconv-rs)

```bash
pip install zhconv-rs
```

## Usage (zhconv-rs)

```python
from zhconv import convert

# Simplified to Traditional (Taiwan)
text = convert("中国", 'zh-tw')
print(text)  # 中國

# Regional variants:
# zh-cn: Mainland China Simplified
# zh-tw: Taiwan Traditional
# zh-hk: Hong Kong Traditional
# zh-sg: Singapore Simplified
# zh-hans: Simplified Chinese
# zh-hant: Traditional Chinese
```

## Warning About PyPI Downloads

The original zhconv still gets 4,251 weekly downloads because:
1. Old projects have it pinned in requirements.txt
2. Tutorials from 2015-2020 recommend it
3. People don't realize it's abandoned

**Don't be fooled by download counts.** Check the last commit date!

---

**Sources:**
- [GitHub - gumblex/zhconv](https://github.com/gumblex/zhconv)
- [PyPI - zhconv](https://pypi.org/project/zhconv/)
- [Snyk Security Advisor - zhconv](https://snyk.io/advisor/python/zhconv)
- [GitHub - Gowee/zhconv-rs](https://github.com/Gowee/zhconv-rs)
- [Libraries.io - zhconv analysis](https://libraries.io/pypi/zhconv)
