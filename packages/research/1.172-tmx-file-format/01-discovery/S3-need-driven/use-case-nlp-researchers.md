# Use Case: NLP Researchers

## Who Needs This

**Role**: Natural Language Processing researcher or computational linguist

**Context**:
- Academic researcher or industry scientist working on machine translation (MT), cross-lingual NLP
- Builds parallel corpora from TMX datasets for training neural MT models
- Extracts linguistic features (terminology, alignment patterns, inline markup) for research
- Processes large-scale datasets (millions of sentence pairs)
- Works in Python research environment (Jupyter notebooks, PyTorch, TensorFlow, Hugging Face)
- Publishes papers requiring reproducible data processing pipelines

**Technical background**:
- Professional programmer (Python, NumPy, pandas, scikit-learn)
- Familiar with NLP tools (spaCy, NLTK, Hugging Face Transformers)
- Uses type-checked codebases (mypy, Pylance) for reproducibility
- Comfortable with streaming data processing (large datasets)
- Prefers programmatic APIs over CLI tools (integration with ML pipelines)

**Volume**:
- Dataset size: 1M-100M parallel sentence pairs
- TMX files: 100 MB - 10 GB (aggregated from multiple sources)
- Processing: One-time extraction + periodic updates
- Output: Cleaned parallel text files (TSV, JSON Lines) for MT training

## Requirements and Constraints

### Must-Have Requirements

1. **TMX Level 2 support**: Must extract structured inline markup (not just text)
   - Why: Inline tags contain linguistic information (named entities, formatting, placeholders) valuable for MT model training and linguistic analysis

2. **Large file handling**: Must process multi-gigabyte TMX files without out-of-memory crashes
   - Why: Public corpora (DGT-TM, OPUS) and industry datasets often exceed 1 GB

3. **Streaming API**: Must iterate over TUs without loading entire file into memory
   - Why: Limited GPU server RAM (8-16 GB shared with model training), batch processing many files

4. **Programmatic API**: Must integrate into Python data pipelines (pandas, Dask, PyTorch DataLoader)
   - Why: CLI tools inadequate for complex preprocessing (tokenization, filtering, augmentation)

5. **Structured data access**: Must access TU metadata (language, creation date, tuid) programmatically
   - Why: Filter by language pair, deduplicate by tuid, analyze translation patterns over time

6. **Type safety**: Must have type hints for IDE autocomplete and static type checking
   - Why: Reproducible research requires correct API usage, type errors caught before long experiments

### Constraints

- **Python version**: Research infrastructure typically Python 3.10+ (Conda, Docker), can adopt 3.12+ if needed
  - Academic clusters may lag (3.9-3.10), but Conda allows user-space upgrades

- **Licensing**: Must be permissive (MIT preferred) for publishing research code
  - GPL problematic if open-sourcing preprocessing pipelines (copyleft forces downstream GPL)

- **Dependencies**: Comfortable with C extensions (lxml) for performance
  - Research servers have compilers, Docker images pre-built with lxml

- **Platform**: Primarily Linux GPU servers
  - Windows/Mac compatibility unnecessary (research on HPC clusters, cloud GPUs)

- **Learning curve**: Willing to invest time learning complex APIs if performance/features justify
  - Research projects span months/years, upfront learning amortized over project lifetime

### Nice-to-Have Features

- Custom validation policies (skip malformed TUs instead of crashing, log warnings)
- Inline markup extraction as structured objects (separate text from tags for linguistic analysis)
- Parallel processing support (multi-process data loading for faster preprocessing)
- Integration with existing NLP tools (spaCy, tokenizers)
- Export to ML-friendly formats (Parquet, Arrow, HDF5)

### Anti-Requirements

- CAT tool compatibility (not importing into commercial translation software)
- Multi-format support beyond TMX (corpora typically TMX or plain text, not PO/XLIFF)
- CLI tools (prefer programmatic API for integration with ML pipelines)
- Production stability (can tolerate pre-1.0 API changes, research code not production)

## Current Workflow and Pain Points

### As-Is Workflow

