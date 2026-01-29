# Stroke Order Resources: Quick Reference

**Research ID**: research-k6iy
**Date**: 2026-01-29
**Pass**: S1 (Rapid Discovery)

## TL;DR

Need stroke order data for CJK characters? Start here:

| Resource | Language | Coverage | Best For |
|----------|----------|----------|----------|
| [Hanzi Writer](https://hanziwriter.org/) | Chinese | 9,000+ | Web apps (easiest) |
| [Make Me a Hanzi](https://github.com/skishore/makemeahanzi) | Chinese | 9,000+ | Custom implementations |
| [KanjiVG](https://github.com/KanjiVG/kanjivg) | Japanese | Kanji | Production-ready SVGs |
| [animCJK](https://github.com/parsimonhi/animCJK) | CJK (all) | 7,672+ | Multi-language apps |
| [CCDB API](http://ccdb.hemiola.com/) | Chinese | 20,902 | Stroke count lookups |

## Quick Start

**Web App (5 minutes)**:
```javascript
import HanziWriter from 'hanzi-writer';
const writer = HanziWriter.create('div-id', '你', {
  width: 100, height: 100
});
writer.animateCharacter();
```

**Stroke Count Lookup**:
- API: `http://ccdb.hemiola.com/characters/unicode/{codepoint}`
- Python: `pip install cjklib`
- Database: [ChineseStrokes](https://github.com/caiguanhao/ChineseStrokes) (81,000 characters)

## Licensing Quick Check

| Resource | License | Commercial OK? |
|----------|---------|----------------|
| Hanzi Writer | MIT | ✅ Yes |
| KanjiVG | CC BY-SA 3.0 | ✅ Yes (with attribution) |
| Make Me a Hanzi | Mixed | ⚠️ Check repo |
| animCJK | Open-source | ⚠️ Verify license |
| cjklib | LGPL | ✅ Yes |

## Next Steps

1. **For web apps**: Start with Hanzi Writer (easiest integration)
2. **For custom needs**: Use Make Me a Hanzi or KanjiVG SVGs directly
3. **For stroke counts**: CCDB API or cjklib
4. **For deep dive**: See S2-comprehensive for full catalog

## Key Files Location

- **S2-comprehensive/**: Full catalog of all data sources
- **S3-need-driven/**: Implementation guides and use cases
- **S4-strategic/**: Implementation roadmap and metrics
