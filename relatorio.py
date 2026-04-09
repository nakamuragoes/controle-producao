from database import (
    obter_totais,
    obter_reprovadas_com_motivo,
    obter_caixas_detalhes,
)

LINHA    = "=" * 60
SUBLINHA = "-" * 60


def exibir_relatorio_completo():
    aprovadas, reprovadas, total_caixas, caixas_fechadas = obter_totais()
    total_pecas = aprovadas + reprovadas

    print(f"\n{LINHA}")
    print("         RELATORIO CONSOLIDADO DE PRODUCAO")
    print(LINHA)

    # 1. Pecas reprovadas
    print(f"\n❌ PECAS REPROVADAS — DETALHAMENTO")
    print(SUBLINHA)
    reprovadas_lista = obter_reprovadas_com_motivo()

    if not reprovadas_lista:
        print("  Nenhuma peca reprovada ate o momento.")
    else:
        for peca_id, peso, cor, comprimento, motivo in reprovadas_lista:
            print(f"\n  ID          : {peca_id}")
            print(f"  Dados       : peso={peso}g | cor={cor} | comprimento={comprimento}cm")
            motivos = motivo.split(" | ")
            for i, m in enumerate(motivos):
                label = "  Motivo     :" if i == 0 else "              "
                print(f"{label} {m}")

    # 2. Resumo geral
    print(f"\n{SUBLINHA}")
    print("📊 RESUMO GERAL")
    print(SUBLINHA)
    print(f"  Total de pecas registradas : {total_pecas}")
    print(f"  ✅ Aprovadas               : {aprovadas}")
    print(f"  ❌ Reprovadas              : {reprovadas}")
    taxa = (aprovadas / total_pecas * 100) if total_pecas > 0 else 0
    print(f"  📈 Taxa de aprovacao       : {taxa:.1f}%")

    # 3. Caixas
    print(f"\n📦 CAIXAS")
    print(SUBLINHA)
    print(f"  Total de caixas criadas    : {total_caixas}")
    print(f"  Caixas fechadas (cheias)   : {caixas_fechadas}")
    print(f"  Caixas abertas (em uso)    : {total_caixas - caixas_fechadas}")

    detalhes = obter_caixas_detalhes()
    if detalhes:
        print(f"\n  {'Caixa':<8} {'Situacao':<12} {'Pecas':>6}  Ocupacao")
        print(f"  {'-'*7} {'-'*11} {'-'*6}  {'-'*12}")
        for caixa_id, situacao, total, criada_em in detalhes:
            barra = "[" + "█" * total + "░" * (10 - total) + "]"
            print(f"  #{caixa_id:<7} {situacao:<12} {total:>4}/10  {barra}")

    print(f"\n{LINHA}\n")


def listar_reprovadas():
    print(f"\n{LINHA}")
    print("         PECAS REPROVADAS")
    print(LINHA)

    reprovadas_lista = obter_reprovadas_com_motivo()

    if not reprovadas_lista:
        print("\n  Nenhuma peca reprovada ate o momento.")
    else:
        print(f"  Total: {len(reprovadas_lista)} peca(s) reprovada(s)\n")
        for peca_id, peso, cor, comprimento, motivo in reprovadas_lista:
            print(f"  ID          : {peca_id}")
            print(f"  Dados       : peso={peso}g | cor={cor} | comprimento={comprimento}cm")
            motivos = motivo.split(" | ")
            for i, m in enumerate(motivos):
                label = "  Motivo     :" if i == 0 else "              "
                print(f"{label} {m}")
            print(f"  {'-' * 54}")

    print(f"\n{LINHA}\n")


def listar_caixas():
    print(f"\n{LINHA}")
    print("         CAIXAS DE ARMAZENAMENTO")
    print(LINHA)

    detalhes = obter_caixas_detalhes()

    if not detalhes:
        print("\n  Nenhuma caixa criada ainda.")
    else:
        print(f"\n  {'Caixa':<8} {'Situacao':<12} {'Pecas':>6}  Ocupacao            Faltam")
        print(f"  {'-'*7} {'-'*11} {'-'*6}  {'-'*20}  {'-'*6}")

        for caixa_id, situacao, total, criada_em in detalhes:
            icone  = "[F]" if situacao == "Fechada" else "[A]"
            barra  = "#" * total + "." * (10 - total)
            faltam = "-" if situacao == "Fechada" else str(10 - total)
            print(f"  {icone} #{caixa_id:<6} {situacao:<12} {total:>4}/10  [{barra}]  {faltam}")

        total_caixas    = len(detalhes)
        fechadas        = sum(1 for _, s, _, _ in detalhes if s == "Fechada")
        total_aprovadas = sum(t for _, _, t, _ in detalhes)

        print(f"\n  {'-' * 54}")
        print(f"  Total de caixas  : {total_caixas}")
        print(f"  Fechadas         : {fechadas}")
        print(f"  Abertas          : {total_caixas - fechadas}")
        print(f"  Pecas armazenadas: {total_aprovadas}")

    print(f"\n{LINHA}\n")


def exibir_relatorio_resumido():
    aprovadas, reprovadas, total_caixas, _ = obter_totais()
    total = aprovadas + reprovadas
    taxa = (aprovadas / total * 100) if total > 0 else 0
    print(f"\n  [Resumo] Total: {total} | "
          f"✅ {aprovadas} aprovadas | "
          f"❌ {reprovadas} reprovadas | "
          f"📦 {total_caixas} caixa(s) | "
          f"Taxa: {taxa:.1f}%")
