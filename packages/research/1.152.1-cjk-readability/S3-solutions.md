# S3: Solutions - Available Tools and Libraries

## Open Source Python Libraries

### 1. HSK Character Profiler
- **Repository**: https://github.com/Ancastal/HSK-Character-Profiler
- **Focus**: HSK-based character proficiency analysis
- **Features**:
  - Identifies HSK level per character in text
  - Generates reports of character counts by HSK level
  - Calculates average HSK level of text
  - Customizable settings
- **Origin**: Master's thesis in Computational Linguistics
- **Best for**: Quick HSK level assessment

### 2. Language-Analyzer
- **Repository**: https://github.com/Ancastal/Language-Analyzer
- **Focus**: Multi-language text analysis
- **Features**:
  - HSK profiling for Chinese
  - Readability analysis (English + Chinese)
  - Advanced text analysis tools
- **Best for**: Projects needing both Chinese and English analysis

### 3. AlphaReadabilityChinese (ARC Chinese)
- **Repository**: https://github.com/leileibama/AlphaReadabilityChinese
- **Developers**: Lei Lei (雷蕾) & Tingyu Zhang (张婷玉), Shanghai International Studies University
- **Features**:
  - Lexical level indices
  - Syntactic level indices
  - Semantic level indices
- **Best for**: Academic research requiring multi-level analysis

### 4. python-readability-cn
- **Repository**: https://github.com/chenryn/python-readability-cn
- **Focus**: Chinese text readability calculation
- **Features**:
  - Word segmentation
  - Part-of-speech analysis
  - Syntactic dependency analysis
  - Multiple NLP provider support (LTP, Jieba, PKU)
  - Scoring metrics named after research authors
- **Best for**: Flexible NLP backend requirements

### 5. Hanzipy
- **Repository**: https://github.com/Synkied/hanzipy
- **Focus**: Chinese character NLP framework
- **Features**:
  - Character processing
  - NLP pipeline for Chinese
  - Learning framework for Chinese language students
- **Best for**: Educational applications, character-level analysis

### 6. CTAP for Chinese
- **Documentation**: https://aclanthology.org/2022.lrec-1.592.pdf
- **Focus**: Linguistic complexity measurement
- **Features**:
  - 196 linguistic complexity measures (most comprehensive)
  - Open-source toolkit
  - 4 levels: character, word, sentence, discourse
- **Best for**: Research requiring comprehensive linguistic features

## Commercial APIs

### 1. LTP-Cloud (Language Technology Platform)
- **Website**: https://www.ltp-cloud.com/intro_en
- **Developer**: Harbin Institute of Technology
- **Features**:
  - Chinese word segmentation
  - POS tagging
  - Dependency parsing
  - Named entity recognition
  - Semantic role labeling
- **Users**: Baidu, Tencent, Huawei, Kingsoft
- **Best for**: Production Chinese NLP at scale
- **Pricing**: Commercial (pay-per-use)

### 2. Google Cloud Natural Language API
- **Website**: https://cloud.google.com/natural-language
- **Features**:
  - Syntactic analysis (Simplified + Traditional Chinese)
  - Sentiment analysis
  - Entity recognition
  - Text annotations
- **Best for**: Multi-language apps (Chinese + other languages)
- **Pricing**: Pay-per-request
  - 0-5K units/month: Free
  - 5K-1M units: $1.00 per 1K units
  - 1M-5M units: $0.50 per 1K units
  - (1 unit = 1,000 characters)

### 3. Tencent Cloud NLP (Hunyuan)
- **Website**: https://www.tencentcloud.com/techpedia/109099
- **Features**:
  - Text generation
  - Sentiment analysis
  - Machine translation
  - Large language model (Hunyuan)
- **Best for**: Chinese market applications, integration with Tencent ecosystem
- **Pricing**: Commercial (contact for pricing)

### 4. NLP Cloud
- **Website**: https://nlpcloud.com/
- **Features**:
  - 200+ language support (including Chinese)
  - Custom model training
  - Pre-trained AI engines
- **Best for**: Multi-language NLP with custom models
- **Pricing**: Starts at $29/month (limited requests)

## Academic Tools

### CRIE (Chinese Readability Index Explorer)
- **Website**: http://www.chinesereadability.net/CRIE/publish.html
- **Paper**: https://link.springer.com/article/10.3758/s13428-015-0649-1
- **Features**:
  - 82 multilevel linguistic features
  - Support Vector Machine (SVM) prediction
  - Grade level classification (1-9)
  - Simplified + Traditional Chinese support
  - Diagnostic readability reports
- **Training data**: Taiwanese primary/secondary school textbooks
- **Status**: Research tool (availability varies)
- **Best for**: Academic research, educational text assessment

## Web-Based Tools (Free)

### 1. Chinese Text Analyser
- **Website**: https://www.chinesetextanalyser.com/
- **Features**:
  - Fast segmentation/analysis (~200-300K characters)
  - Web-based (no installation)
  - Character frequency analysis
- **Best for**: Quick one-off analysis, students

