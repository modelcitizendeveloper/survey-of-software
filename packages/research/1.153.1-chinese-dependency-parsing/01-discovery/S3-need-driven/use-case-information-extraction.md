# Use Case: Information Extraction from Chinese Text

## Who Needs This

**Data analysts and automation engineers** extracting structured information from unstructured Chinese text:
- Financial analysts monitoring Chinese news for investment signals
- Market research firms tracking product mentions and sentiment
- Government agencies monitoring social media for public opinion
- Legal tech companies extracting clauses from Chinese contracts
- Pharmaceutical companies mining Chinese medical literature

## Why Dependency Parsing Matters

### Entity Relationship Extraction

Chinese news and documents express relationships through grammatical dependencies:

**Financial news**: "阿里巴巴收购了饿了么" (Alibaba acquired Ele.me)
- Dependency structure reveals:
  - Subject (acquirer): "阿里巴巴" (Alibaba)
  - Action: "收购" (acquired)
  - Object (target): "饿了么" (Ele.me)

Without dependency parsing, NER alone gives you:
- ORG: Alibaba
- ORG: Ele.me
- But misses WHO acquired WHO

**Contract extraction**: "甲方应在收到货物后十个工作日内付款"
- Party: "甲方" (Party A)
- Obligation: "付款" (pay)
- Condition: "收到货物后" (after receiving goods)
- Deadline: "十个工作日内" (within 10 business days)

### Event Extraction

News monitoring requires understanding event structures:

**Example**: "昨天晚上北京发生了一起交通事故，造成三人受伤"
- Event type: Traffic accident
- Location: "北京" (Beijing)
- Time: "昨天晚上" (last night)
- Consequence: "三人受伤" (three people injured)

Dependency parsing links:
- "发生" (occurred) as the root
- "事故" (accident) as direct object
- Time and location as modifiers
- "造成" (caused) introduces the consequence clause

### Distinguishing Active vs. Passive Relationships

Chinese passive constructions affect who did what:

**Active**: "公司解雇了张三" (Company fired Zhang San)
- Agent: company
- Patient: Zhang San

**Passive (被-construction)**: "张三被公司解雇了" (Zhang San was fired by company)
- Same semantic roles, reversed word order
- "被" marker signals passive
- Dependency parsing identifies true agent/patient

**Passive (implicit)**: "这个问题已经解决了" (This problem has been solved)
- No explicit agent
- Dependency parsing reveals "问题" is patient, agent unknown

## Real-World Impact

### Financial News Monitoring

**Bloomberg/Reuters China desks** extracting market-moving events:

**News**: "腾讯第二季度净利润同比增长29%"
- Company: "腾讯" (Tencent)
- Metric: "净利润" (net profit)
- Change: "增长29%" (increased 29%)
- Period: "第二季度" (Q2)
- Comparison: "同比" (year-over-year)

**Value**: Automated extraction feeds trading algorithms
- Speed matters: First to extract = trading advantage
- Accuracy matters: Wrong relationship = wrong trade

**Error cost**: In 2015, a mistranslation of Chinese regulatory news caused $500M in trading losses

### Supply Chain Monitoring

**Multinational companies** tracking supplier mentions in Chinese news:

**News**: "富士康因环保问题被罚款500万元"
- Company: "富士康" (Foxconn)
- Issue: "环保问题" (environmental issues)
- Action: "被罚款" (was fined)
- Amount: "500万元" (5 million yuan)

**Value**: Early warning system for supply chain risks
- Dependency parsing identifies company-risk relationships
- Distinguishes "Company X reported on Company Y's fine" from "Company X was fined"

### Legal Contract Analysis

**Law firms** reviewing Chinese M&A contracts:

**Clause**: "如果目标公司未能在截止日前完成审计，买方有权终止本协议"
- Condition: "目标公司未能...完成审计" (target company fails to complete audit)
- Deadline: "截止日前" (before deadline)
- Right: "买方有权终止" (buyer can terminate)
- Object: "本协议" (this agreement)

