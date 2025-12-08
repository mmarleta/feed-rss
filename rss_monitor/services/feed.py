import asyncio
import logging
import feedparser # type: ignore
import aiohttp
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from rss_monitor.models import NewsItem

class FeedService:
    def __init__(self, max_age_hours: int):
        self.max_age_hours = max_age_hours

    async def fetch_all(self, urls: List[str]) -> List[NewsItem]:
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_feed(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        all_items = []
        for res in results:
            if isinstance(res, list):
                all_items.extend(res)
            else:
                logging.error(f"Erro ao buscar feed: {res}")
        return all_items

    async def _fetch_feed(self, session: aiohttp.ClientSession, url: str) -> List[NewsItem]:
        logging.info("Lendo feed: %s", url)
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                content = await response.text()
                return self._parse_feed(content, url)
        except Exception as e:
            logging.error(f"Falha no feed {url}: {e}")
            return []

    def _parse_feed(self, content: str, source: str) -> List[NewsItem]:
        parsed = feedparser.parse(content)
        items: List[NewsItem] = []
        for entry in parsed.entries:
            normalized = self._normalize_entry(dict(entry), source)
            if normalized:
                items.append(normalized)
        return items

    def _normalize_entry(self, entry: dict, source: str) -> Optional[NewsItem]:
        entry_id = entry.get("id") or entry.get("link")
        if not entry_id:
            return None

        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        summary = (entry.get("summary") or entry.get("description") or "").strip()
        published_dt = self._parse_datetime(entry)
        
        # Age check
        if not published_dt:
            logging.debug(f"Item {title} sem data. Usando data atual.")
            published_dt = datetime.now(timezone.utc)

        if not self._is_recent(published_dt):
            return None

        return NewsItem(
            source=source,
            id=entry_id,
            title=title,
            link=link,
            summary=summary,
            published=published_dt,
        )

    def _parse_datetime(self, entry: dict) -> Optional[datetime]:
        time_struct = entry.get("published_parsed") or entry.get("updated_parsed")
        if not time_struct:
            return None
        return datetime.fromtimestamp(
            int(datetime(*time_struct[:6]).timestamp()), tz=timezone.utc
        )

    def _is_recent(self, published: Optional[datetime]) -> bool:
        if not published:
            return False
        now = datetime.now(timezone.utc)
        return now - published <= timedelta(hours=self.max_age_hours)
