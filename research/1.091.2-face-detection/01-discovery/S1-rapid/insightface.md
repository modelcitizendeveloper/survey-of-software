# InsightFace: 2D & 3D Face Analysis

## 1. Overview

**What it is**: InsightFace is a state-of-the-art open-source 2D and 3D face analysis toolkit. Known for industry-leading face recognition (ArcFace method), face detection, face alignment, and face attribute analysis. Production-ready with ONNX Runtime support.

**Maintainer**: Jia Guo and Jiankang Deng (DeepInsight team, originally Megvii/Face++)

**License**: Mixed:
- Non-commercial research: Free
- Commercial use: Requires separate license (contact team)
- Models: Various licenses per model

**Primary Language**: Python (primary), with C++ support via ONNX Runtime

**Active Development Status**:
- Repository: https://github.com/deepinsight/insightface
- Last updated: Actively maintained (2024-2025)
- GitHub stars: 23,000+
- Status: Production-ready, widely used in industry

## 2. Core Capabilities

### Face Detection
- **RetinaFace**: High-accuracy single-stage detector
- **SCRFD**: Efficient face detection (Sample and Computation Redistribution)
- Multi-scale detection
- Facial landmark output (5 points) with detection

### Facial Landmarks
- **5-point landmarks**: Eyes, nose, mouth corners (with detection)
- **106-point landmarks**: Dense 2D landmarks (optional model)
- **3D landmarks**: 68-point 3D landmarks via 3D reconstruction models
- Integrated with detection pipeline

### Face Recognition/Identification
- **ArcFace**: State-of-the-art recognition method (99.83% LFW)
- **Multiple backbones**: iResNet, MobileFaceNet, others
- **128-512D embeddings**: Configurable vector size
- One-shot and few-shot learning
- Partial face recognition
- **Masked face recognition**: Trained on occluded faces

### Face Attributes
- Age estimation
- Gender classification
- Face quality assessment
- Pose estimation (yaw, pitch, roll)

### 3D Face Reconstruction
- **Yes**: Full 3D face reconstruction models available
- 3D alignment
- 3D shape and texture extraction

### Real-time Performance
- Optimized for real-time: 30+ FPS with efficient models
- ONNX Runtime enables GPU/CPU acceleration
- Mobile-friendly models available (MobileFaceNet)

## 3. Technical Architecture

### Underlying Models

#### Face Detection
1. **RetinaFace**: Single-stage detector with multi-task learning
   - Backbone: ResNet, MobileNet variants
   - Detects faces + 5 landmarks simultaneously
   - Multi-scale pyramid network

2. **SCRFD**: Efficient detection
   - Sample and Computation Redistribution
   - Faster than RetinaFace with comparable accuracy
   - Optimized for edge devices

#### Face Recognition
1. **ArcFace (Additive Angular Margin Loss)**
   - Backbone: iResNet (improved ResNet) - ResNet34, 50, 100
   - Trained on large-scale datasets (MS1MV2, MS1MV3, WebFace)
   - Metric learning with angular margin
   - 512D embeddings (standard)

2. **Alternative methods**: CosFace, Combined Margin, SphereFace

#### Landmark Detection
- Integrated with detection models
- Separate dense landmark models available

### Pre-trained Models
- **buffalo_l**: General-purpose, balanced accuracy/speed
- **buffalo_sc**: High accuracy, larger model
- **antelopev2**: Latest model pack
- **Models available**: Detection, recognition, alignment, attributes, 3D reconstruction
- **Model zoo**: https://github.com/deepinsight/insightface/tree/master/model_zoo

### Custom Training
- **Fully supported**: Complete training pipelines
- **ArcFace training**: PyTorch implementation available
- **Detection training**: RetinaFace, SCRFD training code
- **Datasets**: Tools for dataset preparation
- **Documentation**: Extensive training guides

### Model Size
- **Detection models**: 1-10 MB (depending on backbone)
- **Recognition models**: 100-300 MB (ResNet-based), 5-15 MB (MobileNet)
- **Total typical deployment**: 50-200 MB
- **Lightweight options**: Sub-10 MB for mobile

### Dependencies
- **ONNX Runtime**: Primary inference engine
- **onnxruntime-gpu** or **onnxruntime** (CPU)
- **NumPy**: Data handling
- **OpenCV**: Image preprocessing (optional)
- **Training**: PyTorch 1.12+, MXNet (legacy)
- **No TensorFlow required**

