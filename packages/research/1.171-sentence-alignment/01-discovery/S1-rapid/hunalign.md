# Hunalign

## What It Is
Hunalign is a fast, efficient sentence alignment tool based on the Gale-Church algorithm with dictionary support. It's widely used in the MT community for aligning parallel texts, particularly known for its speed and reliability.

**Origin**: Developed at MTA SZTAKI (Hungarian Academy of Sciences), open-source project

## Key Characteristics

### Algorithm Foundation
- **Gale-Church algorithm**: Statistical length-based alignment
- **Dictionary enhancement**: Optional bilingual dictionary improves accuracy
- **Sentence length correlation**: Exploits the tendency for parallel sentences to have similar lengths
- **Diagonal band search**: Reduces computational complexity

### Alignment Modes
1. **Dictionary mode**: Uses bilingual word pairs for better accuracy
2. **Length-based mode**: Pure statistical approach without dictionary
3. **Ladder mode**: Handles pre-aligned segments (anchor points)

## Speed

- **Very fast**: Can align millions of sentence pairs in minutes
- **Linear complexity**: O(n) with diagonal band constraint
- **Low memory footprint**: Suitable for large corpora
- **Typical throughput**: ~100K sentence pairs per minute on modern hardware

## Accuracy

### Benchmark Performance
- **F1 scores**: 85-95% on well-formed parallel corpora
- **Best results**: Clean web-crawled or official translation documents
- **Degradation**: Lower accuracy on noisy or loosely parallel texts
- **Dictionary impact**: +5-10% accuracy improvement with good dictionaries

**Tradeoff**: Prioritizes speed and robustness over maximum accuracy

## Ease of Use

### Installation
```bash
# From source
git clone https://github.com/danielvarga/hunalign
cd hunalign/src/hunalign
make

# Or use pre-built binaries
```

### Basic Usage
```bash
# With dictionary
./hunalign dict.txt source.txt target.txt > aligned.txt

# Without dictionary
./hunalign -realign source.txt target.txt > aligned.txt
```

### Input Format
- Plain text files with one sentence per line
- Optional pre-segmentation markers
- Dictionary format: source_word TAB target_word

## Maintenance

- **Status**: Stable, maintained
- **Community**: Well-established in MT research
- **Platform support**: Linux, macOS, Windows (with compilation)
- **Integration**: Used by Moses, Bitextor, and other MT pipelines

## Best For

- **Large-scale corpus alignment** where speed is critical
- **Web-crawled parallel data** from official sources
- **MT training data preparation**
- **Projects with existing bilingual dictionaries**
- **Production pipelines** requiring reliable, fast alignment

## Limitations

- Requires sentence-segmented input (doesn't handle raw text)
- Struggles with highly divergent translations or paraphrases
- Dictionary quality significantly affects results
- No deep semantic understanding (purely statistical)

## References

- [GitHub Repository](https://github.com/danielvarga/hunalign)
- [Original Paper](http://mokk.bme.hu/resources/hunalign/)
- [Gale-Church Algorithm](https://aclanthology.org/J93-1004/)
