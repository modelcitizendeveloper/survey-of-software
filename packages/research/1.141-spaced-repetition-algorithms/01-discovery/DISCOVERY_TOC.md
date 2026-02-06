# Discovery Research: Spaced Repetition Algorithms

**Experiment**: 1.141
**Date**: 2026-01-16
**Method**: Web search research
**Algorithms Researched**: SM-2, SM-18, FSRS

---

## Research Queries Executed

### SM-2 Algorithm Research
**Query**: "SM-2 algorithm spaced repetition SuperMemo implementation 2026"

**Key Sources**:
- [GitHub - thyagoluciano/sm2](https://github.com/thyagoluciano/sm2)
- [SuperMemo - Wikipedia](https://en.wikipedia.org/wiki/SuperMemo)
- [SATHEE: SM-2 Algorithm](https://sathee.iitk.ac.in/pyqs/spaced-repetition/algorithms/sm2-algorithm/)
- [supermemo2 · PyPI](https://pypi.org/project/supermemo2/)
- [SuperMemo method](https://www.supermemo.com/en/supermemo-method)
- [What spaced repetition algorithm does Anki use?](https://faqs.ankiweb.net/what-spaced-repetition-algorithm)
- [SM-2 Algorithm Explained](https://tegaru.app/en/blog/sm2-algorithm-explained)
- [SuperMemo 2: Algorithm](https://super-memory.com/english/ol/sm2.htm)

**Key Findings**:
- SM-2 is a simple spaced repetition algorithm calculating review intervals based on recall ease
- Tracks 3 properties: repetition number (n), easiness factor (EF, starts at 2.5), interval (I) in days
- E-Factors vary between 1.1 (most difficult) and 2.5 (easiest)
- Most popular SRS algorithm: used (modified) in Anki, Mnemosyne
- Anki 23.10+ offers two algorithms: SM-2 based and FSRS
- Reduces study time by 50-70% vs traditional methods
- **Limitations**: Hardcoded 1-day and 6-day first intervals, doesn't account for individual differences

---

### SM-18 Algorithm Research
**Query**: "SM-18 algorithm SuperMemo spaced repetition latest version 2026"

**Key Sources**:
- [SuperMemo Algorithm](https://help.supermemo.org/wiki/SuperMemo_Algorithm)
- [Algorithm SM-17](https://supermemo.guru/wiki/Algorithm_SM-17)
- [Algorithm SM-18](https://supermemo.guru/wiki/Algorithm_SM-18)
- [Universal metric for cross-comparison](https://supermemo.guru/wiki/Universal_metric_for_cross-comparison_of_spaced_repetition_algorithms)
- [First fast-converging SRS algorithm: SM-5](https://supermemo.guru/wiki/First_fast-converging_spaced_repetition_algorithm:_Algorithm_SM-5)

**Key Findings**:
- **SM-18** is the newest SuperMemo algorithm (released 2019)
- Used in SuperMemo 18 (as of May 2019)
- **Main improvement**: New model for estimating item difficulty (departure from assumption that difficulty is constant)
- Improves approximation of stabilization function
- **Key innovation**: Accounts for dramatic changes in item difficulty during learning (explained by anchoring - new mnemonic context converts difficult → easy overnight)
- **Predecessor**: SM-17 (2016) introduced two-component model of memory
- **No SM-19/SM-20 publicly released as of 2026** (though October 2025 benchmarks claim SM-20 exists)

---

### FSRS Algorithm Research
**Query**: "FSRS free spaced repetition scheduler algorithm Anki 2026"

**Key Sources**:
- [GitHub - fsrs4anki](https://github.com/open-spaced-repetition/fsrs4anki)
- [How to use FSRS on Anki](https://forums.ankiweb.net/t/how-to-use-the-next-generation-spaced-repetition-algorithm-fsrs-on-anki/25415)
- [The Algorithm](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)
- [FSRS Helper](https://ankiweb.net/shared/info/759844606)
- [GitHub - free-spaced-repetition-scheduler](https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler)
- [ABC of FSRS](https://github.com/open-spaced-repetition/fsrs4anki/wiki/abc-of-fsrs)
- [Open Spaced Repetition](https://github.com/open-spaced-repetition)
- [FSRS - RemNote Help](https://help.remnote.com/en/articles/9124137-the-fsrs-spaced-repetition-algorithm)

**Key Findings**:
- FSRS = Free Spaced Repetition Scheduler
- Developed by Jarrett Ye (MaiMemo Inc research engineer)
- Based on DSR model (Difficulty, Stability, Retrievability)
- Memory state represented by Stability (S) and Difficulty (D)
- **Performance**: 20-30% fewer reviews than SM-2 for same retention level
- Allows targeting specific retention percentage
- **Integration**: Built into Anki 23.10+ (toggle in Deck Options → Advanced/FSRS section)
- **Training data**: Created in 2023 using ML trained on 700M reviews from 20K users
- **Current benchmark**: ~1.7B reviews from 20K Anki users
- Open-source, actively maintained by Open Spaced Repetition community

---

### Algorithm Comparison Research
**Query**: "SM-2 SM-18 FSRS comparison spaced repetition algorithms 2026"

**Key Sources**:
- [FSRS - RemNote Help](https://help.remnote.com/en/articles/9124137-the-fsrs-spaced-repetition-algorithm)
- [Comparing Spaced Repetition Algorithms - Brainscape](https://www.brainscape.com/academy/comparing-spaced-repetition-algorithms/)
- [What algorithm does Anki use?](https://faqs.ankiweb.net/what-spaced-repetition-algorithm)
- [Benchmark of SRS Algorithms](https://expertium.github.io/Benchmark.html)
- [FSRS Algorithm: Next-Gen](https://www.quizcat.ai/blog/fsrs-algorithm-next-gen-spaced-repetition)
- [ABC of FSRS](https://github.com/open-spaced-repetition/fsrs4anki/wiki/abc-of-fsrs)
- [Anki - Wikipedia](https://en.wikipedia.org/wiki/Anki_(software))
- [FSRS vs SM2 live comparison discussion](https://forums.ankiweb.net/t/has-anyone-done-a-live-comparison-of-fsrs-and-sm2-as-implemented-in-anki-it-looks-like-no-so-can-anyone-help-me-set-it-up/34996)
- [SuperMemo dethroned by FSRS](https://supermemopedia.com/wiki/SuperMemo_dethroned_by_FSRS)

**Key Findings**:
- **FSRS vs SM-17**: Preliminary tests show roughly on par
- **SM-18**: Proprietary, requires licensing (not available for open-source apps like Anki)
- **FSRS advantages over SM-2**: 20-30% fewer reviews, learns user memory patterns, customizable retention targets
- **FSRS complexity**: More difficult to understand than SM-2, less customizable, but more accurate
- **Recent performance (2025)**:
  - LECTOR: 90.2%
  - FSRS: 89.6%
  - SSP-MMC: 88.4%
  - ANKI (SM-2): 60.5%
  - SM-2: 47.1%
- **October 2025 claim**: SM-20 "reached perfection," beating FSRS 20:0.04 in universal metric (but SM-20 not publicly available)

---

### Python Libraries Research
**Query**: "spaced repetition Python libraries implementation SM-2 FSRS Anki 2026"

**Key Sources**:
- [GitHub - anki-sm-2](https://github.com/open-spaced-repetition/anki-sm-2)
- [Open Spaced Repetition GitHub](https://github.com/open-spaced-repetition)
- [Anki SM-2 - RemNote Help](https://help.remnote.com/en/articles/6026144-the-anki-sm-2-spaced-repetition-algorithm)
- [ABC of FSRS](https://github.com/open-spaced-repetition/fsrs4anki/wiki/abc-of-fsrs)
- [spaced-repetition-algorithm GitHub Topics](https://github.com/topics/spaced-repetition-algorithm)
- [GitHub - sm-2](https://github.com/open-spaced-repetition/sm-2)

**Key Findings**:
- **anki-sm-2**: Python package implementing Anki's SM-2-based algorithm (available on PyPI)
- **sm-2**: Another Python implementation from open-spaced-repetition org
- **fsrs-rs-python**: Python bindings for fsrs-rs (reduces size from 2GB to 6MB)
- **py-fsrs**: Python implementation with optimization
- **Open Spaced Repetition org**: Maintains all implementations, active development in 2026

---

### Adoption & Migration Research
**Query**: "Anki FSRS adoption statistics user migration SuperMemo 2026"

**Key Sources**:
- [ABC of FSRS](https://github.com/open-spaced-repetition/fsrs4anki/wiki/abc-of-fsrs)
- [Understanding the New Anki FSRS Algorithm](https://gist.ly/youtube-summarizer/understanding-the-new-anki-fsrs-algorithm-a-comprehensive-guide)
- [FSRS vs SM-2 Guide - MemoForge](https://memoforge.app/blog/fsrs-vs-sm2-anki-algorithm-guide-2025/)
- [Spaced Repetition Systems Have Gotten Way Better](https://domenic.me/fsrs/)
- [SuperMemo dethroned by FSRS](https://supermemopedia.com/wiki/SuperMemo_dethroned_by_FSRS)
- [The History of FSRS for Anki](https://www.lesswrong.com/posts/G7fpGCi8r7nCKXsQk/the-history-of-fsrs-for-anki)
- [srs-benchmark](https://github.com/open-spaced-repetition/srs-benchmark)

**Key Findings**:
- **Timeline**: FSRS integrated into Anki 23.10 (2023), mainstream adoption by 2025
- **Training**: Created in 2023 using ML on 700M reviews from 20K users
- **Current dataset**: ~1.7B reviews from 20K Anki users
- **Medical student reports**: 20-30% fewer daily reviews while maintaining retention
- **Simulation data**: 20-30% review reduction at 90% retention rate
- **Migration**: 1-5 minutes depending on deck size, preserves review history, can switch back to SM-2
- **SuperMemo API**: Expected to become available in 2026
- **SM-20 claim (October 2025)**: Reportedly beat FSRS 20:0.04, but not publicly available

---

### Market Size Research
**Query**: "spaced repetition market size language learning apps SRS 2026"

**Key Sources**:
- [Best Language Learning Apps with SRS 2025](https://www.taalhammer.com/best-language-learning-apps-with-spaced-repetition-srs-and-ai-in-2025-taalhammer-vs-11-other-apps/)
- [The Guide to Effective SRS Language Learning](https://www.fluentu.com/blog/learn/srs-spaced-repetition-language-learning/)
- [Master Language Learning with Spaced Repetition](https://migaku.com/blog/language-fun/spaced-repetition-language-learning)
- [Spaced Repetition Software Market Research Report 2033](https://dataintelo.com/report/spaced-repetition-software-market)
- [SRS in Language Learning - Taalhammer](https://www.taalhammer.com/spaced-repetition-in-language-learning/)
- [Flashcard App Market Size 2035](https://www.wiseguyreports.com/reports/flashcard-app-market)

**Key Findings**:
- **SRS Market Size (2024)**: USD $1.23 billion
- **Flashcard App Market (2035 projection)**: USD $4 billion
- **CAGR**: 6.3% (2025-2035)
- **Education segment (2024)**: $900M
- **Growth Drivers**:
  - Personalized/adaptive learning demand
  - Scientifically validated memory recall optimization
  - Expansion beyond education: healthcare, language learning, exam prep, professional certification
  - Smartphone adoption
  - Post-pandemic e-learning surge

---

## Summary of Key Insights

### Algorithm Positioning
1. **SM-2**: Classic, simple, widely adopted (Anki, Mnemosyne), 50-70% time reduction vs traditional methods
2. **SM-18**: Latest SuperMemo version (2019), proprietary, accounts for changing item difficulty, superior to SM-2
3. **FSRS**: Modern ML-based (2023), open-source, 20-30% better than SM-2, integrated into Anki 23.10+

### Performance Hierarchy (2025 Benchmarks)
1. **SM-20** (claimed): 20:0.04 vs FSRS (not publicly available)
2. **LECTOR**: 90.2%
3. **FSRS**: 89.6%
4. **SSP-MMC**: 88.4%
5. **Anki SM-2**: 60.5%
6. **SM-2**: 47.1%

### Market Dynamics
- **SRS Market**: $1.23B (2024), growing 6.3% CAGR
- **Flashcard Apps**: Projected $4B by 2035
- **Adoption**: FSRS integrated into Anki (millions of users), mainstream by 2025
- **Open-source dominance**: Anki can only use freely available algorithms (excludes SM-18)

### Strategic Trends
- **SuperMemo**: Proprietary (SM-18), licensing required, superior but inaccessible for open-source
- **FSRS**: Open-source, ML-driven, rapidly adopted, backed by academic research
- **Python ecosystem**: Active development via open-spaced-repetition GitHub org
- **User migration**: Medical students leading FSRS adoption (20-30% review reduction)

---

## Research Gaps & Future Work

### Not Covered in This Research
- Detailed mathematical formulas for each algorithm
- Code examples and implementation complexity
- Integration complexity with existing systems
- Cost modeling for SRS app development
- Longitudinal retention studies beyond benchmarks
- SM-18 vs FSRS head-to-head comparison (not possible: SM-18 proprietary)

### Recommended Follow-Up
1. Hands-on implementation with SM-2 and FSRS Python libraries
2. Performance testing on representative datasets
3. Integration testing with language learning applications
4. Cost analysis for developing SRS-based products
5. User experience comparison (SM-2 vs FSRS migration)

---

**Research Duration**: ~2 hours
**Primary Method**: Web search with official docs + academic benchmarks
**Confidence Level**: High for algorithm descriptions and FSRS performance, Medium for SM-18/SM-20 (proprietary, limited public info)
