# S3-Need-Driven: Recommendation

## Summary of Use Cases

| Use Case | Feasibility | Market Size | Impact | Recommendation |
|----------|-------------|-------------|--------|----------------|
| Reading Assistant | High | Medium | Medium | ⭐⭐⭐ Strong |
| Document Digitization | Medium | Small (specialized) | Very High | ⭐⭐⭐⭐ Excellent (with institutional backing) |
| Literature Search | Medium | Small (academic) | High | ⭐⭐⭐ Strong (grant-funded) |

## Key Insights from Use Case Analysis

### 1. No One-Size-Fits-All Solution

Different use cases require different parsing features:

- **Reading Assistant**: Needs fast, good-enough segmentation + definitions
- **Document Digitization**: Needs error-tolerant NER + quality assessment
- **Literature Search**: Needs structural indexing + quotation detection

**Implication**: Classical Chinese parsing tools should be modular, not monolithic. Users pick components they need.

### 2. Accuracy Requirements Vary Widely

- **Reading Assistant**: 70-80% parsing accuracy sufficient (users can adapt)
- **Document Digitization**: 80%+ needed (but manual review expected)
- **Literature Search**: 90%+ recall critical (precision less so)

**Implication**: Don't over-engineer for perfect accuracy. Most use cases tolerate errors with good UX for correction.

### 3. Market is Specialized but Global

- **Total classical Chinese students worldwide**: 50,000-200,000
- **Digital humanities projects**: Hundreds of institutions
- **Commercial market**: Small but underserved

**Implication**: Sustainable with niche focus, not venture-scale. Best suited for:
- Grant-funded research projects
- Institutional services
- Open-source with commercial support
- Educational tool companies (Pleco, Skritter, etc.)

### 4. Existing Tools Fill Partial Needs

- **ctext.org**: Excellent corpus, basic search
- **Jiayan**: Good segmentation, no parsing
- **Stanford CoreNLP**: Good parsing, wrong domain
- **Commercial apps (Pleco, Wenlin)**: Dictionaries, basic analysis

**Implication**: Integration and improved UX more valuable than starting from scratch. Partner with existing tools rather than compete.

## Recommended Development Priorities

### Priority 1: Classical Chinese Reading Assistant (Months 1-4)

**Why First:**
- Technically achievable with existing tools (Jiayan + ctext.org)
- Clear user need (students, researchers)
- Fast time to market
- Validates architecture for other use cases

**Scope:**
- Segmentation (Jiayan)
- Definitions (ctext.org API + CC-CEDICT)
- Basic POS tagging (rule-based)
- Simple web UI
- Mobile-responsive

**Go-to-Market:**
- Beta with university Chinese departments
- Freemium model (free basic, $5-10/mo premium)
- Partner with Pleco or Skritter for distribution

**Success Criteria:**
- 1,000+ users in first year
- 4+ star average rating
- Break-even on operating costs

### Priority 2: Document Digitization Pipeline (Months 5-12)

**Why Second:**
- Leverages reading assistant architecture
- High impact for cultural preservation
- Grant funding available (NEH, Mellon Foundation)
- Institutional customers have budgets

**Scope:**
- OCR integration (Tesseract)
- Error-tolerant parsing
- NER for historical entities
- Quality assessment
- Manual review workflow
- Batch processing API

**Go-to-Market:**
- Pilot with 2-3 university libraries
- Grant applications for development
- Open-source core, commercial support/hosting

**Success Criteria:**
- 3+ institutional deployments
- 100,000+ pages processed
- Grant funding secured for maintenance

### Priority 3: Literature Search Engine (Months 13-24)

**Why Third:**
- Most complex technically
- Builds on previous two projects
- Requires larger corpus and computing resources
- Best as mature, well-funded project

**Scope:**
- Full corpus indexing (ctext.org + other sources)
- Structural search
- Quotation detection
- Temporal analysis
- Research-grade API

**Go-to-Market:**
- Partnership with major research institution
- NEH Digital Humanities advancement grant
- Subscription for institutions ($500-2K/year)
- Free for individual researchers

**Success Criteria:**
- 50+ institutional subscribers
- 5,000+ registered users
- Cited in 100+ academic papers within 3 years

