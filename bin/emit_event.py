#!/usr/bin/env python3
"""Emit a live event to the agent_command_center dashboard JSONL feed.

Usage:
  emit_event.py <agent> start
  emit_event.py <agent> step --tool salesforce --text "sf data query · 17 accounts"
  emit_event.py <agent> end

agent       one of: signal, friday, sunday, postcall, email, linkedin, intel
--tool      optional planet to fire a beam toward:
              salesforce | gmail | slack | linkedin | chrome | web
--text      free-form telemetry line (shown in dashboard transcript)
--file      override the events file path
              (default: <product>/signal_reports/live_events.jsonl, resolved relative to this script)
"""
import argparse
import json
import os
from datetime import datetime, timezone

DEFAULT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "signal_reports", "live_events.jsonl"
)

VALID_AGENTS = {"signal", "friday", "sunday", "postcall", "email", "linkedin", "intel"}
VALID_TOOLS = {"salesforce", "gmail", "slack", "linkedin", "chrome", "web", "techcrunch", "wired"}
VALID_EVENTS = {"start", "step", "end"}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("agent", help=f"agent id (one of: {', '.join(sorted(VALID_AGENTS))})")
    p.add_argument("event", choices=sorted(VALID_EVENTS))
    p.add_argument("--tool", default=None, help=f"target tool/planet (one of: {', '.join(sorted(VALID_TOOLS))})")
    p.add_argument("--text", default="", help="telemetry line text")
    p.add_argument("--file", default=DEFAULT_FILE, help="events file path")
    args = p.parse_args()

    if args.agent not in VALID_AGENTS:
        p.error(f"unknown agent {args.agent!r}; valid: {sorted(VALID_AGENTS)}")
    if args.tool and args.tool not in VALID_TOOLS:
        p.error(f"unknown tool {args.tool!r}; valid: {sorted(VALID_TOOLS)}")

    ev = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "agent": args.agent,
        "event": args.event,
    }
    if args.tool:
        ev["tool"] = args.tool
    if args.text:
        ev["text"] = args.text

    os.makedirs(os.path.dirname(args.file), exist_ok=True)
    with open(args.file, "a") as f:
        f.write(json.dumps(ev) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
