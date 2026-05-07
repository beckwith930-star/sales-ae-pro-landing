#!/usr/bin/env python3
"""Paced replay of a Friday Pipeline Update run for the live dashboard."""
import json, os, time
from datetime import datetime, timezone

EVENTS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "signal_reports", "live_events.jsonl"
)
AGENT = "friday"

STEPS = [
    ("start", None, None,                                                              1.4),
    ("step", "salesforce", "sf data query · 11 open opportunities · 182ms",             1.6),
    ("step", None,         "fanning out across 11 accounts",                            1.0),
    ("step", "gmail",      "gmail.search · 47 threads since last Friday",               1.6),
    ("step", "slack",      "slack.history · 22 messages · 9 channels",                  1.4),
    ("step", None,         "llm.synthesize · 7 Next Step proposals",                    1.4),
    ("step", None,         "awaiting approval ... approved with 3 inline edits",        1.8),
    ("step", "salesforce", "sf apex run · 7 Opportunities updated",                     1.4),
    ("step", None,         "fs.write · weekly_pipeline_2026-WW.md",                     1.0),
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
