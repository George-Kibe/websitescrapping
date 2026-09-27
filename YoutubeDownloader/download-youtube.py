"""
Simple YouTube downloader for personal reference use.

Usage:
    python download_youtube.py
    (then paste a YouTube URL when prompted)

    or

    python download_youtube.py "https://www.youtube.com/watch?v=XXXXXXXX"

Downloads are saved into a local "downloads/" folder, with the video
title used as the filename. Requires yt-dlp (see requirements.txt) and
ffmpeg installed on your system (needed to merge separate video/audio
streams into a single file).

YouTube now requires a JavaScript runtime to solve its download
challenges; without one, yt-dlp falls back to limited clients whose
stream URLs fail with "HTTP Error 403: Forbidden". Installing the
requirements (yt-dlp[default,deno]) provides both the solver scripts
and a deno runtime. An existing Node.js install also works.
"""

import sys
from pathlib import Path

from yt_dlp import YoutubeDL

DOWNLOAD_DIR = Path(__file__).parent / "downloads"


def download_video(url: str) -> None:
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    ydl_opts = {
        # Best video+audio, merged into an mp4 where possible
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s [%(id)s].%(ext)s"),
        "noplaylist": True,       # only download the single video, not a whole playlist
        "restrictfilenames": True,  # avoid special characters that can break filesystems
        "quiet": False,
        "no_warnings": False,
        # JavaScript runtimes used to solve YouTube's challenges (first one found is used)
        "js_runtimes": {"deno": {}, "node": {}},
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "video")
        print(f"\nDone. Saved '{title}' to: {DOWNLOAD_DIR.resolve()}")


def main() -> None:
    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
    else:
        url = input("Enter YouTube URL: ").strip()

    if not url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    try:
        download_video(url)
    except Exception as e:
        print(f"Failed to download video: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()