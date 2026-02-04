# Face Detection & Recognition Libraries: S1 Rapid Discovery

## Research Overview

This directory contains comprehensive S1 Rapid Discovery research on face detection and recognition libraries for experiment **1.091.2** in the spawn-solutions research framework.

**Research Date**: January 2025
**Research Type**: Generic reference material (Hardware Store for Software)
**Scope**: Comparative analysis of 8 face detection/recognition solutions

---

## Documents in This Research

### Individual Library Analyses

1. **[mediapipe.md](./mediapipe.md)** (364 lines)
   - Google's MediaPipe Face Detection & Mesh
   - 468-point 3D face mesh, mobile-optimized
   - Best for: AR filters, mobile apps, 3D face tracking

2. **[dlib.md](./dlib.md)** (468 lines)
   - Dlib Face Detection & Recognition
   - 68-point landmarks, 99.38% LFW recognition accuracy
   - Best for: Face recognition, landmark detection, desktop apps

3. **[insightface.md](./insightface.md)** (527 lines)
   - InsightFace 2D & 3D Face Analysis
   - State-of-the-art recognition (99.83% LFW), ArcFace method
   - Best for: Production face recognition, high accuracy requirements

4. **[mtcnn.md](./mtcnn.md)** (485 lines)
   - Multi-task Cascaded Convolutional Networks
   - Lightweight (2 MB), cascade detector
   - Best for: Legacy systems, embedded devices, educational

5. **[retinaface.md](./retinaface.md)** (515 lines)
   - RetinaFace Single-stage Dense Face Localisation
   - Highest detection accuracy (91.4% WIDER FACE hard)
   - Best for: Challenging conditions, occlusions, production systems

6. **[opencv.md](./opencv.md)** (562 lines)
   - OpenCV Face Detection Methods (Haar, LBP, DNN)
   - Traditional (fast CPU) and modern (DNN) approaches
   - Best for: Quick prototyping, embedded systems, universal compatibility

7. **[commercial-apis.md](./commercial-apis.md)** (747 lines)
   - Face++ API (Megvii) and Amazon Rekognition
   - Cloud-based, comprehensive face attributes
   - Best for: MVPs, no infrastructure, need age/gender/emotion

### Synthesis & Decision Framework

8. **[synthesis.md](./synthesis.md)** (609 lines)
   - **Master comparison table** across all libraries
   - **Decision framework**: "Choose X if you need Y"
   - **Accuracy vs speed spectrum** with benchmarks
   - **Use case patterns**: Security, photo organization, AR, attendance, etc.
   - **Self-hosted vs cloud trade-offs**
   - **Quick decision tree** for choosing libraries
   - **Performance optimization tips**
   - **Privacy implications** (GDPR-compliant options)

---

## Quick Reference

### By Primary Need

| Need | Recommended Library | Document |
|------|-------------------|----------|
| **Highest detection accuracy** | RetinaFace (91.4%) | [retinaface.md](./retinaface.md) |
| **Highest recognition accuracy** | InsightFace (99.83% LFW) | [insightface.md](./insightface.md) |
| **Dense 3D face mesh** | MediaPipe (468 points) | [mediapipe.md](./mediapipe.md) |
| **68-point landmarks** | Dlib | [dlib.md](./dlib.md) |
| **Fastest CPU detection** | OpenCV Haar Cascades | [opencv.md](./opencv.md) |
| **Mobile/web support** | MediaPipe | [mediapipe.md](./mediapipe.md) |
| **Face attributes (age/gender)** | Face++, AWS Rekognition | [commercial-apis.md](./commercial-apis.md) |
| **Smallest model (<2 MB)** | MTCNN, RetinaFace (MobileNet) | [mtcnn.md](./mtcnn.md), [retinaface.md](./retinaface.md) |
| **Privacy-friendly (on-device)** | All self-hosted libraries | See individual docs |
| **Quick MVP (cloud)** | AWS Rekognition, Face++ | [commercial-apis.md](./commercial-apis.md) |

### Accuracy Benchmarks

| Library | Detection Accuracy | Recognition Accuracy (LFW) |
|---------|-------------------|---------------------------|
| **RetinaFace** | 91.4% (WIDER FACE hard) | N/A (detection only) |
| **InsightFace** | 91.4% (uses RetinaFace) | **99.83%** |
| **MediaPipe** | 99.3% (comparative study) | N/A (detection only) |
| **Dlib** | Excellent (CNN), Good (HOG) | 99.38% |
| **MTCNN** | 97.56% AUC (2016) | N/A (detection only) |
| **OpenCV DNN** | 85-95% | N/A (weak built-in) |
| **OpenCV Haar** | 70-85% (frontal only) | N/A (weak built-in) |
| **Face++** | 99%+ (proprietary) | 99%+ (proprietary) |
| **AWS Rekognition** | High (production-grade) | High (production-grade) |

### Speed Comparison (CPU)

| Library | Speed (FPS) | Notes |
|---------|-------------|-------|
| **OpenCV Haar** | 30+ FPS | Fastest, frontal faces only |
| **Dlib HOG** | 30+ FPS | Fast, frontal faces only |
| **MediaPipe** | 60-100 FPS | Optimized, but 468 landmarks |
| **OpenCV DNN** | 15-30 FPS | Good balance |
| **MTCNN** | 5-15 FPS | Cascade design |
| **RetinaFace** | 3-20 FPS | Depends on backbone |
| **Dlib CNN** | 1-3 FPS | Requires GPU for real-time |

