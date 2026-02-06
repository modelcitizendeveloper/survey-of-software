# S3 Need-Driven Research: Approach

## Goal

Understand how terminology extraction libraries fit into **real-world workflows**, not just technical capabilities. Focus on:
1. Actual use cases (translation, technical writing, domain NLP)
2. Integration with existing tools (CAT tools, documentation systems)
3. Total Cost of Ownership (installation, maintenance, training)
4. Workflow patterns that maximize value
5. CJK quality in practice (not just theoretical support)

## Research Method

1. **Translation Workflow Analysis**: How do translators use terminology extraction?
   - CAT tool integration (SDL Trados, MemoQ, Smartcat)
   - Bilingual glossary creation
   - Productivity impact (time savings, quality improvement)

2. **Technical Writing Workflow**: Documentation team use cases
   - Glossary generation for user manuals
   - Terminology consistency across documents
   - Integration with documentation tools (Sphinx, MkDocs)

3. **Integration Patterns**: How to integrate pyate/KeyBERT into existing stacks
   - spaCy pipeline integration (pyate)
   - sentence-transformers ecosystem (KeyBERT)
   - Batch processing, API deployment

4. **TCO Analysis**: Beyond pip install
   - Installation complexity (dependencies, models, corpora)
   - Resource requirements (CPU, memory, disk)
   - Maintenance overhead (updates, model management)
   - Training requirements (learning curve for teams)

5. **Community Feedback**: What do users report?
   - GitHub issues, discussions
   - Blog posts, case studies
   - Translator/writer testimonials

## Key Questions

### For Translation Workflows:
- Do CAT tools integrate with Python libraries, or is manual export/import needed?
- What is the typical glossary creation time with vs without automated extraction?
- How well do extracted terms match translator expectations (precision, recall)?
- Does CJK extraction quality justify automation, or is manual curation still needed?

### For Technical Writing:
- How do teams manage terminology consistency across large documentation sets?
- What is the workflow for validating extracted terms (human-in-the-loop)?
- Do teams run extraction once (initial glossary) or continuously (every doc update)?

### For Integration:
- Can pyate/KeyBERT run in batch mode (process thousands of documents)?
- What are API deployment patterns (REST service, microservice)?
- How do teams handle versioning (model updates, algorithm changes)?

### For TCO:
- What is the total installation footprint (pyate: spaCy models, KeyBERT: BERT models)?
- What are ongoing maintenance costs (model updates, dependency conflicts)?
- What is the learning curve for non-ML engineers?

## Expected Outcome

**Practical recommendations** for:
1. **When** to use terminology extraction (value > cost threshold)
2. **How** to integrate into existing workflows (step-by-step patterns)
3. **Which** library for which use case (pyate vs KeyBERT decision criteria)
4. **What** to expect from CJK extraction (quality assessment, manual review needs)

## Sources

- **Translation community**: linguagreca.com, translator blogs, CAT tool documentation
- **Technical writing**: Docs-as-code community, Sphinx/MkDocs forums
- **Integration**: GitHub issues, Stack Overflow, Medium blog posts
- **TCO**: PyPI package statistics, model sizes, dependency graphs
