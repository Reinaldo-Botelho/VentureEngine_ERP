"""
Módulo de Regras de Negócio Financeiro (Business Logic Layer)
Responsável por cálculos analíticos, balanço financeiro e lançamentos de caixa.
"""
from db_postgres import conectar

def registrar_transacao(descricao: str, tipo: str, valor: float) -> None:
    """Valida e grava um lançamento financeiro no banco de dados."""
    if valor <= 0:
        raise ValueError("O valor da transação deve ser positivo.")
        
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO financeiro (descricao, tipo, valor) VALUES (?, ?, ?)",
        (descricao, tipo, valor)
    )
    conn.commit()
    conn.close()

def calcular_resumo_financeiro(df_financeiro) -> dict:
    """
    Processa o DataFrame de transações e retorna os KPIs consolidados:
    - Receita Total
    - Despesas Totais
    - Saldo Líquido
    """
    if df_financeiro.empty:
        return {"receita": 0.0, "despesa": 0.0, "saldo": 0.0}    
        
    receita = df_financeiro[df_financeiro['tipo'] == 'Receita']['valor'].sum()
    despesa = df_financeiro[df_financeiro['tipo'] == 'Despesa']['valor'].sum()
    saldo = receita - despesa
    
    return {
        "receita": float(receita),
        "despesa": float(despesa),
        "saldo": float(saldo)
    }