import csv
import re
from collections import Counter

filepath = r"d:\Lucas Formagio\Projects\Jornada de Dados - Projetos\Trilha Claude - Projeto 2 - Engenharia e Analise de Dados\Bloco 01 - Limpeza, diagnostico, prompt e validacao\f_Vendas.csv"

with open(filepath, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total de registros: {len(rows)}")
print(f"Colunas: {list(rows[0].keys())}")
print()

# 1. Valores ausentes
print("=" * 60)
print("1. VALORES AUSENTES / VAZIOS")
print("=" * 60)
for col in rows[0].keys():
    missing = [(i+2, r['ID Pedido']) for i, r in enumerate(rows) if not r[col].strip()]
    if missing:
        print(f"  Coluna '{col}': {len(missing)} ausente(s)")
        for line, pid in missing:
            print(f"    - Linha {line}, ID Pedido {pid}")
print()

# 2. Formatos de data inconsistentes
print("=" * 60)
print("2. FORMATOS DE DATA INCONSISTENTES")
print("=" * 60)
date_formats = {}
for i, r in enumerate(rows):
    d = r['Data do Pedido'].strip()
    if re.match(r'\d{2}/\d{2}/\d{4}', d):
        fmt = 'DD/MM/AAAA'
    elif re.match(r'\d{4}-\d{2}-\d{2}', d):
        fmt = 'AAAA-MM-DD'
    elif re.match(r'\d+ \w+\.? \d{4}', d):
        fmt = 'D mês AAAA (extenso)'
    else:
        fmt = f'DESCONHECIDO: {d}'
    date_formats.setdefault(fmt, []).append((i+2, r['ID Pedido'], d))

for fmt, entries in date_formats.items():
    print(f"  Formato '{fmt}': {len(entries)} registro(s)")
    for line, pid, val in entries:
        print(f"    - Linha {line}, ID {pid}: {val}")
print()

# 3. Casing inconsistente (nomes e status)
print("=" * 60)
print("3. CASING INCONSISTENTE")
print("=" * 60)
for col in ['Nome do Cliente', 'Região', 'Representante', 'Status']:
    cases = {}
    for i, r in enumerate(rows):
        val = r[col].strip()
        if not val:
            continue
        if val == val.upper():
            c = 'MAIÚSCULAS'
        elif val == val.lower():
            c = 'minúsculas'
        elif val == val.title():
            c = 'Title Case'
        else:
            c = f'Misto ({val})'
        cases.setdefault(c, []).append((i+2, r['ID Pedido'], val))
    if len(cases) > 1:
        print(f"  Coluna '{col}' — {len(cases)} padrões diferentes:")
        for c, entries in cases.items():
            print(f"    {c}: {len(entries)} registro(s)")
            for line, pid, val in entries[:5]:
                print(f"      - Linha {line}, ID {pid}: '{val}'")
            if len(entries) > 5:
                print(f"      ... e mais {len(entries)-5}")
print()

# 4. Status em inglês
print("=" * 60)
print("4. STATUS EM IDIOMA DIFERENTE (INGLÊS)")
print("=" * 60)
for i, r in enumerate(rows):
    s = r['Status'].strip().lower()
    if 'closed' in s or 'won' in s or 'lost' in s:
        print(f"  Linha {i+2}, ID {r['ID Pedido']}: '{r['Status'].strip()}' (esperado em português)")
print()

# 5. Duplicados
print("=" * 60)
print("5. POSSÍVEIS DUPLICADOS")
print("=" * 60)
# Exatos
seen = {}
for i, r in enumerate(rows):
    key = (r['Nome do Cliente'].strip().lower(), r['Data do Pedido'].strip(), r['Receita'].strip(), r['Produto'].strip())
    seen.setdefault(key, []).append((i+2, r['ID Pedido']))
for key, entries in seen.items():
    if len(entries) > 1:
        print(f"  Duplicado EXATO (nome+data+receita+produto):")
        print(f"    Cliente: {key[0]}, Data: {key[1]}, Receita: {key[2]}, Produto: {key[3]}")
        for line, pid in entries:
            print(f"    - Linha {line}, ID {pid}")

# Por nome normalizado + receita + produto (datas diferentes)
seen2 = {}
for i, r in enumerate(rows):
    key = (r['Nome do Cliente'].strip().lower(), r['Receita'].strip(), r['Produto'].strip())
    seen2.setdefault(key, []).append((i+2, r['ID Pedido'], r['Data do Pedido'].strip()))
print()
print("  Possíveis duplicados (mesmo nome+receita+produto, datas diferentes):")
for key, entries in seen2.items():
    if len(entries) > 1:
        dates = set(e[2] for e in entries)
        if len(dates) > 1:
            print(f"    Cliente: {key[0]}, Receita: {key[1]}, Produto: {key[2]}")
            for line, pid, dt in entries:
                print(f"      - Linha {line}, ID {pid}, Data: {dt}")
print()

# 6. Receita - formato
print("=" * 60)
print("6. FORMATO DE RECEITA")
print("=" * 60)
for i, r in enumerate(rows):
    rec = r['Receita'].strip()
    if rec and 'R$' in rec:
        valor = rec.replace('R$', '').strip()
        if ',' not in valor and '.' in valor:
            print(f"  Linha {i+2}, ID {r['ID Pedido']}: '{rec}' — usa ponto como decimal (padrão BR usa vírgula)")
print()

# 7. Região inconsistente
print("=" * 60)
print("7. REGIÃO - VARIAÇÕES DE CASING")
print("=" * 60)
regioes = {}
for i, r in enumerate(rows):
    reg = r['Região'].strip()
    if reg:
        regioes.setdefault(reg.lower(), set()).add(reg)
for norm, variants in regioes.items():
    if len(variants) > 1:
        print(f"  '{norm}' aparece como: {variants}")
print()

# 8. Observações que sinalizam problemas
print("=" * 60)
print("8. OBSERVAÇÕES QUE SINALIZAM PROBLEMAS")
print("=" * 60)
for i, r in enumerate(rows):
    obs = r['Observações'].strip()
    if obs:
        print(f"  Linha {i+2}, ID {r['ID Pedido']}: '{obs}'")
