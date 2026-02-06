# What Are CJK Tokenizers?

> A brief, accessible explanation for readers new to tokenization for Chinese, Japanese, and Korean languages in Large Language Models.

## The Basic Problem

Large Language Models (LLMs) don't process text directly - they work with **tokens**, small units of meaning. Tokenization is the process of breaking text into these units.

**For English:**
```
"Hello world" → ["Hello", " world"] → [15496, 1917]
```

**For Chinese:**
```
"你好世界" → [?, ?, ?] → How many tokens?
```

The answer depends on your tokenizer, and getting it wrong costs you money and performance.

## Why CJK Is Different

### The Space Problem

**English:** Words separated by spaces → obvious boundaries
```
"The cat sat" → ["The", " cat", " sat"]
```

**Chinese:** No spaces between words → ambiguous boundaries
```
"猫坐着" (cat sitting) → ["猫", "坐着"]? or ["猫坐", "着"]?
```

### The Character Inventory Problem

**English:** 26 letters + punctuation = small alphabet
**Chinese:** 20,000+ commonly used characters

**Impact on vocabulary:**
- English: Can dedicate 50,000 tokens to common words/phrases
- Chinese: Need tokens for 20,000 base characters PLUS common combinations

## Core Concepts

### 1. Subword Tokenization

Modern tokenizers break text into **subwords** - units between characters and words.

**Why subwords?**
- Handles rare words (break into pieces)
- Efficient vocabulary size
- Balances granularity vs coverage

### 2. Byte Pair Encoding (BPE)

The most common tokenization algorithm:
1. Start with individual bytes or characters
2. Merge frequently co-occurring pairs
3. Repeat until target vocabulary size

**Example training:**
```
Initial: ["h", "e", "l", "l", "o"]
After merges: ["hel", "lo"]
Result: Fewer tokens, same meaning
```

### 3. Byte-Level vs Character-Level

**Byte-level:**
- Treats text as UTF-8 bytes
- Chinese character 猫 = 3 bytes → potentially 3 tokens

**Character-level:**
- Treats text as Unicode characters
- Chinese character 猫 = 1 character → 1+ tokens depending on vocabulary

**Critical insight:** For CJK, byte-level with English-trained vocabulary is inefficient.

## The CJK Efficiency Problem

### Token Multiplication

**GPT-4 (tiktoken, English-optimized vocabulary):**
```
English: "Hello world" → 2 tokens
Chinese: "你好世界" (Hello world) → 4-6 tokens
```

**Qwen (Chinese-optimized vocabulary):**
```
English: "Hello world" → 2 tokens
Chinese: "你好世界" (Hello world) → 2-3 tokens
```

**Why it matters:**
1. **API costs:** Pay per token (2× more tokens = 2× cost)
2. **Context windows:** 8k token limit = 4k Chinese characters vs 8k English words
3. **Performance:** More tokens = slower inference

### The UTF-8 Problem

Chinese characters use **3 bytes in UTF-8**:
```
猫 → 0xE7 0x8C 0xAB (3 bytes)
```

If a tokenizer trained on English doesn't learn to merge these bytes:
```
猫 → [0xE7, 0x8C, 0xAB] → 3 separate tokens
```

**This is why English-trained tokenizers are inefficient for CJK.**

## Common Approaches

### 1. SentencePiece

**Philosophy:** Language-independent, train from scratch

**How it works:**
- Trains directly on your corpus (no pre-tokenization)
- Learns character boundaries from data
- Handles spaces and no-spaces equally

**CJK advantage:** Explicitly designed for languages without word boundaries

**Used by:** T5, ALBERT, XLNet, many multilingual models

### 2. tiktoken (OpenAI)

**Philosophy:** Fast, universal byte-level tokenizer

**How it works:**
- Byte-level BPE on UTF-8
- Pre-built vocabulary (cl100k_base)
- Optimized for speed

**CJK challenge:** Vocabulary trained heavily on English → inefficient for CJK

