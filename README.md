# ChargeGrid Intelligence

Agente de IA para o EV Challenge GoodWe/FIAP, focado em gerenciamento comercial de recarga veicular.

O projeto usa:

- LangChain para o fluxo conversacional;
- Google Gemini como modelo real de IA;
- memória por sessão;
- guardrails básicos contra prompt injection e orientação elétrica perigosa.

## Executar no Google Colab

Instale o projeto direto do GitHub:

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

while True:
    pergunta = input("Usuário: ")
    if pergunta.lower() in {"sair", "exit", "quit"}:
        break

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
