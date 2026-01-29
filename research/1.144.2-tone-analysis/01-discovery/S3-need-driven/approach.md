# S3 Need-Driven Pass: Approach

## Objective
Analyze tone analysis technology through the lens of **specific use cases**, understanding:
- What each user type actually needs
- Which technical choices serve those needs
- Trade-offs specific to each scenario
- Decision criteria for implementation

## Methodology
Starting from real-world needs rather than technology capabilities:
1. Identify distinct user archetypes
2. Map technical requirements to user goals
3. Recommend stack optimized for each use case
4. Highlight critical decision points

## Use Cases Selected

### 1. Pronunciation Practice Apps
**User archetype:** Language learner using mobile/web app
**Core need:** Real-time feedback on tone accuracy
**Key constraint:** Latency (<200ms for "feels instant")

### 2. Speech Recognition Systems
**User archetype:** ASR engineer building Mandarin/Cantonese recognizer
**Core need:** Accurate F0 features for acoustic models
**Key constraint:** Batch processing efficiency

### 3. Linguistic Research
**User archetype:** Phonetics researcher studying tone variation
**Core need:** Publication-grade accuracy, reproducibility
**Key constraint:** Praat compatibility for peer review

### 4. Content Creation Tools
**User archetype:** Audiobook narrator, podcast host
**Core need:** Quality control for tonal language content
**Key constraint:** Non-technical user workflow

### 5. Clinical Assessment
**User archetype:** Speech-language pathologist
**Core need:** Diagnostic precision for tone perception deficits
**Key constraint:** Regulatory compliance, defensible measurements

## Key Questions for Each Use Case

1. **What's the MVP?** Minimum viable implementation
2. **What's the ideal?** Best-case scenario with unlimited resources
3. **What breaks it?** Critical failure modes
4. **What's the budget?** Realistic cost constraints
5. **What's the timeline?** Development schedule

## Differentiation from S1/S2

- **S1**: Surveyed available tools
- **S2**: Deep-dived into technical capabilities
- **S3**: Maps tools to human needs ← **YOU ARE HERE**
- **S4**: Strategic viability analysis (market, ecosystem)

## Documents Created

1. **use-case-01-pronunciation-practice.md** - Real-time learner feedback
2. **use-case-02-speech-recognition.md** - ASR F0 feature extraction
3. **use-case-03-linguistic-research.md** - Academic phonetics studies
4. **use-case-04-content-creation.md** - Quality control for creators
5. **use-case-05-clinical-assessment.md** - Speech therapy diagnostics
6. **recommendation.md** - Decision matrix for use case selection
