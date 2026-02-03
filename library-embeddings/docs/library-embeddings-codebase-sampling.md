# Codebase Sampling Methodology for Library Embeddings

**Goal:** Extract co-import patterns from real Python codebases to enhance library embeddings with pragmatic usage data.

**Challenge:** GitHub has millions of Python repositories. We need a sampling strategy that is:
- **Representative** - Captures diverse usage patterns across domains
- **Unbiased** - Avoids skewing toward popular/trending repos
- **Ethical** - Respects privacy, uses only public code
- **Scalable** - Feasible to process with available compute

---

## Sampling Strategy Options

### Option 1: Stratified Random Sampling by Domain

**Approach:**
- Manually curate domain categories (web, data-science, ML, devtools, etc.)
- For each domain, identify seed repos (well-known exemplars)
- Sample N repos per domain that depend on those seed libraries
- Extract import patterns from sampled repos

**Pros:**
- Ensures domain diversity
- Prevents ML repos from dominating (they're 40% of GitHub Python)
- Interpretable: "We sampled X web apps, Y ML projects, Z data pipelines"

**Cons:**
- Manual curation of domains (labor intensive)
- Risk of researcher bias in domain definitions
- Misses emerging/cross-domain usage patterns

**Sample size:** 50-100 repos per domain × 10 domains = 500-1000 repos

---

### Option 2: Library-Centric Sampling

**Approach:**
- For each library in our vocabulary (97 libraries), find repos that import it
- Sample K repos per library (stratified by library popularity)
- Weight less-popular libraries higher to avoid numpy/pandas dominance

**Pros:**
- Directly tied to our embedding vocabulary
- Ensures coverage of niche libraries
- Can weight samples inversely to library popularity (counter-bias)

**Cons:**
- Popular libraries (numpy) appear in 1M+ repos - need smart subsampling
- Doesn't capture co-import patterns for libraries not in our vocab

**Sample size:** 10-50 repos per library × 97 libraries = 1000-5000 repos

---

### Option 3: Temporal Sampling (Time-Stratified)

**Approach:**
- Sample repos created in different time periods (2015, 2017, 2019, 2021, 2023, 2025)
- Captures evolution of library ecosystems over time
- Equal repos per time period

**Pros:**
- Captures how library usage patterns change
- Can identify deprecated libraries vs emerging ones
- Temporal validity for embeddings training

**Cons:**
- Old repos may use outdated practices (not representative of current usage)
- Requires more data to maintain per-period sample size
- May miss domain diversity within time periods

**Sample size:** 100-200 repos per year × 6 years = 600-1200 repos

---

### Option 4: GitHub Search API with Multi-Stage Filtering

**Approach:**
1. **Stage 1:** Query GitHub Search API for Python repos
   - Filter: `language:Python stars:10..1000 size:>100`
   - Rationale: 10+ stars = some usage, &lt;1000 stars = not mega-popular
   - size:&gt;100KB = non-trivial codebase
2. **Stage 2:** Random sample 2000 repos from results
3. **Stage 3:** Clone + parse imports from all `.py` files
4. **Stage 4:** Filter to repos using ≥3 libraries from our vocabulary

**Pros:**
- Reproducible (GitHub API queries are deterministic)
- Avoids mega-popular repos (reduces numpy/pandas dominance)
- Lower bound on stars ensures quality code
- Scales well with API rate limits

**Cons:**
- Star count is popularity bias (just less extreme)
- Repos with 10-1000 stars may still skew toward certain domains
- API rate limits (5000 requests/hour for authenticated)

**Sample size:** 2000 repos queried → ~500-1000 repos with sufficient library usage

---

## Recommended Approach: Hybrid Stratified + Library-Centric

Combine Option 1 and Option 2 for best balance:

### Step 1: Define Domains (Manual Curation)

Use PyPI Trove classifiers as starting point:
- **Web Development** (Django, Flask, FastAPI ecosystems)
- **Data Science** (Pandas, NumPy, Matplotlib)
- **Machine Learning** (PyTorch, TensorFlow, scikit-learn)
- **DevOps/Infrastructure** (Ansible, Kubernetes clients, monitoring)
- **NLP** (spaCy, NLTK, Transformers)
- **Scientific Computing** (SciPy, SymPy, BioPython)
- **Testing/QA** (pytest, unittest, coverage tools)
- **CLI Tools** (Click, Typer, argparse-based)
- **Data Engineering** (Airflow, Spark, dask)
- **Security/Crypto** (cryptography, jwt, oauth)

### Step 2: Library-Centric Sampling Within Domains

For each domain:
1. Identify 3-5 anchor libraries (e.g., Web → fastapi, flask, django)
2. Query GitHub: `language:Python import:anchor_library stars:10..500`
3. Sample 30-50 repos per domain
4. Extract imports from all `.py` files

### Step 3: Bias Correction

- **Popularity weighting:** Over-sample repos using rare libraries (inverse frequency)
- **Temporal filter:** Only repos updated in last 2 years (current practices)
- **Size filter:** 100KB - 10MB (excludes toy projects and monoliths)

### Step 4: Data Extraction

Use Python AST parser (not regex):
```python
import ast

def extract_imports(file_path):
    with open(file_path) as f:
        tree = ast.parse(f.read())

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports
```

**Why AST over regex:**
- Handles multi-line imports
- Ignores commented-out imports
- Parses `from x import y` correctly
- Syntactically valid (fails on broken code, which we skip)

---

## Privacy & Ethics

### What's Allowed
✅ Public repos with open-source licenses (MIT, Apache, GPL)
✅ Extracting import statements (factual metadata, not copyrightable)
✅ Aggregate statistics (co-occurrence counts)
✅ Publishing embeddings derived from aggregates

### What's NOT Allowed
❌ Private repos or repos without explicit licenses
❌ Copying/republishing source code
❌ Using repo names or author identities in published data
❌ Proprietary/internal codebases (even if accidentally public)

### License Filtering

Only sample repos with OSI-approved licenses:
- Check `LICENSE` file or GitHub API `license` field
- Skip repos without clear licensing
- Document license distribution in methodology

---

## Scale & Compute

### Target Sample Size
**500-1000 repositories** across 10 domains

**Rationale:**
- Small enough to process in &lt;1 day on single machine
- Large enough to capture domain diversity
- Comparable to academic studies (e.g., PROMISE dataset, StackOverflow survey)

### Processing Time Estimates

Assuming 500 repos:
- Clone repos: ~10 sec/repo × 500 = **83 minutes**
- Parse imports: ~2 sec/repo × 500 = **17 minutes**
- Build co-occurrence matrix: **&lt;1 minute**
- **Total: ~2 hours** (parallelizable)

### Storage

- 500 repos × 5MB average = **2.5GB** disk space
- Extracted import data: **&lt;1MB** (just library names + counts)
- Can delete repos after extraction (keep only metadata)

---

## Validation

After sampling, validate representativeness:

### 1. Domain Coverage Check
```
Web:      50 repos (10%)
ML:       80 repos (16%)
Data Sci: 70 repos (14%)
...
(Should be roughly balanced, no domain >25%)
```

### 2. Library Coverage Check
```
97 libraries in vocabulary
→ How many appear in sampled repos?
→ Target: 80%+ coverage
```

### 3. Popularity Distribution
```
Plot stars distribution of sampled repos
→ Should be roughly uniform in 10-500 range
→ Not exponential (which would indicate popularity bias)
```

### 4. Temporal Distribution
```
Check last-updated dates
→ 80%+ repos updated in last 2 years
→ Avoid deprecated codebases
```

---

## Comparison: Metadata-Only vs Metadata+Codebase

| Signal | Metadata-Only (Current) | + Codebase Sampling |
|--------|------------------------|---------------------|
| **Functional similarity** | ✅ Tags, categories | ✅ Same |
| **Research co-occurrence** | ✅ Survey topics | ✅ Same |
| **Pragmatic co-use** | ❌ Missing | ✅ Real import patterns |
| **Substitutability** | ⚠️ Inferred | ✅ Direct observation |
| **Dependencies** | ❌ Missing | ✅ Explicit in code |
| **Data volume** | 75 "sentences" | 500-1000 "sentences" |
| **Data quality** | High (curated) | Medium (noisy) |

**Expected impact:** Embeddings will better capture how libraries are **actually used together** vs how they're **theoretically similar**.

---

## Example: What Changes?

### Before (Metadata-Only)
```
numpy → pandas, matplotlib, scipy (research co-occurrence)
```

### After (+ Codebase)
```
numpy → pandas, matplotlib, scipy, pytest, logging, argparse
         ↑                              ↑
    (research co-occurrence)    (pragmatic co-use in real code)
```

Real codebases will reveal:
- **Testing patterns:** Libraries often imported with pytest, unittest
- **Logging patterns:** Logger setup alongside main libs
- **CLI patterns:** argparse/click with domain libs
- **Async patterns:** asyncio co-imported with aiohttp, httpx

These patterns are invisible in research metadata but crucial for developers choosing libraries.

---

## Proposed Workflow

### Phase 1: Sampling (Week 1)
1. Define 10 domain categories
2. Identify anchor libraries per domain
3. Query GitHub API (stratified sampling)
4. Validate sample (coverage, diversity checks)

### Phase 2: Extraction (Week 1-2)
1. Clone repos (shallow clone, 1 commit depth)
2. Parse all `.py` files with AST
3. Extract import statements
4. Build co-occurrence matrix
5. Delete repos (keep only metadata + imports)

### Phase 3: Integration (Week 2)
1. Merge codebase co-occurrence with research co-occurrence
2. Re-train embeddings (metadata + codebase as dual signals)
3. Compare old vs new embeddings (nearest neighbors, analogies)
4. Document methodology + publish

### Phase 4: Publication (Week 3)
1. Write methodology paper (reproducibility focus)
2. Publish embeddings + code on GitHub
3. Add visualization to SoS homepage

**Total timeline:** 3-4 weeks for full pipeline

---

## Alternative: Use Existing Datasets

Instead of sampling ourselves, use existing curated datasets:

### Option A: Libraries.io Dependency Data
- **Source:** https://libraries.io/data
- **Data:** Dependency graphs for 5M+ packages across ecosystems
- **Pros:** Pre-curated, massive scale, includes PyPI dependencies
- **Cons:** Only shows declared dependencies, not actual imports in code

### Option B: Software Heritage Archive
- **Source:** https://archive.softwareheritage.org/
- **Data:** 250M+ repositories archived
- **Pros:** Massive scale, diverse sources (not just GitHub)
- **Cons:** No API for "sample N Python repos", must process entire dataset

### Option C: WorldOfCode (WoC)
- **Source:** http://worldofcode.org/
- **Data:** Git commit data from 200M+ repos
- **Pros:** Pre-indexed, supports queries like "repos importing X"
- **Cons:** Access requires academic affiliation, complex data format

**Recommendation:** Start with GitHub API sampling (Option 4 hybrid), then augment with Libraries.io for dependency data if needed.

---

## Open Questions for User

1. **Scale preference:** 500 repos (fast proof-of-concept) or 2000+ repos (comprehensive)?
2. **Domain balance:** Equal repos per domain, or weight by domain size?
3. **Temporal focus:** Only recent repos (2023-2025) or include historical (2015+)?
4. **Dependencies:** Include PyPI declared dependencies, or only parsed imports?
5. **Publication:** Publish sampled repo list (for reproducibility) or keep anonymous?

---

## Next Steps

If this methodology looks good:
1. Create beads for Phase 1-4 (sampling, extraction, integration, publication)
2. Start with Phase 1: Define domains + build GitHub query script
3. Run pilot on 50 repos to validate extraction pipeline
4. Scale to full 500-1000 repo sample

**Estimated effort:** 20-30 hours of agent work over 3-4 weeks (parallelizable across phases)
