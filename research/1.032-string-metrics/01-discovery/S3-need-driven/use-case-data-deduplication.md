# Use Case: Data Deduplication and Record Linkage

## Who Needs This

**Primary personas:**
- **Data Engineers:** Building ETL pipelines for data warehouses
- **Database Administrators:** Cleaning up duplicate customer/vendor records
- **Analytics Engineers:** Preparing datasets for BI reporting

**Organizational context:**
- Enterprises with CRM systems (Salesforce, HubSpot, custom)
- Data warehouses aggregating from multiple sources
- Healthcare systems with patient record matching requirements
- Financial services with KYC (Know Your Customer) compliance

**Technical environment:**
- Batch processing (nightly ETL runs)
- SQL databases (PostgreSQL, MySQL, SQL Server)
- Big data platforms (Spark, Hadoop)
- Python data pipelines (pandas, dbt)

## Why They Need String Metrics

### Pain Point 1: Duplicate Customer Records

**Problem:**
Same customer entered multiple times:
- "John Smith, john.smith@email.com"
- "Jon Smith, johnsmith@email.com"
- "J. Smith, john_smith@email.com"

CRM inflates customer count, marketing sends duplicate emails, sales call same person multiple times.

**Business impact:**
- Wasted marketing spend (10-30% duplicate emails)
- Poor customer experience (multiple reps, inconsistent data)
- Compliance risk (GDPR requires single source of truth)
- Bad analytics (revenue attribution errors)

**Why string metrics help:**
Fuzzy name + email matching identifies likely duplicates for human review or automated merging.

### Pain Point 2: Vendor/Product Master Data

**Problem:**
Multiple purchasing systems create variant vendor names:
- "International Business Machines"
- "IBM Corporation"
- "I.B.M. Corp"
- "IBM Inc."

Spend analytics broken, can't negotiate volume discounts, audit trails unclear.

