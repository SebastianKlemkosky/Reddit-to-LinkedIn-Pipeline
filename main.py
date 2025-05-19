# main.py

from reddit import get_reddit_client, fetch_recent_posts, select_best_post, is_safe_post
import config


def main():
    reddit = get_reddit_client()
    print(f"Logged in as: {reddit.user.me()}")

    for subreddit in config.SUBREDDITS:
        posts = fetch_recent_posts(subreddit, limit=10, mode="top")
        print(f"\nFetched {len(posts)} posts from r/{subreddit}:")
        for i, post in enumerate(posts, start=1):
            print(f"{i}. {post['title']}")

if __name__ == "__main__":
    main()
