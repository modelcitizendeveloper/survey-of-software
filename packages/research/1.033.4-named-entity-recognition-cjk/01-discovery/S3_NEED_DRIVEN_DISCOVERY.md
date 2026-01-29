# S3: NEED-DRIVEN DISCOVERY
## Named Entity Recognition for CJK Languages - Generic Use Case Patterns

**Discovery Date**: 2026-01-29
**Focus**: Matching CJK NER solutions to common business application patterns and constraints
**Methodology**: Solution-first analysis mapping libraries to parameterized use case categories

---

## Executive Summary

This discovery maps CJK NER solutions to five common business application patterns, providing implementation blueprints for typical scenarios:

- **Pattern #1 (International Business Intelligence)**: HanLP BERT for Chinese competitor monitoring achieves 95% accuracy, self-hosted for data sovereignty
- **Pattern #2 (Cross-Border E-Commerce)**: LTP fast CPU inference (<100ms) for real-time address parsing and customer data extraction
- **Pattern #3 (Legal/Compliance Processing)**: Stanza multi-language for contract analysis across Chinese, Japanese, Korean jurisdictions
- **Pattern #4 (Social Media Monitoring)**: Cloud APIs (Google/Azure) for variable-volume brand mentions, influencer tracking
- **Pattern #5 (Customer Data Normalization)**: Hybrid architecture for CRM deduplication and entity resolution at scale

**Implementation Roadmap**: Week 1 cloud API prototype, Month 1 self-hosted deployment, Month 3 domain-specific fine-tuning

---

## Use Case Pattern #1: International Business Intelligence and Competitor Monitoring

### Generic Requirements Profile
- **Scenario**: Monitor Chinese/Japanese/Korean news, social media, regulatory filings for competitor activities, M&A, product launches
- **Constraints**: Data sovereignty required (China regulations), high accuracy critical (95%+ for company/executive names), Traditional + Simplified Chinese
- **Volume**: 10K-100K articles/day, batch processing acceptable (not real-time)
- **Priority**: Accuracy over speed, false negatives more costly than false positives

### Example Application Domains
- Competitive intelligence platforms monitoring Asian markets
- Investment research firms tracking Chinese companies
- Market analysis tools for Japan/Korea business environment
- Regulatory compliance monitoring (CSRC, FSA Japan, FSC Korea filings)

### Recommended Solution: HanLP BERT (Self-Hosted GPU)

**Primary Approach**: HanLP MSRA_NER_BERT_BASE_ZH for Chinese, Stanza for Japanese/Korean

#### Why This Solution?
1. **State-of-Art Accuracy**: 95.5% F1 on MSRA benchmark, 10-15% better than generic models for Chinese entities
2. **Traditional/Simplified Support**: Native dual-script handling without conversion preprocessing
3. **Data Sovereignty**: Self-hosted deployment complies with China data localization laws
4. **Domain Adaptability**: Fine-tuning on financial/business terminology achieves 97%+ accuracy
5. **Batch Processing Optimized**: GPU throughput 500-1,000 docs/hour, suitable for overnight processing

#### Technical Implementation

