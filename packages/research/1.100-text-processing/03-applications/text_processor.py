"""
Text Processor - Local Model Application for Text Processing
Part of 1.100-text-processing experiment

Design Strategy:
- Simple text operations that local models handle well
- Clear input/output expectations with fallbacks
- Uses Ollama for local model integration
"""

import subprocess
import json
import re
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """Supported text processing tasks for local models"""
    CLEAN = "clean"
    EXTRACT_EMAILS = "extract_emails"
    EXTRACT_NAMES = "extract_names"
    SENTIMENT = "sentiment"
    SUMMARIZE = "summarize"
    CATEGORIZE = "categorize"


@dataclass
class ProcessingResult:
    """Result of text processing operation"""
    success: bool
    result: Union[str, List[str], Dict]
    task_type: TaskType
    model_used: str
    error: Optional[str] = None


class LocalTextProcessor:
    """
    Text processor using local Ollama models for simple operations
    Based on findings from 1.100-text-processing/02-implementations
    """

    def __init__(self, model: str = "gemma2:2b", timeout: int = 30):
        """
        Initialize with specific model and timeout

        Args:
            model: Ollama model name (gemma2:2b recommended from experiments)
            timeout: Maximum seconds to wait for model response
        """
        self.model = model
        self.timeout = timeout

    def _call_ollama(self, prompt: str) -> Optional[str]:
        """Make a call to Ollama with the given prompt"""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return None

        except subprocess.TimeoutExpired:
            return None
        except Exception:
            return None

    def clean_text(self, text: str) -> ProcessingResult:
        """Clean and normalize text using local model"""
        prompt = f"""Clean this text by removing extra whitespace, fixing basic formatting issues, and normalizing punctuation. Return only the cleaned text:

{text}"""

        response = self._call_ollama(prompt)

        if response:
            cleaned = response.replace('\n\n\n', '\n\n').strip()
            return ProcessingResult(
                success=True,
                result=cleaned,
                task_type=TaskType.CLEAN,
                model_used=self.model
            )
        else:
            # Fallback: basic Python cleaning
            cleaned = re.sub(r'\s+', ' ', text).strip()
            return ProcessingResult(
                success=False,
                result=cleaned,
                task_type=TaskType.CLEAN,
                model_used="fallback",
                error="Model timeout or failure"
            )

    def extract_emails(self, text: str) -> ProcessingResult:
        """Extract email addresses from text"""
        prompt = f"""Extract all email addresses from this text. Return only the email addresses, one per line:

{text}"""

        response = self._call_ollama(prompt)

        if response:
            emails = []
            for line in response.split('\n'):
                line = line.strip()
                if '@' in line and '.' in line:
                    emails.append(line)

            return ProcessingResult(
                success=True,
                result=emails,
                task_type=TaskType.EXTRACT_EMAILS,
                model_used=self.model
            )
        else:
            # Fallback: regex extraction
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            return ProcessingResult(
                success=False,
                result=emails,
                task_type=TaskType.EXTRACT_EMAILS,
                model_used="fallback",
                error="Model timeout or failure"
            )

    def simple_sentiment(self, text: str) -> ProcessingResult:
        """Simple sentiment analysis - positive, negative, neutral"""
        prompt = f"""Analyze the sentiment of this text. Respond with exactly one word: positive, negative, or neutral.

{text}"""

        response = self._call_ollama(prompt)

        if response:
            sentiment = response.lower().strip()
            if sentiment in ['positive', 'negative', 'neutral']:
                return ProcessingResult(
                    success=True,
                    result=sentiment,
                    task_type=TaskType.SENTIMENT,
                    model_used=self.model
                )

        # Fallback: simple word-based sentiment
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible']

        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        if pos_count > neg_count:
            result = 'positive'
        elif neg_count > pos_count:
            result = 'negative'
        else:
            result = 'neutral'

        return ProcessingResult(
            success=False,
            result=result,
            task_type=TaskType.SENTIMENT,
            model_used="fallback",
            error="Model timeout or failure"
        )


def demo():
    """Demonstrate the text processor"""
    processor = LocalTextProcessor()

    print("🧪 1.100-text-processing: Text Processor Demo\n")
    print("Based on local model capabilities research")
    print("=" * 60)

    # Test text cleaning
    messy_text = "Hello    world!  This   is a    test.\n\n\nExtra   spaces everywhere."
    print("\n📝 Text Cleaning Test:")
    print(f"Input: {repr(messy_text)}")
    result = processor.clean_text(messy_text)
    print(f"Output: {repr(result.result)}")
    print(f"Success: {result.success}, Model: {result.model_used}")

    # Test email extraction
    text_with_emails = "Contact us at support@company.com or sales@business.org for more info."
    print("\n📧 Email Extraction Test:")
    print(f"Input: {text_with_emails}")
    result = processor.extract_emails(text_with_emails)
    print(f"Emails found: {result.result}")
    print(f"Success: {result.success}, Model: {result.model_used}")

    # Test sentiment analysis
    positive_text = "I love this product! It's amazing and works perfectly."
    print("\n💭 Sentiment Analysis Test:")
    print(f"Input: {positive_text}")
    result = processor.simple_sentiment(positive_text)
    print(f"Sentiment: {result.result}")
    print(f"Success: {result.success}, Model: {result.model_used}")


if __name__ == "__main__":
    demo()