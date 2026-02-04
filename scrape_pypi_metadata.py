#!/usr/bin/env python3
"""
Scrape PyPI metadata for all vocabulary libraries.

Input: ~/gt/research/dev/library-embeddings/data/training_corpus_v3.txt
Output: data/library_pypi_metadata.json

Collects: version, summary, license, homepage, release date, dependency count,
python versions, and GitHub stars (throttled).
"""

import requests
import json
import re
import time
from pathlib import Path
from datetime import datetime


def get_pypi_metadata(library_name: str) -> dict:
    """Fetch metadata from PyPI."""
    url = f"https://pypi.org/pypi/{library_name}/json"

    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 404:
            return {'error': 'not_found'}
        resp.raise_for_status()

        data = resp.json()
        info = data['info']

        # Get latest release date
        latest_version = info['version']
        releases = data.get('releases', {})
        latest_release = releases.get(latest_version, [])
        release_date = None
        if latest_release:
            release_date = latest_release[0].get('upload_time_iso_8601')

        # Count dependencies
        deps = info.get('requires_dist', []) or []
        dep_count = len([d for d in deps if 'extra ==' not in d])

        # Extract GitHub URL
        github_url = None
        for url_field in [info.get('home_page'), info.get('project_url')]:
            if url_field and 'github.com' in url_field:
                github_url = url_field
                break

        # Check project_urls dict
        if not github_url:
            project_urls = info.get('project_urls', {})
            if project_urls:
                for key, url_val in project_urls.items():
                    if url_val and 'github.com' in url_val:
                        github_url = url_val
                        break

        return {
            'name': library_name,
            'version': info.get('version'),
            'summary': info.get('summary'),
            'license': info.get('license'),
            'homepage': info.get('home_page'),
            'github_url': github_url,
            'release_date': release_date,
            'dependency_count': dep_count,
            'python_versions': info.get('requires_python')
        }

    except Exception as e:
        return {'error': str(e)}


def get_github_stars(github_url: str) -> int:
    """Get GitHub stars (if available)."""
    if not github_url:
        return None

    # Parse owner/repo from URL
    match = re.search(r'github\.com/([^/]+)/([^/]+)', github_url)
    if not match:
        return None

    owner, repo = match.groups()
    repo = repo.rstrip('.git')

    try:
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        resp = requests.get(api_url, timeout=10)
        if resp.status_code == 200:
            return resp.json().get('stargazers_count')
    except:
        pass

    return None


def main():
    # Load libraries from training corpus
    corpus_path = Path.home() / 'gt' / 'research' / 'dev' / 'library-embeddings' / 'data' / 'training_corpus_v3.txt'

    libraries = set()
    with open(corpus_path) as f:
        for line in f:
            libraries.update(line.strip().split())

    print(f"Loaded {len(libraries)} unique libraries from training corpus")

    # Scrape metadata
    results = {}
    found_count = 0

    for i, lib in enumerate(sorted(libraries), 1):
        print(f"[{i:3d}/{len(libraries)}] {lib:<40}", end=' ')

        metadata = get_pypi_metadata(lib)

        # Add GitHub stars if available (throttle to avoid rate limit)
        # GitHub allows 60 req/hour unauthenticated, so check every 50th library
        if 'github_url' in metadata and metadata['github_url']:
            if i % 50 == 0:
                stars = get_github_stars(metadata['github_url'])
                if stars is not None:
                    metadata['github_stars'] = stars

        results[lib] = metadata

        if 'error' not in metadata:
            found_count += 1
            print("✓")
        else:
            print(f"✗ ({metadata['error']})")

        time.sleep(0.1)  # Be nice to PyPI

    # Save results
    output_path = Path('data/library_pypi_metadata.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*70}")
    print(f"Results saved to: {output_path}")
    print(f"Libraries found: {found_count}/{len(libraries)}")
    print(f"Success rate: {found_count/len(libraries)*100:.1f}%")

    # Validation
    if found_count >= 700:
        print("✓ VALIDATION PASSED: At least 700/833 libraries found")
    else:
        print(f"⚠ VALIDATION FAILED: Only {found_count}/833 libraries found (need 700+)")


if __name__ == '__main__':
    main()
