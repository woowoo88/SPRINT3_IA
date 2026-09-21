# ChargeGrid Intelligence

Agente de IA para o EV Challenge GoodWe/FIAP, focado em gerenciamento comercial de recarga veicular.

O projeto usa:

- LangChain para o fluxo conversacional;
- Google Gemini como modelo real de IA;
- memória por sessão;
- agente guardião de escopo para bloquear perguntas fora do contexto ChargeGrid;
- guardrails básicos contra prompt injection e orientação elétrica perigosa.

## Agentes da aplicação

A aplicação possui dois agentes:

- `ChargeGridAgent`: agente principal, responsável por conversar com o usuário, manter memória da sessão e consultar o Gemini via LangChain.
- `ScopeGuardAgent`: agente guardião, responsável por avaliar a pergunta antes da chamada ao modelo e bloquear temas fora do ChargeGrid Intelligence.

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

os.environ.pop("GEMINI_API_KEY", None)
os.environ["GOOGLE_API_KEY"] = getpass("Cole sua chave Gemini: ")
os.environ["GEMINI_MODEL"] = "gemini-3.6-flash"
```

Use o agente em modo conversa contínua:

```python
!python chat_colab.py
```

Se preferir, execute direto em uma célula:

```python
from chargegrid_intelligence import ChargeGridAgent

agent = ChargeGridAgent()

while True:
    pergunta = input("Usuário: ")
    if pergunta.lower() in {"sair", "exit", "quit"}:
        print("ChargeGrid: sessão encerrada.")
        break

    resposta = agent.ask(pergunta, session_id="demo")
    print("ChargeGrid:", resposta["answer"])
    print()
```

Você pode fazer quantas perguntas quiser na mesma execução. Para encerrar, digite `sair`.

## Executar localmente

Crie um arquivo `.env` baseado em `.env.example`:

```env
GOOGLE_API_KEY=sua-chave-aqui
GEMINI_MODEL=gemini-3.6-flash
```

Instale e rode:

```bash
pip install -r requirements.txt
python chat_colab.py
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
chat_colab.py
```
