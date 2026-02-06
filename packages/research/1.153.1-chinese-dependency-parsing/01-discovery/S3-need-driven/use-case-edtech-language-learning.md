# Use Case: Educational Technology for Chinese Language Learning

## Who Needs This

**User Persona**: Product managers and engineers at language learning platforms building Chinese grammar checking, writing assistance, and interactive exercises.

**Organization Context**:
- EdTech companies (Duolingo, Rosetta Stone, ChinesePod)
- University language learning labs
- Corporate training platforms (Chinese for business)
- Grammar checking tools (Chinese Grammarly equivalent)

**Technical Background**:
- Software engineers (web/mobile apps)
- Educational technologists (pedagogical design)
- Some ML experience (not NLP experts)

**Scale**: Serving thousands to millions of learners, processing millions of sentences per month

## Why They Need Dependency Parsing

### Primary Goals

**Grammar Error Detection**:
- Identify syntactic errors in learner writing
- Example: "我很喜欢吃的中国菜" (incorrect 的 placement) → flag structural error
- Provide corrections with explanations ("的 should follow 中国, not 吃")

**Sentence Pattern Practice**:
- Generate exercises based on syntactic structures
- Example: Teach "把" (ba) construction → identify sentences using this pattern
- Scaffold learning (simple SVO → complex topic-comment structures)

**Difficulty Estimation**:
- Assess sentence complexity for leveled content
- Metrics: Average dependency distance, tree depth, non-projective arcs
- Match content to learner proficiency (HSK levels, ACTFL guidelines)

**Intelligent Feedback**:
- Explain why a sentence is incorrect (not just "wrong")
- Show syntactic structure visually (dependency tree diagrams)
- Compare learner output to correct patterns

### Success Criteria

- **Pedagogical value**: Learners improve faster (pre/post testing)
- **Engagement**: Features used frequently (not ignored)
- **Accuracy**: Grammar checks correct (few false positives)
- **Explainability**: Feedback understandable to beginners
- **Cost-effective**: Reasonable compute costs at scale

## Requirements and Constraints

### Technical Requirements

**Must-have**:
- High accuracy (false positives frustrate learners)
- Explainable output (learners need to understand errors)
- Handling learner errors (robust to non-native syntax)
- Real-time feedback (interactive writing assistance)

**Nice-to-have**:
- Visual tree rendering (show dependency structure)
- Pedagogical annotations (HSK level tagging)
- Integration with learning management systems (LMS)

### Resource Constraints

**Compute**:
- Cloud-based (AWS, GCP) or edge (mobile apps)
- Cost-sensitive (educational margins, not enterprise)
- Latency-critical (interactive feedback)

**Budget**:
- Open-source required (per-API costs prohibitive for EdTech)
- Minimal infrastructure (small team, limited budget)

