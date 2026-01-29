# ctext.org API (Comprehensive)

## Architecture

**Type**: Web-based corpus access API with basic NLP features
**Data Source**: Chinese Text Project digital library (~30,000 texts)
**Coverage**: Pre-Qin to Qing dynasty texts

## Detailed Capabilities

### Text Retrieval
- **URN-based access**: Canonical references (e.g., `ctp:analects/xue-er`)
- **Granularity**: Work, chapter, paragraph, or character-level
- **Formats**: JSON, XML, plain text
- **Editions**: Multiple editions of same text available

### Segmentation
- **Character-level**: Always available
- **Word-level**: Basic segmentation provided
- **Quality**: Variable - based on text formatting and punctuation
- **Classical Chinese fit**: Good - designed for pre-modern texts

### Search Capabilities
- **Full-text search**: Across entire corpus or specific works
- **Regex support**: Pattern matching for Classical Chinese
- **Parallel texts**: Search across translations simultaneously
- **Context**: Results include surrounding text for context

### Metadata
- **Author information**: Biographical data
- **Dating**: Text dating (with uncertainty indicators)
- **Categories**: Genre classification (philosophy, history, poetry, etc.)
- **Relationships**: Quotations, references between texts

## API Endpoints

### Core Endpoints
```
GET /gettext        - Retrieve text by URN
GET /searchtexts    - Full-text search
GET /gettextinfo    - Metadata about a text
GET /getanalysis    - Basic linguistic analysis
```

### Example: Retrieve Analects passage
```python
import requests

response = requests.get('https://api.ctext.org/gettext', params={
    'urn': 'ctp:analects/xue-er/1',
    'if': 'en'
})

data = response.json()
# {
#   "text": "子曰：「學而時習之，不亦說乎？」",
#   "translation": "The Master said, \"Is it not pleasant to learn...\""
# }
```

## Pricing Model

### Free Tier
- 100 API calls per day
- Basic text retrieval
- Search functionality

### Academic ($5/month)
- 10,000 API calls per day
- Advanced features
- Priority support

### Commercial (Custom)
- Unlimited API calls
- Bulk data access
- Custom integrations

## Limitations for Parsing

1. **No syntactic analysis**: Does not provide parse trees or dependency graphs
2. **No POS tagging**: Part-of-speech information not available
3. **Basic segmentation only**: Word boundaries are approximate
4. **API dependency**: Requires internet connection
5. **Rate limits**: Free tier may be restrictive for large projects
6. **No offline mode**: Cannot process texts without API access

## Integration Patterns

### As Training Data Source
```python
# Download corpus for training custom parser
def download_corpus(category='confucian-works'):
    texts = []
    # Retrieve text list
    # Download each text
    # Format for training
    return texts
```

### As Reference Database
```python
# Look up historical context
def get_historical_context(character_name):
    results = search_texts(character_name)
    return analyze_occurrences(results)
```

### Combined with Other Tools
```python
# Use ctext for data, Stanford CoreNLP for parsing
text = ctext.get_text('ctp:mencius')
parsed = corenlp.parse(text)  # May be inaccurate
```

## Strengths for Classical Chinese

1. **Authentic sources**: Pre-modern texts, not modern translations
2. **Comprehensive coverage**: Broad range of genres and periods
3. **Easy access**: No installation, works from any language
4. **Well-maintained**: Active development and updates
5. **Community**: Large user base, active forums

## Best Use Cases

- **Corpus building**: Gathering training data for ML models
- **Text research**: Literary analysis, quotation finding
- **Context lookup**: Understanding usage of characters/phrases
- **Parallel texts**: Studying translations
- **Educational tools**: Building learning applications

## Verdict

Essential resource for Classical Chinese text access, but not a parsing solution. Excellent complement to parsing tools as a data source. Best used in combination with other NLP libraries.
