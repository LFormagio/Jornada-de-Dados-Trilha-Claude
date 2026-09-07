import pytest
import pandas as pd
from data.supabase_client import load_full_dataset

@pytest.fixture(scope="module")
def data():
    return load_full_dataset()

def test_receita_total_calculation(data):
    vendas = data["vendas_enriquecidas"]
    receita_calculada = (vendas["quantidade"] * vendas["preco_unitario"]).sum()
    assert round(receita_calculada, 2) == 974077.28, f"Faturamento incorreto: {receita_calculada}"

def test_ticket_medio_positive(data):
    vendas = data["vendas_enriquecidas"]
    ticket = vendas["valor_total"].mean()
    assert 300.0 < ticket < 350.0, f"Ticket médio fora da faixa esperada: {ticket}"

def test_canais_proporcao(data):
    vendas = data["vendas_enriquecidas"]
    canal_sum = vendas.groupby("canal_venda")["valor_total"].sum()
    assert "ecommerce" in canal_sum.index
    assert "loja_fisica" in canal_sum.index
    assert canal_sum["ecommerce"] > canal_sum["loja_fisica"], "O E-commerce deve ser o maior canal de faturamento"

def test_indice_competitividade_preco(data):
    comp = data["competidores"]
    prod = data["produtos"]
    
    comp_merged = comp.merge(prod[["id_produto", "preco_atual"]], on="id_produto")
    comp_avg = comp_merged.groupby("id_produto").agg(
        preco_atual=("preco_atual", "first"),
        preco_medio_concorrencia=("preco_concorrente", "mean")
    ).reset_index()
    
    comp_avg["icp"] = comp_avg["preco_atual"] / comp_avg["preco_medio_concorrencia"]
    
    # Valida que o ICP médio está entre 0.9 e 1.2
    assert 0.9 < comp_avg["icp"].mean() < 1.2
    
    # Valida presença das 3 categorias de status
    sobrepreco = (comp_avg["icp"] > 1.05).sum()
    paridade = ((comp_avg["icp"] >= 0.95) & (comp_avg["icp"] <= 1.05)).sum()
    subpreco = (comp_avg["icp"] < 0.95).sum()
    
    assert sobrepreco > 0, "Deve haver produtos com sobrepreço identificado"
    assert paridade > 0, "Deve haver produtos com paridade de mercado"
    assert subpreco > 0, "Deve haver produtos com oportunidade de margem"
