# Use Case: Classical Literature Search Engine

## Context

**Who**: Researchers, students, translators working with classical texts
**Why**: Finding parallel passages, tracking quotations, and studying usage patterns across the classical corpus requires sophisticated search beyond simple string matching.

**Problem Statement**: Classical Chinese texts heavily quote and reference each other. Researchers need to find thematically similar passages, track how phrases evolve across texts, and discover quotations even when wording varies slightly. Character-based search returns too many false positives; semantic search requires understanding grammatical structure.

## User Story

> "As a scholar studying the concept of 仁 (benevolence) in Confucian texts, I want to:
> 1. Find all passages discussing 仁 across the entire classical corpus
> 2. Filter by grammatical context (仁 as subject vs. object vs. modifier)
> 3. Group similar passages together even if exact wording differs
> 4. Track how usage patterns change from Pre-Qin to Han to Tang
> 5. Identify direct quotations vs. thematic parallels
> 6. Export results with citations for academic writing"

## Specific Requirements

### Must Have
- **Corpus-wide search**: Cover major classical texts (Confucian, historical, philosophical)
- **Structural search**: Filter by grammatical role, sentence position
- **Fuzzy matching**: Find similar passages with character substitutions
- **Citation tracking**: Identify quotations and allusions
- **Result clustering**: Group thematically similar passages
- **Export**: CSV, BibTeX, or markdown with citations

### Nice to Have
- **Semantic search**: Find conceptually related passages (requires embeddings)
- **Temporal analysis**: Visualize usage changes over time
- **Co-occurrence**: What terms appear near the query term?
- **Parallel text display**: Show translations alongside classical text
- **API access**: Programmatic search for research pipelines

### Not Critical
- **Real-time search**: 5-10 second response time acceptable
- **Web UI**: API + command-line sufficient initially
- **User accounts**: Can be added later

## Data Characteristics

- **Corpus size**: 30,000+ texts from ctext.org (hundreds of millions of characters)
- **Text types**: Prose (histories, philosophy), poetry, official documents
- **Periods**: Pre-Qin (春秋战国) through Qing dynasty
- **Languages**: Classical Chinese (文言文), some modern annotations
- **Format**: Need to ingest and index from ctext.org API

## Accuracy Requirements

- **Search recall**: 90%+ (critical not to miss relevant passages)
- **Search precision**: 70%+ (some false positives acceptable)
- **Quotation detection**: 85%+ precision (high confidence needed)
- **Structural filtering**: 80%+ accuracy (incorrect filtering is misleading)
- **Response time**: <10 seconds for complex queries

## Recommended Solution

### Architecture

```
Data Ingestion Layer
  ├─ ctext.org API crawler
  ├─ Text preprocessing (punctuation, variants)
  └─ Periodic updates (new texts, corrections)
    ↓
Parsing Layer
  ├─ Jiayan segmentation
  ├─ POS tagging (custom model)
  ├─ Dependency parsing (basic patterns)
  └─ NER (people, places, concepts)
    ↓
Index Layer
  ├─ Elasticsearch (full-text + structural search)
  ├─ PostgreSQL (metadata, citations)
  └─ Vector DB (semantic embeddings - optional Phase 2)
    ↓
Search Layer
  ├─ Query parser (interpret search syntax)
  ├─ Structural filters (grammatical role, position)
  ├─ Fuzzy matching (character variants, synonyms)
  └─ Result ranking (relevance + frequency + source authority)
    ↓
Analysis Layer
  ├─ Quotation detection (n-gram matching + clustering)
  ├─ Passage grouping (semantic similarity)
  ├─ Temporal analysis (usage over time)
  └─ Co-occurrence statistics
    ↓
API & UI
  ├─ REST API (JSON responses)
  ├─ Web UI (React + visualization)
  └─ Export (CSV, BibTeX, markdown)
```

### Tech Stack

