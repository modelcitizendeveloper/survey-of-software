# Use Case 2: Multilingual Customer Support

## Business Context

**Industry**: Global SaaS, Enterprise Software
**Application**: Automated ticket routing, knowledge base search
**Scale**: 10K-100K support tickets/month
**Languages**: Chinese (Simplified & Traditional), Japanese, Korean, English
**User Expectations**: Accurate ticket classification, relevant KB article suggestions

## Technical Requirements

- **Languages**: CJK + English (mandatory multilingual)
- **Latency**: <500ms acceptable (not real-time)
- **Quality**: High (wrong routing costs agent time)
- **Integration**: LangChain RAG pipeline (existing infrastructure)

## Model Evaluation

**Winner: multilingual-e5-base**

| Model | CJK Support | English Support | LangChain Integration | Score |
|-------|-------------|-----------------|----------------------|-------|
| multilingual-e5-base | ★★★★★ | ★★★★★ | Native | Best |
| LaBSE | ★★★★ | ★★★★★ | Compatible | Good |
| M3E-base | ★★★★★ (CN only) | ★★ | Compatible | Poor (no J/K) |

**Rationale**: Only multilingual-e5 and LaBSE handle all CJK languages + English. multilingual-e5 newer, better benchmarks, active development.

## Deployment Architecture

```
[Ticket Submission] → [LangChain RAG Pipeline]
                              ↓
              [Embeddings: multilingual-e5-base]
              (Hosted on AWS SageMaker, 2x ml.g4dn.xlarge)
                              ↓
              [Vector DB: Pinecone (managed)]
              - 50K KB articles (768-dim embeddings)
              - Metadata filtering (language, category)
                              ↓
              [Retrieved Context] → [LLM (GPT-4/Claude)]
              → [Suggested Response + Routing]
```

## TCO Analysis (50K Tickets/Month)

- **Embedding Service** (SageMaker): 2x ml.g4dn.xlarge × $0.526/hour × 720h = **$757/month**
- **Vector DB** (Pinecone): 1 pod (50K vectors) = **$70/month**
- **LLM Calls** (GPT-4): 50K tickets × $0.03/ticket = **$1,500/month**
- **Total**: **$2,327/month** ($0.047 per ticket)

**Alternative** (Commercial Embedding API):
- OpenAI embeddings: 50K tickets × 200 tokens avg × $0.0001/1K tokens = **$1/month** (negligible)
- But: Vendor lock-in, data privacy concerns (customer data)

**Recommendation**: Self-host for data privacy, negligible cost difference for embeddings vs LLM costs.

## Fine-Tuning Strategy

- **Training Data**: 10K labeled tickets (issue type, routing, resolution)
- **Method**: Fine-tune multilingual-e5 on ticket-article pairs
- **Expected Improvement**: +8% routing accuracy, +12% KB article relevance
- **Cost**: $30 (one-time training)

## Implementation Timeline

- **Week 1**: Integrate multilingual-e5 into existing LangChain pipeline
- **Week 2**: Migrate KB articles to Pinecone (embed 50K articles)
- **Week 3**: A/B test vs existing system (20% traffic)
- **Week 4**: Full rollout + monitoring

## Recommendation

**Model**: multilingual-e5-base
**Deployment**: AWS SageMaker + Pinecone
**TCO**: $2,327/month ($0.047/ticket)
**ROI**: 15-20% reduction in average handle time = $5K/month savings (assuming $25/hour agent cost)
**Payback**: <1 month
