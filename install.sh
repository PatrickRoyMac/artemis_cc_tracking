#!/bin/bash
set -e

SCRIPT_DIR="$HOME/.claude/scripts"
SCRIPT_URL="https://raw.githubusercontent.com/PatrickRoyMac/artemis_cc_tracking/main/artemis_status.py"

echo ""
echo "🚀 Installing Artemis II tracker for Claude Code..."
echo ""

# Create scripts dir if needed
mkdir -p "$SCRIPT_DIR"

# Download the tracker script
curl -fsSL "$SCRIPT_URL" -o "$SCRIPT_DIR/artemis_status.py"
echo "✓ Downloaded artemis_status.py → ~/.claude/scripts/"

# Merge statusLine into settings.json (preserves existing config)
python3 - <<'PYEOF'
import json, os

settings_file = os.path.expanduser("~/.claude/settings.json")

if os.path.exists(settings_file):
    with open(settings_file) as f:
        settings = json.load(f)
else:
    settings = {}

settings["statusLine"] = {
    "type": "command",
    "command": "python3 ~/.claude/scripts/artemis_status.py"
}

with open(settings_file, "w") as f:
    json.dump(settings, f, indent=2)

print("✓ Updated ~/.claude/settings.json")
PYEOF

echo ""
echo "✅ Done! Restart Claude Code to activate."
echo ""
echo "   🌍 347,837 km ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦  🚀← ✦ ✦ ✦  104,695 km 🌙  ⚡0.711 km/s"
echo ""
