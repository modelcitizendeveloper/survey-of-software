# LTP - Comprehensive Assessment

## Language Technology Platform Overview

### Core Architecture
From [LTP documentation](https://aclanthology.org/C10-3004/):
- Integrated Chinese NLP platform
- Developed by HIT (Harbin Institute of Technology)
- Research Center for Social Computing and Information Retrieval

### Neural Architecture: N-LTP
[ArXiv paper](https://arxiv.org/abs/2009.11616) describes modern version:
- Multi-task learning framework
- Shared pretrained models
- Unified approach across tasks
- More efficient than independent models

## Six Core Tasks

**Lexical Analysis:**
1. Chinese word segmentation (分词)
2. Part-of-speech tagging (词性标注)
3. Named entity recognition (命名实体识别)

**Syntactic Parsing:**
4. Dependency parsing (依存句法分析)

**Semantic Parsing:**
5. Semantic dependency parsing (语义依存分析)
6. Semantic role labeling (语义角色标注)

## Terminology: "Lexical" not "Morphological"

**Important distinction:**
- LTP documentation uses "lexical analysis" (词法分析)
- NOT "morphological analysis" in linguistic sense
- Refers to word-level token analysis
- Includes segmentation, POS, NER

### Why "Lexical"?
- Chinese word segmentation is primary challenge
- Identifying word boundaries from character stream
- POS tagging and NER follow segmentation
- Focus on lexicon (words) not morphemes (sub-word units)

## Character Decomposition

**None** - LTP operates at word level. No character structure analysis, IDS support, or radical extraction.

## Compound Word Analysis

**Word segmentation, not morpheme decomposition:**
- Segments text into words
- Tags each word's part of speech
- Identifies named entities
- Does NOT decompose compounds into constituent morphemes

### Example Processing
Input: "中国人民大学"
- LTP might segment as: ["中国", "人民", "大学"] or ["中国人民大学"]
- Tags: [NOUN, NOUN, NOUN] or [ORG]
- Does NOT decompose: "人民" = "人" (person) + "民" (people)

## Production Readiness

**High:**
- ✅ Python 3 support: [GitHub](https://github.com/HIT-SCIR/ltp)
- ✅ pip installable
- ✅ Cloud service: [LTP-Cloud](https://www.ltp-cloud.com/intro_en)
- ✅ Academic backing (HIT)
- ✅ N-LTP modernization (2020+)
- ✅ Active Chinese NLP community

## Comparison with HanLP

**Similar scope, different implementations:**
- Both provide Chinese NLP pipelines
- Both include segmentation, POS, NER, parsing
- LTP: Chinese-specific, HIT research
- HanLP: Multilingual, broader language support
- Both operate at word level, not character level

## Integration with Character Analysis

**Preprocessing pipeline:**
1. LTP segments and tags text
2. Provides linguistic context
3. Separate tool needed for character decomposition
4. LTP output useful for identifying important words to analyze

### Workflow
1. LTP segments: "学习汉字需要耐心"
2. Output: ["学习"/VERB, "汉字"/NOUN, "需要"/VERB, "耐心"/NOUN]
3. Focus on nouns/verbs for character analysis
4. Use cjklib/makemeahanzi for "汉字" decomposition

## Verdict for Our Needs

**Word segmentation: Yes (excellent)**
**Lexical tagging: Yes (comprehensive)**
**Character decomposition: No**
**Morpheme analysis: No**

LTP is a production-ready Chinese NLP platform for word-level processing. Like HanLP and Stanza, it doesn't provide character structure analysis. The term "morphological analysis" in our requirements doesn't align with what LTP offers unless we interpret it as "word segmentation."

## Clarification Needed

The project requirements mention:
- Character decomposition ✓ (clearly sub-character components)
- Compound word analysis ? (ambiguous)

If "compound word analysis" means:
- **Identifying compounds from simple words:** LTP does this (word segmentation)
- **Decomposing compounds into morphemes:** LTP does NOT do this
- **Analyzing character structure:** LTP does NOT do this

---

Sources:
- [LTP Paper (ACL Anthology)](https://aclanthology.org/C10-3004/)
- [N-LTP ArXiv Paper](https://arxiv.org/abs/2009.11616)
- [LTP GitHub](https://github.com/HIT-SCIR/ltp)
- [LTP-Cloud Service](https://www.ltp-cloud.com/intro_en)
