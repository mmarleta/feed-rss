from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class NewsItem(BaseModel):
    source: str
    id: str
    title: str
    link: str
    summary: str
    published: Optional[datetime] = None

class ProcessedItem(BaseModel):
    news: NewsItem
    script: Optional[str] = None
    error: Optional[str] = None
