# DailyBriefing

An **open, config-driven, personal daily briefing** that arrives every morning in your
inbox, Google Drive, and Obsidian vault — tailored to whatever you care about. Built
on scheduled LLM agents and an Obsidian-backed memory graph that keeps briefings
fresh as your archive grows.

**Status:** working prototype, actively used, Anthropic-runtime only (see
[*LLM Compatibility*](#llm-compatibility) below).

---

## What It Does

Every day at a time you choose, a fleet of LLM subagents researches the topics you
define — news, science, sports, hobbies, anything — each behind its own source
allowlist and filter rules. A curator synthesizes their output, deduplicates
against recent briefings via the Obsidian graph, and writes:

- a Markdown file (Obsidian-ready, with frontmatter tags and `[[backlinks]]`)
- a styled PDF (modern editorial design, customizable)

The result is committed to your private Git repo, uploaded to Google Drive, and
emailed to you as a PDF attachment.

## Why It's Different

- **Fully config-driven.** No hardcoded topics. Your `config/sections.yml` defines
  everything: sources, filters, political-bias handling, output length.
- **Bias-aware research.** Multi-lens mode dispatches parallel subagents (e.g.
  left / center / right, or any custom frames) and a synthesizer combines them.
  Modes: `balanced-consensus`, `highlight-conflicts`, `raw-all`.
- **Obsidian as memory.** Each briefing gets YAML tags + covered-topic slugs.
  The curator grep-scans recent briefings to avoid repetition and adds
  `[[YYYY-MM-DD]]` backlinks for ongoing stories. The archive becomes a searchable
  topic-graph, not just a pile of files.
- **Variable scope.** Set a verbosity default per user, override per section,
  or let the curator decide per item (`variable-by-impact` — one sentence for
  routine news, multi-page deep-dives for world-changing events).
- **Delivery-agnostic.** Git / Drive / Email / (Slack, Telegram planned) — mix
  and match.

## Architecture

```
[Scheduled trigger] ──> clones repo, reads config/prompts/orchestrator.md
       │
       ├── Parse config/*.yml
       │
       ├── Recent-coverage scan (grep last 14 days of Daily/*.md)
       │
       ├── For each enabled section:
       │     single-lens → 1 research subagent
       │     multi-lens  → N parallel subagents + synthesizer
       │
       ├── Curator assembles, dedups using Obsidian memory,
       │   writes Daily/YYYY-MM-DD.md + frontmatter + backlinks
       │
       ├── runtime/build_pdf.py renders styled PDF from design.yml
       │
       └── git commit + push
             │
             └── GitHub Action fires: upload to Drive + email PDF
```

## Quickstart

### Option 1 — LLM-guided (recommended, ~10 min)

1. **Use this repo as a template** on GitHub (green "Use this template" button).
2. Clone your new repo.
3. Open [`BOOTSTRAP.md`](BOOTSTRAP.md), copy its contents, paste into a capable
   LLM chat (Claude Opus/Sonnet, GPT-5, Gemini, etc.).
4. The LLM interviews you about your interests, generates your `config/*.yml`,
   and walks you through the one-time infrastructure setup (Google OAuth,
   GitHub secrets, scheduled trigger).

### Option 2 — CLI wizard

```bash
git clone https://github.com/YOUR_USER/YOUR_FORK
cd YOUR_FORK
pip install -r requirements.txt
python3 setup.py
```

Answers the same questions as BOOTSTRAP, produces the same configs.

### Option 3 — Manual

Read [`SETUP.md`](SETUP.md). All steps documented, nothing automated.

## LLM Compatibility

| Phase | Works with |
|---|---|
| **Setup interview** (BOOTSTRAP.md) | Any capable LLM — Anthropic (Opus/Sonnet/Haiku), OpenAI (GPT-5+), Google Gemini, xAI Grok, Mistral Large. Paste BOOTSTRAP.md and the LLM handles the rest. |
| **Daily runtime** (scheduled-trigger) | **Currently Anthropic only** — uses Claude Code's scheduled-agent API ([claude.ai/code/scheduled](https://claude.ai/code/scheduled)). |

Porting the runtime to OpenAI / Google / Grok is feasible but requires replacing
the scheduled-agent mechanism (likely with a GitHub-Actions cron job that calls
the provider's API with a function-calling orchestration pattern). Contributions
welcome.

## Project Structure

```
dailybriefing/
├── config/                    # Your personal config — edit freely
│   ├── user.yml               # name, email, language, tone
│   ├── sections.yml           # THE core file — what you want to know
│   ├── design.yml             # PDF visual styling
│   ├── delivery.yml           # Drive / email / future channels
│   ├── dedup.yml              # Obsidian dedup + backlink policies
│   └── prompts/               # LLM prompt templates (Markdown)
├── runtime/build_pdf.py       # Config-aware PDF renderer
├── .github/
│   ├── workflows/deliver.yml  # Drive + Email delivery pipeline
│   └── scripts/               # Python for Drive upload, SMTP send
├── Daily/                     # Your briefings — user data, Obsidian vault
│   ├── 2026-04-21.md
│   └── Briefing_21-04-2026.pdf
├── setup.py                   # Interactive CLI wizard (optional)
├── BOOTSTRAP.md               # LLM-driven setup guide
├── SETUP.md                   # Manual setup guide
├── EXAMPLES.md                # 20+ section-idea recipes
└── LICENSE                    # MIT
```

## Using the Obsidian Vault Locally

```bash
git clone https://github.com/YOUR_USER/YOUR_FORK ~/Documents/Briefings
# Open Obsidian → Open folder as vault → select ~/Documents/Briefings
```

Each briefing has YAML frontmatter with `tags` and `covered_topics` —
search across briefings with `tag:#ai-news` or `covered_topics:iran-ceasefire`.
Backlinks render as live graph edges in Obsidian's graph view.

## Contributing

Issues and PRs welcome — especially for:
- Additional design presets (Swiss grid, magazine, brutalist, etc.)
- New delivery channels (Slack, Telegram, RSS)
- Non-Anthropic runtime adapters
- Section-idea recipes for `EXAMPLES.md`

## License

[MIT](LICENSE). Use it, modify it, ship it commercially — no restrictions.
