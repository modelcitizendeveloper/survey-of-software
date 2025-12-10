# PromptFoo

## Overview
- **Type**: Open-source CLI and library
- **License**: MIT
- **GitHub**: 51,000+ developers
- **Focus**: Prompt testing, A/B testing, red teaming

## Key Features
- **CLI-first**: Simple command-line interface, no cloud required
- **YAML configuration**: Declarative test case definition
- **Side-by-side comparison**: Diff views for prompt variations
- **Red teaming**: Automated security testing (injections, toxic content)
- **CI/CD ready**: Integrates into deployment pipelines

## Supported Providers
- OpenAI, Anthropic, Azure, Google, HuggingFace
- Open-source models (Llama, etc.)
- Custom API providers

## Evaluation Capabilities
- Basic RAG metrics
- Safety/security testing
- LLM-as-judge evaluations
- Custom assertion logic

## Limitations
- Limited metric set compared to DeepEval (basic RAG + safety only)
- YAML-heavy workflow harder to customize at scale
- Less comprehensive than code-first alternatives

## Best For
- Quick prompt iterations
- Security/red team testing
- Teams preferring declarative config over code
- Lightweight experimentation without SDK dependencies

## Installation
```bash
npm install -g promptfoo
# or
npx promptfoo@latest
```

## Pricing
- **Open-source**: Free, self-hosted
- **Cloud**: Optional hosted dashboard
