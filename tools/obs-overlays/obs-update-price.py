#!/usr/bin/env python3
"""
OBS Overlay - Update Price Display

Reads config.json and writes the current price to price.txt for OBS to display.
Supports multiple pricing tiers (full, discount, live).

Usage:
    python obs-update-price.py full        # Show full price ($99)
    python obs-update-price.py discount    # Show discount price ($49)
    python obs-update-price.py live        # Show live-only price ($29)
    python obs-update-price.py --clear     # Clear price display
"""

import json
import argparse
from pathlib import Path

OVERLAY_DIR = Path("/mnt/c/obs-overlay")
CONFIG_FILE = OVERLAY_DIR / "config.json"
PRICE_FILE = OVERLAY_DIR / "price.txt"


def load_config():
    """Load config.json"""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def write_price(text):
    """Write price to price.txt"""
    with open(PRICE_FILE, 'w') as f:
        f.write(text)
    print(f"✓ Price updated: {text}")


def update_price(tier, clear=False):
    """Update price display from config"""
    if clear:
        write_price("")
        return

    config = load_config()
    prices = config.get('prices', {})

    if tier not in prices:
        print(f"⚠ Unknown tier: {tier}")
        print(f"Available tiers: {', '.join(prices.keys())}")
        return

    price = prices[tier]
    text = f"${price}"
    write_price(text)


def main():
    parser = argparse.ArgumentParser(description="Update OBS price overlay")
    parser.add_argument('tier', nargs='?', choices=['full', 'discount', 'live'],
                        help='Price tier to display')
    parser.add_argument('--clear', action='store_true', help='Clear price display')

    args = parser.parse_args()

    if not args.tier and not args.clear:
        parser.print_help()
        return

    update_price(args.tier, clear=args.clear)


if __name__ == '__main__':
    main()
