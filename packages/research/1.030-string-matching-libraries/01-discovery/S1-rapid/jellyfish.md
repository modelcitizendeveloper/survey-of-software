# Jellyfish

**Repository:** github.com/jamesturk/jellyfish
**GitHub Stars:** 2,200
**Forks:** 162
**Last Updated:** 2025 (active)
**License:** MIT

## Quick Assessment

- **Popularity:** Moderate-High (2.2k stars)
- **Maintenance:** Active (591 commits, ongoing development)
- **Documentation:** Good (available at jpt.sh/projects/jellyfish/)
- **Production Adoption:** Moderate (specialized use cases)

## Pros

- **Phonetic matching**: Soundex, Metaphone, NYSIIS, Match Rating
- **Approximate matching**: Levenshtein, Jaro-Winkler distances
- **Specialized algorithms**: Unique phonetic encoders not in other libraries
- **MIT license**: Permissive for commercial use
- **Pure purpose-built**: Focused specifically on string comparison

## Cons

- **Performance**: Slower than RapidFuzz (recent benchmarks show struggles with long text)
- **Limited scope**: Phonetic matching less needed for exact/fuzzy use cases
- **Smaller ecosystem**: Less community support than RapidFuzz
- **Memory concerns**: Higher memory use with long strings

## Quick Take

Jellyfish excels at phonetic matching (finding "Smith" when user types "Smyth"). Best for name matching, spell-checking, and search applications where pronunciation similarity matters. For pure fuzzy matching, RapidFuzz is faster. Use Jellyfish when you specifically need phonetic algorithms like Soundex or Metaphone.

## Data Sources

- [GitHub - jamesturk/jellyfish](https://github.com/jamesturk/jellyfish)
- [Python Jellyfish for Enhanced String Matching | Medium](https://medium.com/wetheitguys/python-jellyfish-for-enhanced-string-matching-6fe18ee32c8b)
- [A Comparative Analysis of Python Text Matching Libraries](https://ijeedu.com/index.php/ijeedu/article/view/188)
