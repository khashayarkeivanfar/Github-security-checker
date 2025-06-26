import random
import requests
from config import GITHUB_TOKENS, BLACKLISTED_USERS

def get_random_token():
    return random.choice(GITHUB_TOKENS)

def github_headers():
    return {
        "Authorization": f"token {get_random_token()}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "SecretScannerBot"
    }

def is_repo_blacklisted(event):
    try:
        actor = event.get("actor", {}).get("login", "")
        return actor.lower() in BLACKLISTED_USERS
    except:
        return True
    
from config import CONTEXT_KEYWORDS

def in_context(text: str, start: int, end: int, window: int = 50) -> bool:
    low = text[max(0, start-window): start].lower() + text[end: end+window].lower()
    return any(kw in low for kw in CONTEXT_KEYWORDS)

def get_context_snippet(text: str, start: int, end: int, window: int = 30) -> str:
    pre = text[max(0, start-window): start]
    match = text[start:end]
    post = text[end:end+window]
    snippet = (pre + match + post).replace('\n', ' ').strip()
    return snippet

def iter_json_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from iter_json_strings(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_json_strings(item)