```python
import hanlp
from typing import List, Dict
import json

# Load models (one-time setup)
ner_zh = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

# Fine-tune on domain-specific data (optional, +5-10% accuracy)
# custom_ner = hanlp.pretrain.ner.TransformerNamedEntityRecognizer()
# custom_ner.fit(train_data='financial_entities_train.conll', epochs=10)

class IntelligencePipeline:
    def __init__(self, entity_database_path='entity_db.json'):
        self.ner_zh = ner_zh
        # Load entity database for linking (companies, executives, products)
        with open(entity_database_path) as f:
            self.entity_db = json.load(f)

    def extract_intelligence(self, article: Dict) -> Dict:
        """
        Extract entities from article and link to known companies/people

        Args:
            article: {
                'text': str,
                'language': 'zh'/'zh-TW'/'ja'/'ko',
                'source': str,
                'date': str
            }

        Returns:
            {
                'entities': [{'text', 'type', 'canonical_id', 'confidence'}],
                'mentions': {'companies': [...], 'executives': [...], 'locations': [...]},
                'insights': {
                    'competitor_activities': [...],
                    'market_signals': [...]
                }
            }
        """
        text = article['text']
        language = article['language']

        # Entity extraction
        if language in ['zh', 'zh-TW']:
            # Handle Traditional Chinese (convert if needed)
            if language == 'zh-TW':
                text = self._convert_traditional_to_simplified(text)

            entities = self.ner_zh(text)
        else:
            # Fallback to Stanza for Japanese/Korean
            entities = self._extract_other_languages(text, language)

        # Entity linking (resolve to canonical IDs)
        linked_entities = self._link_entities(entities, language)

        # Categorize mentions
        mentions = self._categorize_mentions(linked_entities)

        # Extract insights
        insights = self._extract_insights(linked_entities, article)

        return {
            'entities': linked_entities,
            'mentions': mentions,
            'insights': insights,
            'metadata': {
                'source': article['source'],
                'date': article['date'],
                'language': language
            }
        }

    def _link_entities(self, entities, language):
        """Link extracted entities to canonical database"""
        linked = []
        for entity in entities:
            entity_text = entity[0] if isinstance(entity, tuple) else entity['text']
            entity_type = entity[1] if isinstance(entity, tuple) else entity['type']

            # Lookup in entity database
            canonical = self._lookup_entity(entity_text, entity_type, language)

            linked.append({
                'text': entity_text,
                'type': entity_type,
                'canonical_id': canonical['id'] if canonical else None,
                'canonical_name': canonical['name'] if canonical else entity_text,
                'confidence': canonical['confidence'] if canonical else 0.8
            })

        return linked

    def _lookup_entity(self, text, entity_type, language):
        """Lookup entity in database by text, type, language"""
        # Normalize text
        normalized = text.lower().strip()

        # Search entity database
        for entity_id, entity_data in self.entity_db.items():
            if entity_data['type'] != entity_type:
                continue

            # Check aliases for this language
            if language in entity_data.get('aliases', {}):
                aliases = [a.lower() for a in entity_data['aliases'][language]]
                if normalized in aliases:
                    return {
                        'id': entity_id,
                        'name': entity_data['canonical_name'],
                        'confidence': 0.95
                    }

        return None

    def _categorize_mentions(self, entities):
        """Categorize entities by type for intelligence reporting"""
        mentions = {
            'companies': [],
            'executives': [],
            'locations': [],
            'products': []
        }

        for entity in entities:
            if entity['type'] == 'ORGANIZATION':
                mentions['companies'].append({
                    'name': entity['canonical_name'],
                    'id': entity['canonical_id'],
                    'confidence': entity['confidence']
                })
            elif entity['type'] == 'PERSON':
                mentions['executives'].append({
                    'name': entity['canonical_name'],
                    'id': entity['canonical_id'],
                    'confidence': entity['confidence']
                })
            elif entity['type'] in ['LOCATION', 'GPE']:
                mentions['locations'].append({
                    'name': entity['canonical_name'],
                    'id': entity['canonical_id'],
                    'confidence': entity['confidence']
                })

        return mentions

    def _extract_insights(self, entities, article):
        """Extract business insights from entity co-occurrences"""
        insights = {
            'competitor_activities': [],
            'market_signals': []
        }

        # Example: Detect M&A signals (company + "acquisition", "merger" keywords)
        if any(e['type'] == 'ORGANIZATION' for e in entities):
            if '收购' in article['text'] or '合并' in article['text'] or 'acquisition' in article['text'].lower():
                companies = [e for e in entities if e['type'] == 'ORGANIZATION']
                insights['competitor_activities'].append({
                    'type': 'M&A_SIGNAL',
                    'companies': [c['canonical_name'] for c in companies],
                    'confidence': 0.7,
                    'source': article['source']
                })

        # Example: Detect executive movements (person + company + "joined", "appointed")
        executives = [e for e in entities if e['type'] == 'PERSON']
        companies = [e for e in entities if e['type'] == 'ORGANIZATION']

        if executives and companies:
            if '加入' in article['text'] or '任命' in article['text'] or 'appointed' in article['text'].lower():
                insights['competitor_activities'].append({
                    'type': 'EXECUTIVE_MOVEMENT',
                    'person': executives[0]['canonical_name'],
                    'company': companies[0]['canonical_name'],
                    'confidence': 0.8
                })

        return insights

# Usage: Process daily news batch
pipeline = IntelligencePipeline(entity_database_path='financial_entities.json')

# Load articles from news crawlers
articles = load_daily_articles()  # [{text, language, source, date}, ...]

results = []
for article in articles:
    try:
        intel = pipeline.extract_intelligence(article)
        results.append(intel)
    except Exception as e:
        print(f"Error processing article from {article['source']}: {e}")

# Generate daily intelligence report
report = generate_intelligence_report(results)
# Report includes: Top mentioned companies, executive movements, M&A signals, market trends
```

#### Production Deployment

**Infrastructure**:
- **GPU Server**: AWS g4dn.xlarge or Azure NC6s_v3 ($400-500/month)
- **Storage**: S3/Azure Blob for raw articles and processed data ($50-100/month)
- **Database**: PostgreSQL for entity database and intelligence records ($100-200/month)
- **Total Cost**: ~$600-800/month for processing 50K-100K articles/day

**Processing Pipeline**:
1. **Overnight batch**: Crawl news/social media articles (scheduled job)
2. **Entity extraction**: Process with HanLP NER (4-8 hours for 50K articles on single GPU)
3. **Entity linking**: Resolve entities to canonical database (1-2 hours)
4. **Insight generation**: Detect patterns, generate alerts (30 minutes)
5. **Reporting**: Email/dashboard with daily intelligence digest (manual review)

**Expected Impact**:
- 90% reduction in analyst time for initial article screening
- 5-10x faster identification of competitor activities
- 95%+ recall on critical entities (companies, executives)
- ROI: $50K-100K/year in analyst time savings

---

## Use Case Pattern #2: Cross-Border E-Commerce Address Parsing and Customer Data Extraction

