# S1-Rapid: Recommendation

## Summary

After rapid evaluation of available tools for Classical Chinese parsing:

| Library | Parsing Capability | Classical Chinese Support | Ease of Use |
|---------|-------------------|---------------------------|-------------|
| Stanford CoreNLP | ✓✓✓ Strong (modern) | ✗ Limited | ✓✓ Moderate |
| ctext.org API | ✗ Minimal | ✓✓✓ Native | ✓✓✓ Easy |

## Key Findings

1. **No ready-made solution**: There is no production-ready parsing toolkit specifically designed for Classical Chinese
2. **Modern vs Classical gap**: Tools trained on modern Chinese (Stanford CoreNLP) struggle with Classical Chinese grammar
3. **Corpus vs Parser distinction**: ctext.org provides excellent corpus access but no syntactic parsing

## Immediate Recommendation

**For corpus access and basic segmentation**: Use **ctext.org API**
- Best for text retrieval and research
- Native Classical Chinese support
- Easy integration via HTTP API

**For deeper parsing needs**: Requires custom solution
- Consider fine-tuning Stanford CoreNLP on Classical Chinese corpus
- Explore specialized academic tools (need S2 comprehensive search)
- May need to build domain-specific parser

## Next Steps for S2

1. **Search for academic tools**: Check if universities have specialized Classical Chinese parsers
2. **Investigate Chinese domestic tools**: Tools like Jiayan (嘉言) or other 文言文-specific libraries
3. **Explore transfer learning**: Can modern Chinese parsers be adapted?
4. **Consider rule-based approaches**: Classical Chinese grammar is well-documented; rule-based parsing might be viable

## Confidence Level

**Low** - Classical Chinese parsing appears to be an underserved niche. More comprehensive research needed.
