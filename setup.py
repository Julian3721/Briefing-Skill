"""DailyBriefing CLI setup wizard.

Interactive configuration generator. Walks you through identity, section
definitions, design presets, and delivery channels. Writes the five
config/*.yml files that drive your daily briefing.

Does NOT configure infrastructure (OAuth, secrets, scheduled trigger) — see
SETUP.md for that walkthrough, or paste BOOTSTRAP.md into an LLM chat
for guided setup.

Usage:
    python3 setup.py
"""
import pathlib
import shutil
import sys
import textwrap

REPO_ROOT = pathlib.Path(__file__).resolve().parent
CONFIG_DIR = REPO_ROOT / "config"


def prompt(msg, default=None):
    suffix = f" [{default}]" if default else ""
    answer = input(f"{msg}{suffix}: ").strip()
    return answer or (default or "")


def prompt_multiline(msg):
    print(f"{msg}")
    print("(finish with an empty line)")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    return "\n".join(lines)


def yes_no(msg, default=True):
    default_char = "Y/n" if default else "y/N"
    answer = input(f"{msg} [{default_char}]: ").strip().lower()
    if not answer:
        return default
    return answer.startswith("y")


def choose(msg, options, default_index=0):
    print(msg)
    for i, opt in enumerate(options):
        marker = " ← default" if i == default_index else ""
        print(f"  {i + 1}. {opt}{marker}")
    while True:
        raw = input(f"Choice [1-{len(options)}]: ").strip()
        if not raw:
            return options[default_index]
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print("Invalid choice, try again.")


def header(txt):
    print()
    print("─" * 60)
    print(f" {txt}")
    print("─" * 60)


