# reddit.py

import config
import praw
import json
from pathlib import Path
from utils import load_blacklist_from_folder

BLACKLIST_WORDS = load_blacklist_from_folder("Blacklist words")
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

    if mode == "top":
        listings = subreddit.top(time_filter="day", limit=limit)
    elif mode == "hot":
        listings = subreddit.hot(limit=limit)
    else:
        listings = subreddit.new(limit=limit)

    recent_posts = []
    for post in listings:
        post_data = {
            'id': post.id,
            'title': post.title,
            'text': post.selftext,
            'score': post.score,
            'url': post.url,
            'is_self': post.is_self,
            'over_18': post.over_18,
            'image_url': None
        }

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
    return not any(bad_word in text for bad_word in BLACKLIST_WORDS)

def is_duplicate(post_id, log_file=LOG_FILE):
    try:
        if not Path(log_file).exists():
            return False
        with open(log_file, "r") as f:
            posted_ids = json.load(f)
        return post_id in posted_ids
    except Exception:
        return False

def log_post(post_id, log_file=LOG_FILE):
    try:
        posted_ids = []
        if Path(log_file).exists():
            with open(log_file, "r") as f:
                posted_ids = json.load(f)
    except Exception:
        posted_ids = []

    posted_ids.append(post_id)
    with open(log_file, "w") as f:
        json.dump(posted_ids, f)

def fetch_and_filter_posts(subreddit, limit=10, mode="top"):
    raw_posts = fetch_recent_posts(subreddit, limit, mode)
    return [
        p for p in raw_posts
        if is_safe_post(p) and not is_duplicate(p["id"])
    ]

def select_best_post(posts):
    def score_post(post):
        score = post["score"]
        score += len(post["text"]) // 20
        if post.get("image_url"):
            score += 20
        return score

    if not posts:
        return None

    best = max(posts, key=score_post)
    log_post(best["id"])
    return best
