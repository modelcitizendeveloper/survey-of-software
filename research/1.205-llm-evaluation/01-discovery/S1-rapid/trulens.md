# TruLens

## Overview
- **Type**: Open-source Python library
- **License**: MIT
- **Maintainer**: Snowflake (acquired TruEra)
- **Focus**: Feedback functions and tracing for LLM apps

## Key Features
- **Feedback functions**: Programmatic evaluation without ground truth
- **RAG Triad pioneer**: Original structured RAG evaluation framework
- **OpenTelemetry support**: Interoperable observability
- **Extensible**: Custom feedback function framework
- **Provider integrations**: OpenAI, HuggingFace, LiteLLM, LangChain

## Feedback Function Types
- **Generation-based**: LLM-as-judge with rubrics
- **Custom logic**: Tailored evaluation tasks
- **Chain-of-thought**: Optional reasoning traces
- **Few-shot**: Example-guided evaluation

## Tracing Capabilities
- OpenTelemetry (OTel) native
- Integrates with existing observability stack
- Detailed execution traces
- Performance monitoring

## Supported Use Cases
- Question-answering
- Summarization
- RAG systems
- Agent-based applications

## Limitations
- Snowflake acquisition may affect roadmap
- Overlaps with Ragas on RAG evaluation
- Less comprehensive metrics than DeepEval
- Community-driven, less commercial support

## Best For
- Teams already using OpenTelemetry
- Snowflake ecosystem users
- Custom feedback function needs
- RAG evaluation with extensibility

## Installation
```bash
pip install trulens
```

## Pricing
- **Open-source**: Free
