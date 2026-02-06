# Classical Chinese Parsing: Domain Explainer

## What This Solves

**The Problem**: Classical Chinese (文言文) - the written language used in China for over 2,000 years - is fundamentally different from modern Chinese. When you look at a classical text, there are no spaces between words, grammar follows different rules, and the vocabulary includes many archaic terms. While billions of characters of classical Chinese text exist in libraries and digital archives, we don't have good automated tools to help people read, analyze, or search these texts effectively.

**Who Encounters This**:
- University students learning Classical Chinese (tens of thousands globally)
- Researchers studying Chinese history, philosophy, and literature
- Libraries and museums digitizing historical documents
- Translators working with historical texts
- Educational technology companies building Chinese learning tools

**Why It Matters**: Classical Chinese texts contain millennia of historical records, philosophical thought, and cultural heritage. Without better tools to parse and analyze these texts, they remain largely inaccessible to modern readers. It's like having millions of books in a library with no catalog system - the knowledge is there, but finding and understanding it is painfully slow.

## Accessible Analogies

### The Space Between Words

Modern English uses spaces to separate words: "The quick brown fox jumps." If you removed all the spaces - "Thequickbrownfoxjumps" - you'd need to figure out where one word ends and another begins. That's what readers face with Classical Chinese, except it's even harder because the word-boundary rules are different from modern Chinese.

Think of it like this: Imagine trying to read old English texts from 1,000 years ago, written without spaces, using grammar rules that changed over centuries. "Hwæthewiltdothissenmething" instead of "What he wants to do with this." You'd need specialized knowledge to parse it correctly.

**Classical Chinese parsing is building the automated tools that can figure out those word boundaries and grammatical relationships** - like having a smart assistant who's read thousands of classical texts and can help you understand new ones.

### The Grammar Evolution Problem

Language changes over time. The way sentences are structured in Shakespeare's English differs from modern English. Now imagine if the change was even more dramatic - different sentence patterns, different function words, and texts spanning 2,000 years of gradual evolution.

Modern Chinese NLP tools are trained on contemporary texts (like news articles from the 1990s-2020s). Asking them to parse Classical Chinese is like asking a tool trained on modern English to parse Old English or Latin. The surface similarity (both use Chinese characters) hides deep structural differences.

**The parsing challenge is teaching computers to understand grammar patterns that were common in 500 BCE but rare or absent in modern usage.**

### The Missing Dictionary Problem

In most languages, you can look up words in a dictionary to find their meaning. But in Classical Chinese, determining what counts as a "word" is itself a challenge. Is "降大任" (confer great responsibility) one word or three? Different contexts might parse it differently.

It's like trying to build a search engine without knowing what counts as a searchable term. You can search for individual characters, but users want to search for concepts and phrases - and the computer doesn't know where those phrase boundaries are.

**Parsing solves the "what counts as a word?" problem, enabling accurate search, translation, and analysis.**

## When You Need This

### Clear Decision Criteria

**You NEED Classical Chinese parsing if:**

1. **You're building educational tools for Classical Chinese learners**
   - Example: A reading app that highlights words and shows definitions
   - Example: A grammar checker for students writing in Classical Chinese
   - Why: Without parsing, you can only offer character-by-character help, which isn't useful

2. **You're digitizing historical Chinese documents at scale**
   - Example: A library scanning 10,000 pages of Qing dynasty records
   - Example: Creating a searchable database of historical texts
   - Why: OCR gives you characters, but parsing makes them searchable and analyzable

3. **You're building research tools for Chinese studies scholars**
   - Example: A search engine for finding quotations across classical literature
   - Example: Tools for tracking how concepts evolved over dynasties
   - Why: Researchers need to find patterns, not just individual characters

4. **You're developing translation tools or services**
   - Example: Machine translation of historical documents
   - Example: Translation memory for professional translators
   - Why: Translation requires understanding sentence structure, not just word-for-word lookup

### When You DON'T Need This

**Skip Classical Chinese parsing if:**

1. **You're working only with modern Chinese**
   - Use modern Chinese NLP tools instead (much more mature)
   - Classical Chinese tools won't help with contemporary text

2. **You need only character-level search**
   - Simple string search is sufficient for basic lookups
   - Parsing adds complexity you don't need

3. **Your text volume is tiny (< 1,000 pages)**
   - Manual analysis may be faster and cheaper
   - Automation overhead not justified

4. **You have no Classical Chinese domain expertise**
   - Building these tools requires linguistic knowledge
   - Partner with experts rather than building in-house

## Trade-offs

### What You're Choosing Between

#### Option 1: Use Existing General Chinese NLP Tools (Stanford CoreNLP, HanLP)

**Pros:**
- Production-ready, well-documented
- Large community, lots of examples
- Free and open-source

