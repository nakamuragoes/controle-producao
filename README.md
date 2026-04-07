# 🏭 Sistema de Controle de Produção e Qualidade

Sistema desenvolvido em Python para automatizar o controle de produção e inspeção de qualidade de peças em uma linha de montagem industrial. O programa avalia automaticamente cada peça cadastrada, aloca as aprovadas em caixas e gera relatórios consolidados.

---

## 📋 Funcionalidades

- Cadastro de peças com avaliação automática de qualidade
- Aprovação ou reprovação com base em critérios pré-definidos
- Armazenamento das peças aprovadas em caixas (limite de 10 peças por caixa)
- Fechamento automático da caixa ao atingir a capacidade máxima
- Listagem de peças reprovadas com o motivo de cada reprovação
- Listagem de caixas com status e ocupação
- Relatório consolidado com totais e taxa de aprovação
- Reset do sistema para iniciar um novo lote

---

## ✅ Critérios de Qualidade

Uma peça é **aprovada** somente se atender aos três critérios simultaneamente:

| Critério      | Condição                        |
|---------------|---------------------------------|
| Peso          | Entre **95g** e **105g**        |
| Cor           | **Azul** ou **Verde**           |
| Comprimento   | Entre **10cm** e **20cm**       |

Se qualquer critério não for atendido, a peça é **reprovada** e o motivo é registrado.

---

## 🗂️ Estrutura do Projeto

```
controle-producao/
├── main.py          # Menu principal e orquestração do sistema
├── database.py      # Comunicação com o banco de dados SQLite
├── qualidade.py     # Regras de avaliação de qualidade
├── relatorio.py     # Geração e exibição de relatórios
└── entrada.py       # Leitura e validação de inputs do usuário
```

---

## 🚀 Como Rodar

### Pré-requisitos

- Python 3.6 ou superior instalado
- Nenhuma biblioteca externa necessária — o projeto usa apenas módulos nativos do Python

### Verificar se o Python está instalado

```bash
python3 --version
```

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/nakamuragoes/controle-producao.git
```

**2. Entre na pasta do projeto**
```bash
cd controle-producao
```

**3. Execute o programa**
```bash
python3 main.py
```

O banco de dados `producao.db` será criado automaticamente na primeira execução.

---

## 🖥️ Menu do Sistema

```
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
╚══════════════════════════════════════════════════════════╝
```

---

## 📌 Exemplos de Uso

### Cadastrando peças

Ao escolher a opção **1**, o sistema pede a quantidade de peças e entra em modo de cadastro:

```
Quantas pecas deseja cadastrar? 3

── Peca 1/3 ──────────────────────────
  Peso (gramas)        : 100
  Cor (azul/verde/...) : azul
  Comprimento (cm)     : 15

  ✅ Peca #1 APROVADA → alocada na Caixa #1

── Peca 2/3 ──────────────────────────
  Peso (gramas)        : 90
  Cor (azul/verde/...) : azul
  Comprimento (cm)     : 15

  ❌ Peca #2 REPROVADA
     • Peso fora do intervalo (90.0g — esperado: 95.0g a 105.0g)

── Peca 3/3 ──────────────────────────
  Peso (gramas)        : 80
  Cor (azul/verde/...) : amarelo
  Comprimento (cm)     : 30

  ❌ Peca #3 REPROVADA
     • Peso fora do intervalo (80.0g — esperado: 95.0g a 105.0g)
     • Cor invalida ('amarelo' — aceitas: azul ou verde)
     • Comprimento fora do intervalo (30.0cm — esperado: 10.0cm a 20.0cm)

  Lote concluido
  ✅ Aprovadas  : 1
  ❌ Reprovadas : 2
```

---

### Listando peças reprovadas

Ao escolher a opção **2**:

```
============================================================
         PECAS REPROVADAS
============================================================
  Total: 2 peca(s) reprovada(s)

  ID          : 2
  Dados       : peso=90.0g | cor=azul | comprimento=15.0cm
  Motivo      : Peso fora do intervalo (90.0g — esperado: 95.0g a 105.0g)
  ------------------------------------------------------
  ID          : 3
  Dados       : peso=80.0g | cor=amarelo | comprimento=30.0cm
  Motivo      : Peso fora do intervalo (80.0g — esperado: 95.0g a 105.0g)
                Cor invalida ('amarelo' — aceitas: azul ou verde)
                Comprimento fora do intervalo (30.0cm — esperado: 10.0cm a 20.0cm)
  ------------------------------------------------------
```

---

### Listando caixas

Ao escolher a opção **3**:

```
============================================================
         CAIXAS DE ARMAZENAMENTO
============================================================
  Caixa    Situacao      Pecas  Ocupacao
  ------- ----------- ------  ------------
  📦 #1    Aberta        1/10  [█░░░░░░░░░]

  Total de caixas  : 1
  🔒 Fechadas      : 0
  📦 Abertas       : 1
  Pecas armazenadas: 1
```

---

### Relatório consolidado

Ao escolher a opção **4**:

```
============================================================
         RELATORIO CONSOLIDADO DE PRODUCAO
============================================================

❌ PECAS REPROVADAS — DETALHAMENTO
------------------------------------------------------------
  ID          : 2
  Dados       : peso=90.0g | cor=azul | comprimento=15.0cm
  Motivo      : Peso fora do intervalo (90.0g — esperado: 95.0g a 105.0g)

------------------------------------------------------------
📊 RESUMO GERAL
------------------------------------------------------------
  Total de pecas registradas : 3
  ✅ Aprovadas               : 1
  ❌ Reprovadas              : 2
  📈 Taxa de aprovacao       : 33.3%

📦 CAIXAS
------------------------------------------------------------
  Total de caixas criadas    : 1
  Caixas fechadas (cheias)   : 0
  Caixas abertas (em uso)    : 1

  Caixa    Situacao      Pecas  Ocupacao
  ------- ----------- ------  ------------
  #1       Aberta        1/10  [█░░░░░░░░░]
```

---

## 🗄️ Banco de Dados

O sistema utiliza **SQLite** — banco de dados nativo do Python, sem necessidade de instalação. O arquivo `producao.db` é criado automaticamente na primeira execução com duas tabelas:

- **`pecas`** — armazena todas as peças cadastradas com seus dados e status
- **`caixas`** — controla o ciclo de vida de cada caixa (aberta/fechada)

---

## 👨‍💻 Tecnologias

- Python 3
- SQLite3 (nativo do Python)

---

## 📄 Licença

Projeto desenvolvido para fins acadêmicos.
