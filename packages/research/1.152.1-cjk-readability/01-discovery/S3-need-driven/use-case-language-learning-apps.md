# Use Case: Language Learning Applications

## Scenario Description
Applications that teach Chinese/Japanese/Korean dynamically adjust content difficulty to match learner proficiency, ensuring materials are challenging but not overwhelming.

## User Persona
- **Primary**: Language learning app developers (Duolingo, HelloChinese, ChinesePod)
- **Secondary**: Adaptive learning platform builders
- **Platforms**: Mobile apps, web apps, spaced repetition systems
- **Scale**: Millions of users across proficiency levels (A1 → C2, HSK 1 → 6)

## Examples of Real Applications
- **Duolingo**: Lessons scaled to learner progress, introducing new characters gradually
- **HelloChinese**: Content graded by HSK level with difficulty indicators
- **ChinesePod**: Podcast lessons tagged by proficiency level (Newbie → Advanced)
- **LingQ/Readlang**: Reading materials with unknown word highlighting
- **Clozemaster**: Sentence difficulty based on vocabulary frequency

## Technical Requirements

### Core Capabilities
1. **Character frequency analysis**: Identify rare characters that exceed learner level
2. **HSK/TOCFL mapping**: Classify words into standardized proficiency levels
3. **Coverage calculation**: % of text the learner can understand
4. **Unknown word detection**: Flag vocabulary outside learner's current level
5. **Difficulty scoring**: Assign numeric readability scores (1-10, beginner-advanced)
6. **Batch processing**: Analyze lesson libraries (thousands of texts)

### Performance Constraints
- **Latency**: Sub-second for individual lessons (real-time preview)
- **Throughput**: Process thousands of lessons during content ingestion
- **Memory**: Efficient on mobile devices (vocabulary databases can be large)
- **Offline capability**: Prefer local processing for mobile apps

