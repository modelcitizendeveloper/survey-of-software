# S1-Rapid: Recommendation

## Quick Decision Matrix

### For Most Projects: **Stanza**
- Clean Python API, no Java dependency
- Stanford-backed reliability
- 80+ languages including Chinese
- UD-compliant output standard
- Active maintenance

**When to choose**: New Python projects, multilingual pipelines, academic research, migrating from CoreNLP

### For Chinese-Specific Needs: **HanLP or LTP**

**HanLP** if you need:
- Semantic dependency parsing (not just syntactic)
- Multiple NLP tasks beyond parsing (sentiment, classification)
- Multilingual capability (130+ languages)
- Modern ML pipeline integration

**LTP** if you need:
- Chinese-only focus with optimizations
- Multi-task learning efficiency
- Semantic role labeling
- Academic research on Chinese linguistics

### For Legacy Systems: **CoreNLP**
- Only if maintaining existing Java infrastructure
- Otherwise migrate to Stanza (Stanford's recommended path)

### Not a Parser: **Universal Dependencies**
- UD is the format and training data, not a tool
- All modern parsers (Stanza, HanLP, LTP) use UD treebanks
- Check UD treebank coverage for your domain needs

## 5-Minute Decision Tree

```
Do you need multilingual support?
├─ Yes → Stanza (80+ languages) or HanLP (130+ languages)
└─ No (Chinese-only) → Continue

Do you need semantic dependencies (not just syntactic)?
├─ Yes → HanLP or LTP
└─ No → Continue

Do you have existing Java infrastructure?
├─ Yes → CoreNLP acceptable, but consider Stanza
└─ No → Stanza (most balanced choice)

Do you need maximum Chinese-specific optimization?
├─ Yes → LTP (HIT research) or HanLP
└─ No → Stanza (Stanford research)
```

## Key Trade-offs

| Criterion | Stanza | HanLP | LTP | CoreNLP |
|-----------|--------|-------|-----|---------|
| **Ease of use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Chinese optimization** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Multilingual** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| **Documentation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Modern architecture** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Community size** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

## Next Steps

1. **Quick prototyping**: Install Stanza, test on your data
2. **Chinese-specific needs**: Compare HanLP and LTP on sample texts
3. **Production planning**: Review S2 for performance benchmarks
4. **Use case validation**: Check S3 for scenario-specific recommendations
5. **Strategic decisions**: Read S4 before committing to architecture

## What This Recommendation Doesn't Cover

- Detailed performance benchmarks (→ S2-comprehensive)
- Domain-specific accuracy (→ S2 + S3)
- Long-term maintenance considerations (→ S4)
- Custom model training requirements (→ S2 + S4)
- Production deployment patterns (→ S3)

## Confidence Level

**70-80% confidence** - S1 rapid assessment balances speed with directional accuracy. Validate with hands-on testing before production commitment.
