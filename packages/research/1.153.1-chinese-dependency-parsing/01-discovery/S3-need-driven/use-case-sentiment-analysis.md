# Use Case: Sentiment Analysis and Opinion Mining

## Who Needs This

**Business intelligence teams** analyzing Chinese customer sentiment:
- E-commerce platforms (Alibaba, JD.com) - product review analysis
- Social media monitoring companies - brand reputation management
- Financial services - market sentiment from Chinese news/social media
- Hotel/restaurant chains - Chinese customer feedback analysis
- Automotive companies - Chinese consumer sentiment on new models
- Government agencies - public opinion monitoring on Weibo/WeChat

## Why Dependency Parsing Matters

### Aspect-Based Sentiment Analysis

Customer reviews often contain mixed sentiment about different product aspects:

**Review**: "这款手机的屏幕很好，但是电池续航太差了"
(This phone's screen is great, but battery life is too poor)

**Sentiment by aspect**:
- Screen: POSITIVE ("很好" = very good)
- Battery life: NEGATIVE ("太差" = too poor)

**Dependency parsing identifies**:
- "屏幕" (screen) ← "好" (good) [nsubj-att relationship]
- "续航" (battery life) ← "差" (poor) [nsubj-att relationship]

**Without parsing**: Bag-of-words sees "good" and "poor", can't assign to aspects
**Value**: Know WHICH features to improve vs. keep

### Negation and Its Scope

Chinese uses various negation markers with different scopes:

**"不" (bu) negation**: "这个产品不好" (This product is not good)
- "不" directly modifies "好"
- Sentiment: NEGATIVE

**"没有" (méiyǒu) negation**: "服务没有想象中好" (Service is not as good as expected)
- "没有" negates comparison
- Sentiment: NEGATIVE (but milder than "不好")

**Double negation**: "不是不好" (Not that it's not good = It's actually good)
- Two negations cancel
- Sentiment: POSITIVE (or neutral)

**Negation scope ambiguity**: "不是所有功能都好用"
(Not all functions are useful)
- Does "不" negate "所有" (not all) or "好用" (all not useful)?
- Correct parse: "not all" → mixed sentiment
- Wrong parse: "all not useful" → purely negative

**Dependency parsing** identifies negation head and its scope boundary

### Modifier-Head Relationships and Intensity

Sentiment intensity depends on modifier-head dependencies:

**Intensifiers**:
- "非常好" (very good) - "非常" intensifies "好"
- "特别差" (especially bad) - "特别" intensifies "差"
- "极其满意" (extremely satisfied) - "极其" intensifies "满意"

**Diminishers**:
- "还算不错" (fairly decent) - "还算" weakens positive
- "有点差" (a bit poor) - "有点" weakens negative

**Without dependency parsing**: Treat "非常" and "有点" equally as modifiers
**With parsing**: Understand modifier type and calculate adjusted sentiment score

### Contrastive Structures

Chinese reviews often use contrastive conjunctions:

**"虽然...但是" (although...but)**: "虽然价格贵，但是质量很好"
(Although price is high, but quality is very good)
- Concession: price (negative aspect)
- Main claim: quality (positive aspect)
- Overall sentiment: POSITIVE (main clause dominates)

**"不但...而且" (not only...but also)**: "不但便宜，而且好用"
(Not only cheap, but also useful)
- Both clauses positive, cumulative
- Overall: STRONGLY POSITIVE

**Dependency parsing** identifies which clause is main vs. subordinate for proper weighting

### Implicit Sentiment Through Comparison

Chinese expresses sentiment via comparisons requiring structural analysis:

**Better-than**: "比我之前用的好多了" (Much better than what I used before)
- Comparative structure: "比...好"
- "好" modified by "多" (much)
- Implicit: Previous product was worse
- Current product: POSITIVE

**Not-as-good-as**: "没有上一代好" (Not as good as previous generation)
- Comparative: "没有...好"
- Sentiment: NEGATIVE (downgrade from before)

**Dependency parsing** identifies comparative head and direction of comparison

## Real-World Impact

### E-commerce Product Reviews (Taobao/JD.com)

**Scale**: Millions of Chinese product reviews daily
**Business value**: Product improvement, customer retention, review summarization

**Example - Phone review**:
"外观设计很漂亮，拍照效果也不错，但是系统经常卡顿，客服态度很差"
(Design is beautiful, camera is decent, but system often lags, customer service attitude is poor)

**Aspect-sentiment extraction**:
- Design: POSITIVE ("漂亮" = beautiful)
- Camera: POSITIVE ("不错" = decent)
- System: NEGATIVE ("卡顿" = lag)
- Customer service: NEGATIVE ("差" = poor)

**Action**:
- Product team: Fix system performance (negative sentiment)
- Marketing: Highlight design in ads (positive sentiment)
- Customer service: Training needed (negative sentiment)

**ROI**:
- 5% improvement in negative aspect → 2% reduction in returns
- Returns cost ~$50M/year → $1M saved per 1% reduction

### Brand Reputation Monitoring (Weibo/WeChat)

**Social listening companies** (DataEye, Miaozhen) monitoring Chinese social media:

**Post**: "刚买的特斯拉就出问题了，客服推来推去，太失望了"
(Just bought Tesla and it has problems, customer service passes the buck, so disappointed)

**Extracted**:
- Brand: Tesla
- Issue: Product defect ("出问题")
- Issue: Customer service ("推来推去" = passing the buck)
- Sentiment: NEGATIVE ("失望" = disappointed)

**Crisis detection**:
- Spike in negative sentiment → alert brand manager
- Common complaint pattern → escalate to product team
- Time-critical: Respond before negative sentiment spreads

**Case study - 2018**:
- Chinese brand detected quality issue from social sentiment spike
- Issued recall before government investigation
- Cost: $10M recall
- Avoided: $100M+ in fines, brand damage

### Financial Market Sentiment

**Hedge funds and trading firms** analyzing Chinese financial news and social media:

**News headline**: "阿里巴巴第三季度业绩超预期，股价大涨"
(Alibaba Q3 results exceed expectations, stock price surges)

**Sentiment extraction**:
- Company: Alibaba
- Metric: Q3 results
- Performance: "超预期" (exceed expectations) → POSITIVE
- Market reaction: "大涨" (surge) → POSITIVE

**Dependency parsing role**:
- "业绩" (results) ← "超预期" (exceed expectations) [performance link]
- "股价" (stock price) ← "大涨" (surge) [market reaction link]
- Distinguishes prediction vs. actual outcome

**Trading impact**:
- Automated trading triggered by sentiment score
- Milliseconds matter in high-frequency trading
- False positive = wrong trade = financial loss

**Accuracy requirement**: >95% for trading signals (vs. 80% acceptable for product reviews)

### Hotel/Restaurant Reviews (Dianping, Meituan)

**Chinese review aggregators** summarizing customer sentiment:

**Review**: "环境很优雅，菜品味道一般，服务员态度不太好，性价比还行"
(Environment very elegant, food taste average, server attitude not great, value for money okay)

**Aspect breakdown**:
- Environment: POSITIVE ("优雅" = elegant, "很" = very)
- Food: NEUTRAL ("一般" = average)
- Service: NEGATIVE ("不太好" = not great)
- Value: NEUTRAL-POSITIVE ("还行" = okay)

**Business use**:
- Restaurant owner sees: Environment is strength, service needs training
- Customers see: Automated summary "Good atmosphere, poor service" (most helpful)

**Dependency parsing challenges**:
- "不太好" = "not very good" (negation + degree modifier)
- Wrong parse: "not" + "very good" → very negative
- Correct parse: "not very good" → mildly negative

### Automotive Reviews (Autohome, Dongchedi)

**Chinese car buyers** researching vehicles on forums:

**Post**: "这款SUV空间确实大，开起来也挺舒服的，油耗就是有点高"
(This SUV space indeed large, drives quite comfortable, fuel consumption is a bit high)

**Extracted**:
- Space: POSITIVE ("大" = large, "确实" = indeed)
- Driving comfort: POSITIVE ("舒服" = comfortable, "挺" = quite)
- Fuel efficiency: NEGATIVE ("油耗高" = high fuel consumption, "有点" = a bit)

**Manufacturer use**:
- Marketing: Emphasize space and comfort
- Engineering: Investigate fuel efficiency improvement
- Competitive analysis: Compare sentiment across competing models

## Libraries Used in Production

**HanLP**
- Used by: Chinese e-commerce platforms, social media analytics
- Strength: Fast, accurate Chinese dependency parsing
- Integration: Combined with sentiment lexicons (HowNet, NTUSD)

**LTP (Language Technology Platform)**
- Used by: Baidu, Chinese sentiment analysis startups
- Strength: Semantic role labeling (SRL) helps identify opinion holder
- Example: "他觉得这个产品很好" → "他" (he) is opinion holder, "产品" (product) is target

**SnowNLP**
- Used by: Chinese NLP beginners, small businesses
- Strength: Simple API, built-in sentiment classification
- Limitation: Less accurate dependency parsing than HanLP/LTP

**TextMind, Rosette**
- Used by: International companies analyzing Chinese sentiment
- Strength: Multi-language support, enterprise SLAs
- Cost: More expensive than open-source alternatives

**Custom BERT-based models**
- Used by: Tech giants with ML teams (Alibaba, Tencent)
- Approach: Fine-tuned BERT for aspect extraction + sentiment
- Trend: Neural models implicit syntax, but dependency parsing aids training

## When Dependency Parsing Isn't Enough

**Sarcasm and irony**:
- Review: "真是太'好'了，用了一天就坏了" (Really 'great', broke after one day)
- Quotes around "好" signal sarcasm
- Dependency parsing sees positive word, needs pragmatics

**Cultural context**:
- "随便" (whatever/casual) can be positive (laid-back atmosphere) or negative (don't care attitude)
- Context: "服务很随便" (service is casual) → NEGATIVE (unprofessional)
- Context: "氛围很随便" (atmosphere is casual) → POSITIVE (relaxed)

**Implicit comparisons**:
- "还可以" (okay/acceptable) - absolute meaning: NEUTRAL
- But in Chinese review culture, implies "not great"
- Pragmatic interpretation: NEGATIVE-LEANING

**Emoji and internet slang**:
- "客服🐶都不理我" (customer service [dog emoji] ignores me)
- 🐶 = derogatory in Chinese internet slang
- Dependency parsing doesn't capture emoji sentiment

## Performance Requirements

**E-commerce (real-time review summarization)**:
- Latency: <1 second per review
- Throughput: 100K+ reviews/day per category
- Accuracy: 80%+ acceptable (statistical aggregation compensates)

**Brand monitoring (near real-time)**:
- Latency: <5 seconds per social media post
- Crisis detection: Aggregate every 15 minutes
- Accuracy: 85%+ (false alarms costly but tolerable)

**Financial sentiment (low-latency)**:
- Latency: <100ms for news headline
- Accuracy: 95%+ (wrong signal = bad trade)
- Cost of error: Potentially millions in wrong trades

**Batch analytics (overnight processing)**:
- Latency: Can process overnight
- Volume: 10M+ reviews for monthly report
- Accuracy: 90%+ for strategic insights

## Accuracy vs. Volume Trade-offs

**High-accuracy approach**:
- Ensemble models (HanLP + LTP + BERT)
- Human verification for uncertain cases
- Use case: Financial trading signals, crisis detection
- Cost: Higher compute, slower processing

**High-throughput approach**:
- Single lightweight model (HanLP only)
- No human verification
- Use case: E-commerce review aggregation, social media trends
- Rationale: Errors cancel out in statistical aggregates
