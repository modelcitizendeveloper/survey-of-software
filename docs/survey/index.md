---
sidebar_position: 0
slug: /survey
id: survey-intro
title: "The Survey"
---

# Survey of Software

> **Systematic coverage of general-purpose software libraries**
> Like the Great Trigonometrical Survey mapped India, we're measuring the software library landscape.

**[What is this? →](/about)** | **[The Vision →](/vision)** | **[Methodology →](/survey/replication)**

---

## 1.001-009: Sorting & Searching Algorithms

**Completed: 5/9**

- ✅ [**1.001** Sorting Libraries](/survey/1-001) - Timsort, parallel sorts, radix sorts
- ✅ [**1.002** Fuzzy Search](/survey/1-002) - FuzzyWuzzy, RapidFuzz, TheFuzz
- ✅ [**1.003** Full-Text Search](/survey/1-003) - Whoosh, Tantivy, MeiliSearch clients
- ✅ [**1.004** Binary Search Trees](/survey/1-004) - B-trees, AVL, Red-Black implementations
- ✅ [**1.005** Spatial Search](/survey/1-005) - PostGIS, Elasticsearch Geo, rtree
- **1.006** Graph Search - A*, Dijkstra, BFS/DFS implementations
- **1.007** Pattern Matching - KMP, Boyer-Moore, Aho-Corasick
- **1.008** Time Series Search - DTW, shapelet discovery
- **1.009** Similarity Search - LSH, MinHash, SimHash

---

## 1.010-019: Graph & Network Algorithms

**Completed: 1/10**

- ✅ [**1.010** Graph Analysis](/survey/1-010) - NetworkX, graph-tool, igraph
- **1.011** Graph Database Clients - Neo4j, ArangoDB, TigerGraph
- **1.012** Community Detection - Louvain, label propagation, spectral
- **1.013** Shortest Path Optimization - Specialized path algorithms
- **1.014** Network Flow - Max flow, min cost flow
- **1.015** Graph Visualization - Graphviz, Gephi, Cytoscape
- **1.016** Social Network Analysis - Centrality, clustering coefficient
- **1.017** Bipartite Matching - Hungarian algorithm, Hopcroft-Karp
- **1.018** Graph Embedding - node2vec, DeepWalk, Graph Neural Networks
- **1.019** Dynamic Graphs - Temporal networks, streaming graphs

---

## 1.020-029: Mathematical & Statistical Algorithms

**Completed: 1/10**

- **1.020** Linear Algebra - NumPy vs Eigen vs Armadillo
- **1.021** Statistical Testing - Hypothesis testing, A/B testing
- ✅ [**1.022** Optimization](/survey/1-022) - scipy.optimize, OR-Tools, CVXPY, PuLP
- **1.023** Symbolic Math - SymPy vs SageMath
- **1.024** Random Number Generation - PCG, Mersenne Twister
- **1.025** Prime Number Libraries - Factorization, primality testing
- **1.026** Combinatorics - Permutations, combinations, partitions
- **1.027** Numerical Integration - Quadrature methods
- **1.028** FFT Libraries - FFTW, pyFFTW, scipy.fft
- **1.029** Matrix Decomposition - SVD, eigenvalue, QR

---

## 1.030-039: String & Text Algorithms

**Completed: 6/10**

- **1.030** String Matching - Exact, approximate, regex engines
- **1.031** Text Diff - Myers, patience diff, semantic diff
- **1.032** String Metrics - Edit distance, Jaro-Winkler, cosine
- ✅ [**1.033** NLP Libraries](/survey/1-033) - spaCy, Transformers, NLTK
  - ✅ [**1.033.1** Intent Classification](/survey/1-033-1) - Zero-Shot, SetFit, sentence-transformers
  - ✅ [**1.033.2** Chinese Word Segmentation](/survey/1-033-2) - Jieba, CKIP, pkuseg, LTP
  - ✅ [**1.033.4** Named Entity Recognition (CJK)](/survey/1-033-4) - spaCy, Stanford NER, BERT-NER
