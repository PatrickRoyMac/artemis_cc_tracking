# artemis_cc_tracking

Real-time Artemis II mission tracker as a Claude Code status bar widget.

Shows live distance from Earth & Moon, Artemis's proportional position on the Earth→Moon track, speed, and approach direction — all in a slim single line at the bottom of Claude Code.

```
🌍 347,837 km ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦  🚀← ✦ ✦ ✦  104,695 km 🌙  ⚡0.711 km/s
```

- **✦ dots** — proportional position between Earth and Moon
- **← / →** — approaching Earth or heading toward Moon
- **⚡** — geocentric speed in km/s
- Data from [NASA JPL Horizons API](https://ssd.jpl.nasa.gov/horizons/), cached 5 min

## Setup

**1. Copy the script**
```bash
cp artemis_status.py ~/.claude/scripts/artemis_status.py
```

**2. Add the status line to `~/.claude/settings.json`**
```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/scripts/artemis_status.py"
  }
}
```

**3. Restart Claude Code** — the bar appears at the bottom under the input.

## Requirements

- Python 3 (stdlib only — no pip installs needed)
- Claude Code
