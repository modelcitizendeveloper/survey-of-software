# Use Case: Search & Indexing

## Scenario Description
Enabling search functionality for Chinese text by indexing with romanization. Users can search using Pinyin, Zhuyin, or partial romanization, and find matching Chinese characters or words.

## User Persona
- **Primary**: Developers building search features for Chinese content
- **Secondary**: End users searching Chinese e-commerce, documents, contacts
- **Platforms**: Web search, mobile app search, database queries, autocomplete
- **Scale**: Hundreds to billions of indexed items

## Examples of Real Applications
- **E-commerce**: Search products by Pinyin (typing "shouji" finds "手机" phones)
- **Contact lists**: Find "张三" by typing "zhangsan"
- **Document search**: Search Chinese PDFs/documents using romanization
- **Autocomplete**: Suggest completions as user types Pinyin
- **Cross-linguistic search**: Match English "Beijing" to "北京"

## Technical Requirements

### Core Capabilities
1. **Indexing**: Convert Chinese text to multiple searchable romanization forms
2. **Fuzzy matching**: Handle tone-less input, partial input, typos
3. **Multi-format matching**: Accept Pinyin, Zhuyin, tone marks, numbers
4. **Fast lookup**: Sub-second query response for millions of documents
5. **Storage efficient**: Minimize index size overhead
6. **Normalization**: Consistent handling of variants

### Performance Constraints
- **Index time**: Can be slow (batch processing)
- **Query time**: Must be fast (< 100ms for user experience)
- **Storage**: Index size matters at scale
- **Memory**: Large indexes must fit in available RAM or cache efficiently

### Accuracy Requirements
- **Critical**: All variants of a query must match the target
- **Important**: Minimize false positives
- **Nice-to-have**: Ranked results by relevance

## Library Analysis

### pypinyin Assessment
**Strengths for Search/Indexing**:
- ✅ **Multiple output styles** (create multiple index keys)
- ✅ **First letter extraction** (fast prefix matching)
- ✅ **Tone and tone-less variants** (fuzzy matching)
- ✅ **Context-aware** (more accurate indexing)
- ✅ **Heteronym support** (index all pronunciations)

**Weaknesses for Search/Indexing**:
- ⚠️ Doesn't solve the matching/ranking problem (just provides romanization)
- ⚠️ Memory usage for large-scale indexing

**Verdict**: **Excellent for index creation**. Provides all romanization variants needed for comprehensive search.

### dragonmapper Assessment
**Strengths for Search/Indexing**:
- ✅ Character → Pinyin/Zhuyin conversion
- ✅ Format identification (detect user query type)
- ✅ Simpler API (easier integration)

