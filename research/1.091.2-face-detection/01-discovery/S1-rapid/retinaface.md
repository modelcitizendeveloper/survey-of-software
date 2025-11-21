# RetinaFace: Single-stage Dense Face Localisation

## 1. Overview

**What it is**: RetinaFace is a state-of-the-art single-stage face detection framework that performs pixel-wise face localization with multi-task learning. Simultaneously predicts face bounding boxes, 5 facial landmarks, and 3D face information. Known for exceptional accuracy on challenging datasets.

**Maintainer**: Original paper by Jiankang Deng et al. (Imperial College London, InsightFace team), multiple open-source implementations

**License**: MIT License (most implementations)

**Primary Language**: Python (PyTorch, MXNet implementations)

**Active Development Status**:
- Original paper: 2019 (CVPR)
- Popular implementations:
  - https://github.com/serengil/retinaface (3,000+ stars)
  - https://github.com/biubug6/Pytorch_Retinaface (7,000+ stars)
- Status: Actively maintained, production-ready, state-of-the-art

## 2. Core Capabilities

### Face Detection
- **Single-stage detector**: No proposal generation (faster than two-stage)
- **Multi-scale detection**: Feature pyramid network
- **High accuracy**: State-of-the-art on WIDER FACE benchmark
- **Dense predictions**: Pixel-wise face localization
- Multi-face detection support

### Facial Landmarks
- **5-point landmarks**: Eyes (2), nose (1), mouth corners (2)
- Output simultaneously with detection
- Used for face alignment and quality assessment

### Face Recognition/Identification
- Not included (detection and landmarks only)
- Often used with InsightFace for full pipeline

### Face Attributes
- Not directly provided
- Face quality score from landmark confidence

### 3D Face Reconstruction
- **3D face information**: Outputs 3D position hints (optional)
- Not full 3D reconstruction
- Helps with pose estimation

### Real-time Performance
- **GPU real-time**: 30+ FPS on modern GPUs
- **CPU acceptable**: 5-15 FPS (depending on backbone)
- MobileNet backbone enables mobile deployment

## 3. Technical Architecture

### Underlying Models

#### Single-stage Dense Face Localization
- **Feature Pyramid Network (FPN)**: Multi-scale feature extraction
- **Backbone options**:
  - **ResNet-50/101/152**: High accuracy
  - **MobileNet-0.25**: Lightweight, mobile-friendly (1.7 MB)
  - **VGG-16**: Legacy option
- **RetinaNet-style**: Anchor-based detection with focal loss

#### Multi-task Learning Branches
1. **Classification branch**: Face vs. non-face
2. **Bounding box regression**: Face localization
3. **Landmark regression**: 5 facial landmarks
4. **3D vertices regression** (optional): 3D face position hints

### Architecture Details
- **Feature pyramid**: 5 levels (P2-P6)
- **Context module**: Increases receptive field
- **SSH modules**: Single Stage Headless design
- **Deformable convolution**: Better geometric variation handling
- **Multi-task loss**: Weighted sum of all branches

### Pre-trained Models
- **ResNet-50 backbone**: Best balance (accuracy/speed)
- **MobileNet-0.25**: Lightweight (1.7 MB, 80.99% WIDER FACE hard)
- **ResNet-152**: Highest accuracy (91.4% WIDER FACE hard)
- Trained on WIDER FACE dataset
- Available from model zoos (PyTorch, MXNet, ONNX)

### Custom Training
- **Fully supported**: Training code available
- **Datasets**: WIDER FACE, custom annotations
- **PyTorch training**: Most actively maintained
- **Configuration**: Flexible anchor, loss, augmentation settings
- **Documentation**: Good training guides

### Model Size
- **MobileNet-0.25**: 1.7 MB (ultra-lightweight)
- **ResNet-50**: 30-50 MB
- **ResNet-152**: 150-200 MB
- **Trade-off**: Accuracy vs. size/speed

### Dependencies
- **PyTorch** or **MXNet** (backend)
- **OpenCV**: Image processing
- **NumPy**: Array operations
- **torchvision**: For PyTorch implementations
- **ONNX Runtime**: For production deployment (optional)

## 4. Performance Benchmarks

### Detection Accuracy (WIDER FACE Benchmark)

#### Original RetinaFace (ResNet-152)
- **Easy set**: 96.3% AP
- **Medium set**: 95.6% AP
- **Hard set**: 91.4% AP
- **Result**: State-of-the-art, 1.1% better than previous best (2019)

#### Lightweight RetinaFace (MobileNet-0.25)
- **Easy set**: 90-94% AP
- **Medium set**: 88-93% AP
- **Hard set**: 80-84% AP
- **Model size**: 1.7 MB only

