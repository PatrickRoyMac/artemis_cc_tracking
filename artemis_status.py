#!/usr/bin/env python3
"""Artemis II Claude Code status bar widget.
Fetches real-time position from NASA's JPL Horizons API.
Results are cached for 5 minutes to avoid hammering the API.

Output (single line for Claude Code status bar):
  🌍 347,837 km ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦  🚀← ✦ ✦ ✦  104,695 km 🌙  ⚡0.711 km/s
"""
import re
import math
import json
import os
from datetime import datetime, timedelta, timezone
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError

CACHE_FILE = os.path.expanduser("~/.claude/artemis_cache.json")
CACHE_TTL_SECONDS = 300   # 5 minutes
MOON_RADIUS_KM = 1737.4
EARTH_RADIUS_KM = 6371.0
JPL_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
TRACK_LEN = 14


def fetch_from_center(center, body_radius_km):
    now = datetime.now(timezone.utc)
    start = now.strftime('%Y-%m-%d %H:%M')
    stop = (now + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M')

    params = urlencode({
        'format': 'json',
        'COMMAND': "'-1024'",   # Artemis II / Orion SPKID
        'MAKE_EPHEM': 'YES',
        'EPHEM_TYPE': 'VECTORS',
        'CENTER': f"'{center}'",
        'START_TIME': f"'{start}'",
        'STOP_TIME': f"'{stop}'",
        'STEP_SIZE': '1m',
        'CSV_FORMAT': 'YES',
    })

    with urlopen(f"{JPL_URL}?{params}", timeout=12) as resp:
        data = json.loads(resp.read().decode())

    if 'error' in data:
        return None

    raw = data.get('result', '')
    m = re.search(r'\$\$SOE(.*?)\$\$EOE', raw, re.DOTALL)
    if not m:
        return None

    line = m.group(1).strip().split('\n')[0]
    cols = [c.strip() for c in line.split(',')]
    if len(cols) < 11:
        return None

    x, y, z = float(cols[2]), float(cols[3]), float(cols[4])
    vx, vy, vz = float(cols[5]), float(cols[6]), float(cols[7])
    rr = float(cols[10])  # range-rate: negative = approaching, positive = receding

    dist_km = math.sqrt(x**2 + y**2 + z**2)
    surface_km = dist_km - body_radius_km
    speed_km_s = math.sqrt(vx**2 + vy**2 + vz**2)
    return round(surface_km), round(speed_km_s, 3), round(rr, 3)


def load_cache():
    try:
        if not os.path.exists(CACHE_FILE):
            return None
        with open(CACHE_FILE) as f:
            data = json.load(f)
        ts = datetime.fromisoformat(data['ts'])
        if (datetime.now(timezone.utc) - ts).total_seconds() < CACHE_TTL_SECONDS:
            return data
    except Exception:
        pass
    return None


def save_cache(earth_km, moon_km, speed, rr):
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump({
                'ts': datetime.now(timezone.utc).isoformat(),
                'earth_km': earth_km,
                'moon_km': moon_km,
                'speed': speed,
                'rr': rr,
            }, f)
    except Exception:
        pass


def fmt(km):
    return f"{int(km):,}"


def build_track(earth_km, moon_km, arrow):
    """Place 🚀 proportionally on an Earth→Moon track of ✦ dots."""
    total = earth_km + moon_km
    earth_dots = max(1, round(earth_km / total * TRACK_LEN))
    moon_dots  = max(1, TRACK_LEN - earth_dots)
    left  = ' ✦' * earth_dots
    right = ' ✦' * moon_dots
    return f"{left}  🚀{arrow}{right}"


def main():
    cache = load_cache()
    if cache:
        earth_km = cache['earth_km']
        moon_km  = cache['moon_km']
        speed    = cache['speed']
        rr       = cache.get('rr', 0)
    else:
        try:
            earth_result = fetch_from_center('500@399', EARTH_RADIUS_KM)
            moon_result  = fetch_from_center('500@301', MOON_RADIUS_KM)
        except (URLError, Exception):
            print("🚀 A-II: offline")
            return

        if not earth_result or not moon_result:
            print("🚀 A-II: no data")
            return

        earth_km, speed, rr = earth_result
        moon_km, _, _       = moon_result
        save_cache(earth_km, moon_km, speed, rr)

    # ← approaching Earth, → heading toward Moon
    arrow = "←" if rr < 0 else "→"
    track = build_track(earth_km, moon_km, arrow)

    print(f"🌍 {fmt(earth_km)} km{track}  {fmt(moon_km)} km 🌙  ⚡{speed} km/s")


if __name__ == '__main__':
    main()
