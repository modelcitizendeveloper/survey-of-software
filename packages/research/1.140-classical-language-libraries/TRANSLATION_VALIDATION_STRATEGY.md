# Translation Validation Strategy

**Date**: 2025-11-18
**Status**: Design document

---

## Problem Statement

Current parser has **75-80% accuracy** with PROIEL + known-words (5 words).
How do we get to **95-98% accuracy** cost-effectively?

---

## Solution: Translation-Based Validation

**Key Insight**: Wrong parses produce nonsensical English translations.

### Example

```
Latin: "Nautam video"

❌ WRONG PARSE:
  Nautam → navo (VERB "to swim")
  video → video (VERB "see")
  English: "swim see" ← NONSENSE!

✅ CORRECT PARSE:
  Nautam → nauta (NOUN "sailor", accusative)
  video → video (VERB "see")
  English: "I see the sailor" ← MAKES SENSE!
```

---

## Why This Works

### 1. Catches Semantic Errors
Morphological checking can't distinguish:
- `navo` (to swim) vs `nauta` (sailor) - both grammatically valid
- Translation reveals which meaning makes sense

### 2. Catches Structural Errors
- Two verbs in a row → suspicious
- Missing subject/object → incomplete sentence
- Wrong case → wrong word role

### 3. Human-Readable
- Non-experts can spot nonsense translations
- Easy to debug (see exactly what went wrong)
- Teaching tool (learners understand errors)

---

## Implementation Approaches

### Approach A: Rule-Based (Simple, Free)

**Components**:
1. **500-word English gloss dictionary**
   - nauta → "sailor"
   - video → "see"
   - puella → "girl"

2. **Simple translation rules**:
   - Nominative NOUN → subject (first position)
   - Accusative NOUN → direct object (add "the")
   - Dative NOUN → indirect object ("to X")
   - VERB → English verb

3. **Coherence checks**:
   - Has subject + verb?
   - No double verbs without conjunction?
   - Word roles make sense?

**Pros**: Free, fast, deterministic
**Cons**: Doesn't handle complex grammar, false positives

---

### Approach B: LLM-Based (Advanced, Low Cost)

**Strategy**:
```
1. Parse Latin → [lemma, POS, case, number]
2. Send to Claude Haiku:
   "Translate this Latin parse to English.
    If the parse seems incorrect, explain why."
3. Compare LLM translation with reference translation
4. If mismatch > threshold → flag for review
5. Use LLM to suggest correction
```

**Prompt Template**:
```
You are a Latin grammar expert. Given this parse, generate English translation:

Latin: "Nautam video"
Parse:
  Nautam → nauta (NOUN, accusative singular)
  video → video (VERB, 1st person singular present)

Expected translation: "I see the sailor"

Tasks:
1. Generate translation from parse
2. Does it match expected? (yes/no)
3. If no, explain what's wrong with the parse
4. Suggest correct parse

Keep response under 100 words.
```

**Cost**:
- Input: ~100 tokens (parse + instructions)
- Output: ~50 tokens (translation + validation)
- Total: ~150 tokens × $0.25/1M = **$0.000038 per word**

For 1000 words with 10% flagged:
- Cost: 100 words × $0.000038 = **$0.0038** (~half a penny)

**Pros**: High accuracy, catches subtle errors, provides explanations
**Cons**: API dependency, small cost

---

### Approach C: Hybrid (Recommended)

**Layer 1: Known-Word Database** (70% coverage)
- 500 curated common words
- 99% accuracy
- FREE, instant

**Layer 2: Rule-Based Translation Validation** (20% coverage)
- Simple gloss dictionary
- Coherence checks
- FREE, fast
- Flags suspicious patterns

**Layer 3: LLM Validation** (10% flagged)
- Only for flagged cases
- Claude Haiku for validation
- ~$0.01 per 1000 words
- 95%+ accuracy

**Layer 4: LLM Arbitration** (5% critical)
- Human review queue
- Claude Sonnet for difficult cases
- ~$0.02 per 1000 words
- 99% accuracy

**Combined Stats**:
- Overall accuracy: **97-98%**
- Cost: **~$0.03 per 1000 words** (~$1/month for typical app)
- Speed: Fast (most words skip LLM)

---

## Validation Workflow

```mermaid
Input Latin word
    ↓
Check known_words.json
    ↓
Found? → Return (99% accurate, FREE)
    ↓ No
Parse with PROIEL
    ↓
Generate simple English translation
    ↓
Coherence check passes?
    ↓ No (suspicious)
Send to Claude Haiku for validation
    ↓
LLM confirms error?
    ↓ Yes
Flag for correction
    ↓
Update known_words.json
    ↓
Return corrected parse
```

---

## Real-World Examples

### Example 1: Catching Wrong Lemma

```
Latin: "Nautam video"
PROIEL parse: navo (VERB)
Rule-based translation: "swim see"
Coherence check: ✗ Two verbs!
LLM validation: "Should be nauta (sailor, accusative)"
Correction: Update known_words.json
Result: "I see the sailor" ✓
```

