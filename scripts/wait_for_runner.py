import os
import time
import requests

OWNER = os.environ["GITHUB_REPOSITORY_OWNER"]
REPO = os.environ["GITHUB_REPOSITORY"].split("/")[1]

TOKEN = os.environ["PAT_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}

URL = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runners"

timeout = 300
interval = 10

start = time.time()

while time.time() - start < timeout:
    response = requests.get(URL, headers=HEADERS, timeout=30)

    data = response.json()

    for runner in data.get("runners", []):
        labels = [x["name"] for x in runner["labels"]]

        if "hetzner-ephemeral" in labels:
            if runner["status"] == "online":
                print("Runner online")
                raise SystemExit(0)

    print("Waiting runner...")
    time.sleep(interval)

raise SystemExit(1)