- **Corpus**: ctext.org API
- **Parsing**: Jiayan + custom POS/dependency parsers
- **Search**: Elasticsearch (full-text + structured data)
- **Database**: PostgreSQL (metadata, citations)
- **Vector search** (Phase 2): Qdrant or Pinecone
- **Backend**: Python (FastAPI)
- **Frontend**: React + D3.js (visualization)
- **Hosting**: Cloud (AWS/GCP) or institutional servers

### Implementation Time

- **Phase 1 (Basic search)**: 2-3 months
  - Ingest corpus
  - Basic segmentation + indexing
  - Simple search API
- **Phase 2 (Structural search)**: 3-4 months
  - POS tagging + parsing
  - Grammatical filters
  - Quotation detection
- **Phase 3 (Advanced features)**: 4-5 months
  - Semantic search
  - Temporal analysis
  - Web UI
- **Total MVP**: 6-8 months
- **Full product**: 12-15 months

## Example Implementation

```python
from elasticsearch import Elasticsearch
import jiayan

class ClassicalChineseSearch:
    def __init__(self):
        self.es = Elasticsearch()
        self.segmenter = jiayan.load()
        self.index = 'classical_chinese_corpus'

    def index_corpus(self):
        """Ingest and index ctext.org corpus"""
        for text in ctext_api.get_all_texts():
            # Parse text
            parsed = self.parse_text(text['content'])

            # Index document
            doc = {
                'title': text['title'],
                'author': text['author'],
                'period': text['period'],
                'content': text['content'],
                'words': parsed['words'],
                'pos_tags': parsed['pos'],
                'dependencies': parsed['deps']
            }
            self.es.index(index=self.index, body=doc)

    def search(self, query, filters=None):
        """
        Search with structural filters

        Example:
        search("仁", filters={'pos': 'NOUN', 'role': 'SUBJECT'})
        """
        # Segment query
        query_words = list(self.segmenter.cut(query))

        # Build Elasticsearch query
        es_query = {
            'bool': {
                'must': [
                    {'match': {'words': ' '.join(query_words)}}
                ]
            }
        }

        # Add structural filters
        if filters:
            if 'pos' in filters:
                es_query['bool']['filter'] = [
                    {'term': {'pos_tags': filters['pos']}}
                ]
            if 'role' in filters:
                es_query['bool']['filter'].append(
                    {'term': {'dependencies.role': filters['role']}}
                )

        # Execute search
        results = self.es.search(
            index=self.index,
            body={'query': es_query},
            size=100
        )

        return self.format_results(results)

    def find_quotations(self, passage, min_length=5):
        """Find passages that quote the given text"""
        # Generate n-grams
        ngrams = self.generate_ngrams(passage, min_length)

        # Search for each n-gram
        quotations = []
        for ngram in ngrams:
            results = self.search(ngram)
            quotations.extend(results)

        # Cluster similar results
        clustered = self.cluster_passages(quotations)

        return clustered

    def semantic_search(self, concept, top_k=50):
        """Find semantically related passages (requires embeddings)"""
        # Get embedding for concept
        query_embedding = self.get_embedding(concept)

        # Vector similarity search
        similar = self.vector_db.search(
            query_embedding,
            top_k=top_k
        )

        return similar

    def temporal_analysis(self, term):
        """Track usage of term across periods"""
        periods = ['pre-qin', 'han', 'tang', 'song', 'ming', 'qing']

        usage = {}
        for period in periods:
            results = self.search(
                term,
                filters={'period': period}
            )
            usage[period] = {
                'count': len(results),
                'texts': [r['title'] for r in results],
                'contexts': [r['context'] for r in results]
            }

        return usage

# Usage examples

search = ClassicalChineseSearch()

# 1. Basic search
results = search.search("君子")

# 2. Structural search: find 仁 used as subject
results = search.search("仁", filters={'pos': 'NOUN', 'role': 'SUBJECT'})

# 3. Find quotations of a passage
passage = "學而時習之不亦說乎"
quotations = search.find_quotations(passage)

# 4. Temporal analysis
usage = search.temporal_analysis("仁")

# 5. Semantic search (Phase 2)
similar = search.semantic_search("道德")
```

