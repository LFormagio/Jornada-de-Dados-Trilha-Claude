"""
Script de Limpeza — f_Vendas.csv
================================
Corrige todas as inconsistências identificadas no diagnóstico:
  1. Padroniza casing (Title Case) em Nome, Região, Representante, Status
  2. Unifica formatos de data para DD/MM/AAAA
  3. Corrige status deslocado (ID 1007: Observações → Status)
  4. Traduz status em inglês (closed won → Fechado Ganho)
  5. Remove duplicado confirmado (ID 1005)
  6. Padroniza formato monetário para padrão brasileiro (R$ 4.320,00)
  7. Corrige variação "Centro-oeste" → "Centro-Oeste"
  8. Registra log de todas as alterações realizadas

Entrada:  f_Vendas.csv
Saída:    f_Vendas_limpa.csv  +  log_limpeza.txt
"""

import csv
import re
import os
from datetime import datetime

# ─────────────────────────────────────────────
# Configuração de caminhos
# ─────────────────────────────────────────────
DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_ENTRADA = os.path.join(DIR, "f_Vendas.csv")
ARQUIVO_SAIDA = os.path.join(DIR, "f_Vendas_limpa.csv")
ARQUIVO_LOG = os.path.join(DIR, "log_limpeza.txt")

# Acumulador de logs
log_alteracoes = []


def log(id_pedido, coluna, valor_antes, valor_depois, motivo):
    """Registra uma alteração no log."""
    log_alteracoes.append({
        "id": id_pedido,
        "coluna": coluna,
        "antes": valor_antes,
        "depois": valor_depois,
        "motivo": motivo,
    })


# ─────────────────────────────────────────────
# Mapeamento de meses em extenso para número
# ─────────────────────────────────────────────
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

# Mapeamento de status inglês → português
STATUS_TRADUCAO = {
    "closed won": "Fechado Ganho",
    "closed lost": "Fechado Perdido",
}

# Regiões válidas (para padronização)
REGIOES_VALIDAS = {
    "norte": "Norte",
    "nordeste": "Nordeste",
    "centro-oeste": "Centro-Oeste",
    "sudeste": "Sudeste",
    "sul": "Sul",
}


# ─────────────────────────────────────────────
# Funções de limpeza
# ─────────────────────────────────────────────

def padronizar_data(valor, id_pedido):
    """Converte qualquer formato de data para DD/MM/AAAA."""
    original = valor.strip()
    if not original:
        return original

    # Formato 1: DD/MM/AAAA (já está correto)
    if re.match(r"^\d{2}/\d{2}/\d{4}$", original):
        return original

    # Formato 2: AAAA-MM-DD (ISO)
    match_iso = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", original)
    if match_iso:
        ano, mes, dia = match_iso.groups()
        novo = f"{dia}/{mes}/{ano}"
        log(id_pedido, "Data do Pedido", original, novo, "Convertido de ISO (AAAA-MM-DD) para DD/MM/AAAA")
        return novo

    # Formato 3: D(D) mês(.) AAAA (extenso)
    match_ext = re.match(r"^(\d{1,2})\s+(\S+)\s+(\d{4})$", original)
    if match_ext:
        dia, mes_texto, ano = match_ext.groups()
        mes_num = MESES.get(mes_texto.lower())
        if mes_num:
            novo = f"{int(dia):02d}/{mes_num}/{ano}"
            log(id_pedido, "Data do Pedido", original, novo, "Convertido de extenso para DD/MM/AAAA")
            return novo

    # Se não reconheceu, mantém e avisa
    log(id_pedido, "Data do Pedido", original, original, "⚠️ Formato não reconhecido — mantido sem alteração")
    return original


def padronizar_casing_nome(valor, id_pedido):
    """Aplica Title Case ao nome do cliente."""
    original = valor.strip()
    if not original:
        return original

    novo = original.title()
    if novo != original:
        log(id_pedido, "Nome do Cliente", original, novo, "Padronizado para Title Case")
    return novo


