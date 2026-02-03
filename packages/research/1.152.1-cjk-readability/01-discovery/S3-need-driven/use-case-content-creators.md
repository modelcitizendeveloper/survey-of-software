# Use Case: Educational Content Creators

## Scenario Description
Textbook authors, curriculum developers, and educators create teaching materials while ensuring vocabulary and grammar match target proficiency levels and curriculum standards.

## User Persona
- **Primary**: Textbook authors, curriculum developers, language teachers
- **Secondary**: Online course creators, YouTube educators, educational bloggers
- **Output**: Textbooks, worksheets, lesson plans, video scripts, blog posts
- **Constraints**: Must align with standardized curricula (HSK, TOCFL, school syllabi)

## Examples of Real Applications
- **University textbook authors**: Creating HSK-aligned coursebooks
- **K-12 curriculum developers**: Designing age-appropriate Chinese lessons
- **YouTube educators**: Scripting comprehensible input videos
- **Blog writers**: Writing learner-friendly explanations of Chinese culture/grammar
- **Worksheet creators**: Generating practice materials at specific levels

## Technical Requirements

### Core Capabilities
1. **Real-time difficulty feedback**: Authors see difficulty as they write
2. **Vocabulary constraint validation**: Alert when using words above target level
3. **Suggested replacements**: Recommend simpler synonyms for complex words
4. **Coverage visualization**: Show what % of text learners can understand
5. **Curriculum alignment check**: Verify content matches HSK/TOCFL standards
6. **Export word lists**: Generate vocabulary lists for lesson appendices

### Performance Constraints
- **Real-time responsiveness**: Sub-second feedback while typing (Google Docs add-on)
- **Batch validation**: Analyze complete chapters (10k-50k words)
- **Lightweight**: Work in browser or lightweight desktop app
- **Offline capability**: Authors work without internet connection

### Accuracy Requirements
- **Critical**: Catch vocabulary above target level (breaks learner flow)
- **Important**: Suggest pedagogically appropriate alternatives
- **Nice-to-have**: Grammar complexity warnings (sentence structure)

## Library Analysis

### CC-CEDICT + HSK Vocabulary Lists
**Strengths for Content Creators**:
- ✅ **HSK 1-6 tagging** (align content with standards)
- ✅ **Comprehensive coverage** (100k+ words)
- ✅ **Synonym lookup** (find simpler alternatives)
- ✅ **Offline-capable** (author workflow often offline)

**Weaknesses for Content Creators**:
- ⚠️ HSK coverage gaps (common words lack tags)
- ⚠️ No real-time integration (need custom tooling)
- ⚠️ Synonym quality (not all alternatives pedagogically sound)

**Verdict**: **Essential reference, needs UI layer**.

### jieba + Custom Dictionaries
**Strengths for Content Creators**:
- ✅ **Fast word segmentation** (real-time feedback possible)
- ✅ **Custom dictionaries** (add HSK tags, proper names)
- ✅ **Lightweight** (runs in browser via WebAssembly)

**Weaknesses for Content Creators**:
- ⚠️ Segmentation errors (need manual correction)
- ⚠️ No built-in simplification suggestions

**Verdict**: **Critical for real-time analysis**.

### Pleco Dictionary (User Tooling Inspiration)
**Strengths for Content Creators**:
- ✅ **HSK tagging in dictionary** (shows word levels)
- ✅ **Synonym explorer** (find alternatives)
- ✅ **Example sentences** (pedagogical context)

**Weaknesses for Content Creators**:
- ❌ Manual lookup (not integrated into writing workflow)
- ❌ Mobile-only (authors work on desktop)

**Verdict**: **Excellent reference but not authoring tool**.

### BLCU HSK Vocabulary Graded Lists
**Strengths for Content Creators**:
- ✅ **Official HSK standard** (authoritative)
- ✅ **Both 2012 and 2021 versions** (cover transitions)
- ✅ **Part-of-speech tags** (syntactic guidance)

**Weaknesses for Content Creators**:
- ⚠️ Static lists (need lookup tool)
- ⚠️ No synonym suggestions

**Verdict**: **Authoritative reference for validation**.

## Detailed Feature Comparison

| Feature | CC-CEDICT+HSK | jieba | Pleco | BLCU Lists | Creator Value |
|---------|---------------|-------|-------|------------|---------------|
| **Real-time feedback** | ⚠️ Manual | ✅ | ❌ | ❌ | Critical (authoring flow) |
| **HSK tagging** | ✅ | ⚠️ Custom | ✅ | ✅ | Critical (curriculum align) |
| **Synonym suggestions** | ⚠️ Manual | ❌ | ✅ | ❌ | High (vocabulary control) |
| **Offline-capable** | ✅ | ✅ | ⚠️ Mobile | ✅ | Important (authoring workflow) |
| **Part-of-speech tags** | ✅ | ⚠️ Custom | ✅ | ✅ | Medium (grammar guidance) |
| **Integration-ready** | ⚠️ API | ✅ | ❌ | ⚠️ CSV | Critical (tooling) |

