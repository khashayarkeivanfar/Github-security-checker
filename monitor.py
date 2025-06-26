import time
import requests
import sys, io


print(" monitor.py is running—changes are live!")


import traceback

from utils import github_headers, is_repo_blacklisted
from config import POLL_INTERVAL
from scanner_wrapper import scan_github_repo
from output import save_findings

GITHUB_EVENTS_URL = "https://api.github.com/events"
seen_repos = set()


def monitor_github_events():
    print("[*] Starting GitHub public event monitor...")
    while True:
        try:
            response = requests.get(GITHUB_EVENTS_URL, headers=github_headers(), timeout=10)
            if response.status_code != 200:
                print(f"[WARN] GitHub API error {response.status_code}: {response.text}")
                time.sleep(POLL_INTERVAL)
                continue

            events = response.json()

            for event in events:
                if event.get("type") not in ["PushEvent", "CreateEvent"]:
                    continue
                if is_repo_blacklisted(event):
                    continue

                repo = event.get("repo", {}).get("name")
                if not repo:
                    continue

                repo_url = f"https://github.com/{repo}"

                if repo_url in seen_repos:
                    continue
                seen_repos.add(repo_url)

                print(f"[+] Scanning new repo: {repo_url}")
                findings = scan_github_repo(repo_url)

                if findings:
                    print(f"[!] Secrets found in {repo_url} - {len(findings)} hits")
                    save_findings(findings)
                else:
                    print(f"[-] No secrets in {repo_url}")

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("[*] Monitor stopped by user.")
            break
        except Exception:
           
            with open("monitor.log", "a", encoding="utf-8") as log_file:
                log_file.write(traceback.format_exc())
            
            print("[ERROR] Exception in monitor loop. See monitor.log for details.")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    monitor_github_events()
