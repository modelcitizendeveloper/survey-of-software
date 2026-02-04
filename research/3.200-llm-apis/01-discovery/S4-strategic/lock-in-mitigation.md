# S4-Strategic: LLM API Lock-In Mitigation Strategies

**Experiment**: 3.200 LLM APIs
**Stage**: S4 - Strategic Analysis
**Date**: November 6, 2025
**Focus**: 4-level framework for managing vendor lock-in risk

---

## Executive Summary

This document provides a strategic framework for managing LLM API vendor lock-in, with 4 mitigation levels ranging from accepting lock-in (for high-viability vendors) to full multi-provider architecture. Key findings:

- **No single "best" approach**: Lock-in acceptable for Google/Anthropic (high viability), unacceptable for Cohere/Mistral
- **Lightweight abstraction**: 20-40 hours engineering cost, useful for medium-risk providers
- **Full abstraction (LangChain)**: 10-20% performance overhead, enables provider independence
- **Multi-provider routing**: For mission-critical, high-volume applications (>$100K/month spend)

---

## 1. Lock-In Risk Assessment Framework

### 1.1 Defining Lock-In Severity

Lock-in occurs when switching providers creates switching costs that make alternative providers uneconomical. Severity depends on:

| Factor | Low Lock-In | Medium Lock-In | High Lock-In |
|--------|------------|----------------|-------------|
| **Integration points** | <2 (basic chat) | 2-5 (functions, caching) | 5+ (RAG, caching, vision) |
| **Provider-specific features** | None | 1-2 (prompt caching) | 3+ (caching + video + code execution) |
| **Code coupling** | Wrapper layer | Some native calls | Deep API integration |
| **Data dependency** | Portable | Mostly portable | Model-specific (fine-tuned) |
| **Switching cost** | <20 hours | 20-60 hours | 60-200+ hours |

### 1.2 Lock-In Severity by Provider (November 2025)

| Provider | Lock-In Severity | Primary Lock-In Driver | Switching Cost |
|----------|-----------------|----------------------|-----------------|
| **Anthropic** | 4/5 (High) | Prompt caching (90% cost savings) | 40-80 hours |
| **Google** | 3.5/5 (High) | 1M token context + video | 20-40 hours |
| **OpenAI** | 3/5 (Medium-High) | Ecosystem maturity, function calling | 20-40 hours |
| **Mistral** | 2/5 (Low) | OpenAI-compatible API | 10-20 hours |
| **Cohere** | 4.5/5 (Very High) | RAG pipeline (generation + embed + rerank) | 60-100 hours |
| **Meta Llama** | 1/5 (Very Low) | Open-source, multi-host options | 5-10 hours |

### 1.3 Cost of Lock-In vs. Mitigation Cost

**Lock-In Cost Calculation**:
```
Lock-In Cost = Switching Cost (hours) × Hourly Rate + Lost Productivity (months)
              + API Integration Rework + Testing + Downtime Risk

Example (Anthropic):
- Switching cost: 50 hours × $150/hour = $7,500
- Lost productivity: 0.5 months × $50K team cost = $25,000
- Integration rework: 30 hours × $150/hour = $4,500
- Risk buffer (downtime): $10,000
- Total lock-in cost: ~$47,000
```

**Mitigation Cost Calculation**:
```
Mitigation Cost = Development (hours) × Hourly Rate + Ongoing Overhead + Testing
                + Performance Impact (% cost increase)

Example (Lightweight abstraction):
- Development: 20 hours × $150/hour = $3,000
- Ongoing overhead: 5% code complexity = 2 hours/month = $1,200/year
- Testing: 10 hours × $150/hour = $1,500
- Year 1 cost: ~$5,700
- Year 3 cost (ongoing): 5% × API costs (assumes $5K/month) = $3,000/year
```

**Decision Rule**: If switching cost > 5× mitigation cost, implement mitigation strategy

---

## 2. Level 1: No Mitigation (Accept Lock-In)

### 2.1 When to Accept Lock-In

Accept lock-in if **all** of the following are true:

