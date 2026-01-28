# S3 NEED-DRIVEN DISCOVERY: Approach

**Experiment**: 1.033.2 Chinese Word Segmentation Libraries
**Pass**: S3 - Need-Driven Discovery
**Date**: 2026-01-28
**Target Duration**: 45-60 minutes

## Objective

Analyze Chinese word segmentation libraries from a **use case perspective**, identifying the optimal tool for specific real-world scenarios. Focus on WHEN to use each tool rather than HOW they work internally.

## Research Method

For each use case, evaluate:

### Use Case Characteristics
- **Domain**: Industry or application context
- **Text characteristics**: Formal/informal, length, complexity
- **Volume**: Requests per second, total corpus size
- **Latency requirements**: Real-time vs. batch acceptable
- **Accuracy requirements**: Good enough vs. mission-critical

### Tool Selection Criteria
- **Primary recommendation**: Best fit based on use case needs
- **Alternative options**: Backup choices with trade-offs
- **Anti-patterns**: Tools to avoid and why
- **Implementation guidance**: Code samples and deployment tips

### Success Metrics
- **Accuracy targets**: Expected F1 score for domain
- **Performance targets**: Throughput and latency goals
- **Resource constraints**: Memory, GPU, cost considerations

## Use Cases in Scope

### 1. E-Commerce Product Search
**Context**: Online marketplace with millions of products
- Indexing product titles and descriptions
- Real-time search query segmentation
- Mixed Simplified/Traditional Chinese
- Custom product names and brands

**Tool focus**: Jieba (search engine mode, custom dictionaries)

### 2. Medical Records Processing
**Context**: Healthcare system digitizing patient records
- Clinical notes and medical reports
- Batch processing of archives
- High accuracy requirement (patient safety)
- Domain-specific medical terminology

**Tool focus**: PKUSeg (medicine model) or LTP (fine-tuned)

### 3. Social Media Analytics
**Context**: Platform analyzing user-generated content (Weibo, WeChat)
- Informal text with slang and emoji
- High volume (millions of posts daily)
- Sentiment analysis pipeline
- Trending topic extraction

**Tool focus**: PKUSeg (web model) or Jieba (high throughput)

### 4. Legal Document Analysis
**Context**: Law firm processing contracts and case law
- Formal legal Chinese with specialized terminology
- High accuracy requirement (legal implications)
- Batch processing acceptable
- Multi-task needs (segmentation + NER for entities)

**Tool focus**: PKUSeg (custom trained) or LTP (dependency parsing)

### 5. News Aggregation Platform
**Context**: Media company processing news articles
- Standard written Chinese
- Batch processing of daily feeds
- Keyword extraction for categorization
- Moderate accuracy requirement

**Tool focus**: PKUSeg (news model) or Jieba (keyword extraction)

### 6. Traditional Chinese Academic Corpus
**Context**: University digitizing historical documents
- Traditional Chinese literature and archives
- Highest accuracy requirement (scholarly use)
- Batch processing (time not critical)
- POS tagging and linguistic analysis

**Tool focus**: CKIP (97.33% F1 Traditional Chinese)

### 7. Real-Time Chatbot
**Context**: Customer service chatbot for online platform
- Real-time conversational Chinese
- Low latency requirement (<100ms)
- Mixed formal/informal text
- High volume (thousands of concurrent users)

**Tool focus**: Jieba or LTP Tiny (low latency)

## Deliverables

1. **approach.md** (this document)
2. **use-case-ecommerce.md** - E-commerce product search
3. **use-case-medical.md** - Medical records processing
4. **use-case-social-media.md** - Social media analytics
5. **use-case-legal.md** - Legal document analysis
6. **use-case-chatbot.md** - Real-time chatbot
7. **recommendation.md** - Use case decision matrix

## Success Criteria

- Identify optimal tool for each use case with clear rationale
- Provide actionable implementation guidance
- Include realistic performance expectations
- Address common pitfalls and edge cases
- Create decision tree for use case selection

## Research Sources

- S1 and S2 findings (technical capabilities)
- Real-world deployment case studies
- User reports from GitHub issues and discussions
- Published benchmarks on domain-specific corpora
- Production deployment patterns
