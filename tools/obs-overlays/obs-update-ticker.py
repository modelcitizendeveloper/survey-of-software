#!/usr/bin/env python3
"""
OBS Overlay - Update Ticker Text

Reads config.json and writes the current ticker message to ticker.txt
for OBS to display. Rotates through ticker_queue if multiple messages exist.

Usage:
    python obs-update-ticker.py                    # Write first message from queue
    python obs-update-ticker.py --rotate           # Rotate queue and write next message
    python obs-update-ticker.py --push "New msg"   # Push urgent message to stack
    python obs-update-ticker.py --pop              # Pop from push stack
"""

import json
import argparse
from pathlib import Path

OVERLAY_DIR = Path("/mnt/c/obs-overlay")
CONFIG_FILE = OVERLAY_DIR / "config.json"
TICKER_FILE = OVERLAY_DIR / "ticker.txt"


def load_config():
    """Load config.json"""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def save_config(config):
    """Save config.json"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def write_ticker(message):
    """Write message to ticker.txt"""
    with open(TICKER_FILE, 'w') as f:
        f.write(message)
    print(f"✓ Ticker updated: {message[:60]}...")


def update_ticker(rotate=False, push_msg=None, pop=False):
    """Update ticker text from config"""
    config = load_config()

    # Handle push stack operations
    if push_msg:
        config['ticker_push_stack'].append(push_msg)
        save_config(config)
        write_ticker(push_msg)
        print(f"✓ Pushed to stack: {push_msg}")
        return

    if pop:
        if config['ticker_push_stack']:
            config['ticker_push_stack'].pop()
            save_config(config)
            print("✓ Popped from stack")
        else:
            print("⚠ Stack empty, nothing to pop")

    # Priority: push stack > queue
    if config['ticker_push_stack']:
        message = config['ticker_push_stack'][-1]
        write_ticker(message)
        return

    # Use queue
    queue = config['ticker_queue']
    if not queue:
        write_ticker("")
        print("⚠ No messages in queue")
        return

    # Rotate queue if requested
    if rotate and len(queue) > 1:
        queue.append(queue.pop(0))
        config['ticker_queue'] = queue
        save_config(config)
        print("↻ Queue rotated")

    # Write first message from queue
    message = queue[0]
    write_ticker(message)


def main():
    parser = argparse.ArgumentParser(description="Update OBS ticker overlay")
    parser.add_argument('--rotate', action='store_true', help='Rotate to next message in queue')
    parser.add_argument('--push', type=str, help='Push urgent message to stack')
    parser.add_argument('--pop', action='store_true', help='Pop message from push stack')

    args = parser.parse_args()

    update_ticker(rotate=args.rotate, push_msg=args.push, pop=args.pop)


if __name__ == '__main__':
    main()
