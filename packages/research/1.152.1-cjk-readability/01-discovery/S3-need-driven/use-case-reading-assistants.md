# Use Case: Reading Assistant Tools

## Scenario Description
Browser extensions, e-reader apps, and mobile applications that help learners read authentic CJK content by providing real-time difficulty indicators, vocabulary popups, and comprehensible input filtering.

## User Persona
- **Primary**: Tool developers building reading assistance features
- **Secondary**: Learners consuming authentic content (news, novels, social media)
- **Platforms**: Browser extensions (Chrome, Firefox), mobile apps, e-readers
- **Scale**: Analyze web pages, articles, ebooks in real-time

## Examples of Real Applications
- **Zhongwen (browser extension)**: Popup dictionary with character frequency indicators
- **Du Chinese Reader**: Articles with difficulty ratings and popup definitions
- **Readibu**: E-reader with HSK level filtering
- **LingQ**: Web reader highlighting known vs unknown words
- **Pleco Reader**: Mobile document reader with tap-to-translate

## Technical Requirements

### Core Capabilities
1. **Real-time difficulty estimation**: Analyze web page difficulty instantly
2. **Character/word frequency lookup**: Show how common each word is
3. **Unknown word highlighting**: Visual distinction between known/unknown vocabulary
4. **Content filtering**: Find articles matching learner's level
5. **Popup dictionary integration**: Quick definitions without context switch
6. **Progress tracking**: Monitor vocabulary growth over time

### Performance Constraints
- **Real-time responsiveness**: Sub-second page analysis (user waiting)
- **Lightweight**: Browser extension memory limits (50-100 MB)
- **Offline capability**: Core features work without internet
- **Battery efficiency**: Mobile apps shouldn't drain battery

### Accuracy Requirements
- **Critical**: Fast performance (slow tools frustrate users)
- **Important**: Character frequency accuracy (difficulty indicators)
- **Nice-to-have**: Perfect HSK tagging (gaps acceptable if core is fast)

## Library Analysis

### Jun Da Character Frequency Lists
**Strengths for Reading Assistants**:
- ✅ **Fast lookup** (8000 character frequency rankings)
- ✅ **Small data file** (~100 KB, browser-friendly)
- ✅ **Research-backed** (corpus-derived)
- ✅ **Offline-capable** (bundle with extension)

**Weaknesses for Reading Assistants**:
- ⚠️ Character-only (no word frequency)
- ⚠️ No HSK mapping
- ⚠️ Requires word segmentation separately

**Verdict**: **Excellent for character-level indicators**.

### CC-CEDICT + HSK Tags
**Strengths for Reading Assistants**:
- ✅ **HSK tagging** (show word difficulty levels)
- ✅ **Comprehensive** (100k+ entries)
- ✅ **Popup dictionary data** (definitions included)
- ✅ **Offline-capable** (bundle with app)

**Weaknesses for Reading Assistants**:
- ⚠️ Large file size (~30 MB, impacts extension load time)
- ⚠️ Incomplete HSK coverage
- ⚠️ Static data (doesn't learn user's vocabulary)

**Verdict**: **Essential for vocabulary lookup, optimize file size**.

### jieba.js (JavaScript port)
**Strengths for Reading Assistants**:
- ✅ **Browser-native** (runs in JavaScript, no server needed)
- ✅ **Fast segmentation** (real-time page analysis)
- ✅ **Offline-capable** (no API calls)
- ✅ **Lightweight** (small bundle size)

**Weaknesses for Reading Assistants**:
- ⚠️ JavaScript slower than native (acceptable trade-off)
- ⚠️ No built-in readability features

**Verdict**: **Critical for browser extensions**.

### IndexedDB / LocalStorage (Browser Storage)
**Strengths for Reading Assistants**:
- ✅ **Persist user vocabulary** (track known words)
- ✅ **Fast local queries** (no network latency)
- ✅ **Privacy-friendly** (data stays on device)

**Weaknesses for Reading Assistants**:
- ⚠️ Storage limits (5-50 MB depending on browser)
- ⚠️ No built-in sync (need custom cloud sync)

**Verdict**: **Essential for personalized features**.

## Detailed Feature Comparison

| Feature | Jun Da | CC-CEDICT+HSK | jieba.js | IndexedDB | Reading Assistant Value |
|---------|--------|---------------|----------|-----------|-------------------------|
| **Fast lookup** | ✅ | ⚠️ Large | ✅ | ✅ | Critical (real-time) |
| **Character frequency** | ✅ | ❌ | ❌ | ⚠️ Cache | Critical (difficulty) |
| **HSK levels** | ❌ | ✅ | ❌ | ⚠️ Cache | High (learner guidance) |
| **Offline-capable** | ✅ | ✅ | ✅ | ✅ | Critical (mobile/privacy) |
| **Small bundle size** | ✅ | ❌ | ✅ | N/A | High (extension limits) |
| **User vocabulary tracking** | ❌ | ❌ | ❌ | ✅ | High (personalization) |

