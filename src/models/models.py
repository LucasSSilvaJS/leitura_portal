import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import Column, Integer, String, DateTime, Text, func
from core.db import Base

class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    source_title = Column(String(512), nullable=False)
    question_title = Column(String(64), nullable=True)
    source_url = Column(String(1024), nullable=True)
    author = Column(String(256), nullable=True)  # Secretaria/Autor da notícia
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    external_response = Column(Text, nullable=True)
