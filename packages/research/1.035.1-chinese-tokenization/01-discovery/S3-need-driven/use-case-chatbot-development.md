# Use Case: Real-Time Chatbot Development

## Who Needs This

**Persona**: Full-stack developer building customer service chatbot

**Context**: Chinese customer service bot for e-commerce/banking. Must respond in <500ms. Handles 10K+ concurrent users during peak. Mixed inputs: formal queries, slang, typos.

**Scale**: 1M+ daily messages, real-time response requirements

## Why They Need Tokenization

### Core Requirements
1. **Low latency**: Tokenization must complete in <50ms
2. **Handles informal text**: Slang, abbreviations, emoji
3. **Robust**: Must not crash on malformed input
4. **Simple integration**: Small team, limited ML expertise

### Business Impact
- Slow tokenization → Slow bot → Poor UX → User abandonment
- Crash on weird input → Service outage
- Example: User inputs "手机坏了😭怎么办" (phone broken + emoji)

## Key Constraints

| Constraint | Requirement | Why |
|------------|-------------|-----|
| Latency | <50ms per message | Real-time chat |
| Throughput | 10K QPS | Concurrent users |
| Robustness | No crashes | Production stability |
| Simplicity | Easy to deploy | Small team |
| Accuracy | Good enough (~90%) | Not critical for chat |

## Recommended Solution

### Primary: LAC (Baidu)

```python
from LAC import LAC

# Joint seg + NER for intent recognition
lac = LAC(mode='lac')

def process_message(text):
    words, tags = lac.run(text)
    # tags include NER (LOC, PER, ORG)
    # Useful for extracting entities from user queries
    return words, tags

# Example
text = "我要查北京到上海的机票"
words, tags = process_message(text)
# words: ['我', '要', '查', '北京', '到', '上海', '的', '机票']
# tags: ['r', 'v', 'v', 'LOC', 'v', 'LOC', 'u', 'n']
# Extracted entities: 北京 (LOC), 上海 (LOC)
```

**Why LAC**:
- ✅ **Fast**: 800 QPS, meets latency requirements
- ✅ **Joint seg + NER**: Extracts entities for intent recognition
- ✅ **Production-tested**: Baidu scale reliability
- ✅ **Good accuracy**: F1 > 91%, sufficient for chatbots

### Fallback Pattern
```python
def robust_tokenize(text):
    try:
        # Try LAC for seg + NER
        return lac.run(text)
    except Exception as e:
        # Fallback to character-level on error
        logger.error(f"LAC failed: {e}")
        return list(text), ['x'] * len(text)
```

## Alternatives

### If Maximum Speed Needed
**Use: Jieba (precise mode)**
- 400 KB/s, faster than LAC for pure segmentation
- No NER (need separate model)
- Good for simple keyword matching

```python
import jieba

def quick_segment(text):
    return list(jieba.cut(text))
```

### If Building with LLMs (GPT, Claude)
**Use: LLM's native tokenizer + no pre-segmentation**
- Modern LLMs handle Chinese without pre-segmentation
- Simpler architecture (fewer components)
- Higher inference cost

## Implementation Pattern

```python
from LAC import LAC
from your_nlu import IntentClassifier

lac = LAC(mode='lac')
intent_clf = IntentClassifier()

def handle_message(user_message):
    # 1. Tokenize + NER (combined in LAC)
    words, tags = lac.run(user_message)

    # 2. Extract entities
    entities = extract_entities(words, tags)

    # 3. Classify intent
    intent = intent_clf.predict(words)

    # 4. Generate response
    response = generate_response(intent, entities)
    return response

def extract_entities(words, tags):
    entities = {}
    for word, tag in zip(words, tags):
        if tag in ['LOC', 'PER', 'ORG', 'TIME']:
            entities[tag] = word
    return entities
```

## Validation Checklist

- [ ] Load test: 10K concurrent requests, <500ms response
- [ ] Test informal inputs: slang, emoji, typos
- [ ] Test malformed inputs: empty strings, very long messages
- [ ] Monitor latency percentiles (p50, p95, p99)
- [ ] Add fallback for LAC failures
- [ ] Test entity extraction accuracy on sample dialogues

## Common Pitfalls

❌ **Using BERT for real-time chat**: Too slow
```python
# WRONG - BERT takes 200-500ms per message
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
```

✅ **Using production-grade segmenter**: Fast enough
```python
# RIGHT - LAC takes 10-20ms per message
lac = LAC(mode='seg')
```

## Summary

**For real-time chatbots, use LAC** because:
- Fast enough for real-time (800 QPS)
- Joint seg + NER helps intent recognition
- Production-tested reliability (Baidu)
- Good accuracy without over-engineering

**Upgrade to LLM native tokenization if**: Building with modern LLMs (GPT-4, Claude) where tokenization is handled internally.
