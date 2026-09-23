"""
Interface Web & Dashboard Analítico (Presentation Layer)
Orquestrador visual construído sobre a biblioteca Streamlit.
"""
import streamlit as st
import plotly.express as px
import db_postgres as db
import api_financeiro as fin
import app_produtos as prod

st.set_page_config(
    page_title="VentureEngine ERP",
    page_icon="🚜",
    layout="wide"
)

# Inicialização da infraestrutura de dados
db.inicializar_banco()

st.title("🚜 VentureEngine ERP — Gestão & Inteligência Operacional")
st.caption("Engenharia de Software Aplicada | Arquitetura Modular em Python")

aba_dashboard, aba_estoque, aba_financeiro = st.tabs([
    "📊 Visão Geral & KPIs", 
    "📦 Gestão de Estoque", 
    "💰 Fluxo de Caixa"
])

# -------------------------------------------------------------
# ABA 1: DASHBOARD
# -------------------------------------------------------------
with aba_dashboard:
    st.subheader("Indicadores Chave (KPIs)")
    df_fin = db.buscar_financeiro()
    resumo = fin.calcular_resumo_financeiro(df_fin)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Receita Total", f"R$ {resumo['receita']:,.2f}")
    col2.metric("Despesas Totais", f"R$ {resumo['despesa']:,.2f}")
    col3.metric("Saldo Líquido", f"R$ {resumo['saldo']:,.2f}")
    
    st.divider()
    
    df_prod = db.buscar_produtos()
    if not df_prod.empty:
        fig = px.bar(
            df_prod, 
            x='nome', 
            y='estoque', 
            color='categoria',
            title="Distribuição de Insumos em Estoque",
            labels={'nome': 'Produto', 'estoque': 'Quantidade Disponível'}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum item cadastrado no estoque para exibição gráfica.")

# -------------------------------------------------------------
# ABA 2: ESTOQUE
# -------------------------------------------------------------
with aba_estoque:
    st.subheader("Novo Item de Estoque")
    with st.form("form_produto"):
        nome = st.text_input("Nome do Item / Insumo")
        categoria = st.selectbox("Categoria", ["Sementes", "Fertilizantes", "Defensivos", "Maquinário", "Tecnologia"])
        preco = st.number_input("Preço Unitário (R$)", min_value=0.0, format="%.2f")
        estoque = st.number_input("Quantidade em Estoque", min_value=1, step=1)
        
        btn_salvar = st.form_submit_button("Cadastrar no Sistema")
        
        if btn_salvar:
            try:
                prod.cadastrar_novo_produto(nome, categoria, preco, estoque)
                st.success(f"Item '{nome}' cadastrado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
                
    st.divider()
    st.subheader("Inventário Atual")
    st.dataframe(db.buscar_produtos(), use_container_width=True)

# -------------------------------------------------------------
# ABA 3: FINANCEIRO
# -------------------------------------------------------------
with aba_financeiro:
    st.subheader("Lançamento de Caixa")
    with st.form("form_financeiro"):
        descricao = st.text_input("Descrição do Lançamento")
        tipo = st.radio("Tipo de Operação", ["Receita", "Despesa"], horizontal=True)
        valor = st.number_input("Valor Operacional (R$)", min_value=0.01, format="%.2f")
        
        btn_financeiro = st.form_submit_button("Registrar Transação")
        
        if btn_financeiro:
            try:
                fin.registrar_transacao(descricao, tipo, valor)
                st.success("Operação lançada com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao registrar: {e}")
                
    st.divider()
    st.subheader("Extrato do Caixa")
    st.dataframe(db.buscar_financeiro(), use_container_width=True)