#!/usr/bin/env python3
"""Paced replay of a Signal Monitor run for the live dashboard.

Writes events one at a time to live_events.jsonl with sleep between, so the
dashboard sees natural live cadence (one beam at a time) instead of a burst.
"""
import json, os, sys, time
from datetime import datetime, timezone

EVENTS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "signal_reports", "live_events.jsonl"
)
AGENT = "signal"

STEPS = [
    ("start", None, None,                     1.4),
    ("step", "salesforce", "sf data query · 8 active accounts · 10 open opps", 1.6),
    ("step", None,         "merged · 8 active + 9 priority ICP · 5 public tickers", 1.0),
    ("step", None,         "fanning out across news + SEC + earnings streams", 1.0),
    ("step", "web",        "web.search · Northbridge Industrial · automation + capex", 1.6),
    ("step", "web",        "web.search · Halcyon Power · supply chain investment", 1.6),
    ("step", "web",        "web.search · Meridian Materials · DC modernization", 1.6),
    ("step", "web",        "web.search · Westgate Brands · warehouse automation", 1.8),
    ("step", "web",        "sec.edgar · NRTH · 10-Q most recent filings", 1.6),
    ("step", "web",        "sec.edgar · WSGT · 10-Q + 8-K productivity plan", 1.6),
    ("step", "web",        "earnings · NRTH Q1 2026 transcript pull", 1.8),
    ("step", None,         "dedupe.hash · 11 raw signals · 0 stale · 11 new", 1.0),
    ("step", None,         "llm.score · top score 360 (Halcyon Power Investor Day)", 1.4),
    ("step", None,         "threshold · 8 immediate · 3 this week · 0 monitor", 1.0),
    ("step", "web",        "lead.search · Halcyon Power · VP Operations / Supply Chain", 1.6),
    ("step", "web",        "lead.search · Westgate · VP Supply Chain / COO", 1.6),
    ("step", "linkedin",   "lead.scan · LinkedIn · 5 candidates surfaced", 1.4),
    ("step", None,         "lead.match · 3 HIGH · 2 MEDIUM · 0 LOW confidence", 1.0),
    ("step", "linkedin",   "lead.linkedin.lookup · profile URLs for 5 candidates", 1.4),
    ("step", None,         "lead.linkedin.match · 4 of 5 found · 1 TBD (Sales Nav)", 1.0),
    ("step", "linkedin",   "lead.bonus · 2 additional ops/CI leaders surfaced", 1.2),
    ("step", "salesforce", "sf lead create queued · 5 new prospects (no auto-create)", 1.2),
    ("step", "gmail",      "gmail draft · Halcyon Power Investor Day · created", 1.4),
    ("step", "gmail",      "gmail draft · Halcyon Q2 expansion · created", 1.4),
    ("step", "gmail",      "gmail draft · Westgate productivity plan · created", 1.4),
    ("step", "salesforce", "sf activity log · 3 records pinned", 1.2),
    ("step", None,         "fs.write · signal_reports/2026-05-04_signal_report.md · 128 lines", 1.0),
    ("end",  None, None,                       0),
]


def emit(event, tool, text):
    ev = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "agent": AGENT,
        "event": event,
    }
    if tool: ev["tool"] = tool
    if text: ev["text"] = text
    os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(ev) + "\n")
    return ev


def main():
    # Truncate the events file so this run starts clean
    open(EVENTS_FILE, "w").close()
    total = len(STEPS)
    for i, (event, tool, text, sleep_s) in enumerate(STEPS, 1):
        ev = emit(event, tool, text)
        label = f"{event}" + (f" → {tool}" if tool else "") + (f": {text[:50]}" if text else "")
        # stdout flushes immediately so Monitor sees one line per event
        print(f"[{i:02d}/{total}] {label}", flush=True)
        if sleep_s > 0:
            time.sleep(sleep_s)
    print(f"DONE · {total} events emitted", flush=True)


if __name__ == "__main__":
    main()
