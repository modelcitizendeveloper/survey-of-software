# Use Case: Question-Answering Systems

## Who Needs This

**Search and knowledge companies** building Chinese QA systems:
- Baidu Search - Featured snippet extraction
- Alibaba's AliMe - E-commerce product Q&A
- Zhihu (Chinese Quora) - Automated answer ranking
- Legal tech companies - Contract and case law search
- Academic search platforms - Research paper Q&A

## Why Dependency Parsing Matters

### Matching Question Syntax to Answer Syntax

Chinese questions and answers often have parallel dependency structures:

**Question**: "谁发明了造纸术?" (Who invented papermaking?)
- Root: "发明" (invented)
- Subject (missing): WHO
- Object: "造纸术" (papermaking)

**Answer**: "蔡伦发明了造纸术" (Cai Lun invented papermaking)
- Root: "发明" (invented)
- Subject: "蔡伦" (Cai Lun)
- Object: "造纸术" (papermaking)

Dependency parsing reveals:
- Same verb root "发明"
- Same object "造纸术"
- Answer fills the missing subject slot

### Handling Complex Chinese Question Patterns

**"是...的" cleft constructions**:
- Question: "张三是在哪里出生的?" (Where was Zhang San born?)
- Answer: "张三是在北京出生的" (Zhang San was born in Beijing)
- Dependency parsing identifies "在哪里" (where) links to location in answer

**"多少/几" quantity questions**:
- Question: "中国有多少个省?" (How many provinces does China have?)
- Answer: "中国有34个省级行政区" (China has 34 provincial-level divisions)
- Parsing links quantity to the correct noun phrase

### Distinguishing Cause-Effect from Temporal Relations

**Temporal**: "他先吃饭再看书" (He eats first, then reads)
- "先...再..." indicates sequence, not causation

**Causal**: "因为下雨所以他没去" (Because it rained, he didn't go)
- "因为...所以..." indicates causation
- Dependency parsing distinguishes these patterns

## Real-World Impact

### Baidu Zhidao (Baidu Knows)
Community Q&A with 1 billion+ answers:
- Automatic answer suggestion: matches question dependencies to answer corpus
- Answer quality ranking: favors answers with complete dependency coverage

**Example**:
- Question: "怎么做红烧肉?" (How to make braised pork?)
- Good answer must have:
  - Root verb: "做" (make) or cooking verb
  - Object: "红烧肉" (braised pork)
  - Modifiers: steps, ingredients, time

### Legal Document Search
Law firms searching millions of Chinese legal documents:

**Query**: "合同违约的赔偿标准是什么?" (What are compensation standards for contract breach?)
- Key dependencies:
  - "违约" (breach) modifies "合同" (contract)
  - "赔偿标准" (compensation standard) is the question focus
- Must match legal text discussing contract breach compensation

**Cost of poor matching**:
- Lawyers waste hours reading irrelevant cases
- Missed precedents lead to weaker legal arguments

### E-commerce Product Q&A
Alibaba's customer service automation:

**Question**: "这款手机支持双卡吗?" (Does this phone support dual SIM?)
- Root: "支持" (support)
- Subject: "手机" (phone)
- Object: "双卡" (dual SIM)

**Product description**: "该手机采用双卡双待技术"
- Different wording but same dependency structure
- Dependency matching finds relevant answer

### Medical Knowledge Bases
Hospital chatbots answering patient questions:

**Question**: "感冒发烧吃什么药?" (What medicine for cold and fever?)
- Symptoms: "感冒" (cold), "发烧" (fever)
- Action: "吃" (take)
- Target: "什么药" (what medicine)

**Knowledge base entry**: "对于感冒引起的发烧，建议服用布洛芬"
- Dependency parsing matches symptom-treatment relationship
- Ensures answer addresses BOTH cold AND fever

## Libraries Used in Production

**HanLP**
- Used by: Alibaba AliMe, various QA startups
- Strength: Fast, accurate Chinese dependency parsing
- Integration: Works with Elasticsearch for answer retrieval

**Stanford CoreNLP**
- Used by: Academic QA research, Zhihu experiments
- Strength: Research-grade accuracy, Universal Dependencies output
- Limitation: Slower, requires Java runtime

**LTP (Language Technology Platform)**
- Used by: Baidu products, iFlytek
- Strength: Optimized for Chinese, includes semantic role labeling
- Integration: Cloud API available

**spaCy with Chinese models**
- Used by: International companies building Chinese QA
- Strength: Python-native, easy integration
- Limitation: Smaller Chinese training data vs. native Chinese tools

## When Dependency Parsing Isn't Enough

Modern QA systems layer dependency parsing with:

**Semantic matching**:
- "买" (buy) vs "购买" (purchase) - synonyms with same dependency role
- Embedding-based similarity catches semantic equivalence

**Entity linking**:
- "首都" (capital) → "北京" (Beijing) in context of China
- "他" (he) → specific person from previous context

**Answer type detection**:
- WHO question → expect PERSON entity
- WHERE question → expect LOCATION entity
- Dependency parsing alone doesn't guarantee type match

**Multi-hop reasoning**:
- Question: "谁是中国最大城市的市长?" (Who is the mayor of China's largest city?)
- Requires: Finding largest city (Shanghai) → Finding Shanghai's mayor
- Dependency parsing structures each hop, but reasoning engine connects them

## Performance Requirements

**Search engines (Baidu)**:
- Must parse millions of questions/day
- Latency: <50ms per question
- Solution: Pre-parsed answer corpus, runtime question parsing only

**Customer service chatbots**:
- Real-time response expected
- Latency: <200ms total (including parsing)
- Solution: Optimized models (HanLP), GPU acceleration

**Legal/medical search**:
- Accuracy > speed
- Can tolerate 500ms+ per query
- Solution: Ensemble models, comprehensive parsing
