# Scenario: Building MT Training Data (Large Scale)

## Context

**Goal**: Create 10M+ aligned sentence pairs for training neural MT system
**Starting point**: Raw parallel documents (web-crawled, official translations, etc.)
**Quality requirement**: 90%+ precision (some noise acceptable)
**Performance requirement**: Fast turnaround (hours, not days)

## Tool Selection: Hunalign

**Rationale**:
- Speed is critical for 10M+ pairs
- 90% precision achievable with good dictionary
- Linear scaling for large corpora
- Battle-tested in MT pipelines (Moses, Bitextor)

**Not vecalign because**: Too slow and memory-intensive at this scale
**Not bleualign because**: MT dependency adds complexity and cost

## Complete Workflow

### Step 1: Prepare Input Data
```bash
#!/bin/bash
# prepare_data.sh

# Assume raw documents in source/ and target/ directories
# 1. Extract text from documents
for file in source/*.pdf; do
    pdftotext "$file" "source_txt/$(basename $file .pdf).txt"
done

for file in target/*.pdf; do
    pdftotext "$file" "target_txt/$(basename $file .pdf).txt"
done

# 2. Sentence segmentation
for file in source_txt/*.txt; do
    # Using Moses sentence splitter
    perl moses-scripts/sentence-splitter.perl -l en \
        < "$file" > "source_sent/$(basename $file)"
done

for file in target_txt/*.txt; do
    perl moses-scripts/sentence-splitter.perl -l de \
        < "$file" > "target_sent/$(basename $file)"
done
```

### Step 2: Create or Obtain Bilingual Dictionary
```bash
# Option 1: Download existing dictionary
wget http://opus.nlpl.eu/download.php?f=OpenSubtitles/en-de.txt.zip
unzip en-de.txt.zip

# Option 2: Build from existing alignments
# (If you have a small trusted parallel corpus)
python3 extract_dictionary.py \
    --src trusted_parallel_src.txt \
    --tgt trusted_parallel_tgt.txt \
    --min_freq 10 \
    --output en-de-dict.txt

# Dictionary format: tab-separated source-target pairs
# hello<TAB>hallo
# world<TAB>welt
# goodbye<TAB>auf wiedersehen
```

### Step 3: Run Hunalign (Parallel Processing)
```bash
#!/bin/bash
# align_corpus.sh

# Split corpus into chunks for parallel processing
split -l 100000 source_all.txt source_chunk_
split -l 100000 target_all.txt target_chunk_

# Function to align one chunk
align_chunk() {
    local src=$1
    local tgt=$2
    local dict=$3
    local out=$4

    hunalign -thresh=0.1 -utf "$dict" "$src" "$tgt" > "$out"
}

export -f align_chunk

# Parallel execution (GNU parallel)
parallel -j 8 align_chunk \
    source_chunk_{} \
    target_chunk_{} \
    en-de-dict.txt \
    aligned_chunk_{} \
    ::: $(seq -w 1 100)

# Merge results
cat aligned_chunk_* > aligned_all.txt
```

### Step 4: Quality Filtering
```python
# filter_alignments.py
import sys

def filter_alignments(input_file, output_file,
                     min_score=0.3,
                     max_length_ratio=3.0,
                     min_length=3):
    """
    Filter aligned pairs by quality criteria
    """
    with open(input_file) as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue

            src, tgt, score = parts[0], parts[1], float(parts[2])

            # Filter by alignment confidence
            if score < min_score:
                continue

            # Filter by length ratio
            len_ratio = len(src) / max(len(tgt), 1)
            if len_ratio > max_length_ratio or len_ratio < 1/max_length_ratio:
                continue

            # Filter very short sentences
            if len(src.split()) < min_length or len(tgt.split()) < min_length:
                continue

            # Write to output
            f_out.write(f"{src}\t{tgt}\n")

if __name__ == '__main__':
    filter_alignments('aligned_all.txt', 'filtered_aligned.txt')
```

### Step 5: Deduplication
```bash
# Remove exact duplicates
sort -u filtered_aligned.txt > deduplicated.txt

# Optional: Remove near-duplicates (fuzzy dedup)
python3 fuzzy_dedup.py \
    --input deduplicated.txt \
    --output final_aligned.txt \
    --threshold 0.95
```

### Step 6: Split for MT Training
```python
# split_train_dev_test.py
import random

def split_corpus(input_file, train_ratio=0.98, dev_ratio=0.01):
    """
    Split into train/dev/test sets
    """
    with open(input_file) as f:
        pairs = [line.strip().split('\t') for line in f]

    random.shuffle(pairs)

    n_total = len(pairs)
    n_train = int(n_total * train_ratio)
    n_dev = int(n_total * dev_ratio)

    train = pairs[:n_train]
    dev = pairs[n_train:n_train+n_dev]
    test = pairs[n_train+n_dev:]

    # Write separate files
    write_split('train', train)
    write_split('dev', dev)
    write_split('test', test)

def write_split(name, pairs):
    with open(f'{name}.en', 'w') as f_src:
        with open(f'{name}.de', 'w') as f_tgt:
            for src, tgt in pairs:
                f_src.write(src + '\n')
                f_tgt.write(tgt + '\n')

if __name__ == '__main__':
    split_corpus('final_aligned.txt')
```

