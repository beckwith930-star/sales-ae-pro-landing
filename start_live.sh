#!/bin/bash
# Start the local server that backs the live dashboard bridge.
#
# Open: http://localhost:8765/agent_command_center.html
# Then click the "○ Live" button in the dashboard top bar.

set -e
cd "$(dirname "$0")"
mkdir -p signal_reports

PORT=${PORT:-8765}

echo ""
echo "╭─────────────────────────────────────────────────────────────╮"
echo "│  Agent Beck · live dashboard bridge                         │"
echo "├─────────────────────────────────────────────────────────────┤"
echo "│  Open:  http://localhost:${PORT}/agent_command_center.html      │"
echo "│  Then:  click ○ Live in the top bar                         │"
echo "│                                                             │"
echo "│  Emit events from another shell:                            │"
echo "│    python3 bin/emit_event.py signal start                   │"
echo "│    python3 bin/emit_event.py signal step \\                  │"
echo "│      --tool salesforce --text \"sf data query · 17 accts\"    │"
echo "│    python3 bin/emit_event.py signal end                     │"
echo "╰─────────────────────────────────────────────────────────────╯"
echo ""

exec python3 -m http.server "$PORT"
