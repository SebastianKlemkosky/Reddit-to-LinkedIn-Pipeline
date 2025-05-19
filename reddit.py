# reddit.py

import config
import praw
from datetime import datetime, timedelta
import json
from pathlib import Path

LOG_FILE = "posted_log.json"


def get_reddit_client():
    return praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        user_agent=config.REDDIT_USER_AGENT,
        username=config.REDDIT_USERNAME,
        password=config.REDDIT_PASSWORD
    )

def fetch_recent_posts(subreddit_name, limit=10, mode="top"):
    reddit = get_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)

    recent_posts = []

    if mode == "top":
        listings = subreddit.top(time_filter="day", limit=limit)
    elif mode == "hot":
        listings = subreddit.hot(limit=limit)
    else:
        listings = subreddit.new(limit=limit)

    for post in listings:
        post_data = {
            'id': post.id,
            'title': post.title,
            'text': post.selftext,
            'score': post.score,
            'url': post.url,
            'is_self': post.is_self,
            'image_url': None
        }

        # Detect image
        if hasattr(post, 'post_hint') and post.post_hint == 'image':
            post_data['image_url'] = post.url
        elif 'i.redd.it' in post.url or 'imgur.com' in post.url:
            post_data['image_url'] = post.url

        recent_posts.append(post_data)

    return recent_posts

def is_safe_post(post):
    if post.get("over_18"):
        return False

    text = f"{post.get('title', '')} {post.get('text', '')}".lower()
    if any(bad_word in text for bad_word in BLACKLIST_WORDS):
        return False

    return True

def is_duplicate(post_id):
    if not Path(LOG_FILE).exists():
        return False

    with open(LOG_FILE, "r") as f:
        posted_ids = json.load(f)

    return post_id in posted_ids

def log_post(post_id):
    posted_ids = []
    if Path(LOG_FILE).exists():
        with open(LOG_FILE, "r") as f:
            posted_ids = json.load(f)

    posted_ids.append(post_id)
    with open(LOG_FILE, "w") as f:
        json.dump(posted_ids, f)

def select_best_post(posts):
    def score_post(post):
        score = post["score"]
        score += len(post["text"]) // 20
        if post.get("image_url"):
            score += 20
        return score

    valid_posts = [
        post for post in posts
        if is_safe_post(post) and not is_duplicate(post["id"])
    ]

    if not valid_posts:
        return None

    best = max(valid_posts, key=score_post)
    log_post(best["id"])
    return best


if __name__ == "__main__":
    reddit = get_reddit_client()
    print(f"Logged in as: {reddit.user.me()}")

