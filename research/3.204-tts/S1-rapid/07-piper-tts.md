# Piper TTS

**Category**: Open Source TTS
**Tier**: Self-hosted, local inference
**Status**: Active development, production-ready
**Last Updated**: November 2025

---

## Overview

Piper is a **fast, lightweight** open-source TTS system optimized for edge devices like Raspberry Pi 4. Built with ONNX models trained on VITS, it prioritizes **speed and low resource requirements** over voice cloning capabilities.

## Key Features

### Performance & Efficiency
- **Extremely fast**: 10× faster than Coqui TTS
- **Low resource requirements**: Runs on Raspberry Pi 4
- **Real-time streaming**: Streams audio directly to speakers
- **Offline operation**: No internet required
- **Small model sizes**: 5-50MB per voice (vs 100s of MB for Coqui)

### Voice Library
- **200+ voices** across 50+ languages
- Multiple quality levels per language (x_low, low, medium, high)
- Quality vs speed tradeoff: Higher quality = slower inference
- Sample rates: 16kHz (low) to 22.05kHz (high)

### Technical Capabilities
- ONNX runtime (CPU-optimized)
- GPU acceleration available (optional --cuda flag)
- Multiple speakers per model (some voices)
- SSML support (basic)
- Easy installation via pip
- Python API and CLI

## Pricing

**$0 infrastructure cost** (runs on minimal hardware):

| Cost Type | Amount | Notes |
|-----------|--------|-------|
| Licensing | $0 | MIT License (permissive) |
| Per-character | $0 | No usage fees |
| Infrastructure | $0-30/month | Runs on RPi4, cheap VPS, or existing hardware |

**Infrastructure costs** (examples):
- **Raspberry Pi 4** (8GB): $75 one-time (no monthly cost)
- **Budget VPS** (2 CPU, 4GB RAM): $10-20/month
- **AWS t3.medium**: ~$30/month (24/7)
- **Local PC/laptop**: $0 (existing hardware)

**Break-even analysis**:
- Language learning app: 5M chars/month
- Google/Azure cost: $80/month
- Break-even: Hosting < $80/month (Piper easily cheaper)

## Language Learning Use Case

### Strengths
- ✅ **$0 per-character cost** (vs $4-16/M cloud providers)
- ✅ **Extremely fast**: Real-time synthesis on CPU (no GPU required)
- ✅ **Runs on Raspberry Pi**: Deploy on $75 device
- ✅ **Offline operation**: No internet required (useful for classroom labs)
- ✅ **50+ languages**: Good coverage
- ✅ **Easy deployment**: Simple pip install, minimal dependencies

