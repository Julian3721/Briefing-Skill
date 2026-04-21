# EXAMPLES — Section Recipes

Copy-paste-adapt these into your `config/sections.yml`. All fictional — tune
to your actual interests.

---

## News & Politics

### National politics — single-lens (fast)

```yaml
- id: politics-national
  title: "National Politics"
  sources: []                # let the curator pick authoritative sources
  filter: |
    Top national political developments in the last 24h. Skip tabloid.
    Focus on legislative actions, executive orders, coalition dynamics,
    major speeches that move policy.
  bias_mode: single
  max_bullets: 5
  length_target: variable-by-impact
```

### National politics — multi-lens (balanced)

```yaml
- id: politics-balanced
  title: "Politics — Balanced"
  sources: []
  filter: |
    Major national political events. Significant legislative, executive,
    or judicial developments. Skip campaign-trail noise.
  bias_mode: multi
  bias_lenses: [left, center, right]
  synthesis: balanced-consensus   # facts all agree on, neutral framing
  max_bullets: 5
```

### International affairs — conflict-surfacing

```yaml
- id: foreign-policy
  title: "International Affairs"
  sources: [reuters.com, ft.com, aljazeera.com, economist.com]
  filter: |
    Cross-border developments: major-nation diplomacy, conflict, treaties,
    economic coordination. Skip bilateral minor news.
  bias_mode: multi
  bias_lenses: [western-press, non-western-press]
  synthesis: highlight-conflicts   # make framing differences visible
  max_bullets: 4
```

---

## Technology

### AI model & tool releases

```yaml
- id: ai-releases
  title: "AI — Models & Tools"
  sources:
    - openai.com/blog
    - anthropic.com/news
    - deepmind.google
    - huggingface.co/blog
    - github.com/trending
  filter: |
    New model releases from top labs, developer tools, viral open-source
    repos (>500 GitHub stars gained in 24h). Technical substance — skip
    mainstream AI hype and opinion pieces.
  bias_mode: single
  max_bullets: 5
  length_target: variable-by-impact
```

### AI research breakthroughs

```yaml
- id: ai-research
  title: "AI Research"
  sources: [arxiv.org/list/cs.LG/recent, paperswithcode.com]
  filter: |
    Only genuine research breakthroughs — new architectures, training
    paradigms, significant benchmark improvements. Skip incremental papers.
    Most days empty.
  bias_mode: single
  max_bullets: 3
  length_target: deep
```

### Hardware & compute

```yaml
- id: hardware
  title: "Hardware"
  sources: [semianalysis.com, theregister.com, nvidia.com]
  filter: |
    New chip architectures, photonic/neuromorphic/quantum compute advances,
    meaningful FLOPS/$ changes. Skip minor spec bumps.
  bias_mode: single
  max_bullets: 4
```

### Cybersecurity

```yaml
- id: security
  title: "Cybersecurity"
  sources: [krebsonsecurity.com, theregister.com, bleepingcomputer.com]
  filter: |
    Major breaches affecting >1M users, critical CVEs in widespread software,
    significant ransomware incidents. Skip vendor marketing and low-severity
    patches.
  bias_mode: single
  max_bullets: 3
```

---

## Finance

### Markets overview — compact

```yaml
- id: markets
  title: "Markets"
  sources: [bloomberg.com, reuters.com/markets, ft.com, cnbc.com]
  filter: |
    S&P 500, NASDAQ, FTSE, DAX closing movements with 1-sentence driver.
    Mag7 headline if significant. BTC/ETH closing + one crypto headline.
  bias_mode: single
  max_bullets: 4
  length_target: one-liner
```

### Crypto deep-dive — multi-lens

```yaml
- id: crypto
  title: "Crypto"
  sources: [coindesk.com, theblock.co, messari.io]
  filter: |
    BTC/ETH price drivers, major protocol news, one altcoin story if material.
  bias_mode: multi
  bias_lenses: [technical-analyst, fundamental-investor, skeptic]
  synthesis: highlight-conflicts
  max_bullets: 4
```

### Personal investment watchlist

```yaml
- id: watchlist
  title: "My Watchlist"
  sources: []
  filter: |
    News moving these tickers: AAPL, MSFT, NVDA, TSLA, ASML. Only earnings,
    guidance changes, product launches, M&A, regulatory actions. Skip
    analyst-rating changes.
  bias_mode: single
  max_bullets: 5
```

---

## Science

### Breakthrough-only

```yaml
- id: science
  title: "Science"
  sources: [nature.com, science.org, quantamagazine.org]
  filter: |
    Only globally relevant breakthroughs — fusion, quantum computing, major
    medical advances, astrophysics, longevity. Happens rarely.
  bias_mode: single
  max_bullets: 3
  length_target: deep
```

### Climate & environment

```yaml
- id: climate
  title: "Climate & Environment"
  sources: [nature.com, grist.org, carbonbrief.org]
  filter: |
    Significant climate science findings, major policy shifts, noteworthy
    environmental events (extreme weather with context).
  bias_mode: multi
  bias_lenses: [mainstream-science, contrarian-economic]
  synthesis: balanced-consensus
  max_bullets: 3
```

---

## Sports

### Football / soccer — results focus

```yaml
- id: football
  title: "Football"
  parent: sports
  sources: [kicker.de, bbc.com/sport/football, marca.com]
  filter: |
    List your favorite leagues and clubs. Skip player drama and tactical
    analysis — results only unless something truly noteworthy happened.
    Emphasize Monday/Tuesday after weekend fixtures.
  bias_mode: single
  max_bullets: 5
  length_target: one-liner
```

