# Import needed libs
import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# initialise "telePython.env", raises a message if .env is not found
REPO_ROOT = Path(__file__).resolve().parents[2]
ENV = os.getenv("ENV", "prod")
env_path = REPO_ROOT / "gitops" / "env" / ENV / "telePython.env"

if not env_path.exists():
    raise FileNotFoundError(f"telePython.env file not found: {env_path}")

# from "telePython.env", populates the env vars
load_dotenv(env_path)
API_BASE = os.getenv('API_BASE')
API_VERSION = os.getenv('API_VERSION')
API_KEY = os.getenv('API_KEY')
COOKIE_TOKEN = os.getenv('COOKIE_TOKEN')
MAGNET_TEST = os.getenv('MAGNET_TEST')
TELE_BOT_TOKEN = os.getenv('TELE_BOT_TOKEN')

# Functions list
def get_torrentID(magnet_link: str) -> str:
    # ADD DESCRIPTION + FUNC ARGS HERE #

    # Extract torrent ID from magnet link
    url = f"{API_BASE}/{API_VERSION}/api/torrents/createtorrent"
    
    payload = {
        'magnet': f'{magnet_link}',
        'seed': '1',
        'allow_zip': '0',
        'add_only_if_cached': '0'
    }

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Cookie': f'{COOKIE_TOKEN}'
    }

    response = (
        json.loads(
            requests.request("POST", url, headers=headers, data=payload, files=None)
            .text
        )
    )

    results = {
        "successStatus": response['success'],
        "errorMessage": response['error'],
        "cacheFound": response['detail'],
        "torrentID": response['data']['torrent_id'],
        "hashID": response['data']['hash']
    }

    return (
        results
    )

def get_torrentDownload(torrentID: int) -> int:
    # ADD DESCRIPTION + FUNC ARGS HERE #

    url = f"{API_BASE}/{API_VERSION}/api/torrents/requestdl?token={API_KEY}&torrent_id={torrentID}&zip_link=1"

    # payload = {}
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Cookie': f'{COOKIE_TOKEN}'
    }

    response = (
        json.loads(
            requests.request("GET", url, headers=headers, data=None)
            .text
        )
    )

    results = {
        "successStatus": response['success'],
        "errorMessage": response['error'],
        "downloadLink": response['data']
    }

    return (
        results
    )