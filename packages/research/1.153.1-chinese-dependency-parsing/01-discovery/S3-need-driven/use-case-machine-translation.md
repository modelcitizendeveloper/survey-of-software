# Use Case: Machine Translation

## Who Needs This

**Translation technology companies** building Chinese-to-other or other-to-Chinese MT systems:
- Google Translate, DeepL, Microsoft Translator - consumer translation
- Alibaba Translate, Baidu Translate - China market leaders
- SDL, Lionbridge - enterprise translation services
- App/game localization companies - Chinese market expansion
- Subtitle translation services - Chinese media consumption

## Why Dependency Parsing Matters

### Preserving Grammatical Relationships Across Languages

Chinese and target languages often have different word orders but shared dependency structures:

**Chinese**: "我昨天在北京见了一个老朋友"
- Word order: I + yesterday + in Beijing + saw + one + old friend
- Dependencies:
  - "见" (saw) = root
  - "我" (I) = subject
  - "朋友" (friend) = object
  - "昨天" (yesterday) = time modifier
  - "在北京" (in Beijing) = location modifier

**English (SVO)**: "I saw an old friend in Beijing yesterday"
- Different word order (time/location at end)
- Same dependencies: see(I, friend) + time(saw, yesterday) + location(saw, Beijing)

**German (SOV in subordinate)**: "Ich habe gestern in Peking einen alten Freund gesehen"
- Verb at end in perfect tense
- Same underlying dependency structure

**Dependency-informed translation**:
- Identifies "见" as root → translates to main verb
- Attaches modifiers correctly regardless of target word order
- Avoids: "In Beijing yesterday I saw an old friend" (awkward)

### Resolving Structural Ambiguity

Chinese sentences often have multiple possible dependency structures:

**Example**: "我看见他在河边钓鱼"

**Parse 1**: I saw [him fishing by the river]
- "看见" (saw) = root
- "他在河边钓鱼" (him fishing by the river) = complement clause

**Parse 2**: I saw him [by the river] [fishing]
- "看见" (saw) = root
- "在河边" (by the river) modifies "看见"
- "钓鱼" (fishing) is a separate event

**Correct parse** depends on context and affects translation:
- Parse 1 → "I saw him fishing by the river" (single event)
- Parse 2 → "I saw him by the river, fishing" (or "while fishing")

### Handling Pro-Drop and Topic-Prominence

Chinese frequently drops subjects and uses topic-comment structures:

**Pro-drop**: "吃了吗？" (Ate already?)
- Subject "你" (you) is dropped
- Target language may require: "Have you eaten?" (English needs subject)
- Dependency parsing identifies missing subject slot

**Topic-comment**: "这本书，我已经看完了"
- Topic: "这本书" (this book)
- Comment: "我已经看完了" (I already finished reading)
- Literal word order wrong for English
- Dependency shows "书" is object of "看完" → "I already finished reading this book"

### Modifier Attachment

Chinese has long modifier chains that attach differently across languages:

**Chinese**: "我买了一本昨天朋友推荐的很有趣的书"
- Modifiers stack before noun: "book that [friend recommended yesterday] [very interesting]"
- Dependencies:
  - "推荐" (recommended) ← "朋友" (friend)
  - "推荐" (recommended) ← "昨天" (yesterday)
  - "有趣" (interesting) ← "很" (very)
  - All modify "书" (book)

**English**: "I bought a very interesting book that a friend recommended yesterday"
- Relative clause moves after noun
- Dependency parsing identifies attachment points for correct restructuring

## Real-World Impact

### Google Translate / DeepL

**Volume**: Billions of Chinese-English translations per year
**Challenge**: Chinese syntax differs maximally from European languages

**Example improvement with dependency parsing**:

**Without parsing**:
- Chinese: "他把门关上了"
- Wrong: "He door closed" (word-by-word)

**With parsing**:
- Identifies "把" construction (disposal form)
- "门" (door) is patient, not subject
- "关上" (close) is main verb
- Correct: "He closed the door"

**Impact**: User satisfaction, reduced need for manual post-editing

### Enterprise Document Translation

**SDL Trados, memoQ** - Computer-aided translation (CAT) tools:

**Chinese source**: Technical manuals, contracts, marketing materials
**Target**: English, German, Japanese, etc.

**Value of dependency parsing**:
- Pre-parsing segments before human translator sees them
- Suggests translation memory matches based on syntactic similarity, not just lexical
- Example:
  - Segment A: "系统自动检测故障"
  - Segment B: "系统会自动检测到故障"
  - Different words ("到"), but same dependency structure → suggest same translation

**Productivity gain**: 20-30% faster translation for technical documents

