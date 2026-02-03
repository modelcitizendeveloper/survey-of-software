# S1: Surface Scan - CJK Readability Analysis

## What This Is

CJK readability analysis evaluates Chinese text difficulty based on character frequency and proficiency level standards (HSK for mainland China, TOCFL for Taiwan). It answers: "What proficiency level does a learner need to read this text?"

## The Core Problem

Unlike alphabetic languages where ~26 letters form all words, Chinese uses thousands of characters. A learner with 500 characters can't read text requiring 2,000 characters. Readability analysis maps text to standardized proficiency levels so learners know if material matches their skill.

## Key Standards

### HSK (Hanyu Shuiping Kaoshi)
- **Old system**: 6 levels (HSK 1-6)
- **New system (2026)**: 9 levels, effective July 2026
- Character requirements:
  - HSK 1: ~300 characters
  - HSK 6: ~2,500 characters
  - HSK 9: 3,000+ characters (academic/professional)
- Most common 1,000 characters cover ~90% of everyday written Chinese
- 2,500 characters cover ~98% of common texts

### TOCFL (Test of Chinese as a Foreign Language - Taiwan)
- 8 levels: Novice 1-2, Levels 1-6
- Organized in 4 bands (Novice, A, B, C)
- Band A: 500-1,000 characters (240-720 learning hours)
- Uses TBCL (Taiwan Benchmarks for the Chinese Language): 3,100 characters, 14,425 words
- Focuses on vocabulary words (ci) rather than character counts

## Existing Tools

### Web-Based
- **Chinese Text Analyser** (chinesetextanalyser.com): Fast segmentation/analysis
- **HSK HSK Analyzer** (hskhsk.com/analyse): HSK level breakdown per text
- **Chinese Text Analyzer** (chine-culture.com): Junda frequency list analysis

### Academic/Research
- **CRIE (Chinese Readability Index Explorer)**: 82 multilevel linguistic features
- **CkipTagger** (Sinica-Taiwan): POS tagging and tokenization

### Libraries
- **cntext** (Python): Word frequency, readability, sentiment analysis
- **Jieba**: Word segmentation (used by many tools)
- **chinese-text-analyzer** (GitHub): HSK breakdown with Jieba

## Key Insights

1. **Character vs word**: Some systems use character counts, others word counts (ci)
2. **Frequency lists**: Junda, HSK official lists, TOCFL/TBCL lists
3. **Coverage metrics**: "90% coverage at HSK 3" = learner knows 90% of characters
4. **Segmentation required**: Chinese text has no spaces; must tokenize before analysis

## Sources
- [The Newly Revised HSK | What You Need to Know in 2026](https://studycli.org/hsk/the-new-hsk/)
- [Everything You Need to Know About the 2026 HSK Overhaul](https://www.hanyuace.com/blog/everything-about-2026-hsk-overhaul)
- [HSK character list](http://hanzidb.org/character-list/hsk)
- [Hanyu Shuiping Kaoshi - Wikipedia](https://en.wikipedia.org/wiki/Hanyu_Shuiping_Kaoshi)
- [Test of Chinese as a Foreign Language - Wikipedia](https://en.wikipedia.org/wiki/Test_of_Chinese_as_a_Foreign_Language)
- [Understanding TOCFL: The Test of Chinese as a Foreign Language](https://cmn-hant.overseas.ncnu.edu.tw/en/further-study-area/summary-of-indonesia/understanding-tocfl-the-test-of-chinese-as-a-foreign-language/)
- [Chinese Text Analyser](https://www.chinesetextanalyser.com/)
- [CRIE: An automated analyzer for Chinese texts](https://link.springer.com/article/10.3758/s13428-015-0649-1)
- [Analyse Your 汉字 Vocabulary/Text](https://hskhsk.com/analyse)
- [cntext · PyPI](https://pypi.org/project/cntext/)
