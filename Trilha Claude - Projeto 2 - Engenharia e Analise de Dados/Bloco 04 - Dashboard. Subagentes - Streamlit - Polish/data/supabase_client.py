import os
from pathlib import Path
import pandas as pd
import requests
from dotenv import load_dotenv

# Carrega .env do diretório atual ou raiz do projeto
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://olusuiwrlolipchuhfyh.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

def get_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

def fetch_table(table_name: str, batch_size: int = 1000) -> pd.DataFrame:
    """Busca todos os dados de uma tabela no Supabase via PostgREST com paginação automática."""
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_KEY não configurada no .env")
    
    all_rows = []
    offset = 0
    
    while True:
        url = f"{SUPABASE_URL}/rest/v1/{table_name}?select=*&limit={batch_size}&offset={offset}"
        response = requests.get(url, headers=get_headers())
        
        if response.status_code != 200:
            raise RuntimeError(f"Erro ao buscar {table_name}: {response.status_code} - {response.text}")
        
        chunk = response.json()
        if not chunk:
            break
            
        all_rows.extend(chunk)
        if len(chunk) < batch_size:
            break
        offset += batch_size
        
    return pd.DataFrame(all_rows)

def load_clientes() -> pd.DataFrame:
    df = fetch_table("clientes")
    if not df.empty and "data_cadastro" in df.columns:
        df["data_cadastro"] = pd.to_datetime(df["data_cadastro"])
    return df

def load_produtos() -> pd.DataFrame:
    df = fetch_table("produtos")
    if not df.empty:
        if "preco_atual" in df.columns:
            df["preco_atual"] = pd.to_numeric(df["preco_atual"], errors="coerce")
        if "data_criacao" in df.columns:
            df["data_criacao"] = pd.to_datetime(df["data_criacao"])
    return df

def load_vendas() -> pd.DataFrame:
    df = fetch_table("vendas")
    if not df.empty:
        if "quantidade" in df.columns:
            df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce").fillna(0).astype(int)
        if "preco_unitario" in df.columns:
            df["preco_unitario"] = pd.to_numeric(df["preco_unitario"], errors="coerce").fillna(0.0)
        if "data_venda" in df.columns:
            df["data_venda"] = pd.to_datetime(df["data_venda"])
        df["valor_total"] = df["quantidade"] * df["preco_unitario"]
    return df

def load_preco_competidores() -> pd.DataFrame:
    df = fetch_table("preco_competidores")
    if not df.empty:
        if "preco_concorrente" in df.columns:
            df["preco_concorrente"] = pd.to_numeric(df["preco_concorrente"], errors="coerce")
        if "data_coleta" in df.columns:
            df["data_coleta"] = pd.to_datetime(df["data_coleta"])
    return df

def load_full_dataset() -> dict:
    """Carrega todas as 4 tabelas e gera a visão integrada de vendas enriquecida."""
    clientes = load_clientes()
    produtos = load_produtos()
    vendas = load_vendas()
    competidores = load_preco_competidores()
    
    # Enriquecimento de vendas com clientes e produtos
    vendas_enriquecidas = vendas.copy()
    if not clientes.empty and "id_cliente" in vendas_enriquecidas.columns:
        vendas_enriquecidas = vendas_enriquecidas.merge(
            clientes[["id_cliente", "nome_cliente", "estado", "pais"]],
            on="id_cliente",
            how="left"
        )
    if not produtos.empty and "id_produto" in vendas_enriquecidas.columns:
        vendas_enriquecidas = vendas_enriquecidas.merge(
            produtos[["id_produto", "nome_produto", "categoria", "marca", "preco_atual"]],
            on="id_produto",
            how="left"
        )
        vendas_enriquecidas["nome_produto"] = vendas_enriquecidas["nome_produto"].fillna("Produto Não Catalogado")
        vendas_enriquecidas["categoria"] = vendas_enriquecidas["categoria"].fillna("Outros")
    
    return {
        "clientes": clientes,
        "produtos": produtos,
        "vendas": vendas,
        "competidores": competidores,
        "vendas_enriquecidas": vendas_enriquecidas
    }
