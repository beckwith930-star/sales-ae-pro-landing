#!/usr/bin/env python3
"""Paced replay of a Sunday 1:1 Update run for the live dashboard."""
import json, os, time
from datetime import datetime, timezone

EVENTS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "signal_reports", "live_events.jsonl"
)
AGENT = "sunday"

STEPS = [
    ("start", None, None,                                                              1.4),
    ("step", "salesforce", "sf data query · 10 open opportunities",                     1.6),
    ("step", "gmail",      "gmail.search · 31 hits this week",                          1.6),
    ("step", "slack",      "slack.history · 18 #discovery messages",                    1.4),
    ("step", None,         "llm.synthesize · 7 account sections drafted",               1.6),
    ("step", None,         "awaiting approval ... approved (Brandon edits applied)",    1.8),
    ("step", "chrome",     "docs.insert · pinned at top of 1:1 doc",                    1.4),
    ("end",  None, None,                                                                0),
]


def emit(event, tool, text):
    ev = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "agent": AGENT, "event": event,
    }
    if tool: ev["tool"] = tool
    if text: ev["text"] = text
    os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(ev) + "\n")


def main():
    open(EVENTS_FILE, "w").close()
    total = len(STEPS)
    for i, (event, tool, text, sleep_s) in enumerate(STEPS, 1):
        emit(event, tool, text)
        label = f"{event}" + (f" → {tool}" if tool else "") + (f": {text[:50]}" if text else "")
        print(f"[{i:02d}/{total}] {label}", flush=True)
        if sleep_s > 0:
            time.sleep(sleep_s)
    print(f"DONE · {total} events emitted", flush=True)


if __name__ == "__main__":
    main()
