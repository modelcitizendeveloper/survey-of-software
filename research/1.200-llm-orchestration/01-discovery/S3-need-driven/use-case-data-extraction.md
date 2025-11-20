# Use Case: Structured Data Extraction from Unstructured Text

## Executive Summary

**Best Framework**: LangChain (function calling) or LlamaIndex (Pydantic programs)

**Time to Production**: 2-3 weeks for MVP, 4-8 weeks for production-ready

**Key Requirements**:
- Extract structured JSON/Pydantic models from text
- Schema validation and error handling
- Batch processing capabilities
- Cost optimization for high volume
- Reliability and accuracy

## Framework Comparison for Data Extraction

| Framework | Extraction Suitability | Key Strengths | Limitations |
|-----------|----------------------|---------------|-------------|
| **LangChain** | Excellent (5/5) | Best function calling support, flexible schemas, easy validation | Higher token overhead |
| **LlamaIndex** | Excellent (5/5) | Pydantic programs are elegant, good for extraction from docs | More RAG-focused |
| **Haystack** | Good (3/5) | Production-ready, lower overhead | Less native extraction support |
| **Semantic Kernel** | Good (4/5) | Strong typed support (especially .NET) | Smaller community |
| **DSPy** | Fair (3/5) | Automated optimization, low overhead | Limited production examples |

**Winner**: **LangChain** for general extraction, **LlamaIndex** for document-based extraction

## Structured Output Methods

### 1. Function Calling (Recommended)

Function calling provides the most reliable structured extraction:

```python
from langchain_openai import ChatOpenAI
from langchain.pydantic_v1 import BaseModel, Field
from typing import List, Optional

# Define schema
class Person(BaseModel):
    """Information about a person"""
    name: str = Field(description="Person's full name")
    age: Optional[int] = Field(description="Person's age if mentioned")
    occupation: Optional[str] = Field(description="Person's job or occupation")
    location: Optional[str] = Field(description="City or country where person lives")

class Article(BaseModel):
    """Extracted information from article"""
    title: str = Field(description="Article title")
    people: List[Person] = Field(description="All people mentioned in the article")
    main_topic: str = Field(description="Primary topic or theme")

# Extract using function calling
llm = ChatOpenAI(model="gpt-4", temperature=0)
structured_llm = llm.with_structured_output(Article)

text = """
Breaking News: Tech Innovator Sarah Chen Launches AI Startup
San Francisco entrepreneur Sarah Chen, 32, announced today the launch of
her new artificial intelligence company. Chen, formerly a machine learning
engineer at Google, will focus on healthcare applications.
"""

result = structured_llm.invoke(text)
print(result)
# Article(
#     title="Tech Innovator Sarah Chen Launches AI Startup",
#     people=[Person(name="Sarah Chen", age=32, occupation="entrepreneur", location="San Francisco")],
#     main_topic="AI startup launch in healthcare"
# )
```

### 2. LlamaIndex Pydantic Programs

Clean, declarative approach for extraction:

```python
from llama_index.program.openai import OpenAIPydanticProgram
from pydantic import BaseModel
from typing import List

class Invoice(BaseModel):
    invoice_number: str
    date: str
    total_amount: float
    vendor_name: str
    line_items: List[dict]

program = OpenAIPydanticProgram.from_defaults(
    output_cls=Invoice,
    prompt_template_str="Extract invoice details from: {invoice_text}",
    verbose=True
)

invoice_text = """
INVOICE #INV-2024-001
Date: January 15, 2024
From: Acme Corp
Total: $1,234.56

Line items:
- Widget A: $500
- Widget B: $734.56
"""

result = program(invoice_text=invoice_text)
print(result.invoice_number)  # "INV-2024-001"
print(result.total_amount)     # 1234.56
```

### 3. JSON Output Parser

For simpler schemas without Pydantic:

```python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Define schema
response_schemas = [
    ResponseSchema(name="product_name", description="name of the product"),
    ResponseSchema(name="price", description="price in USD"),
    ResponseSchema(name="features", description="list of key features"),
    ResponseSchema(name="sentiment", description="overall sentiment: positive, neutral, or negative")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

prompt = PromptTemplate(
    template="Extract information from this review:\n{review}\n{format_instructions}",
    input_variables=["review"],
    partial_variables={"format_instructions": format_instructions}
)

llm = ChatOpenAI(temperature=0)
chain = prompt | llm | output_parser

review = """
I just bought the SuperWidget Pro for $299. The wireless connectivity and
battery life are amazing. Very happy with this purchase!
"""

result = chain.invoke({"review": review})
# {
#     "product_name": "SuperWidget Pro",
#     "price": "299",
#     "features": ["wireless connectivity", "battery life"],
#     "sentiment": "positive"
# }
```