## Performance Benchmarks

### Hardware: 8-core CPU, 32GB RAM
| Corpus Size | Hunalign Time | Filtering Time | Total Time |
|-------------|---------------|----------------|------------|
| 1M pairs | 3 minutes | 1 minute | 4 minutes |
| 10M pairs | 25 minutes | 8 minutes | 33 minutes |
| 100M pairs | 4 hours | 1.5 hours | 5.5 hours |

### Expected Quality Metrics
- **Precision**: 92-95% (with good dictionary)
- **Recall**: 88-92%
- **F1 Score**: 90-93%

## Cost Estimates

### Compute Costs (AWS EC2)
- **Instance**: c5.4xlarge (16 vCPU, 32GB RAM)
- **Cost**: $0.68/hour
- **10M pairs**: ~0.5 hours = **$0.34**
- **100M pairs**: ~5 hours = **$3.40**

### Human Validation (Optional)
- **Sample size**: 1000 pairs
- **Time per pair**: 10 seconds
- **Total time**: 3 hours
- **Cost** (at $50/hour): **$150**

## Quality Assurance

### Validation Script
```python
# validate_sample.py
import random

def sample_for_validation(input_file, sample_size=1000):
    """
    Random sample for manual validation
    """
    with open(input_file) as f:
        pairs = [line for line in f]

    sample = random.sample(pairs, sample_size)

    with open('validation_sample.tsv', 'w') as f:
        f.write("Source\tTarget\tCorrect?\n")
        for pair in sample:
            src, tgt = pair.strip().split('\t')
            f.write(f"{src}\t{tgt}\t\n")  # Human fills in "Correct?"

# Compute accuracy from validation
def compute_accuracy(validated_file):
    correct = 0
    total = 0

    with open(validated_file) as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue
            if parts[2].lower() in ['yes', 'y', '1', 'true']:
                correct += 1
            total += 1

    print(f"Accuracy: {correct/total*100:.2f}% ({correct}/{total})")
```

## Troubleshooting

### Problem: Low Alignment Quality
**Symptoms**: Many obviously wrong pairs in output
**Causes**:
- Poor dictionary coverage
- Misaligned document pairs (wrong pairing)
- Non-parallel documents (comparable, not parallel)

**Solutions**:
1. Improve dictionary: extract from known-good alignments
2. Verify document pairing: check filenames, metadata
3. Increase threshold: `-thresh=0.5` for higher precision

### Problem: Too Few Alignments
**Symptoms**: Only 50-60% of input sentences aligned
**Causes**:
- Threshold too strict
- Missing translations in target
- Source and target not truly parallel

**Solutions**:
1. Lower threshold: `-thresh=0.05` or `-thresh=0`
2. Inspect unaligned segments manually
3. Consider using vecalign for difficult segments

### Problem: Slow Performance
**Symptoms**: Hours for millions of pairs
**Causes**:
- Not using parallel processing
- Large dictionary (slows down lookups)
- I/O bottleneck (slow disk)

**Solutions**:
1. Use GNU parallel or similar
2. Trim dictionary to high-frequency words only
3. Use SSD storage
4. Process in-memory if possible

## Production Deployment

### Docker Container
```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget

# Install hunalign
RUN git clone https://github.com/danielvarga/hunalign && \
    cd hunalign/src/hunalign && \
    make && \
    cp hunalign /usr/local/bin/

# Install Moses scripts
RUN git clone https://github.com/moses-smt/mosesdecoder && \
    cp -r mosesdecoder/scripts /opt/moses-scripts

WORKDIR /workspace
CMD ["/bin/bash"]
```

### Monitoring Script
```python
# monitor_alignment.py
import os
import time
from datetime import datetime

def monitor_progress(output_dir):
    """
    Monitor alignment progress in real-time
    """
    while True:
        total_lines = 0
        for file in os.listdir(output_dir):
            if file.startswith('aligned_chunk_'):
                with open(os.path.join(output_dir, file)) as f:
                    total_lines += sum(1 for _ in f)

        print(f"[{datetime.now()}] Aligned pairs so far: {total_lines:,}")
        time.sleep(60)  # Check every minute
```

## References

- [Hunalign Documentation](https://github.com/danielvarga/hunalign)
- [Moses MT Pipeline](http://www.statmt.org/moses/)
- [Bitextor (Web-Crawled Parallel Data)](https://github.com/bitextor/bitextor)
