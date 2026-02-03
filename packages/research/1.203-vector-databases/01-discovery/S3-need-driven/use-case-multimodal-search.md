# Use Case: Multi-Modal Search (Images + Text)

## Scenario

**Context**: Digital asset management for media company
**Data**: 500K images + captions, CLIP embeddings (both image and text vectors)
**Usage**: Creatives search by text description OR upload similar image
**Stack**: Python, CLIP model, LangChain

## Requirements

### Must-Have
1. ✅ **Multi-vector support**: Store both image embedding AND text embedding per asset
2. ✅ **Framework integration**: CLIP, LangChain, image2vec support
3. ✅ **Easy deployment**: Small team, limited DevOps
4. ✅ **Metadata filtering**: Search by date, photographer, license, tags

### Nice-to-Have
1. **Built-in embedding**: img2vec, text2vec modules reduce custom code
2. **Batch ingestion**: Import 100k+ images efficiently
3. **Cross-modal search**: Query with text, find similar images (and vice versa)

## Candidate Evaluation

| Database | Multi-Vector | Ecosystem | Deploy | Filtering | Fit |
|----------|--------------|-----------|--------|-----------|-----|
| **ChromaDB** | ⚠️ Workaround | ✅ Good | ✅ BEST | ⚠️ Basic | **70%** (multi-vector hacky) |
| **Pinecone** | ❌ Single vector | ✅ Good | ✅ Easy | ✅ Good | **FAILS** (no multi-vector) |
| **Qdrant** | ✅ Named vectors | ⚠️ Growing | ⚠️ Moderate | ✅ BEST | **90%** |
| **Weaviate** | ✅ Multi-vector | ✅ BEST (28+ modules) | ⚠️ Moderate | ✅ Good | **100%** |

## Recommendation

### Primary: **Weaviate**

**Why:**
1. **Best ecosystem**: img2vec, multi2vec, CLIP modules built-in
2. **Multi-vector native**: `img2vec-neural` + `text2vec-openai` in same object
3. **Cross-modal search**: Query text, retrieve images (built-in)
4. **Rich integrations**: 28+ modules reduce custom code significantly

**Example schema:**
```python
{
  "class": "Image",
  "vectorizer": "multi2vec-clip",  # Built-in CLIP support
  "moduleConfig": {
    "multi2vec-clip": {
      "imageFields": ["image"],
      "textFields": ["caption"]
    }
  },
  "properties": [
    {"name": "caption", "dataType": ["text"]},
    {"name": "image", "dataType": ["blob"]},
    {"name": "photographer", "dataType": ["string"]},
    {"name": "license", "dataType": ["string"]}
  ]
}
```

**Query with text, find images:**
```graphql
{
  Get {
    Image(
      nearText: {concepts: ["sunset over mountains"]}
      where: {path: ["license"], operator: Equal, valueString: "CC-BY"}
    ) {
      caption
      photographer
      _additional { certainty }
    }
  }
}
```

**Cost**: ~$150-250/month self-hosted, $300/month Weaviate Cloud

### Alternative: **Qdrant** (if GraphQL is unfamiliar)

**Why:**
- Named vectors support (store image + text vectors separately)
- Better performance than Weaviate
- Lower cost (~$100/month)
- REST API (more familiar)

**Trade-off**: Less integrated (manual CLIP embedding vs Weaviate's built-in modules)

## Confidence

**High (85%)** - Weaviate's module ecosystem and multi-vector support is uniquely strong for this use case.