## Schema Validation and Error Handling

### Input Validation

```python
from pydantic import BaseModel, Field, validator, ValidationError
from typing import List
from datetime import datetime

class Event(BaseModel):
    """Event with validation rules"""
    event_name: str = Field(min_length=3, max_length=100)
    date: str
    attendees: List[str] = Field(min_items=1)
    budget: float = Field(gt=0, description="Budget must be positive")

    @validator('date')
    def validate_date(cls, v):
        try:
            # Ensure date is in ISO format
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError('Date must be in ISO format (YYYY-MM-DD)')

    @validator('attendees')
    def validate_attendees(cls, v):
        if len(v) > 1000:
            raise ValueError('Too many attendees')
        return v

# Use with retry logic
from tenacity import retry, stop_after_attempt, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    retry_if=retry_if_exception_type(ValidationError)
)
def extract_with_validation(text: str):
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    structured_llm = llm.with_structured_output(Event)

    try:
        result = structured_llm.invoke(text)
        return result
    except ValidationError as e:
        # Log validation errors
        print(f"Validation failed: {e}")
        # Could implement refinement prompt here
        raise
```

### Output Validation with Guardrails

```python
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, field_validator

class ExtractedData(BaseModel):
    email: str
    phone: str
    company: str

    @field_validator('email')
    def validate_email(cls, v):
        import re
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('Invalid email format')
        return v

    @field_validator('phone')
    def validate_phone(cls, v):
        # Remove common formatting
        cleaned = ''.join(filter(str.isdigit, v))
        if len(cleaned) < 10:
            raise ValueError('Phone number too short')
        return cleaned

parser = PydanticOutputParser(pydantic_object=ExtractedData)

def extract_with_fallback(text: str):
    """Extract with fallback to manual parsing"""
    try:
        result = parser.parse(llm_output)
        return result
    except ValidationError as e:
        print(f"Validation failed: {e}")
        # Fallback: try again with more explicit instructions
        refined_prompt = f"Extract again, ensuring valid formats: {text}"
        # ... retry logic
        return None
```

## Batch Processing

### Processing Large Datasets

```python
import asyncio
from typing import List
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class ProductInfo(BaseModel):
    name: str
    category: str
    price: float

async def extract_batch(texts: List[str], batch_size: int = 10):
    """Process documents in parallel batches"""
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    structured_llm = llm.with_structured_output(ProductInfo)

    results = []

    # Process in batches to avoid rate limits
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]

        # Run batch in parallel
        tasks = [structured_llm.ainvoke(text) for text in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle errors
        for j, result in enumerate(batch_results):
            if isinstance(result, Exception):
                print(f"Error processing item {i+j}: {result}")
                results.append(None)
            else:
                results.append(result)

        # Rate limiting delay
        await asyncio.sleep(1)

    return results

# Usage
texts = [...]  # 1000+ product descriptions
results = asyncio.run(extract_batch(texts))
```

### Streaming for Large Files

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_from_large_document(file_path: str, chunk_size: int = 4000):
    """Extract from large documents by chunking"""

    # Read document
    with open(file_path, 'r') as f:
        text = f.read()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=200
    )
    chunks = splitter.split_text(text)

    # Extract from each chunk
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    structured_llm = llm.with_structured_output(ProductInfo)

    all_results = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}")
        result = structured_llm.invoke(chunk)
        all_results.append(result)

    return all_results
```

## Cost Optimization

### Model Selection Strategy

```python
from langchain_openai import ChatOpenAI

