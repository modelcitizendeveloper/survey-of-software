---
sidebar_position: 1
---

# Survey of Software

> A methodological approach to library selection

**Like the Great Trigonometrical Survey mapped India over 70 years, we're systematically measuring the software library landscape.** Each research piece is a triangulation point—a precise measurement you can use to navigate your own technical decisions.

---

## What We Catalog

✅ **General-purpose software components:**
- Algorithm libraries (sorting, graph algorithms, compression)
- Data processing tools (JSON parsing, serialization, streaming)
- ML frameworks (PyTorch, TensorFlow, ONNX)
- Infrastructure components (databases, messaging, caching)
- Development tools (testing, logging, monitoring)

❌ **What we exclude:**
- Application-specific integrations
- Vertical-specific solutions
- Business logic implementations
- Custom SaaS platforms

**The principle:** We catalog components you'd find in a hardware store—general-purpose tools, not custom applications.

---

## Quick Start

### 📚 Browse the Research Library

**[View the complete Research Library →](/survey)**

Organized into categories:

- 🔢 **Algorithms & Data Structures** (14 pieces)
- 📊 **Data Processing & Serialization** (14 pieces)
- 🤖 **Machine Learning & Deep Learning** (8 pieces)
- 📄 **Document & Text Processing** (6 pieces)
- 🎨 **Frontend & UI** (4 pieces)
- 🏠 **Self-Hosted & Infrastructure** (2 pieces)
- 🧠 **LLM & AI Stack** (1 piece)

### 🔍 Popular Research Pieces

- **[1.001 Sorting Libraries](/survey/1-001)** - How hardware drives algorithm choice
- **[1.050 JSON Libraries](/survey/1-050)** - Performance vs features trade-offs
- **[1.071 Deep Learning Frameworks](/survey/1-071)** - PyTorch vs TensorFlow ecosystem
- **[1.100 PDF Libraries](/survey/1-100)** - Rendering vs extraction strategies
- **[1.200 LLM Orchestration](/survey/1-200)** - Agent frameworks comparison

---

## Research Structure

Each piece contains 5 sections:

| Tab | Purpose | Read When |
|-----|---------|-----------|
| **S1: Rapid** | Quick landscape scan (10 min) | Need fast overview |
| **S2: Comprehensive** | Deep technical analysis (30-60 min) | Evaluating specific libraries |
| **S3: Need-Driven** | Methodologies & use cases (20 min) | Planning your approach |
| **S4: Strategic** | Long-term insights (15 min) | Making architectural decisions |
| **Explainer** | Domain fundamentals (10 min) | New to this technology area |

---

## How to Use This Research

### For Decision-Making

1. Read **S4** for strategic insights
2. Check **S1** for quick comparisons
3. Deep-dive **S2** when you need technical details

### For Learning

1. Start with **Explainer** to build foundations
2. Skim **S1** to see the landscape
3. Study **S3** for methodology patterns

### For Architecture

- **S4** reveals ecosystem-level patterns
- **S3** informs evaluation approaches
- **S2** provides implementation depth

---

**Ready to explore?** [Start with the Research Library →](/survey)

**Want the bigger picture?** [Read our Vision →](/vision)

## 🔍 Recent Additions

### Dimensional Research Expansion (January 2026)

The survey now includes **dimensional coverage** across three axes:

**1. Core Topics** - General-purpose library research (1.xxx)
- 1.081: OCR Libraries (Tesseract, EasyOCR, PaddleOCR)
- 1.088: ASR Libraries (Whisper, SpeechRecognition)
- 1.089: TTS Libraries (MeloTTS, gTTS, pyttsx3)
- 1.169: Text Summarization (Sumy, snownlp, TextRank)

**2. Language-Specific Variants** (1.xxx.n)
- 1.001.1: CJK Collation & Sorting (radical-stroke, pinyin order)
- 1.033.5: Chinese Dialect NLP (PyCantonese, taibun for Hokkien)

**3. Specialized Tools**
- 1.168: Chinese Spell & Grammar Checking
- 1.167: CJK Text Layout & Wrapping
- 1.175: Furigana & Ruby Annotation

**Total Research Topics:** 34+ topics across general-purpose libraries and CJK-specific tools

---

## 🐉 "Here Be Dragons"

Some areas reveal **gaps in the software ecosystem** - categories where libraries don't yet exist:
- Wu & Hakka NLP libraries (corpora exist, no pip-installable tools)
- Low-resource tonal languages (Thai, Vietnamese, Burmese)

These gaps show what software still needs to be built.
