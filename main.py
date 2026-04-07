"""
=============================================================
  SISTEMA DE CONTROLE DE PRODUCAO E QUALIDADE
  Setor Industrial — Linha de Montagem
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


# ──────────────────────────────────────────────────────────────────
# HELPERS DE INTERFACE
# ──────────────────────────────────────────────────────────────────

def limpar_tela():
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except:
        pass


def cabecalho(titulo):
    print("\n" + "=" * 60)
    print(f"  {titulo}")
    print("=" * 60)


def pausar():
    input("\n  Pressione ENTER para continuar...")


# ──────────────────────────────────────────────────────────────────
# LÓGICA DE NEGÓCIO
# ──────────────────────────────────────────────────────────────────

def processar_peca(peso, cor, comprimento):
    status, motivos = qld.avaliar_peca(peso, cor, comprimento)
    motivo_formatado = " | ".join(motivos) if motivos else None
    caixa_id = None

    if status == "aprovada":
        caixa_id = db.obter_caixa_atual()
        peca_id  = db.inserir_peca(peso, cor, comprimento, status, motivo_formatado, caixa_id)
        if db.contar_pecas_na_caixa(caixa_id) >= 10:
            db.fechar_caixa(caixa_id)
            print(f"\n  📦 Caixa #{caixa_id} fechada — capacidade maxima atingida (10 pecas).")
    else:
        peca_id = db.inserir_peca(peso, cor, comprimento, status, motivo_formatado, caixa_id)

    return peca_id, status, motivo_formatado, caixa_id


def exibir_resultado_peca(peca_id, status, motivo, caixa_id):
    if status == "aprovada":
        print(f"\n  ✅ Peca #{peca_id} APROVADA → alocada na Caixa #{caixa_id}")
    else:
        print(f"\n  ❌ Peca #{peca_id} REPROVADA")
        for m in motivo.split(" | "):
            print(f"     • {m}")


# ──────────────────────────────────────────────────────────────────
# AÇÕES DO MENU
# ──────────────────────────────────────────────────────────────────

def cadastrar_pecas():
    cabecalho("CADASTRAR PECAS")
    print("  Digite 0 no peso para voltar ao menu.\n")

    aprovadas  = 0
    reprovadas = 0
    quantidade = ler_inteiro("  Quantas pecas deseja cadastrar? ", minimo=1, maximo=500)

    for i in range(1, quantidade + 1):
        print(f"\n  ── Peca {i}/{quantidade} ──────────────────────────")

        peso        = ler_float("  Peso (gramas)        : ")
        cor         = ler_texto("  Cor (azul/verde/...) : ")
        comprimento = ler_float("  Comprimento (cm)     : ")

        peca_id, status, motivo, caixa_id = processar_peca(peso, cor, comprimento)
        exibir_resultado_peca(peca_id, status, motivo, caixa_id)

        if status == "aprovada":
            aprovadas += 1
        else:
            reprovadas += 1

    print(f"\n  ─── Lote concluido ───────────────────────────────")
    print(f"  ✅ Aprovadas  : {aprovadas}")
    print(f"  ❌ Reprovadas : {reprovadas}")
    rel.exibir_relatorio_resumido()
    pausar()


def ver_relatorio():
    cabecalho("RELATORIO CONSOLIDADO")
    rel.exibir_relatorio_completo()
    pausar()


def listar_reprovadas():
    cabecalho("PECAS REPROVADAS")
    rel.listar_reprovadas()
    pausar()


def listar_caixas():
    cabecalho("CAIXAS DE ARMAZENAMENTO")
    rel.listar_caixas()
    pausar()


def resetar_sistema():
    cabecalho("RESETAR SISTEMA")
    print("\n  ⚠  ATENCAO: Esta acao apagara TODOS os dados do sistema.")

    if ler_confirmacao("\n  Confirma o reset completo?"):
        db.limpar_banco()
        print("\n  ✅ Sistema resetado com sucesso. Banco de dados limpo.")
    else:
        print("\n  Operacao cancelada.")
    pausar()


# ──────────────────────────────────────────────────────────────────
# MENU PRINCIPAL
# ──────────────────────────────────────────────────────────────────

def menu_principal():
    opcoes = {"1", "2", "3", "4", "5", "0"}

    while True:
        limpar_tela()
        print("""
╔══════════════════════════════════════════════════════════╗
║       SISTEMA DE CONTROLE DE PRODUCAO E QUALIDADE        ║
║              Linha de Montagem Industrial                 ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   1 │ Cadastrar pecas                                    ║
║   2 │ Listar pecas reprovadas                            ║
║   3 │ Listar caixas de armazenamento                     ║
║   4 │ Gerar relatorio consolidado                        ║
║   5 │ Resetar sistema (apagar todos os dados)            ║
║   0 │ Sair                                               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝""")

        escolha = ler_opcao_menu(opcoes)

        if escolha == "1":
            cadastrar_pecas()
        elif escolha == "2":
            listar_reprovadas()
        elif escolha == "3":
            listar_caixas()
        elif escolha == "4":
            ver_relatorio()
        elif escolha == "5":
            resetar_sistema()
        elif escolha == "0":
            limpar_tela()
            print("\n  Sistema encerrado. Ate logo!\n")
            break


# ──────────────────────────────────────────────────────────────────
# PONTO DE ENTRADA
# ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    db.inicializar_banco()
    menu_principal()
