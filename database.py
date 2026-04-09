import sqlite3

DB_PATH = "producao.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS caixas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fechada     INTEGER NOT NULL DEFAULT 0,
            criada_em   TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pecas (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            peso              REAL NOT NULL,
            cor               TEXT NOT NULL,
            comprimento       REAL NOT NULL,
            status            TEXT NOT NULL,
            motivo_reprovacao TEXT,
            caixa_id          INTEGER,
            registrada_em     TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (caixa_id) REFERENCES caixas(id)
        )
    """)

    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
# CAIXAS
# ──────────────────────────────────────────────

def criar_caixa():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO caixas (fechada) VALUES (0)")
    caixa_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return caixa_id


def fechar_caixa(caixa_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE caixas SET fechada = 1 WHERE id = ?", (caixa_id,))
    conn.commit()
    conn.close()


def obter_caixa_atual():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.id, COUNT(p.id) AS total
        FROM caixas c
        LEFT JOIN pecas p ON p.caixa_id = c.id
        WHERE c.fechada = 0
        GROUP BY c.id
        ORDER BY c.id ASC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return criar_caixa()

    caixa_id, total = row
    if total >= 10:
        fechar_caixa(caixa_id)
        return criar_caixa()

    return caixa_id


def contar_pecas_na_caixa(caixa_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pecas WHERE caixa_id = ?", (caixa_id,))
    total = cursor.fetchone()[0]
    conn.close()
    return total


# ──────────────────────────────────────────────
# PEÇAS
# ──────────────────────────────────────────────

def inserir_peca(peso, cor, comprimento, status, motivo, caixa_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pecas (peso, cor, comprimento, status, motivo_reprovacao, caixa_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (peso, cor, comprimento, status, motivo, caixa_id))
    peca_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return peca_id


def listar_pecas(filtro=None):
    conn = conectar()
    cursor = conn.cursor()
    if filtro:
        cursor.execute("""
            SELECT id, peso, cor, comprimento, status, motivo_reprovacao, caixa_id
            FROM pecas WHERE status = ? ORDER BY id
        """, (filtro,))
    else:
        cursor.execute("""
            SELECT id, peso, cor, comprimento, status, motivo_reprovacao, caixa_id
            FROM pecas ORDER BY id
        """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def reabrir_caixa(caixa_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE caixas SET fechada = 0 WHERE id = ?", (caixa_id,))
    conn.commit()
    conn.close()


def buscar_peca(peca_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, peso, cor, comprimento, status, motivo_reprovacao, caixa_id
        FROM pecas WHERE id = ?
    """, (peca_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def remover_peca(peca_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pecas WHERE id = ?", (peca_id,))
    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
# RELATÓRIO
# ──────────────────────────────────────────────

def obter_totais():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM pecas WHERE status = 'aprovada'")
    aprovadas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pecas WHERE status = 'reprovada'")
    reprovadas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM caixas")
    total_caixas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM caixas WHERE fechada = 1")
    caixas_fechadas = cursor.fetchone()[0]

    conn.close()
    return aprovadas, reprovadas, total_caixas, caixas_fechadas


def obter_reprovadas_com_motivo():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, peso, cor, comprimento, motivo_reprovacao
        FROM pecas
        WHERE status = 'reprovada'
        ORDER BY registrada_em
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def obter_caixas_detalhes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id,
               CASE WHEN c.fechada = 1 THEN 'Fechada' ELSE 'Aberta' END AS situacao,
               COUNT(p.id) AS total_pecas,
               c.criada_em
        FROM caixas c
        LEFT JOIN pecas p ON p.caixa_id = c.id
        GROUP BY c.id
        ORDER BY c.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def limpar_banco():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pecas")
    cursor.execute("DELETE FROM caixas")
    cursor.execute("DELETE FROM sqlite_sequence")
    conn.commit()
    conn.close()