### Generic Requirements Profile
- **Scenario**: Extract customer names, addresses, company names from multilingual order forms, shipping documents, invoices
- **Constraints**: Real-time processing (<500ms per order), cost-sensitive (millions of orders/month), CPU-only deployment preferred
- **Volume**: 100K-1M orders/day, continuous stream processing
- **Priority**: Speed and cost over accuracy (90%+ acceptable if fast), automated validation for low-confidence cases

### Example Application Domains
- International e-commerce platforms (Alibaba, Rakuten, Coupang integrations)
- Cross-border logistics and fulfillment systems
- Payment processing for Asian markets
- International shipping label generation

### Recommended Solution: LTP (Fast CPU Inference)

**Primary Approach**: LTP v4 for Chinese, spaCy or Stanza for Japanese/Korean

#### Why This Solution?
1. **Fast CPU Inference**: 50-100ms per order (10-20 orders/sec per CPU core)
2. **Cost-Effective**: No GPU required, standard CPU servers ($150-300/month for high volume)
3. **Good Accuracy**: 90-93% F1 sufficient for e-commerce (validation catches errors)
4. **Integrated Pipeline**: Word segmentation + NER in single pass
5. **Production-Proven**: Used by major Chinese e-commerce platforms

#### Technical Implementation

```python
from ltp import LTP
import re
from typing import Dict, List, Optional

ltp = LTP()  # Load LTP model

class AddressParser:
    def __init__(self):
        self.ltp = ltp
        # Common address patterns (regex for validation)
        self.address_patterns = {
            'zh': [
                r'([\u4e00-\u9fa5]+[省市区县])',  # Province/City/District
                r'([\u4e00-\u9fa5]+[路街道巷弄])',  # Road/Street
                r'(\d+号楼?)',  # Building number
            ],
            'jp': [r'[都道府県]', r'[市区町村]'],
            'kr': [r'[시도]', r'[구군]']
        }

    def parse_order(self, order_data: Dict) -> Dict:
        """
        Extract customer name, address, company from order data

        Args:
            order_data: {
                'customer_input': str,  # Free-form customer input
                'language': 'zh'/'ja'/'ko',
                'order_id': str
            }

        Returns:
            {
                'customer_name': str,
                'company_name': Optional[str],
                'address': {
                    'country': str,
                    'province': str,
                    'city': str,
                    'district': str,
                    'street': str,
                    'building': str,
                    'unit': str
                },
                'confidence': float,  # Overall confidence
                'validation_required': bool  # Manual review needed?
            }
        """
        text = order_data['customer_input']
        language = order_data['language']

        # Extract entities
        if language == 'zh':
            result = self.ltp.pipeline([text], tasks=["cws", "ner"])
            entities = self._parse_ltp_entities(result.ner[0], result.cws[0])
        else:
            # Fallback for other languages
            entities = self._extract_other(text, language)

        # Extract structured fields
        customer_name = self._find_customer_name(entities)
        company_name = self._find_company_name(entities)
        address_components = self._parse_address(text, entities, language)

        # Calculate confidence
        confidence = self._calculate_confidence(entities, address_components)

        return {
            'customer_name': customer_name,
            'company_name': company_name,
            'address': address_components,
            'confidence': confidence,
            'validation_required': confidence < 0.85,  # Manual review if low confidence
            'entities': entities  # For debugging
        }

    def _parse_ltp_entities(self, ner_tags, words):
        """Convert LTP NER tags to entity list"""
        entities = []
        current_entity = None
        current_type = None

        for i, (word, tag) in enumerate(zip(words, ner_tags)):
            if tag[0] == 'B':  # Begin entity
                if current_entity:
                    entities.append({'text': current_entity, 'type': current_type})
                current_entity = word
                current_type = tag[2:]  # Remove B- prefix
            elif tag[0] == 'I' and current_entity:  # Inside entity
                current_entity += word
            else:  # Outside entity
                if current_entity:
                    entities.append({'text': current_entity, 'type': current_type})
                    current_entity = None
                    current_type = None

        if current_entity:
            entities.append({'text': current_entity, 'type': current_type})

        # Map LTP tags to standard tags
        # Ni -> ORGANIZATION, Nh -> PERSON, Ns -> LOCATION
        tag_map = {'Ni': 'ORGANIZATION', 'Nh': 'PERSON', 'Ns': 'LOCATION'}
        for entity in entities:
            entity['type'] = tag_map.get(entity['type'], entity['type'])

        return entities

    def _find_customer_name(self, entities):
        """Extract customer name (first PERSON entity)"""
        for entity in entities:
            if entity['type'] == 'PERSON':
                return entity['text']
        return None

    def _find_company_name(self, entities):
        """Extract company name (first ORGANIZATION entity)"""
        for entity in entities:
            if entity['type'] == 'ORGANIZATION':
                return entity['text']
        return None

    def _parse_address(self, text, entities, language):
        """Parse address components from text and entities"""
        address = {
            'country': None,
            'province': None,
            'city': None,
            'district': None,
            'street': None,
            'building': None,
            'unit': None
        }

        # Extract location entities
        locations = [e for e in entities if e['type'] == 'LOCATION']

        if language == 'zh':
            # Chinese address pattern: Province City District Street Building Unit
            for loc in locations:
                if '省' in loc['text']:
                    address['province'] = loc['text']
                elif '市' in loc['text']:
                    address['city'] = loc['text']
                elif '区' in loc['text'] or '县' in loc['text']:
                    address['district'] = loc['text']
                elif '路' in loc['text'] or '街' in loc['text']:
                    address['street'] = loc['text']

            # Extract building/unit numbers with regex
            building_match = re.search(r'(\d+号楼?)', text)
            if building_match:
                address['building'] = building_match.group(1)

            unit_match = re.search(r'(\d+单元)', text)
            if unit_match:
                address['unit'] = unit_match.group(1)

        # TODO: Japanese and Korean address patterns

        return address

    def _calculate_confidence(self, entities, address_components):
        """Calculate overall confidence score"""
        confidence = 0.5  # Base confidence

        # Boost for key entities found
        if any(e['type'] == 'PERSON' for e in entities):
            confidence += 0.2
        if any(e['type'] == 'LOCATION' for e in entities):
            confidence += 0.2

        # Boost for address components
        filled_components = sum(1 for v in address_components.values() if v is not None)
        confidence += (filled_components / 7) * 0.3  # Up to 0.3 for complete address

        return min(confidence, 1.0)

# Usage: Real-time order processing
parser = AddressParser()

# Streaming order processing (e.g., from Kafka)
def process_order_stream():
    while True:
        order = consume_order_from_queue()  # {customer_input, language, order_id}

        try:
            parsed = parser.parse_order(order)

            if parsed['validation_required']:
                # Send to manual validation queue
                send_to_validation_queue(order['order_id'], parsed)
            else:
                # Auto-approve and process order
                process_order(order['order_id'], parsed)

        except Exception as e:
            # Handle errors gracefully
            send_to_error_queue(order['order_id'], str(e))

# Batch processing mode (for backlog)
orders = load_orders_batch(limit=10000)
results = [parser.parse_order(order) for order in orders]

# Statistics
auto_approved = sum(1 for r in results if not r['validation_required'])
print(f"Auto-approved: {auto_approved}/{len(results)} ({auto_approved/len(results)*100:.1f}%)")
```

