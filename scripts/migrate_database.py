"""
Script de migração para adicionar a coluna 'author' à tabela news_items.
Execute este script uma vez para atualizar o banco de dados existente.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import sqlite3
from src.config.config import Config

def migrate_database():
    """
    Adiciona a coluna 'author' à tabela news_items se ela não existir.
    """
    # Determina o caminho do banco de dados
    db_path = Config.DATABASE_URL
    if db_path and db_path.startswith("sqlite:///"):
        db_path = db_path.replace("sqlite:///", "")
    else:
        # Fallback para um banco SQLite local
        db_path = "news_portal.db"
    
    print(f"Conectando ao banco de dados: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verifica se a coluna 'author' já existe
        cursor.execute("PRAGMA table_info(news_items)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'author' not in columns:
            print("Adicionando coluna 'author' à tabela news_items...")
            cursor.execute("ALTER TABLE news_items ADD COLUMN author VARCHAR(256)")
            conn.commit()
            print("Coluna 'author' adicionada com sucesso!")
        else:
            print("Coluna 'author' já existe na tabela.")
        
        # Verifica a estrutura atual da tabela
        cursor.execute("PRAGMA table_info(news_items)")
        columns_info = cursor.fetchall()
        print("\nEstrutura atual da tabela news_items:")
        for col in columns_info:
            print(f"  {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        conn.close()
        print("\nMigração concluída com sucesso!")
        
    except sqlite3.Error as e:
        print(f"Erro ao executar migração: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False
    
    return True

if __name__ == "__main__":
    migrate_database()