## Recommendation

### Custom Authoring Tool Required
**No off-the-shelf tool exists for real-time content creation.** Authors need custom integration:

1. **jieba**: Real-time word segmentation as author types
2. **CC-CEDICT + HSK lists**: Vocabulary level lookup
3. **Custom synonym engine**: Suggest simpler alternatives
4. **Browser extension or Google Docs add-on**: Inline feedback

### Authoring Tool Architecture
```python
# Pseudocode for real-time authoring assistant
import jieba

class ContentCreatorAssistant:
    def __init__(self, target_level='HSK3'):
        self.target_level = target_level
        self.hsk_vocab = load_hsk_vocabulary()
        self.synonyms = load_synonym_database()

    def analyze_as_you_type(self, text):
        """Real-time feedback while author writes"""
        words = jieba.cut(text)
        issues = []

        for word in words:
            word_level = self.hsk_vocab.get(word, 'unknown')

            if word_level > self.target_level:
                suggestions = self.find_simpler_alternatives(word)
                issues.append({
                    'word': word,
                    'level': word_level,
                    'severity': 'high' if word_level > self.target_level + 1 else 'medium',
                    'suggestions': suggestions,
                })

        return {
            'issues': issues,
            'difficulty_estimate': self.estimate_difficulty(words),
            'target_level_compliance': len(issues) == 0,
        }

    def find_simpler_alternatives(self, word):
        """Suggest simpler synonyms"""
        candidates = self.synonyms.get(word, [])
        return [
            syn for syn in candidates
            if self.hsk_vocab.get(syn, 99) <= self.target_level
        ]
```

## Implementation Patterns

### Pattern 1: Google Docs Add-On (Real-Time Highlighting)
Highlight vocabulary violations as author writes:

```javascript
// Google Apps Script for Docs add-on
function analyzeDocument() {
  var doc = DocumentApp.getActiveDocument();
  var body = doc.getBody();
  var text = body.getText();

  // Call backend API (jieba + HSK lookup)
  var issues = analyzeText(text, targetLevel='HSK3');

  // Highlight violations in yellow
  issues.forEach(function(issue) {
    var range = body.findText(issue.word);
    if (range) {
      range.getElement().asText().setBackgroundColor(
        issue.severity === 'high' ? '#FFFF00' : '#FFFFE0'
      );
    }
  });

  // Show sidebar with suggestions
  showSuggestionsSidebar(issues);
}
```

### Pattern 2: Browser Extension (Webpage Content Validation)
Validate content on educational blogs/websites:

```javascript
// Browser extension for content creators
chrome.action.onClicked.addListener(async (tab) => {
  // Extract text from current page
  const text = await extractTextFromPage(tab.id);

  // Analyze difficulty
  const analysis = await analyzeDifficulty(text, 'HSK4');

  // Show popup with results
  chrome.notifications.create({
    type: 'basic',
    title: 'Content Difficulty Analysis',
    message: `Level: ${analysis.level}\nCompliance: ${analysis.compliant ? 'Yes' : 'No'}\nViolations: ${analysis.violations.length}`,
  });

  // Highlight violations on page
  highlightViolations(tab.id, analysis.violations);
});
```

### Pattern 3: Vocabulary Constraint Checker
Validate entire manuscript before publication:

```python
def validate_manuscript_constraints(manuscript, target_level, allowed_exceptions):
    """Check if content meets vocabulary constraints"""
    words = segment(manuscript)
    violations = []

    # Check each word
    for word in set(words):
        # Skip allowed exceptions (proper names, technical terms)
        if word in allowed_exceptions:
            continue

        word_level = get_hsk_level(word)

        if word_level > target_level or word_level == 'unknown':
            occurrences = words.count(word)
            simpler_alternatives = find_simpler_synonyms(word, target_level)

            violations.append({
                'word': word,
                'level': word_level,
                'occurrences': occurrences,
                'suggested_replacements': simpler_alternatives,
                'example_sentences': find_sentences_with_word(manuscript, word)[:3],
            })

    # Generate report
    return {
        'compliant': len(violations) == 0,
        'total_violations': len(violations),
        'violations_by_severity': categorize_violations(violations),
        'detailed_violations': sorted(violations, key=lambda x: x['occurrences'], reverse=True),
        'recommended_action': 'fix' if len(violations) > 10 else 'review',
    }
```