#### Production Deployment

**Infrastructure**:
- **CPU Servers**: 3x t3.2xlarge (8 vCPU, 32GB RAM) with load balancer ($900/month total)
- **Throughput**: 60-120 orders/sec per server, 180-360 orders/sec total
- **Latency**: 50-100ms per order (p95)
- **Availability**: 99.9% with 3-node HA setup

**Processing Flow**:
1. **Order ingestion**: Kafka queue receives orders from web/mobile app
2. **NER extraction**: LTP processes customer input, extracts entities
3. **Address parsing**: Structured address components extracted
4. **Confidence scoring**: Automated confidence assessment
5. **Routing**: High-confidence → auto-process, Low-confidence → manual validation queue
6. **Validation**: Human review for 10-15% of orders flagged as uncertain

**Expected Impact**:
- 85-90% of orders auto-processed without manual review
- 50-100ms latency enables real-time checkout experience
- $150-300/month infrastructure cost (vs $2,000-4,000/month for cloud APIs at this volume)
- ROI: $500K-1M/year in manual data entry cost savings at 1M orders/month scale

---

## Use Case Pattern #3: Legal and Compliance Contract Analysis (Multi-Jurisdiction)

### Generic Requirements Profile
- **Scenario**: Extract parties, obligations, locations, dates from contracts in Chinese, Japanese, Korean for legal review and compliance
- **Constraints**: Multi-language consistency critical, high precision required (false positives costly), human-in-loop for verification
- **Volume**: 1K-10K contracts/month, batch processing acceptable
- **Priority**: Accuracy and consistency over speed, multi-language unified output format

### Example Application Domains
- International law firms handling Asian contracts
- Corporate compliance teams processing supplier agreements
- M&A due diligence document review
- Regulatory filing analysis (CSRC, SEC, FSA)

### Recommended Solution: Stanza (Multi-Language Unified API)

**Primary Approach**: Stanza with unified pipeline for Chinese, Japanese, Korean

#### Why This Solution?
1. **Multi-Language Consistency**: Same API and output format across all CJK languages
2. **Academic Quality**: Stanford NLP credibility important for legal applications
3. **Good Accuracy**: 88-92% F1 across languages, sufficient with human review
4. **Customizable**: Fine-tuning on legal terminology improves accuracy to 92-95%
5. **Transparent**: Clear model provenance and methodology for legal compliance

#### Technical Implementation

