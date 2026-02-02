# Use Case: E-commerce Product Search

## Who Needs This

**Persona**: Backend engineer at e-commerce platform

**Context**: Building search functionality for Chinese product listings. Users search for products like "苹果手机" (Apple phone), "运动鞋" (sneakers), or long-tail queries like "无线蓝牙耳机降噪" (wireless Bluetooth noise-canceling earphones).

**Scale**: 1M+ products, 10K+ queries per second peak

## Why They Need Tokenization

### Core Requirements
1. **High recall**: Must match even if user query differs from product title
   - User: "手机" → Should match: "智能手机", "苹果手机"
2. **Fast indexing**: Index 1M products in reasonable time
3. **Real-time query**: <50ms query response time
4. **Handle variations**: Brand names, model numbers, mixed Chinese-English

### Business Impact
- Poor tokenization → Low recall → Lost sales
- Slow tokenization → Slow search → User abandonment
- Example: "iPhone 15 Pro Max" must tokenize correctly despite mixed language

## Key Constraints

| Constraint | Requirement | Why |
|------------|-------------|-----|
| Speed | >400 KB/s indexing | 1M products to index |
| Latency | <10ms per query | Real-time search |
| Recall | >95% | Can't miss products |
| Precision | Less critical | Users can filter results |
| Complexity | Low | Small team, fast iteration |

## Recommended Solution

### Primary: Jieba (Search Mode)

```python
import jieba

# Index products with fine-grained segmentation
def index_product(title):
    # Search mode creates overlapping segments
    terms = jieba.cut_for_search(title)
    return list(terms)

# Example
title = "苹果iPhone15手机无线充电器套装"
terms = index_product(title)
# Output: ['苹果', 'iPhone', '15', '手机', '无线', '充电', '充电器', '套装']

# Query also uses search mode
query = "苹果手机充电器"
query_terms = jieba.cut_for_search(query)
# Matches: '苹果', '手机', '充电器'
```

**Why Jieba Search Mode**:
- ✅ **Fine-grained segmentation**: Creates overlapping terms for high recall
- ✅ **Fast**: 1.5 MB/s in full mode, can index 1M products in minutes
- ✅ **Simple**: Works out of the box, easy to maintain
- ✅ **Custom dictionary**: Add brand names/SKUs easily

### Custom Dictionary for Brands
```python
# Add e-commerce specific terms
jieba.load_userdict("ecommerce_brands.txt")

# brands.txt:
# 小米 5 n
# 华为 5 n
# iPhone 5 n
```

### Implementation Pattern
```python
from elasticsearch import Elasticsearch
import jieba

es = Elasticsearch()

def index_product(product_id, title):
    # Fine-grained tokenization for recall
    tokens = jieba.cut_for_search(title)

    doc = {
        'title': title,
        'tokens': list(tokens)
    }
    es.index(index='products', id=product_id, body=doc)

def search_products(query):
    # Same tokenization for query
    query_tokens = jieba.cut_for_search(query)

    search_query = {
        'query': {
            'match': {
                'tokens': ' '.join(query_tokens)
            }
        }
    }
    return es.search(index='products', body=search_query)
```

## Alternatives

### If Accuracy Matters More Than Speed
**Use: PKUSEG (web model) + Elasticsearch**
- Better accuracy on product titles
- Handles new brands better (neural model)
- Trade-off: 3x slower indexing (still acceptable for millions of products if batch processed)

### If Multilingual (Chinese + English)
**Use: SentencePiece trained on product corpus**
- Handles mixed Chinese-English naturally
- Learns common product patterns
- Requires training corpus of product titles

### If Already Using LLMs
**Use: transformers (BERT-base-chinese) + vector search**
- Semantic search (not just keyword matching)
- Handles synonyms automatically
- Higher infrastructure cost

## Validation Checklist

- [ ] Test recall on sample queries (aim for >95%)
- [ ] Benchmark indexing speed (1M products in <1 hour acceptable)
- [ ] Measure query latency (aim for <50ms end-to-end)
- [ ] Add brand names to custom dictionary
- [ ] Test mixed Chinese-English queries
- [ ] Handle numbers and model names (e.g., "iPhone 15")

## Common Pitfalls

❌ **Using precise mode for search**: Loses recall
```python
# WRONG
jieba.cut("苹果手机")  # ['苹果', '手机']
# User searches "手机" → Won't match if indexed as "苹果手机"
```

✅ **Using search mode**: High recall
```python
# RIGHT
jieba.cut_for_search("苹果手机")  # ['苹果', '手机', '苹果手机']
# Matches both "苹果手机" and individual terms
```

## Summary

**For e-commerce search, use Jieba search mode** because:
- Fast enough for real-time indexing and queries
- Fine-grained segmentation maximizes recall
- Easy custom dictionary for brands
- Battle-tested by Taobao, JD.com scale

**Upgrade to PKUSEG only if**: Accuracy testing shows Jieba missing too many products (unlikely with good custom dictionary).