## 4. Performance Benchmarks

### Detection Accuracy
- **RetinaFace ResNet-50**: 96.3% (easy), 95.6% (medium), 91.4% (hard) on WIDER FACE
- **SCRFD**: Comparable to RetinaFace with better speed
- State-of-the-art on WIDER FACE benchmark

### Face Recognition Accuracy
- **ArcFace on LFW**: 99.83% (top-tier)
- **IJB-B**: 96.21% at FAR=1e-4
- **IJB-C**: 97.37% at FAR=1e-4
- **AgeDB-30**: 98.15%
- **CFP-FP**: 99.08%
- **buffalo_l model**: 99.88% detection success on LFW

### Comparison with Competitors
- **ArcFace**: 99.83% LFW
- **CosineFace**: 99.80% LFW
- **SphereFace**: 99.76% LFW
- **Dlib**: 99.38% LFW
- InsightFace consistently top-5 on NIST-FRVT 1:1 leaderboard

### Speed

| Model | Device | Performance |
|-------|--------|-------------|
| SCRFD-0.5GF | CPU | 100+ FPS |
| SCRFD-10GF | GPU | 200+ FPS |
| RetinaFace (MobileNet) | GPU | 60+ FPS |
| ArcFace (iResNet100) | GPU | 30-50 ms per face |
| MobileFaceNet | CPU | 10-20 ms per face |

### Latency
- **Detection**: 10-30 ms per image (GPU)
- **Recognition embedding**: 20-100 ms per face (depending on model)
- **End-to-end**: 50-150 ms per face (detection + recognition)

### Resource Requirements
- **RAM**: 200-500 MB (loaded models)
- **GPU memory**: 1-4 GB (depending on batch size)
- **CPU**: Multi-threaded, efficient
- **Disk**: 100-300 MB (typical deployment)

## 5. Platform Support

### Desktop
- **Windows**: ✓ (Python, ONNX)
- **macOS**: ✓ (Python, ONNX)
- **Linux**: ✓ (Python, ONNX, primary platform)

### Mobile
- **iOS**: ✓ (ONNX Runtime, CoreML conversion)
- **Android**: ✓ (ONNX Runtime, TFLite conversion)
- MobileFaceNet optimized for mobile

### Web
- **JavaScript/WebAssembly**: Possible via ONNX.js
- Not officially supported
- Requires conversion and optimization

### Edge Devices
- **Raspberry Pi**: ✓ (lightweight models)
- **Jetson Nano/Xavier**: ✓ (excellent with GPU)
- **NVIDIA devices**: First-class support

### Cloud
- Easily deployed in cloud (Docker, Kubernetes)
- ONNX Runtime cloud-friendly

## 6. API & Usability

### Python API Quality
**Rating**: 9/10
- Clean, modern Python API
- Well-structured model zoo
- Easy model loading and inference
- Good abstraction over ONNX complexity

### Code Example: Face Detection and Recognition

```python
import cv2
import numpy as np
from insightface.app import FaceAnalysis

# Initialize the face analysis app
app = FaceAnalysis(name='buffalo_l', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

# Read image
image = cv2.imread('photo.jpg')

# Detect and analyze faces
faces = app.get(image)

# Iterate through detected faces
for face in faces:
    # Bounding box
    bbox = face.bbox.astype(int)
    print(f"Face detected at: {bbox}")

    # Draw bounding box
    cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

    # 5-point landmarks
    landmarks = face.kps.astype(int)
    for point in landmarks:
        cv2.circle(image, tuple(point), 2, (0, 0, 255), -1)

    # Face embedding (512D vector)
    embedding = face.embedding
    print(f"Embedding shape: {embedding.shape}")  # (512,)

    # Face attributes
    if hasattr(face, 'age'):
        print(f"Age: {face.age}")
    if hasattr(face, 'gender'):
        gender = 'Male' if face.gender == 1 else 'Female'
        print(f"Gender: {gender}")

    # Face quality score
    if hasattr(face, 'det_score'):
        print(f"Detection confidence: {face.det_score:.2f}")

cv2.imshow('Face Analysis', image)
cv2.waitKey(0)
```

### Code Example: Face Comparison (1:1 Verification)