```python
import stanza
from typing import List, Dict
import json
from datetime import datetime

# Download and initialize models
stanza.download('zh')
stanza.download('ja')
stanza.download('ko')

nlp_zh = stanza.Pipeline('zh', processors='tokenize,ner')
nlp_ja = stanza.Pipeline('ja', processors='tokenize,ner')
nlp_ko = stanza.Pipeline('ko', processors='tokenize,ner')

class ContractAnalyzer:
    def __init__(self):
        self.nlp_models = {
            'zh': nlp_zh,
            'ja': nlp_ja,
            'ko': nlp_ko
        }
        # Legal entity types
        self.legal_entity_types = ['PERSON', 'ORGANIZATION', 'GPE', 'DATE', 'MONEY', 'LAW']

    def analyze_contract(self, contract: Dict) -> Dict:
        """
        Extract legal entities from contract for review

        Args:
            contract: {
                'text': str,
                'language': 'zh'/'ja'/'ko',
                'contract_id': str,
                'contract_type': 'NDA'/'SLA'/'Purchase Agreement'/etc.
            }

        Returns:
            {
                'contract_id': str,
                'language': str,
                'parties': [{'name', 'type', 'role'}],  # Contracting parties
                'obligations': [{'party', 'obligation', 'deadline'}],
                'locations': [{'location', 'context'}],  # Jurisdictions
                'dates': [{'date', 'context'}],  # Effective dates, deadlines
                'amounts': [{'amount', 'currency', 'context'}],
                'entities_raw': [...],  # All extracted entities
                'confidence': float,
                'review_flags': [...]  # Potential issues for manual review
            }
        """
        text = contract['text']
        language = contract['language']

        # Extract entities
        nlp = self.nlp_models[language]
        doc = nlp(text)

        # Convert Stanza entities to structured format
        entities = []
        for ent in doc.entities:
            entities.append({
                'text': ent.text,
                'type': ent.type,
                'start': ent.start_char,
                'end': ent.end_char
            })

        # Extract legal-specific fields
        parties = self._extract_parties(entities, text)
        locations = self._extract_locations(entities, text)
        dates = self._extract_dates(entities, text)
        amounts = self._extract_amounts(entities, text)

        # Identify obligations (keyword-based + entity context)
        obligations = self._extract_obligations(text, parties)

        # Quality checks
        review_flags = self._quality_check(parties, locations, dates, contract)

        # Confidence scoring
        confidence = self._calculate_contract_confidence(entities, parties, locations)

        return {
            'contract_id': contract['contract_id'],
            'language': language,
            'contract_type': contract['contract_type'],
            'parties': parties,
            'obligations': obligations,
            'locations': locations,
            'dates': dates,
            'amounts': amounts,
            'entities_raw': entities,
            'confidence': confidence,
            'review_flags': review_flags,
            'processed_at': datetime.now().isoformat()
        }

    def _extract_parties(self, entities, text):
        """Extract contracting parties (organizations and persons)"""
        parties = []

        # Look for organizations and persons near "甲方/乙方" (Party A/B in Chinese)
        # or "当事者" (parties in Japanese), "당사자" (parties in Korean)
        party_keywords = {
            'zh': ['甲方', '乙方', '丙方', '买方', '卖方', '承包方', '发包方'],
            'ja': ['甲', '乙', '買主', '売主', '当事者'],
            'kr': ['갑', '을', '당사자']
        }

        for entity in entities:
            if entity['type'] in ['ORGANIZATION', 'PERSON']:
                # Determine role by checking context
                role = self._determine_party_role(entity, text)

                parties.append({
                    'name': entity['text'],
                    'type': entity['type'],
                    'role': role  # 'Party A', 'Party B', 'Buyer', 'Seller', etc.
                })

        return parties

    def _determine_party_role(self, entity, text):
        """Determine party role based on context"""
        # Check if entity appears near party keywords
        entity_text = entity['text']
        start = entity['start']

        # Context window (50 characters before entity)
        context_start = max(0, start - 50)
        context = text[context_start:start]

        if '甲方' in context or '买方' in context:
            return 'Party A (Buyer)'
        elif '乙方' in context or '卖方' in context:
            return 'Party B (Seller)'
        else:
            return 'Unknown Role'

    def _extract_locations(self, entities, text):
        """Extract locations (jurisdictions, governing law)"""
        locations = []

        for entity in entities:
            if entity['type'] in ['GPE', 'LOCATION']:
                # Context: Look for jurisdiction keywords nearby
                context = self._get_entity_context(entity, text)

                locations.append({
                    'location': entity['text'],
                    'context': context
                })

        return locations

    def _extract_dates(self, entities, text):
        """Extract dates (effective date, expiration, deadlines)"""
        dates = []

        for entity in entities:
            if entity['type'] == 'DATE':
                context = self._get_entity_context(entity, text)

                dates.append({
                    'date': entity['text'],
                    'context': context
                })

        return dates

    def _extract_amounts(self, entities, text):
        """Extract monetary amounts (contract value, penalties)"""
        amounts = []

        for entity in entities:
            if entity['type'] == 'MONEY':
                context = self._get_entity_context(entity, text)

                amounts.append({
                    'amount': entity['text'],
                    'context': context
                })

        return amounts

    def _extract_obligations(self, text, parties):
        """Extract obligations (keyword-based pattern matching)"""
        obligations = []

        # Obligation keywords by language
        obligation_patterns = {
            'zh': ['应当', '必须', '承诺', '负责', '保证', '义务'],
            'ja': ['義務', '責任', 'べき', '保証'],
            'kr': ['의무', '책임', '보증']
        }

        # Simple pattern: Find obligation keywords and associate with nearest party
        # (Real implementation would use dependency parsing for more accuracy)

        return obligations

    def _get_entity_context(self, entity, text, window=100):
        """Get surrounding context for entity"""
        start = max(0, entity['start'] - window)
        end = min(len(text), entity['end'] + window)
        return text[start:end]

    def _quality_check(self, parties, locations, dates, contract):
        """Flag potential issues for manual review"""
        flags = []

        if len(parties) == 0:
            flags.append("NO_PARTIES_FOUND")
        elif len(parties) == 1:
            flags.append("ONLY_ONE_PARTY_FOUND")

        if len(locations) == 0:
            flags.append("NO_JURISDICTION_FOUND")

        if len(dates) == 0:
            flags.append("NO_DATES_FOUND")

        return flags

    def _calculate_contract_confidence(self, entities, parties, locations):
        """Calculate confidence score"""
        confidence = 0.5

        if len(parties) >= 2:
            confidence += 0.2
        if len(locations) >= 1:
            confidence += 0.15
        if len(entities) >= 10:  # Sufficient entities extracted
            confidence += 0.15

        return min(confidence, 1.0)

# Usage: Batch contract processing
analyzer = ContractAnalyzer()

contracts = load_contracts_from_database(limit=100)
# [{text, language, contract_id, contract_type}, ...]

results = []
for contract in contracts:
    try:
        analysis = analyzer.analyze_contract(contract)
        results.append(analysis)

        # Store in database for legal review interface
        store_contract_analysis(analysis)
    except Exception as e:
        print(f"Error analyzing contract {contract['contract_id']}: {e}")

# Generate review report
report = generate_review_report(results)
# Flag high-risk contracts, missing information, inconsistencies
```