def padronizar_regiao(valor, id_pedido):
    """Padroniza região usando mapeamento de valores válidos."""
    original = valor.strip()
    if not original:
        return original

    chave = original.lower()
    novo = REGIOES_VALIDAS.get(chave, original.title())
    if novo != original:
        log(id_pedido, "Região", original, novo, "Padronizado casing da região")
    return novo


def padronizar_representante(valor, id_pedido):
    """Aplica Title Case ao nome do representante."""
    original = valor.strip()
    if not original:
        return original

    novo = original.title()
    if novo != original:
        log(id_pedido, "Representante", original, novo, "Padronizado para Title Case")
    return novo


def padronizar_status(valor, id_pedido):
    """Padroniza status: traduz inglês e aplica Title Case."""
    original = valor.strip()
    if not original:
        return original

    # Verifica se é status em inglês
    chave = original.lower()
    if chave in STATUS_TRADUCAO:
        novo = STATUS_TRADUCAO[chave]
        log(id_pedido, "Status", original, novo, "Traduzido de inglês para português")
        return novo

    # Aplica Title Case
    novo = original.title()
    if novo != original:
        log(id_pedido, "Status", original, novo, "Padronizado para Title Case")
    return novo


def padronizar_receita(valor, id_pedido):
    """Converte formato monetário para padrão brasileiro (R$ 4.320,00)."""
    original = valor.strip()
    if not original:
        return original

    # Extrai o valor numérico
    valor_limpo = original.replace("R$", "").strip()
    try:
        numero = float(valor_limpo)
    except ValueError:
        log(id_pedido, "Receita", original, original, "⚠️ Não foi possível converter — mantido")
        return original

    # Formata no padrão brasileiro: R$ 1.234,56
    parte_inteira = int(numero)
    parte_decimal = round((numero - parte_inteira) * 100)

    # Formata com separador de milhar (ponto)
    inteiro_formatado = f"{parte_inteira:,}".replace(",", ".")
    novo = f"R$ {inteiro_formatado},{parte_decimal:02d}"

    if novo != original:
        log(id_pedido, "Receita", original, novo, "Formatado para padrão monetário brasileiro")
    return novo


# ─────────────────────────────────────────────
# Processamento principal
# ─────────────────────────────────────────────

