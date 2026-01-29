# S2-Comprehensive: Recommendation

## Executive Summary

After comprehensive analysis, **no single production-ready solution exists** for Classical Chinese parsing. The best approach depends on project requirements and resources.

## Tool Rankings

### For Segmentation Only
1. **Jiayan** (Best for Classical Chinese)
2. Stanford CoreNLP (Better for modern Chinese)
3. ctext.org API (Basic, but convenient)

### For Full NLP Pipeline
1. **Build custom solution** using Jiayan + custom components
2. Fine-tune Stanford CoreNLP on Classical Chinese corpus
3. Hybrid rule-based + ML approach

### For Corpus Access
1. **ctext.org API** (Unmatched Classical Chinese corpus)
2. Stanford CoreNLP training data (For modern Chinese reference)

## Recommended Approaches by Use Case

### Use Case 1: Research/Academic Project

**Minimal Viable Pipeline:**
```
1. Text source: ctext.org API
2. Segmentation: Jiayan
3. Analysis: Manual or rule-based
```

**Investment**: Low (2-4 weeks)
**Accuracy**: Moderate for segmentation, variable for analysis

### Use Case 2: Production Application

**Hybrid Pipeline:**
```
1. Text source: ctext.org API (corpus) + user input
2. Segmentation: Jiayan
3. POS tagging: Train custom model on annotated data
4. Parsing: Rule-based parser using Classical grammar rules
5. NER: Gazetteer + pattern matching for historical entities
```

**Investment**: High (6-12 months)
**Accuracy**: Good with proper training data

### Use Case 3: Modern + Classical Mixed

**Combined Pipeline:**
```
1. Language detection: Classify as modern vs classical
2. Modern Chinese: Stanford CoreNLP
3. Classical Chinese: Jiayan + custom rules
4. Post-processing: Merge results
```

**Investment**: Moderate (3-6 months)
**Accuracy**: Good for modern, moderate for classical

## Critical Gaps to Address

### 1. Annotated Training Data
**Problem**: No large-scale Classical Chinese treebank exists
**Solution Options**:
- Annotate subset of ctext.org corpus (high cost)
- Transfer learning from modern Chinese (moderate accuracy)
- Active learning approach (iterative improvement)

**Estimated effort**: 500-2000 hours of expert annotation

### 2. POS Tagset for Classical Chinese
**Problem**: Modern Chinese tagsets don't fit classical grammar
**Solution**: Design Classical Chinese tagset based on:
- Classical grammar references
- Linguistic literature on 文言文
- Consultation with classical philologists

**Estimated effort**: 2-3 months of linguistic research

### 3. Parsing Algorithm
**Problem**: Classical Chinese syntax differs from modern
**Solution Options**:
- **Rule-based**: Encode classical grammar rules (faster, lower accuracy ceiling)
- **Neural**: Train on annotated data (slower, higher accuracy potential)
- **Hybrid**: Rules for structure, ML for ambiguity resolution (balanced)

**Recommended**: Hybrid approach
**Estimated effort**: 6-9 months

## Phased Implementation Plan

### Phase 1: Foundation (Months 1-2)
- Set up Jiayan for segmentation
- Integrate ctext.org API for corpus access
- Build evaluation framework with manually annotated test set
- **Deliverable**: Basic segmentation pipeline

### Phase 2: POS Tagging (Months 3-5)
- Design Classical Chinese POS tagset
- Annotate training data (500-1000 sentences)
- Train custom POS tagger
- Evaluate and iterate
- **Deliverable**: POS tagger with ~75% accuracy

### Phase 3: Parsing (Months 6-9)
- Implement rule-based parser for common patterns
- Train neural parser on annotated data
- Develop hybrid system
- **Deliverable**: Parser with ~70% accuracy

### Phase 4: NER & Refinement (Months 10-12)
- Build historical entity gazetteer
- Implement NER system
- End-to-end evaluation
- Performance optimization
- **Deliverable**: Production-ready Classical Chinese NLP pipeline

## Budget Estimates

### Minimal Approach (Research)
- **Development time**: 2-4 weeks
- **Developer cost**: $5,000-$10,000
- **Tools**: Free/open-source
- **Total**: $5,000-$10,000

### Production System
- **Development time**: 12 months
- **Team**: 2 engineers + 1 linguist consultant
- **Developer cost**: $200,000-$300,000
- **Annotation cost**: $30,000-$60,000
- **Infrastructure**: $5,000/year
- **Total**: $235,000-$365,000

### Quick Adaptation (Stanford CoreNLP fine-tuning)
- **Development time**: 3-6 months
- **Developer cost**: $50,000-$100,000
- **Annotation cost**: $20,000-$40,000
- **Total**: $70,000-$140,000

## Risk Assessment

### High Risk Areas
1. **Annotation quality**: Classical Chinese requires expert linguists
2. **Performance ceiling**: May not reach modern Chinese accuracy levels
3. **Maintenance**: Specialized system requires ongoing expertise
4. **Corpus representativeness**: Different periods have different characteristics

### Mitigation Strategies
1. Collaborate with academic institutions for annotation
2. Set realistic accuracy expectations (70-80%, not 95%+)
3. Document extensively for knowledge transfer
4. Focus on one period initially (e.g., Pre-Qin), expand later

## Final Recommendation

### For Most Projects: Incremental Approach

**Start with Jiayan + ctext.org**, then build custom components as needed:

1. **Week 1-2**: Set up Jiayan segmentation + ctext.org integration
2. **Month 1-2**: Build rule-based POS tagger for common patterns
3. **Month 3-4**: Add pattern-based parsing for frequent structures
4. **Month 5+**: Incrementally improve based on real usage data

**Advantages**:
- Fast time to initial value
- Learn from real usage before heavy investment
- Validate use case before committing resources
- Can pivot to different approach if needed

**This approach balances speed, cost, and flexibility while acknowledging that Classical Chinese NLP is still an open research problem.**