1. **Provider viability is very high** (>90% 10-year survival probability)
   - Example: Google, Anthropic, (OpenAI with Microsoft backing)
   - Rationale: Provider unlikely to fail, shut down, or lose competitiveness

2. **Lock-in severity is justified by feature value**
   - Anthropic prompt caching: 77-90% cost reduction (worth lock-in)
   - Google video understanding: 1M token context (unique capability)
   - Rationale: Feature advantage > switching cost risk

3. **API spend is small relative to total costs** (<$10K/month)
   - Rationale: Switching cost (~$50K) is bearable if provider fails
   - At $5K/month, switching cost = 10 months of API spend

4. **Exit strategy is pre-planned** (even if not implemented)
   - Backup provider identified
   - Rough migration timeline documented
   - Rationale: If viability assessment changes, can pivot quickly

### 2.2 Example: Anthropic Lock-In

**Why accept Anthropic lock-in**:
- Viability: 95% 5-year, 85-90% 10-year survival (very high)
- Feature value: Prompt caching saves 77-90% on cached prompts (massive)
- Example savings: $100K/month → $30K/month with caching (vs. OpenAI $80K/month)
- Lock-in is worth it: $70K/month savings >> $50K switching cost

**Implementation**:
```python
# Minimal wrapper around Anthropic SDK
import anthropic

class LLMClient:
    def __init__(self, provider="anthropic"):
        self.provider = provider
        if provider == "anthropic":
            self.client = anthropic.Anthropic()

    def generate(self, system, user_prompt, cached_context=None):
        """
        Generate response, optionally with cached context
        """
        messages = [{"role": "user", "content": user_prompt}]

        # Use prompt caching for repeated context
        system_content = system
        if cached_context:
            system_content = [
                {"type": "text", "text": system},
                {
                    "type": "text",
                    "text": cached_context,
                    "cache_control": {"type": "ephemeral"}
                }
            ]

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system=system_content,
            messages=messages
        )
        return response.content[0].text
```

### 2.3 Risk Management for Accepted Lock-In

Even when accepting lock-in, implement these safeguards:

| Safeguard | Implementation | Frequency |
|-----------|-----------------|-----------|
| **Provider health monitoring** | Track funding rounds, revenue reports, customer losses | Quarterly |
| **Backup provider exploration** | Maintain cost estimate for migration | Quarterly |
| **Feature parity assessment** | Identify which features have no alternative | Annually |
| **Contract leverage** | Negotiate SLAs, price locks, volume discounts | Annually |
| **Documentation** | Detailed integration guide for future migration | Ongoing |

### 2.4 Benefits and Limitations

**Benefits**:
- Zero complexity (use provider SDK natively)
- 0% performance overhead
- Access to all provider-specific features
- Fastest time-to-market

**Limitations**:
- Switching cost is $50K-200K
- Dependent on provider viability (small risk, but non-zero)
- No negotiating leverage (single-vendor dependence)
- Feature updates may not be backward-compatible

---

## 3. Level 2: Lightweight Abstraction (Partial Mitigation)

### 3.1 When to Use Lightweight Abstraction

Use lightweight abstraction if:

1. **Medium lock-in risk** (3-4/5 severity)
   - Example: OpenAI (feature-rich but not unique), Mistral, Google

2. **Access to unique features is needed**
   - Cannot sacrifice prompt caching (Anthropic), video (Google), function calling (all)
   - But willing to pay small performance cost (~5-10% latency)

3. **Switching cost acceptable** (20-40 hours)
   - Cost-benefit analysis favors mitigation (can switch providers within 1-2 weeks)

4. **Company size** (small-to-medium, <20 engineers working on AI)
   - Lighter overhead than full abstraction layer
   - Team can maintain simple wrapper

### 3.2 Lightweight Abstraction Architecture

**Core Concept**: Wrapper around provider SDK with conditional logic, no actual abstraction.

**Architecture Diagram**:
```
Application Code
       ↓
[Lightweight Wrapper Layer] ← Routes to provider, conditional logic
       ↓
[Provider-specific SDK] ← Anthropic, OpenAI, Google, Mistral
       ↓
LLM API
```

### 3.3 Implementation Example: Multi-Provider Wrapper