def processar():
    """Executa todas as etapas de limpeza."""
    print("=" * 60)
    print("  LIMPEZA DE DADOS — f_Vendas.csv")
    print("=" * 60)
    print()

    # Lê o arquivo original
    with open(ARQUIVO_ENTRADA, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        colunas = reader.fieldnames
        registros = list(reader)

    total_original = len(registros)
    print(f"📥 Registros lidos: {total_original}")

    # ──────────────────────────────────────
    # ETAPA 1: Corrigir status deslocado (ID 1007)
    # ──────────────────────────────────────
    print("\n[1/7] Corrigindo status deslocado para Observações...")
    for r in registros:
        status = r["Status"].strip()
        obs = r["Observações"].strip().lower()

        if not status and obs in ("fechado ganho", "fechado perdido", "closed won", "closed lost"):
            log(r["ID Pedido"], "Status", "(vazio)", obs, "Movido da coluna Observações para Status")
            log(r["ID Pedido"], "Observações", r["Observações"].strip(), "", "Valor movido para coluna Status")
            r["Status"] = obs
            r["Observações"] = ""

    # ──────────────────────────────────────
    # ETAPA 2: Remover duplicado confirmado (ID 1005)
    # ──────────────────────────────────────
    print("[2/7] Removendo duplicado confirmado (ID 1005)...")
    registros_limpos = []
    removidos = 0
    for r in registros:
        if r["ID Pedido"].strip() == "1005":
            log("1005", "(registro)", "presente", "REMOVIDO",
                "Duplicado exato confirmado de ID 1001 (mesmo cliente, data, receita, produto)")
            removidos += 1
            continue
        registros_limpos.append(r)
    registros = registros_limpos
    print(f"   → {removidos} registro(s) removido(s)")

    # ──────────────────────────────────────
    # ETAPA 3: Padronizar casing
    # ──────────────────────────────────────
    print("[3/7] Padronizando casing (Title Case)...")
    for r in registros:
        pid = r["ID Pedido"].strip()
        r["Nome do Cliente"] = padronizar_casing_nome(r["Nome do Cliente"], pid)
        r["Região"] = padronizar_regiao(r["Região"], pid)
        r["Representante"] = padronizar_representante(r["Representante"], pid)
        r["Status"] = padronizar_status(r["Status"], pid)

    # ──────────────────────────────────────
    # ETAPA 4: Padronizar datas
    # ──────────────────────────────────────
    print("[4/7] Unificando formato de datas para DD/MM/AAAA...")
    for r in registros:
        pid = r["ID Pedido"].strip()
        r["Data do Pedido"] = padronizar_data(r["Data do Pedido"], pid)

    # ──────────────────────────────────────
    # ETAPA 5: Padronizar receita
    # ──────────────────────────────────────
    print("[5/7] Formatando receita para padrão brasileiro...")
    for r in registros:
        pid = r["ID Pedido"].strip()
        r["Receita"] = padronizar_receita(r["Receita"], pid)

    # ──────────────────────────────────────
    # ETAPA 6: Limpar observações de metadados
    #          (remove "duplicado" do 1005 já removido,
    #           mantém observações informativas)
    # ──────────────────────────────────────
    print("[6/7] Limpando observações redundantes...")
    # Nenhuma ação adicional necessária — o registro 1005 já foi removido
    # e o status do 1007 já foi movido na etapa 1

    # ──────────────────────────────────────
    # ETAPA 7: Gravar arquivo limpo
    # ──────────────────────────────────────
    print("[7/7] Gravando arquivo limpo...")

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(registros)

    total_final = len(registros)
    print(f"\n📤 Registros gravados: {total_final}")
    print(f"📊 Diferença: {total_original - total_final} registro(s) removido(s)")
    print(f"📁 Arquivo salvo: {ARQUIVO_SAIDA}")

    # ──────────────────────────────────────
    # Gravar log de alterações
    # ──────────────────────────────────────
    with open(ARQUIVO_LOG, "w", encoding="utf-8") as f:
        f.write("LOG DE LIMPEZA — f_Vendas.csv\n")
        f.write(f"Data de execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Total de alterações: {len(log_alteracoes)}\n")
        f.write("=" * 80 + "\n\n")

        for i, entry in enumerate(log_alteracoes, 1):
            f.write(f"[{i:03d}] ID Pedido: {entry['id']}\n")
            f.write(f"      Coluna:  {entry['coluna']}\n")
            f.write(f"      Antes:   {entry['antes']}\n")
            f.write(f"      Depois:  {entry['depois']}\n")
            f.write(f"      Motivo:  {entry['motivo']}\n")
            f.write("-" * 80 + "\n")

    print(f"📝 Log salvo: {ARQUIVO_LOG}")
    print(f"   → {len(log_alteracoes)} alteração(ões) registrada(s)")

    # ──────────────────────────────────────
    # Resumo final
    # ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("  RESUMO DA LIMPEZA")
    print("=" * 60)

    categorias = {}
    for entry in log_alteracoes:
        categorias.setdefault(entry["motivo"], []).append(entry["id"])

    for motivo, ids in categorias.items():
        print(f"  • {motivo}: {len(ids)} registro(s)")

    print("\n✅ Limpeza concluída com sucesso!")

    # ──────────────────────────────────────
    # Alertas sobre valores que permanecem vazios
    # ──────────────────────────────────────
    print("\n⚠️  VALORES QUE PERMANECEM VAZIOS (requerem validação manual):")
    campos_criticos = ["Região", "Receita", "Representante", "Status"]
    tem_vazio = False
    for r in registros:
        for campo in campos_criticos:
            if not r[campo].strip():
                print(f"   → ID {r['ID Pedido'].strip()}: coluna '{campo}' continua vazia")
                tem_vazio = True
    if not tem_vazio:
        print("   Nenhum campo crítico vazio restante (exceto os já sinalizados no diagnóstico).")


if __name__ == "__main__":
    processar()
