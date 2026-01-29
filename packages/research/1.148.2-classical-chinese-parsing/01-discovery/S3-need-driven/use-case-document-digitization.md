# Use Case: Historical Document Digitization

## Context

**Who**: Libraries, museums, archives, digital humanities projects
**Why**: Millions of historical Chinese documents exist only in physical form or as images. Need to convert to searchable, analyzable digital text.

**Problem Statement**: OCR can extract characters from scanned documents, but raw character sequences are hard to analyze without word boundaries and structure. Need automated parsing to make digitized texts useful for research and preservation.

## User Story

> "As a digital humanities researcher, we have 10,000 scanned pages of Qing dynasty local gazetteers (地方志). OCR gives us character sequences, but to build a searchable database of place names, officials, and events, we need:
> 1. Word segmentation to identify multi-character names and terms
> 2. Named entity recognition to extract person names, place names, titles
> 3. Structural analysis to identify sections (biographies, geography, events)
> 4. Quality metrics to flag OCR errors for manual review"

## Specific Requirements

### Must Have
- **Batch processing**: Process thousands of documents
- **OCR error tolerance**: Handle misrecognized characters gracefully
- **Named entity extraction**: Identify people, places, offices
- **Structured output**: JSON/XML for database ingestion
- **Quality scoring**: Flag low-confidence parses for review

### Nice to Have
- **Period-specific models**: Different models for different dynasties
- **Format preservation**: Maintain original document structure
- **Variant normalization**: Map variant characters to standard forms
- **Automated correction**: Suggest fixes for likely OCR errors

### Not Critical
- **Real-time processing**: Batch processing overnight is acceptable
- **Perfect accuracy**: 80%+ accuracy acceptable with manual review
- **UI**: Command-line or API sufficient

## Data Characteristics

- **Text type**: Historical documents (gazetteers, official records, chronicles)
- **Period**: Wide range (Tang to Qing dynasties)
- **Volume**: Large (millions of characters)
- **Format**: OCR output, potentially with errors (5-15% character error rate)
- **Structure**: Mixed text, tables, lists

## Accuracy Requirements

- **Segmentation**: 80%+ (will be manually reviewed)
- **NER**: 70%+ recall (better to over-extract than miss entities)
- **OCR error detection**: 60%+ (flagging for human review)
- **Structure extraction**: 85%+ (critical for usability)

## Recommended Solution

### Architecture

```
Scanned Documents
  ↓
OCR (Tesseract + Chinese models)
  ↓
Raw Character Sequences (with errors)
  ↓
Preprocessing
  - Detect OCR confidence scores
  - Identify section headers
  - Extract metadata (page numbers, document IDs)
  ↓
Jiayan Segmentation (with error tolerance)
  ↓
NER Pipeline
  - Historical name gazetteer
  - Pattern matching (官职, 地名 patterns)
  - ML-based NER (trained on historical texts)
  ↓
Quality Assessment
  - Flag low confidence segments
  - Identify likely OCR errors
  ↓
Structured Output (JSON/XML)
  ↓
Database Ingestion + Manual Review Queue
```

### Tech Stack

- **OCR**: Tesseract 4+ with chi_tra/chi_sim models
- **Preprocessing**: Python + custom rules
- **Segmentation**: Jiayan (modified for error tolerance)
- **NER**:
  - Gazetteers from CBDB (China Biographical Database)
  - Custom CRF model trained on historical texts
  - Pattern matching for titles/offices
- **Database**: PostgreSQL with full-text search
- **Review interface**: Web UI for manual correction

### Implementation Time

- **Phase 1 (OCR + segmentation)**: 1-2 months
- **Phase 2 (NER)**: 3-4 months
- **Phase 3 (Quality assessment)**: 2 months
- **Total**: 6-10 months

## Example Implementation

