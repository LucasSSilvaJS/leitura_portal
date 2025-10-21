import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.db import SessionLocal
from models.models import NewsItem
from typing import List, Optional

class NewsRepository:
    def __init__(self):
        self._session = SessionLocal()

    def create(self, source_title: str, source_url: Optional[str] = None, author: Optional[str] = None) -> NewsItem:
        item = NewsItem(source_title=source_title, source_url=source_url, author=author)
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def get(self, item_id: int) -> Optional[NewsItem]:
        return self._session.query(NewsItem).filter(NewsItem.id == item_id).first()

    def list(self, limit: int = 100) -> List[NewsItem]:
        return self._session.query(NewsItem).order_by(NewsItem.id.desc()).limit(limit).all()

    def update(self, item: NewsItem, **kwargs) -> NewsItem:
        for k, v in kwargs.items():
            if hasattr(item, k) and v is not None:
                setattr(item, k, v)
        self._session.commit()
        self._session.refresh(item)
        return item

    def delete(self, item: NewsItem):
        self._session.delete(item)
        self._session.commit()
