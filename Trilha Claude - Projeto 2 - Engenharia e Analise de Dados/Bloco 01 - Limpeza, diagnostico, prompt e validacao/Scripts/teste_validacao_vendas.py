"""
Script de Testes de Validação — f_Vendas_limpa.csv
===================================================
Valida que todas as correções do diagnóstico foram aplicadas corretamente.

Testes:
  1. Estrutura do arquivo (colunas, quantidade de registros)
  2. Duplicado confirmado removido (ID 1005)
  3. Formato de data unificado (DD/MM/AAAA)
  4. Casing padronizado (Title Case) em Nome, Região, Representante, Status
  5. Status traduzido (sem inglês)
  6. Status deslocado corrigido (ID 1007)
  7. Formato monetário brasileiro (R$ X.XXX,XX)
  8. Região padronizada (valores válidos)
  9. Valores ausentes conhecidos (não introduziu novos)
"""

import csv
import re
import os
import sys

# ─────────────────────────────────────────────
# Configuração
# ─────────────────────────────────────────────
DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_LIMPO = os.path.join(DIR, "f_Vendas_limpa.csv")

COLUNAS_ESPERADAS = [
    "ID Pedido", "Nome do Cliente", "Região", "Representante",
    "Data do Pedido", "Receita", "Produto", "Status", "Observações"
]

REGIOES_VALIDAS = {"Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"}
STATUS_VALIDOS = {"Fechado Ganho", "Fechado Perdido"}
PRODUTOS_VALIDOS = {"Licença de Software", "Consultoria", "Hardware", "Pacote Empresarial"}

# Campos que já sabemos que continuam vazios (validação manual pendente)
VAZIOS_CONHECIDOS = {
    ("1006", "Região"),
    ("1016", "Região"),
    ("1009", "Receita"),
    ("1021", "Receita"),
    ("1027", "Representante"),
}

# ─────────────────────────────────────────────
# Framework de testes
# ─────────────────────────────────────────────
total_testes = 0
testes_ok = 0
testes_falha = 0
falhas = []


def teste(nome, condicao, detalhe=""):
    """Executa um teste e registra o resultado."""
    global total_testes, testes_ok, testes_falha
    total_testes += 1
    if condicao:
        testes_ok += 1
        print(f"  [PASS] {nome}")
    else:
        testes_falha += 1
        msg = f"  [FAIL] {nome}"
        if detalhe:
            msg += f" --> {detalhe}"
        print(msg)
        falhas.append((nome, detalhe))


# ─────────────────────────────────────────────
# Carregar dados
# ─────────────────────────────────────────────
print("=" * 65)
print("  TESTES DE VALIDACAO - f_Vendas_limpa.csv")
print("=" * 65)
print()

if not os.path.exists(ARQUIVO_LIMPO):
    print(f"[ERRO] Arquivo nao encontrado: {ARQUIVO_LIMPO}")
    sys.exit(1)