1. **Corpus acquisition**: Download TMX corpora from OPUS, DGT-TM, commercial vendors
2. **Data loading**: Parse TMX into Python data structures
3. **Preprocessing**:
   - Extract source/target text pairs
   - Filter by language pair (e.g., en-de only)
   - Deduplicate by tuid or content hash
   - Tokenize with spaCy or Hugging Face tokenizers
   - Handle inline markup (strip or preserve for analysis)
4. **Export**: Write parallel text files (source.txt, target.txt) for MT training
5. **Training**: Feed into PyTorch DataLoader → Transformer model training

### Pain Points

1. **Inline markup loss**: Existing tools (lxml, BeautifulSoup) parse TMX as XML but lose TMX-specific structure
   - Need: TMX-aware parser that preserves inline tag semantics (bpt/ept pairing, nesting)

2. **Memory exhaustion**: Loading 5 GB TMX file into memory crashes on 16 GB GPU server
   - Need: Streaming API to iterate over TUs without loading entire file

3. **Type errors in pipelines**: Untyped TMX parsers cause runtime errors after hours of preprocessing
   - Need: Type-hinted API for static checking (mypy catches errors before experiments)

4. **No structured metadata access**: Parsing TMX with lxml requires manual XPath queries for tuid, creation date
   - Need: Pythonic API (dataclasses, properties) for accessing TU metadata

5. **Malformed TMX handling**: Public corpora contain errors (unclosed tags, invalid UTF-8), strict parsers crash
   - Need: Lenient parsing with configurable error handling (skip bad TUs, log warnings, continue)

6. **Manual inline tag extraction**: Need custom XPath/regex to extract tags separately from text for linguistic analysis
   - Need: Structured inline markup objects (separate `<bpt>`, `<ept>`, `<ph>` from text segments)

## Library Fitness Assessment

### hypomnema

**Fitness rating**: **Primary fit**

**Rationale**:
- **TMX Level 2 support**: Parses inline markup as structured objects (InlineElement, PlaceholderElement), enabling linguistic analysis of tags
- **Streaming API**: Processes multi-gigabyte files with constant ~50 MB RAM usage, critical for GPU servers
- **Type safety**: Full type hints (Python 3.12+), IDE autocomplete, mypy/Pylance static checking
- **Policy-driven validation**: Custom policies for error handling (skip malformed TUs, log warnings, continue parsing)
- **Programmatic API**: Dataclasses (TMX, TU, TUV) integrate cleanly with pandas, PyTorch DataLoader
- **MIT licensing**: Safe for open-sourcing research code, no GPL copyleft concerns
- **Python 3.12+ requirement**: Acceptable for research environments (Conda, Docker allow easy upgrade)

**Trade-offs**:
- **Pre-1.0 status**: API changes may require code updates between experiments
  - Mitigation: Pin version in requirements.txt, update only during paper revisions

- **Small community**: Limited third-party examples, slower issue resolution
  - Mitigation: Read source code (well-typed, readable), contribute fixes if needed

- **TMX-only**: No PO/XLIFF support
  - Non-issue: Research corpora primarily TMX, not multi-format

- **lxml dependency (optional)**: Faster with lxml, but can fall back to stdlib if needed
  - Impact: stdlib backend 10x slower, but acceptable for one-time corpus preprocessing

**Why it fits**: Designed for programmatic TMX processing with type safety, exactly matching research requirements (structured inline markup, streaming, type hints, MIT licensing).

### translate-toolkit

**Fitness rating**: **Acceptable fit for small corpora**

**Rationale**:
- **TMX Level 1 support**: Parses TMX, but inline markup preserved as unstructured text
- **Stable and mature**: 10+ years in production, rare breaking changes
- **Multi-format support**: Can process PO, XLIFF corpora if needed (beyond TMX)
- **Python 3.11 compatible**: Works on older research infrastructure

**Trade-offs**:
- **No streaming API**: Must load entire file into memory
  - Impact: Cannot process large corpora (>1 GB) without high-RAM servers

- **TMX Level 1 limitation**: Inline markup not structured
  - Impact: Manual XPath/regex required to extract tags separately from text

- **No type hints**: Runtime errors not caught until execution
  - Impact: Long preprocessing pipelines fail late, wasting compute time

- **GPL licensing**: Copyleft forces downstream GPL
  - Impact: Cannot open-source research preprocessing code under permissive license (MIT, Apache)

