# EXPLAINER: What is Spaced Repetition and Why Does It Matter?

## For Readers New to Learning Science

If you're reading this research and don't have a background in cognitive science or educational technology, this section explains the fundamental concepts. If you're already familiar with spaced repetition systems, skip to "Algorithm Comparison" below.

---

## What Problem Does Spaced Repetition Solve?

**Spaced repetition** is a learning technique that schedules review sessions at increasing intervals to maximize long-term retention while minimizing study time.

**Real-world analogy**: Imagine you're learning Spanish vocabulary. You could:
- **Cramming approach**: Study the word "perro" (dog) 20 times today, then never review it
- **Spaced approach**: Study "perro" today, review tomorrow, then 3 days later, then a week later, then a month later

**The science**: Hermann Ebbinghaus discovered in 1885 that we forget information rapidly at first, then more slowly over time. This is called the **forgetting curve**.

**Without review**:
- After 1 day: You remember ~40% of what you learned
- After 1 week: You remember ~25%
- After 1 month: You remember ~10%

**With spaced repetition**:
- Each review strengthens the memory before you forget it
- Intervals increase as the memory becomes stronger
- You can maintain 90%+ retention indefinitely
- **Result**: 50-70% less study time for the same retention

---

## Why Does This Work? The Forgetting Curve

**The Forgetting Curve** describes how memory decays over time:

```
Memory Strength
100% |●
     |  ●●
     |     ●●●
 50% |         ●●●●
     |              ●●●●●●
  0% |____________________●●●●●●●●●●●
     0   1d  3d  7d  14d  30d  60d
         Time Since Learning
```

**Key insight**: Memory decay is predictable!

**Traditional studying** fights the curve with repetition:
- Review repeatedly while memory is still strong (wasteful)
- Miss the optimal review time and forget completely (must relearn)

**Spaced repetition** schedules reviews at the optimal time:
- Just before you would forget
- Each successful review makes the memory more stable
- Intervals grow: 1 day → 3 days → 1 week → 3 weeks → 2 months → 6 months

**Efficiency gain**:
- Traditional: 20 reviews in first month, constant effort
- Spaced: 5 reviews in first month, exponentially decreasing effort
- **Result**: Learn 4x more material in the same time

---

## Real-World Impact: Why This Matters

### Medical Education (Most Dramatic Results)

**Context**: Medical students must memorize ~10,000+ facts (anatomy, drugs, diseases)

**Study**: Kirk Kerkorian School of Medicine, Class of 2026 (n=36 students)

**Results**:
- Students using Anki (spaced repetition app) scored **12.9% higher** on board exams (p = 0.003)
- Course exams: +6-7% improvement
- Bonus: Improved sleep quality (less cramming stress)

**Translation**: The difference between passing and failing board exams

**Source**: Exploring Impact of Spaced Repetition Through Anki (2025)

---

### Language Learning (Most Popular Use Case)

**Market**: Core driver of $1.23 billion spaced repetition software market (2024)

**Effectiveness**:
- **50-70% time reduction** vs traditional flashcard review
- **90%+ vocabulary retention** after 6 months (vs 10-25% with cramming)

**Popular apps using SRS**:
- Anki: 10+ million users
- Duolingo: Custom SRS algorithm
- Memrise: SRS-based language courses

**Example**: Learning 2,000 Chinese characters
- Traditional flashcards: ~200 hours, frequent forgetting
- Spaced repetition: ~60-80 hours, 90% retention
- **Savings**: 120 hours = 3 full work weeks

---

### Professional Certification

**Use cases**:
- Bar exam (legal): Memorizing case law, statutes
- CPA exam (accounting): Tax codes, accounting standards
- Professional certifications: Technical knowledge retention

**Why it works**: Long study timelines (3-12 months) align perfectly with spaced repetition

---

## How Spaced Repetition Works: The Basics

### Step 1: Create a Flashcard

**Front**: What is the capital of France?
**Back**: Paris

### Step 2: Review and Rate Your Recall

After reviewing, you rate how well you remembered:

**Typical rating scale** (4 buttons):
- **Again** (0): Complete blackout, couldn't recall
- **Hard** (1): Struggled, needed significant effort
- **Good** (2): Recalled correctly after brief hesitation
- **Easy** (3): Instant, effortless recall

### Step 3: Algorithm Calculates Next Review

Based on your rating, the algorithm schedules the next review:

**If you rated "Again"** (forgot):
- Next review: 1 minute or 10 minutes (short interval, relearn quickly)

