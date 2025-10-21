from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime

class NewsItemCreate(BaseModel):
    source_title: str = Field(..., max_length=512)
    source_url: Optional[HttpUrl] = None
    author: Optional[str] = Field(None, max_length=256)

class NewsItemUpdate(BaseModel):
    question_title: Optional[str]
    external_response: Optional[str]
    author: Optional[str] = Field(None, max_length=256)

class NewsItemRead(BaseModel):
    id: int
    source_title: str
    question_title: Optional[str]
    source_url: Optional[str]
    author: Optional[str]
    fetched_at: datetime
    external_response: Optional[str]

    class Config:
        orm_mode = True
