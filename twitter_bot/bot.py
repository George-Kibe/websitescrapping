"""
Small X (Twitter) API v2 command-line bot built on Tweepy.

Usage:
    python bot.py verify                      # check your credentials
    python bot.py tweet "Hello from Python"   # post a tweet
    python bot.py search "#python -is:retweet" --max 10
    python bot.py mentions --max 10

Credentials come from environment variables (or a .env file next to this
script); see .env.example. Create them in the X developer portal:
https://developer.x.com/en/portal/dashboard

Which endpoints work depends on your API access tier: the Free tier can
post tweets and read your own account, while searching and reading
mentions need the Basic tier or higher.
"""

import argparse
import os
import sys
from pathlib import Path

import tweepy
from dotenv import load_dotenv

REQUIRED = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"]


def make_client() -> tweepy.Client:
    load_dotenv(Path(__file__).with_name(".env"))
    missing = [name for name in REQUIRED if not os.getenv(name)]
    if missing:
        sys.exit(f"Missing environment variables: {', '.join(missing)} (see .env.example)")
    return tweepy.Client(
        bearer_token=os.getenv("X_BEARER_TOKEN"),
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
        wait_on_rate_limit=True,
    )


def verify(client: tweepy.Client, args) -> None:
    me = client.get_me(user_auth=True).data
    print(f"Authenticated as @{me.username} (id {me.id})")


def tweet(client: tweepy.Client, args) -> None:
    response = client.create_tweet(text=args.text)
    print(f"Posted: https://x.com/i/web/status/{response.data['id']}")


def search(client: tweepy.Client, args) -> None:
    response = client.search_recent_tweets(
        query=args.query, max_results=args.max, tweet_fields=["created_at"], user_auth=True
    )
    for item in response.data or []:
        print(f"[{item.created_at:%Y-%m-%d %H:%M}] {item.id}\n  {item.text}\n")
    if not response.data:
        print("No tweets found.")


def mentions(client: tweepy.Client, args) -> None:
    me = client.get_me(user_auth=True).data
    response = client.get_users_mentions(me.id, max_results=args.max, user_auth=True)
    for item in response.data or []:
        print(f"{item.id}: {item.text}\n")
    if not response.data:
        print("No mentions found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="X (Twitter) API v2 bot.")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("verify", help="check your credentials").set_defaults(func=verify)

    tweet_parser = commands.add_parser("tweet", help="post a tweet")
    tweet_parser.add_argument("text")
    tweet_parser.set_defaults(func=tweet)

    search_parser = commands.add_parser("search", help="search tweets from the last 7 days")
    search_parser.add_argument("query")
    search_parser.add_argument("--max", type=int, default=10, help="10-100 (default 10)")
    search_parser.set_defaults(func=search)

    mentions_parser = commands.add_parser("mentions", help="show recent mentions of your account")
    mentions_parser.add_argument("--max", type=int, default=10, help="5-100 (default 10)")
    mentions_parser.set_defaults(func=mentions)

    args = parser.parse_args()
    try:
        args.func(make_client(), args)
    except tweepy.TweepyException as error:
        sys.exit(f"X API error: {error}")


if __name__ == "__main__":
    main()