#### Production Deployment

**Infrastructure**:
- **CPU Server**: c5.2xlarge (8 vCPU, 16GB RAM) for batch processing ($250/month)
- **Processing**: 50-100 contracts/hour (depends on contract length)
- **Storage**: PostgreSQL for contract analysis results ($100/month)
- **Review Interface**: Web app for legal team review ($200/month hosting)
- **Total Cost**: ~$600/month

**Workflow**:
1. **Upload**: Legal team uploads contracts (PDF/DOCX) → OCR if needed
2. **NER Extraction**: Stanza processes contract text, extracts entities
3. **Structuring**: Parties, obligations, dates, locations structured into fields
4. **Quality Check**: Automated flags for missing information or anomalies
5. **Manual Review**: Legal team reviews flagged contracts, corrects errors
6. **Database**: Verified contract data stored for compliance reporting

**Expected Impact**:
- 70-80% reduction in time for initial contract review (highlighting key entities)
- 90%+ accuracy with human-in-loop verification
- Unified workflow across Chinese, Japanese, Korean contracts
- ROI: $100K-300K/year in legal team time savings for firms handling 1K+ contracts/year

---

## Use Case Pattern #4: Social Media and Brand Monitoring Across CJK Platforms

### Generic Requirements Profile
- **Scenario**: Monitor mentions of brands, products, competitors, influencers on Weibo, RED (小红书), LINE, KakaoTalk, etc.
- **Constraints**: Variable volume (spikes during campaigns), multi-platform APIs, need managed service reliability
- **Volume**: 10K-500K posts/day (highly variable), real-time preferred (<5 min latency)
- **Priority**: Reliability and ease of integration over cost, need multi-language support

### Example Application Domains
- Brand reputation monitoring across Asian markets
- Influencer marketing campaign tracking
- Customer sentiment analysis for product launches
- Competitor intelligence on social platforms

### Recommended Solution: Cloud APIs (Google Cloud or Azure)

**Primary Approach**: Google Cloud Natural Language API with streaming ingestion

#### Why This Solution?
1. **Managed Service**: No infrastructure to maintain during traffic spikes
2. **Multi-Language**: Native support for Chinese (Simplified/Traditional), Japanese, Korean
3. **Scalability**: Auto-scales to handle 100K+ posts during viral events
4. **Integration**: Easy integration with social platform APIs
5. **Fast Deployment**: Prototype to production in 1-2 weeks

#### Technical Implementation

