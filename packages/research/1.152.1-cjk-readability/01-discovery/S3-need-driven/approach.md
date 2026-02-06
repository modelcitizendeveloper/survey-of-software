# S3-Need-Driven Approach

## Objective
Analyze real-world use cases for CJK readability assessment. Move from "what can these libraries do" to "what problems do they solve" and "who needs them."

## Methodology
1. Identify 3-5 concrete application categories
2. For each use case, define:
   - The user persona and their goal
   - The specific technical requirements
   - Which library features are essential vs nice-to-have
   - Trade-offs specific to that use case
   - Library recommendation with rationale
3. Avoid abstract capabilities; focus on actual workflows

## Use Cases Selected

### 1. Language Learning Applications
**User**: App developers matching content difficulty to learner proficiency
**Example**: Duolingo, HelloChinese, ChinesePod grading lesson content

### 2. Graded Reader Publishers
**User**: Publishers categorizing books/articles by reading difficulty
**Example**: Mandarin Companion, The Chairman's Bao content leveling

### 3. Educational Content Creators
**User**: Textbook authors and educators validating material difficulty
**Example**: Teachers ensuring vocabulary matches curriculum standards (HSK, TOCFL)

### 4. Reading Assistant Tools
**User**: Developers building browser extensions and e-reader features
**Example**: Zhongwen popup dictionary showing character frequencies, difficulty warnings

### 5. Curriculum Designers
**User**: Language program coordinators planning lesson progression
**Example**: University programs sequencing materials from HSK 1 → HSK 6

## Analysis Framework

For each use case, address:

### Requirements
- What readability metrics are needed? (character frequency, word frequency, HSK/TOCFL levels)
- Is batch analysis or real-time assessment required?
- How important is accuracy vs speed?
- What granularity is needed? (character-level, word-level, document-level)
- Are there performance constraints? (mobile apps vs server processing)

### Library Fit
- Which library's strengths align with this use case?
- What features are critical vs optional?
- Are there missing capabilities?

### Implementation Considerations
- Typical code patterns for this use case
- Integration challenges
- Performance implications
- Edge cases to handle (proper names, specialized vocabulary, mixed scripts)

### Decision Factors
- Why one library over another?
- When would you need multiple libraries?
- When is a custom solution required?

## CJK Readability Dimensions

### Character Frequency
- **Jun Da frequency lists**: 8000+ characters ranked by corpus frequency
- **Modern Chinese Character Frequency List**: BCC corpus (10 billion characters)
- **Use**: Identify rare characters that signal difficulty

### Word-Level Proficiency Standards
- **HSK (Hanyu Shuiping Kaoshi)**: 6 levels, ~5000 words for HSK 6
- **TOCFL (Test of Chinese as a Foreign Language)**: Taiwan standard, 8000+ words
- **Use**: Map vocabulary to standardized learning curricula

### Readability Metrics
- **Character coverage**: % of text composed of high-frequency characters
- **Unknown word ratio**: % of words outside learner's level
- **Average word frequency**: Lower rank = harder text
- **Unique character count**: More unique characters = more cognitive load

## Success Criteria
- Clear guidance for developers choosing readability tools
- Realistic assessment of what each library enables
- Identification of gaps no library fills
- Practical code patterns for common scenarios
- Honest trade-off discussions (not just feature promotion)
