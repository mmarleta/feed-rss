from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    FEEDS: List[str] = [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "https://www.wired.com/feed/tag/artificial-intelligence/latest/rss",
        "https://arstechnica.com/feed/",
        "https://www.technologyreview.com/feed/",
        "https://www.engadget.com/rss.xml",
    ]
    
    KEYWORDS: List[str] = [
        "ia", "ai", "inteligência artificial", "inteligencia artificial",
        "openai", "chatgpt", "gpt-", "gpt ", "gemini", "claude",
        "llm", "nvidia", "machine learning", "aprendizado de máquina",
        "modelo generativo", "robô", "robot", "neural", "rag",
    ]

    MAX_AGE_HOURS: int = 24
    LIMIT: int = 10
    MODEL: str = "gpt-4o-mini"
    
    # Paths
    STATE_FILE: str = "data/seen_items.json"
    SAVE_DIR: str = ""  # Empty means don't save JSONs by default
    
    # Integrations
    OPENAI_API_KEY: str = ""
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    DISCORD_WEBHOOK_URL: str = ""
    
    # Flags
    NO_AI: bool = False
    TELEGRAM_ENABLED: bool = False
    DISCORD_ENABLED: bool = False
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
