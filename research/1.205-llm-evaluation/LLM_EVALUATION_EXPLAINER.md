# LLM Evaluation: A Domain Explainer

## What is LLM Evaluation?

LLM evaluation is the systematic measurement of language model outputs against quality criteria. Unlike traditional software testing with deterministic pass/fail outcomes, LLM evaluation deals with probabilistic outputs where "correct" is often subjective or context-dependent.

**The core challenge:** Given the same input, an LLM might produce different outputs each time, and multiple outputs could all be "acceptable." Evaluation frameworks help quantify quality across dimensions like accuracy, relevance, safety, and coherence.

## Why Evaluation is Hard

### The Ground Truth Problem
Traditional testing compares output to expected values. LLM outputs rarely have single correct answers:
- "Summarize this article" → Many valid summaries exist
- "Answer this question" → Phrasing, completeness, and tone all vary
- "Generate code for X" → Multiple correct implementations possible

### The Scale Problem
Manual review doesn't scale. A production LLM application might handle thousands of requests daily. Human evaluation of every response is impractical.

### The Drift Problem
LLM behavior changes over time—model updates, prompt modifications, and context variations all affect output quality. Continuous evaluation is necessary to catch regressions.

## Evaluation Approaches

### 1. Reference-Based Evaluation
Compare outputs against known good answers using traditional NLP metrics.

**Metrics:**
- **BLEU**: N-gram overlap with reference text (originally for translation)
- **ROUGE**: Recall-oriented overlap (originally for summarization)
- **Exact Match**: Binary match against expected output

**Limitations:** Penalizes valid paraphrases. "The cat sat on the mat" and "A feline rested upon the rug" score poorly against each other despite similar meaning.

### 2. LLM-as-Judge
Use another LLM to evaluate outputs. The evaluator LLM receives the input, output, and a rubric, then scores the response.

**How it works:**
```
System: You are an evaluation assistant. Score the following response
on a scale of 1-5 for helpfulness, accuracy, and clarity.

Input: [user question]
Output: [model response]
Rubric: [scoring criteria]
```

**Advantages:**
- Handles semantic equivalence (understands paraphrases)
- Scales to large volumes
- Can evaluate subjective qualities (tone, helpfulness)

**Limitations:**
- Costs money (API calls for evaluation)
- Judge LLM has its own biases
- Can be gamed (outputs that "sound good" but are wrong)

### 3. Programmatic/Heuristic Evaluation
Code-based checks for specific criteria.

**Examples:**
- JSON validity for structured outputs
- Regex patterns for format compliance
- Length constraints
- Profanity/PII detection
- Citation presence in RAG outputs

**Advantages:** Fast, deterministic, no API costs

**Limitations:** Only catches specific, predictable issues

## The RAG Triad

For Retrieval-Augmented Generation (RAG) systems, three metrics form the foundational evaluation framework:

```
┌─────────────┐     retrieves     ┌─────────────┐
│   Query     │ ───────────────→  │  Context    │
└─────────────┘                   └─────────────┘
                                        │
                                        │ generates
                                        ▼
                                  ┌─────────────┐
                                  │   Answer    │
                                  └─────────────┘
```

### 1. Context Relevance
**Question:** Is the retrieved context relevant to the query?

Measures retrieval quality. If your vector search returns irrelevant documents, the LLM can't produce good answers regardless of its capabilities.

**Low score means:** Fix your retrieval (embeddings, chunking, search parameters)

### 2. Faithfulness (Groundedness)
**Question:** Is the answer supported by the retrieved context?

Measures hallucination. The LLM should only state things present in the provided context, not invent information.

**Low score means:** The model is hallucinating or over-generalizing

### 3. Answer Relevance
**Question:** Does the answer actually address the query?

Measures response quality. Even with good context and no hallucination, the answer might miss the point or be incomplete.

**Low score means:** Prompt engineering needed, or model limitations

## Metric Taxonomy

### Correctness Metrics
- **Factual accuracy**: Are stated facts true?
- **Faithfulness**: Is output grounded in provided context?
- **Hallucination rate**: How often does the model invent information?

### Relevance Metrics
- **Answer relevance**: Does output address the input?
- **Context relevance**: Is retrieved context pertinent?
- **Completeness**: Are all aspects of the query addressed?

### Quality Metrics
- **Coherence**: Is the output logically structured?
- **Fluency**: Is the language natural and grammatical?
- **Conciseness**: Is the output appropriately brief?

### Safety Metrics
- **Toxicity**: Does output contain harmful content?
- **Bias**: Does output show unfair preferences?
- **PII leakage**: Does output expose personal information?
- **Jailbreak resistance**: Does the model refuse harmful requests?

### Task-Specific Metrics
- **Code correctness**: Does generated code execute properly?
- **SQL validity**: Is generated SQL syntactically correct?
- **Tool use accuracy**: Did the agent call the right tools with right parameters?

