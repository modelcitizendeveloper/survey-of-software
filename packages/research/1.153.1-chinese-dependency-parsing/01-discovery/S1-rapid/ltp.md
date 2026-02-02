# LTP (Language Technology Platform)

## What It Is
Chinese-focused NLP platform from Harbin Institute of Technology (HIT-SCIR). N-LTP is the neural version using multi-task learning with shared pretrained models.

## Chinese Support
Six fundamental Chinese NLP tasks:
- **Lexical analysis**: Word segmentation, POS tagging, NER
- **Syntactic parsing**: Dependency parsing
- **Semantic parsing**: Semantic dependency parsing, semantic role labeling

**Unique approach**: Multi-task framework with knowledge distillation (single-task teacher models train multi-task student)

## Technical Overview

**Language**: Python
**Architecture**: Shared pretrained model for all tasks (vs independent models per task)

**Dependency parsing**:
- Deep biaffine neural parser (Dozat & Manning 2017)
- Eisner algorithm for decoding (Rust implementation for speed)
- Both syntactic and semantic dependency parsing

**Key innovation**: Captures shared knowledge across related Chinese tasks through multi-task learning

**Availability**:
- Open-source on GitHub
- LTP-Cloud service (REST API)
- Pretrained models included

## Ecosystem Position

**Strengths**:
- Specifically optimized for Chinese (not adapted from multilingual)
- Multi-task learning captures Chinese linguistic patterns efficiently
- First toolkit supporting all six fundamental Chinese NLP tasks
- Both local and cloud deployment options
- Academic backing from HIT-SCIR

**Limitations**:
- Chinese-only (no multilingual support)
- Smaller community than HanLP or Stanza
- Performance issues noted in early versions (LTP>ICTCLAS but slower)
- Less English documentation than alternatives
- Requires understanding of Chinese-specific annotation schemes

## Quick Assessment

**Use LTP when**:
- Building Chinese-only applications
- Need semantic dependency parsing (SDP) specific to Chinese
- Want multi-task efficiency for comprehensive Chinese NLP
- Prefer single model over pipeline of independent models
- Academic research on Chinese linguistics

**Choose alternatives when**:
- Need multilingual support (→ Stanza, HanLP)
- Prioritize raw speed over task breadth (→ Stanza)
- Require extensive English documentation (→ Stanza)
- Building lightweight deployments (multi-task model is heavier)
- Need wider community support

## Key Resources
- GitHub: https://github.com/HIT-SCIR/ltp
- N-LTP paper: https://arxiv.org/abs/2009.11616
- LTP-Cloud: https://www.ltp-cloud.com/intro_en
- ACL Anthology: https://aclanthology.org/2021.emnlp-demo.6/
