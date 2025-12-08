from typing import List
from rss_monitor.models import NewsItem

class FilterService:
    def __init__(self, keywords: List[str]):
        self.keywords = [k.lower() for k in keywords]

    def matches_keywords(self, text: str) -> bool:
        text_lower = text.lower()
        return any(kw in text_lower for kw in self.keywords)

    def filter_items(self, items: List[NewsItem]) -> List[NewsItem]:
        filtered = []
        for item in items:
            blob = f"{item.title} {item.summary}"
            if self.matches_keywords(blob):
                filtered.append(item)
        return filtered
