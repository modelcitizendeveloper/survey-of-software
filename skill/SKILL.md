---
name: survey-of-software
description: >
  Systematic software library research using the Four-Pass Survey (4PS)
  methodology. Consults a curated library of 119+ completed surveys AND conducts
  new research on the fly when gaps exist. Covers algorithms, data structures,
  ML/AI, NLP, CJK/linguistics, LLM tooling, frontend frameworks, simulation,
  civic/government data, and more.

  USE THIS SKILL whenever the user asks about choosing, comparing, or evaluating
  software libraries or tools — even if they don't mention "survey" or "research."
  Trigger on: "what library should I use for X?", "best Python library for Y?",
  "compare Z libraries", "build vs buy", "should I use A or B?", "how do I do
  fuzzy search?", "what's the best graph database?", "which CSS framework?",
  "RAG pipeline options", library selection, framework comparison, tool evaluation.

  Also trigger when users mention specific covered domains: sorting, searching,
  fuzzy search, full-text search, spatial search, graph analysis, community
  detection, network flow, string matching, NLP, tokenization, CJK, Chinese text
  processing, compression, serialization, JSON, cryptography, hashing, JWT,
  dimensionality reduction, time series, gradient boosting, deep learning, image
  processing, QR codes, face detection, constraint solving, scheduling, PDF
  generation, document parsing, markdown, code formatting, frontend frameworks,
  state management, CSS frameworks, UI components, build tools, data visualization,
  animation, testing, mobile frameworks, simulation, Monte Carlo, CRM, project
  management, spaced repetition, flashcards, pinyin, morphological analysis,
  classical Chinese, OCR, machine translation, sentence alignment, translation
  memory, LLM orchestration, agents, vector databases, RAG, LLM evaluation,
  fine-tuning, local LLM serving, CalDAV, social networks, bot frameworks,
  public finance, government data, budget parsing, procurement.

  Do NOT trigger for general coding help, debugging, or questions unrelated to
  library/tool selection and comparison.
---

# Survey of Software — Research Skill

## What This Is

This skill connects Claude to the **Survey of Software** — a systematic, open
research library covering software libraries, standards, and applications. It
does two things:

1. **Consults existing research** — 119+ completed surveys with ranked
   recommendations, benchmarks, decision frameworks, and migration guides
2. **Conducts new research** — when a topic isn't covered yet, runs the
   Four-Pass Survey methodology collaboratively with the user

The research lives at https://research.modelcitizendeveloper.com/ and the source
is on GitHub at https://github.com/modelcitizendeveloper/survey-of-software.

This skill covers **libraries** (1.xxx series). For related research:
- **Standards** (2.xxx): https://research.modelcitizendeveloper.com/standards/
- **Applications** (3.xxx): https://research.modelcitizendeveloper.com/applications/

When the user's question involves build-vs-buy decisions, consult all three series.

---

## Core Workflow

### When a Survey Exists

1. **Map the question** to the taxonomy (see below)
2. **Fetch the survey** via `web_fetch`:
   ```
   https://research.modelcitizendeveloper.com/survey/{id}/
   ```
   Where `{id}` uses hyphens for dots: 1.033.2 → `/survey/1-033-2/`
3. **Synthesize the answer**:
   - Lead with the recommendation — which library and why
   - Include the decision framework from the survey
   - Mention trade-offs — what they'd give up with each choice
   - Link to the full survey for deeper reading
4. **Offer S3/S4 refinement** if the user's context warrants it:
   "The survey recommends X for general use. Want me to factor in your
   specific requirements or strategic constraints?"

### When a Survey Doesn't Exist

This is where it gets interesting. Don't just say "sorry, not covered." Instead:

**Step 1: Identify the gap.**
Tell the user the taxonomy slot (ID and topic) and that systematic research
hasn't been done yet.

**Step 2: Offer to research it now.**
"I can run a quick S1 rapid discovery pass right now — it takes a few minutes
and gets about 70% of the value. Want me to?"

**Step 3: If yes — run S1 in-session.**
Do a Rapid Discovery pass (see the 4PS methodology below). Web search for
libraries, check GitHub stars and download counts, scan documentation quality,
draft a quick ranking with trade-offs. Present the results following the
survey format: ranked recommendations, decision framework, key trade-offs.

