# Use Case: Graded Reader Publishers

## Scenario Description
Publishers create and categorize books, articles, and reading materials by difficulty level, ensuring learners can find content matching their proficiency without frustration.

## User Persona
- **Primary**: Educational publishers (Mandarin Companion, Chinese Breeze, Sinolingua)
- **Secondary**: Content platforms (The Chairman's Bao, Du Chinese, Decipher Chinese)
- **Output**: Graded readers, leveled articles, children's books
- **Scale**: Catalogs of 100-1000+ books/articles needing consistent leveling

## Examples of Real Applications
- **Mandarin Companion**: Graded readers leveled 1-2 (breakthrough → elementary)
- **Chinese Breeze**: 8 levels (300 → 3000 character vocabulary)
- **The Chairman's Bao**: Daily news articles graded by HSK level
- **Du Chinese**: Stories leveled from HSK 1 → HSK 6
- **Decipher Chinese**: Chapters marked by character frequency coverage

## Technical Requirements

### Core Capabilities
1. **Automated level assignment**: Classify texts into difficulty tiers (HSK 1-6, CEFR A1-C2)
2. **Vocabulary coverage analysis**: Ensure text uses only characters/words at target level
3. **Difficulty validation**: Verify author hasn't accidentally used advanced vocabulary
4. **Comparative analysis**: Rank books within same level (easier HSK 3 vs harder HSK 3)
5. **Batch processing**: Analyze entire book catalog for consistency
6. **Vocabulary extraction**: Generate word lists for each book (appendix material)

### Performance Constraints
- **Batch processing**: Analyze 50k-100k word manuscripts
- **Latency**: Minutes acceptable (editorial workflow, not real-time)
- **Accuracy**: High priority (mislabeled books hurt learner trust)
- **Reporting**: Detailed breakdowns for editors (which chapters are too hard?)

### Accuracy Requirements
- **Critical**: No advanced vocabulary in beginner texts (breaks learner flow)
- **Critical**: Consistent leveling across book series
- **Important**: Character frequency accuracy (rare characters stand out)
- **Nice-to-have**: Sentence complexity metrics (long sentences = harder)

## Library Analysis

### CC-CEDICT + HSK Word Lists
**Strengths for Publishers**:
- ✅ **HSK 1-6 tagging** (~5000 words with level assignments)
- ✅ **Standardized levels** (aligns with learner expectations)
- ✅ **Comprehensive coverage** (100k+ dictionary entries)
- ✅ **Batch-friendly** (process entire manuscripts)

**Weaknesses for Publishers**:
- ⚠️ HSK 2012 vs 2021 standard differences (vocabulary lists changed)
- ⚠️ Incomplete coverage (many common words lack HSK tags)
- ⚠️ No proper name filtering (character names counted as rare)

**Verdict**: **Essential foundation but needs editorial oversight**.

### BCC Character Frequency List
**Strengths for Publishers**:
- ✅ **10 billion character corpus** (authoritative frequency data)
- ✅ **Fine-grained rankings** (differentiate top 500 vs top 1500)
- ✅ **Contemporary relevance** (2000-2020 text sources)

**Weaknesses for Publishers**:
- ❌ Character-only (books need word-level analysis)
- ❌ No proficiency mapping (frequency ≠ HSK level)

**Verdict**: **Excellent for character difficulty, insufficient alone**.

### SUBTLEX-CH (Word Frequency from Subtitles)
**Strengths for Publishers**:
- ✅ **Word frequency data** (from 46 million subtitle words)
- ✅ **Spoken language focus** (matches conversational content)
- ✅ **Psycholinguistic validity** (frequency correlates with familiarity)

**Weaknesses for Publishers**:
- ⚠️ Subtitle corpus bias (informal language overrepresented)
- ⚠️ No HSK mapping
- ⚠️ Not ideal for literary/formal texts

**Verdict**: **Useful for conversational readers, less so for classical texts**.

### jieba + Custom Dictionaries
**Strengths for Publishers**:
- ✅ **Word segmentation** (essential for word-level analysis)
- ✅ **Custom dictionaries** (add HSK tags, proper names)
- ✅ **Fast batch processing** (analyze full books in seconds)

**Weaknesses for Publishers**:
- ⚠️ Segmentation errors on literary text (classical Chinese, idioms)
- ⚠️ No built-in leveling (requires custom logic)

**Verdict**: **Critical infrastructure, needs integration layer**.

## Detailed Feature Comparison

| Feature | CC-CEDICT+HSK | BCC Freq | SUBTLEX-CH | jieba | Publisher Value |
|---------|---------------|----------|------------|-------|-----------------|
| **HSK levels** | ✅ | ❌ | ❌ | ⚠️ Custom | Critical (reader expectations) |
| **Character frequency** | ❌ | ✅ | ⚠️ Partial | ❌ | High (difficulty signals) |
| **Word frequency** | ❌ | ❌ | ✅ | ⚠️ Custom | High (vocabulary difficulty) |
| **Batch processing** | ✅ | ✅ | ✅ | ✅ | Critical (catalog analysis) |
| **Proper name handling** | ❌ | ❌ | ❌ | ⚠️ Custom | Important (avoid false positives) |
| **Coverage reports** | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | Critical (editorial feedback) |

## Recommendation

### Multi-Source Integration for Publishers
**Publishing workflow requires combining multiple data sources:**

1. **jieba**: Segment manuscripts into words
2. **CC-CEDICT + HSK**: Map words to proficiency levels
3. **BCC Character Frequency**: Identify rare characters
4. **Custom proper name dictionary**: Filter character/place names
5. **Editorial rules engine**: Custom vocabulary limits per level

### Publishing Workflow Integration
```python
# Pseudocode for manuscript grading
import jieba
from collections import Counter

def grade_manuscript(text, target_level='HSK3'):
    """Analyze manuscript for difficulty and vocabulary compliance"""

    # 1. Segment into words
    words = list(jieba.cut(text))

    # 2. Look up HSK levels
    word_levels = {word: hsk_dict.get(word, 'unknown') for word in set(words)}

    # 3. Find vocabulary violations (words above target level)
    violations = [
        word for word, level in word_levels.items()
        if level > target_level or level == 'unknown'
    ]

    # 4. Calculate character coverage
    chars = [c for c in text if is_cjk(c)]
    rare_chars = [c for c in chars if char_frequency_rank(c) > 3000]

    # 5. Generate editorial report
    return {
        'recommended_level': estimate_level(word_levels, rare_chars),
        'target_level': target_level,
        'compliant': len(violations) == 0,
        'violations': violations[:20],  # Show first 20
        'vocabulary_distribution': Counter(word_levels.values()),
        'character_coverage_at_target': calculate_coverage(chars, target_level),
        'editorial_notes': generate_suggestions(violations),
    }
```

## Implementation Patterns

### Pattern 1: Manuscript Compliance Check
Validate that book uses only target-level vocabulary:

```python
def validate_vocabulary_compliance(manuscript, target_hsk_level):
    """Check if manuscript stays within vocabulary constraints"""
    words = segment(manuscript)
    violations = []

    for word in set(words):
        word_level = get_hsk_level(word)

        if word_level > target_hsk_level:
            occurrences = words.count(word)
            violations.append({
                'word': word,
                'level': word_level,
                'occurrences': occurrences,
                'suggested_alternatives': find_simpler_synonyms(word, target_hsk_level),
            })

    return {
        'compliant': len(violations) == 0,
        'violations': sorted(violations, key=lambda x: x['occurrences'], reverse=True),
        'compliance_rate': (len(set(words)) - len(violations)) / len(set(words)),
    }
```

### Pattern 2: Catalog Consistency Validation
Ensure books labeled same level have similar difficulty:

```python
def validate_catalog_consistency(books_by_level):
    """Check that books within same level have comparable difficulty"""

    for level, books in books_by_level.items():
        difficulties = [calculate_difficulty_score(book.text) for book in books]
        mean_diff = statistics.mean(difficulties)
        std_dev = statistics.stdev(difficulties)

        # Flag outliers
        for book, difficulty in zip(books, difficulties):
            if abs(difficulty - mean_diff) > 2 * std_dev:
                print(f"WARNING: {book.title} at level {level} is outlier")
                print(f"  Difficulty: {difficulty:.2f} (mean: {mean_diff:.2f})")
                suggest_relevel(book, difficulty)
```

### Pattern 3: Chapter-by-Chapter Difficulty Curve
Ensure book difficulty increases gradually:

```python
def analyze_chapter_progression(chapters):
    """Validate that book maintains consistent difficulty"""
    chapter_difficulties = []

    for i, chapter in enumerate(chapters):
        difficulty = calculate_difficulty_score(chapter.text)
        new_vocabulary = count_new_words_since_chapter(chapter, chapters[:i])

        chapter_difficulties.append({
            'chapter': i + 1,
            'difficulty_score': difficulty,
            'new_vocabulary_count': new_vocabulary,
        })

        # Flag sudden jumps
        if i > 0:
            prev_difficulty = chapter_difficulties[i-1]['difficulty_score']
            jump = difficulty - prev_difficulty

            if jump > 1.0:  # Difficulty spike
                print(f"WARNING: Chapter {i+1} has difficulty spike (+{jump:.2f})")

    return chapter_difficulties
```

### Pattern 4: Vocabulary Appendix Generation
Auto-generate word lists for book appendices:

```python
def generate_vocabulary_appendix(manuscript, target_level):
    """Create word list for back-of-book appendix"""
    words = segment(manuscript)
    word_freq = Counter(words)

    # Categorize vocabulary
    appendix = {
        'target_level_words': [],
        'review_words': [],  # Below target level
        'challenge_words': [],  # Above target level
    }

    for word, freq in word_freq.items():
        level = get_hsk_level(word)
        entry = {
            'word': word,
            'pinyin': get_pinyin(word),
            'definition': get_definition(word),
            'frequency_in_text': freq,
        }

        if level == target_level:
            appendix['target_level_words'].append(entry)
        elif level < target_level:
            appendix['review_words'].append(entry)
        else:
            appendix['challenge_words'].append(entry)

    # Sort by frequency
    for category in appendix.values():
        category.sort(key=lambda x: x['frequency_in_text'], reverse=True)

    return appendix
```

### Pattern 5: Comparative Difficulty Ranking
Rank books within same level from easiest to hardest:

```python
def rank_books_within_level(books, level):
    """Order books by difficulty for reader recommendations"""
    scored_books = []

    for book in books:
        if book.target_level != level:
            continue

        # Multiple difficulty signals
        score = {
            'character_coverage': character_coverage_at_level(book.text, level),
            'unique_char_count': count_unique_characters(book.text),
            'avg_sentence_length': average_sentence_length(book.text),
            'rare_word_ratio': count_rare_words(book.text, level) / count_words(book.text),
        }

        # Weighted composite score
        composite = (
            score['character_coverage'] * 0.4 +
            (1 - score['rare_word_ratio']) * 0.3 +
            (3000 - score['unique_char_count']) / 3000 * 0.2 +
            (30 - score['avg_sentence_length']) / 30 * 0.1
        )

        scored_books.append({
            'book': book,
            'composite_score': composite,
            'breakdown': score,
        })

    # Return from easiest to hardest
    return sorted(scored_books, key=lambda x: x['composite_score'], reverse=True)
```

## Trade-offs

### Automated Grading Benefits
- **Consistency**: Objective metrics reduce subjective leveling errors
- **Scale**: Analyze hundreds of books quickly
- **Quality assurance**: Catch vocabulary violations before publication
- **Competitive analysis**: Benchmark against other publishers

### Automated Grading Costs
- **False positives**: Proper names flagged as rare (need manual filtering)
- **Context blindness**: Algorithms miss stylistic difficulty (prose quality)
- **HSK evolution**: Vocabulary standards change (2012 → 2021 revision)
- **Genre differences**: News articles ≠ fiction ≠ textbooks (different vocab)

### When Automation is Worth It
Use automated grading when:
- Large catalog requiring consistent leveling (50+ books)
- Series with strict vocabulary control (graded readers)
- Multiple authors need alignment (editorial coordination)
- Competitive positioning requires precise differentiation

### When Manual is Better
Rely on editorial judgment when:
- Small catalog (under 20 books)
- Literary quality more important than strict leveling
- Genre-specific vocabulary (business, medicine) not in HSK
- Pioneering new content types (no benchmarks)

## Missing Capabilities

No existing tool provides:
- ❌ **Proper name dictionaries** (character/place names for filtering)
- ❌ **Genre-specific vocabulary** (literary vs conversational vs academic)
- ❌ **Sentence complexity metrics** (grammar difficulty, not just vocab)
- ❌ **Readability formulas** (CJK equivalent of Flesch-Kincaid)
- ❌ **Comparative benchmarking** (how does this compare to competitors?)
- ❌ **HSK 2021 migration tools** (map old levels to new standard)

Publishers must build custom solutions for these needs.

## Real-World Integration Examples

### Editorial Dashboard
```python
class ManuscriptGrader:
    def __init__(self, target_level):
        self.target_level = target_level
        self.hsk_vocab = load_hsk_vocabulary(target_level)
        self.char_freq = load_character_frequency()

    def grade_and_report(self, manuscript):
        """Generate comprehensive grading report for editors"""
        words = segment(manuscript)
        chars = extract_cjk_characters(manuscript)

        report = {
            'summary': {
                'target_level': self.target_level,
                'recommended_level': self.estimate_level(words, chars),
                'compliant': self.check_compliance(words),
                'word_count': len(words),
                'unique_words': len(set(words)),
            },
            'vocabulary_analysis': self.analyze_vocabulary(words),
            'character_analysis': self.analyze_characters(chars),
            'violations': self.find_violations(words),
            'suggestions': self.generate_suggestions(words),
            'appendix_preview': self.generate_vocabulary_list(words)[:50],
        }

        return report
```

### Catalog Management System
```python
def update_catalog_leveling(catalog):
    """Re-grade entire catalog for consistency"""
    graded_catalog = []

    for book in catalog:
        auto_level = estimate_level_from_text(book.text)
        manual_level = book.assigned_level

        if auto_level != manual_level:
            print(f"MISMATCH: {book.title}")
            print(f"  Manual: {manual_level}, Auto: {auto_level}")
            review_needed = True
        else:
            review_needed = False

        graded_catalog.append({
            'book': book,
            'auto_level': auto_level,
            'manual_level': manual_level,
            'review_needed': review_needed,
            'difficulty_score': calculate_difficulty_score(book.text),
        })

    return graded_catalog
```

### Quality Assurance Pipeline
```python
def pre_publication_qa(manuscript, target_level):
    """Final check before printing"""
    issues = []

    # Check 1: Vocabulary compliance
    vocab_check = validate_vocabulary_compliance(manuscript, target_level)
    if not vocab_check['compliant']:
        issues.append({
            'type': 'vocabulary_violation',
            'severity': 'high',
            'details': vocab_check['violations'],
        })

    # Check 2: Rare character check
    rare_chars = find_rare_characters(manuscript, max_rank=3000)
    if len(rare_chars) > 10:
        issues.append({
            'type': 'rare_characters',
            'severity': 'medium',
            'details': rare_chars,
        })

    # Check 3: Consistency with series
    if series_books:
        consistency = check_series_consistency(manuscript, series_books)
        if consistency['outlier']:
            issues.append({
                'type': 'series_inconsistency',
                'severity': 'medium',
                'details': consistency,
            })

    return {
        'ready_for_publication': len(issues) == 0,
        'issues': issues,
    }
```

## Performance Considerations

### Typical Workload
Publishers process:
- 50k-100k word manuscripts (full books)
- Batch analysis of 100-500 books (catalog updates)
- Chapter-by-chapter review (editorial workflow)

### Optimization Strategies
```python
# Cache character frequency lookups
char_freq_cache = load_character_frequency()  # Load once

# Parallel processing for catalog
from multiprocessing import Pool
with Pool() as pool:
    graded_books = pool.map(grade_book, book_catalog)

# Incremental chapter analysis (don't reprocess whole book)
def analyze_chapter_incremental(new_chapter, previous_chapters_vocab):
    new_words = set(segment(new_chapter)) - previous_chapters_vocab
    return analyze_vocabulary(new_words)
```

## Conclusion

**Publishers need multi-library integration with editorial oversight.** Automated grading provides:
- Consistency across large catalogs
- Objective vocabulary compliance checking
- Quality assurance before publication

However, algorithms cannot replace editorial judgment on:
- Literary quality and prose style
- Genre-appropriate vocabulary
- Proper name handling
- Reader engagement factors

Best practice: Use automation for QA and consistency, rely on editors for final leveling decisions.
