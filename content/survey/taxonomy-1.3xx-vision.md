---
sidebar_position: 99
title: "Taxonomy Vision: 1.3xx Domain-Specific Data & Analysis"
---

# 1.3xx Series Vision: Domain-Specific Data & Analysis

> **Status**: Planning document for future taxonomy expansion
> **Created**: 2025-02-05
> **Context**: Emerging from civic budget analysis work (see task 271842)

## Overview

The 1.3xx series will cover **domain-specific data infrastructure and analysis libraries** - specialized tools for working with real-world data in specific industries and sectors.

### Thematic Structure

- **1.0xx-1.1xx**: Core computer science (algorithms, data structures, ML, NLP, UI)
- **1.2xx**: Modern infrastructure (LLMs, calendaring, social protocols, messaging)
- **1.3xx**: Domain-specific data & analysis ← NEW SERIES
- **2.xxx**: Standards and protocols
- **3.xxx**: Commercial platforms and applications

## Rationale

Domain-specific data work has unique characteristics:
1. **Specialized data sources** - Often messy, unstructured, or semi-structured
2. **Entity resolution challenges** - Domain-specific entities need normalization
3. **Regulatory requirements** - Compliance, standardization, reporting mandates
4. **Fragmented tooling** - Libraries exist but aren't cataloged
5. **High-stakes domains** - Finance, healthcare, legal, government

These domains need the same infrastructure (parsing, entity resolution, data access, analysis) but general-purpose tools fall short.

## Proposed Structure

### 1.300-329: Financial Data & Analysis

**1.300-309: Public Finance & Civic Data**
- Public finance modeling (OpenFisca, PolicyEngine, Tax-Calculator)
- Government data access (Census, USAspending APIs)
- Budget document parsing (CAFR/ACFR extraction)
- Civic entity resolution (agency names, jurisdictions)
- Procurement & contract analysis
- Fiscal health metrics

**1.310-319: Corporate Finance & Securities**
- SEC filing parsers (EDGAR access, 10-K/10-Q extraction)
- Financial statement analysis
- Company entity resolution
- Credit analysis libraries
- Market data access

**1.320-329: Financial Infrastructure**
- Financial entity resolution (LEI, CUSIP, ISIN)
- Financial document parsing (earnings calls, prospectuses)
- Time-series financial data
- Financial data standards (XBRL, FIX)

### 1.330-339: Legal & Regulatory Data

- Contract analysis (NDA parsing, clause extraction, risk assessment)
- Case law research (legal search engines, citation analysis)
- Legal entity identification (parties, jurisdictions, citations)
- Regulatory compliance checking
- Court data access (PACER, state court systems)
- Legal document generation

### 1.340-349: Healthcare & Medical Data

- HL7/FHIR libraries (healthcare interoperability standards)
- Medical NLP (clinical text analysis, entity extraction)
- Medical coding (ICD-10, CPT, SNOMED CT)
- Drug/pharmaceutical databases
- EHR integration tools
- Public health datasets (CDC, WHO)

### 1.350-359: Real Estate & Property Data

- Property records access (assessor data, deeds, titles)
- Parcel/GIS data integration
- Zoning analysis
- Real estate market data
- Title search & deed parsing
- Property valuation models

### 1.360-369: Supply Chain & Logistics

- Shipping carrier APIs (FedEx, UPS, USPS, DHL)
- Inventory management libraries
- Trade/customs data (harmonized tariff codes)
- Supply network analysis
- Warehouse optimization
- Freight tracking

### 1.370-379: Energy & Climate Data

- Energy market APIs (CAISO, PJM, ERCOT)
- Smart grid/IoT data
- Carbon accounting & emissions tracking
- Climate datasets (NOAA, NASA, IPCC)
- Renewable energy modeling
- Building energy analysis

### 1.380-389: Scientific Research Data

- Lab equipment APIs/drivers
- Scientific file formats (NetCDF, HDF5, FITS)
- Research data repositories (Zenodo, Dryad)
- Unit conversion & measurement libraries
- Data provenance tracking
- Scientific workflow tools

### 1.390-399: Government Operations (non-financial)

- Legislative data (bills, votes, sponsors, amendments)
- Regulatory actions & Federal Register
- FOIA/public records access
- Open data portal APIs
- Election data & results
- Government entity resolution (agencies, departments, programs)

## Scope & Boundaries

### What Belongs in 1.3xx

✅ **Domain-specific data infrastructure**
- Parsers for domain-specific documents
- Entity resolution for domain entities
- Data access libraries for domain data sources
- Analysis frameworks tailored to domain needs

