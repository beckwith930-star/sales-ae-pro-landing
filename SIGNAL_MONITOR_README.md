# 🛰️ Signal Monitor

**Daily buying-signal scan for enterprise AEs. News, SEC filings, LinkedIn job postings, saved-contact social, and earnings — scored, deduped, and turned into draft outreach every morning before you sit down at your desk.**

> Built into [Sales AE Pro](./README.md). Runs on Claude Code with the Anthropic Salesforce MCP server.

---

## What it does

Every weekday at **07:00 local time**, Signal Monitor:

1. Pulls your active account list from Salesforce
2. Scans 5 source streams in parallel for buying signals tied to those accounts
3. Dedupes anything you already saw this week
4. Scores each signal `(Type × Contact × Fit × Recency) / 10`
5. Drafts a personalized email or LinkedIn DM for every signal scoring ≥ 20
6. Writes a daily Markdown report to `signal_reports/YYYY-MM-DD.md`
7. Pins an activity-history note to the matching Account/Opportunity

Your Gmail Drafts folder fills up with high-context outreach. You review, edit, hit send. **Nothing is ever sent automatically.**

---

## Why it works

Most AEs find signals by accident — a colleague forwards a LinkedIn post, an SDR mentions an earnings call. Signal Monitor flips that:

- **Catches signals first.** A new "VP Revenue Operations" job posting at a target account is worth more on day 1 than day 7.
- **Forces relevance into every touch.** No more "just checking in" emails. Every draft cites a specific public signal with a source URL.
- **Prioritizes by math, not vibes.** A scored queue prevents the loudest signal (yesterday's news article) from drowning out the highest-leverage one (a job posting from a Director of Operations).

---

## The scoring matrix

```
Signal Score = (Type × Contact × Fit × Recency) / 10
```

| Dimension | Value | Weight |
|---|---|---|
| **Type** | competitor loss / earnings mention | 9 |
|  | job posting at target account | 8 |
|  | LinkedIn engagement by decision-maker | 7 |
|  | social post by saved contact | 6 |
|  | news article | 5 |
|  | conference attendance | 4 |
| **Contact level** | C-suite | 10 |
|  | VP | 8 |
|  | Director | 6 |
|  | Manager | 4 |
|  | Unknown / no contact mapped | 2 |
| **Account fit** | existing target account | 10 |
|  | matches ICP perfectly | 8 |
|  | adjacent fit | 5 |
|  | weak fit | 2 |
| **Recency** | today | 10 |
|  | this week | 7 |
|  | this month | 4 |
|  | older | 1 |

**Action thresholds:**

| Score | Action |
|---|---|
| **> 40** | Immediate. Draft outreach today, top of the queue. |
| **20 – 40** | This week. Drop into the upcoming touches list. |
| **< 20** | Log and monitor. No outreach this cycle. |

The math is shown for every signal in the daily report so you (or your manager) can challenge any score.

---

## Source streams

| Stream | What it scans | Tool |
|---|---|---|
| **News + editorial** | Google News, TechCrunch, WIRED, Reuters, plus whatever trade pubs you list in your vertical pack (Crunchbase + The Information for SaaS, Fierce Pharma + Modern Healthcare for life sciences, Finextra for fintech, Industry Week for industrial — bring your own) | `WebSearch` + `WebFetch` |
| **SEC + earnings** | SEC EDGAR (10-K, 10-Q, 8-K), earnings call transcripts, IR press release feeds | `WebFetch` to EDGAR |
| **LinkedIn jobs** | Sales Navigator saved-search alerts, last 24 hours, your job-keyword list | Chrome MCP |
| **Saved-contact social** | LinkedIn feed of your champions + economic buyers + tradeshow connections, last 24 hours | Chrome MCP |
| **(Pluggable)** | Add your own — Crunchbase, G2, Glassdoor, etc. via the source adapter pattern | Custom |

---

## Sample report excerpt

```markdown
# Signal Report — 2026-05-04

## Run summary
- Accounts scanned: 17 (priority) + 42 (ICP)
- Sources: news (4), SEC (2), LinkedIn jobs (1), social (1)
- Total raw signals: 22 | Top of queue: 4 | This week: 7 | Monitor: 7
- Run duration: 11.7s

## Top of queue (score > 40) — IMMEDIATE

### Acme Industrial · job posting · score 51.2 = (8 × 10 × 10 × 8) / 10
- Detail: "Warehouse Automation Engineer · Midwest DC" posted 2026-05-03
  → https://www.linkedin.com/jobs/view/...
- Recommended action: email
- Linked SF: Opp 006xxx00000XXXXX (Acme Industrial — ILC Racks pilot)
- Draft: gmail://drafts/d:r-12345 (subject: "Saw the automation role — quick thought")

[...]

## Hash log (for dedupe)
- 8a3f...c2e1 (Acme · job posting · 2026-05-03)
- b91e...d7c0 (Highland Pharma · 10-Q · 2026-05-02)
```

---

## Vertical packs

Signal Monitor is vertical-agnostic. Scoring, dedupe, and orchestration are all generic. What you tune for your market is the **keywords and trade-pub sources** — that bundle is a *vertical pack*.

Pick one of the example packs to start, or write your own:

| Pack | Example ICP signals | Example job titles | Example trade sources |
|---|---|---|---|
| **SaaS / dev tools** | seed-to-Series funding, headcount growth, platform consolidation | VP Eng, RevOps, Head of Data | Crunchbase, The Information, TechCrunch |
| **Fintech / payments** | new banking license, regulatory action, partnerships | Head of Risk, VP Compliance, Treasury | Finextra, American Banker, PYMNTS |
| **Healthcare / pharma** | FDA filings, clinical-trial milestones, M&A | VP Clinical Ops, Director of Quality | Fierce Pharma, Modern Healthcare, Endpoints |
| **Industrial / supply chain** | DC capex, automation initiatives, labor changes | VP Supply Chain, Director of Operations | Industry Week, Supply Chain Dive |
| **Your market** | *the pains your buyers actually name in discovery* | *the titles your champion actually has* | *the 2–3 pubs your buyers actually read* |

Packs live in `config/packs/`. Copy one to `config/signal_monitor.json` and edit your priority accounts on top.

---

## Configuration

`config/signal_monitor.json` schema. The `icp_keywords` and `job_keywords` come from your vertical pack — see above.

```json
{
  "priority_accounts": [
    "Your Account A",
    "Your Account B",
    "Your Account C"
  ],
  "icp_keywords": [
    "<pain your buyers name in discovery>",
    "<strategic initiative your champion is funding>",
    "<competitor or category-defining keyword>",
    "<regulatory or financial pressure>"
  ],
  "job_keywords": [
    "<title that signals your champion is hiring>",
    "<title that signals a new initiative in your category>",
    "<title that signals a competitor is being replaced>"
  ],
  "saved_contact_handles": [
    "linkedin.com/in/your-champion-1",
    "linkedin.com/in/your-champion-2"
  ],
  "public_tickers": [
    { "ticker": "ACME", "account": "Acme Industrial" }
  ],
  "schedule": "Mon-Fri 07:00 PT",
  "thresholds": { "immediate": 40, "this_week": 20 },
  "dedupe_window_days": 7,
  "skip_holidays": true,
  "auto_send": false
}
```

`auto_send` is **always false** by design. Drafts only.

---

## Privacy & safety guarantees

- **No automated sending.** Every outreach artifact is a Gmail Draft or a markdown queue entry. The human pulls every send trigger.
- **Source-cited.** Every signal in the report includes a verifiable source URL. No hallucinated job postings or earnings quotes.
- **7-day dedupe.** A signal hash log prevents the same news article or job posting from cluttering your queue all week.
- **Weekend + US holiday skip.** No Sunday-night reports.
- **Rate-limit safe.** LinkedIn scans use Sales Nav saved alerts (a paid feature you control) rather than scraping public pages — keeps you in good standing with LI ToS.

---

## Quick start

```bash
# 1. Install Sales AE Pro
git clone https://github.com/beckwith930-star/sales-ae-pro-plugin.git
cd sales-ae-pro

# 2. Configure your accounts + keywords
cp config/signal_monitor.example.json config/signal_monitor.json
$EDITOR config/signal_monitor.json

# 3. Wire up Salesforce MCP (one-time)
claude mcp add salesforce <your-instance-url>

# 4. First manual run
claude run signal-monitor

# 5. Schedule daily
claude schedule signal-monitor "0 7 * * 1-5"
```

After the first run:
- Open `signal_reports/YYYY-MM-DD_signal_report.md` for the readable daily output
- Open Gmail → Drafts to review the high-priority outreach drafts
- Edit, send, move on

---

## Live demo

Watch the agent execute in your browser: **[demo/agent_command_center.html](./demo/agent_command_center.html)**

Pick "Daily Signal Monitor" from the agent list, hit **Run agent**, and watch the 14-node graph light up node-by-node as each tool call completes. The transcript on the right streams every step in real time.

---

## What's coming

- **Slack notifier** — optional 07:30 PT message to a private Slack channel summarizing the top 3 immediate-action signals
- **More example packs** — partner-channel sales, public sector, education, ESG/climate
- **Signal feedback loop** — mark drafts as "sent + replied" / "sent + ignored" / "skipped" and let the scoring model learn your hit rate over time

PRs welcome. Open an issue if you want a source adapter for your stack.

---

## License

MIT — same as the rest of Sales AE Pro.

---

*Built by an AE who got tired of finding out about job postings at target accounts a week late.*