#### 2024 Performance Reports
- **ResNet-based**: 94-96% (easy), 93-95% (medium), 83-91% (hard)
- **Improved variants**: Up to 94.1% easy, 92.2% medium, 82.1% hard

### Comparison with Other Methods (WIDER FACE Hard)
- **RetinaFace (ResNet-152)**: 91.4%
- **MTCNN**: 83.55%
- **Dlib CNN**: Not specifically benchmarked on WIDER FACE
- **Haar cascades**: ~60-70%

### Speed

| Backbone | Device | Performance |
|----------|--------|-------------|
| MobileNet-0.25 | CPU | 10-20 FPS |
| MobileNet-0.25 | GPU | 60+ FPS |
| ResNet-50 | CPU | 3-7 FPS |
| ResNet-50 | GPU | 30-50 FPS |
| ResNet-152 | GPU | 15-25 FPS |

### Speed vs. Accuracy Trade-off
- **MobileNet-0.25**: Fast, lightweight, 80% hard accuracy
- **ResNet-50**: Balanced, 85-88% hard accuracy
- **ResNet-152**: Highest accuracy (91.4%), slower

### Latency
- **MobileNet (GPU)**: 15-30 ms per frame
- **ResNet-50 (GPU)**: 30-60 ms per frame
- **CPU latency**: 100-300 ms (depending on backbone)

### Resource Requirements
- **RAM**: 200-500 MB (loaded models)
- **GPU memory**: 1-3 GB (depending on backbone, batch size)
- **CPU**: Multi-threaded, moderate to high usage
- **Disk**: 2 MB - 200 MB (model dependent)

## 5. Platform Support

### Desktop
- **Windows**: ✓ (Python, PyTorch/MXNet)
- **macOS**: ✓ (Python, PyTorch/MXNet)
- **Linux**: ✓ (Python, primary platform)

### Mobile
- **iOS**: ✓ (CoreML conversion, MobileNet backbone)
- **Android**: ✓ (TFLite conversion, MobileNet backbone)
- MobileNet variant optimized for mobile

### Web
- **JavaScript**: Possible (ONNX.js, TensorFlow.js)
- Not officially supported
- Community implementations exist

### Edge Devices
- **Raspberry Pi**: ✓ (MobileNet backbone, acceptable performance)
- **Jetson Nano/Xavier**: ✓ (excellent with GPU)
- **NVIDIA devices**: First-class support
- **Embedded**: ✓ (MobileNet is edge-friendly)

### Cloud
- Easily deployed in cloud (Docker, Kubernetes)
- ONNX export for production

## 6. API & Usability

### Python API Quality
**Rating**: 8/10 (varies by implementation)
- serengil/retinaface: Simple, high-level API (9/10)
- biubug6/Pytorch_Retinaface: Lower-level, more control (7/10)
- Good documentation in popular repos

### Code Example: Simple Face Detection (serengil/retinaface)

```python
from retinaface import RetinaFace
import cv2

# Detect faces (automatically downloads model on first use)
faces = RetinaFace.detect_faces('photo.jpg')

# Read image for visualization
image = cv2.imread('photo.jpg')

# Iterate through detected faces
for key, face in faces.items():
    # Bounding box
    facial_area = face['facial_area']
    x1, y1, x2, y2 = facial_area
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Confidence score
    score = face['score']
    cv2.putText(image, f'{score:.2f}', (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 5-point landmarks
    landmarks = face['landmarks']
    for landmark_name, point in landmarks.items():
        cv2.circle(image, (int(point[0]), int(point[1])), 2, (0, 0, 255), -1)

    # Individual landmarks
    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']
    nose = landmarks['nose']
    mouth_left = landmarks['mouth_left']
    mouth_right = landmarks['mouth_right']

    print(f"Face: {key}, Score: {score:.2f}, Box: {facial_area}")

cv2.imshow('RetinaFace Detection', image)
cv2.waitKey(0)
```

### Code Example: Custom Model and Threshold

```python
from retinaface import RetinaFace

# Build model with specific backend
model = RetinaFace.build_model()

# Detect with custom threshold
faces = RetinaFace.detect_faces(
    img_path='photo.jpg',
    threshold=0.9,          # Higher threshold = fewer false positives
    model=model,
    allow_upscaling=True    # Detect smaller faces
)

print(f"Detected {len(faces)} faces with high confidence")
```

### Code Example: PyTorch Implementation (biubug6)

