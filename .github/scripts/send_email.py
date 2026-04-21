"""Send latest briefing PDF via SMTP using user OAuth app-password.

Reads `config/delivery.yml` for email settings and `config/user.yml` for name.
Secret from GitHub Actions env: GMAIL_APP_PASSWORD.
"""
import locale
import os
import pathlib
import smtplib
import ssl
import subprocess
import sys
from datetime import datetime
from email.message import EmailMessage

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DELIVERY_YML = REPO_ROOT / "config" / "delivery.yml"
USER_YML = REPO_ROOT / "config" / "user.yml"


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def pick_pdf():
    event = os.environ.get("GITHUB_EVENT_NAME", "push")
    if event == "workflow_dispatch":
        pdfs = sorted(pathlib.Path("Daily").glob("Briefing_*.pdf"))
        return pdfs[-1] if pdfs else None
    diff = subprocess.check_output(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
    ).decode()
    pdfs = [
        pathlib.Path(line)
        for line in diff.splitlines()
        if line.startswith("Daily/Briefing_") and line.endswith(".pdf")
    ]
    return pdfs[-1] if pdfs else None


def format_date_short(pdf_path, date_locale):
    """Extract DD-MM-YYYY from filename, format as localized date."""
    stem = pdf_path.stem
    parts = stem.split("_")
    if len(parts) != 2:
        return ""
    try:
        dt = datetime.strptime(parts[1], "%d-%m-%Y")
    except ValueError:
        return parts[1]
    try:
        locale.setlocale(locale.LC_TIME, date_locale)
    except locale.Error:
        pass
    return dt.strftime("%d.%m.%Y")


def main():
    delivery = load(DELIVERY_YML)
    user = load(USER_YML)

    email_cfg = delivery.get("email", {})
    if not email_cfg.get("enabled"):
        print("Email delivery disabled in config/delivery.yml; skipping.")
        return

    sender = email_cfg.get("sender")
    recipient = email_cfg.get("recipient") or sender
    smtp_host = email_cfg.get("smtp_host", "smtp.gmail.com")
    smtp_port = email_cfg.get("smtp_port", 465)
    subject_tpl = email_cfg.get(
        "subject_template", "Daily Briefing for {{name}} — {{date_short}}"
    )

    if not sender:
        print("ERROR: email.sender not set in config/delivery.yml", file=sys.stderr)
        sys.exit(1)

    pdf = pick_pdf()
    if not pdf or not pdf.exists():
        print("No PDF to send; skipping.")
        return

    datum = format_date_short(pdf, user.get("date_locale", "en_US.UTF-8"))
    subject = (
        subject_tpl
        .replace("{{name}}", user.get("name", "User"))
        .replace("{{date_short}}", datum)
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(
        f"{user.get('greeting_template', 'Hello').replace('{{name}}', user.get('name', ''))}"
        f"\n{datum}\n\nPDF attached."
    )

    with open(pdf, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=pdf.name,
        )

    password = os.environ["GMAIL_APP_PASSWORD"]
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=ctx) as server:
        server.login(sender, password)
        server.send_message(msg)

    print(f"Sent {pdf.name} to {recipient}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
