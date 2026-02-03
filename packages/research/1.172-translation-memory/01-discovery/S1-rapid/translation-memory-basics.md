# Translation Memory: Core Concepts

## What is Translation Memory?

Translation Memory (TM) is a database that stores previously translated segments of text (sentences or paragraphs) as bilingual or multilingual pairs. Each entry contains a source segment and its corresponding translation(s).

## How It Works

### 1. Segmentation
- Source documents are split into segments (phrases, sentences, or paragraphs)
- Each segment becomes a discrete unit for translation
- Translators work segment-by-segment through the document

### 2. Storage
- When a translator approves a translation, it's automatically saved to the TM database
- Storage includes:
  - Source text
  - Target translation
  - Metadata (author, date, document name, context)
  - Context information (segments before/after)

### 3. Matching Process
TM works in the background, offering suggestions as translators work:

**100% Matches (Perfect):**
- Segment is identical to previously translated text
- **Context Match**: Segment AND surrounding segments match exactly (strongest confidence)
- **Exact Match**: Only the segment itself matches (still 100%, but less context)

**Fuzzy Matches (Partial):**
- Similarity rated by percentage (e.g., 85% match)
- Differences highlighted visually
- Translator reviews and adjusts as needed

### 4. Reuse
- System suggests previous translations instead of translating from scratch
- Translators can accept, modify, or reject suggestions
- Productivity increases as TM grows

## Benefits

**Productivity Gains:**
- 10-60% increase in translator productivity
- Larger TMs offer more matches over time
- Significant time savings on repetitive content

**Consistency:**
- Same terms/phrases translated identically
- Critical for technical documentation, legal texts, product catalogs
- Maintains brand voice across documents

**Cost Reduction:**
- Less human translation time needed
- Clients often pay reduced rates for high-percentage matches
- One-time translation of recurring content

## CAT Tools (Computer-Assisted Translation)

Translation Memory is the core feature of CAT tools. These tools provide:
- Segmentation and translation interface
- TM storage and retrieval
- Fuzzy matching algorithms
- Glossary/termbase management
- Quality assurance checks
- File format handling

**Note:** CAT tools assist human translators; they're different from Machine Translation (MT) systems like Google Translate.

## Typical Use Cases

- **Technical Documentation**: Manuals with recurring terminology
- **Software Localization**: UI strings, help files across versions
- **Legal Documents**: Contracts with standard clauses
- **Marketing Materials**: Brand-consistent messaging across campaigns
- **E-commerce**: Product descriptions with similar structure

## Sources

- [Translation memory in CAT tools – all you need to know](https://www.smartcat.com/blog/what-is-translation-memory-why-you-need-it/)
- [What is Translation Memory and how it works? - memoQ](https://www.memoq.com/tools/what-is-a-translation-memory/)
- [Maintain translation memories - Microsoft Learn](https://learn.microsoft.com/en-us/globalization/localization/translation-memories)
- [Computer-assisted translation - Wikipedia](https://en.wikipedia.org/wiki/Computer-assisted_translation)
- [CAT Tools: Your Guide to Computer-Assisted Translation [2026]](https://www.pairaphrase.com/blog/cat-tools)
- [Translation Memory (TM): Ultimate Guide for Organizations [2026]](https://www.pairaphrase.com/blog/what-is-translation-memory)
