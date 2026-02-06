# Use Case: Content Migration Tool

**Scenario:** One-time migration of 10 million legacy documents (Simplified Chinese) to Traditional Chinese for Taiwan market entry. Must complete within 48 hours.

---

## Requirements

### Must-Have (Deal-Breakers)

1. **High Throughput** - Process >100 documents/second (avg 10KB each)
2. **Batch Processing** - Handle millions of files efficiently
3. **Accuracy** - >95% correct conversion (Taiwan vocabulary)
4. **Headless Operation** - Run as background job (no human intervention)
5. **Error Handling** - Log failures, continue processing

### Nice-to-Have (Preferences)

6. **Low Cost** - Minimize cloud compute spend
7. **Resume Support** - Restart from checkpoint if interrupted
8. **Progress Tracking** - Know completion ETA
9. **Parallel Processing** - Multi-core utilization
10. **Simple Deployment** - Docker one-liner

### Constraints

- **Timeline:** 48 hours to completion
- **Budget:** <$100 total compute cost (one-time)
- **Infrastructure:** AWS EC2 (any instance type)
- **Data:** 10M files × 10KB = 100 GB total text

---

## Library Evaluation

### OpenCC

#### Must-Haves
- ✅ **Throughput:** 3.4M chars/sec = ~340 docs/sec (10KB each) → **Meets**
- ✅ **Batch processing:** Efficient for large-scale
- ✅ **Accuracy:** s2tw handles Taiwan vocabulary correctly
- ✅ **Headless:** Command-line tool available
- ✅ **Error handling:** Python exception handling works

#### Nice-to-Haves (7/10 points)
- ⚠️ **Cost:** Medium (see calculation below)
- ✅ **Resume support:** Easy to implement with checkpoint files
- ✅ **Progress tracking:** Simple to add with tqdm
- ✅ **Parallel:** Python multiprocessing works
- ✅ **Deployment:** Docker image straightforward

**Calculation:**
- 100 GB ÷ 3.4 MB/s = ~8 hours on single core
- 8 vCPU: ~1 hour total
- c5.2xlarge (8 vCPU): $0.34/hour × 1 hour = **$0.34**

**Fit Score:** **97/100** (60 must-haves + 37 nice-to-haves)

---

### zhconv-rs

#### Must-Haves
- ✅ **Throughput:** 100-200 MB/sec = ~10,000-20,000 docs/sec → **Exceeds**
- ✅ **Batch processing:** Rust efficiency excellent
- ✅ **Accuracy:** zh-tw handles Taiwan vocabulary correctly
- ✅ **Headless:** CLI tool available
- ✅ **Error handling:** Rust Result type for safety

#### Nice-to-Haves (8/10 points)
- ✅ **Cost:** Very low (see calculation below)
- ✅ **Resume support:** Easy to implement
- ✅ **Progress tracking:** Rust libraries available
- ✅ **Parallel:** Rayon for easy parallelism
- ⚠️ **Deployment:** Requires Rust binary build (slightly harder)

**Calculation:**
- 100 GB ÷ 150 MB/s = ~11 minutes on single core
- 8 vCPU: ~2 minutes total (with parallel processing)
- c5.2xlarge: $0.34/hour × 0.05 hour = **$0.02**

**Fit Score:** **98/100** (60 must-haves + 38 nice-to-haves)

---

### HanziConv

#### Must-Haves
- ❌ **Throughput:** 0.5 MB/sec = ~50 docs/sec → **20 hours on 8 cores** (fails 48hr deadline)
- ⚠️ **Batch processing:** Python overhead limits efficiency
- ❌ **Accuracy:** No Taiwan vocabulary (軟件 not 軟體)
- ✅ **Headless:** Python script works
- ✅ **Error handling:** Basic Python exceptions

#### Nice-to-Haves (3/10 points)
- ❌ **Cost:** High due to long runtime
- ✅ **Resume support:** Easy to implement
- ✅ **Progress tracking:** tqdm works
- ⚠️ **Parallel:** GIL limits Python multiprocessing
- ✅ **Deployment:** Simplest (pure Python)

**Calculation:**
- 100 GB ÷ 0.5 MB/s = ~56 hours on single core
- 8 vCPU (limited by GIL): ~20 hours actual
- c5.2xlarge: $0.34/hour × 20 hours = **$6.80**

**Fit Score:** **13/100** (10 must-haves (partial) + 3 nice-to-haves)

**Eliminated:** Can't meet 48-hour deadline + wrong vocabulary for Taiwan.

---

## Recommendation

### Winner: **zhconv-rs**

**Rationale:**
1. **30x faster than OpenCC** (100-200 MB/s vs 3-7 MB/s)
2. **Completes in 2 minutes vs 1 hour** (96% time savings)
3. **17x cheaper** ($0.02 vs $0.34 compute cost)
4. **Same accuracy** (Taiwan vocabulary correct)

**Why speed matters here:**
- Faster completion = less business risk (can retry if issues found)
- Lower cost = can afford to over-provision for safety margin
- One-time migration = maturity less critical than throughput

**Trade-off Accepted:**
- zhconv-rs is less mature than OpenCC, BUT...
- For batch migration (not ongoing production), risk is manageable
- Can validate output on sample before full run

### Implementation Script

```python
# batch_migrate.py
from zhconv import convert
from pathlib import Path
import multiprocessing as mp
from tqdm import tqdm

def convert_file(input_path):
    """Convert single file to Taiwan Traditional"""
    try:
        text = input_path.read_text(encoding='utf-8')
        converted = convert(text, 'zh-tw')
        output_path = Path('output') / input_path.name
        output_path.write_text(converted, encoding='utf-8')
        return True
    except Exception as e:
        with open('errors.log', 'a') as f:
            f.write(f"{input_path}: {e}\n")
        return False

def main():
    input_files = list(Path('input').glob('*.txt'))

    # Parallel processing (8 workers for 8 vCPU)
    with mp.Pool(8) as pool:
        results = list(tqdm(
            pool.imap(convert_file, input_files),
            total=len(input_files)
        ))

    success_count = sum(results)
    print(f"Converted {success_count}/{len(input_files)} files")

if __name__ == '__main__':
    main()
```

### Execution Plan

```bash
# Build Docker image
docker build -t migrate-zh .

# Run migration on EC2
docker run -v $(pwd)/data:/data migrate-zh \
  python batch_migrate.py

# Est. completion: 2 minutes (10M files, 8 vCPU)
# Est. cost: $0.02 (c5.2xlarge spot pricing)
```

---

## Alternative: OpenCC for Safety

If you're **risk-averse** and the 48-hour deadline has buffer:

**Use OpenCC instead:**
- More proven for large-scale (Wikipedia uses it)
- Still completes in 1 hour (well under 48hr deadline)
- Only $0.32 more expensive ($0.34 vs $0.02)

**Decision Matrix:**
- **Aggressive (maximize speed/cost):** zhconv-rs
- **Conservative (maximize reliability):** OpenCC

For a one-time migration where speed saves 59 minutes and $0.32, **zhconv-rs is the optimal choice** unless organizational policy mandates proven libraries only.

---

**Use Case Winner:** **zhconv-rs** (98/100 fit, 30x faster)

**Conservative Alternative:** OpenCC (97/100 fit, still meets deadline)
