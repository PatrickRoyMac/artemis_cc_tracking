#!/bin/bash
set -e

echo ""
echo "🗑️  Uninstalling Artemis II tracker..."
echo ""

# Remove the script
rm -f "$HOME/.claude/scripts/artemis_status.py"
echo "✓ Removed artemis_status.py"

# Remove cache
rm -f "$HOME/.claude/artemis_cache.json"
echo "✓ Removed cache"

# Remove statusLine from settings.json
python3 - <<'PYEOF'
import json, os

settings_file = os.path.expanduser("~/.claude/settings.json")

if not os.path.exists(settings_file):
    print("✓ No settings.json found — nothing to clean up")
    exit()

with open(settings_file) as f:
    settings = json.load(f)

if "statusLine" in settings:
    del settings["statusLine"]
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=2)
    print("✓ Removed statusLine from ~/.claude/settings.json")
else:
    print("✓ statusLine already absent from settings.json")
PYEOF

echo ""
echo "✅ Done! Restart Claude Code to apply."
echo ""