```python
import cv2
import numpy as np
from insightface.app import FaceAnalysis

# Initialize
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0)

def get_face_embedding(image_path):
    """Extract face embedding from image"""
    img = cv2.imread(image_path)
    faces = app.get(img)

    if len(faces) == 0:
        return None

    # Return embedding of first face
    return faces[0].embedding

# Compare two faces
embedding1 = get_face_embedding('person1.jpg')
embedding2 = get_face_embedding('person2.jpg')

if embedding1 is not None and embedding2 is not None:
    # Compute cosine similarity
    similarity = np.dot(embedding1, embedding2) / (
        np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
    )

    # Threshold: typically 0.3-0.5 for ArcFace (higher = more similar)
    threshold = 0.4
    if similarity > threshold:
        print(f"Same person! Similarity: {similarity:.3f}")
    else:
        print(f"Different people. Similarity: {similarity:.3f}")
```

### Code Example: Custom Model Loading

```python
import cv2
from insightface.model_zoo import get_model

# Load specific detection model
detector = get_model('retinaface_r50_v1', providers=['CUDAExecutionProvider'])
detector.prepare(ctx_id=0, input_size=(640, 640))

# Load specific recognition model
recognizer = get_model('arcface_r100_v1', providers=['CUDAExecutionProvider'])
recognizer.prepare(ctx_id=0)

# Read image
image = cv2.imread('photo.jpg')

# Detect faces
bboxes, landmarks = detector.detect(image)

# Extract embeddings
for i, bbox in enumerate(bboxes):
    # Align face using landmarks
    aligned_face = recognizer.get_aligned_face(image, landmarks[i])

    # Get embedding
    embedding = recognizer.get_embedding(aligned_face)
    print(f"Face {i} embedding: {embedding.shape}")
```

### Code Example: Face Search (1:N Identification)

```python
import numpy as np
import cv2
from insightface.app import FaceAnalysis

# Initialize
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0)

# Build database of known faces
database = {}

def register_face(name, image_path):
    """Add face to database"""
    img = cv2.imread(image_path)
    faces = app.get(img)
    if len(faces) > 0:
        database[name] = faces[0].embedding
        print(f"Registered: {name}")

# Register known faces
register_face("Alice", "alice.jpg")
register_face("Bob", "bob.jpg")
register_face("Charlie", "charlie.jpg")

def search_face(query_image_path, threshold=0.4):
    """Find matching face in database"""
    img = cv2.imread(query_image_path)
    faces = app.get(img)

    if len(faces) == 0:
        return None, 0.0

    query_embedding = faces[0].embedding

    # Compare with all database embeddings
    best_match = None
    best_similarity = 0.0

    for name, db_embedding in database.items():
        similarity = np.dot(query_embedding, db_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(db_embedding)
        )

        if similarity > best_similarity:
            best_similarity = similarity
            best_match = name

    if best_similarity > threshold:
        return best_match, best_similarity
    else:
        return "Unknown", best_similarity

# Search for face
name, score = search_face("query.jpg")
print(f"Matched: {name} (confidence: {score:.3f})")
```

### Learning Curve
**Rating**: Intermediate (3/5 difficulty)
- Simple API for basic use
- Model zoo structure requires understanding
- ONNX Runtime setup can be tricky (GPU drivers)
- Advanced features need deeper knowledge
- Good examples available

### Documentation Quality
**Rating**: 8/10
- Comprehensive GitHub documentation
- Good model zoo descriptions
- Training guides available
- Community support on GitHub Issues
- Some Chinese-language resources
- Links:
  - GitHub: https://github.com/deepinsight/insightface
  - Model Zoo: https://github.com/deepinsight/insightface/tree/master/model_zoo

## 7. Pricing/Cost Model

**Open Source with Commercial Considerations**
- **Research/Non-commercial**: Free
- **Commercial use**: Contact team for licensing
- **Model licenses**: Vary by model (check model zoo)
- **No API fees**: Self-hosted only
- **Training code**: Freely available

## 8. Integration Ecosystem

### Works With
- **ONNX Runtime**: Primary inference engine
- **OpenCV**: Image I/O and preprocessing
- **NumPy**: Embedding manipulation
- **PyTorch**: Training pipelines
- **MXNet**: Legacy training (older versions)
- **TensorRT**: NVIDIA optimization
- **CoreML**: iOS deployment
- **TFLite**: Android optimization

### Output Format
- **Detections**: Bounding boxes (x1, y1, x2, y2), confidence scores
- **Landmarks**: 5-point (eyes, nose, mouth) or 106-point arrays
- **Embeddings**: NumPy arrays (512D or 128D)
- **Attributes**: Age (int), gender (binary), pose (yaw/pitch/roll)
- **Format**: Python objects, easily serialized to JSON

