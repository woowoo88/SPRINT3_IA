# ChargeWise AI

Assistente inteligente especializado em carregadores veiculares GoodWe, mobilidade elétrica e infraestrutura de recarga.

Projeto desenvolvido para o EV Challenge 2026 — GoodWe em parceria com a FIAP.

---

# Sprint 03 - ChargeGrid Intelligence

Na Sprint 03, o projeto evoluiu para o **ChargeGrid Intelligence**, uma arquitetura baseada em agentes para gerenciamento automatizado de infraestrutura comercial de recarga.

A nova versao foca em:

- controle de demanda em eletropostos comerciais;
- registro do ciclo de sessao de recarga;
- integracao conceitual com OCPP e MODBUS;
- politicas de cobranca dinamica;
- memoria por sessao;
- guardrails contra prompt injection, alucinacoes tecnicas e orientacoes inseguras.

O nucleo conversacional foi refatorado com **LangGraph**, separando o fluxo em nos de guardrails, memoria, contexto e resposta. Isso torna o comportamento mais testavel e mais facil de evoluir.

## Como executar a Sprint 03

```bash
pip install -r requirements.txt
pip install -e .
python -m chargegrid_intelligence.cli --model openai --session demo
```

Para rodar os testes automatizados:

```bash
python -m pytest -q
```

## Como executar no Google Colab

Use `%pip` no Colab, porque ele instala as dependências no mesmo kernel que executa o notebook.

```python
!git clone https://github.com/woowoo88/SPRINT3_IA.git
%cd SPRINT3_IA

%pip install -q -r requirements.txt
%pip install -q --no-deps -e .
```

Configure sua chave da OpenAI no Colab:

```python
import os
from getpass import getpass

os.environ["OPENAI_API_KEY"] = getpass("OPENAI_API_KEY: ")
os.environ["OPENAI_MODEL"] = "gpt-4o-mini"
```

Depois, execute o agente com modelo real:

```python
from chargegrid_intelligence import ChargeGridAgent

agent = ChargeGridAgent()

for pergunta in [
    "Estou usando o eletroposto Campus FIAP Paulista.",
    "Existem 12 vagas de recarga nesse local.",
    "Como vejo o status dos conectores?",
    "Faça um relatório operacional resumido.",
    "Como funciona o pagamento?",
    "Explique OCPP e MODBUS no projeto.",
    "E se um conector apresentar falha?",
]:
    print("Usuário:", pergunta)
    print("ChargeGrid:", agent.ask(pergunta, session_id="demo")["answer"])
    print()
```

Se o Colab ainda mostrar `ModuleNotFoundError`, rode esta célula antes do import:

```python
import sys
sys.path.insert(0, "/content/SPRINT3_IA/src")
```

Se você já tinha clonado uma versão anterior no Colab, rode uma instalação limpa:

```python
%cd /content
!rm -rf SPRINT3_IA
%pip uninstall -y chargegrid-intelligence
!git clone https://github.com/woowoo88/SPRINT3_IA.git
%cd SPRINT3_IA
%pip install -q -r requirements.txt
%pip install -q --no-deps -e .
```

Se o Colab continuar mostrando respostas antigas, use `Ambiente de execução > Reiniciar sessão` e rode as células novamente.

Observação: os testes de resposta real usam `OPENAI_API_KEY`. Sem a chave, esses testes são ignorados; os testes de guardrails continuam rodando.

Documentos principais da Sprint 03:

- `docs/relatorio_modelos.md`
- `docs/casos_teste_sprint03.md`
- `docs/relatorio_evolucao.md`
- `output/pdf/relatorio_evolucao_chargegrid.pdf`

---

# Integrantes

| Nome | RM |
|---|---|
| Mateus de Oliveira Fernandes Neves | RM 572431 |
| Pedro Soares de Souza | RM 571285 |
| Paulo Henrique Lira Bilac de Araujo | RM 569496 |
| Olavo Dadario Vianna Barreto | RM 569272 |
| Angela Sousa Takezawa | RM 570797 |

---

# Sobre o Projeto

O ChargeWise AI é um chatbot inteligente desenvolvido para auxiliar usuários, síndicos, administradores de condomínio, operadores e profissionais da área elétrica com informações relacionadas a carregadores veiculares, infraestrutura de recarga e soluções GoodWe.

Durante a Sprint 2 foram implementadas técnicas de Inteligência Artificial Generativa para tornar as respostas mais contextualizadas, coerentes e alinhadas ao cenário do EV Challenge 2026.

O sistema utiliza o modelo Llama 3.2 1B executado localmente através do Ollama, permitindo interações em linguagem natural e respostas especializadas no contexto de mobilidade elétrica.