```python
# lightweight_llm_client.py
import anthropic
import openai
import google.generativeai as genai
from typing import Optional, List, Dict

class LLMProvider:
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"

class LLMClient:
    def __init__(self, provider: str = "anthropic", **config):
        self.provider_name = provider
        self.config = config

        if provider == self.ANTHROPIC:
            self.client = anthropic.Anthropic(api_key=config.get("api_key"))
            self.model = config.get("model", "claude-3-5-sonnet-20241022")

        elif provider == "openai":
            openai.api_key = config.get("api_key")
            self.model = config.get("model", "gpt-4o")

        elif provider == "google":
            genai.configure(api_key=config.get("api_key"))
            self.model = config.get("model", "gemini-1.5-pro")

    def generate(
        self,
        system_prompt: str,
        user_message: str,
        cached_context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate response from LLM.
        Supports provider-specific features via optional parameters.
        """

        if self.provider_name == self.ANTHROPIC:
            return self._generate_anthropic(
                system_prompt, user_message, cached_context, temperature, max_tokens
            )

        elif self.provider_name == self.OPENAI:
            return self._generate_openai(
                system_prompt, user_message, temperature, max_tokens
            )

        elif self.provider_name == self.GOOGLE:
            return self._generate_google(
                system_prompt, user_message, temperature, max_tokens
            )

    def _generate_anthropic(
        self,
        system_prompt: str,
        user_message: str,
        cached_context: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Anthropic-specific generation with prompt caching"""

        system_content = [{"type": "text", "text": system_prompt}]

        # Add cached context if provided
        if cached_context:
            system_content.append({
                "type": "text",
                "text": cached_context,
                "cache_control": {"type": "ephemeral"}
            })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_content,
            messages=[{"role": "user", "content": user_message}]
        )

        return response.content[0].text

    def _generate_openai(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """OpenAI-specific generation"""

        client = openai.OpenAI(api_key=self.config.get("api_key"))
        response = client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        return response.choices[0].message.content

    def _generate_google(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Google Gemini-specific generation"""

        model = genai.GenerativeModel(self.model)
        response = model.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": f"{system_prompt}\n\n{user_message}"}]}
            ],
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens
            }
        )

        return response.text

# Usage Example
if __name__ == "__main__":
    # Easy to swap providers by changing config
    providers = {
        "anthropic": {
            "api_key": "sk-ant-...",
            "model": "claude-3-5-sonnet-20241022"
        },
        "openai": {
            "api_key": "sk-proj-...",
            "model": "gpt-4o"
        }
    }

    # Production code stays the same, provider changes via config
    client = LLMClient(provider="anthropic", **providers["anthropic"])
    result = client.generate(
        system_prompt="You are a helpful assistant",
        user_message="What is 2+2?",
        cached_context="Math context for caching..."
    )
    print(result)

    # To switch to OpenAI:
    # client = LLMClient(provider="openai", **providers["openai"])
```

### 3.4 Benefits and Limitations

**Benefits**:
- ~5-10% performance overhead (minimal latency impact)
- Provider swap requires config change only (easy A/B testing)
- Access to all provider-specific features (prompt caching, function calling)
- Simple maintenance (wrapper is 200-400 lines of code)

**Limitations**:
- Still requires code changes for migration (20-40 hours, mostly testing)
- Doesn't abstract away API differences (developers must know each provider's quirks)
- Feature parity unclear (caching works differently on each provider)
- No automatic fallback (if provider down, no built-in retry to backup)

### 3.5 Migration Path Using Lightweight Abstraction

**Scenario: Migrate from OpenAI to Anthropic**

```python
# Current: Using OpenAI
client = LLMClient(provider="openai", api_key="sk-...", model="gpt-4o")

# Step 1: Switch to Anthropic in production (via config)
client = LLMClient(provider="anthropic", api_key="sk-ant-...", model="claude-3-5-sonnet")

# Step 2: Run comparative tests (Anthropic vs OpenAI)
openai_client = LLMClient(provider="openai", ...)
anthropic_client = LLMClient(provider="anthropic", ...)

test_cases = [...]
for test in test_cases:
    openai_result = openai_client.generate(...)
    anthropic_result = anthropic_client.generate(...)
    # Compare quality, latency, cost

# Step 3: Gradually migrate traffic (canary deployment)
# 10% to Anthropic, 90% to OpenAI → 50% / 50% → 100% Anthropic

# Step 4: Retire OpenAI integration after 2 weeks of validation
```

