# config.py
from dotenv import load_dotenv
import os

load_dotenv()

# Reddit
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

# OpenAI
CHATGPT_SECRET = os.getenv("CHATGPT_SECRET")

# Subreddits and template remain as is
SUBREDDITS = [
    "programming",
    "learnprogramming",
    "ProgrammerHumor"
]

GPT_TEMPLATE = """
You are a professional content writer managing a LinkedIn profile for someone in the software development and IT industry.

Here is a post pulled from Reddit:
{post_json}

Your task is to rewrite this into a LinkedIn post that is appropriate for a professional audience. Specifically:

- If the post contains profanity or slang (e.g., "fucking", "wtf", "omfg", etc.), remove or replace them with clean, professional alternatives.
- Simplify complex or cluttered language where needed.
- Preserve the core message or humor if it's appropriate — but avoid meme tone or Reddit-style formatting.
- Use bullet points or a clean paragraph structure if possible.
- Add helpful context or a closing insight if the original post is minimal.
- Write it as something the user might share to educate, reflect, or spark discussion in the tech community.

The final output should be professional, readable, and LinkedIn-ready — even if the original post was short, edgy, or meme-like.
"""