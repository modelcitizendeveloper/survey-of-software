# TM Alignment: Creating TMX from Existing Translations

## What is Alignment?

**Problem:** You have source documents and translated documents, but no translation memory.

**Solution:** Alignment tools match corresponding sentences between source and target to create TMX files.

## Key Alignment Tools

### LF Aligner

**Platform:** Cross-platform (Windows, Linux, macOS)
**License:** Free and open source

**Features:**
- Automatic sentence pairing (uses Hunalign algorithm)
- Input formats: TXT, DOC, DOCX, RTF, PDF, HTML
- Output formats: TMX, tab-delimited TXT, XLS

**Download:** [LF Aligner on SourceForge](https://sourceforge.net/projects/aligner/)

**Use Case:** Non-technical users needing GUI tool for occasional alignment

### bitext2tmx

**Platform:** Java (cross-platform)
**License:** Free and open source

**Features:**
- Command-line and GUI interfaces
- Align plain text files
- Generate TMX format output
- Works on Linux, macOS X, Solaris, Windows

**Download:** [bitext2tmx on SourceForge](https://sourceforge.net/projects/bitext2tmx/)

**Use Case:** Batch processing multiple file pairs, automation scripts

### TMPotter

**Platform:** Cross-platform (Java-based)
**License:** Open source

**Features:**
- Accepts text files (source + translation)
- Accepts PO catalog files
- Accepts TMX/XLIFF input
- Produces TMX output

**Repository:** [TMPotter on GitHub](https://github.com/miurahr/tmpotter)

**Use Case:** Developers familiar with Java, PO file workflows

### YouAlign (Cloud-Based)

**Platform:** Web-based
**License:** Commercial (free tier available)

**Website:** [YouAlign](https://youalign.com/)

**Features:**
- No installation required
- Upload documents, get TMX output
- Supports multiple formats

**Use Case:** Quick one-off alignments without local setup

## Alignment Process

### 1. Prepare Source Files

**Requirements:**
- Same content structure (paragraph breaks in same locations)
- Same formatting (avoid mixing formats like PDF and DOCX)
- Clean text (no headers/footers that differ between files)

**Best Practices:**
- Convert to plain text or simple format
- Remove page numbers, headers, footers
- Ensure 1:1 correspondence (no added/removed paragraphs)

### 2. Run Alignment

**LF Aligner Example:**
1. Launch LF Aligner GUI
2. Load source file (File > Open Source Document)
3. Load target file (File > Open Translation Document)
4. Set source and target languages
5. Click "Align" button
6. Review suggested alignments
7. Manually adjust incorrect pairings
8. Export to TMX (File > Export > TMX)

**bitext2tmx Command Line:**
```bash
java -jar bitext2tmx.jar -s source.txt -t target.txt -o output.tmx
```

### 3. Review and Clean

**Common Issues:**
- Misaligned sentences (merge/split corrections needed)
- Headers mistakenly aligned with body text
- Empty segments
- Duplicate entries

**Manual Review:**
- Check first/last 10 segments
- Spot-check random samples
- Look for obviously wrong translations

### 4. Import into CAT Tool

Load TMX into OmegaT, MemoQ, Trados, etc.

## Alignment Algorithms

**Hunalign (used by LF Aligner):**
- Statistical alignment based on sentence length correlation
- Uses dictionaries (if available) to improve accuracy
- Open-source C++ implementation

**Length-Based:**
- Simple approach: match sentences by character count ratio
- Works well for similar languages (English/French)
- Less accurate for dissimilar languages (English/Japanese)

**Dictionary-Assisted:**
- Uses bilingual dictionary to identify corresponding words
- Improves accuracy
- Requires dictionary resources

## Automation Workflow

### Batch Process Multiple Documents

```python
import subprocess
import os

# Directory containing source-target pairs
source_dir = "sources/"
target_dir = "targets/"
output_dir = "tmx/"

# Get all source files
source_files = os.listdir(source_dir)

for source_file in source_files:
    source_path = os.path.join(source_dir, source_file)
    target_path = os.path.join(target_dir, source_file)  # Assumes same filename
    output_path = os.path.join(output_dir, source_file.replace(".txt", ".tmx"))

    # Run bitext2tmx
    subprocess.run([
        "java", "-jar", "bitext2tmx.jar",
        "-s", source_path,
        "-t", target_path,
        "-o", output_path
    ])

print("Alignment complete!")
```

### Merge Aligned TMX Files

After aligning multiple document pairs, merge into single TM:

```python
from pythontmx import TmxFile

master_tm = TmxFile(source_lang="en-US")

for tmx_file in ["doc1.tmx", "doc2.tmx", "doc3.tmx"]:
    tm = TmxFile.read(tmx_file)
    for tu in tm.body.translation_units:
        master_tm.body.add_translation_unit(tu)

# Deduplicate before saving
master_tm.write("master.tmx")
```

## Best Practices

1. **Start Small:** Test alignment on a few pages before processing full documents
2. **Review Output:** Always manually review at least a sample of alignments
3. **Clean Input:** Remove extraneous content (page numbers, headers) before alignment
4. **Use Dictionaries:** If available, provide bilingual dictionaries to alignment tools
5. **Version Control:** Keep original source/target files and alignment output in git

## Sources

- [LF Aligner download | SourceForge.net](https://sourceforge.net/projects/aligner/)
- [bitext2tmx: Bitext Aligner/Converter](https://bitext2tmx.sourceforge.net/)
- [bitext2tmx CAT bitext aligner/converter download | SourceForge.net](https://sourceforge.net/projects/bitext2tmx/)
- [YouAlign](https://youalign.com/)
- [New Tool! Bitext Aligner | BasicCAT](https://www.basiccat.org/new-tool-bitext-aligner/)
- [GitHub - TMPotter](https://github.com/miurahr/tmpotter)
- [Linux for Translators: Alignment tools](https://www.linuxfortranslators.org/align.html)
