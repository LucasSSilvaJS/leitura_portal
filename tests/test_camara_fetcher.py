"""
Teste do fetcher atualizado para o portal da Câmara Municipal do Recife.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.clients.recife_portal_fetcher import RecifePortalFetcher
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_camara_fetcher():
    """Testa o fetcher com o portal da Câmara Municipal do Recife."""
    print("Testando fetcher da Câmara Municipal do Recife...")
    
    try:
        fetcher = RecifePortalFetcher()
        items = fetcher.fetch_latest_list()
        
        print(f"\nEncontradas {len(items)} notícias:")
        print("-" * 80)
        
        for i, (title, url, author) in enumerate(items[:5], 1):
            print(f"{i}. Título: {title}")
            print(f"   URL: {url}")
            print(f"   Autor: {author}")
            print("-" * 80)
        
        if items:
            print(f"\n[SUCESSO] Fetcher funcionando! Primeira notícia:")
            print(f"Título: {items[0][0]}")
            print(f"URL: {items[0][1]}")
            print(f"Autor: {items[0][2]}")
            return True
        else:
            print("\n[AVISO] Nenhuma notícia encontrada")
            return False
            
    except Exception as e:
        print(f"\n[ERRO] Falha no teste: {e}")
        return False

if __name__ == "__main__":
    print("Iniciando teste do fetcher da Câmara Municipal do Recife...\n")
    success = test_camara_fetcher()
    
    if success:
        print("\n[SUCESSO] Teste concluído com sucesso!")
    else:
        print("\n[FALHA] Teste falhou!")