### 2. HSK HSK Analyzer
- **Website**: https://hskhsk.com/analyse
- **Features**:
  - Word and character statistics
  - HSK level breakdown
  - Suggests high-frequency words to learn
- **Best for**: Language learners checking text difficulty

### 3. Chinese Text Analyzer (Chine-culture)
- **Website**: https://new.chine-culture.com/en/chinese-language/resources/chinese-text-analyzer
- **Features**:
  - Junda frequency list analysis
  - Character threshold evaluation
  - Based on Joël Belassen's work
- **Best for**: Frequency-based analysis

## Supporting NLP Tools

### CkipTagger (Sinica-Taiwan)
- **Developer**: Academia Sinica, Taiwan
- **Features**:
  - Chinese word segmentation
  - POS tagging
  - Named entity recognition
- **Best for**: Traditional Chinese, Taiwan-focused applications

### Jieba
- **Repository**: https://github.com/fxsjy/jieba
- **PyPI**: https://pypi.org/project/jieba/
- **Features**:
  - Fast word segmentation (~200K chars/sec)
  - Prefix dictionary + DAG + HMM
  - Customizable dictionary
- **Best for**: Foundation for building custom tools
- **Most widely used**: Nearly all Chinese NLP tools use Jieba or build on it

## Data Resources

### HSK 3.0 Lists (2026)
- **Repository**: https://github.com/krmanik/HSK-3.0
- **Content**:
  - HSK 1-9 characters
  - Handwritten characters
  - Words and grammar lists
  - Anki deck format
  - Frequency, pinyin, zhuyin, meaning

### TOCFL Lists
- **Repository**: https://github.com/skishore/inkstone/pull/47
- **Content**:
  - 華語文能力測驗 (TOCFL) vocabulary
  - Traditional Chinese focus
  - Differences between Simplified/Traditional

### SUBTLEX-CH
- **Paper**: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0010729
- **Content**:
  - 46.8 million characters from film/TV subtitles
  - 33.5 million words
  - Psychologically/cognitively relevant frequency data

## Comparison Matrix

| Tool | Type | Features | HSK | TOCFL | Traditional | Best For |
|------|------|----------|-----|-------|------------|----------|
| HSK Character Profiler | OSS Python | Character profiling | ✓ | ✗ | ? | Quick HSK assessment |
| AlphaReadabilityChinese | OSS Python | Multi-level indices | ? | ? | ✓ | Academic research |
| python-readability-cn | OSS Python | Multiple backends | ? | ? | ✓ | Flexible NLP needs |
| CTAP | OSS Python | 196 features | ✗ | ✗ | ✓ | Comprehensive analysis |
| CRIE | Academic | 82 features + SVM | ✗ | ✗ | ✓ | Grade level prediction |
| LTP-Cloud | Commercial API | Full NLP pipeline | ✗ | ✗ | ✓ | Production scale |
| Google Cloud NLP | Commercial API | Multi-language | ✗ | ✗ | ✓ | Enterprise apps |
| HSK HSK Analyzer | Web | HSK breakdown | ✓ | ✗ | ? | Students/learners |

## Decision Tree

**For learners checking text difficulty:**
→ Use **HSK HSK Analyzer** (web, free)

**For developers building language learning apps:**
→ Use **HSK Character Profiler** or **Language-Analyzer** (OSS Python)

**For academic research:**
→ Use **CTAP** (most features) or **AlphaReadabilityChinese** (multi-level)

**For production apps at scale:**
→ Use **LTP-Cloud** (Chinese-focused) or **Google Cloud NLP** (multi-language)

**For custom requirements:**
→ Build on **Jieba** + **HSK 3.0 lists** + frequency data

## Sources
- [HSK Character Profiler - GitHub](https://github.com/Ancastal/HSK-Character-Profiler)
- [Language-Analyzer - GitHub](https://github.com/Ancastal/Language-Analyzer)
- [AlphaReadabilityChinese - GitHub](https://github.com/leileibama/AlphaReadabilityChinese)
- [python-readability-cn - GitHub](https://github.com/chenryn/python-readability-cn)
- [Hanzipy - GitHub](https://github.com/Synkied/hanzipy)
- [CTAP for Chinese](https://aclanthology.org/2022.lrec-1.592.pdf)
- [LTP-Cloud](https://www.ltp-cloud.com/intro_en)
- [Google Cloud Natural Language](https://cloud.google.com/natural-language)
- [Tencent Cloud NLP](https://www.tencentcloud.com/techpedia/109099)
- [NLP Cloud](https://nlpcloud.com/)
- [CRIE: An automated analyzer for Chinese texts](https://link.springer.com/article/10.3758/s13428-015-0649-1)
- [Chinese Text Analyser](https://www.chinesetextanalyser.com/)
- [HSK HSK Analyzer](https://hskhsk.com/analyse)
- [HSK 3.0 Lists - GitHub](https://github.com/krmanik/HSK-3.0)
- [TOCFL Lists - Inkstone PR](https://github.com/skishore/inkstone/pull/47)