**Weaknesses for Search/Indexing**:
- ❌ Fewer romanization variants (can't create as many index keys)
- ❌ No heteronym support (misses alternate pronunciations)
- ❌ No first-letter extraction (can't do prefix matching easily)

**Verdict**: **Adequate but limited**. Works for basic search but lacks features for sophisticated matching.

## Detailed Feature Comparison for Search

| Feature | pypinyin | dragonmapper | Search Value |
|---------|----------|--------------|--------------|
| **Multiple romanization styles** | ✅ 13+ | ⚠️ 2 | High (more match variants) |
| **First letter indexing** | ✅ | ❌ | High (prefix search) |
| **Tone-less variant** | ✅ | ❌ | Critical (most users don't type tones) |
| **All heteronym pronunciations** | ✅ | ❌ | High (comprehensive indexing) |
| **Zhuyin indexing** | ✅ | ✅ | Medium (Taiwan market) |
| **Query format detection** | ❌ | ✅ | Medium (convenience) |

## Recommendation

### Primary Recommendation: **pypinyin**
pypinyin's rich output options are perfect for creating comprehensive search indexes. The ability to generate multiple romanization variants enables robust fuzzy matching.

### Use dragonmapper for:
- Query preprocessing (detect and normalize user input format)
- Converting user queries between Pinyin/Zhuyin

### Combined Approach:
Use **pypinyin for indexing** + **dragonmapper for query processing**

## Implementation Patterns

### Pattern 1: Multi-Key Indexing
Create multiple index keys for comprehensive matching:

```python
from pypinyin import pinyin, lazy_pinyin, Style

def generate_search_keys(chinese_text):
    """Generate all searchable variants for indexing"""
    return {
        # Full Pinyin with tones (exact match)
        'pinyin_full': ' '.join([p[0] for p in pinyin(chinese_text, style=Style.TONE)]),

        # Pinyin without tones (fuzzy match - most common query)
        'pinyin_notone': ' '.join(lazy_pinyin(chinese_text)),

        # First letters only (fast prefix match)
        'pinyin_abbrev': ''.join([p[0] for p in pinyin(chinese_text, style=Style.FIRST_LETTER)]),

        # Zhuyin (Taiwan users)
        'zhuyin': ' '.join([p[0] for p in pinyin(chinese_text, style=Style.BOPOMOFO)]),

        # Original Chinese
        'chinese': chinese_text,
    }

# Example: Indexing "手机" (mobile phone)
keys = generate_search_keys('手机')
# {
#   'pinyin_full': 'shǒu jī',
#   'pinyin_notone': 'shou ji',
#   'pinyin_abbrev': 'sj',
#   'zhuyin': 'ㄕㄡˇ ㄐㄧ',
#   'chinese': '手机'
# }
```

### Pattern 2: Autocomplete / Prefix Search
Enable fast prefix matching using first letters:

```python
from pypinyin import pinyin, Style

def build_autocomplete_index(products):
    """Build prefix-based autocomplete index"""
    index = {}

    for product in products:
        name = product['name_chinese']

        # Get first letter abbreviation
        abbrev = ''.join([p[0] for p in pinyin(name, style=Style.FIRST_LETTER)])

        # Store all prefixes
        for i in range(1, len(abbrev) + 1):
            prefix = abbrev[:i]
            if prefix not in index:
                index[prefix] = []
            index[prefix].append(product)

    return index

# User types "sj" → matches "手机" (shouji)
# User types "sjz" → matches "手机壳" (shoujike)
```

### Pattern 3: Fuzzy Matching with Tone Tolerance
Accept queries with or without tones:

```python
from pypinyin import lazy_pinyin

def normalize_query(query):
    """Convert query to tone-less form for fuzzy matching"""
    # If query is Chinese, convert to Pinyin
    if has_chinese(query):
        return ' '.join(lazy_pinyin(query))

    # If already Pinyin, strip tones (if present)
    return remove_tones(query)  # Custom function

def search(index, user_query):
    """Search using normalized form"""
    normalized = normalize_query(user_query)

    # Match against tone-less index keys
    return index.get(normalized, [])
```

### Pattern 4: Heteronym Coverage
Index all possible pronunciations for comprehensive matching:

```python
from pypinyin import pinyin, Style

def index_with_heteronyms(text):
    """Index all possible pronunciations"""
    # Get all pronunciation variants
    variants = pinyin(text, style=Style.NORMAL, heteronym=True)

    # Generate all combinations
    keys = []
    for pronunciations in variants:
        keys.extend(pronunciations)

    return set(keys)  # Unique pronunciations

# Example: "行" can be "xing" or "hang"
# Both will be indexed, so either query finds it
```

### Pattern 5: Database Integration (PostgreSQL)
Store multiple romanization columns for fast querying:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name_chinese TEXT,
    name_pinyin TEXT,           -- shǒu jī
    name_pinyin_notone TEXT,    -- shou ji (most queries)
    name_pinyin_abbrev TEXT,    -- sj (fast prefix)
    name_zhuyin TEXT            -- ㄕㄡˇ ㄐㄧ
);

-- Index for fast lookups
CREATE INDEX idx_pinyin_notone ON products USING GIN (to_tsvector('simple', name_pinyin_notone));
CREATE INDEX idx_abbrev ON products (name_pinyin_abbrev);

-- Query examples
SELECT * FROM products WHERE name_pinyin_notone LIKE 'shou ji%';
SELECT * FROM products WHERE name_pinyin_abbrev = 'sj';
```

```python
# Populate database using pypinyin
from pypinyin import pinyin, lazy_pinyin, Style

def index_product(product):
    keys = generate_search_keys(product['name_chinese'])

    cursor.execute("""
        INSERT INTO products (name_chinese, name_pinyin, name_pinyin_notone, name_pinyin_abbrev, name_zhuyin)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        product['name_chinese'],
        keys['pinyin_full'],
        keys['pinyin_notone'],
        keys['pinyin_abbrev'],
        keys['zhuyin'],
    ))
```

### Pattern 6: Elasticsearch Integration
Use Elasticsearch with custom analyzers:

```python
from pypinyin import lazy_pinyin

# Create Elasticsearch index with Pinyin field
index_mapping = {
    "mappings": {
        "properties": {
            "name_chinese": {"type": "text", "analyzer": "standard"},
            "name_pinyin": {"type": "text", "analyzer": "simple"},
            "name_abbrev": {"type": "keyword"},  # Exact match for abbreviations
        }
    }
}

# Index documents
def index_to_elasticsearch(doc):
    es_doc = {
        'name_chinese': doc['name'],
        'name_pinyin': ' '.join(lazy_pinyin(doc['name'])),
        'name_abbrev': ''.join([p[0] for p in pinyin(doc['name'], style=Style.FIRST_LETTER)]),
    }

    es.index(index='products', body=es_doc)

# Query: Search across all fields
query = {
    "multi_match": {
        "query": user_input,
        "fields": ["name_chinese^3", "name_pinyin^2", "name_abbrev"]  # Boost Chinese matches
    }
}
```

## Trade-offs

### Index Size vs Match Quality
**Trade-off**: More romanization variants = larger index but better matching

**pypinyin enables**:
- Full index (4-5 variants per item): Comprehensive matching, higher storage
- Minimal index (1-2 variants): Lower storage, missed matches

**Recommendation**: Include at least:
1. Tone-less Pinyin (90% of queries)
2. First-letter abbreviation (fast prefix search)

### Pre-Processing vs Query-Time Conversion
**Trade-off**: Convert at index time (pypinyin) or query time (dragonmapper)?

**Index-time conversion (RECOMMENDED)**:
- ✅ Fast queries (no conversion needed)
- ✅ Consistent romanization across index
- ❌ Slower indexing, larger index size

**Query-time conversion**:
- ✅ Smaller index
- ✅ Faster indexing
- ❌ Slower queries
- ❌ Inconsistent if query format varies

**Recommendation**: Use pypinyin at index time for best search performance.

### Heteronym Handling
**Trade-off**: Index all pronunciations (pypinyin heteronym=True) or just most common?

**Index all pronunciations**:
- ✅ Comprehensive (won't miss rare pronunciations)
- ❌ Larger index (more keys per item)
- ❌ Possible false positives

**Index most common only**:
- ✅ Smaller index
- ✅ Fewer false positives
- ❌ Might miss valid matches

**Recommendation**: For most applications, index most common pronunciation (default). Use heteronym=True for critical applications (medical, legal) where missing a match is unacceptable.

## Performance Considerations

### Index Creation Time
- **Small scale** (< 10k items): Real-time indexing acceptable
- **Medium scale** (10k-1M items): Batch processing, minutes to hours
- **Large scale** (> 1M items): Distributed processing, optimize pypinyin calls

### Optimization Tips
```python
# Batch processing for large datasets
from pypinyin import lazy_pinyin, pinyin, Style

def batch_index(items, batch_size=1000):
    """Process items in batches to optimize memory"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]

        for item in batch:
            # Generate keys
            keys = generate_search_keys(item['name'])
            # Store in index
            store_keys(item['id'], keys)

# Cache common characters/words
common_words = ['手机', '电脑', '书', ...]  # Top 10k words
pinyin_cache = {word: lazy_pinyin(word) for word in common_words}

def get_pinyin_cached(text):
    if text in pinyin_cache:
        return pinyin_cache[text]
    return lazy_pinyin(text)
```

### Query Performance
- **Average query time**: Sub-second for millions of items (with proper indexing)
- **Bottleneck**: Usually database/search engine, not pypinyin
- **Optimization**: Use database indexes (GIN, GiST for PostgreSQL) or search engines (Elasticsearch)

## Real-World Example: Contact Search

```python
from pypinyin import lazy_pinyin, pinyin, Style

class ContactSearchIndex:
    def __init__(self):
        self.index = {
            'full': {},      # Full Pinyin: "zhang san"
            'abbrev': {},    # Abbreviation: "zs"
            'chinese': {},   # Original: "张三"
        }

    def add_contact(self, contact_id, name_chinese):
        """Add contact to search index"""
        # Full Pinyin (tone-less)
        full_pinyin = ' '.join(lazy_pinyin(name_chinese))
        self.index['full'][full_pinyin] = contact_id

        # Abbreviation
        abbrev = ''.join([p[0] for p in pinyin(name_chinese, style=Style.FIRST_LETTER)])
        self.index['abbrev'][abbrev] = contact_id

        # Chinese
        self.index['chinese'][name_chinese] = contact_id

    def search(self, query):
        """Search contacts by any format"""
        # Try all index types
        results = []

        # Check Chinese
        if query in self.index['chinese']:
            results.append(self.index['chinese'][query])

        # Check full Pinyin
        if query in self.index['full']:
            results.append(self.index['full'][query])

        # Check abbreviation
        if query in self.index['abbrev']:
            results.append(self.index['abbrev'][query])

        # Prefix matching for autocomplete
        for abbrev, contact_id in self.index['abbrev'].items():
            if abbrev.startswith(query):
                results.append(contact_id)

        return list(set(results))  # Deduplicate

# Usage
index = ContactSearchIndex()
index.add_contact(1, '张三')
index.add_contact(2, '李四')

# All of these find "张三":
index.search('张三')      # Chinese name
index.search('zhang san') # Full Pinyin
index.search('zs')        # Abbreviation
index.search('z')         # Prefix (autocomplete)
```

## Missing Capabilities

Neither library helps with:
- ❌ Ranking/scoring results (need search engine logic)
- ❌ Typo tolerance (need fuzzy matching algorithms)
- ❌ Natural language queries (need NLP)
- ❌ Relevance tuning (need machine learning)
- ❌ Real-time index updates (need database optimization)

These require additional components beyond romanization libraries.

## Conclusion

**pypinyin is essential for Chinese search/indexing.** Its ability to generate multiple romanization variants enables comprehensive, fuzzy-tolerant search. The feature-rich output options allow developers to balance index size, match quality, and query speed.

Use pypinyin at index creation time, store multiple romanization forms in your database/search engine, and enjoy fast, flexible Chinese text search.

dragonmapper can supplement query preprocessing but isn't sufficient on its own for search indexing.
