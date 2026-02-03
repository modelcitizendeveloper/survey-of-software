#!/usr/bin/env python3
"""Score user observations using keyword matching and LLM evaluation."""

import re
import json
import requests
from typing import Dict, List, Any, Tuple


class ObservationScorer:
    """Score user observations against ground truth insights."""

    def __init__(self, key_insights: List[Dict[str, Any]], llm_provider: str = "ollama",
                 llm_model: str = "llama3.2:latest", llm_base_url: str = "http://localhost:11434",
                 scenario_id: str = "unknown"):
        """Initialize scorer.

        Args:
            key_insights: Ground truth insights from scenario
            llm_provider: LLM provider ('ollama', 'openai', 'claude')
            llm_model: Model name (e.g., 'llama3.2:latest', 'gpt-4', 'claude-3-sonnet')
            llm_base_url: Base URL for LLM API (Ollama default)
            scenario_id: Scenario identifier for logging
        """
        self.key_insights = key_insights
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        self.llm_base_url = llm_base_url
        self.scenario_id = scenario_id

        self.matched_insights = set()
        self.observation_log = []

    def score_observation(self, observation: str, use_llm: bool = False) -> Dict[str, Any]:
        """Score a single observation.

        Args:
            observation: User's observation text
            use_llm: Whether to use LLM scoring (default: keyword only)

        Returns:
            Score result with points, matches, and feedback
        """
        observation_lower = observation.lower()

        # Keyword matching
        matches = []
        near_misses = []
        points = 0

        for insight in self.key_insights:
            insight_id = insight['id']

            # Skip if already matched
            if insight_id in self.matched_insights:
                continue

            # Check keywords
            keywords = insight.get('keywords', [])
            matched_keywords = [kw for kw in keywords if kw.lower() in observation_lower]

            if matched_keywords:
                matches.append({
                    'insight_id': insight_id,
                    'description': insight['description'],
                    'points': insight['points'],
                    'keywords_matched': matched_keywords
                })
                points += insight['points']
                self.matched_insights.add(insight_id)
            else:
                # Check for near misses (related words but not exact keywords)
                near_miss_score = self._check_near_miss(observation_lower, insight)
                if near_miss_score > 0:
                    near_misses.append({
                        'insight_id': insight_id,
                        'description': insight['description'],
                        'keywords': keywords[:3],  # Show first 3 keywords
                        'score': near_miss_score
                    })

        result = {
            'observation': observation,
            'matches': matches,
            'near_misses': near_misses,
            'points': points,
            'method': 'keyword'
        }

        # LLM evaluation - validates ALL observations (matched or not)
        if use_llm:
            llm_result = self._evaluate_with_llm(observation, matches)
            result['llm_feedback'] = llm_result.get('feedback', '')
            result['llm_bonus'] = llm_result.get('bonus_points', 0)

            # If no keyword match but LLM gives points, count it
            if not matches and result['llm_bonus'] >= 3:
                result['points'] = result['llm_bonus']
                result['method'] = 'llm'
            else:
                result['points'] += result['llm_bonus']

        self.observation_log.append(result)
        return result

    def _check_near_miss(self, observation: str, insight: Dict[str, Any]) -> float:
        """Check if observation is close to matching an insight.

        Args:
            observation: User's observation (lowercased)
            insight: Insight to check against

        Returns:
            Score 0-1 indicating how close (0 = not close, 1 = very close)
        """
        # Define synonym groups for common financial terms
        synonyms = {
            'opex': ['operating expense', 'operating cost', 'overhead'],
            'cogs': ['cost of goods', 'cost of sales', 'product cost'],
            'revenue': ['sales', 'income', 'top line'],
            'profit': ['earnings', 'bottom line', 'net income'],
            'margin': ['profitability', 'markup'],
            'grow': ['increase', 'rise', 'expand', 'rising', 'growing'],
            'decline': ['decrease', 'fall', 'drop', 'falling', 'declining'],
            'hire': ['employee', 'headcount', 'staff', 'hiring'],
            'unit economics': ['roi', 'return on investment', 'payback', 'efficiency'],
        }

        # Check if observation contains synonyms of insight keywords
        keywords = insight.get('keywords', [])
        synonym_matches = 0

        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Check if keyword has synonyms
            for canonical, syns in synonyms.items():
                if canonical in keyword_lower or keyword_lower in canonical:
                    # Check if observation contains any synonym
                    for syn in syns:
                        if syn in observation:
                            synonym_matches += 1
                            break

        # If found related terms, return score
        if synonym_matches > 0:
            return min(synonym_matches / len(keywords), 1.0)

        return 0.0

    def _evaluate_with_llm(self, observation: str, matches: List[Dict]) -> Dict[str, Any]:
        """Use LLM to evaluate observation quality and nuance.

        Args:
            observation: User observation
            matches: Keyword matches found

        Returns:
            LLM evaluation with feedback and bonus points
        """
        if self.llm_provider != "ollama":
            # Phase 2: Add OpenAI/Claude support
            return {'feedback': '', 'bonus_points': 0, 'error': 'Only Ollama supported'}

        # Ollama evaluation
        try:
            prompt = self._build_evaluation_prompt(observation, matches)
            response = self._call_ollama(prompt)

            # Parse response
            parsed = self._parse_llm_response(response)
            return parsed

        except requests.exceptions.ConnectionError as e:
            return {'feedback': '', 'bonus_points': 0,
                   'error': 'Ollama not running. Start with: ollama serve'}
        except Exception as e:
            return {'feedback': '', 'bonus_points': 0,
                   'error': f'LLM error: {str(e)[:50]}'}

    def _build_evaluation_prompt(self, observation: str, matches: List[Dict]) -> str:
        """Build evaluation prompt for LLM."""
        if matches:
            matched_insights = "\n".join([
                f"- {m['description']} ({m['points']} points)"
                for m in matches
            ])
            scenario = f"This observation matched these key insights:\n{matched_insights}"
        else:
            # No keyword matches - ask LLM if observation is still valid
            all_insights = "\n".join([
                f"- {insight['description']}"
                for insight in self.key_insights
            ])
            scenario = f"This observation didn't match keywords, but here are the key insights for this scenario:\n{all_insights}"

        prompt = f"""You are a financial analysis instructor serving as a SECOND JUDGE evaluating a student's observation.

Student Observation: "{observation}"

{scenario}

Your role as SECOND JUDGE with OVERRIDE power:
1. Review if the observation is factually accurate and insightful
2. You can AWARD bonus points (+1 to +10) for good insights
3. You can DEDUCT points (-10 to -1) if keywords matched but observation is wrong
4. You can OVERRIDE and award points even without keyword matches (if insight is valid)
5. Teach professional financial terminology in your feedback

Scoring Guide:
NEGATIVE (Deductions):
- -10 to -5: Keyword matched but observation is significantly wrong
- -4 to -1: Minor error or misinterpretation despite keyword match

ZERO (Neutral):
- 0: Vague, already fully covered by keywords, or no additional insight

POSITIVE (Bonus):
- +1 to +3: Correct observation, good use of casual language
- +4 to +6: Insightful analysis connecting multiple data points
- +7 to +9: Deep insight with implications and proper terminology
- +10: Exceptional analysis showing mastery

Feedback Guidelines:
- Keep feedback CONCISE: 50-100 characters maximum (screen space is limited!)
- If keywords matched correctly: "Good! In finance: '[jargon term]'"
- If keywords matched but wrong: "Not quite. [Brief correction]"
- If no keyword match but valid: "Excellent! This is '[jargon term]'"
- Focus on teaching ONE key term per feedback

Return ONLY valid JSON:
{{"bonus_points": <-10 to +10>, "feedback": "<50-100 chars max, teach jargon>"}}"""

        return prompt

    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API.

        Args:
            prompt: Prompt text

        Returns:
            Response text
        """
        url = f"{self.llm_base_url}/api/generate"

        payload = {
            "model": self.llm_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # More consistent for evaluation
                "num_predict": 200   # Short responses
            }
        }

        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        return data.get('response', '')

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM JSON response.

        Args:
            response: Raw LLM response

        Returns:
            Parsed feedback and bonus points
        """
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                return {
                    'feedback': parsed.get('feedback', ''),
                    'bonus_points': max(-10, min(10, parsed.get('bonus_points', 0)))
                }
        except Exception:
            pass

        return {'feedback': '', 'bonus_points': 0}

    def get_missed_insights(self) -> List[Dict[str, Any]]:
        """Get insights user didn't catch.

        Returns:
            List of missed insights
        """
        missed = []
        for insight in self.key_insights:
            if insight['id'] not in self.matched_insights:
                missed.append(insight)
        return missed

    def get_total_score(self) -> Tuple[int, int]:
        """Get user's score and max possible score.

        Returns:
            (user_score, max_score) tuple
        """
        user_score = sum(obs['points'] for obs in self.observation_log)
        max_score = sum(insight['points'] for insight in self.key_insights)
        return user_score, max_score

    def get_summary(self) -> Dict[str, Any]:
        """Get complete scoring summary.

        Returns:
            Summary with scores, catches, misses
        """
        user_score, max_score = self.get_total_score()
        percentage = (user_score / max_score * 100) if max_score > 0 else 0

        # Categorize insights
        caught = [
            insight for insight in self.key_insights
            if insight['id'] in self.matched_insights
        ]
        missed = self.get_missed_insights()

        # Determine depth level
        if percentage >= 81:
            depth = "Advanced"
        elif percentage >= 61:
            depth = "Intermediate"
        elif percentage >= 31:
            depth = "Basic"
        else:
            depth = "Surface"

        return {
            'user_score': user_score,
            'max_score': max_score,
            'percentage': percentage,
            'depth_level': depth,
            'caught': caught,
            'missed': missed,
            'observation_count': len(self.observation_log)
        }

    def save_session_log(self, output_file: str = "training_sessions.jsonl"):
        """Save session observations to JSONL for analysis.

        Args:
            output_file: Path to JSONL log file
        """
        import json
        from datetime import datetime
        from pathlib import Path

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'scenario_id': self.scenario_id,
            'observations': self.observation_log,
            'summary': self.get_summary()
        }

        # Append to JSONL file
        log_path = Path(output_file)
        with open(log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        return log_path