## Alternative Development Path: Open-Source Components

Instead of building products, create ecosystem of reusable components:

### Component 1: Classical Chinese NLP Library
```
pypi: classical-chinese-nlp
Features: Segmentation, POS, basic parsing
License: MIT
Maintenance: Community + institutional sponsors
```

### Component 2: Historical Chinese NER
```
pypi: historical-chinese-ner
Features: Pre-trained models, gazetteers, tools
License: MIT
Data: CBDB integration, place name databases
```

### Component 3: Classical Text Search
```
pypi: classical-search
Features: Elasticsearch config, quotation detection
License: MIT
Includes: Docker compose for quick deploy
```

### Why This Approach:
- **Lower maintenance burden**: Community contributes
- **Wider adoption**: Free removes barrier to entry
- **Academic credibility**: Open science model
- **Funding**: Academic grants support open-source
- **Long-term sustainability**: Not dependent on commercial success

### Revenue from Services:
- **Consulting**: Help institutions deploy
- **Hosting**: Managed services for libraries/universities
- **Support**: Commercial support contracts
- **Training**: Workshops and courses

## Phased Funding Strategy

### Phase 1: Bootstrap ($50K-100K)
- **Source**: Personal funds, small grants, Kickstarter
- **Timeline**: 6 months
- **Deliverable**: Reading Assistant MVP
- **Goal**: Prove concept, gather users

### Phase 2: Seed Funding ($200K-500K)
- **Source**: Institutional partnerships, NEH Digital Humanities Startup Grant
- **Timeline**: 12 months
- **Deliverable**: Document Digitization pipeline + expanded Reading Assistant
- **Goal**: Institutional adoption

### Phase 3: Growth ($500K-1M)
- **Source**: NEH Implementation Grant, university partnerships, Mellon Foundation
- **Timeline**: 18-24 months
- **Deliverable**: Literature Search Engine + mature platform
- **Goal**: Field standard for Classical Chinese NLP

### Phase 4: Sustainability (Ongoing)
- **Sources**: Subscriptions, support contracts, grants, donations
- **Maintenance**: 2-3 FTE sustained by revenue
- **Community**: Open governance, advisory board

## Risk Management Across Use Cases

### Technical Risks
- **Mitigation**: Start with proven components (Jiayan, ctext.org)
- **Fallback**: If custom parsing fails, fall back to rule-based

### Market Risks
- **Mitigation**: Validate with beta users before major investment
- **Pivot options**: Can pivot to modern Chinese if market too small

### Funding Risks
- **Mitigation**: Multiple revenue streams (grants + subscriptions + services)
- **Plan B**: Open-source + consulting model if product sales weak

### Sustainability Risks
- **Mitigation**: Design for low ongoing costs (efficient architecture)
- **Endgame**: Donate to academic institution if commercial model fails

## Final Recommendation

### Recommended Path: Hybrid Approach

**Years 1-2: Product Focus (Reading Assistant)**
- Build commercial product for students/researchers
- Prove technical approach and gather user feedback
- Become profitable enough to self-fund further development

**Years 2-4: Platform Expansion (Digitization + Search)**
- Transition to open-source component model
- Seek institutional partnerships and grant funding
- Build sustainable academic infrastructure

**Years 4+: Maintenance & Community**
- Transition governance to academic consortium
- Continue commercial services for revenue
- Focus on community building and research applications

### Success Looks Like (Year 5):
- **Reading Assistant**: 10,000+ active users, break-even or profitable
- **Document Digitization**: Deployed at 20+ institutions
- **Literature Search**: Standard tool cited in hundreds of papers
- **Open Source Components**: Used by dozens of research projects
- **Financially Sustainable**: Combination of grants, subscriptions, and services
- **Impact**: Measurably accelerated classical Chinese research globally

### Start Small, Think Big
**Month 1 Action Items:**
1. Build minimal reading assistant (Jiayan + simple UI)
2. Deploy beta to 50 users
3. Collect feedback
4. Prepare NEH Digital Humanities startup grant application

**Don't wait for perfect solution. Ship iteratively, learn from users, adapt.**
