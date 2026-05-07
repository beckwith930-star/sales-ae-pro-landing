# Sales AE Pro — Landing Site

Marketing site and live agent-constellation demo for the [Sales AE Pro Claude Code plugin](https://github.com/beckwith930-star/sales-ae-pro-plugin).

**Live site:** https://beckwith930-star.github.io/sales-ae-pro-landing/

## What's in here

- `index.html` — the landing page (hero animation, agent grid, CTAs)
- `demo/agent_command_center.html` — the interactive 3D agent constellation
- `bin/` — paced replay scripts that drive the dashboard's live event feed for the demo
- `SIGNAL_MONITOR_README.md` — deep-dive doc for the Daily Signal Monitor agent
- `start_live.sh` — local dev server for testing the landing + demo locally

## Run locally

```bash
bash start_live.sh
# then open http://localhost:8765/
```

To see the agent constellation animate, in a second terminal:

```bash
python3 bin/replay_signal.py     # one agent
# or
python3 bin/replay_all_agents.py # all seven
```

The replay writes events to `signal_reports/live_events.jsonl`, which the dashboard reads when you click the **○ Live** button in the top bar.

## License

MIT — see [LICENSE](./LICENSE).
