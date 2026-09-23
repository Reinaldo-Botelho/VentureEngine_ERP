"""
Módulo de Gestão de Estoque (Domain Services Layer)
Responsável pela manutenção do catálogo de produtos e insumos.
"""
from db_postgres import conectar

def cadastrar_novo_produto(nome: str, categoria: str, preco: float, estoque: int) -> None:
    """Valida as entradas operacionais e insere um novo item de estoque."""
    if not nome.strip():
        raise ValueError("O nome do produto não pode ser vazio.")
    if preco < 0 or estoque < 0:
        raise ValueError("Preço e estoque não podem ser negativos.")
        
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, categoria, preco, estoque) VALUES (?, ?, ?, ?)",
        (nome, categoria, preco, estoque)
    )
    conn.commit()
    conn.close()