**Estimated Timeline**: 2-3 weeks for full migration (10-20 hours engineering)

---

## 4. Level 3: Full Abstraction Layer (Strong Mitigation)

### 4.1 When to Use Full Abstraction

Use full abstraction if:

1. **High lock-in risk** (4-5/5 severity) AND provider viability is uncertain
   - Example: Cohere (4.5/5 lock-in + 65-75% 10-year survival)

2. **Multi-provider strategy is required**
   - Primary provider + fallback provider
   - Want seamless failover without code changes

3. **Large engineering team** (10+ engineers, can maintain abstraction)
   - Abstraction layer adds complexity (~2 hours/week maintenance)
   - Requires careful documentation and training

4. **API spend is significant** ($50K+/month)
   - Performance overhead cost (<10% = $5K/month) acceptable
   - Switching cost savings justify investment

### 4.2 Full Abstraction Architecture: LangChain Example

**Core Concept**: Use mature framework (LangChain, LlamaIndex) for provider abstraction.

**Architecture Diagram**:
```
Application Code
       ↓
[LangChain / LlamaIndex] ← Provider-agnostic interface
       ↓
[Provider Modules] ← Anthropic, OpenAI, Google, Mistral (pluggable)
       ↓
LLM API
```

### 4.3 LangChain Implementation Example

```python
# Full abstraction using LangChain
from langchain.llms import Anthropic, OpenAI, GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming import StreamingStdOutCallbackHandler

class AbstractLLMClient:
    """
    Fully abstracted LLM client using LangChain.
    Supports swapping providers with zero application code changes.
    """

    def __init__(self, provider: str = "anthropic", **config):
        self.provider = provider
        self.config = config
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize provider-specific LLM"""

        if self.provider == "anthropic":
            return Anthropic(
                model="claude-3-5-sonnet-20241022",
                temperature=self.config.get("temperature", 0.7),
                max_tokens=self.config.get("max_tokens", 1000),
                api_key=self.config.get("api_key")
            )

        elif self.provider == "openai":
            return OpenAI(
                model_name="gpt-4o",
                temperature=self.config.get("temperature", 0.7),
                max_tokens=self.config.get("max_tokens", 1000),
                openai_api_key=self.config.get("api_key")
            )

        elif self.provider == "google":
            return GoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=self.config.get("temperature", 0.7),
                google_api_key=self.config.get("api_key")
            )

    def generate(self, system_prompt: str, user_message: str) -> str:
        """
        Generate response using unified LangChain interface.
        Works identically regardless of provider.
        """

        template = "{system_prompt}\n\nUser: {user_message}"
        prompt = PromptTemplate(
            input_variables=["system_prompt", "user_message"],
            template=template
        )

        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(
            system_prompt=system_prompt,
            user_message=user_message
        )

        return response

    def stream_generate(self, system_prompt: str, user_message: str):
        """Stream response token-by-token"""

        # LangChain provides unified streaming interface
        streaming_handler = StreamingStdOutCallbackHandler()

        template = "{system_prompt}\n\nUser: {user_message}"
        prompt = PromptTemplate(
            input_variables=["system_prompt", "user_message"],
            template=template
        )

        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            callbacks=[streaming_handler]
        )

        return chain.run(
            system_prompt=system_prompt,
            user_message=user_message
        )

# Example: Switch providers with config change only
providers_config = {
    "anthropic": {"api_key": "sk-ant-..."},
    "openai": {"api_key": "sk-proj-..."},
    "google": {"api_key": "AIza..."}
}

# Production code is completely provider-agnostic
def main(provider_name: str):
    client = AbstractLLMClient(
        provider=provider_name,
        **providers_config[provider_name]
    )

    result = client.generate(
        system_prompt="You are a helpful assistant",
        user_message="Explain quantum computing"
    )

    print(result)

# Call with any provider:
main("anthropic")  # Works identically
main("openai")     # Same code, different provider
main("google")     # Same code, different provider
```

