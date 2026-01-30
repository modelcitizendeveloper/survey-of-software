# Overview: CJK OCR Fundamentals

## What is OCR for CJK Text?

OCR for CJK (Chinese, Japanese, Korean) text refers to specialized optical character recognition systems designed to handle the unique challenges of East Asian writing systems.

## Why CJK OCR is Different

CJK text recognition presents fundamentally different challenges compared to Latin alphabet OCR:

### Character Set Complexity
- **Scale**: Unicode defines [101,996 characters in the CJK Unified Ideographs set](https://en.wikipedia.org/wiki/CJK_Unified_Ideographs)
- **Classes**: [Large number of character classes creates high probability of confusions between similar character shapes](https://link.springer.com/rwe/10.1007/978-0-85729-859-1_14)
- **Monospacing**: [CJK characters are typically monospaced/fixed-pitch](https://tesseract-ocr.github.io/docs/MOCRadaptingtesseract2.pdf)

### Language-Specific Differences
- **Word boundaries**: [Chinese and Japanese don't use spaces between words, unlike Korean](https://github.com/TheJoeFin/Text-Grab/issues/191)
- **Mixed scripts**: Japanese uses Hiragana, Katakana, and Kanji in the same text
- **Vertical text**: Japanese often written vertically (top to bottom, right to left)

### Handwriting Challenges
- **Shape variations**: [Primary difficulty comes from writers' habits, styles, and times](https://pnclink.org/annual/annual2000/2000pdf/4-7-3.pdf)
- **Cursive strings**: Classical CJK text requires preprocessing from color filtering to segmentation
- **Seals and stamps**: Traditional documents include seals that must be distinguished from text

## When You Need CJK-Specific OCR

**Use CJK OCR when**:
- Processing documents in Chinese, Japanese, or Korean
- Handling mixed-script documents (e.g., Japanese with Kanji + Hiragana)
- Working with vertical text layouts (Japanese publications)
- Dealing with historical or classical CJK texts
- Processing forms with thousands of possible character classes

**General OCR is insufficient because**:
- Latin-focused OCR trained on 26-letter alphabets can't handle 100,000+ ideographs
- Word segmentation algorithms assume space-delimited words
- Character similarity detection needs CJK-specific training
- [Pattern training not supported for CJK in some commercial systems](https://support.abbyy.com/hc/en-us/articles/360003422379-Using-pattern-training-for-Chinese-Japanese-and-Korean-CJK-languages-in-FineReader-Engine)

## Key Insight

The fundamental challenge is scale and ambiguity: [CJK languages have large symbol sets and lack clear word boundaries, posing serious tests for classification engines designed for well-delimited words from small alphabets](https://tesseract-ocr.github.io/docs/MOCRadaptingtesseract2.pdf).