class ExtractionOptimizer:
    """Choose model based on complexity"""

    def __init__(self):
        self.simple_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.complex_model = ChatOpenAI(model="gpt-4", temperature=0)
        self.mini_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def extract(self, text: str, schema: BaseModel, complexity: str = "auto"):
        """Choose model based on complexity"""

        # Auto-detect complexity
        if complexity == "auto":
            complexity = self._assess_complexity(text, schema)

        if complexity == "simple":
            # $0.002/1K tokens - good for simple extractions
            model = self.simple_model
        elif complexity == "moderate":
            # $0.015/1K tokens - balanced
            model = self.mini_model
        else:
            # $0.03/1K tokens - complex schemas
            model = self.complex_model

        structured_model = model.with_structured_output(schema)
        return structured_model.invoke(text)

    def _assess_complexity(self, text: str, schema: BaseModel) -> str:
        """Heuristics for complexity"""
        field_count = len(schema.model_fields)
        text_length = len(text)

        if field_count <= 5 and text_length < 1000:
            return "simple"
        elif field_count <= 10 and text_length < 5000:
            return "moderate"
        else:
            return "complex"

# Usage
optimizer = ExtractionOptimizer()

# Simple extraction - uses GPT-3.5
result1 = optimizer.extract(short_text, SimpleSchema, "simple")

# Complex extraction - uses GPT-4
result2 = optimizer.extract(long_text, ComplexSchema, "complex")
```

### Caching for Repeated Extractions

```python
from langchain.cache import InMemoryCache, RedisCache
from langchain.globals import set_llm_cache
import hashlib

# Enable caching
set_llm_cache(InMemoryCache())

# For production, use Redis
# from redis import Redis
# set_llm_cache(RedisCache(redis_=Redis()))

def extract_with_cache(text: str, schema: BaseModel):
    """Extract with caching - identical inputs return cached results"""
    llm = ChatOpenAI(model="gpt-4", temperature=0)  # temp=0 for deterministic
    structured_llm = llm.with_structured_output(schema)

    # Cache automatically used by LangChain
    result = structured_llm.invoke(text)
    return result

# First call: hits API ($$$)
result1 = extract_with_cache(text, Schema)

# Second call with same text: cached (FREE)
result2 = extract_with_cache(text, Schema)
```

### Token Optimization

```python
def optimize_extraction_prompt(text: str, schema: BaseModel):
    """Minimize tokens while maintaining quality"""

    # 1. Remove unnecessary whitespace
    text = ' '.join(text.split())

    # 2. Use shorter schema descriptions
    # Instead of: "The full legal name of the person including middle names"
    # Use: "Person's name"

    # 3. Extract only needed fields
    # Don't extract everything if you only need specific fields

    # 4. Use JSON mode instead of function calling for simple cases
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}}
    )

    prompt = f"""Extract to JSON matching this schema: {schema.model_json_schema()}

    Text: {text}

    Return only the JSON, no explanation."""

    return llm.invoke(prompt)
