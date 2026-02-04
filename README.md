# feed-rss

Async RSS monitor that watches feeds, filters by keywords, and optionally generates content using OpenAI. Sends notifications to Telegram or Discord.

Built this to track AI/tech news and auto-generate short-form video scripts from interesting articles.

## Setup

```bash
pip install -r requirements.txt
python -m rss_monitor.main --limit 5
```

For AI generation, set `OPENAI_API_KEY`. For notifications, configure Telegram/Discord in env vars (see `.env.example`).

## How it works

- Fetches feeds async with aiohttp
- Filters items by keywords and time window
- Optionally sends to GPT for content generation
- Delivers via Telegram/Discord webhooks
- Tracks seen items to avoid spam

## Running on a schedule

```bash
# cron, every 20 min
*/20 * * * * cd /path/to/feed-rss && python -m rss_monitor.main >> rss.log 2>&1
```

There's a systemd service example in `ops/` if you prefer that.

## Stack

Python 3.10+, aiohttp, feedparser, OpenAI, pydantic-settings
