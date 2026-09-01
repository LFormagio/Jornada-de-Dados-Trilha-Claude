import sys
import os
import pandas as pd
import pytest

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis.engine import compute_kpis

def test_compute_kpis():
    # Mock data
    vendas = pd.DataFrame({
        'id_venda': [1, 2],
        'id_cliente': [101, 102],
        'id_produto': [201, 202],
        'quantidade': [2, 1],
        'preco_unitario': [50.0, 100.0],
        'canal_venda': ['loja', 'online']
    })
    clientes = pd.DataFrame({'id_cliente': [101, 102], 'categoria': ['A', 'B']})
    produtos = pd.DataFrame({'id_produto': [201, 202], 'categoria': ['Eletronicos', 'Casa']})
    
    result = compute_kpis(vendas, clientes, produtos)
    
    assert result['kpis']['faturamento_total'] == 200.0
    assert result['kpis']['vendas_totais'] == 2
    assert result['kpis']['ticket_medio'] == 100.0
    assert result['kpis']['clientes_ativos'] == 2
    
    assert 'Eletronicos' in result['charts']['categories']['labels']