```

## Which Framework is Most Efficient?

### Performance Comparison

| Framework | Overhead | Token Efficiency | Extraction Accuracy | Best For |
|-----------|----------|-----------------|-------------------|----------|
| **LangChain** | 10ms | 2.40k tokens | Excellent | General extraction, flexibility |
| **LlamaIndex** | 6ms | 1.60k tokens | Excellent | Document-based extraction |
| **Haystack** | 5.9ms | 1.57k tokens | Good | High-volume production |
| **Semantic Kernel** | ~8ms | ~2.0k tokens | Excellent | .NET/typed environments |
| **DSPy** | 3.53ms | 2.03k tokens | Good (with training) | Research, optimization |

**Most Efficient Overall**: **Haystack** (lowest overhead + token usage)

**Most Efficient for Accuracy**: **LangChain** or **LlamaIndex** (function calling)

### Efficiency Recommendations

**High Volume (>10M extractions/month)**:
- Use **Haystack** for best cost efficiency
- Implement aggressive caching
- Use GPT-3.5-turbo for simple schemas

**High Accuracy Required**:
- Use **LangChain** with GPT-4 function calling
- Implement validation and retry logic
- Budget for higher token costs

**Balanced (Accuracy + Cost)**:
- Use **LlamaIndex** Pydantic programs
- GPT-4o-mini for most extractions
- GPT-4 for complex schemas only

## Example Extraction Pipeline

### Invoice Processing Pipeline

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
import asyncio
from datetime import datetime

# Schema definition
class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float

class Invoice(BaseModel):
    invoice_number: str
    invoice_date: str
    due_date: Optional[str]
    vendor_name: str
    vendor_address: Optional[str]
    total_amount: float
    tax_amount: Optional[float]
    line_items: List[LineItem]

    @field_validator('invoice_date', 'due_date')
    def validate_date_format(cls, v):
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date must be YYYY-MM-DD format')
        return v

class InvoiceExtractionPipeline:
    """Production pipeline for invoice extraction"""

    def __init__(self, model: str = "gpt-4"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.structured_llm = self.llm.with_structured_output(Invoice)

    async def extract_invoice(self, invoice_text: str) -> Optional[Invoice]:
        """Extract single invoice with error handling"""
        try:
            result = await self.structured_llm.ainvoke(invoice_text)

            # Validate extraction quality
            if not self._validate_extraction(result, invoice_text):
                print("Validation failed, retrying...")
                return await self._retry_extraction(invoice_text)

            return result

        except Exception as e:
            print(f"Extraction error: {e}")
            return None

    def _validate_extraction(self, invoice: Invoice, original_text: str) -> bool:
        """Basic validation checks"""
        # Check total matches sum of line items
        if invoice.line_items:
            calculated_total = sum(item.total for item in invoice.line_items)
            if abs(calculated_total - invoice.total_amount) > 0.01:
                return False

        # Check required fields present
        if not invoice.invoice_number or not invoice.vendor_name:
            return False

        return True

    async def _retry_extraction(self, text: str) -> Optional[Invoice]:
        """Retry with more explicit instructions"""
        enhanced_prompt = f"""
        Extract invoice data very carefully. Ensure:
        - All amounts are accurate decimals
        - Dates are in YYYY-MM-DD format
        - Line item totals sum to invoice total

        Invoice text:
        {text}
        """

        try:
            result = await self.structured_llm.ainvoke(enhanced_prompt)
            return result
        except Exception as e:
            print(f"Retry failed: {e}")
            return None

    async def process_batch(self, invoices: List[str]) -> List[Optional[Invoice]]:
        """Process multiple invoices in parallel"""
        tasks = [self.extract_invoice(inv) for inv in invoices]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions
        processed = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Invoice {i} failed: {result}")
                processed.append(None)
            else:
                processed.append(result)

        return processed

# Usage
async def main():
    pipeline = InvoiceExtractionPipeline(model="gpt-4")

    invoice_texts = [...]  # Load from files/database

    results = await pipeline.process_batch(invoice_texts)

    # Save to database
    successful = [r for r in results if r is not None]
    print(f"Successfully extracted {len(successful)}/{len(invoice_texts)} invoices")

    for invoice in successful:
        save_to_database(invoice)

# Run
asyncio.run(main())
```

### Resume Parsing Pipeline

```python
from pydantic import BaseModel
from typing import List, Optional

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str]
    graduation_year: Optional[int]

class Experience(BaseModel):
    company: str
    title: str
    start_date: str
    end_date: Optional[str]
    description: Optional[str]

class Resume(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    location: Optional[str]
    summary: Optional[str]
    skills: List[str]
    education: List[Education]
    experience: List[Experience]

def extract_resume(resume_text: str) -> Resume:
    """Extract structured data from resume"""
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    structured_llm = llm.with_structured_output(Resume)

    result = structured_llm.invoke(resume_text)
    return result

# Batch processing for ATS (Applicant Tracking System)
async def process_applicants(resume_files: List[str]):
    """Process multiple resumes for ATS"""
    pipeline = InvoiceExtractionPipeline(model="gpt-4o-mini")  # Cheaper for high volume

    # Read files
    resume_texts = [read_pdf(f) for f in resume_files]

    # Extract in parallel
    results = await pipeline.process_batch(resume_texts)

    return results
```

## Production Deployment

### Cost Estimation

```python
# Example: Processing 10,000 invoices/month

# Model: GPT-4
# Avg input tokens per invoice: 1,500 (1 page invoice)
# Avg output tokens: 500 (structured data)
# Cost: $0.03/1K input + $0.06/1K output

input_cost = (1500 / 1000) * 0.03 * 10000  # $450
output_cost = (500 / 1000) * 0.06 * 10000   # $300
total_llm_cost = input_cost + output_cost    # $750/month

# With GPT-4o-mini (10x cheaper):
# Cost: $0.003/1K input + $0.006/1K output
mini_input_cost = (1500 / 1000) * 0.003 * 10000   # $45
mini_output_cost = (500 / 1000) * 0.006 * 10000   # $30
total_mini_cost = mini_input_cost + mini_output_cost  # $75/month

print(f"GPT-4 cost: ${total_llm_cost}/month")
print(f"GPT-4o-mini cost: ${total_mini_cost}/month")
print(f"Savings: ${total_llm_cost - total_mini_cost}/month")
```