- ✅ [**1.034** Email Libraries](/survey/1-034) - smtplib, yagmail, MIME handling
- **1.035** Tokenization - Wordpiece, BPE, SentencePiece
- **1.036** Stemming & Lemmatization - Porter, Snowball, WordNet
- **1.037** String Compression - LZ4, Snappy, Zstandard for strings
- **1.038** Unicode Handling - Normalization, transliteration
- ✅ [**1.039** Template Engines](/survey/1-039) - Jinja2, Handlebars, Mustache

---

## 1.040-049: Data Structure Libraries

**Completed: 5/10**

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

## 1.060-069: Cryptographic & Hashing

**Completed: 3/10**

- ✅ [**1.060** Cryptographic Libraries](/survey/1-060) - cryptography vs PyNaCl
- ✅ [**1.061** Hashing](/survey/1-061) - hashlib, xxhash, blake3
- **1.062** Password Hashing - argon2-cffi vs bcrypt (covered in 1.060)
- ✅ [**1.063** JWT Libraries](/survey/1-063) - PyJWT, python-jose, Authlib
- **1.064** _Covered by 1.060_
- **1.065** _Covered by 1.060_
- **1.066** _Covered by 1.060_
- **1.067** Random Token Generation - secrets, uuid patterns
- **1.068** Certificate Handling - cryptography x509, certifi
- **1.069** Blockchain Libraries - Merkle trees, hash chains

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

**Completed: 2/10**

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

**Completed: 3/10**

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

**Completed: 2/10**

- ✅ [**1.100** Text Processing](/survey/1-100) - Regex, string manipulation, NLP utilities
- **1.101** PDF Processing - ReportLab, WeasyPrint, PyPDF2
- **1.102** Document Parsing - python-docx, openpyxl, pandas Excel
- **1.103** Markdown Processing - markdown-it, mistune, commonmark
- **1.104** Syntax Highlighting - Pygments, highlight.js
  - ✅ [**1.104.1** Code Parsing & AST](/survey/1-104-1) - libcst, ast, redbaron
  - **1.104.2** Code Formatting - Black, Prettier, ruff
- **1.105** Translation & i18n - gettext, Babel, i18next
- **1.106** Speech Recognition & TTS - Whisper, Coqui, Piper
- **1.107** OCR Libraries - Tesseract, EasyOCR
- **1.108** Spell Checking - SymSpell, LanguageTool
- **1.109** Content Extraction - BeautifulSoup, Scrapy, newspaper3k

---

## 1.110-119: User Interface & Frontend

**Completed: 1/10**

- ✅ [**1.110** Frontend Frameworks](/survey/1-110) - React, Vue, Svelte, Angular
  - **1.110.1** React Meta-Frameworks - Next.js, Remix, Gatsby
  - **1.110.2** Vue Meta-Frameworks - Nuxt, VitePress
  - **1.110.3** Svelte Meta-Frameworks - SvelteKit
  - **1.110.4** Browser Python - Pyodide, JupyterLite, PyScript
- **1.111** State Management - Redux, Zustand, Jotai, Pinia
- **1.112** CSS Frameworks - Tailwind, Bootstrap, Material UI
- **1.113** UI Component Libraries - shadcn/ui, Radix, Headless UI
- **1.114** Build Tools - Vite, Webpack, Turbopack, esbuild
- **1.115** Form & Validation - React Hook Form, Zod, Yup
- **1.116** Data Visualization - D3.js, Chart.js, Recharts
- **1.117** Animation - Framer Motion, GSAP, React Spring
- **1.118** Testing - Jest, Vitest, Playwright, Cypress
- **1.119** Mobile Frameworks - React Native, Flutter, Expo

---

## 1.120-129: Simulation & Modeling

**Completed: 3/10**

- ✅ [**1.120** Discrete Event Simulation](/survey/1-120) - SimPy, Salabim, Mesa
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

**Completed: 4/10**