- Link para o vídeo com funicionamento e testes: [ChargeWise-AI](https://youtu.be/Utbi84uknSo)

---

# Problema Abordado

Com o crescimento da adoção de veículos elétricos, surgem desafios relacionados à instalação, gerenciamento e utilização de carregadores veiculares.

Entre os principais desafios estão:

Falta de suporte automatizado aos usuários;
Dúvidas sobre instalação e utilização dos carregadores;
Gerenciamento da demanda energética;
Compartilhamento da infraestrutura em condomínios;
Integração com sistemas de energia solar;
Eficiência energética e balanceamento de carga.

O ChargeWise AI foi desenvolvido para auxiliar na solução desses desafios através de atendimento automatizado e contextualizado.

---

# Objetivos

- Responder dúvidas sobre carregadores GoodWe;
- Auxiliar usuários de veículos elétricos;
- Fornecer orientações sobre infraestrutura de recarga;
- Apoiar síndicos e administradores de condomínio;
- Explicar conceitos de eficiência energética;
- Fornecer informações sobre integração com energia solar;
- Melhorar a experiência dos usuários através de IA Generativa.
- Funcionalidades Implementadas
- Contextualização especializada através de System Prompt;
- Memória conversacional utilizando histórico de mensagens;
- Few-Shot Prompting para direcionamento das respostas;
- Adaptação da linguagem conforme o perfil do usuário;
- Controle de escopo para evitar respostas fora do contexto do projeto;
- Histórico de conversa para diálogos contínuos;
- Respostas especializadas no contexto GoodWe;
- Escalonamento para suporte técnico quando necessário.
- Personas Atendidas
- Usuário Final

Busca informações sobre carregamento, horários recomendados e utilização dos carregadores.

## Síndico ou Administrador

Necessita avaliar viabilidade de instalação, compartilhamento da infraestrutura e gestão energética.

## Técnico ou Eletricista

Precisa de informações relacionadas à infraestrutura elétrica, dispositivos de proteção e boas práticas de instalação.

---

# Tecnologias Utilizadas

|Tecnologia	| Função |
|---|---|
|Python	| Desenvolvimento do chatbot |
|Ollama	| Execução local do modelo de IA |
|Llama 3.2 1B	| Modelo de linguagem |
|LangGraph | Framework de agentes da Sprint 03 |
|Pytest | Testes automatizados |
|Google Colab	| Ambiente de desenvolvimento |
|Markdown	| Documentação |
|Draw.io	| Fluxograma |
|GitHub	| Versionamento |

---

# Arquitetura da Solução

## Sprint 03

```text
Usuario
   ↓
ChargeGridAgent (LangGraph)
   ↓
Guardrails
   ↓
Memoria por sessao
   ↓
Contexto ChargeGrid
   ↓
Modelo configurado
   ↓
Resposta segura e contextualizada
```

## Sprints 1 e 2

```text
Usuário
   ↓
Interface Conversacional
   ↓
System Prompt
   ↓
Few-Shot Prompting
   ↓
Base de Conhecimento GoodWe
   ↓
Histórico de Conversa
   ↓
Llama 3.2 1B (Ollama)
   ↓
Resposta Contextualizada
   ↓
Usuário
```

---

# Técnicas de IA Aplicadas

### System Prompt

Define o comportamento do assistente e restringe sua atuação ao contexto GoodWe, mobilidade elétrica e infraestrutura de recarga.

### Few-Shot Prompting

Utilização de exemplos de perguntas e respostas para orientar o comportamento esperado do modelo.

### Memória Conversacional

Implementação de histórico de mensagens para permitir conversas contínuas e contextualizadas.

### Context Injection

Inserção de informações específicas relacionadas ao cenário GoodWe e ao EV Challenge.

### Ajuste de Parâmetros

Configuração de temperatura e limite de geração de tokens para melhorar consistência e desempenho.

---

# Base de Conhecimento Utilizada

O chatbot foi configurado utilizando informações relacionadas a:

Carregadores GoodWe;
Veículos elétricos;
Infraestrutura de recarga;
Gestão energética;
Balanceamento inteligente de carga;
Integração com energia solar;
Utilização de carregadores em condomínios.

---

# Resultados Obtidos

- Responde adequadamente perguntas relacionadas ao contexto GoodWe;
- Mantém o escopo definido pelo projeto;
- Utiliza memória de conversa para melhorar a continuidade das interações;
- Adapta respostas ao perfil do usuário;
- Recusa perguntas fora do domínio do projeto;
- Mantém coerência durante diálogos contínuos.
- Melhorias Implementadas Durante a Sprint 2
- Refinamento do System Prompt;
- Implementação de memória conversacional;
- Inclusão de Few-Shot Prompting;
- Ajuste dos parâmetros do modelo;
- Otimização do contexto enviado ao LLM;
- Controle de escopo para respostas fora do domínio.

---

# Como Executar

### Pré-requisitos
Python 3.10+
Ollama instalado
Instalação
pip install ollama
Download do Modelo
ollama pull llama3.2:1b

### Execução

Abra o notebook disponível na pasta:

colab/chatbot_teste.ipynb

ou execute o script Python principal do projeto.

Para encerrar o chatbot:

sair

---

# Estrutura do Projeto

```text
chargewise-ai/
│
├── docs/
│   ├── goodwe chatbot.drawio.png
│   ├── modelo-teste.md
│   ├── casos_teste_sprint03.md
│   ├── relatorio_evolucao.md
│   ├── relatorio_modelos.md
│   └── system-prompt.md
│
├── src/
│   └── chargegrid_intelligence/
│       ├── agent.py
│       ├── cli.py
│       ├── guardrails.py
│       ├── knowledge.py
│       ├── memory.py
│       └── models.py
│
├── tests/
│   └── test_chargegrid_agent.py
│
├── colab/
│   ├── chatbot.py
│   └── chatbot_charge.py
│
├── assets/
│   ├── chatbot-demo-1.jpeg
│   ├── chatbot-demo-2.jpeg
│   ├── chatbot-demo-3.jpeg
│   └── chatbot-demo-4.jpeg
|
└── README.md
```

---

## EV Challenge 2026 — GoodWe

Projeto acadêmico desenvolvido para o EV Challenge 2026 da GoodWe em parceria com a FIAP, com foco na aplicação de Inteligência Artificial Generativa para suporte a usuários de carregadores veiculares e soluções de mobilidade elétrica.