### 4.4 Limitations of Full Abstraction

**Performance Overhead**:
- **Latency**: 10-20% increase (2-3x slower inference due to abstraction layer parsing)
- **Cost**: 5-10% higher API costs (LangChain retry logic, token recounting)
- **Reliability**: Potential bugs in LangChain adapter code (simpler than raw SDK)

**Feature Loss**:
- **Provider-specific features**: Prompt caching (Anthropic), token counting (OpenAI) may not work
- **Advanced features**: Computer use (Anthropic), video understanding (Google) not abstracted
- **Lowest common denominator**: Only features all providers support are available

**Maintenance Cost**:
- **LangChain updates**: Framework upgrades may break compatibility
- **Provider API changes**: When provider updates API, LangChain adapter needs update
- **Debugging**: Harder to debug when issues are in abstraction layer

### 4.5 Benefits of Full Abstraction

**Provider Independence**:
- Provider swap requires config change only (0-5 hours testing)
- Seamless fallback if primary provider fails
- No code changes, no recompilation, no deployment

**Risk Mitigation**:
- Lock-in risk effectively zero
- Can evaluate new providers without code changes
- Easy A/B testing (route 50% to Provider A, 50% to Provider B)

**Feature Consistency**:
- Unified logging, error handling, retry logic
- Consistent rate limiting across providers
- Built-in token counting for all providers

---

## 5. Level 4: Multi-Provider Architecture (Maximum Mitigation)

### 5.1 When to Use Multi-Provider Architecture

Use multi-provider architecture only if:

1. **Mission-critical application** (service outage = revenue loss)
   - Example: Customer support chatbot used by all customers
   - Downtime cost > API cost (10-100× relationship)

2. **Very large API spend** (>$100K/month)
   - Performance overhead cost acceptable ($10K-20K/month)
   - Can afford 2-3 parallel providers for resilience

3. **Lock-in is unacceptable** (strategic requirement)
   - Avoid single-vendor dependence
   - Want maximum optionality

4. **Large engineering team** (20+ engineers)
   - Complexity of routing, monitoring, cost allocation
   - Requires dedicated infrastructure team

### 5.2 Multi-Provider Architecture Design

**Core Concept**: Run multiple providers in production, route based on cost/latency/quality.

**Architecture Diagram**:
```
[User Request]
       ↓
[Request Router] ← Analyzes complexity, cost, latency requirements
       ↓
   ┌───┼───┬────────┐
   ↓   ↓   ↓        ↓
  [Simple] [Complex] [Long Context] [Video]
   Fast    Expensive  Large Context  Gemini
   Tier    Model      Model

   ↓ Llama    ↓ Claude  ↓ Google    ↓ Google
   ↓ Flash    ↓ Opus    ↓ Pro       ↓ Pro

   [Response Aggregation]
       ↓
   [Fallback Logic]
   (If primary fails, retry with backup)
       ↓
   [Cost/Performance Logging]
       ↓
   [User Response]
```

### 5.3 Multi-Provider Router Implementation