## Evaluation vs Observability

These terms are often conflated but serve different purposes:

| Aspect | Evaluation | Observability |
|--------|------------|---------------|
| **Purpose** | Measure quality | Monitor operations |
| **When** | Development, CI/CD, batch | Production, real-time |
| **Focus** | "Is the output good?" | "Is the system healthy?" |
| **Metrics** | Faithfulness, relevance | Latency, errors, costs |
| **Tools** | DeepEval, Ragas | LangSmith, Datadog |

**Observability** tells you the system is running. **Evaluation** tells you it's running well.

In practice, production systems need both:
- Observability catches outages, latency spikes, error rates
- Evaluation catches quality degradation, hallucination increases, relevance drift

## Self-Explaining Metrics

A key differentiator among evaluation tools is whether metrics are self-explaining.

**Non-explaining metric:**
```
Faithfulness Score: 0.4
```
Why is it 0.4? Which claims weren't grounded? Unclear.

**Self-explaining metric:**
```
Faithfulness Score: 0.4
Reason: The response claims "revenue increased 50%" but the context
only states "revenue showed growth." The specific percentage is not
supported by the retrieved documents.
```

Self-explaining metrics dramatically reduce debugging time by pointing directly to the problem.

## Evaluation Pipeline Architecture

A typical evaluation setup:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Test Cases  │ ──→ │  LLM App     │ ──→ │  Evaluators  │
│  (Dataset)   │     │  (Target)    │     │  (Metrics)   │
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
                                                 ▼
                                          ┌──────────────┐
                                          │   Results    │
                                          │  Dashboard   │
                                          └──────────────┘
```

### Components

**Test Cases (Dataset)**
Curated inputs with optional expected outputs or evaluation criteria. Good datasets cover:
- Happy path scenarios
- Edge cases
- Adversarial inputs
- Domain-specific examples

**Evaluators**
Functions that score outputs. Can be:
- LLM-as-judge (semantic evaluation)
- Programmatic (format, length, patterns)
- Human-in-the-loop (gold standard, expensive)
- Composite (multiple metrics combined)

**Results Dashboard**
Aggregates scores across test runs. Enables:
- Regression detection (quality dropped after change)
- A/B comparison (which prompt is better?)
- Trend analysis (quality over time)

## Common Evaluation Mistakes

### 1. Evaluating Too Late
Testing only before deployment misses production drift. Implement continuous evaluation on sampled production traffic.

### 2. Single Metric Fixation
Optimizing for one metric (e.g., relevance) can tank others (e.g., safety). Use balanced metric sets.

### 3. Insufficient Test Coverage
A few dozen test cases won't catch edge cases. Aim for hundreds covering diverse scenarios.

### 4. Ignoring Evaluator Bias
LLM judges have preferences. Validate judge outputs against human ratings periodically.

### 5. Static Datasets
Real user queries evolve. Continuously expand test cases from production samples.

## Cost Considerations

Evaluation has direct costs:

| Approach | Cost Driver | Approximate Cost |
|----------|-------------|------------------|
| LLM-as-Judge (GPT-4) | API calls | $0.01-0.05 per eval |
| LLM-as-Judge (GPT-3.5) | API calls | $0.001-0.005 per eval |
| Programmatic | Compute | Negligible |
| Human Review | Labor | $0.10-1.00 per eval |

**Cost optimization strategies:**
- Use cheaper models for initial filtering, expensive for edge cases
- Cache evaluation results for identical outputs
- Sample production traffic rather than evaluating everything
- Use programmatic checks where possible

## When to Invest in Evaluation

**Minimal evaluation (just starting):**
- Manual spot checks
- Basic programmatic checks (format, length)
- A few dozen test cases

**Moderate evaluation (production app):**
- Automated test suite in CI/CD
- LLM-as-judge for key metrics
- Hundreds of test cases
- Basic dashboard

**Comprehensive evaluation (critical application):**
- Continuous production evaluation
- Multiple metric coverage (correctness, safety, quality)
- Thousands of test cases
- Regression alerts
- Human-in-the-loop for edge cases

## Glossary

**Chain-of-Thought (CoT)**: Prompting technique where the model shows reasoning steps. Can improve both generation and evaluation accuracy.

**Few-Shot Evaluation**: Providing example evaluations to guide the judge LLM's scoring.

**Golden Dataset**: Curated test cases with human-verified expected outputs or scores.

**Hallucination**: When an LLM generates information not present in its context or training data.

**Red Teaming**: Adversarial testing to find vulnerabilities, jailbreaks, or failure modes.

**Rubric**: Scoring criteria provided to an LLM judge explaining how to rate responses.

**Synthetic Data**: Machine-generated test cases, often used to expand coverage cheaply.
