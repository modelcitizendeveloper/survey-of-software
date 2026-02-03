# Discovery Table of Contents: Translation Memory

## S1: Rapid Pass (Quick Landscape Survey)

- **approach.md** - Rapid pass objectives and focus areas
- **translation-memory-basics.md** - Core TM concepts, how it works, CAT tools
- **tmx-format.md** - TMX standard, history, why it matters
- **omegat.md** - Open source CAT tool overview
- **memoq.md** - Commercial CAT tool overview
- **recommendation.md** - S1 findings and tool decision framework

## S2: Comprehensive Pass (Deep Dive into Ecosystem)

- **approach.md** - Comprehensive pass objectives
- **tmx-specification.md** - TMX 1.4b technical details, XML structure, compliance levels
- **xliff-format.md** - XLIFF for localization workflows, vs. TMX comparison
- **tbx-terminology.md** - TermBase eXchange for glossary management
- **cat-tools-landscape.md** - Major CAT tools (Trados, Smartcat, Phrase, Wordfast)
- **recommendation.md** - Technical insights and implementation patterns

## S3: Need-Driven Pass (Practical Implementation)

- **approach.md** - Need-driven pass objectives
- **programmatic-tmx-handling.md** - Python libraries, code examples, TMX manipulation
- **alignment-and-tm-creation.md** - Creating TM from legacy translations (LF Aligner, bitext2tmx)
- **tm-quality-cleaning.md** - TM cleaning tools, quality metrics, automated checks
- **mt-tm-hybrid-workflows.md** - Combining machine translation with TM, post-editing
- **continuous-localization.md** - CI/CD integration, GitHub Actions, automated workflows
- **recommendation.md** - Implementation priorities and tool recommendations

## S4: Strategic Pass (Business Decisions)

- **approach.md** - Strategic pass objectives
- **build-vs-buy.md** - ROI calculations, self-hosted vs. cloud, commercial vs. open source
- **tm-governance.md** - Ownership models, quality standards, asset valuation, lifecycle
- **recommendation.md** - Executive summary, decision frameworks, strategic priorities

## Key Takeaways

### Standards (Work Together)
- **TMX** - Translation memory exchange (archival, sharing)
- **XLIFF** - Active translation workflows (extract, translate, merge)
- **TBX** - Terminology management (glossaries, approved terms)

### Tools (By Use Case)
- **OmegaT** - Free, open source, self-hosted (freelancers, privacy-sensitive)
- **MemoQ** - Commercial desktop ($44/month, advanced features)
- **SDL Trados** - Industry standard (agencies require it)
- **Smartcat** - Cloud TMS with marketplace (agencies, vendor management)
- **Phrase** - Cloud TMS for CI/CD (software companies, automation)

### Workflows (Modern Approach)
- **Continuous Localization** - CI/CD integrated, XLIFF extraction/merging
- **MT + TM Hybrid** - Use TM for high matches, MT for new content, store post-edits in TM
- **TM Cleaning** - Quarterly maintenance, 20-45% removal typical
- **Quality Governance** - Client-owned TM, quarterly exports, version control

### ROI (Measurable)
- **Freelancers** - Tools pay for themselves month 1 (20-40% match rates)
- **Agencies** - Cloud TMS payback in 3-4 months (PM time savings)
- **Software** - Continuous localization reduces time-to-market from weeks to days

## Total Files: 21 discovery documents
