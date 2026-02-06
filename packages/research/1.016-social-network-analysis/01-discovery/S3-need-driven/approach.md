# S3-Need-Driven: Social Network Analysis Libraries

## Research Approach

**Question**: Who needs social network analysis, and why?

**Philosophy**: Start with requirements, find exact-fit solutions. Different users need different libraries based on their specific contexts, constraints, and goals.

**Methodology**:
1. Identify distinct user personas with network analysis needs
2. Document their specific requirements and constraints
3. Map requirements to library capabilities
4. Recommend best-fit solutions per persona

**Output**: Requirement → library mapping for decision validation

## S3 Focus: WHO + WHY, Not HOW

**✅ Covered**:
- User personas and their contexts
- Why they need network analysis
- What constraints they face (scale, budget, expertise)
- Which library fits their needs best

**❌ NOT Covered**:
- Implementation details
- Code examples
- Installation tutorials
- How-to guides

S3 validates library choice against real-world requirements.

## User Personas Analyzed

1. **Data science researchers** - Academic research on social phenomena
2. **Network infrastructure engineers** - Production monitoring and optimization
3. **Bioinformatics researchers** - Protein interaction and gene networks
4. **Security analysts** - Fraud detection and threat networks
5. **Product analysts** - User engagement and viral growth

## Selection Criteria by Persona

### Data Science Researchers
- **Priority**: Comprehensive algorithms, reproducibility
- **Scale**: 10K-1M nodes typically
- **Constraint**: Publication deadlines, exploratory workflow

### Network Engineers
- **Priority**: Reliability, speed, real-time analysis
- **Scale**: 100K-10M nodes (infrastructure graphs)
- **Constraint**: SLAs, uptime requirements

### Bioinformatics
- **Priority**: Statistical rigor, advanced community detection
- **Scale**: 1M-100M nodes (omics data)
- **Constraint**: Complex analysis, peer review standards

### Security Analysts
- **Priority**: Speed, pattern detection, scalability
- **Scale**: Millions of events → graphs
- **Constraint**: Real-time threat detection

### Product Analysts
- **Priority**: Ease of integration, visualization
- **Scale**: 10K-1M users typically
- **Constraint**: Fast iteration, A/B testing