### Weaknesses
- ❌ **No voice cloning**: Pre-trained voices only (vs Coqui's 6-second cloning)
- ❌ **Voice quality**: Good but not premium (behind ElevenLabs, similar to cloud providers)
- ❌ **Limited customization**: Can't fine-tune models easily
- ❌ **No emotion control**: Basic prosody only
- ❌ **Quality levels tradeoff**: Fast = lower quality, high quality = slower

### Ideal For
- **Edge deployments**: Raspberry Pi classroom labs, offline kiosks
- **Real-time applications**: Voice assistants, robotics (CPU-friendly)
- **Cost-sensitive**: Cheapest TTS option (runs on $10/month VPS)
- **Offline requirements**: No internet connectivity needed
- **High-volume, basic needs**: Vocabulary drills where voice quality "good enough"

### Not Ideal For
- **Voice cloning**: No cloning capability (use Coqui instead)
- **Premium voice quality**: Behind ElevenLabs and even cloud providers
- **Emotional expression**: Limited prosody control
- **Custom voices**: Pre-trained voices only

## Competitive Position

**vs. Coqui TTS**: 10× faster, 10× smaller models, but no voice cloning
**vs. Google/Azure/Amazon**: $0/char vs $4-16/M, similar quality, but infrastructure complexity
**vs. ElevenLabs**: $0/char vs $20-66/M, but ElevenLabs voice quality significantly better

**Value Proposition**: Fastest, cheapest TTS for basic needs; best for edge devices and offline use

## Production Readiness

| Factor | Rating | Notes |
|--------|--------|-------|
| Voice Quality | ⭐⭐⭐ | Good quality, not premium |
| Latency | ⭐⭐⭐⭐⭐ | Excellent (real-time on CPU) |
| Language Support | ⭐⭐⭐⭐ | 50+ languages |
| Pricing | ⭐⭐⭐⭐⭐ | $0/char, runs on minimal hardware |
| Ease of Deployment | ⭐⭐⭐⭐⭐ | Easy pip install, minimal deps |
| Voice Cloning | ⭐ | Not supported (pre-trained only) |
| Edge Compatibility | ⭐⭐⭐⭐⭐ | Runs on Raspberry Pi 4 |

## Voice Quality Levels

Piper voices offer quality vs speed tradeoffs:

| Quality | Sample Rate | Model Size | Speed | Use Case |
|---------|------------|------------|-------|----------|
| x_low | 16kHz | 5-10MB | Fastest | Voice assistants, prototyping |
| low | 16kHz | 10-20MB | Very fast | Basic apps, high volume |
| medium | 22.05kHz | 20-30MB | Fast | General purpose |
| high | 22.05kHz | 30-50MB | Moderate | Best quality (still fast) |

**Recommendation for language learning**: **medium** quality (good balance)

## Technical Requirements

### Minimum Requirements
- **CPU**: Any modern CPU (even Raspberry Pi 4)
- **RAM**: 2GB
- **Storage**: 100MB-1GB (depending on voices installed)
- **Python**: 3.8+

### Recommended Setup
- **CPU**: 2+ cores
- **RAM**: 4GB
- **Storage**: SSD for faster model loading
- **OS**: Linux, macOS, Windows (cross-platform)

### GPU Support (Optional)
- Install `onnxruntime-gpu`
- Run with `--cuda` flag
- **Speedup**: 2-5× faster (but CPU already fast enough)

## Inference Speed Comparison

**10-second audio synthesis**:

| Platform | Hardware | Time | Real-time Factor |
|----------|----------|------|------------------|
| Piper (CPU) | 4-core CPU | 0.5-2s | 5-20× real-time |
| Piper (GPU) | RTX 3080 | 0.2-0.5s | 20-50× real-time |
| Coqui (CPU) | 4-core CPU | 10-30s | 0.3-1× real-time |
| Coqui (GPU) | RTX 3080 | 0.5-2s | 5-20× real-time |

**Conclusion**: Piper CPU ≈ Coqui GPU (10× faster)

## Installation & Usage

### Installation (2025)
```bash
# Easy installation via pip
pip install piper-tts

# Or from GitHub (latest)
pip install git+https://github.com/OHF-Voice/piper1-gpl
```

### Basic Usage
```python
from piper import PiperVoice

# Load voice model
voice = PiperVoice.load("en_US-lessac-medium")

# Synthesize audio
voice.synthesize("Hello, how are you?", "output.wav")
```

### CLI Usage
```bash
# Synthesize from text
echo "Hello, world!" | piper --model en_US-lessac-medium --output_file output.wav

# Real-time streaming to speakers
echo "Hello, world!" | piper --model en_US-lessac-medium | aplay
```

## Available Voices

- **Browse voices**: https://rhasspy.github.io/piper-samples/
- **Download models**: Hugging Face (piper models)
- **Voice formats**: `{language}_{region}-{name}-{quality}`
  - Example: `en_US-lessac-medium`, `es_ES-mls-high`, `ja_JP-kokoro-low`

## Edge Deployment Use Cases

### 1. Raspberry Pi Classroom Lab
- 30 Raspberry Pi devices
- Offline vocabulary drills
- $0 ongoing costs (one-time $75/device)

### 2. Voice Assistant (Home Automation)
- Real-time TTS on Raspberry Pi
- No cloud latency
- Privacy (no data leaves device)

### 3. Kiosk/Museum Exhibit
- Offline interactive displays
- Tourist information in multiple languages
- No internet dependency

## When to Choose Piper TTS

Choose Piper TTS when:
1. **Edge deployment** (Raspberry Pi, embedded devices)
2. **Offline operation required** (no internet)
3. **Real-time CPU synthesis** (no GPU available)
4. **Ultra-low cost** (runs on $10/month VPS or $75 RPi)
5. **Speed critical** (fastest open-source TTS)
6. **Good-enough quality** (basic vocabulary drills)

Don't choose Piper TTS when:
1. **Voice cloning needed** (use Coqui instead)
2. **Premium quality required** (use ElevenLabs/cloud)
3. **Emotional expression** (use Coqui or ElevenLabs)
4. **Low volume** (<1M chars/month, cloud easier)

## Recent Updates (2025)

- **Development moved**: https://github.com/OHF-Voice/piper1-gpl
- **Easy installation**: pip install now works reliably
- **GPU support**: CUDA acceleration via --cuda flag
- **More voices**: 200+ voices available
- **Better documentation**: Updated guides and examples

## References

- [Piper TTS (GitHub)](https://github.com/rhasspy/piper)
- [New development (OHF-Voice)](https://github.com/OHF-Voice/piper1-gpl)
- [Voice Samples](https://rhasspy.github.io/piper-samples/)
- [Models on Hugging Face](https://huggingface.co/rhasspy/piper-voices)