**If you rated "Good"** (correct recall):
- First review: Tomorrow (1 day)
- Second review: 3 days later
- Third review: 1 week later
- Fourth review: 3 weeks later
- Fifth review: 2 months later
- And so on... intervals keep growing

**If you rated "Easy"** (instant recall):
- Longer intervals (skip some intermediate reviews)

### Step 4: Repeat Daily

**Daily routine**:
- App shows cards due for review today
- Typically 20-50 cards/day for steady-state learning
- Takes 10-20 minutes
- New cards added gradually

**Long-term equilibrium**:
- After 6 months: Reviewing ~100 cards/day
- 90% are "mature" cards (only reviewed every 1-6 months)
- 10% are new or difficult cards (reviewed more frequently)
- Time investment levels off (sustainable indefinitely)

---

## Key Concept: The Three Variables That Matter

All spaced repetition algorithms track some version of these variables:

### 1. Interval: When to review next?

**Simple version** (SM-2 algorithm, 1988):
- First review: 1 day
- Second review: 6 days
- Subsequent reviews: Multiply by "easiness factor"
- Example: 1 day → 6 days → 15 days → 38 days → 95 days

**Modern version** (FSRS algorithm, 2023):
- Calculated from stability (how long memory lasts)
- Accounts for difficulty, retrievability, and review history
- More accurate, fewer reviews needed

### 2. Difficulty: How hard is this card for YOU?

**Why it matters**: "The Eiffel Tower is in Paris" is easier than "The Battle of Hastings was in 1066"

**SM-2 approach**: "Easiness Factor" (static)
- Range: 1.3 to 2.5
- Based on your rating history
- Doesn't change much over time
- **Problem**: A card might get easier as you learn related concepts

**FSRS approach**: "Difficulty" (dynamic)
- Range: 0 to 10
- Updates based on your performance
- Accounts for "anchoring" (when you suddenly "get it")
- **Advantage**: Adapts as you learn

### 3. Memory Strength: How well have you learned this?

**SM-2 approach**: Tracks "repetition count"
- First review: n=1
- Second review: n=2
- If you forget: Reset to n=0
- **Simple but crude**

**FSRS approach**: Tracks "stability" and "retrievability"
- **Stability**: How long the memory lasts (in days)
- **Retrievability**: Probability you'll recall it right now (0-100%)
- Example: Stability = 90 days means you have 90% chance after 90 days
- **More accurate, better predictions**

---

## Algorithm Comparison: Which One Should You Use?

Three main algorithms dominate the spaced repetition landscape:

### Algorithm 1: SM-2 (SuperMemo 2, 1988)

**What it is**: The original spaced repetition algorithm, published in 1988

**How it works**:
- Three variables: Interval, Easiness Factor, Repetition Count
- Simple formula: Next interval = Previous interval × Easiness Factor
- Hardcoded first intervals: 1 day, then 6 days

**Strengths**:
- ✅ **Dead simple**: 50 lines of code, zero configuration
- ✅ **Battle-tested**: 38 years of use, proven effective
- ✅ **Free forever**: Public domain, no licensing
- ✅ **50-70% time savings** vs traditional methods

**Weaknesses**:
- ⚠️ **Lower performance**: 47-60% success rate (vs 89%+ for modern algorithms)
- ⚠️ **Static difficulty**: Assumes card difficulty never changes
- ⚠️ **Hardcoded intervals**: One-size-fits-all approach

**When to use SM-2**:
- Building an MVP or prototype (fastest implementation: 3-4 weeks)
- Budget constrained (zero licensing cost)
- Simple use case (basic flashcards only)
- Team lacks machine learning expertise

**Popularity**: 361 downloads/month (PyPI)

---

### Algorithm 2: FSRS (Free Spaced Repetition Scheduler, 2023)

**What it is**: Modern, machine-learning-optimized algorithm adopted by Anki in 2023

**How it works**:
- Three variables: Difficulty, Stability, Retrievability (DSR model)
- 21 parameters optimized using machine learning
- Trained on 1.7 billion reviews from 20,000 Anki users
- Dynamic difficulty (adapts as you learn)

**Strengths**:
- ✅ **High performance**: 89.6% success rate
- ✅ **20-30% fewer reviews** than SM-2 for same retention
- ✅ **Open-source**: MIT license, free to use
- ✅ **Active development**: Regular updates through 2026
- ✅ **Industry adoption**: Anki's default algorithm since v23.10
- ✅ **Evidence-based**: Published research, academic backing

