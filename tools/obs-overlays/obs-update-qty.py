#!/usr/bin/env python3
"""
OBS Overlay - Update Quantity Display

Reads config.json and writes the current quantity to qty.txt for OBS to display.
Supports countdown mode (decreasing availability) or count-up mode (sales counter).

Usage:
    python obs-update-qty.py                # Write current value
    python obs-update-qty.py --decrement    # Decrease by 1 (someone claimed)
    python obs-update-qty.py --increment    # Increase by 1 (count up)
    python obs-update-qty.py --set 25       # Set specific value
    python obs-update-qty.py --mode up      # Switch to count-up mode
    python obs-update-qty.py --mode down    # Switch to countdown mode
    python obs-update-qty.py --clear        # Clear display
"""

import json
import argparse
from pathlib import Path

OVERLAY_DIR = Path("/mnt/c/obs-overlay")
CONFIG_FILE = OVERLAY_DIR / "config.json"
QTY_FILE = OVERLAY_DIR / "qty.txt"


def load_config():
    """Load config.json"""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def save_config(config):
    """Save config.json"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def write_qty(text):
    """Write quantity to qty.txt"""
    with open(QTY_FILE, 'w') as f:
        f.write(text)
    print(f"✓ Quantity updated: {text}")


def update_qty(increment=False, decrement=False, set_value=None, mode=None, clear=False):
    """Update quantity display from config"""
    if clear:
        write_qty("")
        return

    config = load_config()

    # Update mode if specified
    if mode:
        config['qty_mode'] = mode
        print(f"✓ Mode changed to: {mode}")

    current_mode = config.get('qty_mode', 'down')
    current_value = config.get('qty_value', 0)

    # Update value
    if set_value is not None:
        current_value = set_value
    elif increment:
        current_value += 1
    elif decrement:
        current_value = max(0, current_value - 1)

    # Save updated value
    config['qty_value'] = current_value
    save_config(config)

    # Format text based on mode
    if current_mode == 'up':
        text = f"{current_value} sold"
    else:  # down mode
        text = f"{current_value} left" if current_value > 0 else "SOLD OUT"

    write_qty(text)


def main():
    parser = argparse.ArgumentParser(description="Update OBS quantity overlay")
    parser.add_argument('--increment', action='store_true', help='Increase by 1')
    parser.add_argument('--decrement', action='store_true', help='Decrease by 1')
    parser.add_argument('--set', type=int, dest='set_value', help='Set specific value')
    parser.add_argument('--mode', choices=['up', 'down'], help='Set counting mode')
    parser.add_argument('--clear', action='store_true', help='Clear quantity display')

    args = parser.parse_args()

    update_qty(
        increment=args.increment,
        decrement=args.decrement,
        set_value=args.set_value,
        mode=args.mode,
        clear=args.clear
    )


if __name__ == '__main__':
    main()