**Cons:**
- Poor accuracy on Classical Chinese (60% vs 95% on modern)
- Trained on wrong kind of text (news, not historical)
- Requires expensive retraining to work well

**Best for:** Organizations already using these tools for modern Chinese who want to experiment with classical texts

#### Option 2: Build Custom Classical Chinese Parser

**Pros:**
- Can achieve 75-85% accuracy (good enough for many uses)
- Optimized for your specific use case
- Full control over features and priorities

**Cons:**
- 6-24 months development time
- Requires Classical Chinese linguistic expertise
- Ongoing maintenance burden

**Best for:** Organizations with long-term commitment to classical Chinese tools and in-house expertise

#### Option 3: Use Specialized Tools (Jiayan for segmentation + ctext.org for corpus)

**Pros:**
- Faster time to market (2-6 months)
- Leverages best-available components
- Lower development cost ($50K-150K vs $200K-500K)

**Cons:**
- Limited to segmentation (not full parsing)
- Dependency on small open-source projects
- May need to build additional components yourself

**Best for:** Startups, educational tool companies, researchers needing good-enough solution quickly

#### Option 4: Wait for Commercial Solutions

**Pros:**
- No development cost
- Professional support
- Maintained by vendor

**Cons:**
- May wait years (no major commercial tools exist yet)
- Miss first-mover advantage
- Vendor lock-in risk

**Best for:** Risk-averse organizations, those with other priorities

### Build vs. Buy Reality

**Truth**: There's nothing comprehensive to "buy" yet for Classical Chinese parsing. You're looking at:

- **Build**: 6-24 months, $100K-$500K
- **Adapt existing tools**: 3-12 months, $50K-$200K
- **Use basic tools + manual**: Ongoing, depends on volume

The market is young enough that building custom solutions is often the only option. The question is how much customization you need.

### Self-Hosted vs. Cloud Services

**Self-hosted** (Run on your own servers):
- **Pros**: Data privacy, full control, no per-use fees
- **Cons**: Infrastructure costs ($2K-10K/year), maintenance burden
- **Best for**: Institutions with existing infrastructure, sensitive data

**Cloud API** (ctext.org and similar):
- **Pros**: No infrastructure, pay-as-you-go, always updated
- **Cons**: Ongoing costs, rate limits, dependency on vendor
- **Best for**: Smaller projects, prototypes, variable usage

**Hybrid** (Local processing + cloud corpus):
- **Pros**: Balance of control and convenience
- **Cons**: More complex architecture
- **Best for**: Production applications with moderate volume

## Cost Considerations

### Pricing Models

**If you build in-house:**

**Development costs:**
- **Minimal (segmentation only)**: $25K-75K (3-6 months, 1 developer)
- **Full pipeline (POS + parsing + NER)**: $200K-500K (12-24 months, 2-3 developers + linguist)

**Operating costs (annual):**
- **Infrastructure**: $2K-15K (depending on usage volume)
- **Maintenance**: $20K-50K (10-20 hours/month engineering time)
- **Data/API access**: $60-500 (ctext.org subscription tiers)

**If you buy/license (when available):**
- **Per-user subscriptions**: $5-15/month per user (for tools like Pleco)
- **Enterprise licensing**: $500-5,000/year for institutions
- **API usage**: $0.01-0.10 per 1,000 characters processed (estimated)

### Break-Even Analysis

**Example: Building a Reading Assistant for Students**

**Development**: $100K (6 months, small team)
**Operating**: $25K/year (hosting + maintenance)
**Total Year 1**: $125K

**Revenue Scenarios**:
- **Conservative**: 500 users @ $10/month = $60K/year → 3 years to break even
- **Moderate**: 2,000 users @ $10/month = $240K/year → 6 months to break even
- **Optimistic**: 5,000 users @ $10/month = $600K/year → Profitable immediately

**Key variables**: User acquisition cost, conversion rate, churn rate

**Market size constraint**: Global Classical Chinese student population is 50K-200K, so market ceiling is real.

### Hidden Costs

**Training Data Creation**: If you need annotated corpus for ML models:
- **Cost**: $50-150 per hour for expert annotation
- **Volume needed**: 1,000-5,000 sentences for basic model
- **Total**: $20K-60K for quality training data

**Domain Expertise**: You need linguists who understand Classical Chinese:
- **Consultant rate**: $100-200/hour
- **Time needed**: 40-200 hours over project
- **Total**: $4K-40K

**Maintenance and Evolution**:
- **Model retraining**: As you get more data, models improve
- **Bug fixes**: Edge cases emerge in production
- **Feature expansion**: Users request new capabilities
- **Budget**: 20-30% of initial development cost annually

## Implementation Reality