```python
# multi_provider_router.py
from enum import Enum
from typing import Optional, List
import logging
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai

class RequestComplexity(Enum):
    SIMPLE = "simple"      # Answer facts, simple classification
    MEDIUM = "medium"      # Reasoning, creative writing
    COMPLEX = "complex"    # Multi-step reasoning, analysis
    VISION = "vision"      # Image or video understanding

class ProviderConfig:
    """Configuration for provider selection strategy"""

    def __init__(self):
        self.providers = {
            "anthropic": {
                "client": None,
                "models": {
                    "fast": "claude-3-haiku-20240307",
                    "balanced": "claude-3-5-sonnet-20241022",
                    "powerful": "claude-3-opus-20240229"
                },
                "cost": {"fast": 0.25, "balanced": 3.00, "powerful": 15.00},
                "reliability": 0.99,
                "latency_ms": 500
            },
            "openai": {
                "client": None,
                "models": {
                    "fast": "gpt-3.5-turbo",
                    "balanced": "gpt-4o",
                    "powerful": "gpt-4"
                },
                "cost": {"fast": 0.50, "balanced": 5.00, "powerful": 30.00},
                "reliability": 0.98,
                "latency_ms": 800
            },
            "google": {
                "client": None,
                "models": {
                    "fast": "gemini-1.5-flash",
                    "balanced": "gemini-1.5-pro",
                    "powerful": "gemini-2.0"
                },
                "cost": {"fast": 0.075, "balanced": 1.25, "powerful": 5.00},
                "reliability": 0.97,
                "latency_ms": 400
            }
        }

class RequestRouter:
    """
    Routes requests to optimal provider based on:
    - Request complexity (simple → fast model, complex → powerful model)
    - Cost sensitivity (budget-conscious → cheapest provider)
    - Latency requirements (real-time → fastest provider)
    - Content type (video → Google only)
    """

    def __init__(self, api_keys: dict):
        self.config = ProviderConfig()
        self.api_keys = api_keys
        self.logger = logging.getLogger(__name__)
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize provider clients"""
        self.config.providers["anthropic"]["client"] = Anthropic(
            api_key=self.api_keys["anthropic"]
        )
        self.config.providers["openai"]["client"] = OpenAI(
            api_key=self.api_keys["openai"]
        )
        genai.configure(api_key=self.api_keys["google"])
        self.config.providers["google"]["client"] = genai

    def route_request(
        self,
        system_prompt: str,
        user_message: str,
        complexity: RequestComplexity,
        cost_priority: float = 0.3,  # 0.0 = quality only, 1.0 = cost only
        has_vision: bool = False,
        max_context_tokens: Optional[int] = None
    ) -> tuple[str, str, dict]:
        """
        Route request to optimal provider.

        Returns:
        - response: Generated text
        - provider: Which provider was used
        - metrics: Cost, latency, quality metrics
        """

        # Step 1: Determine required model tier
        model_tier = self._select_model_tier(complexity)

        # Step 2: Select optimal provider
        provider = self._select_provider(
            model_tier,
            cost_priority,
            has_vision,
            max_context_tokens
        )

        # Step 3: Generate response with fallback
        response, metrics = self._generate_with_fallback(
            provider,
            system_prompt,
            user_message,
            model_tier
        )

        # Step 4: Log metrics for cost optimization
        self._log_metrics(provider, metrics)

        return response, provider, metrics

    def _select_model_tier(self, complexity: RequestComplexity) -> str:
        """Select model tier based on complexity"""

        tier_map = {
            RequestComplexity.SIMPLE: "fast",
            RequestComplexity.MEDIUM: "balanced",
            RequestComplexity.COMPLEX: "powerful",
            RequestComplexity.VISION: "balanced"
        }
        return tier_map[complexity]

    def _select_provider(
        self,
        model_tier: str,
        cost_priority: float,
        has_vision: bool,
        max_context_tokens: Optional[int]
    ) -> str:
        """
        Select provider based on cost priority and requirements.

        Algorithm:
        1. If vision required: Google (only provider with native video)
        2. If cost_priority high (>0.7): Google (cheapest)
        3. If cost_priority medium (0.3-0.7): Anthropic (balanced cost/quality)
        4. If cost_priority low (<0.3): OpenAI (best quality)
        """

        # Vision is Google-only
        if has_vision:
            return "google"

        # Cost-based selection
        if cost_priority > 0.7:
            return "google"  # Cheapest
        elif cost_priority > 0.3:
            return "anthropic"  # Balanced
        else:
            return "openai"  # Best quality

    def _generate_with_fallback(
        self,
        provider: str,
        system_prompt: str,
        user_message: str,
        model_tier: str
    ) -> tuple[str, dict]:
        """
        Generate response with automatic fallback to secondary provider.

        Fallback sequence:
        - Primary fails → Secondary provider
        - Secondary fails → Tertiary provider
        - All fail → Return error
        """

        fallback_sequence = {
            "anthropic": ["openai", "google"],
            "openai": ["anthropic", "google"],
            "google": ["anthropic", "openai"]
        }

        providers_to_try = [provider] + fallback_sequence[provider]

        for attempt_provider in providers_to_try:
            try:
                response, metrics = self._call_provider(
                    attempt_provider,
                    system_prompt,
                    user_message,
                    model_tier
                )
                return response, metrics

            except Exception as e:
                self.logger.warning(
                    f"Provider {attempt_provider} failed: {str(e)}. "
                    f"Falling back to next provider..."
                )
                continue

        raise Exception("All providers failed")

    def _call_provider(
        self,
        provider: str,
        system_prompt: str,
        user_message: str,
        model_tier: str
    ) -> tuple[str, dict]:
        """Call specific provider and return response + metrics"""

        import time
        start_time = time.time()

        if provider == "anthropic":
            client = self.config.providers["anthropic"]["client"]
            model = self.config.providers["anthropic"]["models"][model_tier]

            response = client.messages.create(
                model=model,
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )

            text = response.content[0].text
            cost = len(user_message) * self.config.providers["anthropic"]["cost"][model_tier] / 1000000

        elif provider == "openai":
            client = self.config.providers["openai"]["client"]
            model = self.config.providers["openai"]["models"][model_tier]

            response = client.chat.completions.create(
                model=model,
                temperature=0.7,
                max_tokens=1000,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )

            text = response.choices[0].message.content
            cost = len(user_message) * self.config.providers["openai"]["cost"][model_tier] / 1000000

        elif provider == "google":
            model = self.config.providers["google"]["models"][model_tier]
            gemini_client = genai.GenerativeModel(model)

            response = gemini_client.generate_content(
                f"{system_prompt}\n\nUser: {user_message}"
            )

            text = response.text
            cost = len(user_message) * self.config.providers["google"]["cost"][model_tier] / 1000000

        latency_ms = (time.time() - start_time) * 1000

        metrics = {
            "provider": provider,
            "model": model,
            "cost": cost,
            "latency_ms": latency_ms,
            "timestamp": time.time()
        }

        return text, metrics

    def _log_metrics(self, provider: str, metrics: dict):
        """Log metrics for cost optimization and provider health monitoring"""

        # In production, write to database or monitoring system
        self.logger.info(f"Provider {provider}: Cost ${metrics['cost']:.4f}, Latency {metrics['latency_ms']:.0f}ms")

# Usage Example
if __name__ == "__main__":
    api_keys = {
        "anthropic": "sk-ant-...",
        "openai": "sk-proj-...",
        "google": "AIza..."
    }

    router = RequestRouter(api_keys)

    # Simple request → cheapest fast model
    response, provider, metrics = router.route_request(
        system_prompt="You are a helpful assistant",
        user_message="What is 2+2?",
        complexity=RequestComplexity.SIMPLE,
        cost_priority=0.8  # Prioritize cost
    )
    print(f"Response from {provider}: {response}")
    print(f"Cost: ${metrics['cost']:.4f}")

    # Complex request → best quality model
    response, provider, metrics = router.route_request(
        system_prompt="You are an expert researcher",
        user_message="Explain quantum entanglement and its implications",
        complexity=RequestComplexity.COMPLEX,
        cost_priority=0.1  # Prioritize quality
    )
    print(f"Response from {provider}: {response}")

    # Video analysis → Google only
    response, provider, metrics = router.route_request(
        system_prompt="Analyze this video",
        user_message="What's happening in the video?",
        complexity=RequestComplexity.VISION,
        has_vision=True
    )
    print(f"Video analyzed by {provider}: {response}")
```