---

## Research Methodology

### Information Sources
- Official documentation and GitHub repositories
- Academic papers (CVPR, ECCV, ICCV)
- Benchmark datasets: WIDER FACE, LFW, IJB-B/C, 300W, AFLW
- Community implementations and performance reports
- Web search (2024-2025 current information)

### Evaluation Criteria
1. Detection accuracy (WIDER FACE benchmark)
2. Recognition accuracy (LFW benchmark)
3. Landmark quality (point count, 2D vs 3D)
4. Speed (FPS on CPU and GPU)
5. Model size (MB)
6. Platform support (desktop, mobile, web, edge)
7. API usability and documentation
8. Licensing and cost
9. Privacy implications
10. Production readiness

---

## How to Use This Research

### For Decision Making
1. **Start with**: [synthesis.md](./synthesis.md) - Decision framework and comparison table
2. **Use case matching**: Find your scenario in the "Generic Use Case Patterns" section
3. **Deep dive**: Read individual library documents for implementation details

### For Implementation
1. **Choose library** based on synthesis recommendations
2. **Review code examples** in individual library documents
3. **Check platform support** for your target deployment
4. **Verify licensing** for commercial use

### For Benchmarking
1. **Compare metrics** in synthesis master table
2. **Review accuracy benchmarks** (WIDER FACE, LFW)
3. **Check speed comparisons** for your hardware profile

---

## Key Insights

### Top 3 for Each Category

**Detection Accuracy**:
1. RetinaFace (ResNet-152): 91.4% WIDER FACE hard
2. InsightFace (RetinaFace): 91.4% WIDER FACE hard
3. MediaPipe: 99.3% comparative study

**Recognition Accuracy**:
1. InsightFace (ArcFace): 99.83% LFW
2. Dlib: 99.38% LFW
3. Face++: 99%+ (proprietary)

**Mobile Performance**:
1. MediaPipe: 30-60 FPS, <10 MB, official SDKs
2. RetinaFace (MobileNet): 1.7 MB, 60+ FPS GPU
3. MTCNN: 2 MB, acceptable mobile performance

**Privacy-Friendly (On-device)**:
1. MediaPipe: No telemetry, Apache 2.0
2. Dlib: No telemetry, Boost License
3. InsightFace: ONNX Runtime, self-hosted

**Cost-Effective (Self-hosted)**:
1. OpenCV: Free, Apache 2.0, minimal dependencies
2. MediaPipe: Free, Apache 2.0, <10 MB
3. MTCNN: Free, MIT License, 2 MB

---

## Document Statistics

- **Total documents**: 8 (7 libraries + 1 synthesis)
- **Total lines**: 4,277
- **Total size**: 148 KB
- **Code examples**: 30+ Python examples across all documents
- **Benchmarks cited**: WIDER FACE, LFW, IJB-B/C, 300W, AFLW
- **Libraries covered**: 8 (6 self-hosted + 2 commercial APIs)

---

## Generic Use Case Examples

These are **generic patterns** applicable to any developer, NOT client-specific:

1. **Security Systems**: Surveillance, access control, attendance tracking
2. **Photo Organization**: Face clustering, search by person, album tagging
3. **AR Applications**: Filters, effects, virtual try-on, face tracking
4. **Video Conferencing**: Background blur, beautification, face position
5. **Retail Analytics**: Customer demographics, emotion analysis
6. **Age Verification**: Online services, retail compliance
7. **Social Media**: Face tagging, verification, content moderation

---

## Navigation Tips

- **New to face detection?** Start with [opencv.md](./opencv.md) (easiest) or [mediapipe.md](./mediapipe.md) (modern)
- **Need highest accuracy?** Read [retinaface.md](./retinaface.md) (detection) and [insightface.md](./insightface.md) (recognition)
- **Building MVP quickly?** Check [commercial-apis.md](./commercial-apis.md) for cloud options
- **Privacy concerns?** All self-hosted libraries support on-device processing (see synthesis)
- **Overwhelmed by choices?** Use the decision tree in [synthesis.md](./synthesis.md)

---

## Updates & Maintenance

This research reflects the state of face detection/recognition libraries as of **January 2025**. Key libraries are actively maintained:

- **MediaPipe**: Google actively developing (2024-2025)
- **Dlib**: Stable, mature (10+ years)
- **InsightFace**: Actively maintained (2024-2025)
- **RetinaFace**: Community implementations maintained
- **OpenCV**: Very actively maintained (2024-2025)
- **MTCNN**: Stable, less active (surpassed by newer methods)
- **Face++, AWS Rekognition**: Commercial services, regularly updated

---

## Contact & Feedback

This research is part of the spawn-solutions research framework, experiment **1.091.2**.

For questions or additions, consult the individual library documentation and GitHub repositories linked in each document.

---

**Research completed**: January 2025
**Framework**: spawn-solutions
**Experiment**: 1.091.2-face-detection
**Phase**: S1 Rapid Discovery