```python
import torch
import cv2
from models.retinaface import RetinaFace
from utils.box_utils import decode, decode_landm
import numpy as np

# Load model
model = RetinaFace(cfg=cfg, phase='test')
model.load_state_dict(torch.load('weights/Resnet50_Final.pth'))
model.eval()
model = model.cuda()

# Prepare image
image = cv2.imread('photo.jpg')
img = np.float32(image)
im_height, im_width, _ = img.shape

# Preprocessing
scale = torch.Tensor([img.shape[1], img.shape[0],
                       img.shape[1], img.shape[0]])
img -= (104, 117, 123)
img = img.transpose(2, 0, 1)
img = torch.from_numpy(img).unsqueeze(0)
img = img.cuda()

# Forward pass
loc, conf, landms = model(img)

# Post-processing
priorbox = PriorBox(cfg, image_size=(im_height, im_width))
priors = priorbox.forward()
priors = priors.cuda()

boxes = decode(loc.data.squeeze(0), priors.data, cfg['variance'])
boxes = boxes * scale
boxes = boxes.cpu().numpy()

scores = conf.squeeze(0).data.cpu().numpy()[:, 1]
landms = decode_landm(landms.data.squeeze(0), priors.data, cfg['variance'])

# Filter by confidence
inds = np.where(scores > 0.5)[0]
boxes = boxes[inds]
landms = landms[inds]
scores = scores[inds]

# Apply NMS
keep = nms(boxes, scores, nms_threshold=0.4)
boxes = boxes[keep]
landms = landms[keep]

# Draw results
for box, landmark in zip(boxes, landms):
    # Bounding box
    x1, y1, x2, y2 = map(int, box[:4])
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Landmarks (5 points)
    landmark = landmark.reshape(-1, 2)
    for point in landmark:
        cv2.circle(image, tuple(map(int, point)), 2, (0, 0, 255), -1)

cv2.imshow('RetinaFace', image)
cv2.waitKey(0)
```

### Code Example: ONNX Runtime Deployment

```python
import onnxruntime as ort
import cv2
import numpy as np

# Load ONNX model
session = ort.InferenceSession(
    'retinaface_resnet50.onnx',
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
)

# Prepare input
image = cv2.imread('photo.jpg')
input_image = cv2.resize(image, (640, 640))
input_image = input_image.astype(np.float32)
input_image = np.transpose(input_image, (2, 0, 1))
input_image = np.expand_dims(input_image, axis=0)

# Run inference
outputs = session.run(None, {'input': input_image})

# Parse outputs (bounding boxes, scores, landmarks)
boxes, scores, landmarks = outputs[0], outputs[1], outputs[2]

# Apply confidence threshold and NMS
# ... (post-processing logic)
```

### Learning Curve
**Rating**: Intermediate (3/5 difficulty)
- High-level implementations: Easy (serengil)
- Low-level implementations: Moderate (PyTorch training)
- Good examples available
- Understanding anchors and FPN helps

### Documentation Quality
**Rating**: 8/10
- Original paper: Excellent theoretical background
- serengil/retinaface: Good README, simple examples
- biubug6/Pytorch_Retinaface: Good for training
- Active community support
- Links:
  - Paper: https://arxiv.org/abs/1905.00641
  - serengil: https://github.com/serengil/retinaface
  - PyTorch: https://github.com/biubug6/Pytorch_Retinaface

## 7. Pricing/Cost Model

**Free and Open Source**
- MIT License (most implementations)
- No usage fees
- Commercial use permitted
- Self-hosted only

## 8. Integration Ecosystem

### Works With
- **PyTorch**: Primary framework
- **MXNet**: Alternative implementation
- **ONNX Runtime**: Production deployment
- **OpenCV**: Image I/O and preprocessing
- **NumPy**: Array operations
- **TensorRT**: NVIDIA optimization
- **CoreML**: iOS deployment
- **TensorFlow Lite**: Android optimization
- **InsightFace**: Often used together for full face pipeline

### Output Format
- **Detections**: Bounding boxes [x1, y1, x2, y2], confidence scores
- **Landmarks**: 5 points (eyes, nose, mouth) as [x, y] coordinates
- **Confidence**: Float (0-1)
- **Format**: NumPy arrays or Python dicts (depending on wrapper)

### Preprocessing Requirements
- **Input**: BGR (OpenCV) or RGB images
- **Resolution**: Flexible (models handle scaling)
- **Normalization**: Mean subtraction (104, 117, 123)
- **Aspect ratio**: Can be maintained or modified

## 9. Use Case Fit