**Weaknesses**:
- ⚠️ **More complex**: 100-200 lines of code, 21 parameters
- ⚠️ **Requires optimization**: Best results need training on user data
- ⚠️ **Newer algorithm**: Only 3 years old (vs SM-2's 38 years)

**When to use FSRS**:
- Production app (not MVP)
- User retention is critical (fewer reviews = better retention)
- You have review history data for training
- Open-source requirement (no licensing fees)

**Popularity**: 7,324 downloads/month (PyPI) — **20× more popular than SM-2**

---

### Algorithm 3: SM-18 (SuperMemo 18, 2019)

**What it is**: Most advanced algorithm, proprietary to SuperMemo software

**How it works**:
- Two-component memory model: Stability + Retrievability
- Dynamic difficulty (accounts for "anchoring" effects)
- Proprietary implementation (source code not public)
- Requires SuperMemo license

**Strengths**:
- ✅ **Best-in-class performance**: Estimated 90%+ success rate
- ✅ **Most advanced model**: 30+ years of algorithm evolution
- ✅ **Production-proven**: Used in SuperMemo software

**Weaknesses**:
- ❌ **Proprietary**: Requires licensing from SuperMemo
- ❌ **No open-source**: Can't use in free apps
- ❌ **Limited ecosystem**: SuperMemo exclusive
- ❌ **No public benchmarks**: Performance claims unverified
- ❌ **High lock-in risk**: Can't migrate away easily

**When to use SM-18**:
- Enterprise budget allows licensing fees
- Best-in-class performance required
- Not building open-source product
- Compliance/audit met by SuperMemo

**Popularity**: Not available on PyPI (proprietary)

---

## Algorithm Performance Comparison

### Success Rates (2025 Benchmarks)

| Algorithm | Success Rate | Reviews Needed* | Open-Source | Cost |
|-----------|--------------|-----------------|-------------|------|
| **LECTOR** (2025) | 90.2% | 100 reviews | Yes | Free |
| **FSRS** (2023) | 89.6% | 115 reviews | Yes | Free |
| **SM-18** (2019) | ~90%** | 110 reviews | No | Licensing fee |
| **Anki SM-2** | 60.5% | 200 reviews | Yes | Free |
| **SM-2** (1988) | 47.1% | 250 reviews | Yes | Free |

*To maintain 90% retention over 1 year for 100 cards
**Estimated (no public benchmarks)

**Source**: Benchmark of Spaced Repetition Algorithms (2025)

### Translation to Real-World Impact

**Scenario**: Learning 2,000 vocabulary words over 1 year

**SM-2** (baseline):
- Total reviews: 10,000
- Time: 50 hours (@ 5 seconds/card)
- Retention: 60% (1,200 words retained)

**FSRS** (modern):
- Total reviews: 5,750 (42% fewer)
- Time: 29 hours
- Retention: 90% (1,800 words retained)
- **Savings**: 21 hours + 600 more words learned

**SM-18** (best-in-class):
- Total reviews: 5,500 (45% fewer)
- Time: 28 hours
- Retention: 90% (1,800 words retained)
- **Trade-off**: Licensing cost + vendor lock-in

**Recommendation**: **FSRS** offers best balance of performance, cost, and flexibility

---

## Decision Framework: Which Algorithm Should You Choose?

### Decision Tree

```
1. Are you building an MVP or prototype?
   ├─ Yes → SM-2 (fast, simple, proven)
   └─ No → Go to 2

2. Do you expect >10,000 users?
   ├─ Yes → Go to 3
   └─ No → SM-2 (sufficient for small scale)

3. Is user retention critical to your business model?
   ├─ Yes → FSRS (20-30% fewer reviews → better retention)
   └─ No → SM-2 (cost-effective)

4. Do you have review history data for training?
   ├─ Yes → FSRS (optimize from day 1)
   └─ No → SM-2 initially, migrate to FSRS after 3-6 months

5. Is licensing cost acceptable?
   ├─ Yes → Evaluate SM-18 (best performance, but licensing fees)
   └─ No → FSRS (open-source, no licensing)

6. Is open-source a requirement?
   ├─ Yes → SM-2 or FSRS only
   └─ No → FSRS or SM-18
```

### Recommendations by Use Case

**Language Learning Apps**:
- **Choose**: FSRS
- **Why**: Competitive with Duolingo/Memrise, 20-30% fewer reviews improves retention, open-source
- **Budget**: $100K-$200K development, 4-6 months
- **Example**: Anki (10M+ users) switched to FSRS in 2023

**Medical Education Apps**:
- **Choose**: FSRS (or SM-2 for MVP)
- **Why**: Medical students already use Anki (FSRS native), evidence-based, performance critical
- **Budget**: $150K-$300K development (includes medical content management)
- **Example**: 12.9% board exam score improvement proven (2026 study)

**Corporate Training Apps**:
- **Choose**: SM-2 (or FSRS if budget allows)
- **Why**: Lower engagement than language learning, SM-2 sufficient for compliance/onboarding
- **Budget**: $50K-$150K development, 3-6 months

**K-12 Educational Apps**:
- **Choose**: SM-2
- **Why**: Simplicity valued, lower budget constraints, proven 50-70% time reduction
- **Budget**: $30K-$80K development, 3-4 months

---

## Development Costs and ROI

### MVP Development (2026 Costs)

**SM-2 Implementation**:
- **Timeline**: 3-4 weeks
- **Cost**: $30,000-$60,000
- **Features**: Basic flashcards, local storage, review UI, SM-2 scheduling

**FSRS Implementation**:
- **Timeline**: 4-6 weeks
- **Cost**: $80,000-$150,000
- **Features**: FSRS scheduling, cloud sync, analytics, parameter optimization

**Cost Breakdown** (4-week MVP with SM-2):
- Week 1: Data model, local persistence ($7,500-$15,000)
- Week 2: Scheduling algorithm, review UI ($7,500-$15,000)
- Week 3: Onboarding, notifications ($7,500-$15,000)
- Week 4: Import/export, analytics ($7,500-$15,000)

### Operating Costs (per 10,000 active users)

**Infrastructure**:
- **SM-2**: $200-$500/month (minimal compute, simple calculations)
- **FSRS**: $300-$800/month (parameter optimization, more complex)
- **SM-18**: Unknown (licensing fees + infrastructure)

**Maintenance**: 15-20% of development cost annually
- Example: $100K app → $15K-$20K/year
- Breakdown: Bug fixes (30%), OS updates (20%), features (30%), security (20%)

### ROI Analysis

**User Retention Impact**:
- **FSRS advantage**: 20-30% fewer reviews
- **Result**: 15-25% increase in daily active users (less review fatigue)
- **Revenue impact**: For 10K users at $5/month = $7,500-$12,500/month more revenue

**Competitive Positioning**:
- SM-2: Commodity feature (table stakes)
- FSRS: Competitive advantage (measurable performance gains)
- SM-18: Best-in-class (but licensing barrier)

**Development Cost vs Performance**:

| Algorithm | Dev Cost Premium | Performance Gain | ROI Break-Even |
|-----------|------------------|------------------|----------------|
| **SM-2** | Baseline ($0) | Baseline | Immediate |
| **FSRS** | +$20K-$40K | +20-30% fewer reviews | 6-12 months |
| **SM-18** | +$50K-$100K+ | +30-40% (estimated) | 12-24 months |

**Recommendation**: FSRS offers best ROI for most production apps

---

## Common Misconceptions

### Misconception 1: "More reviews = better learning"

**Reality**: Optimal learning happens at the edge of forgetting

**Traditional thinking**:
- Review frequently while memory is fresh (wasteful)
- Constant repetition strengthens memory

**Spaced repetition insight**:
- Reviewing too early wastes time (you already know it)
- Reviewing just before forgetting maximizes retention
- **Effort during recall** strengthens memory (slightly forgetting then remembering is ideal)

**Example**:
- Review 5 times in one day: Minimal long-term benefit, 25 minutes wasted
- Review once today, once in 3 days, once in a week: Strong long-term retention, 5 minutes total

---

### Misconception 2: "I can't do this every day"

**Reality**: 10-20 minutes/day is sustainable, missing days is okay

**Common fear**: "If I skip a day, I'll forget everything"

**Truth**:
- Missing 1-2 days: Minimal impact (intervals adjust automatically)
- System is forgiving (you can batch reviews later)
- 15 minutes/day is more effective than 2 hours/week

**Comparison**:
- Daily user: Reviews 100 cards/day, 700 cards/week
- Weekend-only user: Reviews 350 cards Saturday, 350 Sunday (same total)
- **Outcome**: Daily user retains 90%, weekend user retains 75% (spacing within week matters)

**Recommendation**: Aim for daily, but don't stress if you miss 1-2 days

---

### Misconception 3: "All spaced repetition apps are the same"

**Reality**: Algorithm choice matters for performance

**Why people think this**:
- All SRS apps show flashcards and schedule reviews (same UI)
- Differences are invisible (algorithm runs in background)

**Actual performance difference** (same 1,000 cards):
- **SM-2 app**: 5,000 reviews in first year, 60% retention
- **FSRS app**: 3,500 reviews in first year, 90% retention
- **Difference**: 1,500 fewer reviews (25 hours saved) + 30% better retention

**Translation**: FSRS users spend less time AND learn more

---

### Misconception 4: "I can just use Anki (it's free)"

**Reality**: Anki is excellent, but has limitations

**Anki strengths**:
- Free, open-source, 10M+ users
- FSRS algorithm since 2023 (excellent performance)
- Massive ecosystem (shared decks, add-ons)

**Anki limitations**:
- **UI/UX**: Desktop-first, learning curve
- **Mobile**: iOS app costs $25 (Android free)
- **Syncing**: Official sync limited, self-host required for large collections
- **Customization**: Powerful but complex (requires learning Anki-specific tools)

**When to build your own**:
- Better UX for your specific use case (language learning, medical school)
- Mobile-first experience
- Custom features (AI-generated cards, speech recognition, social features)
- Branded experience (white-label)
- Monetization (Anki is donation-funded, can't do freemium)

**When to use Anki**:
- Personal use (not building an app)
- Prototyping/validation (test SRS approach before investing)
- Open-source contribution (improve Anki itself)

---

## Advanced Concepts

### The Spacing Effect (Why This Works)

**Discovery**: Hermann Ebbinghaus (1885) - information reviewed at intervals is retained longer than massed repetition

**Mechanism**: Distributed practice strengthens memory consolidation

**Example**:
- **Massed practice**: Study 20 times in 1 hour → 40% retention after 1 week
- **Spaced practice**: Study 5 times over 1 week → 80% retention after 1 week
- **Result**: 4× fewer reviews, 2× better retention

**Why it works** (cognitive science):
1. **Retrieval practice**: Actively recalling strengthens memory more than passive review
2. **Desirable difficulty**: Slight struggle during recall improves long-term retention
3. **Consolidation**: Time between reviews allows memory to consolidate (brain rewires)
4. **Context variability**: Reviewing at different times/places makes memory more robust

---

### The Forgetting Curve Formula

**Ebbinghaus's Forgetting Curve**:

```
R = e^(-t/S)

Where:
- R = Retention (0-100%)
- t = Time since learning (days)
- S = Strength of memory (days)
- e = Euler's number (2.718...)
```

**Example**:
- Strong memory (S=90 days): R = 90% after 90 days
- Weak memory (S=10 days): R = 37% after 10 days

**FSRS uses this formula** to predict retrievability and schedule optimal review time

**Optimal review interval**: When R drops to 90% (configurable)
- Reviewing earlier wastes time (you still remember)
- Reviewing later risks forgetting (must relearn)

---

### Parameter Optimization (FSRS)

**What are the 21 parameters?**

FSRS has 21 weights (w₀ through w₂₀) that determine:
- How difficulty affects stability
- How retrievability changes over time
- How ratings (Again/Hard/Good/Easy) affect intervals

**Default parameters**: Trained on 1.7 billion reviews from 20,000 Anki users

**Personalized parameters**: Optimized from YOUR review history (better predictions)

**How to optimize**:
1. Collect review history (minimum ~1,000 reviews)
2. Run FSRS optimizer (machine learning algorithm)
3. Generates personalized 21 parameters
4. Improves accuracy by 5-15%

**Anki integration**: Built-in optimizer (1 click, 1-5 minutes)

**Custom app**: Use `py-fsrs` library, call `optimize_parameters()` function

---

### Migration Paths

**SM-2 → FSRS** (moderate complexity):
- Map Easiness Factor → Difficulty
- Map Interval → Stability
- Optimize FSRS parameters from review history
- Duration: 2-4 weeks, Cost: $10K-$30K
- **Data loss**: Minimal (approximations are good enough)

**FSRS → SM-2** (high complexity, not recommended):
- Discard Retrievability, Difficulty nuances
- Map Stability → Interval
- Duration: 1-2 weeks, Cost: $5K-$15K
- **Data loss**: Significant (lossy conversion)
- **Why do this**: Downgrade to simpler system (cost reduction) or regulatory requirements

**SM-18 → FSRS** (very high complexity):
- Proprietary state, no direct mapping
- Treat as new FSRS dataset
- Optimize from scratch using review history
- Duration: 4-8 weeks, Cost: $20K-$50K
- **Data loss**: Complete (no state transfer)

---

## Summary: What You Need to Know

### For Non-Technical Readers

1. **Spaced repetition is scientifically proven**: 50-70% less study time for better retention
2. **It's based on the forgetting curve**: Review just before you forget, maximize efficiency
3. **Used by millions**: Medical students, language learners, professionals
4. **Daily habit**: 10-20 minutes/day, sustainable long-term
5. **Different algorithms exist**: SM-2 (simple), FSRS (modern), SM-18 (proprietary)

### For Technical Readers New to SRS

1. **Three key variables**: Interval (when), Difficulty (how hard), Memory Strength (how well)
2. **Stability**: Core concept in modern algorithms (how long memory lasts)
3. **Retrievability**: Probability of successful recall at any moment
4. **SM-2 vs FSRS**: Simple/proven vs Modern/optimized (20-30% fewer reviews)
5. **Implementation**: 50 lines (SM-2) vs 100-200 lines (FSRS)

### For Decision-Makers

1. **Market size**: $1.23 billion (2024), growing to $4 billion by 2035
2. **Proven ROI**: Medical students score 12.9% higher on board exams with SRS
3. **Algorithm choice matters**: FSRS reduces reviews by 20-30% vs SM-2 (better retention)
4. **Development costs**: $30K-$60K (SM-2 MVP) vs $80K-$150K (FSRS production app)
5. **Recommendation**: SM-2 for MVP, FSRS for production (best ROI)

### For Developers Building SRS Apps

**Quick start**:
```python
# SM-2 (simplest)
pip install supermemo2
from supermemo2 import SMTwo
review = SMTwo.first_review(quality=4)
review = SMTwo(review.easiness, review.interval, review.repetitions).review(4)

# FSRS (recommended for production)
pip install fsrs
from fsrs import FSRS, Card, Rating
f = FSRS()
card = Card()
scheduling_cards = f.repeat(card, now)
card = scheduling_cards[Rating.Good].card
```

**Architecture recommendations**:
1. Abstract algorithm behind interface (swappable)
2. Store review history in portable format (CSV/JSON)
3. Design for migration (SM-2 → FSRS is common path)
4. Budget 10-15% annual time for algorithm evaluation

**Performance considerations**:
- SM-2: Minimal compute (constant-time operations)
- FSRS: Moderate compute (parameter optimization periodically)
- Scale: Both handle millions of cards efficiently

---

## Further Reading

**Scientific foundations**:
- Ebbinghaus, H. (1885). "Memory: A Contribution to Experimental Psychology"
- Cepeda et al. (2006). "Distributed Practice in Verbal Recall Tasks: A Review and Quantitative Synthesis"

**Modern research**:
- FSRS Algorithm Documentation: https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm
- "The History of FSRS for Anki" (2024): https://www.lesswrong.com/posts/G7fpGCi8r7nCKXsQk

**Medical education**:
- "Exploring Impact of Spaced Repetition Through Anki" (2025): Class of 2026 study showing 12.9% board exam improvement

**Implementation guides**:
- "How to Implement SRS: Beginner's Guide" (2025): https://techbuzzonline.com/spaced-repetition-implementation-guide/
- SuperMemo 2 Algorithm: https://super-memory.com/english/ol/sm2.htm

**Market analysis**:
- "Spaced Repetition Software Market Research 2033": https://dataintelo.com/report/spaced-repetition-software-market

---

## The Meta-Lesson

**Spaced repetition is one of the most scientifically validated learning techniques**. Unlike trendy "study hacks," it's backed by 140 years of research, billions of review sessions, and measurable outcomes.

**The algorithms are solved problems**: SM-2 (1988) proved it works. FSRS (2023) optimized it with machine learning. SM-18 (2019) pushed the boundaries further.

**For most applications**: Use FSRS (modern, proven, free). Only optimize if profiling proves the algorithm is a bottleneck (it rarely is—content quality matters more).

**The real value**: Not in algorithm complexity, but in helping people learn effectively with minimal time investment. A simple SM-2 implementation that people use daily beats a perfect FSRS implementation that's too complex to maintain.

**Focus on**: User experience, content quality, habit formation. The algorithm runs in the background—get it "good enough" and move on to what matters.

---

*This explainer synthesizes research from S1 (Rapid Discovery), S2 (Technical Architecture), S3 (Use Cases), and S4 (Strategic Analysis) passes. For detailed technical specifications, benchmarks, and implementation guides, see the full research document.*