**Business impact:**
- Lost volume discounts (5-15% of procurement spend)
- Audit failures (can't trace spend to vendor)
- Vendor relationship gaps (duplicated contacts)

**Why string metrics help:**
Canonical name matching clusters variants, enables master data management (MDM).

### Pain Point 3: Data Integration from Acquisitions

**Problem:**
Company acquires competitor, needs to merge customer databases. No common IDs, names/addresses vary:
- "Acme Corp" vs "ACME Corporation"
- "123 Main St" vs "123 Main Street, Suite 100"

Manual merge takes months, blocks integration value.

**Business impact:**
- Delayed synergy realization ($millions in M&A context)
- Duplicate customer outreach (brand damage)
- Incomplete view of customer value (analytics broken)

**Why string metrics help:**
Automated fuzzy matching flags likely matches, reduces manual review from months to weeks.

## Requirements and Constraints

### Must-Have Requirements

**Accuracy:**
- Precision: >95% (few false positives to minimize manual review)
- Recall: >85% (catch most duplicates, some manual search acceptable)
- F1 score: >90% (balanced for human review workload)

**Performance:**
- Batch throughput: 10K-100K comparisons/second
- Latency: Not critical (batch processing overnight)
- Scalability: Handle 1M-100M records

**Compliance:**
- Audit trail: Track all merge decisions
- Reversibility: Undo incorrect merges
- Data privacy: Hash PII before fuzzy matching (GDPR/HIPAA)

### Nice-to-Have Features

**Workflow integration:**
- Export likely duplicates to CSV for review
- Integration with MDM tools (Informatica, Talend)
- Confidence scores for auto-merge vs human review

**Advanced matching:**
- Multi-field similarity (name + address + phone)
- Transitive clustering (if A≈B and B≈C, then A≈C)
- Temporal awareness (recent records weighted higher)

### Constraints

**Technical:**
- Must work with existing SQL databases (can't require NoSQL)
- Python or Java ecosystem (team skills)
- No cloud-only solutions (on-prem data residency requirements)

**Business:**
- One-time project budget (not recurring SaaS)
- 3-6 month timeline for implementation
- Minimal ongoing maintenance (set-and-forget preferred)

## Success Criteria

### Quantitative Metrics

**Data quality:**
- Duplicate customer records: Reduce from 15% to <2%
- Vendor master duplicates: Reduce from 25% to <5%
- Manual review time: <8 hours/week (down from 40+ hours)

**Business outcomes:**
- Procurement savings: 5-10% from volume discount negotiations
- Marketing efficiency: 15-25% reduction in wasted email sends
- Compliance: Pass audit with single customer source of truth

**Technical performance:**
- Processing time: <4 hours for nightly deduplication run
- False positive rate: <5% (minimize unnecessary reviews)
- False negative rate: <15% (some duplicates missed acceptable)

### Qualitative Indicators

**User confidence:**
- Data analysts trust customer counts in reports
- Sales reps confident they're not duplicating outreach
- Finance can trace vendor spend accurately

**Process improvement:**
- Manual deduplication time reduced by 80%+
- New acquisitions: Merge databases in weeks not months
- Proactive duplicate prevention (catch at data entry)

## Common Pitfalls

**Naive pairwise comparison (O(n²)):**
Comparing 1M records → 500B comparisons → weeks of processing.
**Fix:** Use blocking (group by first 2 chars of last name), then fuzzy-match within groups.

**Single-field matching:**
"John Smith" + "jsmith@gmail.com" vs "John Smith" + "john_smith@yahoo.com" - same name, different people.
**Fix:** Multi-field similarity (weighted combination of name + email + address).

**Over-automation:**
Auto-merging without human review → irreversible data loss when false positive occurs.
**Fix:** Confidence thresholds: >95% auto-merge, 70-95% human review, <70% skip.

**Ignoring data entry prevention:**
Deduplication after the fact → duplicates keep appearing.
**Fix:** Real-time fuzzy matching at data entry (warn user "similar record exists").

## Technology Fit

**Recommended approach:**

1. **Blocking strategy (reduce search space):**
   - Group records by first 2-3 chars of name/company
   - Or use locality-sensitive hashing (LSH) for large datasets

2. **Fuzzy matching within blocks:**
   - Python + rapidfuzz for batch processing
   - Jaro-Winkler for person names
   - Token-based for company names ("IBM Corp" ≈ "Corp IBM")

3. **Scoring and thresholds:**
   - Weighted similarity: name (40%), email (30%), address (20%), phone (10%)
   - Thresholds: >95 auto-merge, 70-95 review, <70 skip
   - Manual review queue for edge cases

4. **Integration:**
   - Python script in ETL pipeline (dbt, Airflow)
   - Export to CSV for manual review
   - Update source systems after verification

**Example workflow:**
```
1. Extract records from CRM/database
2. Normalize (lowercase, trim, remove punctuation)
3. Blocking (group by first 3 chars + zip code)
4. Pairwise fuzzy matching within blocks (rapidfuzz)
5. Compute weighted similarity score
6. Auto-merge (>95), queue for review (70-95), skip (<70)
7. Human review of queued pairs
8. Update records with canonical IDs
```

## Validation Questions

Before implementing deduplication project:

- [ ] Do we have significant duplicate records? (Audit suggests >10% duplication)
- [ ] Is manual review time excessive? (>20 hours/week currently)
- [ ] Can we define blocking strategy? (Common fields for pre-grouping)
- [ ] Do we have resources for human review? (Can't be 100% automated)
- [ ] Is there budget for deduplication project? (3-6 month effort)

**Decision point:** If 4+ validation questions are "yes", invest in fuzzy matching deduplication solution.

## Domain-Specific Considerations

**Healthcare (patient matching):**
- HIPAA compliance: Hash PII, audit all access
- Name variations: Nicknames, maiden names, cultural naming
- High precision required: False positive = wrong patient treatment

**Financial services (KYC):**
- Regulatory compliance: Document match decisions
- Entity resolution: Companies, subsidiaries, beneficial owners
- Global: Handle non-Latin names, diacritics, transliterations

**B2B CRM (account matching):**
- Company name variations: Legal entity vs trade name
- Hierarchy: Parent company, subsidiaries, divisions
- Contact deduplication: Job title changes, email updates