## Recommendation

### Hybrid Approach for Reading Assistants
**Combine lightweight data with user personalization:**

1. **Jun Da frequency**: Character-level difficulty indicators (fast, small)
2. **Pruned CC-CEDICT**: Top 10k words only (reduce size from 30 MB → 3 MB)
3. **jieba.js**: Word segmentation in browser
4. **IndexedDB**: Track user's known vocabulary for highlighting
5. **Optional cloud sync**: Sync vocabulary across devices

### Browser Extension Architecture
```javascript
// Pseudocode for browser extension
class ReadingAssistant {
  constructor() {
    this.charFreq = loadCharacterFrequency();  // Jun Da data
    this.wordDict = loadPrunedDictionary();    // Top 10k words only
    this.userVocab = loadUserVocabulary();     // IndexedDB
  }

  async analyzePage() {
    // 1. Extract text from page
    const text = document.body.innerText;

    // 2. Segment into words
    const words = jieba.cut(text);

    // 3. Calculate difficulty
    const difficulty = this.estimateDifficulty(words);

    // 4. Highlight unknown words
    this.highlightUnknownWords(words);

    // 5. Show difficulty badge
    this.showDifficultyBadge(difficulty);
  }

  highlightUnknownWords(words) {
    words.forEach(word => {
      if (!this.userVocab.has(word)) {
        const hskLevel = this.wordDict.getHSKLevel(word);
        const color = this.getLevelColor(hskLevel);
        // Highlight word in page with color
        highlightWord(word, color);
      }
    });
  }
}
```

## Implementation Patterns

### Pattern 1: Real-Time Difficulty Badge
Show page difficulty instantly:

```javascript
function showDifficultyBadge(pageText) {
  // Segment text
  const words = jieba.cut(pageText);

  // Calculate character coverage
  const chars = [...pageText].filter(isChineseChar);
  const commonChars = chars.filter(c => charFreq[c] <= 1500);  // Top 1500
  const coverage = commonChars.length / chars.length;

  // Estimate difficulty
  let difficulty, color;
  if (coverage >= 0.95) {
    difficulty = 'Beginner';
    color = 'green';
  } else if (coverage >= 0.85) {
    difficulty = 'Intermediate';
    color = 'orange';
  } else {
    difficulty = 'Advanced';
    color = 'red';
  }

  // Show badge in corner
  showBadge(difficulty, color);
}
```

### Pattern 2: Unknown Word Highlighting
Visual feedback on comprehension:

```javascript
function highlightUnknownWords(text, userVocabulary) {
  const words = jieba.cut(text);

  words.forEach(word => {
    if (!userVocabulary.has(word)) {
      // Find word in DOM and highlight
      const nodes = findTextNodes(word);
      nodes.forEach(node => {
        const span = document.createElement('span');
        span.className = 'unknown-word';
        span.style.backgroundColor = '#FFEB3B';  // Yellow
        span.textContent = word;

        // Add click handler for popup
        span.onclick = () => showPopupDictionary(word);

        node.replaceWith(span);
      });
    }
  });
}
```

### Pattern 3: Content Filtering by Difficulty
Find readable articles:

```javascript
function filterContentByLevel(articles, targetLevel) {
  const readable = [];

  articles.forEach(article => {
    const words = jieba.cut(article.text);
    const difficulty = estimateDifficulty(words);

    // Check if within learner's range
    if (difficulty >= targetLevel - 0.5 && difficulty <= targetLevel + 0.5) {
      readable.push({
        article: article,
        difficulty: difficulty,
        newWords: countUnknownWords(words, userVocabulary),
      });
    }
  });

  // Sort by fewest new words (easiest to hardest within level)
  return readable.sort((a, b) => a.newWords - b.newWords);
}
```

### Pattern 4: Popup Dictionary with Frequency Info
Show comprehensive word information:

```javascript
function showPopupDictionary(word) {
  // Look up word data
  const definition = dictionary.lookup(word);
  const hskLevel = dictionary.getHSKLevel(word);
  const frequency = calculateWordFrequency(word);

  // Calculate character frequencies
  const charFrequencies = [...word].map(c => charFreq[c]);
  const rareChar = Math.max(...charFrequencies);

  // Build popup content
  const popup = createPopup({
    word: word,
    pinyin: definition.pinyin,
    definition: definition.english,
    hskLevel: hskLevel || 'Not in HSK',
    frequency: frequency ? `Top ${frequency}` : 'Rare',
    characterDifficulty: rareChar > 3000 ? 'Contains rare characters' : 'Common characters',
    example: definition.example || null,
  });

  showPopup(popup);
}
```

