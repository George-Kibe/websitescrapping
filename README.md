# Web scraping & automation projects

A collection of small, independent Python projects for scraping websites and
automating browsers and APIs: BeautifulSoup, Scrapy, Selenium, Playwright,
yt-dlp, Django, Tweepy and Tkinter.

Each project lives in its own folder with its own `requirements.txt`, so
install only what you need, in its own virtual environment.

| Project | What it does | Main libraries |
| --- | --- | --- |
| [`YoutubeDownloader/`](#youtubedownloader) | Download YouTube videos/audio and list a channel's videos | yt-dlp |
| [`beautifulsoup/`](#beautifulsoup) | Stand-alone scrapers: IMDb Top 250, rental listings, leaderboards, tables, contact details | requests, BeautifulSoup, openpyxl |
| [`scrapy/postscrape/`](#scrapy-projects) | Scrapy spider for blog posts on zyte.com | Scrapy |
| [`scrapy/whiskyscrapper/`](#scrapy-projects) | Scrapy spider for whisky names and prices on whiskyshop.com | Scrapy |
| [`amazon-deals-bot/`](#amazon-deals-bot) | Finds Amazon coupons and deals and posts them to Telegram | Playwright, BeautifulSoup |
| [`Atuspid/atuspid_amazon/`](#atuspid-django-app) | Django web app with buttons that run the Amazon deal jobs, plus an async-views demo | Django, Playwright, aiohttp |
| [`selenium/`](#selenium) | Browser automation demos (search, navigation, Cookie Clicker bot) | Selenium |
| [`twitter_bot/`](#twitter_bot) | X (Twitter) API v2 command-line bot | Tweepy |
| [`tkinter-projects/`](#tkinter-projects) | Student data entry desktop form that saves to console, Excel or SQLite | Tkinter, openpyxl |

## Getting started

Requirements: **Python 3.11 or newer** (3.12+ recommended).

For any project:

```bash
cd <project-folder>
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Projects that need credentials read them from environment variables or from a
`.env` file in the project folder. Copy the project's `.env.example` to `.env`
and fill it in. `.env` files are git-ignored; never commit real keys.

Most projects include offline tests that check the parsing logic against small
HTML samples:

```bash
python -m unittest discover -s tests -t .      # inside the project folder
python manage.py test                          # for the Django app
```

> Websites change their HTML often. If a scraper suddenly returns nothing,
> inspect the page in your browser's developer tools and update the CSS
> selectors. Always respect each site's terms of service and `robots.txt`.

---

## YoutubeDownloader

Downloads a YouTube video (or just the audio) into `YoutubeDownloader/downloads/`,
and lists the videos on a channel.

**Extra requirement:** [ffmpeg](https://ffmpeg.org/download.html) on your `PATH`
(used to merge video and audio streams).

```bash
python download_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID"
python download_youtube.py --audio-only "https://www.youtube.com/watch?v=VIDEO_ID"
python download_youtube.py                       # prompts for a URL

python list_channel_videos.py "https://www.youtube.com/@SomeChannel" --limit 20 --csv videos.csv
```

YouTube now makes yt-dlp solve a JavaScript challenge. Installing
`yt-dlp[default,deno]` (already in `requirements.txt`) gives you both the
challenge-solver scripts and the deno JavaScript runtime. Node.js also works if
you already have it. **If downloads start failing with `HTTP Error 403`, update
first:** `pip install -U "yt-dlp[default,deno]"`.

## beautifulsoup

Stand-alone scripts built on `requests` + BeautifulSoup (`lxml` parser), sharing
helpers in `common.py` (browser-like headers, timeouts, CSV writing).

| Script | Output |
| --- | --- |
| `imdb_top_movies.py` | IMDb Top 250 (rank, title, rating, votes, genre, URL) in `IMDB Movie Ratings.xlsx` |
| `pararius_listings.py [--city amsterdam] [--pages 3]` | Rental listings from pararius.com in `housing.csv` |
| `umg_leaderboard.py` | UMG Gaming XP leaderboard, printed and saved to `leaderboard.csv` |
| `table_scraper.py URL [--selector CSS] [--rows CSS]` | Every HTML table on a page saved as `table_N.csv` |
| `contact_extractor.py URL` | Phone numbers and email addresses found on a page |

## Scrapy projects

Two separate Scrapy projects, each with its own `requirements.txt`. Both obey
`robots.txt`, throttle themselves, and follow pagination. Run them from inside
the project folder:

```bash
cd scrapy/postscrape
scrapy crawl posts -O posts.json         # title, date, author of each blog post

cd scrapy/whiskyscrapper
scrapy crawl whisky -O whisky.csv        # name, price (GBP), in_stock, link
```

Items are dataclasses (`items.py`). The pipelines drop incomplete items, and
`postscrape` also drops duplicates.

## amazon-deals-bot

Checks Amazon for coupons, today's deals, or discounted search results and posts
each one (photo + caption) to a Telegram chat. Amazon loads its content with
JavaScript, so pages are rendered in headless Chromium via Playwright.

```bash
pip install -r requirements.txt
playwright install chromium               # one-time browser download
cp .env.example .env                      # add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID

python amazon_deals.py coupons            # one random coupon category
python amazon_deals.py daily              # today's deals
python amazon_deals.py search             # discounted search results (2 pages)
python amazon_deals.py coupons --loop     # keep going until Ctrl+C
python amazon_deals.py daily --dry-run    # print instead of posting to Telegram
```

Create a bot token with [@BotFather](https://t.me/BotFather) and add the bot to
your group or channel.

## Atuspid Django app

A Django 5.2 LTS web UI for the Amazon deal jobs above. Each button starts a job
in the background and returns straight away; results go to Telegram.

```bash
cd Atuspid/atuspid_amazon
pip install -r requirements.txt
playwright install chromium
cp .env.example .env        # set DJANGO_DEBUG=true for local use, plus Telegram settings
python manage.py migrate
python manage.py runserver
```

- `http://127.0.0.1:8000/` shows the Coupons / Today's deals / Discounted search results buttons.
- `http://127.0.0.1:8000/async/books/` is an async Django view that fetches four
  pages of books.toscrape.com at the same time with `aiohttp` and returns the titles as JSON.
- `testingasync/taskstogether.py` and `testingasync/testaiohttp.py` are stand-alone
  asyncio learning scripts.

With `DJANGO_DEBUG` not set to `true`, the app requires `DJANGO_SECRET_KEY` and
enables HTTPS-only cookies and redirects (production mode).

## selenium

Selenium 4 demos. Selenium Manager downloads the right chromedriver automatically;
you only need Google Chrome installed.

```bash
python selenium_bot.py "python" [--headless]   # search techwithtim.net and print results
python selenium_events.py [--headless]         # click through links, go back/forward
python advanced_events.py [--clicks 5000]      # play Cookie Clicker and buy upgrades
```

## twitter_bot

A command-line bot for the X (Twitter) API v2 using Tweepy.

```bash
cp .env.example .env      # add keys from https://developer.x.com/en/portal/dashboard
python bot.py verify
python bot.py tweet "Hello from Python"
python bot.py search "#python -is:retweet" --max 10
python bot.py mentions
```

The Free API tier can post and read your own account. Search and mentions need
the Basic tier or higher.

## tkinter-projects

A Tkinter student data entry form (based on
[this tutorial](https://youtu.be/vusUfPBsggw)) that validates the input and
saves each entry to the backend you choose:

```bash
python main.py                    # print entries to the console
python main.py --storage excel    # append to tkinter-projects/data.xlsx
python main.py --storage sqlite   # insert into tkinter-projects/data.db
```

Tkinter ships with the python.org installers. On Linux you may need the
`python3-tk` package.
