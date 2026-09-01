import pandas as pd
import json

def load_data(data_dir):
    import os
    vendas = pd.read_csv(os.path.join(data_dir, 'vendas.csv'))
    clientes = pd.read_csv(os.path.join(data_dir, 'clientes.csv'))
    produtos = pd.read_csv(os.path.join(data_dir, 'produtos.csv'))
    return vendas, clientes, produtos

def compute_kpis(vendas, clientes, produtos):
    # Joins
    vendas_enrich = vendas.merge(clientes, on='id_cliente', how='left')
    vendas_enrich = vendas_enrich.merge(produtos, on='id_produto', how='left')
    vendas_enrich['valor_total'] = vendas_enrich['quantidade'] * vendas_enrich['preco_unitario']

    # Globals
    faturamento = vendas_enrich['valor_total'].sum()
    volume_vendas = vendas_enrich['id_venda'].nunique()
    ticket_medio = faturamento / volume_vendas if volume_vendas else 0
    clientes_ativos = vendas_enrich['id_cliente'].nunique()

    # Category Chart Data
    cat_group = vendas_enrich.groupby('categoria')['valor_total'].sum().sort_values(ascending=False)
    
    # Channel Chart Data
    channel_group = vendas_enrich.groupby('canal_venda')['valor_total'].sum()

    return {
        "kpis": {
            "faturamento_total": round(faturamento, 2),
            "ticket_medio": round(ticket_medio, 2),
            "vendas_totais": int(volume_vendas),
            "clientes_ativos": int(clientes_ativos)
        },
        "charts": {
            "categories": {
                "labels": cat_group.index.tolist(),
                "values": [round(v, 2) for v in cat_group.values.tolist()]
            },
            "channels": {
                "labels": channel_group.index.tolist(),
                "values": [round(v, 2) for v in channel_group.values.tolist()]
            }
        },
        "enriched_vendas": vendas_enrich
    }
