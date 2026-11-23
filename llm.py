"""Call GPT-OSS-120B on Purdue's RCAC GenAI server. API key is read from .env (RCAC_API_KEY=...)."""
import os
import time
from pathlib import Path

import requests

URL = "https://genai.rcac.purdue.edu/api/chat/completions"
MODEL = "gpt-oss:120b"

# Read RCAC_API_KEY from .env (unless it's already set in the shell).
for line in (Path(__file__).resolve().parent / ".env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())

#this is the api call 
def ask_llm(prompt):
    """Send one prompt, return the text reply. Waits and retries on the 20 calls/min limit and on server
    errors/timeouts (5xx), which the RCAC server returns now and then. The server reports the rate limit
    as 429 or (since Nov 2026) as 400 {"detail":"Rate limit exceeded. Please try again later."}; it
    resets within about a minute."""
    headers = {"Authorization": f"Bearer {os.environ['RCAC_API_KEY']}"}
    body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0}
    for attempt in range(10):
        try:
            r = requests.post(URL, headers=headers, json=body, timeout=300)
        except requests.exceptions.RequestException:
            time.sleep(30)
            continue
        rate_limited = r.status_code == 429 or (r.status_code == 400 and "rate limit" in r.text.lower())
        if rate_limited or r.status_code >= 500:
            time.sleep(60 if rate_limited else 30)
            continue
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    raise RuntimeError("RCAC server: gave up after 10 tries")
