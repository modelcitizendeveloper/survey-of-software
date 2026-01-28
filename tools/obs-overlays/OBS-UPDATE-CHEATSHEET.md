# OBS Update Cheatsheet

Quick reference for live streaming overlay control.

## 🚀 Quick Start

```bash
# Pre-stream setup
obs-update ticker                    # Load first ticker message
obs-update price live                # Show live price ($29)
obs-update qty --set 50 --mode down  # 50 spots available

# During stream
obs-update qty --dec                 # Someone bought (49 left)
obs-update ticker --rotate           # Next message
obs-update timer --start 30          # Launch urgency offer

# Post-stream
obs-update clear                     # Clear everything
```

## 📋 Command Reference

### Ticker Control

```bash
obs-update ticker                    # Show first message from queue
obs-update ticker --rotate           # Rotate to next message
obs-update ticker --push "🔥 URGENT!" # Override with urgent message
obs-update ticker --pop              # Remove urgent, back to queue
```

**Config:** Edit `/mnt/c/obs-overlay/config.json` → `ticker_queue` array

### Price Display

```bash
obs-update price full                # $99
obs-update price discount            # $49
obs-update price live                # $29
obs-update price --clear             # Hide price
```

**Config:** Edit `prices` object in config.json

### Quantity Counter

```bash
# Countdown mode (spots remaining)
obs-update qty --set 50 --mode down  # Start at 50
obs-update qty --dec                 # 49 left
obs-update qty --dec                 # 48 left

# Count-up mode (sales tracker)
obs-update qty --set 0 --mode up     # Start at 0
obs-update qty --inc                 # 1 sold
obs-update qty --inc                 # 2 sold

obs-update qty --clear               # Hide counter
```

### Countdown Timer

```bash
obs-update timer --start 30          # Start 30-min countdown
obs-update timer --update            # Update display (cron)
obs-update timer --stop              # Stop & clear
```

**Automation:** Add to crontab:
```bash
*/1 * * * * obs-update timer --update
```

### Status & Control

```bash
obs-update status                    # Show all current values
obs-update clear                     # Clear all overlays
obs-update help                      # Command help
obs-update cheat                     # This cheatsheet
```

## 🎬 Live Stream Workflows

### LinkedIn Live Demo

**Pre-stream (5 min before):**
```bash
obs-update price live                # Set live price
obs-update qty --set 50 --mode down  # 50 spots
obs-update ticker                    # Start ticker rotation

# Auto-rotate ticker every 2 minutes
watch -n 120 obs-update ticker --rotate &
```

**During stream - Someone buys:**
```bash
obs-update qty --dec                 # Update count
```

**Launch urgency offer (30 min remaining):**
```bash
obs-update ticker --push "🔥 NEXT 30 MIN: DOUBLE CREDITS!"
obs-update timer --start 30
obs-update price discount            # Show discount price
```

**Post-stream:**
```bash
killall watch                        # Stop ticker rotation
obs-update clear                     # Clean up
```

### PuPPy Tech Talk

**Pre-talk:**
```bash
obs-update ticker --push "Demo: Prompt → Working App in 15 minutes"
obs-update price --clear             # No pricing for tech talk
obs-update qty --clear
```

**During demo:**
```bash
obs-update ticker --push "Live coding in progress..."
```

**Q&A:**
```bash
obs-update ticker --push "Questions? factumerit.com/demo"
```

### Research Presentation

**Title slide:**
```bash
obs-update ticker --push "Survey of Software • github.com/modelcitizendeveloper"
```

**Code demo:**
```bash
obs-update ticker --push "Live: SEA Pattern Classifier Demo"
```

## 🔄 Automation Examples

### Ticker Auto-Rotation

**Background process (during stream):**
```bash
# Rotate every 2 minutes
watch -n 120 obs-update ticker --rotate &

# Stop when done
killall watch
```

### Timer Updates

**Crontab entry:**
```bash
# Update countdown every minute
*/1 * * * * obs-update timer --update
```

### Quantity Sync from Database

**Cron job (every 5 minutes):**
```bash
*/5 * * * * REMAINING=$(psql $DB_URL -t -c "SELECT COUNT(*) FROM claim_codes WHERE state='available'") && obs-update qty --set $REMAINING
```

## 🎯 Use Cases

### Scarcity Marketing
```bash
obs-update qty --set 100 --mode down  # Start countdown
# Each purchase: obs-update qty --dec
# Shows: "99 left", "98 left", etc.
```

### Social Proof
```bash
obs-update qty --set 0 --mode up      # Count sales
# Each purchase: obs-update qty --inc
# Shows: "1 sold", "2 sold", etc.
```

### Flash Sales
```bash
obs-update timer --start 15           # 15-min flash sale
obs-update ticker --push "⚡ FLASH SALE: 50% OFF!"
obs-update price discount
```

### Multi-Tier Offers
```bash
# Starter tier announcement
obs-update ticker --push "🥉 STARTER: $X - 30 days + $5 credits"
obs-update price full

# Switch to premium
obs-update ticker --push "🥇 PREMIUM: $Z - 1 YEAR + $50 credits"
obs-update price live
```

## 🛠️ Troubleshooting

### OBS Not Showing Updates

1. Verify Text source uses **"Read from file"** mode
2. Check file path: `C:\obs-overlay\ticker.txt` (Windows format)
3. Enable **"Chat log mode"** for auto-refresh

### Commands Not Working

```bash
# Check overlay directory exists
ls /mnt/c/obs-overlay/

# Check config file
cat /mnt/c/obs-overlay/config.json

# Test scripts directly
python ~/gt/research/crew/ivan/tools/obs-overlays/obs-update-ticker.py
```

### Timer Not Counting Down

```bash
# Check if timer started
cat /mnt/c/obs-overlay/config.json | grep timer_end

# Verify cron job running
crontab -l | grep timer

# Manually trigger update
obs-update timer --update
```

## 📁 Files Reference

**Scripts:**
- `~/gt/research/crew/ivan/tools/obs-overlays/obs-update` (main)
- `~/gt/research/crew/ivan/tools/obs-overlays/obs-update-*.py` (individual)

**Overlay Files (read by OBS):**
- `/mnt/c/obs-overlay/ticker.txt`
- `/mnt/c/obs-overlay/price.txt`
- `/mnt/c/obs-overlay/qty.txt`
- `/mnt/c/obs-overlay/timer.txt`

**Config:**
- `/mnt/c/obs-overlay/config.json`

## 🔗 Related Docs

- Full README: `~/gt/research/crew/ivan/tools/obs-overlays/OBS-OVERLAY-README.md`
- LinkedIn Live: `~/gt/solutions/crew/ivan/docs/factumerit/LINKEDIN_LIVE_QUICK_REFERENCE.md`

---

**Quick Access:**
```bash
obs-update cheat        # Show this cheatsheet
obs-update help         # Command reference
obs-update status       # Current state
```