### Preprocessing Requirements
- **Input**: BGR images (OpenCV format) or RGB
- **Resolution**: Flexible (models handle scaling)
- **Alignment**: Handled internally for recognition
- **Normalization**: Automatic

## 9. Use Case Fit

### Best For
- **Face recognition systems**: Industry-leading accuracy (99.83% LFW)
- **Security and surveillance**: High accuracy, handles occlusions
- **Photo organization**: Face clustering, search by person
- **Access control**: Authentication, attendance systems
- **Social media**: Face tagging, verification
- **Research**: State-of-the-art benchmarks, reproducible
- **Production deployments**: ONNX Runtime stability, cross-platform
- **Masked face recognition**: Models trained on occluded faces

### Ideal Scenarios
- Large-scale face databases (millions of identities)
- Banking/fintech KYC (Know Your Customer) verification
- Airport security and border control
- Photo album auto-tagging (Google Photos style)
- Video surveillance analytics
- Attendance tracking in schools/offices
- Age verification systems
- Celebrity/VIP recognition

### Limitations
- **Commercial licensing**: Requires permission for commercial use
- **No 468-point mesh**: Less detailed than MediaPipe for AR
- **Model size**: Larger than MediaPipe for high accuracy
- **GPU recommended**: CPU performance acceptable but slower
- **ONNX Runtime dependency**: Additional setup complexity
- **No face attributes in all models**: Age/gender require specific models

## 10. Comparison Factors

### Accuracy vs Speed
- **Highest accuracy**: 99.83% on LFW (beats Dlib, MediaPipe for recognition)
- **Flexible speed**: Lightweight models (SCRFD) to high-accuracy (RetinaFace)
- **Sweet spot**: Best accuracy-speed trade-off for recognition
- **GPU-optimized**: Excellent performance with GPU

### Self-hosted vs API
- **Self-hosted only**: No official cloud API
- **Advantage**: No per-call costs, privacy, control
- **ONNX portability**: Deploy anywhere

### Landmark Quality
- **5 points (standard)**: Basic alignment, fast
- **106 points (optional)**: More detailed than Dlib 68
- **Less than MediaPipe**: 468 points vs 106/5
- **Sufficient for recognition**: 5 points adequate for alignment

### 3D Capability
- **Yes**: 3D reconstruction models available
- **3D alignment**: Supported
- **Not as detailed**: Less than MediaPipe's 3D mesh

### Privacy
- **On-device processing**: Complete privacy
- **No cloud dependency**: GDPR-compliant
- **Self-hosted**: Full control over data

---

## Summary Table

| Feature | Rating/Value |
|---------|--------------|
| **Detection Accuracy (WIDER FACE)** | 91.4% (hard), 96.3% (easy) |
| **Face Recognition (LFW)** | 99.83% (ArcFace) |
| **Landmark Count** | 5 points (standard), 106 (optional) |
| **Speed (GPU, detection)** | 60-200+ FPS |
| **Speed (GPU, recognition)** | 30-50 ms per face |
| **Model Size** | 50-200 MB (typical) |
| **Learning Curve** | Intermediate |
| **Platform Support** | Excellent (desktop, mobile via ONNX) |
| **Cost** | Free (non-commercial), License (commercial) |
| **3D Support** | Yes (3D reconstruction models) |
| **Privacy** | On-device (excellent) |

---

## When to Choose InsightFace

Choose InsightFace if you need:
1. **Highest face recognition accuracy** (99.83% LFW, industry-leading)
2. **Production-grade recognition** (security, banking, surveillance)
3. **Large-scale face databases** (millions of identities)
4. **State-of-the-art models** (ArcFace, RetinaFace, SCRFD)
5. **Flexible deployment** (ONNX Runtime, cross-platform)
6. **Masked face recognition** (occluded faces, COVID-era use cases)
7. **Research benchmarks** (reproducible SOTA results)
8. **Custom training** (full training pipelines available)

Avoid InsightFace if you need:
- Dense 3D mesh (468 points) for AR effects (use MediaPipe)
- Simple 68-point landmarks without recognition (use Dlib)
- Commercial use without licensing (use MediaPipe, Dlib)
- Minimal setup complexity (use cloud APIs like AWS Rekognition)
- Web-first deployment (use MediaPipe JavaScript)

---

**Last Updated**: January 2025
