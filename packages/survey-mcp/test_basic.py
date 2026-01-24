#!/usr/bin/env python3
"""Basic test to verify survey-mcp functionality."""

import sys
from survey_mcp.cache import get_cache_manager


def test_cache_manager():
    """Test that cache manager initializes."""
    print("Testing cache manager...")
    cache = get_cache_manager()
    print(f"✅ Cache manager initialized at: {cache.cache.directory}")
    print(f"   Base URL: {cache.base_url}")
    print(f"   TTL: {cache.ttl}s")
    return True


def test_fetch_index():
    """Test fetching survey index."""
    print("\nTesting survey index fetch...")
    cache = get_cache_manager()

    try:
        index = cache.get_survey_index()
        print(f"✅ Survey index fetched")
        print(f"   Categories found: {len(index.get('categories', []))}")
        return True
    except Exception as e:
        print(f"❌ Failed to fetch index: {e}")
        return False


def test_fetch_survey():
    """Test fetching a specific survey."""
    print("\nTesting survey page fetch...")
    cache = get_cache_manager()

    # Get a real survey ID from the index
    index = cache.get_survey_index()
    survey_id = None

    for category in index.get('categories', []):
        for survey in category.get('surveys', []):
            if survey.get('completed'):
                survey_id = survey['id']
                break
        if survey_id:
            break

    if not survey_id:
        print("⚠️  No completed surveys found in index, skipping survey fetch test")
        return True

    # Try to fetch a real survey
    try:
        survey = cache.parse_survey_page(survey_id)
        print(f"✅ Survey fetched: {survey['title']}")
        print(f"   Category: {survey['category']}")
        print(f"   Has S1: {'✅' if survey.get('s1_rapid') else '❌'}")
        print(f"   Has S2: {'✅' if survey.get('s2_comprehensive') else '❌'}")
        print(f"   Has S3: {'✅' if survey.get('s3_need_driven') else '❌'}")
        print(f"   Has S4: {'✅' if survey.get('s4_strategic') else '❌'}")
        return True
    except Exception as e:
        print(f"❌ Survey fetch failed: {e}")
        return False


def main():
    """Run basic tests."""
    print("=" * 60)
    print("survey-mcp Basic Tests")
    print("=" * 60)

    tests = [
        test_cache_manager,
        test_fetch_index,
        test_fetch_survey,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
