# BOOTSTRAP — LLM-Guided Setup

**Paste this entire file into a capable LLM chat (Claude, GPT-5, Gemini, Grok,
etc.). The LLM becomes your setup assistant.**

**Note on LLM compatibility:** Any model that can read this file and follow
multi-step instructions works for SETUP. For daily RUNTIME, this project
currently requires Anthropic's Claude Code scheduled-agent API. Porting to
OpenAI/Google/etc. is planned — see README for status.

---

## Your Role as the LLM

You are setting up a personalized daily briefing system for the user. Follow
these four phases in order. Be patient, explain trade-offs clearly, and pause
for confirmation before writing files or making commits.

## Phase 1 — Interview

Ask the user conversationally (don't hurl all questions at once):

1. **Identity**
   - Name (used in the greeting)
   - Email (for delivery and Gmail SMTP sender)
   - Preferred output language (briefing will be written in this language)

2. **Topics** *(the most important phase)*
   - Open-ended: "What do you want to know about each morning? Just describe
     in natural language — news topics, hobbies, sports, fields of research,
     anything."
   - Let them freeform. Then help them structure each topic into a section:
     - A short `id` (kebab-case slug)
     - A display `title`
     - Preferred `sources` (or "let the LLM decide" → empty list)
     - A `filter` paragraph — what's in, what's out, what bar to clear
     - **Political bias handling** (only ask for politics/news-heavy sections):
       - `single` — one research subagent, efficient
       - `multi` — N parallel subagents with different lenses (e.g.
         `[left, center, right]` or custom frames) + synthesizer
       - If `multi`: ask for lens labels + synthesis mode
         (`balanced-consensus` / `highlight-conflicts` / `raw-all`)
     - **Length target**:
       - `one-liner` — always one sentence
       - `normal` — 2–5 sentences
       - `deep` — 5–15 sentences, explainer depth
       - `variable-by-impact` — curator decides per item
     - `max_bullets` (default 5)

3. **Global defaults**
   - Overall verbosity (sections can override)
   - Tone (e.g. "editorial-minimalist", "warm-personal", "punchy-newsroom" —
     free-form string)
   - Closing style (`stoic` / `performance` / `philosophical` / `poetic` /
     `none` / free-form description)

4. **Design**
   - Preset (default: `editorial-minimalist`) or "describe what you like"
   - Accent color (hex)
   - Font preferences (any Google Font or system font)

5. **Delivery**
   - Git repo URL
   - Google Drive folder? (optional, will need OAuth setup in Phase 3)
   - Email delivery? (optional, will need Gmail app-password in Phase 3)

6. **Dedup policy**
   - Scan window (default 14 days)
   - Default policy per-section (`updates-only` recommended)
   - Any sections that should bypass dedup entirely (e.g. markets, sports
     results — always fresh)

## Phase 2 — Generate Configs

Based on the interview, write these files (show diffs, ask for approval):

- `config/user.yml` — identity, language, tone, verbosity, closing style
- `config/sections.yml` — every section with sources, filters, bias config,
  length targets
- `config/design.yml` — only if user customized; otherwise copy from
  `config/design.yml.example`
- `config/delivery.yml` — only the channels they enabled
- `config/dedup.yml` — policies and overrides

**Reference files:**
- Schema: `config/*.yml.example` (commented with all options)
- Recipes: `EXAMPLES.md` (20+ section ideas across domains — suggest these
  if user seems unsure)

**Rules:**
- Never put user's personal data into files that will be publicly shared
  (BOOTSTRAP / SETUP / EXAMPLES / README are public; `config/*.yml` is
  user's private)
- Default every field to reasonable value if user is unsure
- If user says "just do a generic one like X", use patterns from EXAMPLES.md

## Phase 3 — Infrastructure Setup

Walk the user through in this order. Pause at each step, confirm success,
then proceed:

### 3.1 Repo

If not yet forked:
- Guide user to click "Use this template" on the GitHub repo
- Clone locally
- Verify the repo is **private** (important — `config/*.yml` contains their data)

### 3.2 Google Drive OAuth (if drive delivery enabled)

1. Open https://console.cloud.google.com/apis/credentials
2. Create OAuth consent screen if needed (external type, add user's email
   as test user)
3. Create OAuth Client ID, **type: Desktop app**
4. Download the JSON client-secret file
5. Run locally:
   ```bash
   pip install google-auth-oauthlib google-api-python-client
   python3 .github/scripts/get_refresh_token.py path/to/client_secret.json
   ```
6. Browser opens → approve → terminal prints 3 values
7. Guide user to add them as **GitHub repository secrets**:
   - `OAUTH_CLIENT_ID`
   - `OAUTH_CLIENT_SECRET`
   - `OAUTH_REFRESH_TOKEN`
8. Guide user to create a Drive folder named "Briefings", copy its folder ID
   (from the URL) into `config/delivery.yml` → `drive.folder_id`

### 3.3 Gmail App-Password (if email delivery enabled)

1. Verify user has 2FA enabled on Google account
2. Open https://myaccount.google.com/apppasswords
3. Generate app password named "DailyBriefing"
4. Add as GitHub secret `GMAIL_APP_PASSWORD` (16 chars, no spaces)

### 3.4 Scheduled Trigger

*Currently Anthropic-only. If the user wants OpenAI/Google, flag this as
a known limitation and suggest filing a PR.*

1. User goes to https://claude.ai/code/scheduled
2. Create new trigger with:
   - **Name:** `Daily Briefing`
   - **Cron:** convert their local time to UTC (e.g. 09:00 Europe/Berlin =
     07:00 UTC → `0 7 * * *`). Mention DST caveat (cron is always UTC).
   - **Repo source:** their fork URL
   - **Model:** `claude-haiku-4-5` (fast) or `claude-sonnet-4-6` (smarter,
     pricier)
   - **Allowed tools:** `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`,
     `Task`, `TodoWrite`, `WebSearch`, `WebFetch`
   - **Prompt body:**
     ```
     Clone the repo. Read config/prompts/orchestrator.md. Execute it end-to-end.
     Derive today's date (UTC) in your preflight.
     ```

## Phase 4 — Test & Iterate

1. Trigger a manual run (from the scheduled-triggers UI)
2. Watch for:
   - Briefing file in `Daily/` in the repo
   - PDF in the Drive folder (~30 seconds later, from GitHub Action)
   - Email in inbox (~30 seconds later)
3. If any channel fails, check the corresponding log:
   - Trigger log → orchestrator errors
   - GitHub Actions log → Drive/email errors
4. Offer the user to refine sections / filters / design after seeing the
   first real output. Common tweaks after day 1:
   - Reword filter rules
   - Adjust `max_bullets` or `length_target`
   - Add/remove sources
   - Change `bias_mode` or `synthesis` mode
5. After 1–2 weeks of live use, user should open `Daily/` as an Obsidian
   vault and explore the graph view — this is where the dedup-and-backlinks
   payoff becomes obvious.

## Closing

When done: briefing arrives automatically every day. User never needs to
touch infrastructure again. All future changes are one-commit edits to
`config/*.yml` — the runtime reads config fresh each run.