**Skills**:
- Generalist engineers (not NLP specialists)
- Pedagogical experts (understand language teaching)
- Need simple tools (don't want to become parsing experts)

## Library Recommendation

### Primary Choice: **Stanza (with UD treebanks including CFL)**

**Why Stanza**:

1. **UD Chinese-CFL treebank**: Trained on learner errors
   - UD_Chinese-CFL = Chinese as Foreign Language corpus
   - Annotated learner essays (500+ sentences)
   - Captures common learner mistakes (word order, particle misuse)
   - Better at handling non-native syntax than news-trained models

2. **Explainable UD output**: Pedagogically valuable
   - CoNLL-U format human-readable (learners can see fields)
   - Universal dependencies terminology (nsubj, obj) teachable
   - Visualizations available (UD Annotatrix, dependency tree libraries)

3. **Clean API**: Easy integration for generalist engineers
   - Python (accessible to web/mobile backend teams)
   - 10 lines of code (minimal learning curve)
   - JSON output (easy to render in web UIs)

4. **Multilingual consistency**: Future-proof
   - Start with Chinese, expand to Japanese, Korean, etc.
   - Same API (code reuse across languages)
   - Same pedagogical framework (UD relations teach grammar concepts)

**Implementation Pattern**:

```
Learner writes Chinese sentence in web/mobile app
 ↓
Backend API (Python + Stanza)
 ├─ Parse with Stanza (use UD_Chinese-CFL model if available)
 ├─ Check for errors:
 │   - Compare to reference patterns (rule-based grammar checks)
 │   - Detect unusual dependencies (low-probability arcs)
 │   - Identify omissions (required dependents missing)
 ├─ Generate feedback:
 │   - Highlight erroneous words/phrases
 │   - Explain syntactic role ("的 is misplaced - should modify noun, not verb")
 │   - Suggest corrections (rewrite with correct structure)
 ├─ Render tree (optional):
 │   - Visualize dependency structure (arrows showing dependencies)
 │   - Color-code by error (red = incorrect, green = correct)
 ↓
Display feedback to learner with explanations
```

**Pedagogical Integration**:
- Lesson planning: Generate exercises from parsed corpus (extract SVO sentences for beginners)
- Progress tracking: Measure learner improvement (dependency accuracy over time)
- Adaptive learning: Adjust difficulty based on parsing success (complex structures → higher level)

### Alternative: **HanLP (for semantic feedback)**

**When to choose HanLP instead**:

**Semantic error detection**:
- Detect meaning errors, not just syntactic
- Example: "我听音乐在图书馆" (I listen to music at library) → syntactically valid, but "在" should mark location of listening, not separate clause
- Semantic dependencies capture Chinese-specific patterns better

**Chinese-specific constructions**:
- Topic-comment structures (common in Chinese, tricky for learners)
- Serial verb constructions
- Resultative complements

**Advanced learners**:
- Intermediate/advanced levels (HSK 4-6)
- Need nuanced feedback beyond basic word order

**Trade-offs**:
- Heavier models (500MB-2GB vs Stanza 300MB)
- More complex output (semantic DAG harder to explain than syntactic tree)
- Prefer GPU (slower on CPU, cost/latency concerns)

### Why Not LTP

**Reasons to avoid**:

1. **Chinese-only**: Limits platform growth
   - Cannot expand to Japanese, Korean, French, etc.
   - Need to rebuild for each new language (different tools)
   - Code duplication, maintenance burden

2. **MTL overhead**: Don't need all six tasks
   - Only need parsing for grammar checking
   - Paying compute cost for segmentation, NER, SRL (unused)
   - Stanza single-task more efficient

3. **Documentation**: Primarily Chinese
   - Team may not read Chinese fluently
   - Harder to troubleshoot, customize

**Exception**: If building Chinese-only platform with no expansion plans (rare).

### Why Not CoreNLP

**Reasons to avoid**:
- Pre-neural (lower accuracy on learner errors)
- No learner corpus (UD-CFL) support
- Java (Python dominates EdTech stacks)
- Slow (frustrates learners with delayed feedback)

## Risk Factors and Mitigations

### Risk: False Positives Frustrate Learners

**Problem**: Parser incorrectly flags correct sentences as errors.
- Learner loses confidence ("My teacher said this is right, but app says wrong")
- Platform reputation damage (reviews: "app is wrong")

**Mitigation**:
- High precision threshold (only flag high-confidence errors)
- Human review (QA team validates grammar rules)
- User feedback loop ("Was this helpful?" → refine rules)
- Graceful degradation (if uncertain, show "unusual pattern" not "error")

### Risk: Explanations Too Technical

**Problem**: UD terminology confuses beginners.
- "nsubj" and "obl" mean nothing to HSK 2 learner
- Learners want simple explanations ("subject", "where/when")

**Mitigation**:
- Simplify terminology mapping:
  - nsubj → "subject (who/what does the action)"
  - obj → "object (receives the action)"
  - obl → "where/when/how"
- Visualize with colors/arrows (less jargon)
- Progressive disclosure (beginners see simple feedback, advanced see UD details)

### Risk: Learner Errors Break Parser

**Problem**: Severely incorrect sentences fail to parse.
- Example: "我喜欢吃的的的中国菜" (triple 的) → parser crashes or outputs garbage
- No feedback provided → learner stuck

**Mitigation**:
- Robust parsing (handle malformed input gracefully)
- Partial parsing (parse valid fragments, ignore broken parts)
- Rule-based fallback (if parser fails, use simple pattern matching)
- Error message ("This sentence is too unusual to analyze. Try simplifying.")

### Risk: UD-CFL Treebank Too Small

**Problem**: UD_Chinese-CFL has only ~500 sentences.
- Insufficient training data for all learner error types
- May not cover intermediate/advanced learners

**Mitigation**:
- Combine with UD_Chinese-GSD (larger corpus, less learner-specific)
- Fine-tune on platform's own learner corpus (collect + annotate user sentences)
- Hybrid approach (UD parsing + rule-based error patterns)
- Community annotation (crowdsource error patterns from teachers)

## Expected Outcomes

**Timeline**: 3-6 months for MVP, 12+ months for mature product
- Month 1-2: Prototype (Stanza + basic grammar rules on sample sentences)
- Month 3-4: Integration (add to web/mobile app, test with beta users)
- Month 5-6: MVP launch (simple grammar checking, sentence pattern practice)
- Month 7-12: Expansion (difficulty estimation, visual tree rendering, adaptive exercises)

**Deliverables**:
- Grammar checking (real-time feedback on learner writing)
- Sentence pattern library (exercises organized by syntactic structure)
- Difficulty estimator (match content to learner level)
- Progress dashboard (track learner improvement via dependency accuracy)

**Pedagogical Impact**:
- Faster learner progress (immediate feedback accelerates learning)
- Reduced teacher workload (automated grammar checking)
- Personalized learning (adaptive difficulty based on parsing success)
- Engagement (interactive syntax visualization keeps learners motivated)

**Cost Estimate**:
- Development: 1-2 engineers × 3-6 months (MVP)
- Infrastructure: $100-500/month (modest traffic, CPU-based)
- Ongoing: 0.5 engineer (content creation, QA, updates)

## Expected Errors and Handling

### Common Learner Errors

1. **Incorrect 的 placement**: "我喜欢吃的中国菜" → Should be "我喜欢吃中国的菜"
   - Detection: Check dependency of 的 (should modify noun, not verb)
   - Feedback: "的 connects to the wrong word - it should describe 菜 (dish), not 吃 (eat)"

2. **Missing 了**: "我昨天去北京" → Should be "我昨天去了北京"
   - Detection: Past time + verb without aspect marker
   - Feedback: "Past tense needs 了 after the verb"

3. **Word order**: "我很喜欢吃在餐厅" → Should be "我很喜欢在餐厅吃"
   - Detection: Location phrase (在X) should precede verb
   - Feedback: "In Chinese, 'where' comes before 'action'"

4. **量词 (measure word) errors**: "三本书" vs "三册书"
   - Detection: Requires semantic knowledge (book → 本/册, animal → 只, person → 个)
   - Limitation: Dependency parsing alone insufficient (need lexical knowledge)

## Summary

**For EdTech language learning platforms, Stanza is the recommended choice** due to UD-CFL learner corpus support, explainable output, and multilingual future-proofing. HanLP is an alternative for semantic feedback at advanced levels. LTP and CoreNLP don't fit EdTech constraints well (Chinese-only / pre-neural respectively).

**Key success factors**:
- Use UD-CFL model (handles learner errors better)
- Simplify terminology (map UD relations to pedagogical concepts)
- High precision (avoid false positives that frustrate learners)
- Visual feedback (show trees, color-code errors)
- Hybrid approach (parsing + rules + lexical knowledge)
