"""
App Streamlit — Limpeza e Validação de Dados de Vendas
=======================================================
Upload de CSV → Diagnóstico → Limpeza automática → Validação → Download (CSV/Excel)

Design: Open Design — tema claro, espaçoso, tipografia limpa, paleta suave.
"""

import streamlit as st
import pandas as pd
import re
import io
from datetime import datetime

# ─────────────────────────────────────────────────────
# Configuração da página
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Limpeza de Dados — Vendas",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────
# CSS — Open Design (Light Theme)
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Tipografia ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Forçar tema claro global ── */
    .stApp {
        background-color: #f8f9fc !important;
        color: #1a1a2e !important;
    }

    /* ── Header hero ── */
    .hero-container {
        background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
        border-radius: 20px;
        padding: 2.8rem 2rem 2.2rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #a78bfa);
        border-radius: 20px 20px 0 0;
    }
    .hero-container h1 {
        color: #1e1b4b;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    .hero-container p {
        color: #6b7280;
        font-size: 0.95rem;
        font-weight: 400;
    }

    /* ── Pipeline Steps ── */
    .pipeline {
        display: flex;
        justify-content: center;
        gap: 0.3rem;
        margin-top: 1.2rem;
        flex-wrap: wrap;
    }
    .pipeline .step {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        background: #f1f5f9;
        border-radius: 100px;
        padding: 0.35rem 0.9rem;
        font-size: 0.78rem;
        font-weight: 500;
        color: #475569;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    .pipeline .step.active {
        background: #6366f1;
        color: #ffffff;
        border-color: #6366f1;
    }
    .pipeline .step-arrow {
        color: #cbd5e1;
        font-size: 0.9rem;
    }

    /* ── Metric cards ── */
    .metric-row {
        display: flex;
        gap: 0.8rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    .metric-card {
        flex: 1;
        min-width: 145px;
        background: #ffffff;
        border-radius: 16px;
        padding: 1.3rem 1rem;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.07);
    }
    .metric-card .value {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 0.25rem;
    }
    .metric-card .label {
        font-size: 0.72rem;
        color: #9ca3af;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .clr-red    { color: #ef4444; }
    .clr-orange { color: #f59e0b; }
    .clr-green  { color: #10b981; }
    .clr-blue   { color: #6366f1; }
    .clr-purple { color: #8b5cf6; }

    /* ── Section headers ── */
    .section-header {
        background: #ffffff;
        border-left: 4px solid #6366f1;
        border-radius: 0 12px 12px 0;
        padding: 0.9rem 1.4rem;
        margin: 2rem 0 1.2rem 0;
        border: 1px solid #e5e7eb;
        border-left: 4px solid #6366f1;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }
    .section-header h3 {
        margin: 0;
        font-size: 1.05rem;
        font-weight: 700;
        color: #1e1b4b;
    }

    /* ── Log entries ── */
    .log-entry {
        background: #ffffff;
        border-left: 3px solid #6366f1;
        border-radius: 0 10px 10px 0;
        padding: 0.65rem 1rem;
        margin-bottom: 0.45rem;
        font-size: 0.82rem;
        border: 1px solid #f1f5f9;
        border-left: 3px solid #6366f1;
        transition: background 0.15s ease, box-shadow 0.15s ease;
    }
    .log-entry:hover {
        background: #f8fafc;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .log-entry .col-name {
        color: #6366f1;
        font-weight: 600;
    }
    .log-entry .arrow {
        color: #cbd5e1;
        margin: 0 0.3rem;
    }
    .log-entry .old-val {
        color: #ef4444;
        text-decoration: line-through;
        opacity: 0.75;
    }
    .log-entry .new-val {
        color: #10b981;
        font-weight: 600;
    }
    .log-entry strong {
        color: #1e1b4b;
    }
    .log-entry small {
        color: #9ca3af !important;
    }

    /* ── Test results ── */
    .test-pass {
        color: #10b981;
        font-weight: 600;
    }
    .test-fail {
        color: #ef4444;
        font-weight: 600;
    }

    /* ── Download cards ── */
    .download-section {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        text-align: center;
        margin-top: 0.8rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        transition: box-shadow 0.2s ease;
    }
    .download-section:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    .download-section p {
        color: #374151 !important;
    }
    .download-section .dl-subtitle {
        color: #9ca3af !important;
        font-size: 0.8rem;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e5e7eb;
    }
    [data-testid="stSidebar"] * {
        color: #1e1b4b !important;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: #4b5563 !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #1e1b4b !important;
    }

    /* ── Uploader ── */
    [data-testid="stFileUploader"] {
        border: 2px dashed #c7d2fe;
        border-radius: 16px;
        padding: 1rem;
        background: #f8f9ff;
        transition: border-color 0.3s ease, background 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
        background: #eef2ff;
    }

    /* ── Empty state ── */
    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
    }
    .empty-state .icon {
        font-size: 3.5rem;
        margin-bottom: 0.8rem;
        opacity: 0.6;
    }
    .empty-state .title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.3rem;
    }
    .empty-state .subtitle {
        font-size: 0.9rem;
        color: #9ca3af;
    }

    /* ── Badge ── */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-red {
        background: #fef2f2;
        color: #ef4444;
        border: 1px solid #fecaca;
    }
    .badge-green {
        background: #ecfdf5;
        color: #10b981;
        border: 1px solid #a7f3d0;
    }
    .badge-blue {
        background: #eef2ff;
        color: #6366f1;
        border: 1px solid #c7d2fe;
    }

    /* ── Expander override ── */
    [data-testid="stExpander"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        margin-bottom: 0.6rem;
    }

    /* ── Footer credits ── */
    .footer-credits {
        text-align: center;
        color: #cbd5e1;
        font-size: 0.72rem;
        padding: 2rem 0 1rem 0;
        letter-spacing: 0.3px;
    }

    /* ── Divider ── */
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1.5rem 0;
    }

    /* ── Summary bar ── */
    .summary-bar {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1rem;
    }
    .summary-bar.error {
        background: #fef2f2;
        border-color: #fecaca;
    }
    .summary-bar .bar-icon {
        font-size: 1.5rem;
    }
    .summary-bar .bar-text {
        font-size: 0.9rem;
        font-weight: 500;
        color: #166534;
    }
    .summary-bar.error .bar-text {
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────
# Constantes e mapeamentos (da limpeza_vendas.py)
# ─────────────────────────────────────────────────────
MESES = {
    "jan": "01", "jan.": "01", "janeiro": "01",
    "fev": "02", "fev.": "02", "fevereiro": "02",
    "mar": "03", "mar.": "03", "março": "03",
    "abr": "04", "abr.": "04", "abril": "04",
    "mai": "05", "mai.": "05", "maio": "05",
    "jun": "06", "jun.": "06", "junho": "06",
    "jul": "07", "jul.": "07", "julho": "07",
    "ago": "08", "ago.": "08", "agosto": "08",
    "set": "09", "set.": "09", "setembro": "09",
    "out": "10", "out.": "10", "outubro": "10",
    "nov": "11", "nov.": "11", "novembro": "11",
    "dez": "12", "dez.": "12", "dezembro": "12",
}

STATUS_TRADUCAO = {
    "closed won": "Fechado Ganho",
    "closed lost": "Fechado Perdido",
}

REGIOES_VALIDAS = {
    "norte": "Norte",
    "nordeste": "Nordeste",
    "centro-oeste": "Centro-Oeste",
    "sudeste": "Sudeste",
    "sul": "Sul",
}

STATUS_VALIDOS = {"Fechado Ganho", "Fechado Perdido"}
PRODUTOS_VALIDOS = {"Licença de Software", "Consultoria", "Hardware", "Pacote Empresarial"}

COLUNAS_ESPERADAS = [
    "ID Pedido", "Nome do Cliente", "Região", "Representante",
    "Data do Pedido", "Receita", "Produto", "Status", "Observações"
]


# ─────────────────────────────────────────────────────
# Funções de limpeza
# ─────────────────────────────────────────────────────

def padronizar_data(valor, id_pedido, log_list):
    original = str(valor).strip()
    if not original or original == "nan":
        return original

    if re.match(r"^\d{2}/\d{2}/\d{4}$", original):
        return original

    match_iso = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", original)
    if match_iso:
        ano, mes, dia = match_iso.groups()
        novo = f"{dia}/{mes}/{ano}"
        log_list.append({"id": id_pedido, "coluna": "Data do Pedido", "antes": original, "depois": novo, "motivo": "Convertido de ISO para DD/MM/AAAA"})
        return novo

    match_ext = re.match(r"^(\d{1,2})\s+(\S+)\s+(\d{4})$", original)
    if match_ext:
        dia, mes_texto, ano = match_ext.groups()
        mes_num = MESES.get(mes_texto.lower())
        if mes_num:
            novo = f"{int(dia):02d}/{mes_num}/{ano}"
            log_list.append({"id": id_pedido, "coluna": "Data do Pedido", "antes": original, "depois": novo, "motivo": "Convertido de extenso para DD/MM/AAAA"})
            return novo

    return original


def padronizar_nome(valor, id_pedido, coluna, log_list):
    original = str(valor).strip()
    if not original or original == "nan":
        return original
    novo = original.title()
    if novo != original:
        log_list.append({"id": id_pedido, "coluna": coluna, "antes": original, "depois": novo, "motivo": "Padronizado para Title Case"})
    return novo


def padronizar_regiao(valor, id_pedido, log_list):
    original = str(valor).strip()
    if not original or original == "nan":
        return original
    chave = original.lower()
    novo = REGIOES_VALIDAS.get(chave, original.title())
    if novo != original:
        log_list.append({"id": id_pedido, "coluna": "Região", "antes": original, "depois": novo, "motivo": "Padronizado casing da região"})
    return novo


def padronizar_status(valor, id_pedido, log_list):
    original = str(valor).strip()
    if not original or original == "nan":
        return original
    chave = original.lower()
    if chave in STATUS_TRADUCAO:
        novo = STATUS_TRADUCAO[chave]
        log_list.append({"id": id_pedido, "coluna": "Status", "antes": original, "depois": novo, "motivo": "Traduzido de inglês para português"})
        return novo
    novo = original.title()
    if novo != original:
        log_list.append({"id": id_pedido, "coluna": "Status", "antes": original, "depois": novo, "motivo": "Padronizado para Title Case"})
    return novo


def padronizar_receita(valor, id_pedido, log_list):
    original = str(valor).strip()
    if not original or original == "nan":
        return original
    valor_limpo = original.replace("R$", "").strip()
    try:
        numero = float(valor_limpo)
    except ValueError:
        return original
    parte_inteira = int(numero)
    parte_decimal = round((numero - parte_inteira) * 100)
    inteiro_formatado = f"{parte_inteira:,}".replace(",", ".")
    novo = f"R$ {inteiro_formatado},{parte_decimal:02d}"
    if novo != original:
        log_list.append({"id": id_pedido, "coluna": "Receita", "antes": original, "depois": novo, "motivo": "Formatado para padrão monetário BR"})
    return novo


def executar_limpeza(df):
    """Executa todas as etapas de limpeza e retorna (df_limpo, log_alteracoes, resumo)."""
    log_list = []
    df = df.copy()

    # Preenche NaN com string vazia para manipulação
    df = df.fillna("")

    # ETAPA 1: Corrigir status deslocado
    for idx, row in df.iterrows():
        status = str(row["Status"]).strip()
        obs = str(row["Observações"]).strip().lower()
        pid = str(row["ID Pedido"]).strip()
        if (not status or status == "nan") and obs in ("fechado ganho", "fechado perdido", "closed won", "closed lost"):
            log_list.append({"id": pid, "coluna": "Status", "antes": "(vazio)", "depois": obs, "motivo": "Movido da coluna Observações para Status"})
            log_list.append({"id": pid, "coluna": "Observações", "antes": row["Observações"], "depois": "", "motivo": "Valor movido para coluna Status"})
            df.at[idx, "Status"] = obs
            df.at[idx, "Observações"] = ""

    # ETAPA 2: Remover duplicados confirmados
    duplicados_mask = []
    seen = {}
    for idx, row in df.iterrows():
        chave = (
            str(row["Nome do Cliente"]).strip().lower(),
            str(row["Data do Pedido"]).strip(),
            str(row["Receita"]).strip(),
            str(row["Produto"]).strip(),
        )
        obs = str(row["Observações"]).strip().lower()
        pid = str(row["ID Pedido"]).strip()
        if chave in seen and obs == "duplicado":
            duplicados_mask.append(idx)
            log_list.append({"id": pid, "coluna": "(registro)", "antes": "presente", "depois": "REMOVIDO", "motivo": f"Duplicado exato confirmado de ID {seen[chave]}"})
        else:
            seen[chave] = pid

    registros_removidos = len(duplicados_mask)
    df = df.drop(duplicados_mask).reset_index(drop=True)

    # ETAPA 3: Padronizar casing
    for idx, row in df.iterrows():
        pid = str(row["ID Pedido"]).strip()
        df.at[idx, "Nome do Cliente"] = padronizar_nome(row["Nome do Cliente"], pid, "Nome do Cliente", log_list)
        df.at[idx, "Representante"] = padronizar_nome(row["Representante"], pid, "Representante", log_list)
        df.at[idx, "Região"] = padronizar_regiao(row["Região"], pid, log_list)
        df.at[idx, "Status"] = padronizar_status(row["Status"], pid, log_list)

    # ETAPA 4: Padronizar datas
    for idx, row in df.iterrows():
        pid = str(row["ID Pedido"]).strip()
        df.at[idx, "Data do Pedido"] = padronizar_data(row["Data do Pedido"], pid, log_list)

    # ETAPA 5: Padronizar receita
    for idx, row in df.iterrows():
        pid = str(row["ID Pedido"]).strip()
        df.at[idx, "Receita"] = padronizar_receita(row["Receita"], pid, log_list)

    # Resumo por categoria
    resumo = {}
    for entry in log_list:
        motivo = entry["motivo"]
        resumo[motivo] = resumo.get(motivo, 0) + 1

    return df, log_list, resumo, registros_removidos


# ─────────────────────────────────────────────────────
# Funções de validação
# ─────────────────────────────────────────────────────

def executar_testes(df):
    """Executa todos os testes de validação e retorna lista de resultados."""
    resultados = []

    def teste(bloco, nome, condicao, detalhe=""):
        resultados.append({
            "bloco": bloco,
            "nome": nome,
            "passou": condicao,
            "detalhe": detalhe,
        })

    ids_presentes = set(df["ID Pedido"].astype(str).str.strip())

    # BLOCO 1: Estrutura
    teste("Estrutura", "Colunas corretas", list(df.columns) == COLUNAS_ESPERADAS)
    teste("Estrutura", "IDs únicos", df["ID Pedido"].nunique() == len(df))

    # BLOCO 2: Duplicados
    teste("Duplicados", "ID 1005 removido", "1005" not in ids_presentes)

    chaves = set()
    tem_dup = False
    for _, row in df.iterrows():
        chave = (
            str(row["Nome do Cliente"]).strip().lower(),
            str(row["Data do Pedido"]).strip(),
            str(row["Receita"]).strip(),
            str(row["Produto"]).strip(),
        )
        if chave in chaves and str(row["Receita"]).strip():
            tem_dup = True
        chaves.add(chave)
    teste("Duplicados", "Nenhum duplicado exato restante", not tem_dup)

    # BLOCO 3: Datas
    padrao_data = re.compile(r"^\d{2}/\d{2}/\d{4}$")
    datas_erradas = []
    for _, row in df.iterrows():
        d = str(row["Data do Pedido"]).strip()
        if d and d != "nan" and not padrao_data.match(d):
            datas_erradas.append(str(row["ID Pedido"]))
    teste("Datas", "Todas as datas em DD/MM/AAAA", len(datas_erradas) == 0,
          f"IDs fora do padrão: {datas_erradas}" if datas_erradas else "")

    iso_res = [str(row["ID Pedido"]) for _, row in df.iterrows()
               if re.match(r"\d{4}-\d{2}-\d{2}", str(row["Data do Pedido"]).strip())]
    teste("Datas", "Sem formato ISO residual", len(iso_res) == 0)

    ext_res = [str(row["ID Pedido"]) for _, row in df.iterrows()
               if re.match(r"\d+ \w+\.? \d{4}", str(row["Data do Pedido"]).strip())]
    teste("Datas", "Sem formato extenso residual", len(ext_res) == 0)

    # BLOCO 4: Casing
    nomes_err = [str(row["ID Pedido"]) for _, row in df.iterrows()
                 if str(row["Nome do Cliente"]).strip() and str(row["Nome do Cliente"]).strip() != str(row["Nome do Cliente"]).strip().title()]
    teste("Casing", "Nomes em Title Case", len(nomes_err) == 0,
          f"IDs: {nomes_err}" if nomes_err else "")

    reg_err = [str(row["ID Pedido"]) for _, row in df.iterrows()
               if str(row["Região"]).strip() and str(row["Região"]).strip() not in REGIOES_VALIDAS and str(row["Região"]).strip() != "" and str(row["Região"]).strip() != "nan"]
    teste("Casing", "Regiões com valores válidos", len(reg_err) == 0,
          f"IDs: {reg_err}" if reg_err else "")

    rep_err = [str(row["ID Pedido"]) for _, row in df.iterrows()
               if str(row["Representante"]).strip() and str(row["Representante"]).strip() != "nan" and str(row["Representante"]).strip() != str(row["Representante"]).strip().title()]
    teste("Casing", "Representantes em Title Case", len(rep_err) == 0,
          f"IDs: {rep_err}" if rep_err else "")

    st_err = [str(row["ID Pedido"]) for _, row in df.iterrows()
              if str(row["Status"]).strip() and str(row["Status"]).strip() != "nan" and str(row["Status"]).strip() not in STATUS_VALIDOS]
    teste("Casing", "Status com valores válidos", len(st_err) == 0,
          f"IDs: {st_err}" if st_err else "")

    # BLOCO 5: Status em inglês
    termos_en = ["closed", "won", "lost", "open", "pending"]
    en_err = [str(row["ID Pedido"]) for _, row in df.iterrows()
              if any(t in str(row["Status"]).lower() for t in termos_en)]
    teste("Idioma", "Nenhum status em inglês", len(en_err) == 0,
          f"IDs: {en_err}" if en_err else "")

    # BLOCO 6: Formato monetário
    padrao_moeda = re.compile(r"^R\$ (\d{1,3}\.)*\d{1,3},\d{2}$")
    moeda_err = []
    for _, row in df.iterrows():
        rec = str(row["Receita"]).strip()
        if rec and rec != "nan" and rec != "" and not padrao_moeda.match(rec):
            moeda_err.append(str(row["ID Pedido"]))
    teste("Monetário", "Receitas no padrão R$ X.XXX,XX", len(moeda_err) == 0,
          f"IDs: {moeda_err}" if moeda_err else "")

    ponto_dec = [str(row["ID Pedido"]) for _, row in df.iterrows()
                 if str(row["Receita"]).strip() and re.search(r"\.\d{2}$", str(row["Receita"]).strip())]
    teste("Monetário", "Sem ponto como separador decimal", len(ponto_dec) == 0,
          f"IDs: {ponto_dec}" if ponto_dec else "")

    # BLOCO 7: Integridade
    prod_found = {str(row["Produto"]).strip() for _, row in df.iterrows() if str(row["Produto"]).strip() and str(row["Produto"]).strip() != "nan"}
    teste("Integridade", "Produtos são valores válidos", prod_found.issubset(PRODUTOS_VALIDOS),
          f"Inválidos: {prod_found - PRODUTOS_VALIDOS}" if not prod_found.issubset(PRODUTOS_VALIDOS) else "")

    nomes_vazio = [str(row["ID Pedido"]) for _, row in df.iterrows() if not str(row["Nome do Cliente"]).strip() or str(row["Nome do Cliente"]).strip() == "nan"]
    teste("Integridade", "Nenhum Nome de Cliente vazio", len(nomes_vazio) == 0)

    return resultados


# ─────────────────────────────────────────────────────
# Funções de diagnóstico (sobre o arquivo ORIGINAL)
# ─────────────────────────────────────────────────────

def diagnosticar(df):
    """Retorna um dicionário com contadores de problemas do arquivo original."""
    problemas = {
        "casing": 0,
        "datas": 0,
        "vazios": 0,
        "duplicados": 0,
        "monetario": 0,
        "status_ingles": 0,
        "status_deslocado": 0,
    }
    detalhes = []

    # Casing
    for _, row in df.iterrows():
        pid = str(row["ID Pedido"])
        for col in ["Nome do Cliente", "Representante"]:
            v = str(row[col]).strip()
            if v and v != "nan" and v != v.title():
                problemas["casing"] += 1
                detalhes.append(f"ID {pid}: {col} '{v}' → casing incorreto")
        reg = str(row["Região"]).strip()
        if reg and reg != "nan" and reg not in REGIOES_VALIDAS.values():
            problemas["casing"] += 1
            detalhes.append(f"ID {pid}: Região '{reg}' → casing incorreto")
        st_val = str(row["Status"]).strip()
        if st_val and st_val != "nan" and st_val not in STATUS_VALIDOS:
            if st_val.lower() not in ("closed won", "closed lost"):
                problemas["casing"] += 1
                detalhes.append(f"ID {pid}: Status '{st_val}' → casing incorreto")

    # Datas
    for _, row in df.iterrows():
        d = str(row["Data do Pedido"]).strip()
        if d and d != "nan" and not re.match(r"^\d{2}/\d{2}/\d{4}$", d):
            problemas["datas"] += 1

    # Vazios
    for _, row in df.iterrows():
        pid = str(row["ID Pedido"])
        for col in ["Região", "Receita", "Representante", "Status"]:
            v = str(row[col]).strip()
            if not v or v == "nan":
                problemas["vazios"] += 1

    # Duplicados
    seen = {}
    for _, row in df.iterrows():
        chave = (
            str(row["Nome do Cliente"]).strip().lower(),
            str(row["Data do Pedido"]).strip(),
            str(row["Receita"]).strip(),
            str(row["Produto"]).strip(),
        )
        if chave in seen:
            problemas["duplicados"] += 1
        else:
            seen[chave] = str(row["ID Pedido"])

    # Monetário
    for _, row in df.iterrows():
        rec = str(row["Receita"]).strip()
        if rec and rec != "nan" and "R$" in rec:
            val = rec.replace("R$", "").strip()
            if "," not in val and "." in val:
                problemas["monetario"] += 1

    # Status em inglês
    for _, row in df.iterrows():
        st_val = str(row["Status"]).strip().lower()
        if "closed" in st_val or "won" in st_val or "lost" in st_val:
            problemas["status_ingles"] += 1

    # Status deslocado
    for _, row in df.iterrows():
        st_val = str(row["Status"]).strip()
        obs = str(row["Observações"]).strip().lower()
        if (not st_val or st_val == "nan") and obs in ("fechado ganho", "fechado perdido", "closed won", "closed lost"):
            problemas["status_deslocado"] += 1

    total = sum(problemas.values())
    return problemas, total, detalhes


# ─────────────────────────────────────────────────────
# Interface principal
# ─────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero-container">
    <h1>🧹 Limpeza de Dados — Vendas</h1>
    <p>Faça upload do seu CSV e receba um arquivo limpo, validado e pronto para análise.</p>
    <div class="pipeline">
        <span class="step">📤 Upload</span>
        <span class="step-arrow">→</span>
        <span class="step">🔍 Diagnóstico</span>
        <span class="step-arrow">→</span>
        <span class="step">🧹 Limpeza</span>
        <span class="step-arrow">→</span>
        <span class="step">✅ Validação</span>
        <span class="step-arrow">→</span>
        <span class="step">📥 Download</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar — Upload
with st.sidebar:
    st.markdown("### 📂 Upload do Arquivo")
    uploaded_file = st.file_uploader(
        "Arraste o CSV aqui ou clique para selecionar",
        type=["csv"],
        help="Formato esperado: CSV com separador vírgula e encoding UTF-8",
    )

    if uploaded_file:
        st.success(f"✅ **{uploaded_file.name}** carregado!")

    st.markdown("---")
    st.markdown("### ℹ️ Sobre o App")
    st.markdown("""
    Pipeline completa de qualidade de dados:

    1. **Diagnóstico** — identifica inconsistências
    2. **Limpeza** — corrige automaticamente
    3. **Validação** — testa todas as correções
    4. **Download** — CSV ou Excel
    """)
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#9ca3af !important; font-size:0.72rem;'>"
        "Bloco 01 — Engenharia e Análise de Dados</p>",
        unsafe_allow_html=True,
    )

# ── Conteúdo principal ──
if not uploaded_file:
    # Estado inicial — instrução
    st.markdown("""
    <div class="empty-state">
        <div class="icon">📤</div>
        <div class="title">Faça o upload de um arquivo CSV na barra lateral</div>
        <div class="subtitle">O arquivo será analisado, limpo e validado automaticamente.</div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Carregar dados
    df_original = pd.read_csv(uploaded_file)

    # ──────────────────────────────────
    # FASE 1: Diagnóstico do Original
    # ──────────────────────────────────
    problemas, total_problemas, detalhes_diag = diagnosticar(df_original)

    st.markdown('<div class="section-header"><h3>🔍 Diagnóstico do Arquivo Original</h3></div>', unsafe_allow_html=True)

    # Summary bar
    st.markdown(f"""
    <div class="summary-bar error">
        <span class="bar-icon">⚠️</span>
        <span class="bar-text">Encontrados <strong>{total_problemas} problemas</strong> em {len(df_original)} registros — a limpeza será aplicada automaticamente.</span>
    </div>
    """, unsafe_allow_html=True)

    # Métricas do diagnóstico
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="value clr-blue">{len(df_original)}</div>
            <div class="label">Registros</div>
        </div>
        <div class="metric-card">
            <div class="value clr-red">{total_problemas}</div>
            <div class="label">Problemas</div>
        </div>
        <div class="metric-card">
            <div class="value clr-orange">{problemas['casing']}</div>
            <div class="label">Casing</div>
        </div>
        <div class="metric-card">
            <div class="value clr-orange">{problemas['datas']}</div>
            <div class="label">Datas</div>
        </div>
        <div class="metric-card">
            <div class="value clr-purple">{problemas['monetario']}</div>
            <div class="label">Receita</div>
        </div>
        <div class="metric-card">
            <div class="value clr-red">{problemas['vazios']}</div>
            <div class="label">Vazios</div>
        </div>
        <div class="metric-card">
            <div class="value clr-red">{problemas['duplicados']}</div>
            <div class="label">Duplicados</div>
        </div>
        <div class="metric-card">
            <div class="value clr-orange">{problemas['status_ingles'] + problemas['status_deslocado']}</div>
            <div class="label">Status</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Preview do original
    with st.expander("👁️  Visualizar dados originais", expanded=False):
        st.dataframe(df_original, use_container_width=True, height=300)

    st.markdown("---")

    # ──────────────────────────────────
    # FASE 2: Limpeza
    # ──────────────────────────────────
    st.markdown('<div class="section-header"><h3>🧹 Limpeza Automática</h3></div>', unsafe_allow_html=True)

    df_limpo, log_alteracoes, resumo, removidos = executar_limpeza(df_original)

    # Summary bar
    st.markdown(f"""
    <div class="summary-bar">
        <span class="bar-icon">✨</span>
        <span class="bar-text">Aplicadas <strong>{len(log_alteracoes)} correções</strong> em {len(resumo)} categorias — {removidos} registro(s) duplicado(s) removido(s).</span>
    </div>
    """, unsafe_allow_html=True)

    # Métricas da limpeza
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="value clr-green">{len(log_alteracoes)}</div>
            <div class="label">Total Correções</div>
        </div>
        <div class="metric-card">
            <div class="value clr-green">{len(df_limpo)}</div>
            <div class="label">Registros Finais</div>
        </div>
        <div class="metric-card">
            <div class="value clr-red">{removidos}</div>
            <div class="label">Removidos</div>
        </div>
        <div class="metric-card">
            <div class="value clr-blue">{len(resumo)}</div>
            <div class="label">Categorias</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Resumo por categoria
    with st.expander("📋  Resumo por categoria de correção", expanded=True):
        for motivo, qtd in sorted(resumo.items(), key=lambda x: -x[1]):
            if "Title Case" in motivo or "Padronizado" in motivo:
                badge = '<span class="badge badge-blue">CASING</span>'
            elif "Convertido" in motivo:
                badge = '<span class="badge badge-blue">DATA</span>'
            elif "Formatado" in motivo:
                badge = '<span class="badge badge-blue">MOEDA</span>'
            elif "Traduzido" in motivo or "Movido" in motivo:
                badge = '<span class="badge badge-green">STATUS</span>'
            elif "Duplicado" in motivo:
                badge = '<span class="badge badge-red">DUPLICADO</span>'
            else:
                badge = '<span class="badge badge-blue">OUTRO</span>'
            st.markdown(
                f'{badge} &nbsp; **{motivo}** — `{qtd}` registro(s)',
                unsafe_allow_html=True,
            )

    # Log detalhado
    with st.expander(f"📝  Log detalhado de alterações ({len(log_alteracoes)} itens)", expanded=False):
        for entry in log_alteracoes:
            st.markdown(
                f'<div class="log-entry">'
                f'<strong>ID {entry["id"]}</strong> · '
                f'<span class="col-name">{entry["coluna"]}</span>'
                f'<span class="arrow"> → </span>'
                f'<span class="old-val">{entry["antes"]}</span>'
                f'<span class="arrow"> ➜ </span>'
                f'<span class="new-val">{entry["depois"]}</span>'
                f'<br><small>{entry["motivo"]}</small>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Preview limpo
    with st.expander("👁️  Visualizar dados limpos", expanded=False):
        st.dataframe(df_limpo, use_container_width=True, height=300)

    st.markdown("---")

    # ──────────────────────────────────
    # FASE 3: Validação
    # ──────────────────────────────────
    st.markdown('<div class="section-header"><h3>✅ Validação Automática</h3></div>', unsafe_allow_html=True)

    resultados_testes = executar_testes(df_limpo)
    testes_ok = sum(1 for r in resultados_testes if r["passou"])
    testes_falha = sum(1 for r in resultados_testes if not r["passou"])
    total_testes = len(resultados_testes)

    # Summary bar
    if testes_falha == 0:
        st.markdown(f"""
        <div class="summary-bar">
            <span class="bar-icon">🎉</span>
            <span class="bar-text"><strong>{testes_ok}/{total_testes} testes aprovados</strong> — Todos os critérios de qualidade foram atendidos!</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="summary-bar error">
            <span class="bar-icon">⚠️</span>
            <span class="bar-text"><strong>{testes_falha} teste(s) falharam</strong> — Verifique os detalhes abaixo.</span>
        </div>
        """, unsafe_allow_html=True)

    # Métricas de validação
    cor_resultado = "clr-green" if testes_falha == 0 else "clr-red"
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="value {cor_resultado}">{testes_ok}/{total_testes}</div>
            <div class="label">Testes</div>
        </div>
        <div class="metric-card">
            <div class="value clr-green">{testes_ok}</div>
            <div class="label">✅ Aprovados</div>
        </div>
        <div class="metric-card">
            <div class="value clr-red">{testes_falha}</div>
            <div class="label">❌ Reprovados</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Resultado por bloco
    blocos = {}
    for r in resultados_testes:
        blocos.setdefault(r["bloco"], []).append(r)

    for bloco, testes in blocos.items():
        all_pass = all(t["passou"] for t in testes)
        icon = "✅" if all_pass else "❌"
        with st.expander(f"{icon}  {bloco} — {sum(1 for t in testes if t['passou'])}/{len(testes)} testes", expanded=not all_pass):
            for t in testes:
                if t["passou"]:
                    st.markdown(f'<span class="test-pass">✅ PASS</span> &nbsp; {t["nome"]}', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="test-fail">❌ FAIL</span> &nbsp; {t["nome"]}', unsafe_allow_html=True)
                    if t["detalhe"]:
                        st.caption(t["detalhe"])

    # Alerta de campos vazios pendentes
    campos_vazios = []
    for _, row in df_limpo.iterrows():
        pid = str(row["ID Pedido"]).strip()
        for col in ["Região", "Receita", "Representante", "Status"]:
            v = str(row[col]).strip()
            if not v or v == "nan":
                campos_vazios.append(f"ID {pid}: **{col}** vazio")

    if campos_vazios:
        st.markdown("---")
        st.warning("⚠️ **Campos que permanecem vazios** (requerem validação manual):")
        for item in campos_vazios:
            st.markdown(f"- {item}")

    st.markdown("---")

    # ──────────────────────────────────
    # FASE 4: Comparação Antes vs Depois
    # ──────────────────────────────────
    st.markdown('<div class="section-header"><h3>🔄 Comparação: Antes vs Depois</h3></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📄 Original** &nbsp; <span class='badge badge-red'>COM ERROS</span>", unsafe_allow_html=True)
        st.dataframe(df_original, use_container_width=True, height=350)
    with col2:
        st.markdown("**✨ Limpo** &nbsp; <span class='badge badge-green'>VALIDADO</span>", unsafe_allow_html=True)
        st.dataframe(df_limpo, use_container_width=True, height=350)

    st.markdown("---")

    # ──────────────────────────────────
    # FASE 5: Download
    # ──────────────────────────────────
    st.markdown('<div class="section-header"><h3>📥 Download do Arquivo Limpo</h3></div>', unsafe_allow_html=True)

    col_csv, col_excel = st.columns(2)

    # CSV
    csv_buffer = io.StringIO()
    df_limpo.to_csv(csv_buffer, index=False, encoding="utf-8")
    csv_data = csv_buffer.getvalue()

    with col_csv:
        st.markdown("""
        <div class="download-section">
            <p style="font-size:2.2rem; margin-bottom:0.3rem;">📄</p>
            <p style="font-weight:700; font-size:1.1rem; margin-bottom:0.2rem;">CSV</p>
            <p class="dl-subtitle">Formato universal, leve e compatível</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="⬇️  Baixar CSV",
            data=csv_data,
            file_name="f_Vendas_limpa.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df_limpo.to_excel(writer, index=False, sheet_name="Vendas Limpas")
        # Adiciona aba com log
        df_log = pd.DataFrame(log_alteracoes)
        if not df_log.empty:
            df_log.columns = ["ID Pedido", "Coluna", "Antes", "Depois", "Motivo"]
            df_log.to_excel(writer, index=False, sheet_name="Log de Alterações")
    excel_data = excel_buffer.getvalue()

    with col_excel:
        st.markdown("""
        <div class="download-section">
            <p style="font-size:2.2rem; margin-bottom:0.3rem;">📊</p>
            <p style="font-weight:700; font-size:1.1rem; margin-bottom:0.2rem;">Excel</p>
            <p class="dl-subtitle">Inclui aba com log de alterações</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="⬇️  Baixar Excel",
            data=excel_data,
            file_name="f_Vendas_limpa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    # Footer
    st.markdown(
        '<div class="footer-credits">Bloco 01 — Limpeza, diagnóstico, prompt e validação · Jornada de Dados</div>',
        unsafe_allow_html=True,
    )
