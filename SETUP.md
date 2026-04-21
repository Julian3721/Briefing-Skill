# SETUP — Manual Setup Guide

Full setup without LLM assistance. If you'd rather have a chat model walk you
through it, see [`BOOTSTRAP.md`](BOOTSTRAP.md).

Estimated time: 25–35 minutes for first-time setup.

---

## Prerequisites

- GitHub account
- Google account (for Drive + Gmail, if you want those channels)
- Anthropic API access with Claude Code scheduled-triggers enabled
  ([claude.ai/code/scheduled](https://claude.ai/code/scheduled))
- Python 3.11+ locally for one-time OAuth step

## Step 1 — Fork the Template

1. Click **"Use this template"** on the GitHub repo page
2. Name your fork (e.g. `my-daily-briefing`)
3. **Set it to private** — your `config/*.yml` will contain personal details
4. Clone locally:
   ```bash
   git clone https://github.com/YOUR_USER/YOUR_FORK ~/Documents/Briefings
   cd ~/Documents/Briefings
   ```

## Step 2 — Create Your Config

Copy each `.example` file to its live name, then edit:

```bash
cp config/user.yml.example config/user.yml
cp config/sections.yml.example config/sections.yml
cp config/design.yml.example config/design.yml
cp config/delivery.yml.example config/delivery.yml
cp config/dedup.yml.example config/dedup.yml
```

### `config/user.yml`
Fill in name, email, output language, closing style.

### `config/sections.yml`
The heart of your briefing. Define sections — one per topic you care about.
See [`EXAMPLES.md`](EXAMPLES.md) for 20+ recipe patterns. Every section needs:
- `id` — unique slug
- `title` — display heading
- `filter` — plain-language rules for the researcher

Common patterns:
- **Single-lens** (`bias_mode: single`) — one subagent, fast, good for non-political
- **Multi-lens** (`bias_mode: multi`) — N parallel subagents with different frames
  (e.g. `[left, center, right]`) + a synthesizer. Best for political news.

### `config/design.yml`
Optional. Defaults to `editorial-minimalist`. Edit fonts, colors, page size.

### `config/delivery.yml`
- Set `git.repo` to your fork URL
- Enable `drive` and/or `email` as desired (configure them in Steps 3–4 below)

### `config/dedup.yml`
Defaults are sensible. Override per-section if needed.

## Step 3 — Google Drive OAuth (optional)

Only if you want daily PDF upload to Drive.

### 3.1 Create OAuth Client

1. Open [Google Cloud Console → APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials)
2. If prompted, create a project (any name)
3. If OAuth consent screen not configured:
   - Type: External
   - App name: `DailyBriefing`
   - User support email + developer email: your address
   - Scopes: skip
   - Test users: **add your Gmail**
   - Save and continue through the rest
4. **Credentials → + Create Credentials → OAuth client ID**
5. **Application type: Desktop app**
6. Name: `DailyBriefing`
7. Click **Create**, then **Download JSON**

### 3.2 Get Refresh Token Locally

```bash
cd ~/Documents/Briefings
pip install google-auth-oauthlib google-api-python-client
python3 .github/scripts/get_refresh_token.py ~/Downloads/client_secret_*.json
```

Browser opens → approve → terminal prints three values:
- `OAUTH_CLIENT_ID`
- `OAUTH_CLIENT_SECRET`
- `OAUTH_REFRESH_TOKEN`

### 3.3 Add GitHub Secrets

1. Go to `https://github.com/YOUR_USER/YOUR_FORK/settings/secrets/actions`
2. Create three **repository secrets** with the names above

### 3.4 Create Drive Folder

1. Open [drive.google.com](https://drive.google.com)
2. Create folder: `Briefings` (or any name)
3. Open the folder → copy folder ID from the URL
   (`https://drive.google.com/drive/folders/FOLDER_ID_HERE`)
4. In `config/delivery.yml`:
   ```yaml
   drive:
     enabled: true
     folder_id: "YOUR_FOLDER_ID"
   ```

### 3.5 Clean Up

Delete the downloaded client-secret JSON — you don't need it again:
```bash
rm ~/Downloads/client_secret_*.json
```

## Step 4 — Gmail App-Password (optional)

Only if you want daily PDF via email.

1. Verify 2FA is on: [myaccount.google.com/security](https://myaccount.google.com/security)
2. Open [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. App name: `DailyBriefing` → **Create**
4. Copy the 16-character password (remove spaces)
5. Add as GitHub secret: `GMAIL_APP_PASSWORD`
6. In `config/delivery.yml`:
   ```yaml
   email:
     enabled: true
     sender: you@gmail.com
     recipient: you@gmail.com
     smtp_host: smtp.gmail.com
     smtp_port: 465
     subject_template: "Daily Briefing for {{name}} — {{date_short}}"
   ```

## Step 5 — Commit Your Config

```bash
cd ~/Documents/Briefings
git add config/
git commit -m "chore: personalize config"
git push
```

## Step 6 — Create Scheduled Trigger (Anthropic)

*Currently the runtime requires Anthropic's Claude Code scheduled-triggers.
Other providers may be supported in the future.*

1. Open [claude.ai/code/scheduled](https://claude.ai/code/scheduled)
2. **New trigger**
3. Configuration:
   - **Name:** `Daily Briefing`
   - **Cron expression:** convert your local time to UTC. For 09:00
     Europe/Berlin in summer (CEST = UTC+2): `0 7 * * *`. In winter
     (CET = UTC+1): `0 8 * * *`. (Cron is always UTC; DST will shift the
     local delivery time twice a year.)
   - **Source:** your repo URL
   - **Model:** `claude-haiku-4-5` recommended (fast, cheap). Use
     `claude-sonnet-4-6` for more nuanced curation (~5× cost).
   - **Allowed tools:** `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`,
     `Task`, `TodoWrite`, `WebSearch`, `WebFetch`
   - **Prompt body:**
     ```
     Clone the repo. Read config/prompts/orchestrator.md. Execute it end-to-end.
     Derive today's date (UTC) in your preflight.
     ```
4. Save. The trigger will fire daily at the specified time.

## Step 7 — Test

From the scheduled-triggers UI, manually trigger a run. After 3–5 minutes:

- Your repo should have a new `Daily/YYYY-MM-DD.md` + PDF (visible in GitHub)
- Your Drive folder should show the PDF (from the Action)
- Your inbox should show the email

If any step fails:
- **Trigger log** (in the UI) — shows orchestrator errors
- **GitHub Action log** (Actions tab of your repo) — shows Drive/email errors

Re-run is safe — duplicates in Drive get updated, email resends.

## Step 8 — Open the Obsidian Vault (optional)

If you use [Obsidian](https://obsidian.md):

1. Obsidian → **Open folder as vault** → select your cloned repo directory
2. `Daily/` shows your briefings, frontmatter tags render, backlinks are live
3. Install the **Obsidian Git** community plugin for auto-pull each morning

## Common Issues

### "No PDF to send; skipping" in email step
The workflow runs on `push` to `Daily/*.pdf`. If you manually trigger the
workflow via `workflow_dispatch`, it will pick up the latest PDF on disk.
If no PDFs exist yet (first day), the message is harmless — wait for the
first scheduled run.

### Google `invalid_client` error
Your `OAUTH_CLIENT_ID` or `OAUTH_CLIENT_SECRET` secret has extra whitespace
or a typo. Copy exact values from your JSON client-secret file.

### Service Account error: "no storage quota"
Service accounts don't get Drive storage with personal Gmail. Use the OAuth
refresh-token flow (Step 3) — that's what this template uses.

### Briefing never arrives
Check the trigger log on [claude.ai/code/scheduled](https://claude.ai/code/scheduled).
Common causes: filter rules too strict (every section returns "NO RELEVANT
EVENTS"), cron expression wrong (UTC vs. local confusion), model refused
(rare — check the trigger's tool allowlist).

## What's Next

- Tweak `config/sections.yml` until briefings match your interests
- Add more sections via `config/sections.yml` — changes take effect next run
- After 2+ weeks of archive, explore the Obsidian graph view
- Consider adding new delivery channels via PR (Slack / Telegram / RSS)
