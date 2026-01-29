# ctext.org API

## Overview

The Chinese Text Project (ctext.org) is a digital library providing comprehensive access to pre-modern Chinese texts. The API provides programmatic access to Classical Chinese texts, metadata, and basic text analysis capabilities.

## Classical Chinese Support

**Status**: Native Classical Chinese support

- **Corpus Access**: Direct access to thousands of pre-modern Chinese texts
- **Text Retrieval**: Retrieve texts by work, chapter, or passage
- **Basic Analysis**: Character frequency, text search, and basic segmentation
- **Metadata**: Author, date, text category information

## Key Features

- Massive Classical Chinese corpus (thousands of works)
- RESTful API with JSON responses
- Text retrieval by URN (Uniform Resource Name)
- Character-level and basic word-level segmentation
- Full-text search capabilities
- Traditional and Simplified character support

## Strengths

- **Authentic Classical Chinese**: Texts are pre-modern sources
- **Comprehensive corpus**: Extensive coverage of classical literature
- **Easy access**: Simple HTTP API, no complex installation
- **Free tier available**: Basic access without authentication
- **Well-documented**: Clear API documentation with examples

## Limitations for Parsing

- **Limited NLP**: Not a full parsing toolkit
- **No dependency parsing**: No syntactic analysis beyond segmentation
- **No POS tagging**: Part-of-speech information not provided
- **API-dependent**: Requires internet connection and API availability
- **Rate limits**: Free tier has usage restrictions

## Availability

- **Website**: https://ctext.org/tools/api
- **API Endpoint**: https://api.ctext.org/
- **License**: Various (depends on text, API terms of service)
- **Authentication**: Optional (free tier available, paid tiers for higher limits)

## Initial Assessment

Excellent resource for Classical Chinese corpus access, but not a parsing toolkit. Best used as a data source for text retrieval and research. Would need to be combined with other tools for syntactic analysis.

## API Example

```python
import requests

# Get text from the Analects
response = requests.get('https://api.ctext.org/gettext', params={
    'urn': 'ctp:analects/xue-er',
    'if': 'en'
})

data = response.json()
# Returns text with English translation
```
