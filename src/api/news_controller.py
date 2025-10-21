import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask_restx import Api, Resource, fields, Namespace
from flask import request
from core.news_repository import NewsRepository
from services.news_service import NewsService
from models.schemas import NewsItemCreate, NewsItemUpdate
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

# Configuração da API com Swagger
api = Api(
    title='Portal de Notícias do Recife API',
    version='1.0',
    description='API para processamento automatizado de notícias do portal oficial do Recife',
    doc='/docs/',  # URL da documentação Swagger
    prefix='/api'
)

# Namespace para notícias
news_ns = Namespace('news', description='Operações relacionadas a notícias')
api.add_namespace(news_ns)

# Modelos para documentação Swagger
news_model = api.model('NewsItem', {
    'id': fields.Integer(required=True, description='ID único da notícia'),
    'source_title': fields.String(required=True, description='Título original da notícia'),
    'question_title': fields.String(description='Título reformulado como pergunta'),
    'source_url': fields.String(description='URL da notícia original'),
    'author': fields.String(description='Autor/Secretaria responsável'),
    'fetched_at': fields.DateTime(description='Data de extração'),
    'external_response': fields.String(description='Resposta da API externa')
})

news_create_model = api.model('NewsItemCreate', {
    'source_title': fields.String(required=True, description='Título da notícia'),
    'source_url': fields.String(description='URL da notícia'),
    'author': fields.String(description='Autor/Secretaria')
})

news_update_model = api.model('NewsItemUpdate', {
    'question_title': fields.String(description='Título reformulado'),
    'external_response': fields.String(description='Resposta da API externa'),
    'author': fields.String(description='Autor/Secretaria')
})

error_model = api.model('Error', {
    'error': fields.String(required=True, description='Tipo do erro'),
    'message': fields.String(description='Mensagem de erro'),
    'details': fields.Raw(description='Detalhes adicionais do erro')
})

success_model = api.model('Success', {
    'status': fields.String(required=True, description='Status da operação'),
    'message': fields.String(description='Mensagem de sucesso')
})

# Inicialização dos serviços
repo = NewsRepository()
service = NewsService(repository=repo)

@news_ns.route('/')
class NewsList(Resource):
    @news_ns.doc('list_news')
    @news_ns.marshal_list_with(news_model)
    def get(self):
        """
        Lista todas as notícias
        
        Retorna uma lista com todas as notícias processadas pelo sistema.
        """
        items = repo.list()
        result = [ {
            "id": it.id,
            "source_title": it.source_title,
            "question_title": it.question_title,
            "source_url": it.source_url,
            "author": it.author,
            "fetched_at": it.fetched_at.isoformat() if it.fetched_at else None,
            "external_response": it.external_response
        } for it in items]
        return result

    @news_ns.doc('create_news')
    @news_ns.expect(news_create_model)
    @news_ns.marshal_with(success_model)
    def post(self):
        """
        Cria uma nova notícia
        
        Cria uma nova entrada de notícia no sistema.
        """
        try:
            payload = NewsItemCreate(**request.json)
        except ValidationError as e:
            return {"error": "validation", "message": "Dados inválidos", "details": e.errors()}, 400
        
        it = repo.create(source_title=payload.source_title, source_url=payload.source_url, author=payload.author)
        return {"status": "created", "message": f"Notícia criada com ID {it.id}"}, 201

@news_ns.route('/<int:item_id>')
@news_ns.param('item_id', 'ID da notícia')
class NewsItem(Resource):
    @news_ns.doc('get_news')
    @news_ns.marshal_with(news_model)
    def get(self, item_id):
        """
        Busca uma notícia por ID
        
        Retorna os detalhes de uma notícia específica.
        """
        it = repo.get(item_id)
        if not it:
            return {"error": "not found", "message": "Notícia não encontrada"}, 404
        
        return {
            "id": it.id,
            "source_title": it.source_title,
            "question_title": it.question_title,
            "source_url": it.source_url,
            "author": it.author,
            "fetched_at": it.fetched_at.isoformat() if it.fetched_at else None,
            "external_response": it.external_response
        }

    @news_ns.doc('update_news')
    @news_ns.expect(news_update_model)
    @news_ns.marshal_with(success_model)
    def put(self, item_id):
        """
        Atualiza uma notícia
        
        Atualiza os dados de uma notícia existente.
        """
        it = repo.get(item_id)
        if not it:
            return {"error": "not found", "message": "Notícia não encontrada"}, 404
        
        try:
            payload = NewsItemUpdate(**request.json)
        except ValidationError as e:
            return {"error": "validation", "message": "Dados inválidos", "details": e.errors()}, 400
        
        updated = repo.update(it, question_title=payload.question_title, external_response=payload.external_response, author=payload.author)
        return {"status": "updated", "message": f"Notícia {updated.id} atualizada com sucesso"}

    @news_ns.doc('delete_news')
    @news_ns.marshal_with(success_model)
    def delete(self, item_id):
        """
        Remove uma notícia
        
        Remove uma notícia do sistema.
        """
        it = repo.get(item_id)
        if not it:
            return {"error": "not found", "message": "Notícia não encontrada"}, 404
        
        repo.delete(it)
        return {"status": "deleted", "message": f"Notícia {item_id} removida com sucesso"}

# Namespace para operações do sistema
system_ns = Namespace('system', description='Operações do sistema')
api.add_namespace(system_ns)

@system_ns.route('/health')
class HealthCheck(Resource):
    @system_ns.doc('health_check')
    @system_ns.marshal_with(success_model)
    def get(self):
        """
        Verifica o status da aplicação
        
        Retorna o status de saúde da aplicação.
        """
        return {"status": "ok", "message": "Aplicação funcionando normalmente"}

@system_ns.route('/trigger')
class ManualTrigger(Resource):
    @system_ns.doc('manual_trigger')
    @system_ns.marshal_with(success_model)
    def post(self):
        """
        Executa processamento manual
        
        Executa manualmente o processamento da primeira notícia mais recente.
        """
        try:
            result = service.process_latest_first_item()
            return {
                "status": "ok", 
                "message": "Processamento executado com sucesso",
                "result": result
            }
        except Exception as e:
            logger.exception("Manual trigger failed")
            return {"error": "processing_failed", "message": str(e)}, 500