### Pattern 4: Synonym Suggestion Engine
Help authors replace complex words with simpler alternatives:

```python
def suggest_replacements(word, target_level, context_sentence):
    """Find pedagogically appropriate synonyms"""
    # Look up synonyms from dictionary
    raw_synonyms = get_synonyms(word)

    # Filter to target level
    level_appropriate = [
        syn for syn in raw_synonyms
        if get_hsk_level(syn) <= target_level
    ]

    # Rank by pedagogical value
    ranked = []
    for syn in level_appropriate:
        score = {
            'synonym': syn,
            'level': get_hsk_level(syn),
            'frequency': get_word_frequency(syn),
            'context_fit': check_context_fit(syn, context_sentence),
            'pedagogical_value': calculate_pedagogical_value(syn, target_level),
        }
        ranked.append(score)

    # Sort by best fit
    ranked.sort(key=lambda x: x['pedagogical_value'], reverse=True)

    return ranked[:5]  # Top 5 suggestions
```

### Pattern 5: Lesson Vocabulary Planner
Plan vocabulary introduction across lesson sequence:

```python
def plan_lesson_vocabulary(lessons, starting_level='HSK1'):
    """Ensure gradual vocabulary progression across lessons"""
    cumulative_vocab = set()
    current_level = starting_level

    lesson_plan = []

    for lesson in lessons:
        words = segment(lesson.text)
        new_words = set(words) - cumulative_vocab

        # Calculate difficulty
        new_word_count = len(new_words)
        difficulty_jump = estimate_difficulty_increase(new_words, cumulative_vocab)

        # Flag if too many new words
        if new_word_count > 20:  # More than 20 new words = too much
            lesson_plan.append({
                'lesson': lesson.title,
                'status': 'warning',
                'issue': f'{new_word_count} new words (max 20 recommended)',
                'suggestions': ['Split into 2 lessons', 'Remove low-frequency words'],
            })
        elif difficulty_jump > 1.0:  # Difficulty spike
            lesson_plan.append({
                'lesson': lesson.title,
                'status': 'warning',
                'issue': f'Difficulty spike (+{difficulty_jump:.2f})',
                'suggestions': ['Add bridge lesson', 'Pre-teach difficult vocabulary'],
            })
        else:
            lesson_plan.append({
                'lesson': lesson.title,
                'status': 'ok',
                'new_words': list(new_words),
                'cumulative_vocab_size': len(cumulative_vocab) + len(new_words),
            })

        cumulative_vocab.update(new_words)

    return lesson_plan
```

## Trade-offs

### Real-Time Authoring Tools Benefits
- **Immediate feedback**: Authors fix issues while writing (not after)
- **Pedagogical guidance**: Suggests appropriate vocabulary choices
- **Quality assurance**: Prevents vocabulary violations before publication
- **Productivity**: Faster than manual dictionary lookups

### Real-Time Authoring Tools Costs
- **Development effort**: Custom tooling required (no off-the-shelf solutions)
- **False positives**: Proper names, technical terms flagged incorrectly
- **Synonym quality**: Not all replacements pedagogically equivalent
- **Author training**: Learning curve for new tool adoption

### When Custom Tooling is Worth It
Build authoring assistant when:
- High-volume content production (multiple textbooks/year)
- Strict curriculum alignment required (HSK, TOCFL)
- Multiple authors need consistency (editorial coordination)
- Competitive advantage in curriculum quality

### When Manual Validation Suffices
Rely on post-writing review when:
- Small-scale production (one-off worksheets)
- Expert authors with deep pedagogical knowledge
- Flexible curriculum (not tied to standardized tests)
- Budget constraints (custom tooling expensive)

## Missing Capabilities

No existing tool provides:
- ❌ **Integrated authoring environment** (Google Docs add-on, VS Code extension)
- ❌ **Grammar complexity metrics** (sentence structure difficulty)
- ❌ **Pedagogical synonym ranking** (not all synonyms equally teachable)
- ❌ **Lesson vocabulary planning** (progression across lesson series)
- ❌ **Age-appropriate vocabulary** (K-12 vs adult learners)
- ❌ **Cultural appropriateness** (Taiwan vs Mainland vocabulary)

Content creators must build custom solutions or rely on manual judgment.

## Real-World Integration Examples

