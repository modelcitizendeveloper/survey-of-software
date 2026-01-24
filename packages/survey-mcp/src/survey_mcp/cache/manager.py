"""Cache manager for survey data using diskcache."""

import os
from pathlib import Path
from typing import Optional
import diskcache
import requests
from bs4 import BeautifulSoup


class CacheManager:
    """
    Manages caching of HTTP requests to research.modelcitizendeveloper.com

    Uses diskcache for persistent local caching with TTL.
    """

    def __init__(self, cache_dir: Optional[Path] = None, ttl: int = 86400):
        """
        Initialize cache manager.

        Args:
            cache_dir: Cache directory path. Defaults to ~/.cache/survey-mcp/
            ttl: Time-to-live in seconds. Default: 86400 (24 hours)
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "survey-mcp"

        cache_dir.mkdir(parents=True, exist_ok=True)

        self.cache = diskcache.Cache(str(cache_dir))
        self.ttl = ttl
        self.base_url = "https://research.modelcitizendeveloper.com"

    def fetch_url(self, path: str, use_cache: bool = True) -> str:
        """
        Fetch URL content with caching.

        Args:
            path: URL path (e.g., "/survey/", "/survey/1.001/")
            use_cache: Whether to use cache. Default: True

        Returns:
            HTML content as string

        Raises:
            requests.RequestException: If HTTP request fails
        """
        cache_key = f"url:{path}"

        # Check cache first
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached

        # Fetch from web
        url = f"{self.base_url}{path}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        content = response.text

        # Store in cache
        self.cache.set(cache_key, content, expire=self.ttl)

        return content

    def parse_survey_page(self, category: str) -> dict:
        """
        Parse a survey page and extract structured data.

        Args:
            category: Survey category ID (e.g., "1-001" or "1.001")

        Returns:
            dict: {
                "category": str,
                "title": str,
                "content": str,  # Full HTML
                "s1_rapid": str or None,
                "s2_comprehensive": str or None,
                "s3_need_driven": str or None,
                "s4_strategic": str or None
            }
        """
        # Normalize category format: 1.001 → 1-001
        category_url = category.replace(".", "-")

        # Fetch survey page
        path = f"/survey/{category_url}"
        html = self.fetch_url(path)

        soup = BeautifulSoup(html, 'lxml')

        # Extract title
        title_elem = soup.find('h1')
        title = title_elem.get_text(strip=True) if title_elem else category

        # Extract 4PS sections
        # Look for headings with "S1", "S2", "S3", "S4" or "01-discovery", "02-comparison", etc.
        result = {
            "category": category,
            "title": title,
            "content": html,
            "s1_rapid": None,
            "s2_comprehensive": None,
            "s3_need_driven": None,
            "s4_strategic": None
        }

        # Find all headings (h2, h3) to locate pass sections
        for heading in soup.find_all(['h2', 'h3']):
            heading_text = heading.get_text(strip=True).lower()

            # Collect content until next heading
            content_parts = []
            for sibling in heading.find_next_siblings():
                if sibling.name in ['h2', 'h3']:
                    break
                content_parts.append(str(sibling))

            section_html = "\n".join(content_parts)

            # Identify pass type
            if 's1' in heading_text or 'rapid' in heading_text or '01-discovery' in heading_text:
                result['s1_rapid'] = section_html
            elif 's2' in heading_text or 'comprehensive' in heading_text or '02-comparison' in heading_text:
                result['s2_comprehensive'] = section_html
            elif 's3' in heading_text or 'need-driven' in heading_text or '03-need-driven' in heading_text:
                result['s3_need_driven'] = section_html
            elif 's4' in heading_text or 'strategic' in heading_text or '04-strategic' in heading_text:
                result['s4_strategic'] = section_html

        return result

    def get_survey_index(self) -> dict:
        """
        Fetch and parse the survey index page.

        Returns:
            dict: {
                "categories": [
                    {
                        "range": "1.001-009",
                        "title": "Sorting & Searching Algorithms",
                        "complete": 5,
                        "total": 9,
                        "surveys": [
                            {"id": "1-001", "title": "...", "completed": True},
                            ...
                        ]
                    },
                    ...
                ]
            }
        """
        cache_key = "index:survey"

        # Check cache
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        # Fetch index page
        html = self.fetch_url("/survey/")
        soup = BeautifulSoup(html, 'lxml')

        categories = []

        # Find all h2 headings (category sections)
        for h2 in soup.find_all('h2'):
            heading_text = h2.get_text(strip=True)

            # Extract category range and title
            # Format: "1.001-009: Sorting & Searching Algorithms"
            if ':' in heading_text:
                range_part, title_part = heading_text.split(':', 1)
                range_id = range_part.strip()
                title = title_part.strip()
            else:
                range_id = heading_text
                title = heading_text

            # Find completion status (Completed: X/Y)
            completed_count = 0
            total_count = 0

            # Look for list items under this heading
            surveys = []
            next_elem = h2.find_next_sibling()
            while next_elem and next_elem.name != 'h2':
                if next_elem.name == 'ul':
                    for li in next_elem.find_all('li'):
                        li_text = li.get_text(strip=True)
                        is_complete = '✅' in li_text

                        # Extract survey link
                        link = li.find('a')
                        if link and link.get('href'):
                            survey_id = link.get('href').replace('/survey/', '').strip('/')
                            survey_title = link.get_text(strip=True)

                            surveys.append({
                                "id": survey_id,
                                "title": survey_title,
                                "completed": is_complete
                            })

                            total_count += 1
                            if is_complete:
                                completed_count += 1

                next_elem = next_elem.find_next_sibling()

            categories.append({
                "range": range_id,
                "title": title,
                "complete": completed_count,
                "total": total_count,
                "surveys": surveys
            })

        result = {"categories": categories}

        # Cache result
        self.cache.set(cache_key, result, expire=self.ttl)

        return result

    def clear(self):
        """Clear all cached data."""
        self.cache.clear()


# Singleton instance
_cache_manager = None


def get_cache_manager() -> CacheManager:
    """Get global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager
