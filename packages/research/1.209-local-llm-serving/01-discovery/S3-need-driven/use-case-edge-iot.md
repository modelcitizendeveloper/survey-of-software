# Use Case: Edge/IoT Deployment

---

## Requirements

### Must-Have
- ✅ Runs on CPU (no GPU available)
- ✅ Low memory footprint (< 8GB RAM)
- ✅ ARM architecture support
- ✅ Minimal dependencies (air-gapped OK)
- ✅ Small binary size
- ✅ Works offline
- ✅ Cross-compilation support

### Nice-to-Have
- Mobile platform support (iOS/Android)
- Power efficiency
- Fast startup time
- Easy model updates
- Remote management capabilities

### Constraints
- Hardware: Raspberry Pi 4 (8GB), edge devices, mobile
- No internet connectivity (edge deployment)
- No GPU
- Power constraints (battery in some cases)

---

## Candidate Analysis

### llama.cpp
- ✅ CPU: Excellent (only viable option)
- ✅ Memory: Efficient (Q4 models fit in 6GB)
- ✅ ARM: Native support (NEON optimization)
- ✅ Dependencies: Just C++ (minimal)
- ✅ Binary: Small (~10MB)
- ✅ Offline: Yes (no internet needed)
- ✅ Cross-compile: Yes
- ✅ Mobile: iOS/Android bindings exist
- ✅ Power: Optimized for low-power CPUs
- ✅ Startup: Fast (memory-mapped GGUF)

**Fit:** 100% (only solution that works)

---

### Ollama
- ❌ CPU: Works but uses llama.cpp underneath
- ⚠️ Memory: Similar to llama.cpp
- ✅ ARM: Supported
- ⚠️ Dependencies: Heavier (Go binary + deps)
- ⚠️ Binary: Larger (~50MB+)
- ✅ Offline: Yes
- ⚠️ Cross-compile: Harder
- ❌ Mobile: No (desktop focus)
- ⚠️ Power: Not optimized
- ⚠️ Startup: Slower than raw llama.cpp

**Fit:** 70% (works but heavier than needed)

---

### vLLM
- ❌ CPU: No support (GPU-only)

**Fit:** 0% (incompatible)

---

### LM Studio
- ❌ Desktop GUI (not for embedded/IoT)

**Fit:** 0% (wrong platform)

---

## Recommendation

**Best Fit:** **llama.cpp** (100%)

**Why:**
- **Only solution with good CPU performance** (vLLM has none)
- **Minimal dependencies** (C++ only, no Python runtime)
- **ARM optimization** (NEON SIMD for RPi/mobile)
- **Mobile bindings** (iOS/Android apps possible)
- **Small footprint** (fits on embedded devices)
- **Proven on edge** (powers mobile LLM apps)

**No viable alternatives** for this use case.

**Real-world example:** Run Llama 3.1 8B (Q4) on Raspberry Pi 4 at 2-3 tok/s

---

**Confidence:** 100%
