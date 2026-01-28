#!/usr/bin/env python3
"""
OBS Overlay - Update Timer Display

Writes countdown timer text to timer.txt for OBS to display.
Useful for "Act Now" limited-time offers during live streams.

Usage:
    python obs-update-timer.py --start 30           # Start 30-minute countdown
    python obs-update-timer.py --update             # Update display (call from cron)
    python obs-update-timer.py --stop               # Stop timer
    python obs-update-timer.py --clear              # Clear display
"""

import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

OVERLAY_DIR = Path("/mnt/c/obs-overlay")
CONFIG_FILE = OVERLAY_DIR / "config.json"
TIMER_FILE = OVERLAY_DIR / "timer.txt"


def load_config():
    """Load config.json"""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def save_config(config):
    """Save config.json"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def write_timer(text):
    """Write timer to timer.txt"""
    with open(TIMER_FILE, 'w') as f:
        f.write(text)
    print(f"✓ Timer updated: {text}")


def start_timer(minutes):
    """Start a countdown timer"""
    config = load_config()

    end_time = datetime.now() + timedelta(minutes=minutes)
    config['timer_end'] = end_time.isoformat()
    save_config(config)

    write_timer(f"{minutes}:00 remaining")
    print(f"✓ Timer started: {minutes} minutes")


def update_timer():
    """Update timer display based on remaining time"""
    config = load_config()

    if 'timer_end' not in config:
        write_timer("")
        return

    end_time = datetime.fromisoformat(config['timer_end'])
    now = datetime.now()

    if now >= end_time:
        write_timer("TIME'S UP!")
        print("⏰ Timer expired")
        return

    remaining = end_time - now
    minutes = int(remaining.total_seconds() // 60)
    seconds = int(remaining.total_seconds() % 60)

    text = f"{minutes}:{seconds:02d} remaining"
    write_timer(text)


def stop_timer():
    """Stop and clear timer"""
    config = load_config()

    if 'timer_end' in config:
        del config['timer_end']
        save_config(config)

    write_timer("")
    print("✓ Timer stopped")


def main():
    parser = argparse.ArgumentParser(description="Update OBS timer overlay")
    parser.add_argument('--start', type=int, metavar='MINUTES', help='Start countdown (minutes)')
    parser.add_argument('--update', action='store_true', help='Update display')
    parser.add_argument('--stop', action='store_true', help='Stop timer')
    parser.add_argument('--clear', action='store_true', help='Clear display')

    args = parser.parse_args()

    if args.start:
        start_timer(args.start)
    elif args.update:
        update_timer()
    elif args.stop or args.clear:
        stop_timer()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
