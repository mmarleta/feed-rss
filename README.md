# 📡 RSS Feed Monitor

> Async RSS monitor with AI-powered content generation and multi-platform notifications.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- 🔄 **Async RSS Processing** — Fetches multiple feeds concurrently using `aiohttp`
- 🔍 **Smart Filtering** — Keyword-based filtering with configurable time windows
- 🤖 **AI Content Generation** — Generates YouTube Shorts scripts via OpenAI API
- 📱 **Multi-Platform Delivery** — Telegram and Discord webhook support
- 🗃️ **Deduplication** — Tracks seen items to avoid duplicates
- ⚙️ **Flexible Config** — Environment variables + CLI arguments

## Quick Start

```bash
# Clone and setup
git clone https://github.com/mmarleta/feed-rss.git
cd feed-rss
pip install -r requirements.txt

# Run with defaults
python -m rss_monitor.main --limit 5

# With AI generation
export OPENAI_API_KEY="your_key"
python -m rss_monitor.main --limit 5
```

## Configuration

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--limit` | Max items per run | 10 |
| `--max-age-hours` | Time window in hours | 24 |
| `--no-ai` | Disable AI genetion | false |
| `--telegram` | Send to Telegram | false |
| `--discord` | Send to Discord | false |

### Environment Variables

```bash
# AI
OPENAI_API_KEY=sk-...
MODEL=gpt-4o-mini

# Telegram
TELEGRAM_ENABLED=true
TELEGRAM_BOT_TOKEN=123:abc
TELEGRAM_CHAT_ID=999999

# Discord
DISCORD_ENABLED=true
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

## Architecture

```
rss_monitor/
├── main.py          # Entry point & orchestration
├── config.py        # Settings management (pydantic-settings)
├── models.py        # Data models
├── services/
│   ├── feed.py      # RSS fetching & parsing
│   ├── ai.py        # OpenAI integration
│   └── notification.py  # Telegram/Discord delivery
└── utils.py         # Helpers
```

## Use Cases

- 📰 **News Aggregation** — Monitor tech/AI feeds for relevant content
- 🎬 **Content Creation** — Auto-generate video scripts from news
- 🔔 **Alerts** — Get notified about specific topics via Telegram/Discord
- 💊 **Research** — Track industry trends with keyword filtering

## Scheduling

```bash
# Cron (every 20 minutes)
*/20 * * * * cd /path/to/feed-rss && python -m rss_monitor.main >> rss.log 2>&1
```

See `ops/` for systemd service examples.

## Tech Stack

- **Python 3.10+**
- **aiohttp** — Async HTTP
- **feedparser** — RSS parsing
- **OpenAI** — Content generation
- **Pydantic** — Config & validation

## License

MIT

---

Built by [Marcelo Marleta](https://github.com/mmarleta)
