#!/usr/bin/env python3
"""Test core fs-train modules."""

from scenario_loader import ScenarioLoader
from view_engine import ViewEngine
from scorer import ObservationScorer

def test_scenario_loading():
    """Test scenario loading."""
    print("Testing scenario loader...")
    loader = ScenarioLoader('scenarios')

    scenarios = loader.list_scenarios()
    print(f"  ✓ Found {len(scenarios)} scenarios")

    # Load first scenario
    scenario = loader.load_scenario('001_simple_growth.yaml')
    print(f"  ✓ Loaded: {scenario['name']}")
    print(f"  ✓ Difficulty: {scenario['difficulty']}")
    print(f"  ✓ Key insights: {len(scenario['key_insights'])}")

    return scenario

def test_view_engine(scenario):
    """Test view engine."""
    print("\nTesting view engine...")
    engine = ViewEngine(scenario)

    print(f"  ✓ Months: {engine.months}")
    print(f"  ✓ Views available: {list(engine.views.keys())}")

    # Test default view
    default = engine.get_view('default')
    print(f"  ✓ Revenue (Jan): ${default['revenue']['jan']:,.0f}")
    print(f"  ✓ Gross profit (Mar): ${default['gross_profit']['mar']:,.0f}")

    # Test formatted output
    print("\n  Default view output:")
    formatted = engine.format_view('default')
    for line in formatted.split('\n')[:7]:  # First 7 lines
        print(f"    {line}")

    # Test MoM view
    print("\n  MoM view output:")
    mom_formatted = engine.format_view('mom')
    for line in mom_formatted.split('\n')[:7]:
        print(f"    {line}")

    return engine

def test_scorer(scenario):
    """Test observation scorer."""
    print("\nTesting scorer...")
    scorer = ObservationScorer(scenario['key_insights'])

    # Test observation matching
    obs1 = "Revenue is growing steadily at about 10% month over month"
    result1 = scorer.score_observation(obs1)
    print(f"  ✓ Observation 1: '{obs1}'")
    print(f"    Points: {result1['points']}")
    print(f"    Matches: {len(result1['matches'])}")

    obs2 = "The company is profitable and the gross margin is stable at 70%"
    result2 = scorer.score_observation(obs2)
    print(f"  ✓ Observation 2: '{obs2}'")
    print(f"    Points: {result2['points']}")
    print(f"    Matches: {len(result2['matches'])}")

    # Test summary
    summary = scorer.get_summary()
    print(f"\n  Score: {summary['user_score']}/{summary['max_score']} ({summary['percentage']:.0f}%)")
    print(f"  Depth: {summary['depth_level']}")
    print(f"  Caught: {len(summary['caught'])} insights")
    print(f"  Missed: {len(summary['missed'])} insights")

    return scorer

def main():
    """Run all tests."""
    print("=" * 60)
    print("fs-train Core Module Tests")
    print("=" * 60)

    try:
        scenario = test_scenario_loading()
        engine = test_view_engine(scenario)
        scorer = test_scorer(scenario)

        print("\n" + "=" * 60)
        print("✓ All core modules working correctly!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