with open(ARQUIVO_LIMPO, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    colunas = reader.fieldnames
    registros = list(reader)

ids_presentes = {r["ID Pedido"].strip() for r in registros}


# ─────────────────────────────────────────────
# BLOCO 1: Estrutura do arquivo
# ─────────────────────────────────────────────
print("[BLOCO 1] Estrutura do Arquivo")
print("-" * 45)

teste(
    "Colunas corretas",
    colunas == COLUNAS_ESPERADAS,
    f"Esperado {COLUNAS_ESPERADAS}, obtido {colunas}"
)

teste(
    "Quantidade de registros = 29 (30 originais - 1 duplicado)",
    len(registros) == 29,
    f"Encontrados {len(registros)} registros"
)

teste(
    "IDs unicos (sem duplicidade de ID)",
    len(ids_presentes) == len(registros),
    f"{len(registros)} registros mas {len(ids_presentes)} IDs unicos"
)
print()


# ─────────────────────────────────────────────
# BLOCO 2: Duplicado removido
# ─────────────────────────────────────────────
print("[BLOCO 2] Remocao de Duplicados")
print("-" * 45)

teste(
    "ID 1005 removido (duplicado confirmado de 1001)",
    "1005" not in ids_presentes,
    "ID 1005 ainda presente no arquivo"
)

teste(
    "ID 1001 mantido (registro original)",
    "1001" in ids_presentes,
    "ID 1001 nao encontrado"
)

# Verifica se nao ha duplicados exatos restantes
chaves_vistas = {}
tem_dup_exato = False
for r in registros:
    chave = (
        r["Nome do Cliente"].strip().lower(),
        r["Data do Pedido"].strip(),
        r["Receita"].strip(),
        r["Produto"].strip()
    )
    if chave in chaves_vistas and r["Receita"].strip():
        tem_dup_exato = True
    chaves_vistas[chave] = r["ID Pedido"]

teste(
    "Nenhum duplicado exato restante (nome+data+receita+produto)",
    not tem_dup_exato,
    "Ainda existem duplicados exatos"
)
print()


# ─────────────────────────────────────────────
# BLOCO 3: Formato de data
# ─────────────────────────────────────────────
print("[BLOCO 3] Formato de Data (DD/MM/AAAA)")
print("-" * 45)

padrao_data = re.compile(r"^\d{2}/\d{2}/\d{4}$")
datas_erradas = []

for r in registros:
    data = r["Data do Pedido"].strip()
    if data and not padrao_data.match(data):
        datas_erradas.append((r["ID Pedido"], data))

teste(
    "Todas as datas no formato DD/MM/AAAA",
    len(datas_erradas) == 0,
    f"Datas fora do padrao: {datas_erradas}"
)

# Verifica se nao ha formato ISO residual
iso_residual = [r["ID Pedido"] for r in registros
                if re.match(r"\d{4}-\d{2}-\d{2}", r["Data do Pedido"].strip())]
teste(
    "Nenhuma data em formato ISO (AAAA-MM-DD)",
    len(iso_residual) == 0,
    f"IDs com formato ISO: {iso_residual}"
)

# Verifica se nao ha formato extenso residual
extenso_residual = [r["ID Pedido"] for r in registros
                    if re.match(r"\d+ \w+\.? \d{4}", r["Data do Pedido"].strip())]
teste(
    "Nenhuma data em formato extenso (D mes AAAA)",
    len(extenso_residual) == 0,
    f"IDs com formato extenso: {extenso_residual}"
)

# Valida que as datas sao validas (dia 1-31, mes 1-12, ano 2024)
datas_invalidas = []
for r in registros:
    data = r["Data do Pedido"].strip()
    if data and padrao_data.match(data):
        dia, mes, ano = int(data[:2]), int(data[3:5]), int(data[6:])
        if not (1 <= dia <= 31 and 1 <= mes <= 12 and ano == 2024):
            datas_invalidas.append((r["ID Pedido"], data))

teste(
    "Todas as datas tem valores validos (dia/mes/ano)",
    len(datas_invalidas) == 0,
    f"Datas invalidas: {datas_invalidas}"
)
print()


# ─────────────────────────────────────────────
# BLOCO 4: Casing padronizado
# ─────────────────────────────────────────────
print("[BLOCO 4] Casing Padronizado (Title Case)")
print("-" * 45)


def eh_title_case(valor):
    """Verifica se o valor esta em Title Case."""
    return valor == valor.title()


# 4.1 Nome do Cliente
nomes_errados = [(r["ID Pedido"], r["Nome do Cliente"])
                 for r in registros
                 if r["Nome do Cliente"].strip() and not eh_title_case(r["Nome do Cliente"].strip())]
teste(
    "Nome do Cliente em Title Case",
    len(nomes_errados) == 0,
    f"Fora do padrao: {nomes_errados}"
)

# 4.2 Regiao
regioes_erradas = [(r["ID Pedido"], r["Região"])
                   for r in registros
                   if r["Região"].strip() and r["Região"].strip() not in REGIOES_VALIDAS]
teste(
    "Regiao com valores validos e casing correto",
    len(regioes_erradas) == 0,
    f"Fora do padrao: {regioes_erradas}"
)

# 4.3 Representante
reps_errados = [(r["ID Pedido"], r["Representante"])
                for r in registros
                if r["Representante"].strip() and not eh_title_case(r["Representante"].strip())]
teste(
    "Representante em Title Case",
    len(reps_errados) == 0,
    f"Fora do padrao: {reps_errados}"
)

# 4.4 Status
status_errados = [(r["ID Pedido"], r["Status"])
                  for r in registros
                  if r["Status"].strip() and r["Status"].strip() not in STATUS_VALIDOS]
teste(
    "Status com valores validos (Fechado Ganho / Fechado Perdido)",
    len(status_errados) == 0,
    f"Fora do padrao: {status_errados}"
)
print()


# ─────────────────────────────────────────────
# BLOCO 5: Status em ingles
# ─────────────────────────────────────────────
print("[BLOCO 5] Status em Idioma Correto (Portugues)")
print("-" * 45)

termos_ingles = ["closed", "won", "lost", "open", "pending"]
status_ingles = [(r["ID Pedido"], r["Status"])
                 for r in registros
                 if any(t in r["Status"].strip().lower() for t in termos_ingles)]

teste(
    "Nenhum status em ingles",
    len(status_ingles) == 0,
    f"Status em ingles encontrados: {status_ingles}"
)
print()


# ─────────────────────────────────────────────
# BLOCO 6: Status deslocado (ID 1007)
# ─────────────────────────────────────────────
print("[BLOCO 6] Status Deslocado Corrigido (ID 1007)")
print("-" * 45)

reg_1007 = next((r for r in registros if r["ID Pedido"].strip() == "1007"), None)

if reg_1007:
    teste(
        "ID 1007: Status preenchido",
        reg_1007["Status"].strip() != "",
        f"Status ainda vazio"
    )
    teste(
        "ID 1007: Status = 'Fechado Perdido'",
        reg_1007["Status"].strip() == "Fechado Perdido",
        f"Status encontrado: '{reg_1007['Status'].strip()}'"
    )
    teste(
        "ID 1007: Observacoes limpa (valor movido para Status)",
        reg_1007["Observações"].strip() == "",
        f"Observacoes ainda contem: '{reg_1007['Observações'].strip()}'"
    )
else:
    teste("ID 1007: Registro encontrado", False, "ID 1007 nao encontrado no arquivo")
print()


# ─────────────────────────────────────────────
# BLOCO 7: Formato monetario
# ─────────────────────────────────────────────
print("[BLOCO 7] Formato Monetario Brasileiro")
print("-" * 45)

# Padrao: R$ X.XXX,XX ou R$ XXX,XX (sem milhar para valores < 1000)
padrao_moeda = re.compile(r"^R\$ (\d{1,3}\.)*\d{1,3},\d{2}$")
receitas_erradas = []

for r in registros:
    receita = r["Receita"].strip()
    if receita and not padrao_moeda.match(receita):
        receitas_erradas.append((r["ID Pedido"], receita))

teste(
    "Todas as receitas no padrao R$ X.XXX,XX",
    len(receitas_erradas) == 0,
    f"Fora do padrao: {receitas_erradas}"
)

# Verifica que nao usa ponto como decimal
receitas_ponto_decimal = [(r["ID Pedido"], r["Receita"])
                          for r in registros
                          if r["Receita"].strip() and re.search(r"\.\d{2}$", r["Receita"].strip())]
teste(
    "Nenhuma receita com ponto como separador decimal",
    len(receitas_ponto_decimal) == 0,
    f"IDs com ponto decimal: {receitas_ponto_decimal}"
)
print()


# ─────────────────────────────────────────────
# BLOCO 8: Valores ausentes
# ─────────────────────────────────────────────
print("[BLOCO 8] Valores Ausentes (somente os conhecidos)")
print("-" * 45)

campos_criticos = ["Região", "Receita", "Representante", "Status"]
vazios_encontrados = set()
vazios_novos = []

for r in registros:
    pid = r["ID Pedido"].strip()
    for campo in campos_criticos:
        if not r[campo].strip():
            par = (pid, campo)
            vazios_encontrados.add(par)
            if par not in VAZIOS_CONHECIDOS:
                vazios_novos.append(par)

teste(
    "Nenhum valor vazio NOVO introduzido pela limpeza",
    len(vazios_novos) == 0,
    f"Novos vazios: {vazios_novos}"
)

# Verifica que os vazios conhecidos continuam (nao inventou dados)
for pid, campo in VAZIOS_CONHECIDOS:
    teste(
        f"ID {pid}: '{campo}' continua vazio (pendente de validacao manual)",
        (pid, campo) in vazios_encontrados,
        f"Foi preenchido automaticamente (nao deveria)"
    )
print()


# ─────────────────────────────────────────────
# BLOCO 9: Integridade geral
# ─────────────────────────────────────────────
print("[BLOCO 9] Integridade Geral")
print("-" * 45)

# IDs sequenciais (exceto 1005 removido)
ids_esperados = set(str(i) for i in range(1001, 1031)) - {"1005"}
teste(
    "Todos os IDs esperados presentes (1001-1030, exceto 1005)",
    ids_presentes == ids_esperados,
    f"Faltando: {ids_esperados - ids_presentes}, Sobrando: {ids_presentes - ids_esperados}"
)

# Produtos validos
produtos_encontrados = {r["Produto"].strip() for r in registros if r["Produto"].strip()}
teste(
    "Todos os produtos sao valores validos",
    produtos_encontrados.issubset(PRODUTOS_VALIDOS),
    f"Produtos invalidos: {produtos_encontrados - PRODUTOS_VALIDOS}"
)

# Nenhum campo ID vazio
ids_vazios = [i for i, r in enumerate(registros) if not r["ID Pedido"].strip()]
teste(
    "Nenhum ID de Pedido vazio",
    len(ids_vazios) == 0,
    f"Linhas com ID vazio: {ids_vazios}"
)

# Nenhum nome de cliente vazio
nomes_vazios = [r["ID Pedido"] for r in registros if not r["Nome do Cliente"].strip()]
teste(
    "Nenhum Nome de Cliente vazio",
    len(nomes_vazios) == 0,
    f"IDs sem nome: {nomes_vazios}"
)
print()


# ─────────────────────────────────────────────
# BLOCO 10: Validacoes cruzadas especificas
# ─────────────────────────────────────────────
print("[BLOCO 10] Validacoes Cruzadas Especificas")
print("-" * 45)

# ID 1019: status traduzido de "closed won" para "Fechado Ganho"
reg_1019 = next((r for r in registros if r["ID Pedido"].strip() == "1019"), None)
if reg_1019:
    teste(
        "ID 1019: Status traduzido para 'Fechado Ganho' (era 'closed won')",
        reg_1019["Status"].strip() == "Fechado Ganho",
        f"Status encontrado: '{reg_1019['Status'].strip()}'"
    )

# ID 1002: data convertida de ISO
reg_1002 = next((r for r in registros if r["ID Pedido"].strip() == "1002"), None)
if reg_1002:
    teste(
        "ID 1002: Data convertida de '2024-01-22' para '22/01/2024'",
        reg_1002["Data do Pedido"].strip() == "22/01/2024",
        f"Data encontrada: '{reg_1002['Data do Pedido'].strip()}'"
    )

# ID 1008: data convertida de extenso
reg_1008 = next((r for r in registros if r["ID Pedido"].strip() == "1008"), None)
if reg_1008:
    teste(
        "ID 1008: Data convertida de '3 marco 2024' para '03/03/2024'",
        reg_1008["Data do Pedido"].strip() == "03/03/2024",
        f"Data encontrada: '{reg_1008['Data do Pedido'].strip()}'"
    )

# ID 1003: nome corrigido de MAIUSCULAS
reg_1003 = next((r for r in registros if r["ID Pedido"].strip() == "1003"), None)
if reg_1003:
    teste(
        "ID 1003: Nome corrigido de 'PEDRO OLIVEIRA' para 'Pedro Oliveira'",
        reg_1003["Nome do Cliente"].strip() == "Pedro Oliveira",
        f"Nome encontrado: '{reg_1003['Nome do Cliente'].strip()}'"
    )

# ID 1029: regiao corrigida de "Centro-oeste" para "Centro-Oeste"
reg_1029 = next((r for r in registros if r["ID Pedido"].strip() == "1029"), None)
if reg_1029:
    teste(
        "ID 1029: Regiao corrigida de 'Centro-oeste' para 'Centro-Oeste'",
        reg_1029["Região"].strip() == "Centro-Oeste",
        f"Regiao encontrada: '{reg_1029['Região'].strip()}'"
    )

# ID 1001: receita formatada
reg_1001 = next((r for r in registros if r["ID Pedido"].strip() == "1001"), None)
if reg_1001:
    teste(
        "ID 1001: Receita formatada de 'R$ 4320.00' para 'R$ 4.320,00'",
        reg_1001["Receita"].strip() == "R$ 4.320,00",
        f"Receita encontrada: '{reg_1001['Receita'].strip()}'"
    )
print()


# ─────────────────────────────────────────────
# Resultado final
# ─────────────────────────────────────────────
print("=" * 65)
print(f"  RESULTADO: {testes_ok}/{total_testes} testes passaram", end="")
if testes_falha > 0:
    print(f"  |  {testes_falha} FALHA(S)")
else:
    print(f"  |  TODOS OK!")
print("=" * 65)

if falhas:
    print()
    print("  FALHAS DETALHADAS:")
    for nome, detalhe in falhas:
        print(f"    - {nome}")
        if detalhe:
            print(f"      {detalhe}")

sys.exit(0 if testes_falha == 0 else 1)
