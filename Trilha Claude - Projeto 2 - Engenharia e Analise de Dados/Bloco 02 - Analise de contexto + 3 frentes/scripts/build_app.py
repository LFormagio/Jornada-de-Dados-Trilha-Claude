import os
import sys
import json
from datetime import datetime

# Adjust Python path to load local modules
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_DIR)

from analysis.engine import load_data, compute_kpis
from analysis.competitor_analysis import analyze_competitors

def build_dashboard():
    data_dir = os.path.join(PROJECT_DIR, 'data')
    output_dir = os.path.join(PROJECT_DIR, 'frontend', 'public')
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("[INIT] Carregando e processando dados...")
    vendas, clientes, produtos = load_data(data_dir)
    engine_data = compute_kpis(vendas, clientes, produtos)
    
    comp_rows = analyze_competitors(data_dir, produtos, top_n=5)
    
    print("[WORK] Gerando data payload para o React App...")
    
    # Structure full payload for React
    payload = {
        "generation_date": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "kpis": engine_data['kpis'],
        "charts": engine_data['charts'],
        "competitors": comp_rows
    }
        
    payload_path = os.path.join(output_dir, 'data_payload.json')
    with open(payload_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        
    print(f"[SUCESSO] Data payload construído com sucesso em: {payload_path}")

if __name__ == '__main__':
    build_dashboard()