**Value**: Automated extraction of:
- Conditional clauses (if-then structures)
- Rights and obligations
- Deadlines and triggers

**Manual review**: Senior lawyer takes 2 hours per contract
**Automated extraction**: Flag critical clauses in 2 minutes, lawyer reviews flagged items

### Medical Literature Mining

**Pharmaceutical R&D** extracting drug-disease relationships from Chinese medical journals:

**Text**: "临床试验表明，该药物能有效降低高血压患者的收缩压"
- Drug: "该药物" (this drug)
- Effect: "降低" (reduce)
- Target: "收缩压" (systolic blood pressure)
- Population: "高血压患者" (hypertensive patients)
- Evidence: "临床试验表明" (clinical trials show)

**Value**: Building knowledge graphs of Chinese medical research
- Dependency parsing links drug → effect → disease
- Distinguishes correlation vs. causation markers

### Social Media Monitoring

**Consumer brands** tracking product sentiment on Weibo/WeChat:

**Post**: "这款手机的电池续航太差了，用不到一天就没电"
- Product: "手机" (phone)
- Feature: "电池续航" (battery life)
- Sentiment: "太差了" (too poor)
- Evidence: "用不到一天就没电" (dies in less than a day)

**Value**:
- Identify which product features get complaints
- Dependency parsing links sentiment to specific features
- Aggregate over millions of posts for product improvement insights

## Libraries Used in Production

**HanLP**
- Used by: Chinese fintech companies, market research firms
- Strength: Joint NER + dependency parsing
- Speed: Can process news feeds in real-time

**LTP (Language Technology Platform)**
- Used by: Baidu, Chinese government agencies
- Strength: Includes semantic role labeling (SRL)
- SRL identifies "who did what to whom" explicitly

**Stanford CoreNLP**
- Used by: International firms analyzing Chinese sources
- Strength: Universal Dependencies standard, research-grade
- Limitation: Slower, Java runtime

**spaCy + custom Chinese models**
- Used by: Data science teams familiar with spaCy
- Strength: Python-native, integrates with pandas/scikit-learn
- Customization: Can train domain-specific models

## When Dependency Parsing Isn't Enough

**Coreference resolution**:
- "阿里巴巴收购了饿了么。这项交易价值95亿美元"
- "这项交易" (this deal) refers to the acquisition
- Dependency parsing structures each sentence, but doesn't link "交易" to "收购"

**Temporal reasoning**:
- "公司在IPO后，收入增长了50%"
- "后" (after) signals temporal sequence
- Dependency parsing shows grammatical link, but temporal reasoner needed for timeline

**Negation scope**:
- "公司没有在第三季度完成融资"
- "没有" (didn't) negates "完成融资" (complete financing)
- Dependency parsing shows negation, but scope resolution requires semantic analysis

**Implicit information**:
- "这家公司很有前途" (This company has good prospects)
- Positive sentiment, but no explicit event/relationship
- Sentiment analysis + domain knowledge needed

## Performance Requirements

**News monitoring (real-time)**:
- Latency: <1 second per article
- Throughput: 1000s of articles/day
- Solution: Streaming pipeline with parallel parsing

**Contract analysis (batch)**:
- Accuracy > speed
- Can take minutes per contract
- Solution: Ensemble models, human-in-the-loop verification

**Social media (high volume)**:
- Throughput: 100K+ posts/day
- Latency: <100ms per post
- Solution: Lightweight models, GPU acceleration, sampling

## Accuracy vs. Coverage Trade-offs

**High-accuracy (90%+)**:
- Use case: Legal contracts, financial filings
- Approach: Ensemble models, domain-specific parsers, human verification

**High-coverage (70-80% accuracy acceptable)**:
- Use case: Social media monitoring, trend detection
- Approach: Fast single-model parsing, statistical aggregation compensates for errors

**Example**: Brand monitoring on Weibo
- 10,000 posts/day mentioning brand
- 75% accuracy = 2,500 errors
- But aggregated statistics (% negative) still reliable
- Cost of human verification: Prohibitive
