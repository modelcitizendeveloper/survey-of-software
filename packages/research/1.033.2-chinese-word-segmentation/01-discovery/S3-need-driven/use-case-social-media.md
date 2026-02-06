# Use Case: Social Media Analytics

**Tool**: PKUSeg (web model) or Jieba
**Volume**: Millions of posts daily (Weibo, WeChat, Douyin)
**Accuracy**: PKUSeg 94.21% F1 on Weibo dataset

## Key Strengths
- PKUSeg web model trained on social media corpus
- Handles informal text, slang, emoji
- Batch processing for sentiment analysis

## Implementation
```python
import pkuseg
seg = pkuseg.pkuseg(model_name='web')

# Process social media post
post = "今天天气超级棒！😊去三里屯逛街了"
segments = seg.cut(post)
# ['今天', '天气', '超级', '棒', '！', '😊', '去', '三里屯', '逛街', '了']
```

## Alternative: Jieba (high-throughput)
- Real-time monitoring: Jieba (1000+ posts/s)
- Offline analytics: PKUSeg (higher accuracy)

**Cross-reference**: [S2 pkuseg.md](../S2-comprehensive/pkuseg.md)