```python
import jiayan
import tesseract
import re
from historical_ner import HistoricalNER

class DocumentDigitizer:
    def __init__(self):
        self.segmenter = jiayan.load()
        self.ner = HistoricalNER()
        self.gazetteers = self.load_gazetteers()

    def process_document(self, image_path):
        # Step 1: OCR
        ocr_result = tesseract.image_to_data(
            image_path,
            lang='chi_tra',
            output_type=tesseract.Output.DICT
        )

        # Extract text and confidence scores
        text = ocr_result['text']
        confidences = ocr_result['conf']

        # Step 2: Preprocess
        sections = self.identify_sections(text)

        # Step 3: Segment
        words = list(self.segmenter.cut(text))

        # Step 4: NER
        entities = self.extract_entities(words)

        # Step 5: Quality assessment
        quality_flags = self.assess_quality(
            words, confidences, entities
        )

        # Step 6: Structure output
        return {
            'document_id': self.extract_id(image_path),
            'sections': sections,
            'entities': {
                'people': entities['PER'],
                'places': entities['LOC'],
                'offices': entities['OFF']
            },
            'quality_score': self.calculate_score(quality_flags),
            'review_needed': quality_flags['needs_review']
        }

    def extract_entities(self, words):
        entities = {'PER': [], 'LOC': [], 'OFF': []}

        # Gazetteer lookup
        for i, word in enumerate(words):
            if word in self.gazetteers['people']:
                entities['PER'].append((word, i))
            elif word in self.gazetteers['places']:
                entities['LOC'].append((word, i))

        # Pattern matching for titles
        title_patterns = [
            r'知.*府', r'.*尚书', r'.*大夫', r'.*侍郎'
        ]
        text = ''.join(words)
        for pattern in title_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                entities['OFF'].append((match.group(), match.start()))

        # ML-based NER for remaining
        ml_entities = self.ner.predict(words)
        entities = self.merge_entities(entities, ml_entities)

        return entities

    def assess_quality(self, words, confidences, entities):
        flags = {
            'low_confidence_chars': [],
            'probable_errors': [],
            'entity_conflicts': [],
            'needs_review': False
        }

        # Flag low confidence OCR
        for i, conf in enumerate(confidences):
            if conf < 70:
                flags['low_confidence_chars'].append(i)

        # Check for impossible character sequences
        # ... more quality checks

        flags['needs_review'] = (
            len(flags['low_confidence_chars']) > 10 or
            len(flags['probable_errors']) > 5
        )

        return flags

    def load_gazetteers(self):
        # Load historical name databases
        # CBDB for person names
        # Historical place name databases
        return gazetteers

# Usage for batch processing
digitizer = DocumentDigitizer()
for doc in document_collection:
    result = digitizer.process_document(doc)
    if result['review_needed']:
        queue_for_review(result)
    else:
        ingest_to_database(result)
```

## Success Metrics

### Efficiency
- **Processing speed**: 100-500 pages/hour (depending on quality)
- **Manual review reduction**: 70% of documents auto-processed
- **Entity extraction recall**: 75%+ for names, 80%+ for places

### Quality
- **Segmentation accuracy**: 85%+ on clean OCR, 75%+ on noisy OCR
- **NER precision**: 80%+ (low false positive rate)
- **OCR error detection**: 70%+ of errors flagged

### Project Impact
- **Digitization speed**: 5-10x faster than fully manual
- **Cost reduction**: 60-80% lower cost per page
- **Searchability**: 95%+ of entities findable

## Cost Estimate

### Development
- **Team**: 2 engineers + 1 historian consultant
- **Duration**: 10 months
- **Cost**: $150K-250K

### Infrastructure (annual)
- **OCR processing**: GPU servers or cloud ($2K-10K/year depending on volume)
- **Storage**: $1K-5K/year for millions of pages
- **Database**: $5K-15K/year
- **Total**: $8K-30K/year

### Per-Document Costs
- **Automated processing**: $0.01-0.05 per page
- **Manual review**: $1-3 per page (when needed)
- **Fully manual**: $5-15 per page
- **Savings**: 70-90% cost reduction

## Risks & Mitigations

### Risk 1: OCR quality varies widely by document condition
**Mitigation**: Pre-assess document quality, route low-quality docs directly to manual processing

### Risk 2: Historical terminology varies by period and region
**Mitigation**: Build period-specific models, maintain region-specific gazetteers

### Risk 3: Rare entity types not in training data
**Mitigation**: Active learning - add frequently-corrected entities to gazetteers

### Risk 4: Format variations hard to handle automatically
**Mitigation**: Template-based extraction for known formats, flag unusual formats for review

## Real-World Projects

### Existing Examples
- **CBDB (China Biographical Database)**: Thousands of digitized biographies
- **CHGIS (China Historical GIS)**: Historical place names database
- **ctext.org**: 30,000+ digitized classical texts
- **National Library of China**: Massive digitization efforts

### Lessons Learned
1. Manual review is always needed - aim to minimize, not eliminate
2. Domain expertise critical - partner with historians
3. Start with high-quality documents, expand to difficult ones
4. Gazetteers are invaluable - invest in building comprehensive lists
5. Version control critical - texts improve over time with corrections

## Competitive Landscape

### Commercial Solutions
- **ABBYY FineReader**: Good OCR, limited Classical Chinese NER
- **Google Cloud Vision**: General OCR, no historical Chinese features
- **Custom academic tools**: Often project-specific, not generalizable

### Market Opportunity
- Large unmet need in digital humanities
- Growing interest in Chinese historical research globally
- Funding available from cultural preservation initiatives
- Could be open-sourced with institutional sponsorship

## Verdict

**Feasibility**: Medium-High - requires significant development but achievable
**Impact**: Very High - enables large-scale digital humanities research
**Market**: Grant-funded or institutional projects
**Recommendation**: **Viable for dedicated project with institutional backing** - combines technical challenge with significant cultural preservation value
