# Tesseract LSTM Architecture

## Overview

[Tesseract Version 4 employs Long Short-Term Memory (LSTM), a form of Recurrent Neural Network (RNN)](https://nanonets.com/blog/ocr-with-tesseract/). [This neural network-based recognition engine delivers significantly higher accuracy than previous versions](https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-lstm).

## How It Works

[The input image is processed in boxes (rectangles) line by line, feeding into the LSTM model](https://www.researchgate.net/figure/Fig6Internal-Architecture-of-OCR-Tesseract-8-Version-4-has-a-dataset-knowledge-of_fig3_341779791). [Tesseract 4 focuses on line recognition](https://learnopencv.com/deep-learning-based-text-recognition-ocr-using-tesseract-and-opencv/).

## Architecture Components

[To recognize a single character, CNNs are typically used. For arbitrary-length text (sequences of characters), RNNs are used, with LSTM being a popular form](https://nanonets.com/blog/ocr-with-tesseract/).

[The network specification string describes the architecture](https://groups.google.com/g/tesseract-ocr/c/ZuXSyBDvPhk/m/vcZWc8FjAAAJ). Example: `[1,36,0,1Ct3,3,16Mp3,3Lfys64Lfx96Lrx96Lfx512O1c1]` includes:
- **Ct3,3,16**: 3x3 convolution with 16 filters
- **Mp3,3**: Max pooling layers
- **Lfys64, Lfx96, Lrx96, Lfx512**: LSTM layers in different dimensions

## CJK-Specific Configurations

[For CJK languages, page segmentation mode (--psm) settings are important](https://tesseract-ocr.github.io/tessdoc/tess5/TrainingTesseract-5.html). [The .traineddata files include script-specific configurations, including vertical text detection in jpn_vert.traineddata](https://deepwiki.com/tesseract-ocr/tessdata/6-developer-guide).

## Training Data

[For Latin languages, models trained on ~400,000 textlines spanning ~4,500 fonts](https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-lstm). [For other scripts, fewer fonts available but similar number of textlines](https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-lstm).
