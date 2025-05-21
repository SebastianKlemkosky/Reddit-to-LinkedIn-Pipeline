import os
import json

def load_blacklist_from_folder(folder_path):
    bad_words = set()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        word = line.strip().lower()
                        if word:
                            bad_words.add(word)

            elif file.endswith(".json"):
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        words = json.load(f)
                        for word in words:
                            if isinstance(word, str):
                                bad_words.add(word.strip().lower())
                    except Exception as e:
                        print(f"⚠️ Failed to load {path}: {e}")

    return list(bad_words)

import json
from pathlib import Path
from datetime import datetime

LOG_FILE = "rewritten_log.json"

# Token pricing (as of May 2025)
COSTS = {
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-3.5-turbo": {"input": 0.001, "output": 0.002}
}

def log_rewritten_post(post, rewritten, input_tokens=None, output_tokens=None, model="gpt-4o"):
    # Cost calculation
    input_cost = (input_tokens or 0) / 1000 * COSTS.get(model, {}).get("input", 0)
    output_cost = (output_tokens or 0) / 1000 * COSTS.get(model, {}).get("output", 0)
    total_cost = round(input_cost + output_cost, 5) if input_tokens and output_tokens else None

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "title": post.get("title"),
        "text": post.get("text"),
        "rewritten": rewritten,
        "image_url": post.get("image_url"),
        "external_url": post.get("url"),
        "reddit_url": f"https://www.reddit.com/comments/{post.get('id')}",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": total_cost
    }

    try:
        if Path(LOG_FILE).exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        data.append(entry)

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"⚠️ Could not log rewritten post: {e}")