### Best For
- **High-accuracy requirements**: State-of-the-art detection (91.4% WIDER FACE hard)
- **Challenging conditions**: Occlusions, varied poses, small faces
- **Production systems**: Robust, well-tested
- **Multi-scale detection**: Faces of various sizes
- **GPU-accelerated pipelines**: Real-time with GPU
- **Mobile deployment**: MobileNet backbone (1.7 MB)
- **Research**: State-of-the-art baseline
- **Face alignment preprocessing**: 5 landmarks for recognition pipelines

### Ideal Scenarios
- Security and surveillance (detecting faces in crowds)
- High-resolution image analysis (photos with many faces)
- Challenging lighting conditions (indoor, outdoor, mixed)
- Occluded faces (masks, glasses, hands)
- Wide age range (children to elderly)
- Pose variations (profile, tilted heads)
- Photo organization (accurate face detection for tagging)
- Attendance systems (multiple people in frame)

### Limitations
- **Only 5 landmarks**: Less detailed than 68-point (Dlib) or 468-point (MediaPipe)
- **No face recognition**: Detection only, needs separate recognition model
- **No face attributes**: Age, gender, emotion not provided
- **GPU recommended**: CPU performance acceptable but slower
- **Setup complexity**: More complex than high-level libraries (depends on implementation)
- **Not 3D mesh**: Only 5 landmarks, not full 3D reconstruction

## 10. Comparison Factors

### Accuracy vs Speed
- **Highest accuracy**: 91.4% WIDER FACE hard (ResNet-152)
- **Flexible speed**: MobileNet (fast) to ResNet-152 (slower)
- **GPU-optimized**: 30+ FPS with ResNet-50
- **Sweet spot**: Best accuracy for single-stage detectors
- **Better than**: MTCNN (83.55%), Dlib, Haar cascades
- **Comparable to**: SCRFD (newer, similar accuracy, better speed)

### Self-hosted vs API
- **Self-hosted only**: No official cloud API
- **Advantage**: No per-call costs, privacy, control
- **Easy deployment**: ONNX export, Docker-friendly

### Landmark Quality
- **5 points**: Basic alignment capability
- **Sufficient for**: Face alignment before recognition
- **Less than**: Dlib (68), MediaPipe (468)
- **More than**: Basic detectors (0)

### 3D Capability
- **Limited 3D**: Optional 3D hints, not full reconstruction
- **Use instead**: MediaPipe for full 3D mesh

### Privacy
- **On-device processing**: Complete privacy
- **No telemetry**: No data collection
- **GDPR-compliant**: Ideal for privacy-sensitive applications

---

## Summary Table

| Feature | Rating/Value |
|---------|--------------|
| **Detection Accuracy (WIDER FACE Hard)** | 91.4% (ResNet-152), 80-84% (MobileNet) |
| **Landmark Count** | 5 points (2D) |
| **Speed (ResNet-50, GPU)** | 30-50 FPS |
| **Speed (MobileNet, GPU)** | 60+ FPS |
| **Speed (CPU)** | 3-20 FPS (backbone-dependent) |
| **Model Size** | 1.7 MB (MobileNet) - 200 MB (ResNet-152) |
| **Learning Curve** | Intermediate |
| **Platform Support** | Excellent (desktop, mobile) |
| **Cost** | Free (MIT License) |
| **3D Support** | Limited (3D hints only) |
| **Privacy** | On-device (excellent) |

---

## When to Choose RetinaFace

Choose RetinaFace if you need:
1. **State-of-the-art detection accuracy** (91.4% WIDER FACE hard)
2. **Challenging conditions**: Occlusions, varied poses, small faces
3. **Production-grade robustness** (well-tested, widely deployed)
4. **Flexible speed/accuracy trade-off** (MobileNet to ResNet-152)
5. **Mobile deployment** (1.7 MB MobileNet model)
6. **Multi-scale detection** (faces of all sizes)
7. **GPU-accelerated pipeline** (real-time 30+ FPS)
8. **Face alignment preprocessing** (5 landmarks before recognition)

Avoid RetinaFace if you need:
- Dense landmarks (68/468 points) for detailed facial analysis (use Dlib, MediaPipe)
- Face recognition (use InsightFace, Dlib)
- Face attributes (age, gender) (use commercial APIs)
- Simplest possible API (use MediaPipe, serengil/retinaface wrapper)
- Full 3D face mesh (use MediaPipe)
- CPU-only fast detection (use Haar cascades, YuNet)

---

## Integration with InsightFace

RetinaFace is part of the InsightFace ecosystem and is often used as the detection component:
1. **RetinaFace**: Detect faces and 5 landmarks
2. **Align faces**: Use landmarks for alignment
3. **ArcFace**: Extract face embeddings for recognition

This combination provides a complete face detection + recognition pipeline with state-of-the-art performance.

---

**Last Updated**: January 2025
