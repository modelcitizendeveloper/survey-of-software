# Cost Comparison Example

## Scenario
Processing 1 million Chinese sentences/month

## Cloud (Google NLP API)
- ~$1-2 per 1000 syntax requests
- Monthly cost: $1,000-2,000
- Zero infrastructure cost
- No maintenance burden

## Self-Hosted (HanLP on cloud VM)
- VM with GPU: ~$300-500/month
- Developer time: ~8-16 hours/month setup/maintenance
- Cost per sentence: negligible after setup
- Monthly cost: $300-500 + developer time

## Break-even Point
Around 500K-1M sentences/month, self-hosted becomes cheaper.