✅ **Open source libraries and free APIs**
- Python/JavaScript/R libraries
- Government/public data APIs
- Open data standards implementations

✅ **Reusable components**
- Can be used across multiple projects
- Solve general problems within the domain
- Have documentation and examples

### What Does NOT Belong

❌ **General-purpose tools** (already covered in 1.0xx-1.1xx)
- Generic parsers → 1.100-109 Text & Document Processing
- Generic graph analysis → 1.010-019 Graph & Network
- Generic NLP → 1.030-039 String & Text Algorithms

❌ **End-user applications** (go in 3.xxx)
- Complete SaaS platforms
- Turnkey solutions
- Commercial applications

❌ **Pure standards** (go in 2.xxx)
- Protocol specifications
- Data format standards
- API specifications (without implementations)

### The Blurred Lines Problem

**Challenge**: Domain-specific work increasingly involves:
- Commercial APIs with free tiers
- Government data portals (free but not "open source")
- Freemium services
- Proprietary data with open source access libraries

**Initial approach**:
1. **Focus on libraries** - Wrapper libraries that access commercial APIs are in scope
2. **Document the ecosystem** - Note when data/APIs are commercial vs. free
3. **Prioritize open** - When multiple options exist, lead with open source
4. **Be transparent** - Mark commercial dependencies clearly

**Examples**:
- ✅ `python-edgar` (open library accessing free SEC EDGAR)
- ✅ `census` (open library accessing free Census Bureau API)
- ✅ `openaq` (open library accessing free air quality data)
- ⚠️ `alpaca-trade-api` (open library accessing freemium brokerage API)
- ❌ Pure Bloomberg Terminal access (commercial, no free option)

We'll document this boundary as we encounter cases.

## Implementation Strategy

### Phase 1: Anchor with Public Finance (1.300-309)
- Start with the best-defined domain (civic budget analysis driver)
- Document existing libraries (OpenFisca, PolicyEngine)
- Identify gaps clearly
- Establish pattern for gap notation

### Phase 2: Expand to Related Domains
- Corporate finance (1.310-319) - natural extension
- Legal data (1.330-339) - similar parsing/entity resolution challenges
- Healthcare (1.340-349) - high-value, well-defined standards

### Phase 3: Fill Out Vision
- Add remaining domains as research capacity allows
- Prioritize by: (a) existing tooling, (b) community need, (c) research interest

## Documentation Standards

Each 1.3xx entry should include:

**For existing libraries:**
- Name & link (GitHub, PyPI, npm)
- Primary use case (1-2 sentences)
- Language/ecosystem
- Maintenance status (active, stable, archived)
- Notable users (if applicable)
- Key dependencies
- Commercial vs. free

**For identified gaps:**
- Problem description
- Why general-purpose tools fall short
- Potential approach (if known)
- Related existing tools
- Estimated complexity

**Cross-references:**
- Link to related 1.0xx-1.1xx general tools
- Link to 2.xxx standards (if applicable)
- Link to 3.xxx commercial alternatives (if applicable)

## Open Questions

1. **Granularity**: When does a subdomain deserve its own 10-slot range vs. being a single entry?
2. **Overlap**: How to handle libraries that span multiple domains (e.g., graph analysis for both finance and supply chain)?
3. **Currency**: How frequently to update as new libraries emerge?
4. **Community input**: Should we solicit domain expert review before publishing each range?
5. **Commercial boundaries**: How to refine the "open library accessing commercial API" boundary?

## Success Criteria

The 1.3xx series succeeds if:
1. **Discovery**: Domain practitioners can find tools faster than Google/GitHub search
2. **Gap identification**: White space becomes visible, inspiring new library development
3. **Legitimacy**: Domain-specific infrastructure elevated as serious software engineering
4. **Composability**: Clear documentation enables combining libraries (parser + analyzer + visualizer)
5. **Community**: Becomes a resource domain communities reference and contribute to

## Next Steps

- [ ] Draft 1.300-309 structure (Public Finance & Civic Data)
- [ ] Research existing libraries in each subsection
- [ ] Document gaps with problem descriptions
- [ ] Add to survey catalog with proper formatting
- [ ] Update homepage/sidebar
- [ ] Get community feedback (Code for America, civic tech community)
- [ ] Iterate on documentation standards based on feedback

---

**References:**
- Original proposal: Vikunja task 271842
- Related: [Survey Methodology](/survey/methodology)
- Related: [Vision](/vision)
