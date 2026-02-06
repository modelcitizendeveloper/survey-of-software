# Use Case: Code Review & Generation Pipeline

## Scenario

Software development team wants AI-assisted code generation and review:
- Generate boilerplate code from requirements
- Review PRs for bugs, style violations, security issues
- Suggest improvements and optimizations
- Generate tests and documentation

## Requirements

### Must-Have
- ✅ Requirements → code generation
- ✅ Code review with multi-aspect analysis (bugs, style, security)
- ✅ Test generation
- ✅ Documentation generation
- ✅ Integration with GitHub/GitLab

### Nice-to-Have
- Architecture design suggestions
- Competitive analysis of similar features
- Performance optimization recommendations

### Constraints
- Python/JavaScript/TypeScript primary languages
- GitHub Actions integration
- Cost <$5 per PR review

## Framework Evaluation

| Requirement | MetaGPT | CrewAI | AutoGen |
|-------------|---------|--------|---------|
| Req → Code | ✅ Native (SOP-driven) | ✅ Proven (PwC: 10→70%) | ✅ Tool calling |
| Code Review | ✅ Multi-aspect (PM, architect review) | ✅ Role-based reviewers | ✅ Conversation-based |
| Test Generation | ✅ Core capability | ✅ Via tools | ✅ Via tools |
| Documentation | ✅ Automatic output | ✅ Writer agent | ✅ Agent task |
| GitHub Integration | ⚠️ Manual setup | ✅ Tool ecosystem | ✅ Tool ecosystem |
| **Fit Score** | **90%** | **95%** | **80%** |

## Recommendation

**Winner: MetaGPT** (for greenfield code generation)
**Runner-up: CrewAI** (for existing codebase PR review, proven 10→70% accuracy at PwC)

**Rationale:**
- MetaGPT specializes in complete project generation (req → code → docs)
- CrewAI proven in production code generation (PwC deployment)
- AutoGen flexible but requires more setup

**When to Choose:**
- **MetaGPT:** Generating new projects/features from scratch
- **CrewAI:** PR review workflows, existing codebase maintenance
- **AutoGen:** Complex, unpredictable code generation tasks

**Proven Evidence:** PwC boosted code-generation accuracy from 10% to 70% using CrewAI.
