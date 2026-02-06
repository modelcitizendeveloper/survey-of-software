# Use Case: Curriculum Designers

## Scenario Description
Language program coordinators, university professors, and school administrators design multi-year learning progressions, ensuring materials sequence from beginner to advanced with appropriate difficulty increases.

## User Persona
- **Primary**: University Chinese program coordinators, K-12 curriculum developers
- **Secondary**: Corporate training program designers, online course architects
- **Output**: Multi-year curricula, semester lesson plans, course sequences
- **Constraints**: Must align with standards (HSK, TOCFL, ACTFL), budget limits

## Examples of Real Applications
- **University Chinese programs**: 4-year BA programs (Year 1 → Year 4 progression)
- **K-12 school districts**: Chinese immersion programs (Grade 1 → Grade 12)
- **Corporate training**: Business Chinese programs (3-month intensive courses)
- **MOOCs**: Coursera/edX Chinese courses (beginner → advanced tracks)
- **Language schools**: Summer intensive programs (8-week progressions)

## Technical Requirements

### Core Capabilities
1. **Material sequencing**: Order materials from easy → hard with smooth progression
2. **Vocabulary distribution analysis**: Ensure even vocabulary load across semesters
3. **Curriculum gap detection**: Find missing proficiency levels in material collection
4. **Textbook comparison**: Evaluate competing textbooks for level appropriateness
5. **Standards alignment**: Verify coverage of HSK/TOCFL/ACTFL requirements
6. **Resource allocation**: Plan budgets based on material difficulty needs

### Performance Constraints
- **Batch analysis**: Process hundreds of textbooks/materials (curriculum library)
- **Latency**: Hours acceptable (strategic planning, not real-time)
- **Reporting**: Detailed visualizations (gap analysis, progression curves)
- **Accuracy**: High priority (curriculum decisions are multi-year commitments)

### Accuracy Requirements
- **Critical**: Accurate level classification (wrong textbook = semester wasted)
- **Critical**: Vocabulary coverage validation (gaps leave students unprepared)
- **Important**: Competitive benchmarking (how do materials compare to other programs?)
- **Nice-to-have**: Cost-per-level optimization (budget allocation)

## Library Analysis

### CC-CEDICT + HSK Vocabulary Lists
**Strengths for Curriculum Design**:
- ✅ **HSK 1-6 tagging** (align materials with standardized progression)
- ✅ **Comprehensive coverage** (validate textbook completeness)
- ✅ **Batch processing** (analyze entire curriculum library)
- ✅ **Standards-based** (matches learner expectations)

**Weaknesses for Curriculum Design**:
- ⚠️ HSK 2012 vs 2021 differences (curriculum transitions needed)
- ⚠️ Incomplete coverage (materials with unique vocabulary hard to assess)
- ⚠️ No curriculum-specific metrics (materials may use same words but different teaching approach)

**Verdict**: **Essential foundation for standards alignment**.

### ACTFL Proficiency Guidelines + Can-Do Statements
**Strengths for Curriculum Design**:
- ✅ **Competency-based framework** (focus on what learners can do)
- ✅ **K-12 adoption** (US schools use ACTFL standards)
- ✅ **Skills-based** (speaking, reading, writing, listening)

**Weaknesses for Curriculum Design**:
- ❌ Not automated (no word lists, manual assessment)
- ❌ Qualitative not quantitative (hard to measure with tools)
- ⚠️ No direct HSK mapping (curriculum spans multiple frameworks)

**Verdict**: **Important for K-12, needs manual integration**.

### Corpus-Based Frequency Data (BCC, SUBTLEX-CH)
**Strengths for Curriculum Design**:
- ✅ **Empirical evidence** (real-world usage patterns)
- ✅ **Genre differentiation** (academic vs conversational vocabulary)
- ✅ **Contemporary relevance** (recent corpus data)

**Weaknesses for Curriculum Design**:
- ❌ No pedagogical sequencing (frequency ≠ learnability)
- ❌ Corpus bias (news ≠ learner needs)
- ⚠️ Requires interpretation (how to map frequency to curriculum levels?)

**Verdict**: **Useful reference but not curriculum design tool alone**.

