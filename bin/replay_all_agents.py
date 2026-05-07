#!/usr/bin/env python3
"""Fire all 7 agents in sequence so the entire constellation lights up.

Pacing: stagger starts ~1.5s apart so each command-received banner is visible,
then weave step events from all 7 agents, then end them all.
"""
import json, os, time, random
from datetime import datetime, timezone

EVENTS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "signal_reports", "live_events.jsonl"
)

AGENTS = [
    ("signal",   "Daily Signal Monitor"),
    ("friday",   "Friday Pipeline"),
    ("sunday",   "Sunday 1:1 Update"),
    ("postcall", "Post-Call Processor"),
    ("email",    "Email Outreach"),
    ("linkedin", "LinkedIn DMs"),
    ("intel",    "Prospect Intel"),
]

# A small library of believable step events per agent for the demo phase
STEPS = {
    "signal":   [("salesforce","sf data query · 17 active accounts"),
                 ("web","web.search · NRTH · automation"),
                 ("web","sec.edgar · WSGT · 10-Q"),
                 ("gmail","gmail draft · 4 signals queued")],
    "friday":   [("salesforce","sf data query · 11 open opps"),
                 ("gmail","gmail.search · 47 threads"),
                 ("slack","slack.history · 22 msgs · 9 channels"),
                 ("salesforce","sf apex · 7 NextStep updates")],
    "sunday":   [("salesforce","sf data query · 10 active opps"),
                 ("gmail","gmail.search · 31 hits this week"),
                 ("slack","slack.history · 18 #discovery msgs"),
                 ("chrome","docs.insert · 1:1 doc updated")],
    "postcall": [("web","webhook · meeting notes received"),
                 ("salesforce","sf data query · Account match"),
                 ("salesforce","sf apex · LeadConvert + Opp"),
                 ("gmail","gmail draft · recap + pricing"),
                 ("slack","slack post · #discovery-* · 1 reaction")],
    "email":    [("salesforce","sf data query · enrichment"),
                 ("web","web.search · pain mapped"),
                 ("gmail","gmail draft · PDF + signature"),
                 ("salesforce","sf task created")],
    "linkedin": [("linkedin","linkedin.search · 1 hit"),
                 ("chrome","browser.open · profile · Connect"),
                 ("linkedin","invite.send · 195/300 chars"),
                 ("salesforce","sf task · pending_acceptance")],
    "intel":    [("web","web.search · 4 queries · 22 results"),
                 ("linkedin","linkedin.profile · 4yr tenure"),
                 ("web","sec.10k · turnaround read"),
                 ("salesforce","sf attach · brief pinned"),
                 ("chrome","docs.append · research_briefs")],
}


def emit(agent_id, event, tool=None, text=None):
    ev = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "agent": agent_id, "event": event,
    }
    if tool: ev["tool"] = tool
    if text: ev["text"] = text
    os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)
    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(ev) + "\n")


def main():
    open(EVENTS_FILE, "w").close()
    rng = random.Random(42)

    # Phase 1 — staggered starts so each command-flash banner is visible
    print("=== PHASE 1: starts (staggered command-received flashes) ===", flush=True)
    for i, (aid, name) in enumerate(AGENTS, 1):
        emit(aid, "start")
        print(f"  [{i}/{len(AGENTS)}] start · {name}", flush=True)
        time.sleep(1.6)

    # Phase 2 — weave step events from all 7 agents in random order
    print("=== PHASE 2: weaving steps from all 7 ===", flush=True)
    work = []
    for aid, _name in AGENTS:
        for tool, text in STEPS[aid]:
            work.append((aid, tool, text))
    rng.shuffle(work)
    total = len(work)
    for i, (aid, tool, text) in enumerate(work, 1):
        emit(aid, "step", tool=tool, text=text)
        print(f"  [{i:02d}/{total}] {aid:8s} → {tool:10s} · {text[:50]}", flush=True)
        time.sleep(0.55)

    # Phase 3 — end all
    print("=== PHASE 3: ends ===", flush=True)
    for aid, name in AGENTS:
        emit(aid, "end")
        print(f"  end · {name}", flush=True)
        time.sleep(0.45)

    print(f"DONE · all 7 agents cycled · {sum(1 for _ in open(EVENTS_FILE))} events", flush=True)


if __name__ == "__main__":
    main()
