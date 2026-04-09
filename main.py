"""
=============================================================
  SISTEMA DE CONTROLE DE PRODUCAO E QUALIDADE
  Setor Industrial - Linha de Montagem
=============================================================
  Execucao: python main.py
=============================================================
"""

import os

import database as db
import qualidade as qld
import relatorio as rel
from entrada import (
    ler_texto,
    ler_float,
    ler_inteiro,
    ler_confirmacao,
    ler_opcao_menu,
)


def limpar_tela():
    print("\n" * 5)


def cabecalho(titulo):
    print("\n" + "=" * 60)
    print(f"  {titulo}")
    print("=" * 60)


def pausar():
    input("\n  Pressione ENTER para continuar...")


def processar_peca(peso, cor, comprimento):
    status, motivos = qld.avaliar_peca(peso, cor, comprimento)
    motivo_formatado = " | ".join(motivos) if motivos else None
    caixa_id = None

    if status == "aprovada":
        caixa_id = db.obter_caixa_atual()
        peca_id  = db.inserir_peca(peso, cor, comprimento, status, motivo_formatado, caixa_id)
        if db.contar_pecas_na_caixa(caixa_id) >= 10:
            db.fechar_caixa(caixa_id)
            print(f"\n  Caixa #{caixa_id} fechada - capacidade maxima atingida (10 pecas).")
    else:
        peca_id = db.inserir_peca(peso, cor, comprimento, status, motivo_formatado, caixa_id)

    return peca_id, status, motivo_formatado, caixa_id


def exibir_resultado_peca(peca_id, status, motivo, caixa_id):
    if status == "aprovada":
        print(f"\n  Peca #{peca_id} APROVADA - alocada na Caixa #{caixa_id}")
    else:
        print(f"\n  Peca #{peca_id} REPROVADA")
        for m in motivo.split(" | "):
            print(f"     - {m}")


# ──────────────────────────────────────────────────────────────────
# 1. CADASTRAR NOVA PECA
# ──────────────────────────────────────────────────────────────────

def cadastrar_pecas():
    cabecalho("CADASTRAR NOVA PECA")
    print("  Digite 0 no peso para voltar ao menu.\n")

    aprovadas  = 0
    reprovadas = 0
    quantidade = ler_inteiro("  Quantas pecas deseja cadastrar? ", minimo=1, maximo=500)

    for i in range(1, quantidade + 1):
        print(f"\n  -- Peca {i}/{quantidade} ------------------------------------------")

        peso        = ler_float("  Peso (gramas)        : ")
        cor         = ler_texto("  Cor (azul/verde/...) : ")
        comprimento = ler_float("  Comprimento (cm)     : ")

        peca_id, status, motivo, caixa_id = processar_peca(peso, cor, comprimento)
        exibir_resultado_peca(peca_id, status, motivo, caixa_id)

        if status == "aprovada":
            aprovadas += 1
        else:
            reprovadas += 1

    print(f"\n  --- Lote concluido ---")
    print(f"  Aprovadas  : {aprovadas}")
    print(f"  Reprovadas : {reprovadas}")
    rel.exibir_relatorio_resumido()
    pausar()


# ──────────────────────────────────────────────────────────────────
# 2. LISTAR PECAS APROVADAS / REPROVADAS
# ──────────────────────────────────────────────────────────────────

def listar_pecas():
    cabecalho("LISTAR PECAS")
    print("\n  1 - Todas as pecas")
    print("  2 - Somente aprovadas")
    print("  3 - Somente reprovadas")

    opcao = ler_opcao_menu({"1", "2", "3"})

    if opcao == "1":
        pecas = db.listar_pecas()
        titulo = "TODAS AS PECAS"
    elif opcao == "2":
        pecas = db.listar_pecas(filtro="aprovada")
        titulo = "PECAS APROVADAS"
    else:
        pecas = db.listar_pecas(filtro="reprovada")
        titulo = "PECAS REPROVADAS"

    cabecalho(titulo)

    if not pecas:
        print("\n  Nenhuma peca encontrada.")
        pausar()
        return

    print(f"\n  Total: {len(pecas)} peca(s)\n")
    print(f"  {'ID':<6} {'Peso':>7} {'Cor':<10} {'Comp':>7} {'Status':<12} {'Caixa'}")
    print(f"  {'-'*5} {'-'*7} {'-'*9} {'-'*7} {'-'*11} {'-'*5}")

    for peca in pecas:
        id_, peso, cor, comp, status, motivo, caixa_id = peca
        caixa_str = f"#{caixa_id}" if caixa_id else "-"
        print(f"  {id_:<6} {peso:>6}g  {cor:<10} {comp:>6}cm  {status:<12} {caixa_str}")
        if motivo:
            for m in motivo.split(" | "):
                print(f"         -> {m}")

    pausar()


