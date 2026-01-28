# OBS Overlay Control Scripts

Control text overlays in OBS by updating text files in `/mnt/c/obs-overlay/`.

## Files

**Scripts (Linux/WSL):**
- `~/obs-update-ticker.py` - Rotating ticker messages
- `~/obs-update-price.py` - Price display (full/discount/live tiers)
- `~/obs-update-qty.py` - Quantity counter (countdown or count-up)
- `~/obs-update-timer.py` - Countdown timer for urgency

**Overlay Files (Windows - read by OBS):**
- `/mnt/c/obs-overlay/ticker.txt` - Current ticker message
- `/mnt/c/obs-overlay/price.txt` - Current price
- `/mnt/c/obs-overlay/qty.txt` - Current quantity
- `/mnt/c/obs-overlay/timer.txt` - Countdown timer
- `/mnt/c/obs-overlay/config.json` - Configuration

## Quick Start

### Ticker Messages

```bash
# Update ticker with first message from queue
python ~/obs-update-ticker.py

# Rotate to next message in queue
python ~/obs-update-ticker.py --rotate

# Push urgent message (overrides queue)
python ~/obs-update-ticker.py --push "🔥 LIMITED TIME: 50% OFF!"

# Pop urgent message (return to queue)
python ~/obs-update-ticker.py --pop
```

### Price Display

```bash
# Show full price ($99)
python ~/obs-update-price.py full

# Show discount price ($49)
python ~/obs-update-price.py discount

# Show live-only price ($29)
python ~/obs-update-price.py live

# Clear price display
python ~/obs-update-price.py --clear
```

### Quantity Counter

```bash
# Initialize countdown mode with 50 remaining
python ~/obs-update-qty.py --set 50 --mode down

# Someone bought one (decrement)
python ~/obs-update-qty.py --decrement

# Switch to count-up mode (sales counter)
python ~/obs-update-qty.py --set 0 --mode up
python ~/obs-update-qty.py --increment  # Each sale

# Clear display
python ~/obs-update-qty.py --clear
```

### Countdown Timer

```bash
# Start 30-minute "Act Now" timer
python ~/obs-update-timer.py --start 30

# Update display (run from cron every minute)
*/1 * * * * python ~/obs-update-timer.py --update

# Stop timer
python ~/obs-update-timer.py --stop
```

## Live Stream Workflow

### Pre-Stream Setup

```bash
# Set initial ticker
python ~/obs-update-ticker.py

# Set starting price
python ~/obs-update-price.py live

# Set available quantity
python ~/obs-update-qty.py --set 50 --mode down
```

### During Stream

```bash
# Rotate ticker every few minutes
watch -n 120 python ~/obs-update-ticker.py --rotate

# Someone buys
python ~/obs-update-qty.py --decrement

# Launch urgency offer
python ~/obs-update-ticker.py --push "🔥 NEXT 30 MIN: DOUBLE CREDITS!"
python ~/obs-update-timer.py --start 30
python ~/obs-update-price.py discount

# Cron updates timer every minute
# */1 * * * * python ~/obs-update-timer.py --update
```

### Post-Stream Cleanup

```bash
# Clear all displays
python ~/obs-update-ticker.py --pop
python ~/obs-update-price.py --clear
python ~/obs-update-qty.py --clear
python ~/obs-update-timer.py --stop
```

## Configuration

Edit `/mnt/c/obs-overlay/config.json`:

```json
{
  "prices": {
    "full": 99,
    "discount": 49,
    "live": 29
  },
  "qty_mode": "down",
  "qty_value": 50,
  "ticker_delimiter": " • ",
  "ticker_queue": [
    "FACTUM ERIT ... it will have been done ... Join the waiting list at https://factumerit.com ... ",
    "🤖 AI-powered task management ... Talk to @eis in Slack/Matrix ... ",
    "🎁 Limited time offer - ask me for details! ..."
  ],
  "ticker_push_stack": []
}
```

## OBS Setup

1. Add **Text (FreeType 2)** sources for each overlay file:
   - Ticker: `C:\obs-overlay\ticker.txt`
   - Price: `C:\obs-overlay\price.txt`
   - Quantity: `C:\obs-overlay\qty.txt`
   - Timer: `C:\obs-overlay\timer.txt`

2. Enable **"Read from file"** and **"Chat log mode"** for auto-updates

3. Style text with fonts, colors, outlines as desired

4. Position in scene (bottom ticker, corner price, etc.)

## Automation

### Ticker Rotation (every 2 minutes)

```bash
*/2 * * * * python ~/obs-update-ticker.py --rotate
```

### Timer Updates (every minute)

```bash
*/1 * * * * python ~/obs-update-timer.py --update
```

### Quantity Sync (from claim code status)

```bash
*/5 * * * * REMAINING=$(./claim-code-status linkedin-live-batch | grep Available | awk '{print $2}') && python ~/obs-update-qty.py --set $REMAINING
```

## Troubleshooting

**OBS not showing updates:**
- Verify file paths use Windows format: `C:\obs-overlay\file.txt`
- Enable "Read from file" in Text source properties
- Check file permissions (scripts run as WSL user)

**Config.json not found:**
- Scripts expect `/mnt/c/obs-overlay/config.json`
- Create directory: `mkdir -p /mnt/c/obs-overlay`
- Initialize config with prices and ticker_queue

**Timer not counting down:**
- Ensure cron job runs: `*/1 * * * * python ~/obs-update-timer.py --update`
- Check timer started: `cat /mnt/c/obs-overlay/config.json | grep timer_end`

## Related Documentation

- `~/gt/solutions/crew/ivan/docs/factumerit/LINKEDIN_LIVE_QUICK_REFERENCE.md`
- `/mnt/c/obs-overlay/config.json`
