# Prior Art: Library Embeddings & Code-as-Language

**Question:** To what extent has treating code as language for building vectors been done before?

**Answer:** Extensively in academia and industry, but mostly focused on **code semantics** rather than **library ecosystems**. Our approach occupies a specific niche.

---

## 🎓 Academic Research Areas

### 1. Code Embeddings (Semantic Code Representations)

**code2vec (2018)**
- **Paper:** "code2vec: Learning Distributed Representations of Code" (Alon et al., POPL 2019)
- **Approach:** AST paths → embeddings, predicts method names
- **Focus:** Code **semantics** (what code does), not library relationships
- **Different from ours:** They embed code snippets; we embed library names

**CodeBERT (2020)**
- **Paper:** "CodeBERT: A Pre-Trained Model for Programming and Natural Languages" (Microsoft Research)
- **Approach:** BERT-style transformer on code + docstrings
- **Focus:** Code understanding, generation, search
- **Different from ours:** Token-level embeddings; we do library-level

**GraphCodeBERT (2021)**
- **Extension:** Adds data flow graphs to CodeBERT
- **Still focused:** Code semantics, not library ecosystems

### 2. API/Library Recommendation Systems

**API2Vec (2018)**
- **Paper:** "API2Vec: Learning Representations of API Sequences" (Nguyen et al.)
- **Approach:** Sequence of API calls → embeddings
- **Focus:** Which **methods** to call within a library
- **Different from ours:** Intra-library API usage; we do inter-library relationships

**LibRec (2016)** ⭐ **Closest to our work**
- **Paper:** "Recommending Software Libraries based on Collaborative Filtering" (Thung et al., MSR 2016)
- **Approach:** Collaborative filtering on GitHub repo dependencies
- **Focus:** "Users who imported X also imported Y"
- **Similar to ours:** Co-occurrence based!
- **Different from ours:** Binary (uses/doesn't use), prescriptive recommendations, declared dependencies only

**REPERTOIRE (2021)**
- **Paper:** "REPERTOIRE: Automated Feature Recommendation for Third-Party Libraries" (IEEE TSE)
- **Approach:** Mines StackOverflow + GitHub for library feature usage
- **Focus:** Which **features** of a library to use
- **Different from ours:** Feature-level, not library-level relationships

### 3. Dependency Network Analysis

**Libraries.io Research (2017-present)**
- **Paper:** "The Evolution of Software Ecosystems" (Decan et al., EMSE 2017)
- **Data:** Dependency graphs of 5M+ packages across 32 ecosystems
- **Approach:** Network analysis (PageRank, centrality, vulnerability propagation)
- **Focus:** Dependency **structure**, not embeddings
- **Complementary to ours:** We could use their dependency data as training signal

**npm Ecosystem Studies (2019)**
- **Paper:** "Breaking the Package Manager Monopoly" (Zerouali et al., MSR 2019)
- **Approach:** Analyze npm dependency networks for security, updates
- **Different from ours:** Network topology, not embeddings

---

## 🏢 Industry Tools

### GitHub Copilot / CodeWhisperer
- **Approach:** LLM trained on massive code corpus
- **Embeddings:** Yes, but at token/subword level (not library level)
- **Focus:** Code completion, generation
- **Different from ours:** Black box, no explicit library embeddings exposed

### Sourcegraph Code Intelligence
- **Approach:** Static analysis + search over code graph
- **Focus:** Code navigation, references, definitions
- **Different from ours:** Graph-based, not embedding-based

### Snyk / Dependabot (Dependency Analysis)
- **Approach:** Dependency graph + vulnerability database
- **Focus:** Security, not library relationships/similarity
- **Different from ours:** Security-focused, not exploratory

---

## 📊 What's Been Done vs What We're Doing

| Aspect | Prior Work | Our Approach |
|--------|-----------|--------------|
| **Unit of analysis** | Code tokens, AST nodes, API calls | **Library names** |
| **Training data** | Code repositories, API sequences | **Research topics + import co-occurrence** |
| **Goal** | Code understanding, completion, search | **Library discovery, ecosystem mapping** |
| **Output** | Predict next token/API call | **Library analogies, similarity, clustering** |
| **Granularity** | Fine (token/method level) | **Coarse (library level)** |
| **Use case** | Code generation, bug finding | **Library selection, tech stack planning** |

---

## 🎯 Our Unique Contribution

### What Makes Our Approach Different

**1. Library-level, not code-level**
- We don't care what numpy **does** (code2vec's domain)
- We care what numpy is **used with** (ecosystem relationships)

**2. Dual signal: Research + Codebase**
- **Research signal:** Curated library comparisons (high quality, low volume)
- **Codebase signal:** Real import patterns (high volume, noisy)
- **Novel:** Combining expert analysis with usage data