### 5.4 Multi-Provider Cost Optimization

**Real-world example** (customer support chatbot):

```
Monthly volume: 500K requests

Breakdown by complexity:
- 60% simple requests (fact lookup, classification)
- 30% medium requests (multi-turn conversation)
- 10% complex requests (reasoning, analysis)

Provider Routing:
- Simple (300K/month) → Google Flash ($0.075/M) = $22.50/month
- Medium (150K/month) → Anthropic Sonnet ($3/M input) = $450/month
- Complex (50K/month) → OpenAI GPT-4 ($5/M input) = $250/month

Total Monthly Cost: ~$723

Single-provider cost (OpenAI GPT-4): 500K × $5/M = $2,500
Multi-provider savings: $2,500 - $723 = $1,777/month (71% reduction!)

Cost of multi-provider infrastructure: ~$5K/month (engineering, monitoring)
Net cost increase: $5K - $1,777 = $3,223/month

Break-even: When monthly volume > 1M requests
```

---

## 6. Migration Cost Matrix

**Estimated switching costs between providers** (engineering hours):

| From → To | Lightweight | Full Abstraction | Multi-Provider |
|-----------|------------|------------------|-----------------|
| **OpenAI → Anthropic** | 20 hours | 5 hours | 40 hours |
| **OpenAI → Google** | 30 hours | 5 hours | 50 hours |
| **OpenAI → Mistral** | 15 hours | 5 hours | 35 hours |
| **Anthropic → OpenAI** | 25 hours | 5 hours | 45 hours |
| **Anthropic → Cohere** | 60+ hours | 10 hours | 80 hours |
| **Cohere → Anthropic** | 70+ hours | 15 hours | 90 hours |
| **Google → Anthropic** | 20 hours | 5 hours | 40 hours |
| **Mistral → OpenAI** | 10 hours | 5 hours | 30 hours |

