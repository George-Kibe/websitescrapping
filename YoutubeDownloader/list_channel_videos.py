"""
List the videos published on a YouTube channel.

Usage:
    python list_channel_videos.py "https://www.youtube.com/@SomeChannel"
    python list_channel_videos.py "https://www.youtube.com/@SomeChannel" --limit 20 --csv videos.csv

Uses yt-dlp's "flat" extraction, which reads the channel's video list
without downloading anything or rendering the page in a browser.
"""

import argparse
import csv
import sys

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


def list_videos(channel_url: str, limit: int | None = None) -> list[dict]:
    if not channel_url.rstrip("/").endswith("/videos"):
        channel_url = channel_url.rstrip("/") + "/videos"

    options = {
        "extract_flat": "in_playlist",
        "quiet": True,
        "js_runtimes": {"deno": {}, "node": {}},
    }
    if limit:
        options["playlistend"] = limit

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    return [
        {
            "title": entry.get("title"),
            "url": entry.get("url") or f"https://www.youtube.com/watch?v={entry['id']}",
            "views": entry.get("view_count"),
        }
        for entry in info.get("entries") or []
        if entry
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="List the videos on a YouTube channel.")
    parser.add_argument("channel_url", help="e.g. https://www.youtube.com/@SomeChannel")
    parser.add_argument("--limit", type=int, help="only list the newest N videos")
    parser.add_argument("--csv", metavar="PATH", help="also write the results to a CSV file")
    args = parser.parse_args()

    try:
        videos = list_videos(args.channel_url, args.limit)
    except DownloadError as e:
        sys.exit(f"Failed to read channel: {e}")

    for video in videos:
        print(f"{video['title']}\n  {video['url']}")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "url", "views"])
            writer.writeheader()
            writer.writerows(videos)
        print(f"\nSaved {len(videos)} videos to {args.csv}")


if __name__ == "__main__":
    main()