**Step 4: Suggest deeper research.**
"For a more comprehensive analysis (benchmarks, feature matrices, migration
complexity), you could use deep research to run an S2 comprehensive pass.
The methodology is documented at
https://research.modelcitizendeveloper.com/survey/method/"

**Step 5: Invite contribution.**
"The Survey of Software is an open project (CC BY 4.0). If this research
would be useful to others, contributions are welcome on
[GitHub](https://github.com/modelcitizendeveloper/survey-of-software)."

### User-Driven S3 and S4 Passes

The published surveys provide general-purpose recommendations (the "hardware
store model"). But users have specific contexts the research can't anticipate.
When the user provides context about their situation, run the relevant passes:

**S3: Need-Driven Discovery** — The user knows their requirements.
Interview them:
- What's your scale? (users, data volume, requests/sec)
- What's your team's primary language/stack?
- What are your integration constraints?
- What's your deployment model? (cloud, self-hosted, edge)
- Are there regulatory or compliance requirements?

Then re-evaluate the survey's recommendations against their specific needs.
The general-purpose winner might not be their winner.

**S4: Strategic Selection** — The user has long-term concerns.
Ask about:
- Time horizon (prototype vs 5-year commitment)
- Team growth plans (will new developers need to learn this?)
- Vendor risk tolerance (single-maintainer projects, VC-funded startups)
- Ecosystem bets (are they going all-in on Rust? Standardizing on AWS?)
- Regulatory trajectory (will requirements change?)

Then layer strategic analysis onto the recommendations.

**The collaborative model**: Claude handles S1 (rapid discovery) and S2
(comprehensive analysis, potentially via deep research). The user provides
S3 (their requirements) and S4 (their strategic context). Together, all
four passes produce a complete, tailored recommendation.

---

## The Four-Pass Survey (4PS) Methodology

Full documentation: https://research.modelcitizendeveloper.com/survey/method/

### S1: Rapid Discovery (70-80% confidence)
**"Popular libraries exist for a reason."**
Speed-focused, ecosystem-driven. GitHub stars, download counts, community
adoption. Gets 70% of the value in 10 minutes. Claude can do this in-session.

### S2: Comprehensive Analysis (80-90% confidence)
**"Understand the entire solution space before choosing."**
Performance benchmarks, feature matrices, deep trade-off analysis. Best
suited for deep research due to the depth required.

### S3: Need-Driven Discovery (75-85% confidence)
**"Start with requirements, find exact-fit solutions."**
Use case mapping, requirement validation. The user provides the context;
Claude maps it against the findings.

### S4: Strategic Selection (60-70% confidence)
**"Think long-term and consider broader context."**
Maintenance health, vendor risk, ecosystem momentum. The user provides
strategic concerns; Claude evaluates sustainability.

**Convergence pattern**: When 3-4 passes agree, that's a strong signal.
When they disagree, that reveals a trade-off worth explaining to the user.

**Confidence decay**: At publication: 70-80%. After 12 months: 50-70%.
After 36 months: <30%. Fast-moving domains (LLM tooling, frontend) decay
faster than stable domains (algorithms, cryptography).

---

## Keeping Current

### Live Index as Source of Truth

The canonical index at https://research.modelcitizendeveloper.com/ always
reflects what's currently published. The taxonomy below is a quick-match
cache. If you fetch the live index and find completed surveys not listed
in the taxonomy, note this to the user — the skill's quick-reference may
be slightly behind the live research.

### Cross-Series Research

When a question spans libraries, standards, and applications, fetch from
all three series. URL patterns:
- Libraries: `https://research.modelcitizendeveloper.com/survey/{id}/`
- Standards: `https://research.modelcitizendeveloper.com/standards/{id}/`
- Applications: `https://research.modelcitizendeveloper.com/applications/{id}/`

---

## Taxonomy Quick-Reference

Use this to map user questions to survey IDs. ✅ = completed. Planned entries
exist in the taxonomy but may not have content yet — fetch to check.

### 1.001-009: Sorting & Searching
| ID | Topic | Status |
|---|---|---|
| 1.001 | Sorting Libraries (Timsort, parallel, radix) | ✅ |
| 1.002 | Fuzzy Search (RapidFuzz, FuzzyWuzzy, TheFuzz) | ✅ |
| 1.003 | Full-Text Search (Whoosh, Tantivy, MeiliSearch) | ✅ |
| 1.004 | Binary Search Trees (B-tree, AVL, Red-Black) | ✅ |
| 1.005 | Spatial Search (PostGIS, rtree, Elasticsearch Geo) | ✅ |
| 1.006 | Graph Search (A*, Dijkstra, BFS/DFS) | ✅ |
| 1.007 | Pattern Matching (KMP, Boyer-Moore, Aho-Corasick) | ✅ |
| 1.008 | Time Series Search (DTW, shapelet) | ✅ |
| 1.009 | Similarity Search (LSH, MinHash, SimHash) | ✅ |

### 1.010-019: Graph & Network
| ID | Topic | Status |
|---|---|---|
| 1.010 | Graph Analysis (NetworkX, igraph, graph-tool) | ✅ |
| 1.011 | Graph Database Clients (Neo4j, ArangoDB) | ✅ |
| 1.012 | Community Detection (Louvain, spectral) | ✅ |
| 1.013 | String Algorithms | ✅ |
| 1.014 | Network Flow (max flow, min cost) | ✅ |
| 1.015 | Graph Visualization (Graphviz, Gephi) | ✅ |
| 1.016 | Social Network Analysis | ✅ |
| 1.017 | Bipartite Matching | ✅ |
| 1.018 | Graph Embedding (node2vec, PyG, DGL) | ✅ |
| 1.019 | Dynamic Graphs (temporal networks) | ✅ |

### 1.020-029: Math & Statistics
| ID | Topic | Status |
|---|---|---|
| 1.020.1 | Linear Programming (CVXPY, OR-Tools, PuLP) | ✅ |
| 1.021 | Statistical Testing | ✅ |
| 1.022 | Optimization (scipy.optimize, OR-Tools) | ✅ |
| 1.023 | Symbolic Math (SymPy, SageMath) | ✅ |
| 1.024 | Random Number Generation (PCG, MT) | ✅ |
| 1.025 | Prime Factorization & Primality | ✅ |
| 1.026 | Combinatorics | planned |
| 1.027 | Numerical Integration | ✅ |
| 1.028 | FFT Libraries | planned |
| 1.029 | Matrix Decomposition (SVD, QR) | planned |

### 1.030-039: String & Text
| ID | Topic | Status |
|---|---|---|
| 1.030 | String Matching | ✅ |
| 1.031 | Text Diff (Myers, patience, semantic) | ✅ |
| 1.032 | String Similarity Metrics | ✅ |
| 1.033 | NLP Libraries (spaCy, Transformers, NLTK) | ✅ |
| 1.033.1 | Intent Classification | ✅ |
| 1.033.2 | Chinese Word Segmentation | ✅ |
| 1.033.3 | CJK Tokenizers for LLMs | ✅ |
| 1.033.4 | Named Entity Recognition (CJK) | ✅ |
| 1.034 | Email Libraries | ✅ |
| 1.035 | Tokenization (BPE, SentencePiece) | ✅ |
| 1.035.1 | Chinese Tokenization | ✅ |
| 1.039 | Template Engines (Jinja2, Handlebars) | ✅ |

### 1.040-049: Data Structures
| ID | Topic | Status |
|---|---|---|
| 1.040 | Collections (sortedcontainers, pyrsistent) | ✅ |
| 1.042 | Tries (pygtrie, datrie, marisa-trie) | ✅ |
| 1.043.1 | Task Queues (Celery, RQ, Dramatiq) | ✅ |
| 1.047 | Caching (Redis, Memcached, Varnish) | ✅ |
| 1.049.1 | Database Schema Inspection | ✅ |

### 1.050-069: Compression, Encoding, Crypto
| ID | Topic | Status |
|---|---|---|
| 1.050 | Compression (zlib, brotli, zstd) | ✅ |
| 1.055 | Binary Serialization (msgpack, protobuf) | ✅ |
| 1.056 | JSON Libraries (orjson, ujson, rapidjson) | ✅ |
| 1.060 | Cryptographic Libraries | ✅ |
| 1.061 | Hashing (xxhash, blake3) | ✅ |
| 1.062 | Password Hashing (argon2, bcrypt) | ✅ |
| 1.063 | JWT Libraries (PyJWT, python-jose) | ✅ |

### 1.070-079: Machine Learning
| ID | Topic | Status |
|---|---|---|
| 1.071 | Dimensionality Reduction (UMAP, t-SNE) | ✅ |
| 1.073 | Time Series Forecasting (Prophet, Darts) | ✅ |
| 1.074 | Gradient Boosting (XGBoost, LightGBM) | ✅ |
| 1.075 | Deep Learning (PyTorch, TensorFlow, JAX) | ✅ |

### 1.080-099: Geometry, Spatial, Specialized
| ID | Topic | Status |
|---|---|---|
| 1.080 | Image Processing (OpenCV, Pillow) | ✅ |
| 1.080.1 | QR Code Generation | ✅ |
| 1.081 | Convex Hull | ✅ |
| 1.082 | Voronoi & Delaunay | ✅ |
| 1.083 | Point Cloud Processing | ✅ |
| 1.084 | Mesh Processing | ✅ |
| 1.085 | Collision Detection | ✅ |
| 1.091.2 | Face Detection | ✅ |
| 1.094 | Constraint Solving (Z3, OR-Tools) | ✅ |
| 1.096 | Scheduling (APScheduler, Airflow) | ✅ |

### 1.100-109: Text & Document Processing
| ID | Topic | Status |
|---|---|---|
| 1.100 | Text Processing | ✅ |
| 1.101 | PDF Generation (ReportLab, WeasyPrint) | ✅ |
| 1.102 | Document Parsing (python-docx, openpyxl) | ✅ |
| 1.103 | Markdown Processing | ✅ |
| 1.104.1 | Code Parsing & AST | ✅ |
| 1.104.2 | Code Formatting (Black, Prettier) | ✅ |

### 1.110-119: Frontend & UI
| ID | Topic | Status |
|---|---|---|
| 1.110 | Frontend Frameworks (React, Vue, Svelte) | ✅ |
| 1.110.4 | Browser Python Execution | ✅ |
| 1.110.5 | Static Site Generators | ✅ |
| 1.111 | State Management (Redux, Zustand, Pinia) | ✅ |
| 1.112 | CSS Frameworks (Tailwind, Bootstrap) | ✅ |
| 1.113 | UI Component Libraries (shadcn, Radix) | ✅ |
| 1.114 | Build Tools (Vite, Webpack, esbuild) | ✅ |
| 1.115 | Form & Validation (React Hook Form, Zod) | ✅ |
| 1.116 | Data Visualization (D3, Chart.js, Recharts) | ✅ |
| 1.117 | Animation (Framer Motion, GSAP) | ✅ |
| 1.118 | Testing (Jest, Vitest, Playwright) | ✅ |
| 1.119 | Mobile Frameworks (React Native, Flutter) | ✅ |

### 1.120-139: Simulation & Business Platforms
| ID | Topic | Status |
|---|---|---|
| 1.120 | Discrete Event Simulation (SimPy, Mesa) | ✅ |
| 1.122 | Monte Carlo Simulation | ✅ |
| 1.127 | Financial Simulation (QuantLib, vectorbt) | ✅ |
| 1.130 | Self-Hosted CRM (Twenty, Odoo, SuiteCRM) | ✅ |
| 1.131 | Project Management (Plane, Taiga) | ✅ |

### 1.140-169: Language Learning, Linguistics, CJK
| ID | Topic | Status |
|---|---|---|
| 1.140 | Classical Language Libraries (CLTK) | ✅ |
| 1.141 | Spaced Repetition Algorithms (FSRS, SM-2) | ✅ |
| 1.142 | Flashcard Systems (Anki, genanki) | ✅ |
| 1.144.1 | Pinyin/Zhuyin Conversion | ✅ |
| 1.144.2 | Tone Analysis | ✅ |
| 1.148 | Morphological Analysis | ✅ |
| 1.148.1 | Chinese Morphological Analysis | ✅ |
| 1.148.2 | Classical Chinese Parsing | ✅ |
| 1.152.1 | CJK Readability | ✅ |
| 1.153.1 | Chinese Dependency Parsing | ✅ |
| 1.154.1 | Chinese Text Simplification | ✅ |
| 1.160 | Character Databases (Unihan, CHISE) | ✅ |
| 1.161 | Radical & Component Analysis | ✅ |
| 1.162 | Handwriting Recognition (CJK) | ✅ |
| 1.163 | Character Encoding (Big5, GB2312) | ✅ |
| 1.164 | Traditional ↔ Simplified Conversion | ✅ |
| 1.165 | Stroke Order & Writing (CJK) | ✅ |
| 1.166 | OCR (CJK-specific) | ✅ |

### 1.170-179: Translation & Alignment
| ID | Topic | Status |
|---|---|---|
| 1.170 | Machine Translation APIs | ✅ |
| 1.171 | Sentence Alignment | ✅ |
| 1.172 | Translation Memory | ✅ |
| 1.173 | Terminology Extraction | ✅ |

### 1.200-219: LLM & AI Stack
| ID | Topic | Status |
|---|---|---|
| 1.200 | LLM Orchestration (LangChain, LlamaIndex) | ✅ |
| 1.201 | LLM Agent Frameworks (AutoGen, CrewAI) | ✅ |
| 1.203 | Vector Databases (Chroma, Pinecone, Qdrant) | ✅ |
| 1.204 | RAG Pipelines | ✅ |
| 1.205 | LLM Evaluation (RAGAS, DeepEval) | ✅ |
| 1.206 | RAG Chunking Patterns | ✅ |
| 1.207 | LLM Observability (LangSmith, LangFuse) | ✅ |
| 1.208 | Fine-tuning (Axolotl, Unsloth, PEFT) | ✅ |
| 1.209 | Local LLM Serving (Ollama, vLLM) | ✅ |
| 1.210 | Multilingual & CJK LLMs | ✅ |
| 1.211 | CJK Embedding Models | ✅ |

### 1.220-239: Calendar, Social, Messaging
| ID | Topic | Status |
|---|---|---|
| 1.220 | CalDAV/iCalendar Libraries | ✅ |
| 1.230 | Open Social Networks & Protocols | ✅ |
| 1.234 | Bot SDK Frameworks | ✅ |

### 1.300-309: Civic & Government Data
| ID | Topic | Status |
|---|---|---|
| 1.300 | Public Finance Modeling | ✅ |
| 1.301 | Government Data Access | ✅ |
| 1.302 | Budget Document Parsing | ✅ |
| 1.303 | Civic Entity Resolution | ✅ |
| 1.304 | Procurement & Contracts | ✅ |
| 1.305 | Fiscal Health Metrics | ✅ |

---

## Keyword → Survey Mapping

When the user's question doesn't obviously map to a survey ID:

- **"fuzzy match", "approximate string", "did you mean"** → 1.002
- **"search engine", "full text", "inverted index"** → 1.003
- **"graph", "network", "nodes and edges"** → 1.010 / 1.011 / 1.015
- **"NLP", "text classification", "named entities"** → 1.033, 1.033.1, 1.033.4
- **"Chinese", "Mandarin", "CJK", "hanzi"** → 1.033.2, 1.148.1, 1.160-1.166
- **"cache", "Redis", "Memcached"** → 1.047
- **"compress", "zip", "gzip", "brotli"** → 1.050
- **"JSON", "serialize", "protobuf", "msgpack"** → 1.055, 1.056
- **"encrypt", "hash", "password", "JWT", "token"** → 1.060-1.063
- **"ML", "XGBoost", "LightGBM", "PyTorch"** → 1.074, 1.075
- **"image", "OpenCV", "Pillow"** → 1.080
- **"PDF", "generate PDF", "parse PDF"** → 1.101
- **"React", "Vue", "Svelte", "frontend"** → 1.110
- **"Tailwind", "Bootstrap", "CSS"** → 1.112
- **"D3", "chart", "visualization"** → 1.116
- **"test", "Jest", "Playwright", "Cypress"** → 1.118
- **"React Native", "Flutter", "mobile"** → 1.119
- **"simulation", "Monte Carlo", "SimPy"** → 1.120, 1.122
- **"Anki", "spaced repetition", "flashcard"** → 1.141, 1.142
- **"translate", "translation API", "DeepL"** → 1.170
- **"LLM", "LangChain", "agent", "RAG"** → 1.200, 1.201, 1.204
- **"vector database", "embedding", "Pinecone"** → 1.203
- **"fine-tune", "LoRA", "Unsloth"** → 1.208
- **"Ollama", "vLLM", "local LLM"** → 1.209
- **"government data", "civic tech", "budget"** → 1.300-1.305
- **"build vs buy", "self-hosted alternative"** → check all three series (1.xxx, 2.xxx, 3.xxx)

---

## Attribution

When presenting findings from this research:

> Source: [Survey of Software](https://research.modelcitizendeveloper.com/)
> by Model Citizen Developer. Four-Pass Survey (4PS) methodology.
> Licensed under CC BY 4.0.