### Combat sports — major events only

```yaml
- id: combat
  title: "Combat Sports"
  parent: sports
  sources: [mmafighting.com, boxingscene.com]
  filter: |
    Championship-level boxing and MMA only. Card announcements, result
    summaries, title changes.
  bias_mode: single
  max_bullets: 3
```

### Formula 1

```yaml
- id: f1
  title: "Formula 1"
  parent: sports
  sources: [motorsport.com, theguardian.com/sport/formulaone]
  filter: |
    Race weekends: qualifying + race results. Outside weekends: only
    major technical regulation changes, driver transfers, team ownership.
  bias_mode: single
  max_bullets: 3
```

---

## Local / Regional

### Local news — broad interest

```yaml
- id: local
  title: "Local"
  sources: []
  filter: |
    Non-political nationwide news of broad public interest. Major accidents,
    cultural moments, viral events, unusual happenings (e.g. "whale in the
    harbor"). Skip crime-blotter.
  bias_mode: single
  max_bullets: 3
```

### City-specific

```yaml
- id: city
  title: "Berlin"
  sources: [berliner-zeitung.de, tagesspiegel.de, rbb24.de]
  filter: |
    Berlin city news, BVG/transit, Senatspolitik, cultural events.
  bias_mode: single
  max_bullets: 4
```

---

## Hobbies & Niche Interests

### Coffee

```yaml
- id: coffee
  title: "Coffee & Espresso"
  parent: hobbies
  sources: [home-barista.com, reddit.com/r/espresso]
  filter: |
    New prosumer machines, grinders, accessories, respected reviews.
    Skip drip coffee and pod-system content.
  bias_mode: single
  max_bullets: 3
```

### Watches

```yaml
- id: watches
  title: "Watches"
  parent: hobbies
  sources: [hodinkee.com, watchesbysjx.com]
  filter: |
    New luxury and independent-brand releases. Auction highlights for
    significant vintage pieces. Skip microbrand crowdfunding noise.
  bias_mode: single
  max_bullets: 2
```

### Chess — elite tournaments

```yaml
- id: chess
  title: "Chess"
  sources: [chess.com, chessbase.com, fide.com]
  filter: |
    Only tournaments with world elite players (top 20 rated). Announcements
    2–3 days before start. Daily result updates during events.
  bias_mode: single
  max_bullets: 3
```

### Video games

```yaml
- id: games
  title: "Games"
  sources: [eurogamer.net, rockpapershotgun.com]
  filter: |
    Major game releases, significant patches for long-tail games, key
    industry news (studio closures, platform deals). Skip review scores
    and influencer drama.
  bias_mode: single
  max_bullets: 3
```

---

## Builder & Indie Hacker

### One founder idea per day

```yaml
- id: founder-idea
  title: "Founder Idea of the Day"
  sources: [producthunt.com, news.ycombinator.com/show, reddit.com/r/SideProject]
  filter: |
    Max 1 idea per day. Criteria: practical everyday utility, AI-enabled
    (not just "AI-wrapper for X"), concrete problem/solution, not already
    a dominant player. If nothing solid today, leave empty.
  bias_mode: single
  max_bullets: 1
  length_target: normal
```

### Trending repos

```yaml
- id: trending
  title: "GitHub Trending"
  sources: [github.com/trending]
  filter: |
    Repos that gained 500+ stars in 24h AND are genuinely novel (not just
    viral boilerplate). Explain briefly what problem the repo solves.
  bias_mode: single
  max_bullets: 3
```

---

## Wellness / Personal

### Fitness research

```yaml
- id: fitness-science
  title: "Fitness & Nutrition Science"
  parent: wellness
  sources: [examine.com, pubmed.ncbi.nlm.nih.gov]
  filter: |
    New meta-analyses or strong RCTs on training, nutrition, supplementation.
    Skip influencer hot-takes and one-off studies without replication.
  bias_mode: single
  max_bullets: 2
```

### Productivity tools

```yaml
- id: productivity
  title: "Productivity Tools"
  parent: wellness
  sources: [producthunt.com, news.ycombinator.com/show]
  filter: |
    New tools for knowledge work that go beyond incremental improvements.
    Skip yet-another-to-do-app.
  bias_mode: single
  max_bullets: 2
```

---

## Creative Prompts

### "Weird & wonderful"

```yaml
- id: serendipity
  title: "Serendipity"
  sources: []
  filter: |
    One genuinely interesting/unusual/delightful thing from the past 24h.
    Unexpected discoveries, weird coincidences, moments of cultural beauty.
    No news headlines — something that makes you smile or think.
  bias_mode: single
  max_bullets: 1
  length_target: normal
```

### "Long-form reading queue"

```yaml
- id: longform
  title: "Long-form Reading"
  sources: [longform.org, theatlantic.com, nautil.us]
  filter: |
    One high-quality long-form article worth saving for the weekend.
    Depth over recency — can be from the last 7 days.
  bias_mode: single
  max_bullets: 1
  length_target: normal
```

---

## Custom Patterns

Nothing here fits? Write your own. Template:

```yaml
- id: your-unique-slug
  title: "Display Heading"
  sources: []                    # list of preferred domains, or empty
  filter: |
    Plain-language rules: what's in, what's out, what bar to clear,
    what to avoid. Be specific about edge cases.
  bias_mode: single              # or multi (politics/hot-takes)
  max_bullets: 5
  length_target: variable-by-impact
```

The orchestrator and curator handle the rest.