- **API design**: lxml-based, requires learning translate-toolkit's storage abstraction
  - Impact: Less Pythonic than dataclass-based APIs (hypomnema, pandas)

**Why it might fit**: If corpus small (<100 MB), Level 1 sufficient (text extraction only, no inline markup analysis), and GPL licensing acceptable, translate-toolkit's stability and multi-format support useful. Otherwise, hypomnema superior.

### polib

**Fitness rating**: **Not suitable**

**Rationale**:
- **No native TMX support**: Requires conversion via translate-toolkit
  - Impact: PO → TMX → extraction overhead, lossy conversion

- **PO-centric**: Designed for gettext workflows, not parallel corpus extraction
  - Impact: Misaligned with research needs (TMX corpora, not software localization)

- **No streaming API**: In-memory only
  - Impact: Cannot handle large corpora

- **No type hints**: Runtime errors not caught
  - Impact: Same as translate-toolkit (late failure in pipelines)

**Trade-offs**:
- **Zero dependencies**: Pure Python
  - Irrelevant: Research servers easily install lxml

- **MIT licensing**: Permissive
  - Irrelevant: polib not suitable for TMX corpus processing

**Why it doesn't fit**: Not designed for TMX research workflows, offers no advantages over hypomnema or translate-toolkit.

## Decision Criteria

### Use hypomnema if:
- TMX Level 2 required (structured inline markup extraction for linguistic analysis)
- Large corpora (>1 GB) common (streaming API critical)
- Type safety valued (reproducible research, static checking)
- MIT licensing required (open-sourcing preprocessing code)
- Python 3.12+ available (Conda, Docker allow easy adoption)
- Comfortable with pre-1.0 API instability (pin version, allocate update time)

### Use translate-toolkit if:
- Small corpora (<100 MB) only (no streaming needed)
- TMX Level 1 sufficient (text extraction, no inline markup analysis)
- Multi-format support valuable (PO, XLIFF corpora beyond TMX)
- GPL licensing acceptable (not open-sourcing code)
- Python 3.11 required (older research infrastructure, cannot upgrade)

### Avoid polib unless:
- Primary corpus format is PO (software localization datasets)
- TMX only needed for occasional conversions
- Even then, use translate-toolkit (po2tmx) instead

## Migration Considerations

### Migrating from lxml-Based Ad-Hoc Parsing

**Scenario**: Currently using lxml + manual XPath for TMX parsing

**With hypomnema**:
- Replace XPath queries with dataclass property access (`tu.tuvs[0].segments`)
- Add type hints to preprocessing pipeline (mypy catches errors before experiments)
- Use streaming API for large corpora (reduce RAM requirements 5-10x)
- Leverage structured inline markup (InlineElement objects) for tag analysis

**Benefits**:
- Type safety catches errors before long experiments (mypy integration)
- Streaming enables processing larger corpora without hardware upgrades
- Structured inline markup simplifies linguistic analysis (no XPath/regex)
- Cleaner code (dataclasses vs lxml ElementTree navigation)

**Costs**:
- Learning curve (new API, though well-typed and intuitive)
- Refactor existing preprocessing scripts (one-time effort)
- Python 3.12 upgrade (if not already on 3.12+)

### Compatibility with ML Pipelines

**Integration points**:
- **PyTorch DataLoader**: Streaming API feeds TUs directly into DataLoader
- **pandas DataFrame**: Convert TUs to pandas rows for filtering, deduplication
- **Hugging Face Datasets**: Stream TUs → write to JSON Lines → load with datasets.load_dataset
- **Dask**: Parallel processing of multiple TMX files via Dask Bag

**Example workflow pattern** (concept, not code):
1. Stream TMX with hypomnema (memory-efficient)
2. Extract source/target text + metadata (tuid, creation date)
3. Filter by language pair, deduplicate by tuid
4. Tokenize with Hugging Face tokenizers
5. Write to Parquet for efficient ML loading
6. Load Parquet into PyTorch DataLoader for training

**Data preservation**:
- Source/target text extracted losslessly
- Inline markup preserved as structured objects (analyze separately or strip)
- Metadata (tuid, language, date) retained for provenance tracking

## Recommended Workflow Patterns

### Pattern 1: Corpus Extraction with Streaming

