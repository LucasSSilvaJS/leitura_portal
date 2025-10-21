import logging
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, jsonify
from flask_cors import CORS
from api.news_controller import api
from core.db import init_db
from services.scheduler_service import SchedulerService
from services.news_service import NewsService
from clients.news_fetcher import RssNewsFetcher, HtmlListFetcher
from clients.recife_portal_fetcher import RecifePortalFetcher
from clients.gemini_client import GeminiClient
from clients.external_client import ExternalClient
from config.config import Config

# Configuração de logging
Config.setup_logging()
logger = logging.getLogger(__name__)

def create_app():
    # Valida configurações
    Config.validate_config()
    
    # Inicializa banco de dados
    init_db()
    
    # Cria aplicação Flask
    app = Flask(__name__)
    
    # Configura CORS para permitir acesso da documentação
    CORS(app)
    
    # Registra a API com Swagger
    api.init_app(app)

    # instantiate services for scheduler/manual trigger
    news_service = NewsService(
        repository=None,
        fetcher=RecifePortalFetcher(),  # Fetcher específico para o portal do Recife
        gemini=GeminiClient(),
        external=ExternalClient()
    )

    scheduler = SchedulerService()
    # schedule weekly Monday 9am
    scheduler.start_weekly_monday_9am(news_service.process_latest_first_item)

    # Rotas de compatibilidade (mantidas para não quebrar integrações existentes)
    @app.route("/healthz", methods=["GET"])
    def health():
        return jsonify({"status":"ok"})

    @app.route("/trigger", methods=["POST"])
    def manual_trigger():
        try:
            result = news_service.process_latest_first_item()
            return jsonify({"status":"ok", "result": result})
        except Exception as e:
            logger.exception("Manual trigger failed")
            return jsonify({"status":"error", "message": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host=Config.SERVER_HOST, port=Config.SERVER_PORT, debug=True)
