# Use Case: Bioinformatics (DNA Sequence Analysis)

## Who

**Persona**: Computational biologist or bioinformatics researcher
**Examples**: Genome alignment, motif finding, RNA-seq analysis
**Scale**: Human genome = 3 billion base pairs, datasets = terabytes

## Why (Requirements)

### Functional Requirements
- **Sequence search**: Find gene sequences in genomes
- **Motif discovery**: Identify conserved patterns (e.g., TATA box)
- **Approximate matching**: Allow mismatches, insertions, deletions
- **Multiple sequences**: Compare many sequences against reference
- **Position reporting**: Need exact locations of matches

### Non-Functional Requirements
- **High accuracy**: False negatives can miss genes
- **Scalability**: Process billions of base pairs
- **Reproducibility**: Results must be consistent (for publication)
- **Citations**: Use established tools (for peer review)

## Constraints Analysis

### Pattern Characteristics
- **Small alphabet**: DNA = 4 chars (A, C, G, T), Protein = 20 amino acids
- **Variable length**: Motifs = 5-50 bp, genes = 100-10,000 bp
- **Ambiguity codes**: N = any nucleotide, R = purine (A or G)
- **Approximate matching**: Allow k% mismatches (sequencing errors)

### Text (Genome) Characteristics
- **Very long**: Human genome = 3×10⁹ bp
- **Structured**: Genes, introns, exons, regulatory regions
- **Repetitive**: Transposons, tandem repeats (up to 45% of genome)
- **Static**: Reference genome doesn't change (can preprocess)

### Performance Constraints
- **Throughput**: Process GB-TB of sequencing data
- **Memory**: Desktop-friendly (8-64 GB RAM typical)
- **Batch processing**: Not real-time (hours-days OK)
- **Accuracy > Speed**: Missing a gene worse than slow search

## Solution: Specialized Algorithms (Not General String Matching)

### Primary Recommendation: Domain-Specific Tools

**Why NOT General Algorithms**:
- Standard string matching doesn't handle mismatches/gaps
- Small alphabet (σ=4) makes Boyer-Moore less effective
- Genome size makes brute force infeasible
- Specialized tools 100-1000x faster than naive approach

### For Different Use Cases

#### 1. Exact Short Sequence Search (50-500 bp)

**Tool**: KMP or Aho-Corasick
**When**: Find exact matches (primers, known sequences)
**Library**:
- Python: biopython (uses KMP internally)
- C++: SeqAn library

**Example**: Find primer sequences in PCR design

#### 2. Read Alignment (NGS: Map Millions of Short Reads)

**Tool**: BWA, Bowtie2, STAR
**Algorithm**: Burrows-Wheeler Transform (BWT) + FM-index
**Why**: Preprocess genome once, map millions of reads efficiently

**Complexity**:
- Preprocessing: O(n) to build BWT index (one-time, hours)
- Query: O(m) per read (m = read length, ~100-300 bp)
- **Key**: Index genome, not reads (genome static, reads change)

**Example**: RNA-seq analysis (map reads to transcriptome)

#### 3. Homology Search (Find Similar Sequences)

**Tool**: BLAST (Basic Local Alignment Search Tool)
**Algorithm**: Seed-and-extend with heuristics
**Why**: Finds similar sequences (not just exact), biologically relevant

**How it works**:
1. **Seed**: Find short exact matches (k-mers, k=11 typical)
2. **Extend**: Use dynamic programming to extend matches
3. **Score**: Use substitution matrix (BLOSUM, PAM)

**Complexity**: Heuristic, much faster than optimal alignment

**Example**: Find homologous genes across species

#### 4. Motif Finding (De Novo Discovery)

**Tool**: MEME, Gibbs sampler, EM algorithms
**Algorithm**: Statistical, not string matching
**Why**: Don't know pattern beforehand (discover it from data)

**Approach**: Find over-represented sequences (motifs)

**Example**: Discover transcription factor binding sites

### Why Small Alphabet Matters

**DNA (σ=4)** vs **English (σ=26)**:

**Boyer-Moore bad-character rule**:
- English: Mismatch 'Z' in pattern "ABC" → Skip 3 positions
- DNA: Mismatch 'A' in "ACG" → 'A' likely in pattern → Skip 1-2 positions

**Result**: BM less effective for DNA (small skips)

**KMP advantage**:
- Linear time guaranteed
- No dependence on alphabet size
- Failure function works well with DNA repetition

## Detailed Solution: Bowtie2 (NGS Alignment)

### Architecture

**Preprocessing (Build Index)**:
```
Reference Genome (FASTA)
  ↓
Burrows-Wheeler Transform
  ↓
FM-Index (compressed suffix array)
  ↓
Save to disk (~4 GB for human genome)
```

**Time**: ~4 hours (one-time)

