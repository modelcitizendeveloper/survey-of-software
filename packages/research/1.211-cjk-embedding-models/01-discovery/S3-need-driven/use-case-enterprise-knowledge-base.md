# Use Case 5: Enterprise Knowledge Base (Mixed CJK-English)

## Business Context

**Industry**: Tech companies, multinational enterprises
**Application**: Internal wiki, document search, corporate knowledge management
**Scale**: 50K-500K documents, 1K-10K daily searches (company-wide)
**Languages**: Mixed Chinese-English (code-switching common)
**Constraints**: Self-hosted (data privacy), domain-specific terminology

## Technical Requirements

- **Code-Switching**: Handle mixed Chinese-English (e.g., "这个API的authentication流程")
- **Domain Terminology**: Engineering, business, product-specific terms
- **Privacy**: Self-hosted on-premise or private cloud
- **Quality**: High (incorrect results reduce productivity)
- **Integration**: Confluence, Notion, SharePoint, or custom wiki

## Model Evaluation

**Winner: multilingual-e5-base (fine-tuned on internal corpus)**

| Model | Code-Switching | Fine-Tuning Support | Self-Hosted | Chinese+English |
|-------|----------------|---------------------|-------------|-----------------|
| multilingual-e5-base | ★★★★ (79.8) | Excellent | ✓ | ★★★★★ |
| M3E-base | ★★ (degrades >30% EN) | Good | ✓ | ★★★ (CN focus) |
| LaBSE | ★★★ (moderate) | Limited | ✓ | ★★★★ |

**Rationale**: multilingual-e5 handles code-switching better than M3E (unified tokenizer). Fine-tuning on internal corpus critical for domain terminology.

**Why not M3E**: Degrades significantly when English content >30% (common in tech companies).

## Deployment Architecture

```
[Employee Search Query]
        ↓
[multilingual-e5-base (fine-tuned)]
(On-premise: 2x NVIDIA A10, Kubernetes cluster)
        ↓
[Weaviate Vector DB]
- 200K internal documents (768-dim)
- Metadata: department, classification, author
- Hybrid search (vector + keyword for acronyms)
        ↓
[Access Control Layer]
(Filter results by employee permissions)
        ↓
[Top-10 Results] → [Preview + Link to Source]
```

## TCO Analysis (200K Documents, 5K Searches/Day)

**Infrastructure** (On-Premise):
- 2x NVIDIA A10 GPUs (amortized): $3K/GPU × 2 = $6K ÷ 36 months = **$167/month**
- Server hardware (64-core CPU, 256GB RAM): $15K ÷ 36 months = **$417/month**
- **Total hardware**: $584/month (amortized)

**Software**:
- Weaviate (open-source, self-hosted): $0
- Kubernetes (existing infrastructure): $0
- **Total software**: $0/month

**Operations**:
- DevOps maintenance: 10 hours/month × $100/hour = **$1,000/month**
- **Total operations**: $1,000/month

**Total TCO**: **$1,584/month** ($0.01 per search)

## Fine-Tuning for Domain Adaptation

**Training Data**:
- 50K internal document pairs (titles + summaries)
- 20K query-document pairs from search logs
- Total: 70K training pairs

**Training Method**: LoRA fine-tuning on multilingual-e5-base
**Training Cost**: $50 (8 hours on A100)
**Expected Improvement**: +8-12% relevance on domain-specific queries

**Example Domain Terms**:
- "PRD" (Product Requirements Document)
- "OKR" (Objectives and Key Results)
- "Tech Spec" mixed with Chinese explanations
- Internal codenames, product names

**Baseline vs Fine-Tuned**:
- Baseline: 62% relevance on internal eval set
- Fine-tuned: 74% relevance (+12 pts)

## Implementation Timeline

**Week 1-2**: Data preparation (extract 200K docs from Confluence/Notion)
**Week 3-4**: Deploy Weaviate cluster, embed documents with base model
**Week 5**: Fine-tune multilingual-e5 on internal corpus (70K pairs)
**Week 6**: Deploy fine-tuned model, A/B test vs keyword search
**Week 7-8**: Roll out to entire company, gather feedback, iterate

**Total**: 8 weeks to production

## ROI Calculation

**Employee Productivity Gains**:
- 1,000 employees × 5 searches/day × 220 workdays = 1.1M searches/year
- Assume 10% of searches save 5 minutes (better results)
- Time saved: 110K searches × 5 min = 550K minutes = 9,167 hours
- Value: 9,167 hours × $50/hour (blended rate) = **$458K/year**

**Cost**:
- TCO: $1,584/month × 12 = **$19K/year**
- Fine-tuning: $50 (one-time)
- Implementation: $40K (developer time)
- **Total Year 1**: $59K

**ROI**: ($458K - $59K) / $59K = **676% first year**
**Payback Period**: ~1.5 months

## Risk & Mitigation

**Risk 1: Data Privacy Concerns**
- **Mitigation**: Self-hosted on-premise, no external APIs
- **Compliance**: GDPR, SOC2 compliant (no data leaves infrastructure)

**Risk 2: Access Control Bypass**
- **Mitigation**: Filter vector search results through existing access control layer
- **Security Audit**: Quarterly penetration testing

**Risk 3: Fine-Tuned Model Overfits to Current Terminology**
- **Mitigation**: Quarterly re-training as company evolves
- **Monitoring**: Track relevance metrics, trigger re-training if degradation

## Recommendation

**Model**: multilingual-e5-base (fine-tuned on internal corpus)
**Deployment**: On-premise (self-hosted Weaviate + Kubernetes)
**Fine-Tuning**: Yes (70K internal pairs, $50 cost, +12% relevance)
**TCO**: $1,584/month ($19K/year)
**ROI**: 676% first year ($458K productivity gains)
**Timeline**: 8 weeks to production
**Confidence**: High (proven approach, clear ROI)

**Key Success Factor**: Fine-tuning on internal corpus essential. Off-the-shelf models insufficient for domain-specific terminology.
