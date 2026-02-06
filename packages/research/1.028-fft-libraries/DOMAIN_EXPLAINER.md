# FFT Libraries: A Decision-Maker's Guide

## What This Solves

**The problem:** You have data changing over time (audio, sensor readings, images), and you need to understand WHAT patterns are happening and HOW OFTEN.

**Who encounters this:**
- Audio engineers analyzing sound frequencies (pitch, harmonics)
- Data scientists finding cycles in time-series (daily, weekly, seasonal patterns)
- Embedded developers processing sensor signals (vibration, acceleration)
- Scientists solving equations using spectral methods
- ML engineers converting audio to spectrograms for neural networks

**Why it matters:**
Some problems are much easier to solve when you look at frequency patterns rather than raw time-series data. Like how sheet music (frequencies) is easier to understand than raw audio waveforms.

---

## Accessible Analogies

### What is an FFT?

**The prism analogy:**
White light passing through a prism splits into rainbow colors (frequencies). An FFT is like a mathematical prism that splits time-series data into its frequency components.

- **Input:** Sound recording (time domain) - wiggly waveform
- **FFT:** Mathematical prism
- **Output:** Spectrum (frequency domain) - which notes are playing

**Why "Fast"?**
The naive approach takes N² operations. FFT uses clever math (divide-and-conquer) to do it in N log N operations. For 1 million samples, that's 1000x faster.

### Library Comparison as Transportation

Think of FFT libraries like transportation options:

- **FFTW:** High-speed train - Fastest, but requires station infrastructure (complex setup)
- **scipy.fft:** Taxi service - Call it when needed, reasonable speed, easy to use
- **numpy.fft:** Old bus - Gets you there, but slowly. Replaced by newer buses (scipy.fft)
- **pyFFTW:** Rental Ferrari - Maximum speed, but you manage everything (insurance, gas, maintenance)
- **KissFFT:** Bicycle - Simple, portable, goes anywhere, but not as fast

---

## When You Need This

### ✅ Clear signals you need an FFT library:

1. **"What frequencies are in this signal?"**
   - Audio: Detecting musical notes, pitch
   - Sensors: Vibration analysis (bearing faults at specific frequencies)
   - Time-series: Finding cycles (weekly sales patterns)

2. **"I need to filter specific frequencies"**
   - Remove noise (high-pass, low-pass filters)
   - Isolate specific bands (heart rate from PPG sensor: 0.8-2 Hz)
   - Audio effects (EQ, reverb via convolution)

3. **"Processing images in frequency domain"**
   - Compression (JPEG uses DCT, similar to FFT)
   - Sharpening, blurring
   - Pattern recognition

4. **"Solving differential equations"**
   - Spectral methods in computational physics
   - Faster than finite difference for some problems

### ❌ When you DON'T need this:

- **Simple statistics:** Mean, median, variance → Don't need FFT
- **Detecting outliers:** Threshold-based anomalies → Don't need FFT
- **Time-domain features:** Peak detection, zero-crossings → Don't need FFT
- **Small datasets:** `<100` samples → FFT isn't useful (too short to find frequencies)

**Rule of thumb:** If you're not asking "what frequencies?" or "how often?", you probably don't need FFT.

---

## Trade-offs

### Performance vs Simplicity

**High performance (FFTW, pyFFTW):**
- ✅ 2-10x faster
- ✅ Scales to massive datasets
- ❌ Complex setup (planning, configuration)
- ❌ Steeper learning curve

**Simple and fast enough (scipy.fft):**
- ✅ One function call, no setup
- ✅ 90% the speed of FFTW
- ✅ Works in Jupyter notebooks
- ⚠️ Slight overhead vs raw FFTW

**Portable and simple (KissFFT):**
- ✅ Runs on microcontrollers
- ✅ 10KB of code (vs 2MB for FFTW)
- ✅ BSD license (commercial-friendly)
- ❌ 50-60% the speed of FFTW

**Key insight:** Most projects don't need the absolute fastest option. scipy.fft is fast enough for 80% of use cases.

### Licensing: Open vs Restricted

**GPL (FFTW):**
- **Good for:** Academic research, internal tools, open source projects
- **Problematic for:** Commercial products you distribute (must provide source OR buy license)
- **Cost:** Free (GPL) OR ~$6K one-time (commercial)

**BSD/MIT (scipy.fft, KissFFT):**
- **Good for:** Any use case, including closed-source commercial
- **Cost:** Free always
- **Note:** scipy.fft uses FFTW backend, but your code stays BSD (dynamic linking)

**Real-world example:** Audio plugin developer
- Selling plugin → Can't use FFTW GPL without source code release
- Options: (1) Buy FFTW commercial license, (2) Use KissFFT (BSD)
- Many choose KissFFT (good enough speed, simpler licensing)

### Language Ecosystem

**Python (scipy.fft):**
- ✅ Integrates with NumPy, pandas, matplotlib
- ✅ Jupyter-friendly (interactive exploration)
- ✅ Easy prototyping
- ⚠️ Python overhead (not for ultra-low latency)

**C/C++ (FFTW, KissFFT):**
- ✅ Maximum performance (no interpreter)
- ✅ Embeddable (audio plugins, firmware)
- ❌ Manual memory management
- ❌ Longer development time

**Embedded (KissFFT):**
- ✅ Tiny footprint (10KB code, 4KB RAM)
- ✅ Pure C (no dynamic allocation)
- ✅ Fixed-point arithmetic (for MCUs without FPU)
- ⚠️ Moderate performance (but often sufficient)

---

## Cost Considerations

