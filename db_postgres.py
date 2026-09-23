import sqlite3
import pandas as pd

NOME_BANCO = "venture_engine.db"

def conectar():
    """Cria e retorna uma conexão ativa com o banco de dados."""
    return sqlite3.connect(NOME_BANCO)

def inicializar_banco():
    """Garante a criação das tabelas relacionais na inicialização do sistema."""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def buscar_produtos():
    """Executa a leitura da tabela de produtos e converte para DataFrame Pandas."""
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM produtos", conn)
    conn.close()
    return df

def buscar_financeiro():
    """Executa a leitura do histórico financeiro e converte para DataFrame Pandas."""
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM financeiro", conn)
    conn.close()
    return df