"""Render a briefing Markdown file to a styled PDF using config/design.yml.

Usage:
    python3 runtime/build_pdf.py <input.md> <output.pdf>

Reads `config/design.yml` for fonts, palette, typography, page geometry.
Strips YAML frontmatter from the Markdown before rendering (Obsidian metadata
isn't meant to show in the PDF).
"""
import pathlib
import sys

import markdown2
import yaml
from weasyprint import CSS, HTML

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DESIGN_YML = REPO_ROOT / "config" / "design.yml"


def load_design():
    with open(DESIGN_YML, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_css(design: dict) -> str:
    """Generate CSS from the design config."""
    fonts = design.get("fonts", {})
    palette = design.get("palette", {})
    page = design.get("page", {})
    typo = design.get("typography", {})
    bullet = design.get("bullet", {})
    rule = design.get("accent_rule_after_h2", {})

    body_font = fonts.get("body", "Inter")
    mono_font = fonts.get("mono", "JetBrains Mono")

    bg = palette.get("background", "#ffffff")
    text = palette.get("text_primary", "#0a0a0a")
    muted = palette.get("text_muted", "#737373")
    accent = palette.get("accent", "#b45309")
    divider = palette.get("divider", "#e5e5e5")

    page_size = page.get("size", "A4")
    mt = page.get("margin_top", "60pt")
    ms = page.get("margin_side", "56pt")

    def resolve_color(ref):
        mapping = {
            "accent": accent,
            "muted": muted,
            "primary": text,
            "background": bg,
            "divider": divider,
        }
        return mapping.get(ref, ref)

    link = typo.get("link", {})
    link_color = resolve_color(link.get("color", "accent"))
    link_size = link.get("size", "7.5pt")
    link_underline = (
        "underline" if link.get("underline", True) else "none"
    )
    link_font = mono_font if link.get("font") == "mono" else body_font

    closing = typo.get("closing_quote", {})
    closing_size = closing.get("size", "9.5pt")
    closing_color = resolve_color(closing.get("color", "muted"))

    bullet_char = bullet.get("char", "▸")
    bullet_color = resolve_color(bullet.get("color", "accent"))

    rule_w = rule.get("width", "36pt")
    rule_h = rule.get("height", "2pt")

    google_fonts = (
        f"https://fonts.googleapis.com/css2?family="
        f"{body_font.replace(' ', '+')}:wght@400;500;600;700;800&"
        f"family={mono_font.replace(' ', '+')}:wght@400;500&display=swap"
    )

    return f"""
@import url("{google_fonts}");
@page {{ size: {page_size}; margin: {mt} {ms}; }}
body {{
  font-family: "{body_font}", system-ui, sans-serif;
  font-size: {typo.get('body', {}).get('size', '10pt')};
  line-height: {typo.get('body', {}).get('line_height', 1.6)};
  color: {text}; background: {bg};
}}
h1 {{
  font-family: "{body_font}", sans-serif;
  font-size: {typo.get('h1', {}).get('size', '30pt')};
  font-weight: {typo.get('h1', {}).get('weight', 800)};
  letter-spacing: {typo.get('h1', {}).get('tracking', '-0.025em')};
  margin: 0 0 2pt 0; color: {text}; line-height: 1.1;
}}
h1 + p {{ font-size: 10pt; color: {muted}; margin: 0 0 4pt 0; font-weight: 400; }}
h1 + p em {{ font-style: normal; font-weight: 500; color: {text}; }}
hr {{ border: none; border-top: 1px solid {divider}; margin: 24pt 0 0 0; }}
h2 {{
  font-family: "{body_font}", sans-serif;
  font-size: {typo.get('h2', {}).get('size', '13pt')};
  font-weight: {typo.get('h2', {}).get('weight', 800)};
  text-transform: {('uppercase' if typo.get('h2', {}).get('uppercase', True) else 'none')};
  letter-spacing: {typo.get('h2', {}).get('tracking', '0.1em')};
  margin: 28pt 0 4pt 0; color: {text};
}}
h2::after {{
  content: ""; display: block; width: {rule_w}; height: {rule_h};
  background: {accent}; margin-top: 6pt; margin-bottom: 6pt;
}}
h3 {{
  font-family: "{body_font}", sans-serif;
  font-size: {typo.get('h3', {}).get('size', '10pt')};
  font-weight: {typo.get('h3', {}).get('weight', 700)};
  text-transform: {('uppercase' if typo.get('h3', {}).get('uppercase', True) else 'none')};
  letter-spacing: {typo.get('h3', {}).get('tracking', '0.08em')};
  margin: 16pt 0 4pt 0; color: {muted};
}}
ul {{ padding-left: 0; margin: 12pt 0 0 0; list-style: none; }}
li {{ margin-bottom: 18pt; position: relative; padding-left: 14pt; }}
li::before {{
  content: "{bullet_char}"; position: absolute; left: 0;
  color: {bullet_color}; font-size: 9pt; top: 1pt;
}}
li p {{ margin: 0 0 4pt 0; }}
li strong {{ font-weight: 700; color: {text}; }}
strong {{ font-weight: 700; }}
p {{ margin: 6pt 0; }}
em {{ color: {muted}; font-style: italic; font-size: 9pt; }}
a {{
  color: {link_color}; text-decoration: {link_underline};
  text-decoration-thickness: 0.5pt; text-underline-offset: 1.5pt;
  font-family: "{link_font}", ui-monospace, monospace;
  font-size: {link_size}; font-weight: 500;
  word-break: break-all; letter-spacing: -0.015em;
}}
li a {{
  display: block; margin-top: 6pt; padding-top: 5pt; padding-bottom: 2pt;
  border-top: 0.5pt solid {divider};
}}
hr + p em, body > p:last-child em {{
  display: block; text-align: right; font-style: italic;
  font-weight: 400; font-size: {closing_size}; color: {closing_color};
  margin: 36pt 0 0 0; max-width: 70%; margin-left: auto;
  font-family: "{body_font}", sans-serif;
}}
"""


def strip_frontmatter(md: str) -> str:
    """Remove leading YAML frontmatter block so it doesn't appear in PDF."""
    if md.startswith("---"):
        parts = md.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip()
    return md


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    input_md = pathlib.Path(sys.argv[1])
    output_pdf = pathlib.Path(sys.argv[2])

    raw = input_md.read_text(encoding="utf-8")
    body = strip_frontmatter(raw)
    html_body = markdown2.markdown(body, extras=["fenced-code-blocks"])

    design = load_design()
    css = build_css(design)

    full_html = (
        f"<!doctype html><html><head><meta charset='utf-8'></head>"
        f"<body>{html_body}</body></html>"
    )
    HTML(string=full_html).write_pdf(output_pdf, stylesheets=[CSS(string=css)])
    print(f"OK {output_pdf}")


if __name__ == "__main__":
    main()