### Textbook Author Workflow
```python
class TextbookAuthorAssistant:
    def __init__(self, book_series_name, target_level):
        self.series = book_series_name
        self.target_level = target_level
        self.cumulative_vocab = load_series_vocabulary(book_series_name)

    def validate_chapter_draft(self, chapter_text):
        """Provide feedback on chapter draft"""
        words = segment(chapter_text)

        # 1. Vocabulary compliance
        violations = find_vocabulary_violations(words, self.target_level)

        # 2. New vocabulary load
        new_words = set(words) - self.cumulative_vocab
        new_word_count = len(new_words)

        # 3. Coverage analysis
        coverage = calculate_coverage(words, self.target_level)

        # 4. Generate feedback
        feedback = {
            'ready_for_review': len(violations) == 0 and new_word_count <= 20,
            'issues': violations,
            'new_vocabulary': {
                'count': new_word_count,
                'words': list(new_words),
                'recommendation': 'ok' if new_word_count <= 20 else 'reduce',
            },
            'coverage': coverage,
            'suggested_edits': generate_edit_suggestions(violations),
        }

        return feedback

    def update_series_vocabulary(self, chapter_text):
        """Track cumulative vocabulary as series progresses"""
        words = set(segment(chapter_text))
        self.cumulative_vocab.update(words)
        save_series_vocabulary(self.series, self.cumulative_vocab)
```

### YouTube Educator Script Validator
```python
def validate_video_script(script, target_audience='HSK3'):
    """Check if video script matches target audience level"""
    # Segment into sentences
    sentences = split_into_sentences(script)

    sentence_analysis = []
    for sent in sentences:
        words = segment(sent)
        difficulty = estimate_difficulty(words)

        # Check if sentence appropriate
        if difficulty > target_audience + 1:  # More than 1 level above
            sentence_analysis.append({
                'sentence': sent,
                'difficulty': difficulty,
                'issue': 'too_hard',
                'suggestion': 'Simplify vocabulary or add explanation',
            })
        else:
            sentence_analysis.append({
                'sentence': sent,
                'difficulty': difficulty,
                'status': 'ok',
            })

    # Overall script assessment
    hard_sentences = [s for s in sentence_analysis if s.get('issue') == 'too_hard']

    return {
        'script_appropriate': len(hard_sentences) < len(sentences) * 0.1,  # < 10% hard
        'hard_sentence_count': len(hard_sentences),
        'recommendations': 'Ready for recording' if len(hard_sentences) == 0 else 'Simplify before recording',
        'detailed_analysis': sentence_analysis,
    }
```

### Worksheet Generator with Difficulty Control
```python
def generate_worksheet(vocabulary_list, target_level, exercise_type='fill_blank'):
    """Create practice worksheet at specific difficulty"""
    # Filter vocabulary to target level
    level_vocab = [
        word for word in vocabulary_list
        if get_hsk_level(word) == target_level
    ]

    # Generate exercises
    exercises = []
    for word in level_vocab[:20]:  # 20 questions
        if exercise_type == 'fill_blank':
            sentence = generate_example_sentence(word, target_level)
            blank_sentence = sentence.replace(word, '____')
            exercises.append({
                'question': blank_sentence,
                'answer': word,
                'pinyin_hint': get_pinyin(word),
            })

    # Validate worksheet difficulty
    validation = validate_worksheet_difficulty(exercises, target_level)

    return {
        'exercises': exercises,
        'difficulty_validated': validation['compliant'],
        'answer_key': [ex['answer'] for ex in exercises],
    }
```

## Performance Considerations

### Typical Workload
Content creators work with:
- Real-time typing (100-500 words/hour)
- Chapter drafts (3k-10k words)
- Full textbook manuscripts (50k-100k words)

### Optimization Strategies
```python
# Incremental analysis (only new text, not whole document)
class IncrementalAnalyzer:
    def __init__(self, target_level):
        self.target_level = target_level
        self.previous_text = ""
        self.cached_issues = []

    def analyze_changes(self, current_text):
        """Only analyze what changed since last call"""
        # Diff to find new text
        new_text = current_text[len(self.previous_text):]

        # Analyze only new portion
        new_issues = analyze_text(new_text, self.target_level)

        # Merge with cached issues
        all_issues = self.cached_issues + new_issues

        # Update cache
        self.previous_text = current_text
        self.cached_issues = all_issues

        return all_issues

# Debounce real-time analysis (don't analyze every keystroke)
import time

def debounced_analysis(text, target_level, delay=1.0):
    """Wait for user to stop typing before analyzing"""
    time.sleep(delay)
    return analyze_text(text, target_level)
```

## Conclusion

**Content creators need custom authoring tools with real-time feedback.** No off-the-shelf solution exists. Best approach:

1. **Build custom integration** (Google Docs add-on, browser extension)
2. **Combine libraries**: jieba (segmentation) + CC-CEDICT/HSK (tagging)
3. **Add synonym engine**: Help authors find simpler alternatives
4. **Validate post-writing**: Batch analysis before publication

Investment in tooling pays off for high-volume content production and multi-author coordination. Small-scale creators can rely on manual validation with reference materials (Pleco, HSK word lists).