### Direct Costs

**Free options:**
- scipy.fft, numpy.fft, pyFFTW wrapper, KissFFT: $0
- FFTW (GPL): $0 if open source

**Commercial licenses:**
- FFTW commercial: ~$6,000 one-time
- Intel MKL: Included with Intel compiler suite (~$500-1000/year)

### Hidden Costs

**Development time:**
- scipy.fft: ~1 hour to learn and integrate
- pyFFTW: ~1 day (plan management complexity)
- FFTW (C): ~2-3 days (build system, memory management)
- KissFFT: ~2-4 hours (simple C integration)

**Maintenance:**
- scipy.fft: Minimal (NumPy/SciPy team maintains)
- FFTW: Monitor for updates (slow release cadence)
- KissFFT: May need to fork/maintain (low activity)

**Infrastructure:**
- Python stack: 20-50MB (NumPy + SciPy)
- FFTW: 2-5MB (compiled library)
- KissFFT: 10-50KB (minimal footprint)

### Break-Even Analysis

**Example: Commercial audio plugin**

**Option A: FFTW commercial license**
- Cost: $6,000 one-time
- Performance: 100% (baseline)
- Break-even: After 60 plugin sales at $100 profit each

**Option B: KissFFT (BSD)**
- Cost: $0 licensing
- Performance: 55% of FFTW
- Trade-off: Acceptable latency for most effects (`<1`ms per 512-sample FFT)

**Verdict:** Many indie developers choose KissFFT (avoid upfront cost, speed is adequate).

---

## Implementation Reality

### What to Expect in First 90 Days

**Week 1-2: Learning and prototyping**
- Python (scipy.fft): ✅ Production-ready code in days
- C (FFTW): ⚠️ Still learning API, plan management
- Embedded (KissFFT): ⚠️ Integration, testing on hardware

**Week 3-6: Integration and optimization**
- Python: Fine-tuning (buffer sizes, windowing)
- C: Profiling, memory layout optimization
- Embedded: Flash/RAM optimization, fixed-point tuning

**Week 7-12: Production hardening**
- Validation (FFT produces expected results)
- Edge case handling (zero-length signals, NaN inputs)
- Performance verification (meets latency requirements)

### Common Pitfalls

**1. Premature optimization**
- **Mistake:** Choosing pyFFTW without profiling
- **Reality:** scipy.fft fast enough, FFT is `<5`% of runtime
- **Fix:** Profile first, optimize only if bottleneck

**2. Ignoring power-of-2 sizes**
- **Mistake:** FFT on 1000 samples (factors: 2³ × 5³)
- **Reality:** 3-5x slower than 1024 (2¹⁰)
- **Fix:** Pad to next power-of-2 if performance matters

**3. Using complex FFT on real data**
- **Mistake:** `fft(real_signal)` computes 1024 complex outputs
- **Reality:** `rfft(real_signal)` exploits symmetry → 513 outputs, 2x faster
- **Fix:** Use `rfft()` for real-valued signals

**4. Not validating results**
- **Mistake:** Assume FFT is correct
- **Reality:** FFTs can fail (NaN inputs, size mismatches)
- **Fix:** Verify Parseval's theorem (energy conservation), test with sine waves

### Team Skill Requirements

**Minimal (scipy.fft):**
- Python basics (NumPy arrays)
- Understanding of frequency domain (high school physics)
- 1 day training for new team member

**Moderate (FFTW, pyFFTW):**
- C/C++ or Python intermediate
- Memory management (C) or plan lifecycle (pyFFTW)
- 1 week ramp-up

**Advanced (embedded, optimization):**
- Embedded C, fixed-point arithmetic
- DSP fundamentals (windowing, spectral leakage)
- 2-4 weeks for junior developer

---

## Decision Flowchart

```
What's your environment?
├─ Python
│  ├─ Exploration → scipy.fft ✅
│  └─ Performance-critical
│     ├─ Profile: FFT < 10% runtime → scipy.fft ✅
│     └─ Profile: FFT > 20% runtime → pyFFTW
│
├─ C/C++
│  ├─ Desktop/server → FFTW ✅
│  ├─ Embedded → KissFFT ✅
│  └─ GPL problem → KissFFT OR buy FFTW license
│
└─ Embedded systems
   ├─ ARM with FPU → KissFFT ✅
   ├─ ARM without FPU → KissFFT (fixed-point)
   └─ Hardware FFT available → Use hardware!
```

---

## Key Takeaways

1. **For most Python projects:** scipy.fft is the answer (simple, fast enough, maintained)

2. **For C/C++ projects:** FFTW is standard (unless GPL is problem → KissFFT)

3. **For embedded systems:** KissFFT wins (simple, portable, BSD)

4. **Performance matters less than you think:** scipy.fft is 90% of FFTW speed, and FFT is often `<10`% of total runtime

5. **Profile before optimizing:** Don't use pyFFTW unless scipy.fft is proven bottleneck

6. **Licensing matters:** GPL (FFTW) is fine for research/internal tools, but problematic for commercial distribution

7. **Simplicity has value:** KissFFT is 50% slower than FFTW, but 10x simpler. Often worth the trade-off.

---

## Further Reading

- **Discovery research:** See `01-discovery/DISCOVERY_TOC.md` for full technical analysis
- **S1 (Rapid):** Quick library comparison and decision matrix
- **S2 (Comprehensive):** Deep technical dive (algorithms, performance)
- **S3 (Need-Driven):** Use case personas (audio, data science, embedded, HPC, ML)
- **S4 (Strategic):** Long-term viability and risk analysis