**Used by:** GPT-3.5, GPT-4, OpenAI API

### 3. HuggingFace Tokenizers

**Philosophy:** Fast, flexible, ecosystem-integrated

**How it works:**
- Rust implementation (fast)
- Supports multiple algorithms (BPE, Unigram, WordPiece)
- Pre-trained models available

**CJK advantage:** Chinese-optimized models available (Qwen, BERT-base-chinese)

**Used by:** Most open-source LLMs (Llama, Qwen, BERT, etc.)

## When You Need This

### High-Volume CJK Processing
Processing millions of Chinese characters monthly → token efficiency = cost savings

### Limited Context Windows
Fitting more CJK content into fixed token limit (8k, 32k, etc.)

### Multilingual Applications
Balanced English/CJK where neither should be second-class

### Training Custom LLMs
Building models that need to understand CJK text efficiently

## What Makes a Good CJK Tokenizer?

### 1. Low Token Ratio
**Goal:** ~1.0-1.2 tokens per Chinese character (vs 2.0-3.0 for English-optimized)

### 2. No Out-of-Vocabulary (OOV)
**Goal:** Handle rare characters without failures (byte-level fallback)

### 3. Semantic Preservation
**Goal:** Common phrases become single tokens (你好 "hello" → 1 token, not 2)

### 4. Speed
**Goal:** Fast enough for real-time applications (<10ms per request)

## Common Misconceptions

### ❌ "Chinese needs character-level tokenization"
**Reality:** Subword tokenization works great IF vocabulary is trained on Chinese data

### ❌ "Byte-level is bad for CJK"
**Reality:** Byte-level is fine; English-trained vocabulary is the problem

### ❌ "You need a special tokenizer for CJK"
**Reality:** Same algorithms work; you need CJK-trained vocabulary

### ❌ "tiktoken is fastest so always use it"
**Reality:** 3× speed doesn't help if 2× token cost doubles your API bill

## Quick Decision Guide

**Using OpenAI API?**
→ tiktoken (no choice, accept the 2× CJK cost)

**Building production CJK service?**
→ HuggingFace Tokenizers with Qwen (fast + efficient)

**Training custom LLM?**
→ SentencePiece (maximum flexibility)

**Building mobile app?**
→ SentencePiece (C++, small model size)

**Research project?**
→ SentencePiece (established methodology, citable)

## Key Metrics to Track

### 1. Character-to-Token Ratio
```
Tokens / Characters = Efficiency Score
```
**Lower is better:** 1.0 = optimal, 2.0 = inefficient

### 2. Vocabulary Coverage
```
% of characters in base vocabulary
```
**Higher is better:** 99%+ coverage (rare chars use byte fallback)

### 3. Inference Speed
```
Characters tokenized per second
```
**Context-dependent:** Real-time needs 100k+/sec, batch OK with 10k+/sec

## Further Reading

### Foundational Papers
- **SentencePiece** (Kudo & Richardson, 2018) - Language-independent tokenization
- **BPE** (Sennrich et al., 2016) - Original byte pair encoding for NMT
- **Tokenizer Unfairness** (Petrov et al., 2023) - Quantifies CJK inefficiency in LLMs

### Technical Resources
- [SentencePiece Documentation](https://github.com/google/sentencepiece) - Official guides
- [tiktoken Repository](https://github.com/openai/tiktoken) - OpenAI's implementation
- [HuggingFace Tokenizers](https://github.com/huggingface/tokenizers) - Modern library

### Blog Posts
- "Working with CJK text in Generative AI pipelines" - Practical guide
- "Why TikToken is Fast" - Deep dive on performance
- "Four Ways to Tokenize Chinese Documents" - Comparison of approaches

---

**Summary:** CJK tokenization is about efficiently representing Chinese, Japanese, and Korean text in LLMs. The key challenge is that English-optimized vocabularies waste tokens on CJK characters. Solution: Use tokenizers trained on CJK data (SentencePiece, HuggingFace-Qwen) for 50% cost savings and better performance.
