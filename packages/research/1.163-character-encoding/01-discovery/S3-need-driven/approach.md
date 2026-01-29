# S3 Need-Driven Discovery - Approach

## Goal

Map character encoding libraries to specific real-world business scenarios and technical requirements. Move from "what can these libraries do?" to "which library solves my specific problem?"

## Methodology

### Scenario-Based Analysis

Instead of library-first evaluation, we use **need-first scenarios**:

1. **Legacy System Integration**: Taiwanese bank exports Big5 CSV → Modern UTF-8 API
2. **Web Scraping**: Unknown encoding, mixed charsets, possibly garbled
3. **User File Uploads**: Users claim UTF-8, actually Big5/GBK
4. **Bilingual Content Management**: Serve both Taiwan and Mainland audiences
5. **Database Migration**: Move from Big5/GBK columns to UTF-8
6. **Email Processing**: MIME multipart, mixed encodings, mojibake from forwarding
7. **Log Aggregation**: Collect logs from systems in different regions

### Evaluation Criteria by Scenario

For each scenario, identify:
- **Primary pain point**: Detection? Conversion? Repair?
- **Volume**: Single files vs batch processing
- **Accuracy requirement**: Can tolerate errors or must be perfect?
- **Performance constraint**: Real-time vs overnight batch?
- **Reversibility**: Need round-trip or one-way conversion?
- **Maintenance**: One-time migration or ongoing processing?

### Decision Framework

```
Scenario
  ↓
Requirements (accuracy, speed, volume)
  ↓
Library recommendation
  ↓
Integration pattern
  ↓
Error handling strategy
```

## Scenarios to Cover

### 1. Legacy Integration: Taiwan Banking System

**Context**: Taiwan bank uses Big5 for internal systems, exports CSV files daily
**Need**: Convert to UTF-8 for modern REST API consumption
**Constraints**:
- High accuracy (financial data)
- Daily batch (performance matters)
- Must preserve Traditional Chinese characters
- Some files have Big5-HKSCS (Hong Kong clients)

**Questions**:
- How to handle Big5-HKSCS without losing characters?
- Should we validate before/after conversion?
- What error handling for corrupted files?
- Performance target: process 10,000 files/day?

### 2. Web Scraping: E-Commerce Sites

**Context**: Scrape product listings from Taiwan, Mainland, and Hong Kong sites
**Need**: Normalize to UTF-8, handle mixed/unknown encodings
**Constraints**:
- Unknown encodings (sites lie in meta tags)
- Possible mojibake (sites with broken charsets)
- Real-time (user requests) or batch (overnight crawl)?
- Must handle JavaScript-rendered content

**Questions**:
- How to detect when meta tag is wrong?
- Should we repair mojibake or reject?
- Confidence threshold for auto-processing?
- Handle sites with mixed encodings (header vs body)?

### 3. User File Uploads: SaaS Platform

**Context**: Users upload CSV/TXT files, claim encoding in form
**Need**: Safely import to UTF-8 database
**Constraints**:
- User-provided encoding often wrong
- Must not corrupt data (SLO: <0.1% errors)
- Real-time validation (show preview before import)
- Support manual override if detection wrong

**Questions**:
- Trust user or always detect?
- How to show preview with uncertain encoding?
- Allow user to choose from top N hypotheses?
- Validate after conversion (how?)?

### 4. Bilingual Content: News Website

**Context**: News site serves Taiwan (Traditional) and Mainland (Simplified) audiences
**Need**: Convert content between variants, maintain regional vocabulary
**Constraints**:
- Professional content (quality critical)
- Regional vocabulary matters (計算機 vs 電腦)
- SEO considerations (need both versions)
- CMS integration (automated workflow)

**Questions**:
- OpenCC vs zhconv for quality?
- Cache converted content or convert on-request?
- How to handle ambiguous conversions?
- Round-trip edit workflow (edit Simplified, sync to Traditional)?

### 5. Database Migration: Legacy → Modern

**Context**: Migrate from MySQL Big5 columns to UTF-8mb4
**Need**: One-time conversion of millions of rows
**Constraints**:
- One-time migration (performance critical)
- Zero data loss acceptable (validate 100%)
- Staged rollout (migrate table by table)
- Rollback plan if issues found

**Questions**:
- Validate before or after migration?
- How to handle unmappable characters?
- Parallel processing strategy?
- How to verify migration success?

### 6. Email Processing: Support Ticket System

**Context**: Parse customer emails in multiple languages/encodings
**Need**: Extract text, handle attachments, preserve formatting
**Constraints**:
- MIME multipart (different parts, different encodings)
- Forwarded emails (nested mojibake)
- Attachments may be mis-encoded
- Must preserve for legal (exact bytes matter)

**Questions**:
- Parse MIME or use Python email library?
- How to handle nested encoding (forward chains)?
- Should we repair or preserve original?
- Attachment detection/handling?

### 7. Log Aggregation: Multi-Region Systems

**Context**: Collect logs from servers in Taiwan, Mainland, Japan, Korea
**Need**: Normalize to UTF-8 for searching/indexing
**Constraints**:
- High volume (TB/day)
- Performance critical (real-time indexing)
- Errors acceptable (logs, not transactions)
- Must handle truncated/corrupted logs

**Questions**:
- Fast detection (cchardet) worth accuracy loss?
- Skip repair (ftfy too slow)?
- Parallel processing on ingest pipeline?
- How to handle corrupted/truncated logs?

## Deliverables

For each scenario:
1. **Requirements analysis**: What matters most?
2. **Library selection**: Which tools to use?
3. **Integration pattern**: How to combine libraries?
4. **Error handling**: What can go wrong?
5. **Code example**: Runnable implementation
6. **Trade-offs**: Speed vs accuracy decisions
7. **Testing strategy**: How to validate?

## Success Criteria

S3 is complete when:
- 7 scenarios documented with requirements
- Library recommendations for each
- Working code examples
- Error handling strategies
- Trade-off analysis (when to sacrifice accuracy for speed)
- Testing/validation approaches
