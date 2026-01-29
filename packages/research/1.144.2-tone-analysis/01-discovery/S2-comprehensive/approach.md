# S2 Comprehensive Pass: Approach

## Objective
Deep-dive investigation of tone analysis technologies, including:
- Complete API and feature analysis of Parselmouth, librosa, and praatio
- Performance benchmarking and accuracy studies
- Tone classification algorithms (HMM, CNN, LSTM)
- Tone sandhi detection approaches
- Comparative analysis for production deployment

## Research Method
- Systematic web search for 2026 documentation and research papers
- Academic literature review (arXiv, ResearchGate, ScienceDirect)
- Official documentation analysis
- GitHub repository exploration
- Performance benchmark comparisons
- Code example synthesis

## Scope Expansion from S1
S1 identified three libraries (Parselmouth, librosa, praatio). S2 expands to:
1. **Pitch detection**: Deep dive into Parselmouth, librosa, CREPE, PESTO
2. **Tone classification**: HMM, GMM, CNN, RNN, LSTM, hybrid architectures
3. **Tone sandhi**: Rule-based, ML-based, hybrid approaches
4. **Complete feature matrix**: All tools × all capabilities
5. **Production guidance**: Performance, cost, deployment considerations

## Documents Created

1. **01-parselmouth-deep-dive.md** - Complete API, benchmarks, examples
2. **02-librosa-advanced.md** - Algorithm comparison, parameter tuning, accuracy
3. **03-praatio-textgrid-manipulation.md** - TextGrid API, batch processing
4. **04-tone-classification-algorithms.md** - HMM to CNN-LSTM-Attention
5. **05-tone-sandhi-detection.md** - Mandarin rules, ML models, hybrid systems
6. **06-comparative-analysis.md** - Performance metrics, decision tree, cost analysis
7. **README.md** - Navigation guide and quick reference

## Key Questions Answered

1. **Accuracy**: How do tools compare?
   - Parselmouth: r=0.999 with Praat
   - librosa pYIN: r=0.730 for F0 mean
   - CREPE: State-of-the-art deep learning

2. **Performance**: Speed and resource requirements?
   - Parselmouth/librosa: 2-3s per file
   - CREPE GPU: 0.4-1s per file
   - PESTO: <10ms latency (real-time)

3. **Tone classification**: Best algorithms?
   - CNN-LSTM-Attention: 90%+ accuracy
   - CNN (ToneNet): 87-88% accuracy
   - RNN: 88-90% accuracy (implicit sandhi learning)

4. **Tone sandhi**: How to detect?
   - Rule-based: 88-97% accuracy
   - CNN: 97%+ accuracy
   - Hybrid (Rules + CNN): Best precision

5. **Production stack**: What to deploy?
   - Parselmouth (pitch) + CNN (tones) + Rule+CNN (sandhi)
   - Cost: ~$12K Year 1
   - Accuracy: 87-88% tones, 97%+ sandhi

## Methodology Notes

- All sources cited with hyperlinks in each document
- Code examples provided for reproducibility
- Comparison tables for quick decision-making
- Trade-off analysis for different deployment scenarios
- Cost-benefit calculations included

## Time Investment
Comprehensive research completed across 7 documents totaling 157 KB.