### Example 2: Validating Correct Parse

```
Latin: "Puella rosam dat"
PROIEL parse: puella (NOUN), rosa (NOUN), do (VERB)
Rule-based translation: "girl gives rose"
Coherence check: ✓ Subject-verb-object
Result: No LLM needed, accept parse ✓
```

### Example 3: Ambiguous Case

```
Latin: "Poeta carmina scribit"
PROIEL parse: poeta (NOUN, nom), carmen (NOUN, acc), scribo (VERB)
Rule-based translation: "poet writes poems"
Coherence check: ✓ Seems okay
Reference translation: "The poet writes poems"
Fuzzy match: ✓ Close enough
Result: Accept parse ✓
```

---

## Implementation Roadmap

### Week 1: Foundation (Rule-Based)
- **Day 1-2**: Build 500-word English gloss dictionary
  - Use Wheelock's Latin vocabulary
  - Map lemma → English gloss
  - Store in JSON

- **Day 3**: Implement simple translation generator
  - Case → word role mapper
  - Basic sentence structure rules
  - Output: "subject verb object"

- **Day 4**: Add coherence checks
  - Detect double verbs
  - Check subject-verb agreement
  - Flag nonsense patterns

- **Day 5**: Test on Wheelock chapters 1-5
  - Measure error detection rate
  - Tune coherence rules
  - Identify false positives

### Week 2: LLM Integration
- **Day 1-2**: Build LLM validation API
  - Claude Haiku integration
  - Prompt engineering
  - Response parsing

- **Day 3**: Implement fuzzy translation matching
  - Compare LLM translation with reference
  - Levenshtein distance or semantic similarity
  - Threshold tuning

- **Day 4**: Build error flagging system
  - Flag high-confidence errors
  - Human review queue
  - Correction feedback loop

- **Day 5**: Measure accuracy improvement
  - Test on 1000 sentences
  - Calculate error detection rate
  - Measure cost per 1000 words

### Week 3: Production Deployment
- **Day 1-2**: Integrate all validation layers
  - Known-words → Rule-based → LLM pipeline
  - Fallback logic
  - Error handling

- **Day 3**: Build correction feedback loop
  - User corrections → known_words.json
  - LLM-suggested corrections → review queue
  - Automatic database updates

- **Day 4**: Test on full corpus
  - Caesar De Bello Gallico
  - Cicero speeches
  - Virgil Aeneid (samples)

- **Day 5**: Deploy and monitor
  - Production deployment
  - Monitor accuracy metrics
  - Track costs

---

## Success Metrics

### Accuracy Targets
- Week 1: 85% (rule-based validation)
- Week 2: 95% (LLM validation)
- Week 3: 97-98% (production system)

### Cost Targets
- Rule-based: $0 (FREE)
- LLM validation: < $0.05 per 1000 words
- Overall: ~$1-3 per month for typical educational app

### Performance Targets
- Latency: < 100ms per word (99th percentile)
- Throughput: 100+ words per second
- Availability: 99.9% uptime

---

## Expected ROI

**Investment**:
- Week 1: Rule-based (1 week effort)
- Week 2: LLM integration (1 week effort)
- Week 3: Production (1 week effort)
- **Total: 3 weeks**

**Returns**:
- Accuracy: 75% → 97% (+22 percentage points)
- User satisfaction: High (reliable translations)
- Cost: ~$1-3/month (negligible)
- Maintenance: Low (self-improving via feedback)

**Ongoing Benefits**:
- Self-improving (corrections feed back to known-words DB)
- Scales to any Latin text (not just beginner corpus)
- Educational value (learners see why errors occurred)
- Production-ready quality (97-98% accuracy)

---

## Risks and Mitigations

### Risk 1: LLM API costs spiral
**Mitigation**:
- Only use LLM for flagged cases (10%)
- Use cheapest model (Haiku)
- Cache LLM responses
- Monitor costs with alerts

### Risk 2: False positives (flagging correct parses)
**Mitigation**:
- Tune coherence rules on training data
- Use confidence thresholds
- Human review for borderline cases
- Improve known-words DB to reduce false flags

### Risk 3: Reference translations not available
**Mitigation**:
- Start with Wheelock (has translations)
- Build own corpus with verified translations
- Use LLM to generate reference translations
- Community contributions

---

## Conclusion

Translation validation is a **powerful, cost-effective** way to improve parser accuracy:

✅ **Catches errors morphology misses** (wrong lemma, right grammar)
✅ **Human-readable** (anyone can spot nonsense)
✅ **Cost-effective** (~$1/month for typical app)
✅ **Self-improving** (corrections feed back to database)
✅ **Production-ready** (97-98% accuracy achievable)

**Next Step**: Implement Week 1 (rule-based validation) to prove concept, then iterate.
