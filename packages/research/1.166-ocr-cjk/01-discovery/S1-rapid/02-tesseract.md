# Tesseract OCR: CJK Capabilities

## What It Is

[Open-source OCR engine originally developed by HP, now maintained by Google](https://en.wikipedia.org/wiki/Tesseract_(software))

## CJK Capabilities

- [Version 3+ supports ideographic (Chinese & Japanese) and 116+ languages total](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html)
- [Trained data files for chi_sim, chi_tra, jpn, jpn_vert, kor](https://pyimagesearch.com/2020/08/03/tesseract-ocr-for-non-english-languages/)
- [Three model variants: tessdata_best (accuracy), tessdata (balanced), tessdata_fast](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html)

## Architecture

[LSTM-based OCR engine with language-specific configurations for fixed-pitch character segmentation](https://tesseract-ocr.github.io/docs/MOCRadaptingtesseract2.pdf)

## Strengths

- Widest language support (100+)
- Mature, established ecosystem
- Well-documented
- Active community

## Limitations

- Lower accuracy on CJK compared to PaddleOCR (87.74% vs 96.58% on invoice benchmark)
- Requires separate trained data files for each language
- Performance acceptable but not optimal for complex CJK documents
