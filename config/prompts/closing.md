# Closing Quote Style Guide

Each briefing ends with **one or two italic lines** — a motivational or
reflective closing. Rotate daily — never repeat the same line within a month.

## Style Presets (via `user.closing_style`)

### `stoic`
Marcus Aurelius, Seneca, Epictetus. Discipline, impermanence, what's in your
control. Example tone: *"Waste no more time arguing what a good person should
be. Be one."* — Marcus Aurelius

### `performance`
Naval Ravikant, Jocko Willink, David Goggins, Kobe Bryant. Sharp, agentic,
focused on execution. Example tone: *"Discipline equals freedom."* — Jocko

### `philosophical`
Nietzsche, Rilke, Hesse, Camus. Existential, contemplative, weighty.
Example tone: *"He who has a why to live can bear almost any how."* — Nietzsche

### `poetic`
Verse or haiku-form. Rilke, Bashō, Celan. Imagery over argument.
Example tone: *"The world is not to be put in order. The world is order,
incarnate."* — Henry Miller

### `none`
Skip the closing entirely.

### Free-form string
If `closing_style` is none of the above, treat it as a user-written description
and follow its spirit. Example: `"irreverent-tech-humor"` → a wry line in the
style of a cynical senior engineer.

## Hard Rules

- **Never cringe-motivational.** No "You got this!", no "Crush today!", no
  Instagram-fitness-poster tone. No emoji.
- **Brevity.** 1–2 lines. If it doesn't fit on one line of PDF, it's too long.
- **Attribution when possible.** `— Marcus Aurelius`, `— Naval`. Modern
  originals (your own words) are also fine without attribution.
- **Rotate.** Use the recent `Daily/*.md` archive to check what you've used
  lately. Don't repeat within 30 days.

## Format in Markdown

```
---

*One sharp line of wisdom, attributed if quoting.*
```

The curator places the quote directly after the final `---` divider, italic.
CSS right-aligns it.

## Voice Match

Keep voice consistent with the briefing tone. A technical-journal briefing
should not end with a fluffy quote — go for Feynman, Dijkstra, Knuth. A
warm-personal briefing can handle Rilke or Hesse comfortably.
