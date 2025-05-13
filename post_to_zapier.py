# post_to_zapier.py

import os
import requests

def post_to_substack_zap(title, content):
    webhook_url = os.getenv("ZAPIER_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("Missing ZAPIER_WEBHOOK_URL environment variable")

    payload = {
        "title": title,
        "content": content
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Zapier webhook failed: {response.status_code} - {response.text}")
    else:
        print("📬 Substack draft sent successfully via Zapier")
