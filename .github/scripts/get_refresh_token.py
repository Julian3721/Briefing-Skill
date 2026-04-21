"""Run ONCE locally to get OAuth refresh token for Drive upload.

Usage:
    pip install google-auth-oauthlib
    python3 get_refresh_token.py path/to/client_secret.json

Output:
    Prints CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN to paste into GitHub secrets.
"""
import json
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive.file']


def main(client_secret_path):
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
    creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')

    with open(client_secret_path) as f:
        cs = json.load(f)
    key = 'installed' if 'installed' in cs else 'web'
    client_id = cs[key]['client_id']
    client_secret = cs[key]['client_secret']

    print('\n' + '=' * 60)
    print('PASTE THESE AS GITHUB SECRETS:')
    print('=' * 60)
    print(f'OAUTH_CLIENT_ID:\n{client_id}')
    print(f'\nOAUTH_CLIENT_SECRET:\n{client_secret}')
    print(f'\nOAUTH_REFRESH_TOKEN:\n{creds.refresh_token}')
    print('=' * 60)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 get_refresh_token.py path/to/client_secret.json')
        sys.exit(1)
    main(sys.argv[1])
