def ler_texto(prompt, max_len=50):
    while True:
        valor = input(prompt).strip()
        if not valor:
            print("  ⚠  Campo obrigatorio. Digite um valor.")
            continue
        if len(valor) > max_len:
            print(f"  ⚠  Maximo de {max_len} caracteres.")
            continue
        return valor


def ler_float(prompt):
    while True:
        entrada = input(prompt).strip().replace(",", ".")
        try:
            return float(entrada)
        except ValueError:
            print("  ⚠  Digite um numero valido (ex: 98.5).")


def ler_inteiro(prompt, minimo=1, maximo=999):
    while True:
        entrada = input(prompt).strip()
        try:
            valor = int(entrada)
        except ValueError:
            print("  ⚠  Digite um numero inteiro valido.")
            continue
        if not (minimo <= valor <= maximo):
            print(f"  ⚠  Valor deve estar entre {minimo} e {maximo}.")
            continue
        return valor


def ler_confirmacao(prompt):
    while True:
        resposta = input(prompt + " [s/n]: ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("  ⚠  Digite 's' para sim ou 'n' para nao.")


def ler_opcao_menu(opcoes_validas):
    while True:
        escolha = input("\n  Escolha uma opcao: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print(f"  ⚠  Opcao invalida. Escolha entre: {', '.join(sorted(opcoes_validas))}")