```python
from google.cloud import language_v1
import tweepy  # For Twitter-like APIs (Weibo)
from typing import List, Dict
import time

client = language_v1.LanguageServiceClient()

class SocialMediaMonitor:
    def __init__(self, brand_keywords, competitor_keywords):
        self.brand_keywords = brand_keywords  # Keywords to track
        self.competitor_keywords = competitor_keywords
        self.api_client = client

        # Rate limiting
        self.requests_per_minute = 600  # Google Cloud free tier limit
        self.request_count = 0
        self.last_reset = time.time()

    def monitor_stream(self, platform='weibo', language='zh'):
        """
        Monitor social media stream for brand/competitor mentions

        Args:
            platform: 'weibo'/'red'/'line'/'kakaotalk'
            language: 'zh'/'ja'/'ko'
        """
        # Connect to platform streaming API
        stream = self._connect_platform_stream(platform)

        for post in stream:
            # Extract entities from post
            entities = self.extract_entities_with_rate_limit(post['text'], language)

            # Check if post mentions brand or competitors
            brand_mentioned = any(e['text'] in self.brand_keywords for e in entities)
            competitor_mentioned = any(e['text'] in self.competitor_keywords for e in entities)

            if brand_mentioned or competitor_mentioned:
                # Store mention for analysis
                mention = {
                    'post_id': post['id'],
                    'platform': platform,
                    'text': post['text'],
                    'author': post['author'],
                    'timestamp': post['timestamp'],
                    'entities': entities,
                    'brand_mentioned': brand_mentioned,
                    'competitor_mentioned': competitor_mentioned,
                    'engagement': post.get('likes', 0) + post.get('shares', 0)
                }

                # Store in database
                self._store_mention(mention)

                # Real-time alerts for high-engagement posts
                if mention['engagement'] > 10000:
                    self._send_alert(mention)

    def extract_entities_with_rate_limit(self, text, language):
        """Extract entities with rate limiting"""
        # Rate limit check
        if time.time() - self.last_reset > 60:
            self.request_count = 0
            self.last_reset = time.time()

        if self.request_count >= self.requests_per_minute:
            time.sleep(60 - (time.time() - self.last_reset))
            self.request_count = 0
            self.last_reset = time.time()

        # Extract entities
        document = {
            "content": text,
            "type_": language_v1.Document.Type.PLAIN_TEXT,
            "language": language
        }

        response = self.api_client.analyze_entities(request={"document": document})
        self.request_count += 1

        entities = [
            {
                'text': entity.name,
                'type': entity.type_.name,
                'salience': entity.salience
            }
            for entity in response.entities
        ]

        return entities

    def generate_daily_report(self, date):
        """Generate daily brand monitoring report"""
        mentions = self._load_mentions(date)

        report = {
            'date': date,
            'total_mentions': len(mentions),
            'brand_mentions': sum(1 for m in mentions if m['brand_mentioned']),
            'competitor_mentions': sum(1 for m in mentions if m['competitor_mentioned']),
            'top_influencers': self._top_influencers(mentions),
            'trending_topics': self._trending_entities(mentions),
            'sentiment_breakdown': self._sentiment_analysis(mentions),
            'high_engagement_posts': self._high_engagement(mentions)
        }

        return report

# Usage
monitor = SocialMediaMonitor(
    brand_keywords=['Nike', '耐克', 'ナイキ', '나이키'],
    competitor_keywords=['Adidas', '阿迪达斯', 'アディダス', '아디다스']
)

# Start monitoring (runs continuously)
monitor.monitor_stream(platform='weibo', language='zh')
```

#### Production Deployment

**Infrastructure**:
- **Cloud API Costs**: $1,000-2,500/month (100K-250K posts processed)
- **Application Server**: t3.medium for stream ingestion ($50/month)
- **Database**: PostgreSQL for mention storage ($100/month)
- **Dashboard**: Grafana/Looker for visualization ($200/month)
- **Total Cost**: ~$1,400-2,900/month

**Expected Impact**:
- Real-time brand monitoring across 3-5 platforms
- 5-10 minute latency from post to dashboard
- 85-90% entity extraction accuracy (sufficient for monitoring)
- ROI: $50K-150K/year in improved brand response time and crisis management

---

## Use Case Pattern #5: Customer Data Normalization and CRM Deduplication

### Generic Requirements Profile
- **Scenario**: Deduplicate and normalize customer records with CJK names, companies, addresses across CRM systems
- **Constraints**: Batch processing acceptable, very high precision required (false positives = data loss), entity resolution complex
- **Volume**: 100K-10M records, one-time migration + ongoing incremental updates
- **Priority**: Accuracy over speed, need fuzzy matching for name variations

### Recommended Solution: Hybrid Architecture (Self-Hosted + Entity Resolution Database)

**Primary Approach**: HanLP/LTP for extraction + custom entity resolution layer

#### Technical Implementation

