# ChargeGrid Intelligence

Agente de IA para o EV Challenge GoodWe/FIAP, focado em gerenciamento comercial de recarga veicular.

O projeto usa:

- LangGraph para fluxo de agente;
- Google Gemini API como modelo real de IA;
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
```

Configure a chave do Gemini:

```python
import os
from getpass import getpass

os.environ["GEMINI_API_KEY"] = getpass("GEMINI_API_KEY: ")
os.environ["GEMINI_MODEL"] = "gemini-2.5-flash"
```

Use o agente:

```python
from chargegrid_intelligence import ChargeGridAgent

agent = ChargeGridAgent()

pergunta = input("Usuário: ")
resposta = agent.ask(pergunta, session_id="demo")
print("ChargeGrid:", resposta["answer"])
```

## Executar localmente

Crie um arquivo `.env` baseado em `.env.example`:

```env
GEMINI_API_KEY=sua-chave-aqui
GEMINI_MODEL=gemini-2.5-flash
```

Instale e rode:

```bash
pip install -r requirements.txt
python -m chargegrid_intelligence.cli --session demo
```

## Estrutura principal

```text
chargegrid_intelligence/
├── agent.py
├── cli.py
├── guardrails.py
├── knowledge.py
├── memory.py
└── models.py
```

Arquivos das sprints anteriores foram mantidos em `colab/`, `docs/` e `assets/`.