def main():
    print(textwrap.dedent("""
        DailyBriefing — CLI Setup Wizard
        =================================

        This wizard generates your personal config/*.yml files.
        You can edit them later in any text editor.

        For infrastructure setup (Google OAuth, GitHub secrets, scheduled
        trigger), see SETUP.md after this wizard finishes.
    """))

    if not CONFIG_DIR.exists():
        print("ERROR: config/ directory not found. Run from repo root.")
        sys.exit(1)

    # -- Phase 1: user.yml --
    header("1. Identity")
    name = prompt("Your name", "User")
    email = prompt("Your email")
    language = prompt("Output language (ISO code: en, de, es, fr, ja)", "en")

    greeting = prompt(
        "Greeting template (use {{name}})",
        f"Good morning, {{{{name}}}}."
        if language == "en"
        else f"Guten Morgen {{{{name}}}},"
        if language == "de"
        else "{{name}},",
    )

    date_locale = prompt(
        "Date locale for formatting (e.g. en_US.UTF-8, de_DE.UTF-8)",
        "en_US.UTF-8" if language == "en" else "de_DE.UTF-8",
    )

    verbosity = choose(
        "Default verbosity per bullet:",
        [
            "one-liner (one sentence always)",
            "normal (2-5 sentences, standard)",
            "deep (5-15 sentences)",
            "variable-by-impact (curator decides per item — recommended)",
        ],
        default_index=3,
    ).split(" ", 1)[0]

    tone = prompt(
        "Tone descriptor (free-form, e.g. editorial-minimalist, warm-personal)",
        "editorial-minimalist",
    )

    closing_style = choose(
        "Closing line style:",
        [
            "stoic (Marcus Aurelius, Seneca — discipline, impermanence)",
            "performance (Naval, Goggins, Jocko — sharp, agentic)",
            "philosophical (Nietzsche, Rilke, Camus)",
            "poetic (verse, imagery)",
            "none (skip the closing)",
        ],
        default_index=0,
    ).split(" ", 1)[0]

    user_yml = textwrap.dedent(f"""\
        name: {name}
        email: {email}
        output_language: {language}
        greeting_template: "{greeting}"
        date_locale: {date_locale}
        verbosity_default: {verbosity}
        tone: {tone}
        closing_style: {closing_style}
    """)
    (CONFIG_DIR / "user.yml").write_text(user_yml)
    print("✓ wrote config/user.yml")

    # -- Phase 2: sections.yml --
    header("2. Sections")
    print(textwrap.dedent("""
        Define the sections of your briefing — one per topic you care about.
        See EXAMPLES.md for 20+ recipe patterns.

        For this wizard, we'll add sections one at a time. Minimal info per
        section: id, title, filter rules. Press empty at 'id' to stop adding.
    """))

    sections = []
    while True:
        print()
        sid = prompt("Section id (kebab-case slug, empty to finish)")
        if not sid:
            break
        title = prompt("Section display title", sid.replace("-", " ").title())
        filter_text = prompt_multiline("Filter rules (plain-language):")
        sources_raw = prompt(
            "Preferred sources (comma-separated domains, empty = curator picks)"
        )
        sources = [s.strip() for s in sources_raw.split(",") if s.strip()]
        bias_mode = choose(
            "Bias handling:",
            ["single (one subagent, fast)", "multi (multiple lenses + synthesis)"],
            default_index=0,
        ).split(" ", 1)[0]
        section = {
            "id": sid,
            "title": title,
            "filter": filter_text,
            "sources": sources,
            "bias_mode": bias_mode,
            "max_bullets": 5,
            "length_target": verbosity,
        }
        if bias_mode == "multi":
            lenses_raw = prompt(
                "Lens labels (comma-separated, e.g. left,center,right)",
                "left,center,right",
            )
            section["bias_lenses"] = [
                l.strip() for l in lenses_raw.split(",") if l.strip()
            ]
            section["synthesis"] = choose(
                "Synthesis mode:",
                ["balanced-consensus", "highlight-conflicts", "raw-all"],
                default_index=0,
            )
        sections.append(section)

    if not sections:
        print("No sections defined — copying sections.yml.example as placeholder.")
        shutil.copy(CONFIG_DIR / "sections.yml.example", CONFIG_DIR / "sections.yml")
    else:
        lines = ["sections:"]
        for s in sections:
            lines.append(f"  - id: {s['id']}")
            lines.append(f"    title: \"{s['title']}\"")
            lines.append("    filter: |")
            for fl in s["filter"].split("\n"):
                lines.append(f"      {fl}")
            if s["sources"]:
                lines.append("    sources:")
                for src in s["sources"]:
                    lines.append(f"      - {src}")
            else:
                lines.append("    sources: []")
            lines.append(f"    bias_mode: {s['bias_mode']}")
            if s["bias_mode"] == "multi":
                lens_list = ", ".join(s["bias_lenses"])
                lines.append(f"    bias_lenses: [{lens_list}]")
                lines.append(f"    synthesis: {s['synthesis']}")
            lines.append(f"    max_bullets: {s['max_bullets']}")
            lines.append(f"    length_target: {s['length_target']}")
            lines.append("")
        (CONFIG_DIR / "sections.yml").write_text("\n".join(lines))
        print(f"✓ wrote config/sections.yml ({len(sections)} section(s))")

    # -- Phase 3: design.yml --
    header("3. Design")
    if yes_no("Use default design preset (editorial-minimalist, NYT-style)?", True):
        shutil.copy(CONFIG_DIR / "design.yml.example", CONFIG_DIR / "design.yml")
        print("✓ copied config/design.yml from example")
    else:
        print("Manual design customization: edit config/design.yml after wizard.")
        shutil.copy(CONFIG_DIR / "design.yml.example", CONFIG_DIR / "design.yml")

    # -- Phase 4: delivery.yml --
    header("4. Delivery")
    repo_url = prompt(
        "Your repo URL",
        "https://github.com/YOUR_USER/YOUR_FORK",
    )
    enable_drive = yes_no("Enable Google Drive delivery?", False)
    drive_folder = ""
    if enable_drive:
        drive_folder = prompt(
            "Google Drive folder ID (from the folder URL)", ""
        )

    enable_email = yes_no("Enable email delivery?", False)
    email_sender = email_recipient = ""
    if enable_email:
        email_sender = prompt("Gmail address for sending", email)
        email_recipient = prompt("Recipient", email_sender)

    delivery_yml = textwrap.dedent(f"""\
        git:
          enabled: true
          repo: "{repo_url}"
          branch: main

        drive:
          enabled: {str(enable_drive).lower()}
          folder_id: "{drive_folder}"

        email:
          enabled: {str(enable_email).lower()}
          sender: {email_sender}
          recipient: {email_recipient}
          smtp_host: smtp.gmail.com
          smtp_port: 465
          subject_template: "Daily Briefing for {{{{name}}}} — {{{{date_short}}}}"
    """)
    (CONFIG_DIR / "delivery.yml").write_text(delivery_yml)
    print("✓ wrote config/delivery.yml")

    # -- Phase 5: dedup.yml --
    header("5. Dedup policy")
    if yes_no("Use default dedup policy (updates-only, 14-day window)?", True):
        shutil.copy(CONFIG_DIR / "dedup.yml.example", CONFIG_DIR / "dedup.yml")
        print("✓ copied config/dedup.yml from example")

    # -- Done --
    print()
    print("═" * 60)
    print(" Setup complete.")
    print("═" * 60)
    print(textwrap.dedent(f"""
        Next steps:

        1. Commit your config:
               git add config/
               git commit -m "chore: personalize config"
               git push

        2. If you enabled Drive or email: follow SETUP.md sections 3 and 4
           to complete OAuth and app-password setup.

        3. Create your scheduled trigger: see SETUP.md section 6.

        4. Test a manual run from the trigger UI.

        Edit any config/*.yml anytime — changes apply on next briefing.
    """))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled. No files written if this is first run.")
        sys.exit(130)