### Architecture

```
┌─────────────────┐
│  Upload Service │
│   (S3/Storage)  │
└────────┬────────┘
         │
┌────────▼────────────────┐
│  Extraction API         │
│  - FastAPI/Flask        │
│  - Queue management     │
│  - Rate limiting        │
└────────┬────────────────┘
         │
┌────────▼────────────────┐
│  LangChain Pipeline     │
│  - Model selection      │
│  - Validation           │
│  - Retry logic          │
└────────┬────────────────┘
         │
┌────────▼────────────────┐
│  OpenAI API             │
│  - GPT-4 / GPT-4o-mini  │
└────────┬────────────────┘
         │
┌────────▼────────────────┐
│  Database               │
│  - PostgreSQL           │
│  - Validation results   │
└─────────────────────────┘

Deployment: Cloud Run / ECS
Cost: $100-500/month (infra + LLM)
Processing: 100-1000 docs/minute
```

### Monitoring

```python
from prometheus_client import Counter, Histogram
import time

extraction_requests = Counter(
    'extraction_requests_total',
    'Total extraction requests',
    ['model', 'schema', 'status']
)

extraction_latency = Histogram(
    'extraction_latency_seconds',
    'Extraction latency'
)

extraction_cost = Counter(
    'extraction_cost_usd',
    'Total extraction cost in USD'
)

def monitored_extract(text: str, schema: BaseModel, model: str = "gpt-4"):
    """Extract with monitoring"""
    start_time = time.time()

    try:
        llm = ChatOpenAI(model=model, temperature=0)
        structured_llm = llm.with_structured_output(schema)
        result = structured_llm.invoke(text)

        # Track success
        extraction_requests.labels(
            model=model,
            schema=schema.__name__,
            status='success'
        ).inc()

        # Track cost
        tokens_used = estimate_tokens(text) + estimate_tokens(str(result))
        cost = calculate_cost(tokens_used, model)
        extraction_cost.inc(cost)

        return result

    except Exception as e:
        extraction_requests.labels(
            model=model,
            schema=schema.__name__,
            status='error'
        ).inc()
        raise

    finally:
        latency = time.time() - start_time
        extraction_latency.observe(latency)
```

## Common Pitfalls

1. **Under-specified schemas**: Vague field descriptions lead to inconsistent extractions
2. **No validation**: Accepting incorrect extractions without verification
3. **Wrong model choice**: Using GPT-4 for simple extractions (expensive)
4. **No error handling**: Pipeline breaks on first failure
5. **Ignoring token limits**: Large documents exceed context windows
6. **No caching**: Re-extracting identical documents
7. **Poor batch processing**: Sequential processing instead of parallel

## Best Practices

1. **Detailed schema descriptions**: Clear field descriptions improve accuracy
2. **Use Pydantic validators**: Catch errors early with validation rules
3. **Implement retry logic**: Automatic retry with refined prompts
4. **Choose right model**: GPT-3.5 for simple, GPT-4 for complex
5. **Batch processing**: Process documents in parallel with rate limiting
6. **Cache results**: Cache identical inputs to save costs
7. **Monitor costs**: Track token usage and costs per extraction
8. **Validate outputs**: Always validate extracted data before using
9. **Test with edge cases**: Test with malformed, missing, or unusual inputs
10. **Use streaming for large files**: Chunk large documents before extraction

## Summary

**For most data extraction use cases, choose LangChain**:
- Best function calling support (most reliable)
- Flexible schema definitions with Pydantic
- Excellent error handling and retry mechanisms
- Production-proven at scale

**Choose LlamaIndex if**:
- Extracting from documents with retrieval
- Want elegant Pydantic program API
- RAG + extraction combined use case

**Choose Haystack if**:
- Processing millions of documents (best efficiency)
- Cost is primary concern
- Production stability critical

**Time to production: 2-8 weeks depending on complexity**
**Cost: $75-$5000/month depending on volume and model choice**
