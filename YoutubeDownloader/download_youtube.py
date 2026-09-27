"""
Simple YouTube downloader for personal reference use.

Usage:
    python download_youtube.py
    (then paste a YouTube URL when prompted)

    or

    python download_youtube.py "https://www.youtube.com/watch?v=XXXXXXXX"
    python download_youtube.py --audio-only "https://www.youtube.com/watch?v=XXXXXXXX"

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

import argparse
import sys
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

DOWNLOAD_DIR = Path(__file__).parent / "downloads"


def build_options(audio_only: bool = False) -> dict:
    options = {
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s [%(id)s].%(ext)s"),
        "noplaylist": True,  # only download the single video, not a whole playlist
        "restrictfilenames": True,  # avoid special characters that can break filesystems
        # JavaScript runtimes used to solve YouTube's challenges (first one found is used)
        "js_runtimes": {"deno": {}, "node": {}},
    }
    if audio_only:
        options["format"] = "bestaudio[ext=m4a]/bestaudio"
    else:
        # Best video+audio, merged into an mp4 where possible
        options["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        options["merge_output_format"] = "mp4"
    return options


def download_video(url: str, audio_only: bool = False) -> None:
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    with YoutubeDL(build_options(audio_only)) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "video")
        print(f"\nDone. Saved '{title}' to: {DOWNLOAD_DIR.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a YouTube video.")
    parser.add_argument("url", nargs="?", help="video URL (prompted for if omitted)")
    parser.add_argument("--audio-only", action="store_true", help="download the audio track only")
    args = parser.parse_args()

    url = (args.url or input("Enter YouTube URL: ")).strip()
    if not url:
        sys.exit("No URL provided. Exiting.")

    try:
        download_video(url, audio_only=args.audio_only)
    except DownloadError as e:
        sys.exit(f"Failed to download video: {e}")


if __name__ == "__main__":
    main()
