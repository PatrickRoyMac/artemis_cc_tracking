# Artemis II — Claude Code Status Bar

While Artemis II is flying to the Moon right now, why not track it live from your terminal?

This adds a real-time mission tracker to the bottom of Claude Code — showing Artemis's distance from Earth and Moon, its proportional position on the Earth→Moon track, speed, and whether it's approaching or receding.

```
🌍 347,837 km ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦  🚀← ✦ ✦ ✦  104,695 km 🌙  ⚡0.711 km/s
```

The ✦ dots shift in real-time as Artemis moves. The ← flips to → when it's heading back toward Earth.

Data pulled directly from [NASA's JPL Horizons API](https://ssd.jpl.nasa.gov/horizons/), cached every 5 minutes.

---

## Install (one line)

```bash
curl -fsSL https://raw.githubusercontent.com/PatrickRoyMac/artemis_cc_tracking/main/install.sh | bash
```

Then restart Claude Code. That's it.

**Requirements:** Python 3, Claude Code. No pip installs — pure stdlib.

---

## How it works

- Queries JPL Horizons twice per refresh — once centered on Earth, once on the Moon — to get surface distances for both
- Extracts the range-rate vector to determine approach direction (← or →)
- Renders position proportionally across a 14-character ✦ track
- Writes to `~/.claude/artemis_cache.json` so it's instant on repeated renders

## Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/PatrickRoyMac/artemis_cc_tracking/main/uninstall.sh | bash
```
