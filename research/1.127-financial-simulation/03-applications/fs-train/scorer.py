#!/usr/bin/env python3
"""Score user observations using keyword matching and LLM evaluation."""

import re
import json
import requests
from typing import Dict, List, Any, Tuple


class ObservationScorer:
    """Score user observations against ground truth insights."""

    def __init__(self, key_insights: List[Dict[str, Any]], llm_provider: str = "ollama",
                 llm_model: str = "llama3", llm_base_url: str = "http://localhost:11434"):
        """Initialize scorer.

        Args:
            key_insights: Ground truth insights from scenario
            llm_provider: LLM provider ('ollama', 'openai', 'claude')
            llm_model: Model name (e.g., 'llama3', 'gpt-4', 'claude-3-sonnet')
            llm_base_url: Base URL for LLM API (Ollama default)
        """
        self.key_insights = key_insights
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        self.llm_base_url = llm_base_url

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

        result = {
            'observation': observation,
            'matches': matches,
            'points': points,
            'method': 'keyword'
        }

        # LLM evaluation (Phase 2 feature)
        if use_llm and matches:
            llm_result = self._evaluate_with_llm(observation, matches)
            result['llm_feedback'] = llm_result.get('feedback', '')
            result['llm_bonus'] = llm_result.get('bonus_points', 0)
            result['points'] += result['llm_bonus']

        self.observation_log.append(result)
        return result

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
            return {'feedback': '', 'bonus_points': 0}

        # Ollama evaluation
        try:
            prompt = self._build_evaluation_prompt(observation, matches)
            response = self._call_ollama(prompt)

            # Parse response
            parsed = self._parse_llm_response(response)
            return parsed

        except Exception as e:
            print(f"LLM evaluation failed: {e}")
            return {'feedback': '', 'bonus_points': 0}

    def _build_evaluation_prompt(self, observation: str, matches: List[Dict]) -> str:
        """Build evaluation prompt for LLM."""
        matched_insights = "\n".join([
            f"- {m['description']} ({m['points']} points)"
            for m in matches
        ])

        prompt = f"""You are a financial analysis instructor evaluating a student's observation.

Student Observation: "{observation}"

This observation matched these key insights:
{matched_insights}

Evaluate the observation:
1. Does it show deeper understanding beyond the matched insights?
2. Does it make connections between multiple metrics?
3. Is the analysis precise and accurate?

Provide:
- bonus_points: 0-10 (0 = basic match, 10 = exceptional insight)
- feedback: 1-2 sentences explaining the quality

Return ONLY valid JSON:
{{"bonus_points": <number>, "feedback": "<text>"}}"""

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
                    'bonus_points': max(0, min(10, parsed.get('bonus_points', 0)))
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