### Accuracy Requirements
- **Critical**: Correct HSK/TOCFL level assignment (misleveling frustrates learners)
- **Important**: Character frequency accuracy (identifies difficulty spikes)
- **Nice-to-have**: Context-aware proper name filtering (names shouldn't count as "rare")

## Library Analysis

### hanziDB / CC-CEDICT with HSK Tags
**Strengths for Learning Apps**:
- ✅ **HSK level tagging** (1-6 classification for ~5000 words)
- ✅ **Comprehensive vocabulary** (100k+ entries)
- ✅ **Offline-capable** (bundled dictionary data)
- ✅ **Open data** (no licensing restrictions)

**Weaknesses for Learning Apps**:
- ⚠️ HSK coverage incomplete (many common words lack tags)
- ⚠️ No character-level frequency data
- ⚠️ Static data (doesn't learn from user interactions)

**Verdict**: **Good foundation but needs supplementation**.

### Jun Da Character Frequency Lists
**Strengths for Learning Apps**:
- ✅ **Character frequency rankings** (8000+ characters from corpus analysis)
- ✅ **Research-backed** (based on real text corpora)
- ✅ **Granular differentiation** (top 500 vs top 3000 vs rare)

**Weaknesses for Learning Apps**:
- ❌ Character-only (no word-level frequency)
- ❌ No HSK mapping
- ❌ Requires separate word segmentation

**Verdict**: **Essential for character-level analysis but incomplete alone**.

### Modern Chinese Character Frequency List (BCC Corpus)
**Strengths for Learning Apps**:
- ✅ **Massive corpus** (10 billion characters from 2000-2020 texts)
- ✅ **Contemporary relevance** (includes internet language)
- ✅ **High accuracy** (large sample size reduces noise)

**Weaknesses for Learning Apps**:
- ❌ Character-only (no word data)
- ❌ No proficiency level mapping
- ❌ Requires preprocessing

**Verdict**: **Best character frequency source, needs integration layer**.

### jieba with Custom Dictionaries
**Strengths for Learning Apps**:
- ✅ **Word segmentation** (essential for word-level analysis)
- ✅ **Custom dictionaries** (add HSK tags, frequency data)
- ✅ **Fast processing** (C++ implementation)
- ✅ **Widely used** (battle-tested in production)

**Weaknesses for Learning Apps**:
- ⚠️ Segmentation errors on domain-specific text
- ⚠️ No built-in readability features (need custom logic)

**Verdict**: **Critical infrastructure component, not a complete solution**.

## Detailed Feature Comparison

| Feature | hanziDB+HSK | Jun Da | BCC Corpus | jieba | Learning Value |
|---------|-------------|--------|------------|-------|----------------|
| **HSK levels** | ✅ | ❌ | ❌ | ⚠️ Custom | Critical (curriculum alignment) |
| **Character frequency** | ❌ | ✅ | ✅ | ❌ | High (difficulty signals) |
| **Word frequency** | ❌ | ❌ | ❌ | ⚠️ Custom | High (readability core metric) |
| **Word segmentation** | ❌ | ❌ | ❌ | ✅ | Critical (prerequisite) |
| **Coverage calculation** | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual | High (comprehension predictor) |
| **Offline-capable** | ✅ | ✅ | ✅ | ✅ | High (mobile apps) |

## Recommendation

### Multi-Library Integration Required
**No single library provides complete readability assessment.** Best practice combines:

1. **jieba**: Word segmentation (prerequisite for all analysis)
2. **BCC Character Frequency** or **Jun Da**: Character-level difficulty
3. **CC-CEDICT + HSK tags**: Word-level proficiency mapping
4. **Custom logic**: Coverage calculation, scoring algorithms

### Implementation Stack
```python
# Pseudocode showing integration pattern
import jieba
from collections import Counter

# 1. Segment text into words
words = jieba.cut(text)

# 2. Look up each word's HSK level
hsk_levels = [hsk_dict.get(word, 'unknown') for word in words]

# 3. Calculate coverage at learner's level
learner_level = 3  # HSK 3
known_words = sum(1 for level in hsk_levels if level <= learner_level)
coverage = known_words / len(words)

# 4. Character frequency analysis
chars = list(text)
rare_chars = [c for c in chars if char_frequency[c] > 3000]  # Beyond top 3000

# 5. Difficulty score
difficulty = calculate_difficulty(coverage, rare_chars, unique_chars)
```

## Implementation Patterns

### Pattern 1: Adaptive Content Selection
Select lesson content matching learner's proficiency:

```python
def select_lesson_for_learner(lessons, learner_hsk_level):
    """Find lessons with 90-95% vocabulary coverage"""
    suitable = []

    for lesson in lessons:
        words = segment(lesson.text)
        known_count = sum(1 for w in words if word_hsk_level(w) <= learner_hsk_level)
        coverage = known_count / len(words)

        if 0.90 <= coverage <= 0.95:  # Sweet spot for learning
            suitable.append(lesson)

    return suitable
```

### Pattern 2: Difficulty Preview
Show learners what % of content they'll understand:

```python
def preview_difficulty(text, learner_vocab):
    """Calculate comprehension metrics before learner starts"""
    words = segment(text)

    known_words = set(words) & learner_vocab
    unknown_words = set(words) - learner_vocab

    return {
        'coverage': len(known_words) / len(set(words)),
        'total_words': len(words),
        'unique_words': len(set(words)),
        'new_words_to_learn': list(unknown_words)[:10],  # Show first 10
        'difficulty_rating': classify_difficulty(coverage),
    }
```

### Pattern 3: Progressive Difficulty Curve
Ensure lesson sequence increases difficulty gradually:

```python
def validate_curriculum_progression(lessons):
    """Check that difficulty increases smoothly"""
    difficulties = [calculate_difficulty(lesson.text) for lesson in lessons]

    # Flag large jumps
    for i in range(1, len(difficulties)):
        jump = difficulties[i] - difficulties[i-1]
        if jump > 1.5:  # More than 1.5 levels jump
            print(f"Warning: Large difficulty spike at lesson {i}")

    # Ensure progression
    if difficulties != sorted(difficulties):
        print("Warning: Lessons not in difficulty order")
```

### Pattern 4: Unknown Word Highlighting
Visual feedback on which vocabulary is new:

```python
def annotate_unknown_words(text, learner_vocab):
    """Mark unknown words for learner attention"""
    words = segment(text)

    annotated = []
    for word in words:
        if word in learner_vocab:
            annotated.append({'word': word, 'status': 'known'})
        else:
            level = word_hsk_level(word)
            annotated.append({
                'word': word,
                'status': 'unknown',
                'hsk_level': level,
                'frequency_rank': word_frequency_rank(word),
            })

    return annotated
```

### Pattern 5: Spaced Repetition Integration
Track which difficult words learner has mastered:

```python
class VocabularyTracker:
    def __init__(self, learner_id):
        self.learner_vocab = load_known_words(learner_id)
        self.learned_words = load_learning_history(learner_id)

    def update_after_lesson(self, lesson_text):
        """Update learner's vocabulary after completing lesson"""
        words = segment(lesson_text)
        new_words = set(words) - self.learner_vocab

        # Add to learning queue for spaced repetition
        for word in new_words:
            self.learned_words.add(word, difficulty=word_hsk_level(word))

        # Promote words to known after N successful reviews
        mastered = self.learned_words.get_mastered()
        self.learner_vocab.update(mastered)
```

## Trade-offs

### Multi-Library Integration Benefits
- **Comprehensive analysis**: Character + word + proficiency levels
- **Curriculum alignment**: HSK/TOCFL mapping for standardized programs
- **Accurate difficulty scoring**: Multiple signals reduce false positives

### Multi-Library Integration Costs
- **Complexity**: Must maintain multiple data sources
- **Data sync**: HSK standards update periodically (2012 → 2021 revision)
- **Segmentation errors**: jieba mistakes propagate through pipeline
- **Memory footprint**: Large dictionaries for offline mobile apps

### When Complexity is Worth It
Use full integration for learning apps when:
- Adaptive content selection is core feature
- Target audience: serious learners (not casual tourists)
- Large content library needs automated grading
- Curriculum must align with standardized tests (HSK, TOCFL)

### When Simpler is Better
Consider lighter approaches if:
- Only need rough difficulty tiers (easy/medium/hard)
- Small, manually curated content library
- Target is single proficiency level (no adaptation needed)
- Memory/size severely constrained (offline mobile)

## Missing Capabilities

No existing library provides:
- ❌ **Context-aware proper name filtering** (names shouldn't count as rare)
- ❌ **Domain-specific vocabulary** (business Chinese, medical Chinese)
- ❌ **Grammar complexity metrics** (sentence structure, not just vocab)
- ❌ **Learner corpus** (actual learner comprehension data for validation)
- ❌ **CEFR mapping** (HSK ≠ CEFR, no standard conversion)

These require custom development or additional data sources.

## Real-World Integration Examples

### Duolingo-Style Adaptive Lessons
```python
def generate_lesson_variants(base_text, learner_level):
    """Create easier/harder versions of same lesson"""
    words = segment(base_text)

    # Easier: Replace rare words with common synonyms
    easy_text = replace_rare_words(words, max_hsk=learner_level - 1)

    # Harder: Keep original text
    hard_text = base_text

    return {
        'review': easy_text,      # Below learner level (reinforcement)
        'lesson': base_text,       # At learner level (learning)
        'challenge': hard_text,    # Above learner level (stretch)
    }
```

### Content Recommendation Engine
```python
def recommend_next_content(learner_id, content_library):
    """Find content at learner's current level + 1"""
    learner_vocab = get_learner_vocabulary(learner_id)
    current_level = estimate_learner_level(learner_vocab)

    # Find content with 85-90% coverage (optimal challenge)
    recommendations = []
    for content in content_library:
        coverage = calculate_coverage(content.text, learner_vocab)
        if 0.85 <= coverage <= 0.90:
            recommendations.append({
                'content': content,
                'coverage': coverage,
                'new_words': count_unknown_words(content.text, learner_vocab),
            })

    # Prioritize content with high-value new vocabulary
    return sorted(recommendations, key=lambda x: vocabulary_value(x))
```

### Progress Tracking Dashboard
```python
def learner_progress_report(learner_id):
    """Show learner's vocabulary growth over time"""
    history = get_learning_history(learner_id)

    return {
        'current_hsk_level': estimate_hsk_level(learner_id),
        'vocabulary_size': len(get_learner_vocabulary(learner_id)),
        'character_coverage': character_coverage_percentage(learner_id),
        'words_learned_this_week': count_new_words(history, days=7),
        'recommended_next_level': calculate_next_milestone(learner_id),
    }
```

## Performance Considerations

### Typical Workload
A learning app might process:
- 100-500 words per lesson
- 10-50 lessons in content library preview
- Real-time difficulty calculation on content creation

### Optimization Strategies
```python
# Pre-compute difficulty for entire library
content_library_cache = {
    lesson.id: {
        'difficulty_score': calculate_difficulty(lesson.text),
        'hsk_level': estimate_hsk_level_of_text(lesson.text),
        'character_coverage_by_level': {1: 0.3, 2: 0.5, 3: 0.7, ...},
    }
    for lesson in content_library
}

# Fast lookup for learner recommendations
def recommend_fast(learner_hsk_level):
    return [
        lesson for lesson in content_library
        if lesson.hsk_level == learner_hsk_level
    ]
```

## Conclusion

**Language learning apps require multi-library integration.** No single library provides complete readability assessment for CJK text. Best practice combines:

1. **jieba** for segmentation
2. **BCC/Jun Da** for character frequency
3. **CC-CEDICT + HSK tags** for word-level proficiency
4. **Custom scoring logic** for coverage and difficulty calculation

The complexity is justified when adaptive content selection and curriculum alignment are core features. For simpler apps with static content tiers, manual classification may suffice.
