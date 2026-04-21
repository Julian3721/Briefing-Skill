"""Upload briefing PDFs to Google Drive using user OAuth refresh token.

Reads `config/delivery.yml` for `drive.enabled` + `drive.folder_id`.
Secrets come from GitHub Actions env: OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET,
OAUTH_REFRESH_TOKEN.
"""
import os
import pathlib
import subprocess
import sys

import yaml
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DELIVERY_YML = REPO_ROOT / "config" / "delivery.yml"


def load_delivery():
    with open(DELIVERY_YML, encoding="utf-8") as f:
        return yaml.safe_load(f)


def pick_pdfs():
    event = os.environ.get("GITHUB_EVENT_NAME", "push")
    if event == "workflow_dispatch":
        pdfs = sorted(pathlib.Path("Daily").glob("*.pdf"))
        print(f"Manual dispatch: syncing all {len(pdfs)} PDFs in Daily/.")
        return [str(p) for p in pdfs]
    diff = subprocess.check_output(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
    ).decode()
    return [
        line
        for line in diff.splitlines()
        if line.startswith("Daily/") and line.endswith(".pdf")
    ]


def main():
    delivery = load_delivery()
    drive_cfg = delivery.get("drive", {})
    if not drive_cfg.get("enabled"):
        print("Drive delivery disabled in config/delivery.yml; skipping.")
        return

    folder_id = drive_cfg.get("folder_id")
    if not folder_id:
        print("ERROR: drive.folder_id not set in config/delivery.yml", file=sys.stderr)
        sys.exit(1)

    creds = Credentials(
        token=None,
        refresh_token=os.environ["OAUTH_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["OAUTH_CLIENT_ID"],
        client_secret=os.environ["OAUTH_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/drive.file"],
    )
    svc = build("drive", "v3", credentials=creds)

    pdfs = pick_pdfs()
    if not pdfs:
        print("No PDFs to upload.")
        return

    for pdf_path in pdfs:
        p = pathlib.Path(pdf_path)
        if not p.exists():
            print(f"SKIP (not on disk): {pdf_path}")
            continue

        print(f"Processing {p.name}...")
        media = MediaFileUpload(str(p), mimetype="application/pdf", resumable=False)

        q = (
            f"name = '{p.name}' and '{folder_id}' in parents "
            f"and trashed = false"
        )
        existing = (
            svc.files().list(q=q, fields="files(id)").execute().get("files", [])
        )

        if existing:
            file = svc.files().update(
                fileId=existing[0]["id"], media_body=media
            ).execute()
            print(f"  UPDATED id={file['id']}")
        else:
            meta = {"name": p.name, "parents": [folder_id]}
            file = svc.files().create(
                body=meta, media_body=media, fields="id,webViewLink"
            ).execute()
            print(f"  CREATED id={file['id']} url={file.get('webViewLink')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
