PESO_MIN        = 95.0
PESO_MAX        = 105.0
CORES_VALIDAS   = {"azul", "verde"}
COMP_MIN        = 10.0
COMP_MAX        = 20.0


def avaliar_peca(peso, cor, comprimento):
    motivos = []

    if not (PESO_MIN <= peso <= PESO_MAX):
        motivos.append(
            f"Peso fora do intervalo ({peso}g — esperado: {PESO_MIN}g a {PESO_MAX}g)"
        )

    if cor.lower().strip() not in CORES_VALIDAS:
        cores_str = " ou ".join(sorted(CORES_VALIDAS))
        motivos.append(
            f"Cor invalida ('{cor}' — aceitas: {cores_str})"
        )

    if not (COMP_MIN <= comprimento <= COMP_MAX):
        motivos.append(
            f"Comprimento fora do intervalo ({comprimento}cm — esperado: {COMP_MIN}cm a {COMP_MAX}cm)"
        )

    status = "reprovada" if motivos else "aprovada"
    return status, motivos