## Success Metrics

### Search Quality
- **Precision**: 70%+ of results relevant
- **Recall**: 90%+ of relevant passages found
- **Speed**: <10 seconds for complex queries
- **Coverage**: 95%+ of major classical texts indexed

### Quotation Detection
- **Precision**: 85%+ (low false positive rate)
- **Recall**: 80%+ (find most quotations)
- **Min length**: Detect quotations ≥5 characters

### User Impact
- **Research efficiency**: 5-10x faster passage finding
- **Discovery**: Find connections not discoverable manually
- **Citation quality**: More comprehensive references

## Cost Estimate

### Development
- **Team**: 2 backend engineers + 1 frontend + 1 classical Chinese consultant
- **Duration**: 12-15 months for full product
- **Cost**: $250K-400K

### Infrastructure (annual)
- **Elasticsearch cluster**: $5K-20K/year (depending on scale)
- **Database**: $2K-5K/year
- **Hosting**: $3K-10K/year
- **ctext.org API**: $60-500/year (depending on tier)
- **Total**: $10K-35K/year

### Revenue Models

#### Academic Subscription
- **Institutions**: $500-2,000/year
- **Individuals**: $50-150/year
- **Target**: 50-200 institutions, 500-2000 individuals
- **Revenue**: $50K-500K/year

#### Grant Funding
- **NEH, Mellon, etc.**: $100K-500K for development
- **Sustainability**: Annual grants for maintenance

#### Open Source + Premium
- **Core search**: Free and open source
- **Premium features**: Advanced analytics, API access, bulk export
- **Freemium revenue**: $30K-100K/year

## Risks & Mitigations

### Risk 1: Parsing accuracy limits search quality
**Mitigation**: Focus on high-confidence features first, add advanced parsing gradually

### Risk 2: Index size very large (billions of characters)
**Mitigation**: Efficient indexing strategy, cloud infrastructure for scaling

### Risk 3: User base small and specialized
**Mitigation**: Partner with academic institutions, seek grant funding

### Risk 4: ctext.org API changes or becomes unavailable
**Mitigation**: Cache corpus locally, negotiate long-term API access

### Risk 5: Semantic search requires significant ML expertise
**Mitigation**: Phase 2 feature, can use pre-trained Chinese embeddings initially

## Competitive Landscape

### Existing Tools
- **ctext.org built-in search**: Basic full-text, no structural features
- **Chinese Text Concordance**: Desktop tool, limited corpus
- **MARKUS (MBDB)**: Semi-automatic markup, not full search
- **Google**: Can search classical texts, but no domain-specific features

### Differentiation
- **Structural search**: Unique capability for classical Chinese
- **Quotation detection**: Automated allusion finding
- **Corpus integration**: Comprehensive coverage beyond single sources
- **Research-focused**: Designed for academic use cases

## Real-World Applications

### Scholarly Research
- Tracing evolution of philosophical concepts
- Identifying intertextual relationships
- Compiling comprehensive references for publications

### Translation
- Finding parallel translations of passages
- Understanding variant readings
- Checking authenticity and provenance

### Education
- Teaching about textual relationships
- Demonstrating usage patterns
- Comparing interpretations across periods

## Verdict

**Feasibility**: Medium - Requires significant engineering but builds on existing technology
**Impact**: High - Transforms classical Chinese research capabilities
**Market**: Academic niche but with international reach
**Recommendation**: **Strong candidate for grant-funded academic project** - High scholarly value, sustainable with institutional support, potential for long-term impact on field

**Key success factor**: Partner with established classical Chinese research centers (e.g., Fairbank Center, Academia Sinica) for credibility, user feedback, and sustained funding.