### Realistic Timeline Expectations

**Minimal viable product (reading assistant with segmentation):**
- **Planning**: 2-4 weeks
- **Development**: 8-12 weeks
- **Testing**: 2-4 weeks
- **Total**: 3-5 months

**Production-ready platform (full NLP pipeline):**
- **Year 1**: Segmentation + POS tagging + basic UI
- **Year 2**: Parsing + NER + research tools
- **Year 3**: Refinement + scale + community
- **Total**: 2-3 years to maturity

**Don't expect**: Overnight solutions. This is a research problem being turned into engineering.

### Team Skill Requirements

**Minimum team:**
- **1 NLP engineer**: Python, ML frameworks (spaCy, PyTorch)
- **1 Classical Chinese linguist**: Part-time consultant
- **1 full-stack developer**: For UI/API (if building product)

**Ideal team:**
- **2 NLP engineers**: Faster development, knowledge redundancy
- **1 linguist**: Ongoing consultation and validation
- **1 product manager**: If commercial product
- **1 full-stack developer**: For polished UX

**Skills gap to watch**:
- Finding someone with BOTH NLP skills AND Classical Chinese knowledge is rare
- Budget for training or two-person pairing

### Common Pitfalls and Misconceptions

**Pitfall 1: "Modern Chinese tools will mostly work"**
- **Reality**: They'll get 60-70% accuracy. That sounds okay but creates frustrating user experience.
- **Mitigation**: Test early, be prepared to build custom solution

**Pitfall 2: "We can train a model with just a few hundred examples"**
- **Reality**: Deep learning needs thousands of examples. Rule-based or hybrid approaches needed with limited data.
- **Mitigation**: Start rule-based, incrementally add ML as you gather data

**Pitfall 3: "Once it's 85% accurate, we're done"**
- **Reality**: The last 10-15% accuracy takes 80% of the time. And users notice errors.
- **Mitigation**: Design UX that gracefully handles errors (easy correction, confidence scores)

**Pitfall 4: "This is a software problem"**
- **Reality**: It's a linguistics problem that requires software. Domain expertise is critical.
- **Mitigation**: Partner with Classical Chinese scholars from day one

**Pitfall 5: "We'll build everything ourselves"**
- **Reality**: Leveraging existing tools (Jiayan, ctext.org) is much faster
- **Mitigation**: Build on existing foundations, contribute improvements back

### First 90 Days: What to Expect

**Weeks 1-4: Foundation**
- Set up development environment
- Integrate Jiayan for segmentation
- Set up ctext.org API access
- Create test dataset (100-200 sentences manually annotated)
- **Deliverable**: Proof-of-concept that can segment sample texts

**Weeks 5-8: Core Features**
- Build basic POS tagger (rule-based)
- Create simple web UI for testing
- Test with 10-20 beta users (students/researchers)
- Gather feedback on accuracy and usability
- **Deliverable**: Alpha version testable by friendly users

**Weeks 9-12: Refinement**
- Fix bugs found by beta users
- Improve accuracy based on error analysis
- Add most-requested features
- Prepare for broader beta launch
- **Deliverable**: Beta ready for 100+ users

**What success looks like at 90 days:**
- 75-80% segmentation accuracy on test set
- 10-20 engaged beta users providing feedback
- Clear understanding of what features matter most
- Validated technical approach (or clear pivot if not working)

**What to worry about if:**
- Accuracy is below 70% (need to rethink approach)
- Users aren't finding it useful (product-market fit issue)
- Technical debt is piling up (need to refactor)
- Costs are exceeding budget (scope creep)

---

## Executive Recommendation

**For CTOs and Engineering Directors:**

If you're considering Classical Chinese parsing for your product or research infrastructure:

**Green light ✅ if you have:**
- $100K-500K budget over 12-24 months
- Access to Classical Chinese linguistic expertise
- Long-term commitment (not a side project)
- Realistic expectations (niche market, not hockey-stick growth)

**Yellow light ⚠️ if you're:**
- Hoping for quick ROI (this is a 2-3 year play)
- Expecting 95%+ accuracy immediately (80-85% is achievable goal)
- Treating it as pure software problem (linguistics expertise required)

**Red light ❌ if you:**
- Need production-ready tool tomorrow (doesn't exist)
- Can't commit resources for 12+ months (won't reach viability)
- Have no Classical Chinese domain access (will fail without expertise)
- Expect huge market (it's niche, be realistic)

**Bottom line**: This is a solvable problem with real user needs and achievable technical solutions. The market is small but underserved, and the timing is good (gap exists, components available). For organizations with the right expectations and resources, it's a viable opportunity that could have significant academic or commercial impact.

**The field needs someone to build this. The question is: Is it you?**
