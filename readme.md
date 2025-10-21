# Portal de Notícias da Câmara Municipal do Recife - API

Sistema automatizado para extrair, processar e enviar notícias do portal oficial da Câmara Municipal do Recife.

## 🚀 Início Rápido

### 1. Instalação
```bash
pip install -r requirements.txt
```

### 2. Configuração
```bash
cp src/config/config_template.env .env
# Edite o arquivo .env com suas configurações
```

### 3. Execução
```bash
python main.py
```

## 📡 API Endpoints

### Documentação Swagger
- **URL**: `http://localhost:8000/docs/`
- **Descrição**: Documentação interativa da API

### Principais Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/news/` | Lista todas as notícias |
| `POST` | `/api/news/` | Cria nova notícia |
| `GET` | `/api/news/{id}` | Busca notícia por ID |
| `PUT` | `/api/news/{id}` | Atualiza notícia |
| `DELETE` | `/api/news/{id}` | Remove notícia |
| `GET` | `/api/system/health` | Status da aplicação |
| `POST` | `/api/system/trigger` | Processamento manual |

## ⚙️ Configurações Principais

```env
# Portal de notícias da Câmara Municipal
NEWS_PORTAL_URL=https://www.recife.pe.leg.br/comunicacao/noticias

# API Gemini (obrigatório)
GEMINI_API_KEY=sua_chave_aqui

# API externa (opcional)
EXTERNAL_API_URL=https://sua-api.com/receive
```

## 🔧 Scripts Úteis

```bash
# Migração do banco
python scripts/migrate_database.py

# Teste do sistema
python tests/test_fetcher.py
```

## 📊 Funcionamento

1. **Extração**: Busca notícias do portal da Câmara Municipal do Recife
2. **Processamento**: Reformula títulos com IA (Gemini)
3. **Envio**: Envia dados para API externa
4. **Agendamento**: Execução automática toda segunda-feira às 9h

## 🏗️ Estrutura

```
src/
├── app/          # Aplicação principal
├── api/          # Endpoints da API
├── clients/      # Clientes externos
├── config/       # Configurações
├── core/         # Banco e repositórios
├── models/       # Modelos de dados
├── services/     # Lógica de negócio
└── utils/        # Utilitários
```

## 📝 Exemplo de Uso

### Criar Notícia
```bash
curl -X POST http://localhost:8000/api/news/ \
  -H "Content-Type: application/json" \
  -d '{
    "source_title": "Título da notícia",
    "author": "Secretaria Municipal",
    "source_url": "https://exemplo.com/noticia"
  }'
```

### Processamento Manual
```bash
curl -X POST http://localhost:8000/api/system/trigger
```

## 🔍 Troubleshooting

- **Erro de conexão**: Verifique `NEWS_PORTAL_URL`
- **Erro de IA**: Configure `GEMINI_API_KEY`
- **Banco não existe**: Execute `python scripts/migrate_database.py`