# ──────────────────────────────────────────────────────────────────
# 3. REMOVER PECA
# ──────────────────────────────────────────────────────────────────

def remover_peca():
    cabecalho("REMOVER PECA CADASTRADA")

    try:
        peca_id = int(input("  Digite o ID da peca que deseja remover: ").strip())
    except ValueError:
        print("  Aviso: ID invalido. Digite um numero inteiro.")
        pausar()
        return

    peca = db.buscar_peca(peca_id)

    if not peca:
        print(f"\n  Aviso: Peca com ID {peca_id} nao encontrada.")
        pausar()
        return

    id_, peso, cor, comp, status, motivo, caixa_id = peca
    print(f"\n  ID          : {id_}")
    print(f"  Dados       : peso={peso}g | cor={cor} | comprimento={comp}cm")
    print(f"  Status      : {status}")
    if caixa_id:
        print(f"  Caixa       : #{caixa_id}")
    if motivo:
        print(f"  Motivo      : {motivo}")

    if ler_confirmacao("\n  Confirma a remocao desta peca?"):
        db.remover_peca(peca_id)
        if status == "aprovada" and caixa_id:
            db.reabrir_caixa(caixa_id)
            print(f"\n  Peca #{peca_id} removida com sucesso.")
            print(f"  Caixa #{caixa_id} reaberta - agora aceita novas pecas.")
        else:
            print(f"\n  Peca #{peca_id} removida com sucesso.")
    else:
        print("\n  Operacao cancelada.")
    pausar()


# ──────────────────────────────────────────────────────────────────
# 4. LISTAR CAIXAS FECHADAS
# ──────────────────────────────────────────────────────────────────

def listar_caixas():
    cabecalho("CAIXAS DE ARMAZENAMENTO")
    rel.listar_caixas()
    pausar()


# ──────────────────────────────────────────────────────────────────
# 5. RELATORIO FINAL
# ──────────────────────────────────────────────────────────────────

def ver_relatorio():
    cabecalho("RELATORIO FINAL")
    rel.exibir_relatorio_completo()
    pausar()


# ──────────────────────────────────────────────────────────────────
# MENU PRINCIPAL
# ──────────────────────────────────────────────────────────────────

def menu_principal():
    opcoes = {"1", "2", "3", "4", "5", "6", "0"}

    while True:
        limpar_tela()
        print("""
╔══════════════════════════════════════════════════════════╗
║       SISTEMA DE CONTROLE DE PRODUCAO E QUALIDADE        ║
║              Linha de Montagem Industrial                 ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   1 | Cadastrar nova peca                                ║
║   2 | Listar pecas aprovadas/reprovadas                  ║
║   3 | Remover peca cadastrada                            ║
║   4 | Listar caixas                                      ║
║   5 | Gerar relatorio final                              ║
║   6 | Resetar sistema (apagar todos os dados)            ║
║   0 | Sair                                               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝""")

        escolha = ler_opcao_menu(opcoes)

        if escolha == "1":
            cadastrar_pecas()
        elif escolha == "2":
            listar_pecas()
        elif escolha == "3":
            remover_peca()
        elif escolha == "4":
            listar_caixas()
        elif escolha == "5":
            ver_relatorio()
        elif escolha == "6":
            if ler_confirmacao("\n  Confirma o reset completo? Todos os dados serao apagados"):
                db.limpar_banco()
                print("\n  Sistema resetado com sucesso.")
            pausar()
        elif escolha == "0":
            limpar_tela()
            print("\n  Sistema encerrado. Ate logo!\n")
            break


if __name__ == "__main__":
    db.inicializar_banco()
    menu_principal()
