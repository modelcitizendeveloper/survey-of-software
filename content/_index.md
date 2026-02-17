---
title: "Survey of Software"
weight: 1
bookFlatSection: false
bookCollapseSection: false
aliases: ["/survey/"]
description: "Software library research across sorting, search, NLP, ML, frontend, LLMs — benchmarks, decision frameworks, production patterns."
---

# Survey of Software

> **Systematic coverage of general-purpose software libraries.**
> Measured research on algorithms, data structures, ML, and infrastructure—so you can build with confidence instead of guessing.

**[What is this? →](/about)** | **[The Vision →](/vision)** | **[Method →](/survey/method)**

**[Claude Skill →](/skill/)** Let Claude consult this research library directly in conversations. Ask about library selection, and Claude fetches surveys, synthesizes recommendations, or runs live research on uncovered topics.

---

**Newsletter:** New library research published as it's ready. Monthly digest of what's new — [subscribe to stay current →](https://modelcitizendeveloper.com/)

---

## 1.001-009: Sorting & Searching Algorithms

**Completed: 9/9**

- ✅ [**1.001** Sorting Libraries](/survey/1-001) - Timsort, parallel sorts, radix sorts
- ✅ [**1.002** Fuzzy Search](/survey/1-002) - FuzzyWuzzy, RapidFuzz, TheFuzz
- ✅ [**1.003** Full-Text Search](/survey/1-003) - Whoosh, Tantivy, MeiliSearch clients
- ✅ [**1.004** Binary Search Trees](/survey/1-004) - B-trees, AVL, Red-Black implementations
- ✅ [**1.005** Spatial Search](/survey/1-005) - PostGIS, Elasticsearch Geo, rtree
- ✅ [**1.006** Graph Search](/survey/1-006) - A*, Dijkstra, BFS/DFS implementations
- ✅ [**1.007** Pattern Matching Algorithms](/survey/1-007) - KMP, Boyer-Moore, Aho-Corasick, Rabin-Karp
- ✅ [**1.008** Time Series Search - DTW, shapelet discovery](/survey/1-008)
- ✅ [**1.009** Similarity Search](/survey/1-009) - LSH, MinHash, SimHash

---

## 1.010-019: Graph & Network Algorithms

**Completed: 10/10**

- ✅ [**1.010** Graph Analysis](/survey/1-010) - NetworkX, graph-tool, igraph
- ✅ [**1.011** Graph Database Clients - Neo4j, ArangoDB, TigerGraph](/survey/1-011)
- ✅ [**1.012** Community Detection](/survey/1-012) - Louvain, label propagation, spectral
- ✅ [**1.013** String Algorithms](/survey/1-013)
- ✅ [**1.014** Network Flow - Max flow, min cost flow](/survey/1-014)
- ✅ [**1.015** Graph Visualization](/survey/1-015) - Graphviz, Gephi, Cytoscape
- ✅ [**1.016** Social Network Analysis](/survey/1-016) - Centrality, clustering coefficient
- ✅ [**1.017** Bipartite Matching Libraries](/survey/1-017) - NetworkX, scipy.optimize, lapjv
- ✅ [**1.018** Graph Embedding](/survey/1-018) - node2vec, DeepWalk, PyTorch Geometric, DGL
- ✅ [**1.019** Dynamic Graphs](/survey/1-019) - NetworkX temporal, DyNetx, teneto

---

## 1.020-029: Mathematical & Statistical Algorithms

**Completed: 7/10**

- ✅ [**1.020.1** Linear Programming](/survey/1-020-1) - CVXPY, OR-Tools, PuLP optimization
- ✅ [**1.021** Statistical Testing Libraries](/survey/1-021) - Hypothesis testing, A/B testing
- ✅ [**1.022** Optimization](/survey/1-022) - scipy.optimize, OR-Tools, CVXPY, PuLP
- ✅ [**1.023** Symbolic Math Libraries](/survey/1-023) - SymPy vs SageMath
- ✅ [**1.024** Random Number Generation Libraries](/survey/1-024) - PCG, Mersenne Twister
- ✅ [**1.025** Prime Factorization & Primality Testing Libraries](/survey/1-025) - Factorization, primality testing
- **1.026** Combinatorics - Permutations, combinations, partitions
- ✅ [**1.027** Numerical Integration Libraries](/survey/1-027) - Quadrature methods
- **1.028** FFT Libraries - FFTW, pyFFTW, scipy.fft
- **1.029** Matrix Decomposition - SVD, eigenvalue, QR

---

## 1.030-039: String & Text Algorithms

**Completed: 12/15**

- ✅ [**1.030** String Matching](/survey/1-030) - Exact, approximate, regex engines
- ✅ [**1.031** Text Diff](/survey/1-031) - Myers, patience diff, semantic diff
- ✅ [**1.032** String Metrics](/survey/1-032) - Edit distance, Jaro-Winkler, cosine
- ✅ [**1.033** NLP Libraries](/survey/1-033) - spaCy, Transformers, NLTK
  - ✅ [**1.033.1** Intent Classification](/survey/1-033-1) - Zero-Shot, SetFit, sentence-transformers
  - ✅ [**1.033.2** Chinese Word Segmentation](/survey/1-033-2) - Jieba, CKIP, pkuseg, LTP
  - ✅ [**1.033.3** CJK Tokenizers for LLMs](/survey/1-033-3) - SentencePiece, tiktoken, HuggingFace
  - ✅ [**1.033.4** Named Entity Recognition (CJK)](/survey/1-033-4) - spaCy, Stanford NER, BERT-NER
- ✅ [**1.034** Email Libraries](/survey/1-034) - smtplib, yagmail, MIME handling
- ✅ [**1.035** Tokenization](/survey/1-035) - SentencePiece, HuggingFace Tokenizers, tiktoken, YouTokenToMe
  - ✅ [**1.035.1** Chinese Tokenization](/survey/1-035-1) - jieba, pkuseg, word segmentation strategies
- **1.036** Stemming & Lemmatization - Porter, Snowball, WordNet
- **1.037** String Compression - LZ4, Snappy, Zstandard for strings
- **1.038** Unicode Handling - Normalization, transliteration
- ✅ [**1.039** Template Engines](/survey/1-039) - Jinja2, Handlebars, Mustache

---

## 1.040-049: Data Structure Libraries

**Completed: 5/12**

- ✅ [**1.040** Collections](/survey/1-040) - sortedcontainers, blist, pyrsistent
- **1.041** Probabilistic Structures - Bloom filters, count-min sketch
- ✅ [**1.042** Tries](/survey/1-042) - pygtrie, datrie, marisa-trie
- **1.043** Heaps & Priority Queues - Binary heap, Fibonacci heap
  - ✅ [**1.043.1** Task Queues](/survey/1-043-1) - Celery, RQ, Huey, Dramatiq
- **1.044** Specialized Trees - Union-Find, Interval tree, Segment tree
- **1.045** Specialized Buffers - Circular buffer, ring buffer
- **1.046** _Available for future use_
- ✅ [**1.047** Caching](/survey/1-047) - Redis, Memcached, Varnish
- **1.048** _Available for future use_
- **1.049** Meta-Data Structures - Schema inspection, reflection
  - ✅ [**1.049.1** Database Schema Inspection](/survey/1-049-1) - SQLAlchemy, Alembic

---

## 1.050-059: Compression & Encoding

**Completed: 3/10**

- ✅ [**1.050** Compression](/survey/1-050) - zlib, brotli, zstd benchmarks
- **1.051** Image Compression - WebP, AVIF, JPEG XL
- **1.052** Video Codecs - FFmpeg bindings, av
- **1.053** Audio Compression - FLAC, Opus, MP3
- **1.054** Base Encoding - base64, base58, base32
- ✅ [**1.055** Binary Serialization](/survey/1-055) - msgpack, protobuf, flatbuffers
- ✅ [**1.056** JSON Libraries](/survey/1-056) - orjson, ujson, rapidjson
- **1.057** CSV Parsing - Performance comparison
- **1.058** XML Processing - lxml vs ElementTree vs xmltodict
- **1.059** YAML Libraries - PyYAML vs ruamel.yaml

---

## 1.060-069: Cryptography, Networking & Security

**Completed: 4/10**

- ✅ [**1.060** Cryptographic Libraries](/survey/1-060) - cryptography vs PyNaCl
- ✅ [**1.061** Hashing](/survey/1-061) - hashlib, xxhash, blake3
- ✅ [**1.062** Password Hashing - argon2-cffi vs bcrypt (covered in 1.060)](/survey/1-062)
- ✅ [**1.063** JWT Libraries](/survey/1-063) - PyJWT, python-jose, Authlib
- **1.064** Threshold Signature / Secret Sharing - FROST, Shamir's Secret Sharing, threshold ECDSA
- **1.065** P2P / Mesh Networking - libp2p, ZeroMQ, nanomsg, NAT traversal, relay discovery
- **1.066** Onion Routing / Anonymous Transport - Tor stem API, I2P SAM bridge, Nym mixnet
- **1.067** WebSocket Libraries - websockets, aiohttp WS, ws, Socket.IO, µWebSockets
- **1.068** API Proxy / MITM Frameworks - mitmproxy, Envoy, Traefik, transparent interception
- **1.069** Mobile Secure Storage / Keychain - iOS Keychain, Android Keystore, react-native-keychain

---

## 1.070-079: Machine Learning Algorithms

**Completed: 4/10**

- **1.070** Clustering - scikit-learn vs hdbscan vs fastcluster
- ✅ [**1.071** Dimensionality Reduction](/survey/1-071) - UMAP, t-SNE, PCA
- **1.072** Anomaly Detection - Isolation Forest, LOF, autoencoders
- ✅ [**1.073** Time Series Forecasting](/survey/1-073) - Prophet, Darts, statsmodels
- ✅ [**1.074** Gradient Boosting](/survey/1-074) - XGBoost, LightGBM, CatBoost
- ✅ [**1.075** Deep Learning Frameworks](/survey/1-075) - PyTorch, TensorFlow, JAX, MXNet
- **1.076** Reinforcement Learning - Stable Baselines, Ray RLlib
- **1.077** AutoML - auto-sklearn vs TPOT vs H2O
- **1.078** Feature Engineering - Featuretools, tsfresh
- **1.079** Model Interpretation - SHAP vs LIME

---

## 1.080-089: Geometric & Spatial Algorithms

**Completed: 2/11**

- ✅ [**1.080** Image Processing](/survey/1-080) - OpenCV, scikit-image, Pillow
  - ✅ [**1.080.1** QR Code Generation](/survey/1-080-1) - qrcode, segno, pyqrcode
- **1.081** Convex Hull - Graham scan, Jarvis march
- **1.082** Voronoi & Delaunay - scipy.spatial, triangle
- **1.083** Point Cloud Processing - Open3D, PCL bindings
- **1.084** Mesh Processing - Trimesh, PyMesh
- **1.085** Collision Detection - Shapely, SAT algorithms
- **1.086** Path Planning - RRT, PRM, A* for robotics
- **1.087** Geographic Libraries - GeoPy, geopandas, Folium
- **1.088** Coordinate Transformation - pyproj, utm
- **1.089** Spatial Indexing - H3, S2, Geohash

---

## 1.090-099: Specialized Algorithm Domains

**Completed: 3/13**

- **1.090** Bioinformatics - Sequence alignment, BLAST, BioPython
- **1.091** Computer Vision (category)
  - **1.091.1** Object Detection - YOLO, Detectron2, MMDetection
  - ✅ [**1.091.2** Face Detection](/survey/1-091-2) - MediaPipe, Dlib, InsightFace
  - **1.091.3** OCR - Tesseract, EasyOCR, PaddleOCR
- **1.092** Signal Processing - scipy.signal vs librosa
- **1.093** Quantum Computing - Qiskit vs Cirq vs Pennylane
- ✅ [**1.094** Constraint Solving](/survey/1-094) - Z3, OR-Tools, PySMT
- **1.095** Game Theory & Auctions - Nashpy, game theory solvers
- ✅ [**1.096** Scheduling](/survey/1-096) - APScheduler, schedule, Airflow
- **1.097** Recommendation Systems - Surprise, LightFM, Implicit
- **1.098** Voting & Consensus - Social choice algorithms
- **1.099** Distributed Algorithms - Raft, Paxos implementations

---

## 1.100-109: Text & Document Processing

**Completed: 5/12**

- ✅ [**1.100** Text Processing](/survey/1-100) - Regex, string manipulation, NLP utilities
- ✅ [**1.101** PDF Processing - ReportLab, WeasyPrint, PyPDF2](/survey/1-101)
- ✅ [**1.102** Document Parsing](/survey/1-102) - python-docx, openpyxl, pandas Excel
- ✅ [**1.103** Markdown Processing](/survey/1-103) - Python-Markdown, Mistune, markdown-it-py, CommonMark
- **1.104** Syntax Highlighting - Pygments, highlight.js
  - ✅ [**1.104.1** Code Parsing & AST](/survey/1-104-1) - libcst, ast, redbaron
  - ✅ [**1.104.2** Code Formatting](/survey/1-104-2) - Code formatting and linting libraries for Python and JavaScript/TypeScript. Black, ruff, autopep8, Prettier, ESLint.
- **1.105** Translation & i18n - gettext, Babel, i18next
- **1.106** Speech Recognition & TTS - Whisper, Coqui, Piper
- **1.107** OCR Libraries - Tesseract, EasyOCR
- **1.108** Spell Checking - SymSpell, LanguageTool
- **1.109** Content Extraction - BeautifulSoup, Scrapy, newspaper3k

---

## 1.110-119: User Interface & Frontend

**Completed: 12/16**

- ✅ [**1.110** Frontend Frameworks](/survey/1-110) - React, Vue, Svelte, Angular
  - **1.110.1** React Meta-Frameworks - Next.js, Remix, Gatsby
  - **1.110.2** Vue Meta-Frameworks - Nuxt, VitePress
  - **1.110.3** Svelte Meta-Frameworks - SvelteKit
  - ✅ [**1.110.4** Browser Python Execution](/survey/1-110-4)
  - ✅ [**1.110.5** Static Site Generators](/survey/1-110-5) - Hugo, Docusaurus, MkDocs, Jekyll
- ✅ [**1.111** State Management - Redux, Zustand, Jotai, Pinia](/survey/1-111)
- ✅ [**1.112** CSS Frameworks - Tailwind, Bootstrap, Material UI](/survey/1-112)
- ✅ [**1.113** UI Component Libraries - shadcn/ui, Radix, Headless UI](/survey/1-113)
- ✅ [**1.114** Build Tools - Vite, Webpack, Turbopack, esbuild](/survey/1-114)
- ✅ [**1.115** Form & Validation - React Hook Form, Zod, Yup](/survey/1-115)
- ✅ [**1.116** Data Visualization - D3.js, Chart.js, Recharts](/survey/1-116)
- ✅ [**1.117** Animation](/survey/1-117) - Framer Motion, GSAP, React Spring, Lottie
- ✅ [**1.118** Testing - Jest, Vitest, Playwright, Cypress](/survey/1-118)
- ✅ [**1.119** Mobile Frameworks](/survey/1-119) - React Native, Flutter, .NET MAUI, Ionic
  - **1.119.1** NFC Libraries - iOS CoreNFC, Android NDEF, react-native-nfc-manager, Web NFC
  - **1.119.2** Push Notification Libraries - ntfy, Gotify, UnifiedPush, expo-notifications, Web Push/VAPID

---

## 1.120-129: Simulation & Modeling

**Completed: 3/11**

- ✅ [**1.120** Discrete Event Simulation](/survey/1-120) - SimPy, Salabim, Mesa
  - **1.120.1** Network Protocol Simulation - ns-3, Shadow, Mininet for adversarial/Sybil testing
- **1.121** Agent-Based Modeling - Mesa, FLAME, Repast
- ✅ [**1.122** Monte Carlo Simulation](/survey/1-122) - scipy.stats, pymc
- **1.123** System Dynamics - PySD, BPTK-Py
- **1.124** Continuous Simulation - scipy.integrate, FEniCS
- **1.125** Network Simulation - ns-3, Mininet
- **1.126** Traffic Simulation - SUMO, MATSim
- ✅ [**1.127** Financial Simulation](/survey/1-127) - QuantLib, vectorbt
- **1.128** Physics Simulation - PyBullet, MuJoCo, Gazebo
- **1.129** Hybrid Simulation - Discrete + continuous combined

---

## 1.130-139: Business Application Platforms (Self-Hosted)

**Completed: 2/10**

- ✅ [**1.130** Self-Hosted CRM](/survey/1-130) - Twenty CRM, Odoo, SuiteCRM
- ✅ [**1.131** Project Management](/survey/1-131) - Plane, Taiga, OpenProject
- **1.132** Collaboration - Nextcloud, Mattermost, Rocket.Chat
- **1.133** Documentation - BookStack, Wiki.js, Outline
- **1.134** E-Commerce - WooCommerce, Magento, Saleor
- **1.135** Analytics - Matomo, Plausible, Umami, PostHog
- **1.136** DevOps - GitLab, Gitea, Jenkins, Drone
- **1.137** Customer Support - Chatwoot, Zammad, Freescout
- **1.138** Marketing Automation - Mautic, Listmonk
- **1.139** Accounting/ERP - Odoo, ERPNext, Dolibarr

---

## 1.140-149: Language Learning & Linguistics

**Completed: 8/14**

- ✅ [**1.140** Classical Languages](/survey/1-140) - CLTK, pyLatinam, PyWORDS
- ✅ [**1.141** Spaced Repetition](/survey/1-141) - SM-2, SM-18, FSRS algorithms
- ✅ [**1.142** Flashcard Systems](/survey/1-142) - Anki, genanki, AnkiConnect
- **1.143** Language Detection - langdetect, polyglot, fastText
- **1.144** Phonetics - IPA transcription, eSpeak, Forvo API
  - ✅ [**1.144.1** Pinyin/Zhuyin Conversion](/survey/1-144-1) - pypinyin, dragonmapper, pinyin
  - ✅ [**1.144.2** Tone Analysis](/survey/1-144-2) - librosa, praatio, pitch detection, tone sandhi
- **1.145** Grammar Checking - LanguageTool, GrammarBot
- **1.146** Vocabulary Databases - WordNet, ConceptNet, Wiktionary
- **1.147** Language Corpora - Brown Corpus, CoNLL datasets
- ✅ [**1.148** Morphological Analysis](/survey/1-148) - SudachiPy, pymorphy3, UDPipe
  - ✅ [**1.148.1** Chinese Morphological Analysis](/survey/1-148-1) - HanLP, Stanza, LTP, cjklib
  - ✅ [**1.148.2** Classical Chinese Parsing](/survey/1-148-2) - Stanford CoreNLP, ctext.org tools, Kanbun
- **1.149** SLA Tools - CEFR assessment, proficiency testing

---

## 1.150-159: Reading & Text Analysis (Language Learning)

**Completed: 3/13**

- **1.150** Classical Text Corpora - Perseus, PHI5/PHI7, Latin Library
- **1.151** Vocabulary Frequency - DCC Core, Dickinson College
- **1.152** Reading Difficulty & Readability - Flesch-Kincaid, lexical coverage, i+1 detection
  - ✅ [**1.152.1** CJK Readability](/survey/1-152-1) - Character frequency, HSK/TOCFL levels, graded readers
- **1.153** Sentence Parsing - Universal Dependencies parsers, Stanza, syntax trees
  - ✅ [**1.153.1** Chinese Dependency Parsing](/survey/1-153-1) - UD Chinese, Stanford CoreNLP, HanLP
- **1.154** Graded Reader Generation - Text leveling, vocab substitution
  - ✅ [**1.154.1** Chinese Text Simplification](/survey/1-154-1) - MCTS dataset, neural approaches
- **1.155** Parallel Text Alignment - Latin-English, sentence alignment
- **1.156** Text Annotation UI - Glossing, interlinear display
- **1.157** Reading Comprehension - Question generation, validation
- **1.158** Vocabulary Tracking - Learning curves, retention modeling
- **1.159** Adaptive Recommendation - Personalized difficulty

---

## 1.160-169: Character-Based Writing Systems (CJK)

**Completed: 7/8**

- ✅ [**1.160** Character Databases](/survey/1-160) - Unihan, CHISE, IDS, CJKVI
- ✅ [**1.161** Radical & Component Analysis](/survey/1-161) - Character decomposition, semantic components
- ✅ [**1.162** Handwriting Recognition (CJK)](/survey/1-162) - Zinnia, Tegaki, Google Cloud Vision, Azure
- ✅ [**1.163** Character Encoding](/survey/1-163) - Big5, GB2312, GBK, GB18030, Unicode CJK
- ✅ [**1.164** Traditional ↔ Simplified Conversion](/survey/1-164) - OpenCC, HanziConv, zhconv-rs
- ✅ [**1.165** Stroke Order & Writing (CJK)](/survey/1-165) - Make Me a Hanzi, KanjiVG, animCJK
- ✅ [**1.166** OCR (CJK-specific)](/survey/1-166) - Tesseract, PaddleOCR, EasyOCR
- **1.167-1.169** _Available for future use_

---

## 1.170-179: Translation & Alignment

**Completed: 4/7**

- ✅ [**1.170** Machine Translation APIs](/survey/1-170) - DeepL, Google Translate, Azure Translator, Amazon Translate
- ✅ [**1.171** Sentence Alignment](/survey/1-171) - Hunalign, Bleualign, vecalign
- ✅ [**1.172** Translation Memory](/survey/1-172) - TMX format, OmegaT, MemoQ
- ✅ [**1.173** Terminology Extraction](/survey/1-173) - KeyBERT, PyATE, YAKE, spaCy
- **1.174** Computer-Assisted Translation - CAT tool comparison
- **1.175** Literary Translation Tools - Context-aware translation
- **1.175-1.179** _Available for future use_

---

## 1.200-219: LLM & AI Stack

**Completed: 11/12**

- ✅ [**1.200** LLM Orchestration](/survey/1-200) - LangChain, LlamaIndex, RAG
- ✅ [**1.201** LLM Agent Frameworks - AutoGen, CrewAI, MetaGPT](/survey/1-201)
- **1.202** Prompt Engineering - DSPy, guidance, LMQL
- ✅ [**1.203** Vector Databases - ChromaDB, Pinecone, Qdrant](/survey/1-203)
- ✅ [**1.204** RAG Pipelines - Document loading, chunking, retrieval](/survey/1-204)
- ✅ [**1.205** LLM Evaluation - RAGAS, DeepEval, PromptFoo](/survey/1-205)
- ✅ [**1.206** RAG Chunking Patterns](/survey/1-206) - Semantic, sliding window, hierarchical strategies
- ✅ [**1.207** LLM Observability & Tracing](/survey/1-207) - LangSmith, Helicone, LangFuse
- ✅ [**1.208** Fine-tuning frameworks](/survey/1-208) - Axolotl, LLaMA Factory, Unsloth, PEFT
- ✅ [**1.209** Local LLM Serving - Ollama, vLLM, llama.cpp](/survey/1-209)
- ✅ [**1.210** Multilingual & CJK LLMs](/survey/1-210) - BLOOM, XLM-RoBERTa, mBERT, ERNIE
- ✅ [**1.211** CJK Embedding Models](/survey/1-211) - M3E, text2vec-chinese, LaBSE, multilingual-e5

---

## 1.220-229: Calendar & Scheduling

**Completed: 1/10**

- ✅ [**1.220** CalDAV/iCalendar](/survey/1-220) - icalendar, caldav, vobject
- **1.221** Calendar Sync - Google Calendar, Outlook, iCloud
- **1.222** Meeting Scheduling - Calendly alternatives
- **1.223** Timezone Handling - pytz, zoneinfo, dateutil
- **1.224** Recurring Events - RRULE parsing, cron expressions
- **1.225** Calendar Visualization - Timeline views, heatmaps
- **1.226** Availability Detection - Free/busy calculation
- **1.227** Event Reminders - Notification systems
- **1.228** Calendar Import/Export - ICS, CSV conversion
- **1.229** Calendar Widgets - Embeddable components

---

## 1.230-239: Social Networks & Messaging

**Completed: 2/10**

- ✅ [**1.230** Open Social Networks](/survey/1-230) - ActivityPub, AT Protocol, Matrix, Nostr
- **1.231** AT Protocol/Bluesky - Decentralized social graph
- **1.232** Matrix Protocol - Federated chat & E2EE
- **1.233** Nostr - Simple relay protocol, Lightning payments
- ✅ [**1.234** Bot SDK Frameworks](/survey/1-234) - matrix-nio, discord.py, python-telegram-bot
- **1.235** Social Media APIs - Twitter, Reddit, Mastodon
- **1.236** Chat Webhooks - Slack, Discord, Teams
- **1.237** Push Notifications - FCM, APNs, WebPush
- **1.238** RSS/Atom Feeds - feedparser, aggregation
- **1.239** Social Graph Analysis - Follow relationships, communities

---

## 1.300-309: Civic & Government Data

**Completed: 6/10**

- ✅ [**1.300** Public Finance Modeling](/survey/1-300) - Revenue forecasting, budget planning, fiscal analysis
- ✅ [**1.301** Government Data Access](/survey/1-301) - Open data APIs, FOIA tools, data.gov integration
- ✅ [**1.302** Budget Document Parsing](/survey/1-302) - PDF extraction, financial statement analysis
- ✅ [**1.303** Civic Entity Resolution](/survey/1-303) - Agency matching, jurisdiction mapping
- ✅ [**1.304** Procurement & Contracts](/survey/1-304) - Vendor analysis, contract tracking
- ✅ [**1.305** Fiscal Health Metrics](/survey/1-305) - Financial indicators, municipal credit analysis
- **1.306-1.309** _Available for future use_

---

## Research Status

**Total Defined**: 192 research slots (including CJK expansion)
**Completed**: 119 pieces (62%)
**Remaining**: 73 pieces

**Navigation**: Use the sidebar to browse completed research, or select a category above.

---

**Want to understand our approach?** [Read the Vision →](/vision)

**Want to replicate this research?** [See the Methodology →](/survey/methodology)

---

© 2026 Ivan Schneider · [Model Citizen Developer](https://modelcitizendeveloper.com/)
Licensed under [CC BY 4.0](/license/)
