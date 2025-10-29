import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.news_repository import NewsRepository
from clients.news_fetcher import RssNewsFetcher, HtmlListFetcher
from clients.recife_portal_fetcher import RecifePortalFetcher
from clients.gemini_client import GeminiClient
from clients.external_client import ExternalClient
from typing import Optional, Tuple
from utils.utils import safe_truncate
import logging

logger = logging.getLogger(__name__)

class NewsService:
    def __init__(
        self,
        repository: Optional[NewsRepository] = None,
        fetcher: Optional[RecifePortalFetcher] = None,
        gemini: Optional[GeminiClient] = None,
        external: Optional[ExternalClient] = None
    ):
        self.repo = repository or NewsRepository()
        self.fetcher = fetcher or RecifePortalFetcher()
        self.gemini = gemini or GeminiClient()
        self.external = external or ExternalClient()

    def process_latest_first_item(self) -> dict:
        """
        1. Fetch list of latest items
        2. Read first item
        3. Store source item
        4. Ask Gemini to reformulate to question <=96 chars
        5. Send to external API and save response
        Returns dict with operation result.
        """
        items = self.fetcher.fetch_latest_list()
        if not items:
            raise RuntimeError("Nenhum item encontrado no portal de notícias")

        title, url, author = items[0]
        logger.info("Found latest item: %s (Autor: %s)", title, author)

        # Save source
        news = self.repo.create(source_title=title, source_url=url, author=author)

        try:
            question = self.gemini.reformulate_to_question(title, max_chars=96)
        except Exception as e:
            logger.exception("Erro ao chamar Gemini: %s", e)
            question = safe_truncate(title, 96)
            # ensure it's a question
            if not question.endswith("?"):
                question = question.rstrip(".!;:,") + "?"
        # update item
        news = self.repo.update(news, question_title=question)

        # send to external API
        payload = {
            "texto": news.question_title,  # Campo que a API externa espera
            "id": news.id,
            "source_title": news.source_title,
            "question_title": news.question_title,
            "source_url": news.source_url,
            "author": news.author
        }
        try:
            external_resp = self.external.send_question(payload)
        except Exception as e:
            logger.exception("Erro ao enviar para API externa: %s", e)
            external_resp = {"error": str(e)}

        news = self.repo.update(news, external_response=str(external_resp))
        return {
            "news_id": news.id,
            "question_title": news.question_title,
            "external_response": external_resp
        }
