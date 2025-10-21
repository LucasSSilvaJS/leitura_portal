"""
Script de teste para o RecifePortalFetcher.
Testa a extração de notícias do portal do Recife.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.clients.recife_portal_fetcher import RecifePortalFetcher
import logging

# Configura logging para debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_fetcher():
    """
    Testa o fetcher do portal do Recife.
    """
    print("=== Teste do RecifePortalFetcher ===\n")
    
    # URL de exemplo - substitua pela URL real do portal
    test_url = "https://www.recife.pe.gov.br/noticias"  # Exemplo
    
    try:
        fetcher = RecifePortalFetcher(portal_url=test_url)
        print(f"Testando extração de notícias de: {test_url}")
        print("-" * 50)
        
        # Busca as notícias
        items = fetcher.fetch_latest_list()
        
        if not items:
            print("[ERRO] Nenhuma notícia encontrada!")
            return False
        
        print(f"[OK] Encontradas {len(items)} notícias:\n")
        
        # Exibe as primeiras 5 notícias
        for i, (title, url, author) in enumerate(items[:5], 1):
            print(f"{i}. Título: {title}")
            print(f"   Autor: {author}")
            print(f"   URL: {url}")
            print()
        
        # Testa busca de detalhes da primeira notícia
        if items and items[0][1]:  # Se tem URL
            print("Testando busca de detalhes da primeira notícia...")
            details = fetcher.fetch_news_details(items[0][1])
            if details:
                print("Detalhes encontrados:")
                for key, value in details.items():
                    print(f"  {key}: {value}")
            else:
                print("Nenhum detalhe adicional encontrado.")
        
        print("\n[OK] Teste concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro durante o teste: {e}")
        logger.exception("Erro detalhado:")
        return False

def test_with_sample_html():
    """
    Testa o fetcher com HTML de exemplo (simulado).
    """
    print("\n=== Teste com HTML de Exemplo ===\n")
    
    # HTML de exemplo baseado no fornecido pelo usuário
    sample_html = """
    <div class="row row-news-small">
        <div class="col-sm-6 col-md-6">
            <div class="box-last-news">
                <h5><a href="/noticias/20/10/2025/procon-recife-promove-semana-das-criancas-com-oficinas-sobre-consumo-consciente">Procon Recife</a></h5>
                <h3><a href="/noticias/20/10/2025/procon-recife-promove-semana-das-criancas-com-oficinas-sobre-consumo-consciente">Procon Recife promove Semana das Crianças com oficinas sobre consumo consciente na Rede Compaz</a></h3>
            </div>
        </div>
        <div class="col-sm-6 col-md-6">
            <div class="box-last-news">
                <h5><a href="/noticias/20/10/2025/arena-go-recife-promove-dois-dias-de-oportunidades-com-foco-em-emprego">Secretaria de Trabalho e Qualificação Profissional</a></h5>
                <h3><a href="/noticias/20/10/2025/arena-go-recife-promove-dois-dias-de-oportunidades-com-foco-em-emprego">Arena GO Recife promove dois dias de oportunidades com foco em emprego, empreendedorismo e bem-estar</a></h3>
            </div>
        </div>
    </div>
    """
    
    try:
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(sample_html, "html.parser")
        items = []
        
        news_boxes = soup.select(".box-last-news")
        
        for box in news_boxes:
            # Extrai o autor/secretaria do h5
            author_tag = box.find("h5")
            author = ""
            if author_tag and author_tag.find("a"):
                author = author_tag.find("a").get_text(strip=True)
            
            # Extrai o título e URL do h3
            title_tag = box.find("h3")
            title = ""
            url = ""
            
            if title_tag and title_tag.find("a"):
                link = title_tag.find("a")
                title = link.get_text(strip=True)
                url = link.get("href", "")
            
            if title and title.strip():
                items.append((title.strip(), url, author.strip()))
        
        print(f"[OK] Extraídas {len(items)} notícias do HTML de exemplo:")
        for i, (title, url, author) in enumerate(items, 1):
            print(f"{i}. Título: {title}")
            print(f"   Autor: {author}")
            print(f"   URL: {url}")
            print()
        
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro ao processar HTML de exemplo: {e}")
        return False

if __name__ == "__main__":
    print("Iniciando testes do RecifePortalFetcher...\n")
    
    # Teste com HTML de exemplo primeiro
    success1 = test_with_sample_html()
    
    # Teste com URL real (comentado para evitar erros de conexão)
    # success2 = test_fetcher()
    
    if success1:
        print("\n[SUCESSO] Todos os testes passaram!")
    else:
        print("\n[FALHA] Alguns testes falharam!")
