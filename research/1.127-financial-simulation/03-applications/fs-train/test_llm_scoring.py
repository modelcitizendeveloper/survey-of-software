#!/usr/bin/env python3
"""Test LLM scoring with local Ollama."""

from scenario_loader import ScenarioLoader
from scorer import ObservationScorer

# Load scenario 003
loader = ScenarioLoader('scenarios')
scenario = loader.load_scenario('003_growth_hiring.yaml')

# Create scorer with LLM enabled
scorer = ObservationScorer(
    scenario['key_insights'],
    scenario_id='003_test',
    llm_provider='ollama',
    llm_model='llama3'
)

# Test the problematic observations from the session
test_cases = [
    ("variable operating expenses", 
     "Should recognize this is about the salary jump in March"),
    
    ("high growth in opex",
     "Should connect to hiring and cost increases"),
    
    ("if they can continue growth without increasing operating expenses, that's fine",
     "Should recognize this is about unit economics and sustainability"),
]

print("Testing LLM scoring with Ollama (llama3):")
print("=" * 70)
print("NOTE: This requires 'ollama serve' to be running")
print("=" * 70)
print()

for obs_text, context in test_cases:
    print(f'Observation: "{obs_text}"')
    print(f'Context: {context}')
    
    # Try with LLM
    try:
        result = scorer.score_observation(obs_text, use_llm=True)
        
        if result['matches']:
            print(f'  ✓ Keyword match: {result["points"]} pts')
        
        if result.get('llm_bonus', 0) > 0:
            print(f'  🤖 LLM bonus: +{result["llm_bonus"]} pts')
            print(f'  💬 Feedback: {result.get("llm_feedback", "")}')
        
        print(f'  TOTAL: {result["points"]} points')
        
    except Exception as e:
        print(f'  ❌ LLM Error: {e}')
        print(f'  (Is Ollama running? Try: ollama serve)')
    
    print()