**3. Exploratory, not prescriptive**
- Not predicting "you should use X" (recommendation systems)
- Revealing "X is similar to Y" (exploratory analysis)
- Enables developer-driven discovery

**4. Methodologically transparent**
- Research methodology published (4PS framework)
- Sampling strategy documented
- Reproducible (unlike black-box LLMs)

### The Niche We Fill

**Existing tools answer:**
- "What does this code do?" (code2vec, CodeBERT)
- "What API should I call next?" (API2Vec, Copilot)
- "Is this library vulnerable?" (Snyk, Dependabot)
- "Which library is most popular?" (GitHub stars, npm trends)

**We answer:**
- "What's the **async equivalent** of requests?" (httpx, via analogies)
- "Which libraries **cluster** with torch?" (ML ecosystem discovery)
- "What are **pragmatic alternatives** to pandas?" (polars, by similarity)
- "How do libraries **relate functionally**?" (not just dependency chains)

---

## 📚 Closest Prior Work

### LibRec (2016) - Most Similar

**What they did:**
- Collaborative filtering on GitHub repo dependencies
- "Repos using X also use Y" → recommend Y
- Evaluated on 50K GitHub repos

**How we differ:**
- **They:** Dependency declarations (package.json, requirements.txt)
- **Us:** Actual imports in code (AST parsing) + research co-occurrence
- **They:** Recommendation (prescriptive)
- **Us:** Embeddings (exploratory)
- **They:** Binary (uses/doesn't use)
- **Us:** Vector space (degrees of similarity, analogies)

### Libraries.io - Complementary Data Source

**What they provide:**
- Pre-built dependency graphs for 5M+ packages
- Network metrics (PageRank, centrality)
- Historical evolution data

**How we could use it:**
- Add as third signal (research + codebase + dependencies)
- Validate our embeddings against their network structure
- Cross-ecosystem comparisons (Python vs JavaScript vs Rust)

---

## 🔬 Validation Strategy

### Compare to LibRec (2016) Baseline
1. Replicate their collaborative filtering approach
2. Compare their recommendations vs our nearest neighbors
3. Quantify: Do embeddings capture more nuance than binary co-occurrence?

### Validate Against Libraries.io
1. Download PyPI dependency graph
2. Compare our embeddings to their network centrality
3. Question: Do libraries with similar embeddings have similar dependency patterns?

### Intrinsic Evaluation
- **Analogy accuracy:** flask→fastapi, requests→httpx
- **Cluster coherence:** Do ML libraries cluster together?
- **Nearest neighbor quality:** Manual inspection of top-10 similar libraries

### Extrinsic Evaluation (User Study)
- Can developers find better libraries using our embeddings?
- Show developers library clusters, measure usefulness
- Compare: embeddings vs GitHub stars vs dependency counts

---

## 📖 Summary: State of the Field

**Code embeddings:** Mature (code2vec, CodeBERT)
**API embeddings:** Emerging (API2Vec, REPERTOIRE)
**Dependency analysis:** Mature (Libraries.io, academic MSR work)
**Library recommendation:** Some work (LibRec), mostly graph-based
**Library embeddings (our approach):** **Gap in literature**

**Our contribution:**
- First to combine research curation + codebase usage
- Library-level embeddings (not code-level or API-level)
- Exploratory tool (not recommendation system)
- Methodologically transparent (unlike LLM black boxes)

**Publication-worthy?** Yes, especially if we:
1. Validate against Libraries.io data
2. Compare to LibRec baseline
3. Run user study showing utility
4. Extend to multiple ecosystems (Python + JavaScript + Rust)

---

## 🔗 Key References

1. **Alon et al. (2019)** - code2vec: Learning Distributed Representations of Code
   https://arxiv.org/abs/1803.09473

2. **Thung et al. (2016)** - Recommending Software Libraries via Collaborative Filtering (LibRec)
   https://dl.acm.org/doi/10.1145/2901739.2901776

3. **Decan et al. (2017)** - Evolution of Software Ecosystems (Libraries.io)
   https://link.springer.com/article/10.1007/s10664-017-9589-y

4. **Nguyen et al. (2018)** - API2Vec: Learning Representations of API Sequences
   https://arxiv.org/abs/1809.10324

5. **Feng et al. (2020)** - CodeBERT: A Pre-Trained Model for Programming and Natural Languages
   https://arxiv.org/abs/2002.08155

**Data sources:**
- Libraries.io: https://libraries.io/data
- Software Heritage: https://archive.softwareheritage.org/
- GitHub Search API: https://docs.github.com/en/rest/search

---

**Bottom line:** Library-level embeddings combining research + usage data is **novel**. We're filling the gap between code embeddings (too fine-grained) and dependency analysis (too structural).