- ✅ [**1.140** Classical Languages](/survey/1-140) - CLTK, pyLatinam, PyWORDS
- ✅ [**1.141** Spaced Repetition](/survey/1-141) - SM-2, SM-18, FSRS algorithms
- ✅ [**1.142** Flashcard Systems](/survey/1-142) - Anki, genanki, AnkiConnect
- **1.143** Language Detection - langdetect, polyglot, fastText
- **1.144** Phonetics - IPA transcription, eSpeak, Forvo API
- **1.145** Grammar Checking - LanguageTool, GrammarBot
- **1.146** Vocabulary Databases - WordNet, ConceptNet, Wiktionary
- **1.147** Language Corpora - Brown Corpus, CoNLL datasets
- ✅ [**1.148** Morphological Analysis](/survey/1-148) - SudachiPy, pymorphy3, UDPipe
- **1.149** SLA Tools - CEFR assessment, proficiency testing

---

## 1.150-159: Reading & Text Analysis (Language Learning)

**Completed: 0/10**

- **1.150** Classical Text Corpora - Perseus, PHI5/PHI7, Latin Library
- **1.151** Vocabulary Frequency - DCC Core, Dickinson College
- **1.152** Reading Difficulty & Readability - Flesch-Kincaid, lexical coverage, i+1 detection
- **1.153** Sentence Parsing - Universal Dependencies parsers, Stanza, syntax trees
- **1.154** Graded Reader Generation - Text leveling, vocab substitution
- **1.155** Parallel Text Alignment - Latin-English, sentence alignment
- **1.156** Text Annotation UI - Glossing, interlinear display
- **1.157** Reading Comprehension - Question generation, validation
- **1.158** Vocabulary Tracking - Learning curves, retention modeling
- **1.159** Adaptive Recommendation - Personalized difficulty

---

## 1.160-169: Character-Based Writing Systems (CJK)

**Completed: 5/10**

- ✅ [**1.160** Character Databases](/survey/1-160) - Unihan, CHISE, IDS, CJKVI
- ✅ [**1.161** Radical & Component Analysis](/survey/1-161) - Character decomposition, semantic components
- ✅ [**1.162** Handwriting Recognition (CJK)](/survey/1-162) - Zinnia, Tegaki, Google Cloud Vision, Azure
- ✅ [**1.163** Character Encoding](/survey/1-163) - Big5, GB2312, GBK, GB18030, Unicode CJK
- ✅ [**1.164** Traditional ↔ Simplified Conversion](/survey/1-164) - OpenCC, HanziConv, zhconv-rs
- **1.165** Stroke Order & Writing - Character writing systems
- **1.166** OCR (CJK-specific) - Specialized CJK optical character recognition
- **1.167-1.169** _Available for future use_

---

## 1.170-179: Translation & Alignment

**Completed: 0/10**

- **1.170** Machine Translation APIs - Google Translate, DeepL, Azure
- **1.171** Sentence Alignment - Parallel corpora alignment
- **1.172** Translation Memory - TM systems, CAT tools
- **1.173** Computer-Assisted Translation - CAT tool comparison
- **1.174** Literary Translation Tools - Context-aware translation
- **1.175-1.179** _Available for future use_

---

## 1.200-209: LLM & AI Stack

**Completed: 1/10**

- ✅ [**1.200** LLM Orchestration](/survey/1-200) - LangChain, LlamaIndex, RAG
- **1.201** LLM Agent Frameworks - AutoGen, CrewAI, MetaGPT
- **1.202** Prompt Engineering - DSPy, guidance, LMQL
- **1.203** Vector Databases - ChromaDB, Pinecone, Qdrant
- **1.204** RAG Pipelines - Document loading, chunking, retrieval
- **1.205** LLM Evaluation - RAGAS, DeepEval, PromptFoo
- **1.206** LLM Caching - GPTCache, prompt caching patterns
- **1.207** Fine-Tuning - Hugging Face Trainer, LoRA, QLoRA
- **1.208** Model Compression - Quantization, pruning, distillation
- **1.209** Local LLM Serving - Ollama, vLLM, llama.cpp

---

## Research Status

**Total Defined**: 189 research slots (including CJK expansion)
**Completed**: 47 pieces (25%)
**Remaining**: 142 pieces

**Navigation**: Use the sidebar to browse completed research, or select a category above.

---

**Want to understand our approach?** [Read the Vision →](/vision)
**Want to replicate this research?** [See the Methodology →](/survey/replication)
