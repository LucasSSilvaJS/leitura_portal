#!/usr/bin/env python3
"""
Arquivo principal para executar a aplicação.
Este arquivo facilita a execução da aplicação reorganizada.
"""
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importa e executa a aplicação
from app.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
