# Use Case: Real-Time Chatbot

**Tool**: Jieba or LTP Tiny (GPU)
**Latency**: <50ms p95 requirement
**Volume**: 1K-10K concurrent conversations

## Key Strengths
- Jieba: <10ms latency (CPU)
- LTP Tiny: 10-15ms (GPU), 96.8% accuracy
- Horizontal scaling for throughput

## Implementation
```python
import jieba
jieba.initialize()  # Pre-load dictionary

def process_user_message(message):
    segments = list(jieba.cut(message))
    # Intent recognition, entity extraction
    return generate_response(segments)

# <10ms latency per message
```

## Alternative: LTP Tiny (GPU)
- Higher accuracy (96.8% vs. 85%)
- Multi-task (WS + NER for entity extraction)
- Requires GPU infrastructure

**Trade-off**: Jieba (speed, cost) vs. LTP Tiny (accuracy)

**Cross-reference**: [S2 jieba.md](../S2-comprehensive/jieba.md), [S2 ltp.md](../S2-comprehensive/ltp.md)
