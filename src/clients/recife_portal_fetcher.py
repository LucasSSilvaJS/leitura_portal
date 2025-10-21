"""
Fetcher específico para o portal de notícias da Câmara Municipal do Recife.
Adaptado para trabalhar com a estrutura HTML específica do portal da Câmara.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from abc import ABC, abstractmethod
from typing import Optional, Tuple, List, Dict
import requests
from bs4 import BeautifulSoup
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class RecifePortalFetcher:
    """
    Fetcher específico para o portal de notícias da Câmara Municipal do Recife.
    Extrai notícias da estrutura HTML específica do portal da Câmara.
    """
    
    def __init__(self, portal_url: str = None):
        self.portal_url = portal_url or Config.NEWS_PORTAL_URL
        
    def fetch_latest_list(self) -> List[Tuple[str, str, str]]:
        """
        Retorna uma lista de tuplas (título, url, autor) das notícias mais recentes.
        Ordem: mais recente primeiro.
        """
        try:
            resp = requests.get(self.portal_url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            items = []
            
            # Busca por todas as notícias na estrutura específica da Câmara
            news_articles = soup.select("article.news-item")
            
            for article in news_articles[:20]:  # Limita a 20 notícias
                try:
                    # Extrai o título e URL do h4.title > a
                    title_tag = article.select_one("h4.title a")
                    title = ""
                    url = ""
                    
                    if title_tag:
                        title = title_tag.get_text(strip=True)
                        url = title_tag.get("href", "")
                        
                        # Converte URL relativa para absoluta se necessário
                        if url.startswith("/"):
                            url = self._make_absolute_url(url)
                    
                    # Para o portal da Câmara, não há autor específico nas notícias
                    # O autor seria "Câmara Municipal do Recife" por padrão
                    author = "Câmara Municipal do Recife"
                    
                    if title and title.strip():
                        items.append((title.strip(), url, author.strip()))
                        
                except Exception as e:
                    logger.warning(f"Erro ao processar notícia: {e}")
                    continue
            
            logger.info(f"Encontradas {len(items)} notícias no portal da Câmara")
            return items
            
        except requests.RequestException as e:
            logger.error(f"Erro ao buscar notícias: {e}")
            raise RuntimeError(f"Falha ao conectar com o portal: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao processar HTML: {e}")
            raise RuntimeError(f"Erro ao processar conteúdo do portal: {e}")
    
    def _make_absolute_url(self, relative_url: str) -> str:
        """
        Converte URL relativa para absoluta baseada na URL base do portal.
        """
        if not self.portal_url:
            return relative_url
            
        # Extrai o domínio base da URL do portal
        from urllib.parse import urljoin
        return urljoin(self.portal_url, relative_url)
    
    def fetch_news_details(self, url: str) -> Dict[str, str]:
        """
        Busca detalhes adicionais de uma notícia específica.
        Retorna um dicionário com informações extras se disponíveis.
        """
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            details = {}
            
            # Busca por data de publicação
            date_selectors = [
                ".news-date",
                ".publication-date", 
                ".date",
                "time",
                "[datetime]"
            ]
            
            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    details["date"] = date_elem.get_text(strip=True)
                    break
            
            # Busca por conteúdo/resumo
            content_selectors = [
                ".news-content",
                ".article-content",
                ".summary",
                ".excerpt"
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    details["content"] = content_elem.get_text(strip=True)[:500]  # Limita a 500 chars
                    break
            
            return details
            
        except Exception as e:
            logger.warning(f"Erro ao buscar detalhes da notícia {url}: {e}")
            return {}