**Key Insight**: Full abstraction (LangChain) reduces switching cost by 75-90% across all providers.

---

## 7. Decision Matrix: Which Mitigation Level?

| Provider | Viability | Lock-In | Mitigation | Rationale |
|----------|-----------|---------|-----------|-----------|
| **OpenAI** | Very High (90%+) | Medium (3/5) | Level 1 (Accept) | Risk is low, switching cost acceptable |
| **Anthropic** | Very High (85-90%) | High (4/5) | Level 1 (Accept) | Feature value (caching) > switching cost |
| **Google** | Very High (99%+) | Medium-High (3.5/5) | Level 1 (Accept) | Public company, infinite backing |
| **Mistral** | High (70-80%) | Low (2/5) | Level 2 (Lightweight) | Medium-risk provider, easy migration |
| **Cohere** | Medium (65-75%) | Very High (4.5/5) | Level 3 (Full Abstraction) | Risk is material, need max flexibility |
| **Meta Llama** | Very High (95%) | Very Low (1/5) | Level 0 (No mitigation) | Open-source, zero lock-in |

---

## 8. Exit Strategy Planning

### 8.1 Triggers for Migration

**Automatic Triggers** (plan migration if any occur):

1. **Financial Distress**: Provider raises prices >50% YoY
2. **Viability Concern**: Provider fails funding round or reports losses
3. **Feature Removal**: Critical features deprecated (prompt caching, context window)
4. **SLA Violations**: >2 outages per quarter or <99% uptime
5. **Competitive Threat**: New provider offers 2× better quality or cost

**Example Trigger**: Cohere raises prices 50% → triggers migration to Anthropic

### 8.2 Migration Playbook (100-day plan)

**Weeks 1-2: Planning & Testing**
- Evaluate 2-3 alternative providers (cost, quality, features)
- Run parallel testing (route 10% traffic to backup provider)
- Estimate switching cost (hours, downtime, risk)

**Weeks 3-6: Development**
- Implement lightweight abstraction or full abstraction layer
- Modify application code to support dual providers
- Set up monitoring and cost tracking

**Weeks 7-8: Validation**
- Run A/B test (50/50 split between providers)
- Validate quality, latency, cost metrics
- Test fallback scenarios (primary provider down)

**Weeks 9-10: Gradual Migration**
- Week 9: 80% old, 20% new provider
- Week 9: 50% old, 50% new provider
- Week 10: 20% old, 80% new provider

**Week 10: Complete Migration**
- 100% to new provider
- Monitor for 1-2 weeks
- Retire old provider integration

**Cost**:
- Development: 40-80 hours ($6K-12K)
- Testing & validation: 20-30 hours ($3K-5K)
- Monitoring & ops: 10-15 hours ($1.5K-2.5K)
- Total: $10K-20K

---

**Document Statistics**: ~650 lines | **Next Document**: api-compatibility.md