### Pattern 5: Vocabulary Progress Tracking
Monitor learning over time:

```javascript
class VocabularyTracker {
  constructor() {
    this.knownWords = new Set(loadFromIndexedDB('knownWords'));
    this.learningWords = new Map(loadFromIndexedDB('learningWords'));
  }

  markWordAsKnown(word) {
    this.knownWords.add(word);
    this.learningWords.delete(word);
    saveToIndexedDB('knownWords', [...this.knownWords]);

    // Update statistics
    this.updateStats();
  }

  getProgressReport() {
    // Calculate HSK level coverage
    const hskCoverage = {};
    for (let level = 1; level <= 6; level++) {
      const hskWords = getHSKWords(level);
      const known = hskWords.filter(w => this.knownWords.has(w));
      hskCoverage[level] = known.length / hskWords.length;
    }

    return {
      totalKnownWords: this.knownWords.size,
      wordsLearningNow: this.learningWords.size,
      hskCoverage: hskCoverage,
      estimatedLevel: this.estimateLevel(),
      progressThisWeek: this.getWeeklyProgress(),
    };
  }

  estimateLevel() {
    // User is at highest level where they know 80%+ vocabulary
    for (let level = 6; level >= 1; level--) {
      if (this.hskCoverage[level] >= 0.8) {
        return level;
      }
    }
    return 1;
  }
}
```

### Pattern 6: Optimized Data Loading
Minimize bundle size and load time:

```javascript
// Lazy-load dictionary data in chunks
class LazyDictionary {
  constructor() {
    this.cache = new Map();
    this.chunkSize = 1000;  // Load 1000 words at a time
  }

  async lookup(word) {
    // Check cache first
    if (this.cache.has(word)) {
      return this.cache.get(word);
    }

    // Load chunk containing this word
    const chunk = await this.loadChunk(word);
    chunk.forEach(entry => this.cache.set(entry.word, entry));

    return this.cache.get(word);
  }

  async loadChunk(word) {
    // Determine which chunk (alphabetical)
    const chunkIndex = Math.floor(pinyinSort(word) / this.chunkSize);

    // Fetch from bundled data or API
    const response = await fetch(`/data/dict_chunk_${chunkIndex}.json`);
    return await response.json();
  }
}
```

## Trade-offs

### Browser-Based Processing Benefits
- **Privacy**: User data stays on device
- **Speed**: No network latency
- **Offline**: Works without internet
- **Cost**: No server infrastructure needed

### Browser-Based Processing Costs
- **Bundle size**: Extension size limits (Chrome: 5 MB packaged)
- **Memory**: Browser memory constraints
- **Processing power**: Slower than server-side
- **Data sync**: Complex cross-device synchronization

### When Client-Side is Worth It
Use browser-based processing when:
- Privacy is important (user vocabulary data sensitive)
- Real-time performance critical (popup dictionary)
- Offline usage required (mobile apps, privacy-conscious users)
- Simple features (lookup, highlighting) not complex NLP

### When Server-Side is Better
Use server API when:
- Complex processing needed (advanced NLP, ML models)
- Large data requirements (full dictionary, corpus analysis)
- Multi-user features (social vocabulary sharing)
- Limited device resources (older mobile devices)

## Missing Capabilities