**Scenario**: Extract en-de parallel text from 5 GB DGT-TM corpus

**Workflow**:
1. Use hypomnema streaming API to iterate over TUs
2. Filter by language pair (en source, de target)
3. Deduplicate by content hash (skip duplicate translations)
4. Write to TSV (source\ttarget\ttuid)
5. Load TSV into pandas for further preprocessing
6. Export to Hugging Face Datasets for MT training

**Benefits**: Constant RAM usage (~50 MB), processes 5 GB file on 8 GB server

### Pattern 2: Inline Markup Analysis

**Scenario**: Analyze named entity markup patterns in translation memories

**Workflow**:
1. Parse TMX with hypomnema (Level 2, structured inline markup)
2. Extract InlineElement objects separately from text segments
3. Classify tags by type (bpt/ept for paired tags, ph for placeholders)
4. Analyze tag distribution (frequency, nesting depth, alignment across languages)
5. Train NER model to predict tag positions in unmarked text

**Benefits**: Structured inline markup objects simplify tag extraction (no XPath/regex)

### Pattern 3: Reproducible Research Pipeline

**Scenario**: Publish paper with reproducible preprocessing code

**Workflow**:
1. Define preprocessing pipeline with type-hinted functions (mypy checked)
2. Use hypomnema for TMX parsing (MIT licensed, safe to open-source)
3. Pin hypomnema version in requirements.txt (reproducibility)
4. Document pipeline in Jupyter notebook with example corpus
5. Publish code on GitHub with citation instructions

**Benefits**: Type safety ensures correctness, MIT license enables open-sourcing, pinned version ensures reproducibility

## Alternative Considerations

### When Custom XML Parsing May Be Better

hypomnema ideal for TMX-specific processing, but custom lxml parsing may fit better if:
- **Non-standard TMX extensions**: Proprietary attributes/elements not in TMX spec
- **Hybrid XML formats**: Mixed TMX + custom namespace elements
- **Extreme performance optimization**: Hand-tuned lxml code for specific use case

In these cases, use lxml directly with custom parsing logic, sacrificing type safety and convenience for flexibility.

### When Plain Text Corpora Better

If inline markup not needed and TMX overhead problematic:
- **Plain text corpora**: Moses format (source.txt, target.txt) simpler for MT training
- **Tab-separated files**: Easier to process with pandas, Dask (no XML parsing overhead)
- **Parquet/Arrow**: Columnar formats faster to load for ML pipelines

Convert TMX → plain text once with hypomnema, then use plain text for experiments.

## Summary: NLP Researcher Recommendation

**Primary recommendation**: hypomnema

**Why**: TMX Level 2 (structured inline markup) enables linguistic analysis beyond text extraction, streaming API handles large corpora (multi-GB files) on memory-constrained GPU servers, type hints (Python 3.12+) ensure reproducible pipelines with static checking, MIT licensing safe for open-sourcing research code, programmatic API integrates cleanly with ML pipelines (PyTorch, pandas, Hugging Face).

**Secondary recommendation**: translate-toolkit for small corpora + multi-format needs

**Why**: If corpus <100 MB (no streaming needed), multi-format support valuable (PO, XLIFF beyond TMX), and GPL licensing acceptable, translate-toolkit's stability and comprehensiveness useful. However, lack of type hints and Level 1 limitation reduce value for research.

**Key requirement match**:
- ✅ TMX Level 2 support (structured inline markup for linguistic analysis)
- ✅ Large file handling (streaming API, constant RAM usage)
- ✅ Streaming API (iterate over TUs without loading entire file)
- ✅ Programmatic API (dataclasses integrate with pandas, PyTorch)
- ✅ Structured data access (TU metadata via dataclass properties)
- ✅ Type safety (full type hints, mypy/Pylance checking)

**When to avoid hypomnema**:
- Python 3.12+ unavailable AND infrastructure upgrade blocked (use translate-toolkit on Python 3.11)
- GPL licensing acceptable AND multi-format support needed (translate-toolkit handles PO, XLIFF)
- Pre-1.0 API instability unacceptable (use translate-toolkit for stability)

This persona prioritizes type safety and structured data access for reproducible research, streaming efficiency for large-scale corpora, and permissive licensing for open-sourcing preprocessing pipelines.