### Textbook Metadata (Publishers' Level Claims)
**Strengths for Curriculum Design**:
- ✅ **Publisher specifications** (stated target levels)
- ✅ **Market positioning** (competitive benchmarking)
- ✅ **Pedagogical intent** (authors' design goals)

**Weaknesses for Curriculum Design**:
- ⚠️ Publisher claims unvalidated (marketing vs reality)
- ⚠️ Inconsistent leveling (different publishers use different scales)
- ⚠️ Lack of granularity (same level can vary widely)

**Verdict**: **Starting point but requires independent validation**.

## Detailed Feature Comparison

| Feature | CC-CEDICT+HSK | ACTFL | BCC Corpus | Textbook Metadata | Curriculum Value |
|---------|---------------|-------|------------|-------------------|------------------|
| **Standards alignment** | ✅ HSK | ✅ ACTFL | ❌ | ⚠️ Varies | Critical (accreditation) |
| **Batch analysis** | ✅ | ❌ Manual | ✅ | ⚠️ Manual | Critical (library evaluation) |
| **Vocabulary sequencing** | ⚠️ Levels only | ❌ | ⚠️ Frequency | ❌ | High (progression planning) |
| **Gap detection** | ⚠️ Manual | ❌ | ❌ | ❌ | High (curriculum holes) |
| **Competitive benchmarking** | ⚠️ Manual | ⚠️ Manual | ❌ | ✅ | Medium (market positioning) |
| **Cost optimization** | ❌ | ❌ | ❌ | ⚠️ Price data | Medium (budget planning) |

## Recommendation

### Multi-Phase Curriculum Design Process
**Curriculum design requires combining automated analysis with expert judgment:**

**Phase 1: Standards Mapping**
1. Use CC-CEDICT + HSK to map materials to standardized levels
2. Validate publisher claims through independent vocabulary analysis
3. Identify gaps in curriculum progression (missing HSK levels)

**Phase 2: Sequencing Analysis**
1. Use corpus frequency data to validate vocabulary introduction order
2. Ensure vocabulary load distributed evenly across semesters
3. Check for difficulty spikes between consecutive courses

**Phase 3: Competitive Benchmarking**
1. Compare program materials to peer institutions
2. Validate that progression matches industry standards
3. Identify unique strengths/weaknesses

**Phase 4: Expert Review**
1. Faculty validate automated recommendations
2. Adjust for pedagogical factors (teachability, cultural relevance)
3. Pilot materials with small cohorts before full adoption

### Curriculum Analysis Workflow
```python
# Pseudocode for curriculum analysis
class CurriculumAnalyzer:
    def __init__(self, materials_library):
        self.materials = materials_library
        self.hsk_vocab = load_hsk_vocabulary()
        self.corpus_freq = load_corpus_frequency()

    def analyze_curriculum_progression(self, course_sequence):
        """Validate multi-year course progression"""
        progression = []

        for i, course in enumerate(course_sequence):
            # Analyze course difficulty
            difficulty = self.estimate_difficulty(course.materials)

            # Check vocabulary coverage
            vocab_coverage = self.check_hsk_coverage(course.materials)

            # Detect gaps from previous course
            if i > 0:
                prev_vocab = set(get_vocabulary(course_sequence[i-1].materials))
                current_vocab = set(get_vocabulary(course.materials))
                new_vocab = current_vocab - prev_vocab
                overlap = current_vocab & prev_vocab

                progression.append({
                    'course': course.name,
                    'difficulty': difficulty,
                    'hsk_level': vocab_coverage['estimated_level'],
                    'new_vocabulary': len(new_vocab),
                    'vocabulary_overlap': len(overlap) / len(prev_vocab),
                    'difficulty_jump': difficulty - progression[i-1]['difficulty'],
                })

        return self.validate_progression(progression)

    def validate_progression(self, progression):
        """Check for curriculum issues"""
        issues = []

        for i, course in enumerate(progression):
            # Check for difficulty spikes
            if course['difficulty_jump'] > 1.5:
                issues.append({
                    'type': 'difficulty_spike',
                    'course': course['course'],
                    'severity': 'high',
                    'message': f"Large difficulty jump (+{course['difficulty_jump']:.2f}) from previous course",
                })

            # Check for vocabulary overload
            if course['new_vocabulary'] > 500:
                issues.append({
                    'type': 'vocabulary_overload',
                    'course': course['course'],
                    'severity': 'medium',
                    'message': f"{course['new_vocabulary']} new words (recommend <500 per semester)",
                })

            # Check for insufficient review
            if course['vocabulary_overlap'] < 0.4:  # Less than 40% overlap
                issues.append({
                    'type': 'insufficient_review',
                    'course': course['course'],
                    'severity': 'medium',
                    'message': f"Only {course['vocabulary_overlap']:.1%} vocabulary overlap with previous course",
                })

        return {
            'progression': progression,
            'issues': issues,
            'overall_assessment': 'needs_revision' if len(issues) > 0 else 'acceptable',
        }
```

## Implementation Patterns

### Pattern 1: Standards Alignment Validator
Ensure curriculum covers required HSK/TOCFL vocabulary:

```python
def validate_standards_coverage(curriculum_materials, target_standard='HSK'):
    """Check if curriculum covers all required vocabulary"""
    # Load standard vocabulary requirements
    if target_standard == 'HSK':
        required_vocab = {
            1: load_hsk_level(1),
            2: load_hsk_level(2),
            3: load_hsk_level(3),
            4: load_hsk_level(4),
            5: load_hsk_level(5),
            6: load_hsk_level(6),
        }

    # Extract curriculum vocabulary
    curriculum_vocab = set()
    for material in curriculum_materials:
        words = extract_vocabulary(material.text)
        curriculum_vocab.update(words)

    # Check coverage for each level
    coverage = {}
    for level, vocab_set in required_vocab.items():
        covered = curriculum_vocab & vocab_set
        coverage[level] = {
            'required': len(vocab_set),
            'covered': len(covered),
            'coverage_rate': len(covered) / len(vocab_set),
            'missing': list(vocab_set - covered)[:20],  # Show first 20 missing
        }

    return coverage
```

### Pattern 2: Gap Detection in Curriculum
Find missing proficiency levels:

```python
def detect_curriculum_gaps(materials_library):
    """Find missing difficulty levels in material collection"""
    # Classify all materials by difficulty
    classified = []
    for material in materials_library:
        difficulty = estimate_difficulty(material.text)
        classified.append({
            'material': material,
            'difficulty': difficulty,
            'estimated_hsk': map_difficulty_to_hsk(difficulty),
        })

    # Group by HSK level
    by_level = {}
    for item in classified:
        level = item['estimated_hsk']
        if level not in by_level:
            by_level[level] = []
        by_level[level].append(item['material'])

    # Detect gaps
    gaps = []
    for level in range(1, 7):  # HSK 1-6
        if level not in by_level or len(by_level[level]) < 3:
            gaps.append({
                'level': level,
                'available_materials': len(by_level.get(level, [])),
                'recommended_materials': 3,  # At least 3 per level
                'priority': 'high' if level <= 3 else 'medium',  # Lower levels more critical
            })

    return {
        'gaps': gaps,
        'distribution': {level: len(materials) for level, materials in by_level.items()},
        'recommendations': generate_acquisition_recommendations(gaps),
    }
```

### Pattern 3: Textbook Comparison for Adoption
Evaluate competing textbooks:

```python
def compare_textbooks(candidates, target_level, criteria):
    """Rank textbooks for curriculum adoption"""
    scored_books = []

    for book in candidates:
        analysis = analyze_textbook(book)

        # Score on multiple dimensions
        score = {
            'book': book,
            'level_accuracy': abs(analysis['estimated_level'] - target_level),  # Lower = better
            'vocabulary_coverage': check_hsk_coverage(book, target_level),
            'progression_quality': analyze_chapter_progression(book),
            'price_per_page': book.price / book.page_count,
            'publisher_reputation': get_publisher_score(book.publisher),
        }

        # Weighted composite score
        composite = (
            (1 - score['level_accuracy'] / 6) * 0.3 +  # 30% level match
            score['vocabulary_coverage'] * 0.3 +        # 30% vocab coverage
            score['progression_quality'] * 0.2 +        # 20% internal progression
            (1 - normalize(score['price_per_page'])) * 0.1 +  # 10% cost
            score['publisher_reputation'] * 0.1         # 10% reputation
        )

        score['composite_score'] = composite
        scored_books.append(score)

    # Rank by composite score
    return sorted(scored_books, key=lambda x: x['composite_score'], reverse=True)
```

### Pattern 4: Vocabulary Distribution Planner
Ensure even vocabulary load across semesters:

```python
def plan_vocabulary_distribution(years=4, semesters_per_year=2):
    """Plan vocabulary introduction across multi-year program"""
    total_semesters = years * semesters_per_year
    hsk_6_vocab = 5000  # HSK 6 target

    # Calculate vocabulary per semester (accounting for forgetting)
    vocab_per_semester = calculate_optimal_load(
        total_vocab=hsk_6_vocab,
        semesters=total_semesters,
        retention_rate=0.85,  # Assume 15% forgetting per semester
    )

    # Build progression plan
    plan = []
    cumulative_vocab = 0

    for year in range(1, years + 1):
        for semester in range(1, semesters_per_year + 1):
            # Vocabulary load increases gradually
            load_multiplier = 1 + (year - 1) * 0.2  # Year 4 = 60% more vocab than Year 1
            semester_load = int(vocab_per_semester * load_multiplier)

            cumulative_vocab += semester_load

            plan.append({
                'year': year,
                'semester': semester,
                'new_vocabulary': semester_load,
                'cumulative': cumulative_vocab,
                'target_hsk_level': map_vocab_to_hsk(cumulative_vocab),
                'weekly_load': semester_load / 15,  # 15-week semester
            })

    return plan
```

### Pattern 5: Competitive Benchmark Report
Compare program to peer institutions:

```python
def generate_benchmark_report(own_program, peer_programs):
    """Compare program materials to competitors"""
    # Analyze own program
    own_analysis = {
        'total_materials': len(own_program.materials),
        'hsk_coverage': analyze_hsk_coverage(own_program),
        'progression_quality': analyze_progression(own_program.course_sequence),
        'cost_per_student': calculate_program_cost(own_program),
    }

    # Analyze peers
    peer_analyses = [
        analyze_program(peer) for peer in peer_programs
    ]

    # Calculate percentiles
    benchmarks = {
        'materials_count': {
            'own': own_analysis['total_materials'],
            'peer_avg': statistics.mean([p['total_materials'] for p in peer_analyses]),
            'percentile': calculate_percentile(own_analysis['total_materials'], [p['total_materials'] for p in peer_analyses]),
        },
        'hsk_coverage': {
            'own': own_analysis['hsk_coverage'],
            'peer_avg': statistics.mean([p['hsk_coverage'] for p in peer_analyses]),
            'percentile': calculate_percentile(own_analysis['hsk_coverage'], [p['hsk_coverage'] for p in peer_analyses]),
        },
        'cost_per_student': {
            'own': own_analysis['cost_per_student'],
            'peer_avg': statistics.mean([p['cost_per_student'] for p in peer_analyses]),
            'percentile': calculate_percentile(own_analysis['cost_per_student'], [p['cost_per_student'] for p in peer_analyses], reverse=True),  # Lower cost = better
        },
    }

    return {
        'benchmarks': benchmarks,
        'competitive_position': assess_competitive_position(benchmarks),
        'recommendations': generate_recommendations(benchmarks),
    }
```

## Trade-offs

### Automated Curriculum Analysis Benefits
- **Objectivity**: Data-driven decisions reduce bias
- **Scale**: Analyze hundreds of materials efficiently
- **Standards alignment**: Validate compliance with HSK/TOCFL
- **Gap detection**: Identify missing levels before students suffer

### Automated Curriculum Analysis Costs
- **Context blindness**: Tools miss pedagogical quality, cultural relevance
- **Over-reliance on metrics**: Vocabulary coverage ≠ teaching effectiveness
- **Standards evolution**: HSK 2012 → 2021 requires recalibration
- **Faculty resistance**: Perception of automation replacing expert judgment

### When Automation is Worth It
Use automated analysis when:
- Large program (>100 students/year, multi-year curriculum)
- Standards-driven (HSK/TOCFL alignment required for accreditation)
- Textbook adoption decisions (objective comparison needed)
- Program review cycles (periodic validation of curriculum quality)

### When Manual Analysis is Better
Rely on faculty judgment when:
- Small programs (20-50 students, boutique courses)
- Experimental curricula (pioneering new approaches)
- Heritage learner programs (different needs than L2 learners)
- Highly specialized content (business Chinese, medical Chinese)

## Missing Capabilities

No existing tool provides:
- ❌ **ACTFL integration** (automated proficiency level mapping)
- ❌ **Pedagogical quality metrics** (teachability, engagement potential)
- ❌ **Cultural content analysis** (cultural relevance, diversity)
- ❌ **Skills-based assessment** (speaking/listening difficulty, not just reading)
- ❌ **Retention modeling** (predict vocabulary forgetting over semesters)
- ❌ **Cost optimization** (budget allocation for maximum curriculum quality)

Curriculum designers must combine automated tools with expert judgment.

## Real-World Integration Examples

### University Program Review Dashboard
```python
class ProgramReviewDashboard:
    def __init__(self, program_name, years=4):
        self.program = load_program(program_name)
        self.years = years

    def generate_annual_report(self):
        """Comprehensive program review"""
        return {
            'enrollment': self.get_enrollment_stats(),
            'standards_coverage': self.validate_hsk_coverage(),
            'progression_quality': self.analyze_course_progression(),
            'material_gaps': self.detect_curriculum_gaps(),
            'competitive_position': self.benchmark_against_peers(),
            'budget_analysis': self.analyze_material_costs(),
            'recommendations': self.generate_action_items(),
        }

    def generate_action_items(self):
        """Prioritized recommendations"""
        gaps = self.detect_curriculum_gaps()
        progression = self.analyze_course_progression()

        actions = []

        # Critical gaps
        for gap in gaps['gaps']:
            if gap['priority'] == 'high':
                actions.append({
                    'priority': 1,
                    'action': f"Acquire {gap['recommended_materials']} materials for HSK {gap['level']}",
                    'deadline': 'Next semester',
                })

        # Progression issues
        if progression['issues']:
            actions.append({
                'priority': 2,
                'action': 'Revise course sequence to fix difficulty spikes',
                'deadline': 'Next academic year',
            })

        return actions
}
```

### Textbook Adoption Committee Tool
```python
def textbook_adoption_analysis(candidates, committee_criteria):
    """Support faculty adoption decision"""
    # Analyze each candidate
    analyses = []
    for book in candidates:
        analysis = {
            'book': book.title,
            'publisher': book.publisher,
            'price': book.price,

            # Automated metrics
            'estimated_level': estimate_difficulty(book.text),
            'hsk_coverage': check_hsk_coverage(book),
            'progression_quality': analyze_chapter_progression(book),

            # Manual review scores (faculty input)
            'pedagogical_quality': None,  # Faculty scores 1-10
            'cultural_content': None,     # Faculty scores 1-10
            'exercises_quality': None,    # Faculty scores 1-10
        }

        analyses.append(analysis)

    # Generate committee report
    return {
        'candidates': analyses,
        'automated_ranking': rank_by_automated_metrics(analyses),
        'faculty_review_form': generate_review_form(analyses),
        'recommendation_template': generate_committee_recommendation(),
    }
```

### Multi-Year Curriculum Builder
```python
def build_curriculum(target_proficiency='HSK6', years=4):
    """Design multi-year curriculum from scratch"""
    # Calculate vocabulary targets per year
    vocab_plan = plan_vocabulary_distribution(years)

    # Find materials matching each year's target
    curriculum = {}
    for year in range(1, years + 1):
        year_plan = [p for p in vocab_plan if p['year'] == year]
        target_level = year_plan[0]['target_hsk_level']

        # Search material library
        suitable_materials = find_materials_for_level(target_level)

        curriculum[f'Year {year}'] = {
            'target_hsk_level': target_level,
            'vocabulary_goal': year_plan[-1]['cumulative'],
            'recommended_materials': suitable_materials[:3],  # Top 3
            'supplementary_resources': suggest_supplementary(target_level),
        }

    return {
        'curriculum': curriculum,
        'vocabulary_progression': vocab_plan,
        'total_cost': calculate_total_cost(curriculum),
        'implementation_timeline': generate_timeline(curriculum),
    }
```

## Performance Considerations

### Typical Workload
Curriculum designers analyze:
- Entire program libraries (100-500 textbooks/materials)
- Multi-year course sequences (4-10 courses)
- Competitor programs (5-20 peer institutions)

### Optimization Strategies
```python
# Cache material analyses (don't re-analyze every time)
material_cache = {}

def analyze_with_cache(material):
    if material.id in material_cache:
        return material_cache[material.id]

    analysis = analyze_material(material)
    material_cache[material.id] = analysis
    return analysis

# Parallel processing for large libraries
from multiprocessing import Pool

def analyze_library_parallel(materials):
    with Pool() as pool:
        results = pool.map(analyze_material, materials)
    return results
```

## Conclusion

**Curriculum design requires automated analysis plus expert judgment.** Tools provide:
- Objective standards alignment validation (HSK/TOCFL coverage)
- Gap detection (missing proficiency levels)
- Competitive benchmarking (compare to peer programs)
- Progression analysis (smooth difficulty increases)

However, automation cannot replace faculty expertise on:
- Pedagogical quality (teachability, engagement)
- Cultural relevance (appropriate content for learners)
- Program-specific needs (heritage learners, specialized domains)
- Budget vs quality trade-offs (institutional constraints)

**Best practice**: Use automation for QA and evidence gathering, rely on faculty for final curriculum decisions. Automated metrics inform but don't dictate.
