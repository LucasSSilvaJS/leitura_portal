"""
NewsFetcher: interface + a simple RSS/HTML implementation.
You can swap this for custom portal code.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from abc import ABC, abstractmethod
from typing import Optional, Tuple
import requests
from bs4 import BeautifulSoup
from config.config import Config

class NewsFetcher(ABC):
    @abstractmethod
    def fetch_latest_list(self) -> list:
        """Return a list of (title, url) tuples of latest items, newest first."""
        pass

class RssNewsFetcher(NewsFetcher):
    def __init__(self, portal_url: str = None):
        self.portal_url = portal_url or Config.NEWS_PORTAL_URL

    def fetch_latest_list(self) -> list:
        resp = requests.get(self.portal_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "xml")
        items = []
        for item in soup.find_all("item")[:20]:
            title_tag = item.find("title")
            link_tag = item.find("link")
            title = title_tag.text.strip() if title_tag else ""
            link = link_tag.text.strip() if link_tag else None
            items.append((title, link))
        return items

class HtmlListFetcher(NewsFetcher):
    def __init__(self, portal_url: str = None, list_selector: str = ".article"):
        self.portal_url = portal_url or Config.NEWS_PORTAL_URL
        self.list_selector = list_selector

    def fetch_latest_list(self) -> list:
        resp = requests.get(self.portal_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        elements = soup.select(self.list_selector)[:20]
        for el in elements:
            title = el.get_text(strip=True)[:512]
            link = None
            a = el.find("a")
            if a and a.get("href"):
                link = a.get("href")
            items.append((title, link))
        return items