**Matching (Align Reads)**:
```
Read (FASTQ)
  ↓
Query FM-Index (exact + mismatches)
  ↓
Score alignment (allow gaps)
  ↓
Report best match(es)
```

**Throughput**: ~1M reads/minute (100 bp reads)

### Why BWT/FM-Index

**Advantages**:
- **Compressed**: Human genome index ~4 GB (vs 12 GB uncompressed)
- **Fast queries**: O(m) per read (linear in read length)
- **Handles mismatches**: Backtracking in index

**Trade-off**: Complex preprocessing, but worth it for millions of queries

## Alternatives

### If Need Exact Matches Only

**Problem**: BLAST too slow for exact search
**Solution**: Aho-Corasick or KMP
- Build AC trie for all query sequences
- Scan genome once
- Much faster than BLAST for exact matches

**Library**: biopython with custom KMP

### If Need Approximate (k Mismatches)

**Problem**: Need to allow sequencing errors
**Solution**:
- **Bitap algorithm** (agrep): k mismatches in O(nm) with bitwise parallelism
- **TRE library**: Approximate regex
- **BLAST**: Heuristic but fast

**For k≤2**: Bitap feasible
**For k>2**: BLAST or local alignment (dynamic programming)

### If Genome Changes (Not Static)

**Problem**: BWT index assumes static genome
**Solution**: Online algorithms (KMP, AC)
- Can't preprocess text
- Linear scan still feasible for smaller genomes (bacteria: ~5 Mbp)

## Performance Expectations

### Exact Search (KMP/AC)

**Task**: Find 100 patterns in human genome (3 Gbp)
**Time**: ~30 seconds (AC single pass)
**Memory**: ~100 MB (trie for 100 patterns)

### Read Alignment (Bowtie2)

**Task**: Align 50M reads (150 bp each) to human genome
**Time**: ~1 hour (8 cores)
**Memory**: ~8 GB (genome index + buffers)

### BLAST

**Task**: Find homologs for 1 gene across 1000 genomes
**Time**: ~10 minutes (heuristic, approximate)
**Database**: Pre-built BLAST database required

## Real-World Examples

### BWA (Burrows-Wheeler Aligner)

**Use**: Map NGS reads to reference genome
**Algorithm**: BWT + FM-index
**Performance**: ~1M reads/min (paired-end)
**Memory**: ~4 GB (human genome)

### Bowtie2

**Use**: Fast read alignment (RNA-seq, ChIP-seq)
**Algorithm**: FM-index with optimizations
**Performance**: ~10M reads/hour (single thread)
**Feature**: Handles paired-end, allows gaps

### BLAST

**Use**: Sequence homology search (find similar sequences)
**Algorithm**: Seed-and-extend heuristic
**Performance**: ~1 second per query (vs nr database)
**Database**: NCBI maintains curated BLAST databases

### BLAT (BLAST-Like Alignment Tool)

**Use**: Fast alignment for similar sequences (>95% identity)
**Algorithm**: Index queries, scan genome
**Performance**: 1000x faster than BLAST for near-exact
**Use case**: Align mRNA to genome (same species)

## Common Pitfalls

### 1. Using General String Matching

**Problem**: KMP on 3 Gbp genome takes hours, can't handle mismatches
**Solution**: Use specialized tools (BWT, BLAST)

### 2. Ignoring Biological Context

**Problem**: Finding motif "ATG" everywhere (start codon)
**Solution**: Filter by context (reading frames, ORFs)

### 3. Not Handling Ambiguity

**Problem**: Pattern "ATCG", genome has "ANCG" (N = any base)
**Solution**: Use IUPAC ambiguity codes, tools that support them

### 4. Memory Exhaustion

**Problem**: Loading full genome into RAM (12 GB)
**Solution**: Use compressed index (BWT: ~4 GB) or streaming

### 5. Ignoring Strand Direction

**Problem**: DNA is double-stranded (forward + reverse complement)
**Solution**: Search both strands, tools handle automatically

## Key Takeaways

**Don't use general string matching**:
- Small alphabet (σ=4) reduces BM advantage
- Need approximate matching (k mismatches)
- Genome size (billions of bp) requires specialized approaches

**Use domain-specific tools**:
- **Exact short patterns**: Aho-Corasick or biopython
- **NGS alignment**: Bowtie2, BWA (BWT-based)
- **Homology search**: BLAST (seed-and-extend)
- **Motif discovery**: MEME, statistical methods

**Index the genome, not the queries**:
- Genome is static (preprocess once)
- Millions of reads/queries (need fast lookup)
- BWT/FM-index: O(n) build, O(m) query

**Accuracy > Speed**:
- False negative = missed gene (unacceptable)
- Slow search = wait longer (acceptable)
- Use established tools (citations, reproducibility)

**Alphabet size matters**:
- DNA (σ=4): KMP competitive with BM
- Protein (σ=20): BM slightly better but not huge advantage
