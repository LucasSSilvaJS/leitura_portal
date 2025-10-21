import os
import logging
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """
    Configurações da aplicação Portal de Notícias do Recife.
    Todas as configurações são carregadas de variáveis de ambiente.
    """
    
    # =============================================================================
    # CONFIGURAÇÕES DO BANCO DE DADOS
    # =============================================================================
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./news.db")
    
    # =============================================================================
    # CONFIGURAÇÕES DO PORTAL DE NOTÍCIAS
    # =============================================================================
    NEWS_PORTAL_URL = os.getenv("NEWS_PORTAL_URL", "https://www.recife.pe.leg.br/comunicacao/noticias")
    
    # =============================================================================
    # CONFIGURAÇÕES DE APIs EXTERNAS
    # =============================================================================
    EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL")
    
    # =============================================================================
    # CONFIGURAÇÕES DE IA (GEMINI)
    # =============================================================================
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # =============================================================================
    # CONFIGURAÇÕES DO AGENDADOR
    # =============================================================================
    SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "America/Sao_Paulo")
    
    # =============================================================================
    # CONFIGURAÇÕES DE DESENVOLVIMENTO
    # =============================================================================
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    
    @classmethod
    def validate_config(cls):
        """
        Valida se as configurações essenciais estão definidas.
        """
        required_configs = [
            ("NEWS_PORTAL_URL", cls.NEWS_PORTAL_URL),
        ]
        
        missing_configs = []
        for name, value in required_configs:
            if not value:
                missing_configs.append(name)
        
        if missing_configs:
            raise ValueError(f"Configurações obrigatórias não definidas: {', '.join(missing_configs)}")
        
        return True
    
    @classmethod
    def setup_logging(cls):
        """
        Configura o sistema de logging baseado nas configurações.
        """
        log_level = getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO)
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