No existing tool provides:
- ❌ **Adaptive difficulty estimation** (learns from user's reading history)
- ❌ **Context-aware definitions** (word meaning varies by context)
- ❌ **Grammar complexity indicators** (sentence structure difficulty)
- ❌ **Cross-device vocabulary sync** (seamless sync across browser/mobile)
- ❌ **Reading speed estimation** (how long will this article take?)
- ❌ **Optimal word learning order** (which unknown words to learn first?)

Reading assistant developers must build these features custom.

## Real-World Integration Examples

### Browser Extension: Zhongwen-Style
```javascript
// Content script injected into web pages
class ZhongwenReader {
  constructor() {
    this.dictionary = new LazyDictionary();
    this.charFreq = loadCharacterFrequency();
    this.userLevel = getUserLevel();  // HSK 1-6

    // Add hover listeners
    this.setupHoverPopups();
  }

  setupHoverPopups() {
    document.addEventListener('mouseover', async (e) => {
      const word = getWordUnderCursor(e);
      if (word && isChineseWord(word)) {
        const data = await this.dictionary.lookup(word);
        this.showPopup(word, data, e.pageX, e.pageY);
      }
    });
  }

  showPopup(word, data, x, y) {
    // Build popup with difficulty indicators
    const popup = document.createElement('div');
    popup.className = 'zhongwen-popup';
    popup.style.left = `${x}px`;
    popup.style.top = `${y}px`;

    // Difficulty badge
    const level = data.hskLevel || 'Unknown';
    const badge = level <= this.userLevel ? '✅' : '⚠️';

    popup.innerHTML = `
      <div class="word">${word} ${badge}</div>
      <div class="pinyin">${data.pinyin}</div>
      <div class="definition">${data.definition}</div>
      <div class="meta">HSK ${level} | Freq: ${getFrequency(word)}</div>
    `;

    document.body.appendChild(popup);
  }
}
```

### Mobile E-Reader App
```javascript
class MobileEReader {
  constructor() {
    this.userVocab = loadUserVocabulary();
    this.touchHandler = this.setupTouchHandler();
  }

  setupTouchHandler() {
    // Tap word to see definition
    document.addEventListener('touchstart', async (e) => {
      const word = getWordAtPoint(e.touches[0]);

      if (word) {
        const definition = await lookup(word);
        this.showDefinitionModal(word, definition);
      }
    });
  }

  showDefinitionModal(word, definition) {
    // Full-screen modal with action buttons
    const modal = createModal({
      word: word,
      pinyin: definition.pinyin,
      definition: definition.english,
      actions: [
        {
          label: 'Mark as Known',
          action: () => this.markAsKnown(word),
        },
        {
          label: 'Add to Study List',
          action: () => this.addToStudyList(word),
        },
      ],
    });

    showModal(modal);
  }

  markAsKnown(word) {
    this.userVocab.add(word);
    saveUserVocabulary(this.userVocab);

    // Update highlighting on page
    this.refreshWordHighlighting();
  }
}
```

### Content Recommendation Engine
```javascript
class ContentRecommender {
  constructor(userProfile) {
    this.userLevel = userProfile.estimatedHSKLevel;
    this.knownWords = userProfile.knownWords;
    this.interests = userProfile.interests;
  }

  async recommendArticles(articlePool) {
    const scored = [];

    for (const article of articlePool) {
      const words = jieba.cut(article.text);

      // Calculate comprehension
      const knownCount = words.filter(w => this.knownWords.has(w)).length;
      const comprehension = knownCount / words.length;

      // Calculate new vocabulary load
      const unknownWords = words.filter(w => !this.knownWords.has(w));
      const newWordLoad = unknownWords.length;

      // Interest match (topic modeling)
      const topicMatch = this.scoreTopicMatch(article, this.interests);

      // Composite score
      const score = {
        article: article,
        comprehension: comprehension,
        newWordLoad: newWordLoad,
        topicMatch: topicMatch,
        recommendScore: (
          comprehension * 0.5 +          // 50% comprehension weight
          (1 - newWordLoad / 100) * 0.3 + // 30% vocabulary load
          topicMatch * 0.2                // 20% interest match
        ),
      };

      // Only recommend if 80-95% comprehension (i+1 zone)
      if (comprehension >= 0.80 && comprehension <= 0.95) {
        scored.push(score);
      }
    }

    // Return top recommendations
    return scored.sort((a, b) => b.recommendScore - a.recommendScore).slice(0, 10);
  }
}
```

## Performance Considerations

### Typical Workload
Reading assistants process:
- Web pages: 500-5000 characters
- Articles: 1000-10000 characters
- Books: 50k-200k characters (chapter at a time)

### Optimization Strategies
```javascript
// 1. Incremental processing (don't re-analyze whole page)
let lastAnalyzedLength = 0;

function analyzePageIncremental() {
  const currentText = document.body.innerText;

  if (currentText.length > lastAnalyzedLength) {
    const newText = currentText.slice(lastAnalyzedLength);
    analyzeText(newText);
    lastAnalyzedLength = currentText.length;
  }
}

// 2. Virtualization for long documents
function renderVisiblePortion(document, viewport) {
  // Only process text visible in viewport
  const visibleText = getTextInViewport(viewport);
  return analyzeAndHighlight(visibleText);
}

// 3. Web Workers for background processing
const worker = new Worker('analyzer.js');
worker.postMessage({ text: pageText });
worker.onmessage = (e) => {
  const { difficulty, unknownWords } = e.data;
  updateUI(difficulty, unknownWords);
};
```

## Conclusion

**Reading assistants need lightweight, browser-optimized solutions.** Best approach:

1. **Pruned data**: Top 10k words only (not full 100k dictionary)
2. **Client-side processing**: jieba.js for real-time segmentation
3. **User vocabulary tracking**: IndexedDB for personalization
4. **Hybrid architecture**: Client-side for speed, optional cloud sync for features

Trade-off bundle size (faster loading) vs features (comprehensive data). Prioritize real-time responsiveness over perfect accuracy - fast feedback more valuable than 100% coverage for learners reading authentic content.
