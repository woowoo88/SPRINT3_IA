# ChargeGrid Intelligence

Agente de IA para o EV Challenge GoodWe/FIAP, focado em gerenciamento comercial de recarga veicular.

O projeto usa:

- LangGraph para fluxo de agente;
- OpenAI API como modelo real de IA;
- memória por sessão;
- guardrails básicos contra prompt injection e orientação elétrica perigosa.

## Integrantes

| Nome | RM |
|---|---|
| Mateus de Oliveira Fernandes Neves | RM 572431 |
| Pedro Soares de Souza | RM 571285 |
| Paulo Henrique Lira Bilac de Araujo | RM 569496 |
| Olavo Dadario Vianna Barreto | RM 569272 |
| Angela Sousa Takezawa | RM 570797 |

## Executar no Google Colab

```python
%cd /content
!rm -rf SPRINT3_IA
%pip uninstall -y chargegrid-intelligence

!git clone https://github.com/woowoo88/SPRINT3_IA.git
%cd SPRINT3_IA

%pip install -q -r requirements.txt
%pip install -q --no-deps -e .
```

Configure a chave da OpenAI:

```python
import os
from getpass import getpass

os.environ["OPENAI_API_KEY"] = getpass("OPENAI_API_KEY: ")
os.environ["OPENAI_MODEL"] = "gpt-4o-mini"
```

Use o agente:

```python
from chargegrid_intelligence import ChargeGridAgent

agent = ChargeGridAgent()

perguntas = [
    "Estou usando o eletroposto Campus FIAP Paulista.",
    "Existem 12 vagas de recarga nesse local.",
    "Como vejo o status dos conectores?",
    "Faça um relatório operacional resumido.",
    "Como funciona o pagamento?",
    "Explique OCPP e MODBUS no projeto.",
    "E se um conector apresentar falha?",
    "Posso estacionar na vaga 12? Tem alguém estacionado?",
]

for pergunta in perguntas:
    print("Usuário:", pergunta)
    print("ChargeGrid:", agent.ask(pergunta, session_id="demo")["answer"])
    print()
```

## Executar localmente

Crie um arquivo `.env` baseado em `.env.example`:

```env
OPENAI_API_KEY=sua-chave-aqui
OPENAI_MODEL=gpt-4o-mini
```

Instale e rode:

```bash
pip install -r requirements.txt
pip install -e .
python -m chargegrid_intelligence.cli --session demo
```

## Estrutura principal

```text
src/chargegrid_intelligence/
├── agent.py
├── cli.py
├── guardrails.py
├── knowledge.py
├── memory.py
└── models.py
```

Arquivos das sprints anteriores foram mantidos em `colab/`, `docs/` e `assets/`.
