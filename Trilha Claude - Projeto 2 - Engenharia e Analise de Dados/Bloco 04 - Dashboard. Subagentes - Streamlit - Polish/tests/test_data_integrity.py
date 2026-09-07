import pytest
import pandas as pd
from data.supabase_client import (
    load_clientes,
    load_produtos,
    load_vendas,
    load_preco_competidores,
    load_full_dataset
)

def test_load_clientes():
    df = load_clientes()
    assert not df.empty, "A tabela clientes não deve estar vazia"
    assert len(df) == 50, f"Esperado 50 clientes, obtido {len(df)}"
    assert "id_cliente" in df.columns
    assert "nome_cliente" in df.columns
    assert "estado" in df.columns
    assert df["id_cliente"].is_unique, "Os IDs de clientes devem ser únicos"

def test_load_produtos():
    df = load_produtos()
    assert not df.empty, "A tabela produtos não deve estar vazia"
    assert len(df) == 215, f"Esperado 215 produtos, obtido {len(df)}"
    assert "id_produto" in df.columns
    assert "preco_atual" in df.columns
    assert pd.api.types.is_numeric_dtype(df["preco_atual"]), "O preço atual deve ser numérico"
    assert (df["preco_atual"] > 0).all(), "Todos os preços devem ser positivos"

def test_load_vendas():
    df = load_vendas()
    assert not df.empty, "A tabela vendas não deve estar vazia"
    assert len(df) == 3020, f"Esperado 3020 vendas, obtido {len(df)}"
    assert "id_venda" in df.columns
    assert "valor_total" in df.columns
    assert pd.api.types.is_numeric_dtype(df["valor_total"]), "O valor total deve ser numérico"
    assert (df["valor_total"] > 0).all(), "Todos os valores de venda devem ser positivos"

def test_load_preco_competidores():
    df = load_preco_competidores()
    assert not df.empty, "A tabela preco_competidores não deve estar vazia"
    assert len(df) == 728, f"Esperado 728 coletas de concorrentes, obtido {len(df)}"
    assert "preco_concorrente" in df.columns
    assert pd.api.types.is_numeric_dtype(df["preco_concorrente"]), "O preço concorrente deve ser numérico"
    assert "nome_concorrente" in df.columns
    assert set(df["nome_concorrente"].unique()).issubset({"Amazon", "Mercado Livre", "Shopee", "Magalu"})

def test_load_full_dataset_enrichment():
    data = load_full_dataset()
    vendas_enriquecidas = data["vendas_enriquecidas"]
    assert not vendas_enriquecidas.empty
    assert "nome_produto" in vendas_enriquecidas.columns
    assert "nome_cliente" in vendas_enriquecidas.columns
    assert len(vendas_enriquecidas) == 3020
