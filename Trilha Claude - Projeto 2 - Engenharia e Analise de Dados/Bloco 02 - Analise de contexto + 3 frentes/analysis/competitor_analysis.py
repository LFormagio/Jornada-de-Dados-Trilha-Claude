import pandas as pd
import os

def analyze_competitors(data_dir, produtos_df, top_n=5):
    preco_comp = pd.read_csv(os.path.join(data_dir, 'preco_competidores.csv'))
    
    # Calculate average competitor price per product
    # preco_concorrente is string like "65,45", need to convert to float
    preco_comp['preco_concorrente'] = preco_comp['preco_concorrente'].astype(str).str.replace(',', '.').astype(float)
    avg_comp_price = preco_comp.groupby('id_produto')['preco_concorrente'].mean().reset_index()
    avg_comp_price.rename(columns={'preco_concorrente': 'media_mercado'}, inplace=True)
    
    # Merge with our products
    merged = produtos_df.merge(avg_comp_price, on='id_produto', how='inner')
    merged['diff_percent'] = ((merged['media_mercado'] - merged['preco_atual']) / merged['media_mercado']) * 100
    
    # We select the top_n most interesting products (e.g. highest potential or just head of list for demo)
    results = merged.head(top_n).copy()
    
    rows = []
    for _, row in results.iterrows():
        nosso_preco = row['preco_atual']
        mercado = row['media_mercado']
        diff = row['diff_percent']
        
        if nosso_preco < mercado:
            status = 'Vantagem'
            badge_class = 'win'
        else:
            status = 'Atenção'
            badge_class = 'lose'
            
        rows.append({
            "nome": row['nome_produto'],
            "nosso_preco": round(nosso_preco, 2),
            "media_mercado": round(mercado, 2),
            "status": status,
            "badge_class": badge_class,
            "margem_dif": round(diff, 2)
        })
    return rows
