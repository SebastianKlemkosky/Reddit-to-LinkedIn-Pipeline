# main.py
import config
from reddit import get_reddit_client, fetch_and_filter_posts, select_best_post
from chat_gpt import rewrite_post_for_linkedin
from dotenv import load_dotenv
import os

load_dotenv()

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    reddit = get_reddit_client()
    print(f"Logged in as: {reddit.user.me()}")

    all_filtered_posts = []

    for subreddit in config.SUBREDDITS:
        filtered = fetch_and_filter_posts(subreddit, limit=25, mode="top")
        print(f"\nr/{subreddit}: {len(filtered)} safe posts")
        all_filtered_posts.extend(filtered)

    best_post = select_best_post(all_filtered_posts)

    if best_post:
        print("\n🟢 Selected Best Post:")
        print(f"Title: {best_post['title']}")
        print(f"Score: {best_post['score']}")
        print(f"Link: {best_post['url']}")

        # ✅ Image detection
        has_image = bool(best_post.get("image_url"))
        print(f"Image present: {'Yes' if has_image else 'No'}")
        if has_image:
            print(f"Image URL: {best_post['image_url']}")
    else:
        print("\n⚠️ No suitable posts found.")
        return  # exit early if no post

    linkedin_post = rewrite_post_for_linkedin(best_post)

    print("\n✍️ LinkedIn-ready content:\n")
    print(linkedin_post)


if __name__ == "__main__":
    main()