### App/Game Localization

**Mobile games** (Genshin Impact, Honor of Kings) localizing to global markets:

**Challenge**: Dialogue must sound natural in target language

**Chinese**: "你终于来了！我等你很久了！"
- Structure: "You finally came! I you very long awaited!"

**Without parsing**: "You finally came! I waited for you very long!" (unnatural stress)
**With parsing**: Identifies emphasis and temporal relationships
**Better**: "You're finally here! I've been waiting forever!"

**Impact**:
- Player experience (immersion, narrative quality)
- Review scores and revenue (poor localization = negative reviews)

### Subtitle Translation

**Netflix, YouTube** - Chinese content for international audiences:

**Challenge**: Subtitles have character limits, must be concise

**Chinese**: "这件事情我早就跟你说过了"
- Literal: "This matter I long ago with you said already"
- Dependencies:
  - "说" (said) = root
  - "这件事情" (this matter) = object (topic-fronted)
  - "我" (I) = subject
  - "跟你" (to you) = recipient
  - "早就...了" (long ago, already) = temporal/aspectual

**Word-by-word**: "This thing I already told you long ago" (18 chars, awkward)
**Dependency-informed**: "I told you this ages ago" (14 chars, natural)

**Constraint**: English subtitles ~42 characters/line for readability
**Value**: Concise, natural subtitles fitting time/space constraints

## Libraries Used in Production

**HanLP**
- Used by: Alibaba Translate, Chinese MT startups
- Strength: Fast, accurate Chinese parsing
- Integration: Python/Java APIs for MT pipelines

**Stanford CoreNLP**
- Used by: Google Translate research, academic MT systems
- Strength: Universal Dependencies enables cross-lingual transfer
- Research: Many MT papers use Stanford parser for Chinese analysis

**LTP (Language Technology Platform)**
- Used by: Baidu Translate
- Strength: Chinese-optimized, integrated with Chinese NLP pipeline

**Neural parser in MT models**
- Used by: DeepL, modern NMT systems
- Approach: Encode dependency structure in neural representation
- Trend: Implicit syntax via attention mechanisms vs. explicit parsing

## When Dependency Parsing Isn't Enough

**Discourse coherence**:
- Chinese: "他很高兴。因为他通过了考试。"
- Correct: "He is happy because he passed the exam."
- Dependency parsing handles individual sentences, but discourse markers ("因为" = because) require discourse-level analysis

**Cultural adaptation**:
- Chinese: "他吃了闭门羹" (idiom: "he ate a closed-door soup" = he was rejected)
- Dependency parsing gives literal structure
- Requires: Idiom detection + cultural equivalent
- English: "He got the cold shoulder" (not literal translation)

**Register and formality**:
- Chinese: "您贵姓？" (formal: What is your honorable surname?)
- Dependency parsing identifies question structure
- But translation must adapt formality level
- Informal English: "What's your name?" (formality loss acceptable in English)

**Ambiguity requiring world knowledge**:
- Chinese: "他在银行工作"
- Parse 1: He works at a bank (financial institution)
- Parse 2: He works at the riverbank (edge of river)
- Dependency parsing alone doesn't resolve "银行" ambiguity
- Requires: Context or word sense disambiguation

## Dependency Parsing in Neural MT

**Evolution**:

**2010s - Phrase-based MT**:
- Explicit dependency parsing as pre-processing
- Reordering rules based on dependency trees
- Example: Chinese "把" constructions → English active voice

**2015-2018 - Early Neural MT**:
- Dependency parsing as auxiliary task
- Multi-task learning: Translate + predict dependencies
- Improved translation quality by 1-2 BLEU points

**2019-present - Transformer models**:
- Implicit syntax via self-attention
- Debate: Does model learn dependency-like structures internally?
- Research: Probing studies show transformers encode syntax in hidden layers

**Current practice**:
- Production systems (Google, DeepL): Mostly implicit syntax via transformers
- Domain-specific systems: Explicit dependency parsing for technical/legal text
- Low-resource languages: Dependency parsing helps with limited training data

## Performance Requirements

**Real-time translation (apps)**:
- Latency: <500ms for short sentences
- Parsing budget: ~50ms if explicit parsing used
- Solution: Lightweight parsers or implicit syntax

**Batch translation (documents)**:
- Quality > speed
- Can afford 1-2 seconds per sentence
- Solution: Ensemble models, explicit syntax-informed reranking

**Subtitle translation**:
- Throughput: 1 hour of video = ~800 subtitle segments
- Latency: <1 second per segment acceptable
- Constraint: Human post-editing is bottleneck, not parsing speed