```python
import hanlp
from fuzzywuzzy import fuzz
from typing import List, Dict, Tuple
import hashlib

ner_zh = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)

class CustomerDataNormalizer:
    def __init__(self, entity_resolution_db_path='entity_resolution.db'):
        self.ner = ner_zh
        self.resolution_db = self._load_resolution_db(entity_resolution_db_path)

    def normalize_customer_record(self, record: Dict) -> Dict:
        """
        Extract and normalize customer name, company, address

        Args:
            record: {
                'raw_input': str,  # Free-form customer input
                'source_system': str,  # CRM system name
                'record_id': str
            }

        Returns:
            {
                'customer_name': str,  # Normalized name
                'customer_id': str,  # Canonical customer ID
                'company_name': str,
                'company_id': str,
                'address_normalized': str,
                'confidence': float,
                'matched_existing': bool,  # Found in existing DB?
                'possible_duplicates': [...]  # Potential matches
            }
        """
        text = record['raw_input']

        # Extract entities
        entities = self.ner(text)

        # Extract customer name
        customer_name_raw = self._extract_customer_name(entities)

        # Normalize name (handle variations)
        customer_name_normalized = self._normalize_name(customer_name_raw)

        # Entity resolution (find canonical ID)
        customer_id, match_confidence = self._resolve_customer(customer_name_normalized)

        # Extract company
        company_name_raw = self._extract_company(entities)
        company_name_normalized = self._normalize_company(company_name_raw)
        company_id, _ = self._resolve_company(company_name_normalized)

        # Normalize address
        address_normalized = self._normalize_address(entities, text)

        # Find possible duplicates
        duplicates = self._find_duplicates(customer_name_normalized, company_name_normalized)

        return {
            'customer_name': customer_name_normalized,
            'customer_id': customer_id,
            'company_name': company_name_normalized,
            'company_id': company_id,
            'address_normalized': address_normalized,
            'confidence': match_confidence,
            'matched_existing': customer_id is not None,
            'possible_duplicates': duplicates,
            'source_system': record['source_system'],
            'source_record_id': record['record_id']
        }

    def _normalize_name(self, name):
        """Normalize Chinese name (handle variations)"""
        if not name:
            return None

        # Remove spaces
        normalized = name.replace(' ', '')

        # Handle traditional/simplified conversion
        # (use OpenCC if needed)

        return normalized

    def _resolve_customer(self, name) -> Tuple[str, float]:
        """Resolve customer to canonical ID"""
        if not name:
            return None, 0.0

        # Exact match
        if name in self.resolution_db['customers']:
            return self.resolution_db['customers'][name], 1.0

        # Fuzzy match
        for existing_name, customer_id in self.resolution_db['customers'].items():
            similarity = fuzz.ratio(name, existing_name) / 100.0
            if similarity > 0.90:  # 90% similarity threshold
                return customer_id, similarity

        # No match - generate new ID
        return None, 0.0

    def _find_duplicates(self, customer_name, company_name):
        """Find possible duplicate records"""
        duplicates = []

        # Search existing records
        for existing_record in self.resolution_db['records']:
            # Compare names
            name_similarity = fuzz.ratio(customer_name, existing_record['customer_name']) / 100.0

            # Compare companies (if both present)
            company_similarity = 0.0
            if customer_name and existing_record.get('company_name'):
                company_similarity = fuzz.ratio(company_name, existing_record['company_name']) / 100.0

            # Duplicate if high similarity
            if name_similarity > 0.85 or (name_similarity > 0.75 and company_similarity > 0.85):
                duplicates.append({
                    'record_id': existing_record['record_id'],
                    'name_similarity': name_similarity,
                    'company_similarity': company_similarity
                })

        return duplicates

# Usage: Batch deduplication
normalizer = CustomerDataNormalizer()

# Load customer records from multiple CRM systems
records = load_customer_records_from_all_systems()

normalized_results = []
for record in records:
    normalized = normalizer.normalize_customer_record(record)
    normalized_results.append(normalized)

    if normalized['possible_duplicates']:
        # Flag for manual review
        flag_for_review(record, normalized)

# Generate master customer database
master_db = build_master_customer_database(normalized_results)
```

#### Expected Impact:
- 80-90% reduction in duplicate customer records
- Unified customer view across CRM systems
- 95%+ accuracy with manual review of flagged duplicates
- ROI: $200K-500K/year in improved marketing efficiency and customer experience

---

## Summary and Implementation Roadmap

### Quick Reference: Solution Selector

| Use Case | Volume | Priority | Recommended Solution | Cost/Month | Time to Production |
|----------|--------|----------|---------------------|-----------|-------------------|
| **Business Intelligence** | 10K-100K docs/day | Accuracy | HanLP BERT (GPU) | $600-800 | 4-6 weeks |
| **E-Commerce Address** | 100K-1M orders/day | Speed & Cost | LTP (CPU) | $300-900 | 2-4 weeks |
| **Legal/Compliance** | 1K-10K contracts/month | Multi-language | Stanza | $600 | 3-5 weeks |
| **Social Media** | Variable 10K-500K/day | Reliability | Google Cloud API | $1,400-2,900 | 1-2 weeks |
| **CRM Deduplication** | 100K-10M records | Precision | Hybrid (HanLP + Custom) | $800-1,200 | 6-10 weeks |

### Implementation Roadmap

**Week 1-2: Rapid Prototyping**
- Choose cloud API (Google Cloud or Azure)
- Implement basic extraction pipeline
- Test on sample data (100-1,000 records)
- Validate accuracy on your domain

**Month 1: Production MVP**
- Deploy self-hosted solution (HanLP, LTP, or Stanza)
- Containerized deployment (Docker)
- Integration with existing systems
- Initial monitoring and alerting

**Month 2-3: Optimization**
- Fine-tune on domain-specific data
- Implement entity resolution/linking
- Build review workflows for low-confidence cases
- Performance optimization (quantization, batching)

**Month 4+: Scale and Enhance**
- Horizontal scaling for high volume
- Multi-language expansion (if needed)
- Advanced features (entity relationships, knowledge graph)
- Continuous improvement via active learning

---

**Next Phase**: S4 Strategic Discovery will examine long-term technology evolution, vendor viability, migration risks, and ecosystem maturity for strategic decision-making.
