# Relatório de Evolução - ChargeGrid Intelligence

## 1. Resumo da evolução

Nas Sprints 1 e 2, o projeto ChargeGrid Intelligence foi estruturado como um chatbot voltado ao EV Challenge GoodWe/FIAP. A solução já possuía um contexto de negócio relacionado à recarga veicular, mas o núcleo conversacional ainda dependia de um fluxo mais manual, com menor separação entre contexto, memória, segurança e chamada ao modelo.

Na Sprint 03, o projeto foi refatorado para uma arquitetura baseada em agentes. A nova versão utiliza LangChain para organizar o fluxo conversacional, Google Gemini como modelo de linguagem, memória por sessão e guardrails para controlar o comportamento do agente. A aplicação também passou a contar com dois agentes: o `ChargeGridAgent`, responsável pela conversa principal, e o `ScopeGuardAgent`, responsável por bloquear perguntas fora do contexto ChargeGrid.

## 2. Refatoração técnica

O framework escolhido foi o LangChain. A escolha foi motivada pela integração com modelos de linguagem, pela facilidade de composição de prompts, pelo suporte a histórico de mensagens e pela adequação ao objetivo acadêmico da Sprint 03.

Principais componentes utilizados:

- `ChatGoogleGenerativeAI`: integração com o Google Gemini.
- `ChatPromptTemplate`: estruturação do prompt de sistema e da pergunta do usuário.
- `MessagesPlaceholder`: inclusão do histórico da conversa.
- `InMemoryChatMessageHistory`: memória por sessão.

O contexto do ChargeGrid passou a ser enviado automaticamente ao modelo. Dessa forma, o usuário não precisa explicar o projeto a cada pergunta. A resposta final também foi tratada para ocultar informações internas, como chaves, variáveis de ambiente, caminhos locais e metadados retornados pela API.

Trade-offs identificados:

- A solução depende de uma chave válida do Gemini.
- Os dados operacionais ainda são simulados, pois não há integração com sensores reais.
- Alguns modelos podem mudar de disponibilidade, exigindo ajuste de configuração.
- O guardião de escopo precisa equilibrar bloqueio de assuntos externos e liberdade para perguntas curtas de continuidade.

## 3. Comparativo antes x depois

| Critério | Sprints 1 e 2 | Sprint 03 |
|---|---|---|
| Arquitetura | Fluxo conversacional mais manual | Arquitetura com agentes e LangChain |
| Agentes | Não havia separação clara de agentes | Dois agentes: `ChargeGridAgent` e `ScopeGuardAgent` |
| Memória | Histórico mais simples | Memória por sessão com histórico de mensagens |
| Segurança | Regras menos estruturadas | Guardrails para prompt injection, escopo, riscos elétricos, jurídico e financeiro |
| Modelo | Configuração anterior menos estável | Gemini 3.6 Flash integrado ao LangChain |
| Execução | Menos padronizada | Execução no Colab com `chat_colab.py` |
| Perguntas fora de escopo | Maior risco de resposta inadequada | Bloqueio pelo `ScopeGuardAgent` |
| Respostas | Mais propensas a formato robótico | Respostas mais naturais em português |
| Chaves de API | Risco maior de exposição manual | Chave fornecida apenas por ambiente seguro |

## 4. Métricas e resultados

| Métrica | Resultado observado |
|---|---|
| Turnos de memória demonstrados | 3 turnos |
| Agentes implementados | 2 agentes |
| Testes funcionais documentados | 5 casos |
| Testes de segurança documentados | 6 casos |
| Modelos/configurações avaliadas | Gemini 2.5 Flash, Gemini 3.6 Flash e ajuste de parâmetros |
| Modelo final | Gemini 3.6 Flash |
| Execução principal | Google Colab |

## 5. Problemas encontrados e soluções

### Problema 1: modelo indisponível

Durante os testes, o modelo Gemini 2.5 Flash retornou erro de indisponibilidade para novos usuários.

Alternativas consideradas:

- manter o modelo antigo;
- migrar para outro fornecedor;
- atualizar para o modelo recomendado pela API.

Solução adotada:

O projeto foi atualizado para Gemini 3.6 Flash.

Justificativa:

O modelo estava disponível, funcionou no Colab e apresentou boa qualidade de resposta em português.

### Problema 2: resposta com metadados internos

Em uma das execuções, o retorno do modelo veio em blocos contendo metadados, o que fez a resposta aparecer com informações técnicas desnecessárias.

Alternativas consideradas:

- imprimir o objeto bruto;
- trocar novamente o modelo;
- tratar a saída antes de exibir ao usuário.

Solução adotada:

Foi criada uma extração limpa de texto, mantendo apenas o conteúdo final da resposta.

Justificativa:

A solução preserva o uso do modelo real e melhora a experiência do usuário, sem expor metadados internos.

### Problema 3: guardião de escopo rígido demais

O `ScopeGuardAgent` inicialmente bloqueava perguntas curtas de continuidade, mesmo quando a conversa já estava dentro do tema ChargeGrid.

Alternativas consideradas:

- remover o bloqueio de escopo;
- liberar qualquer pergunta;
- considerar histórico da sessão.

Solução adotada:

O guardião passou a considerar se já existe contexto de conversa e passou a aceitar perguntas curtas de continuidade.

Justificativa:

O agente manteve a segurança sem prejudicar a fluidez da conversa.

## 6. Divisão da equipe

| Integrante | RM | Responsabilidade principal |
|---|---:|---|
| Mateus de Oliveira Fernandes Neves | 572431 | Data Structures and Algorithms |
| Angela Sousa Takezawa | 570797 | Prompt and Artificial Intelligence |
| Pedro Soares de Souza | 571285 | Modelagem Matemática e Computacional |
| Paulo Henrique Lira Bilac de Araújo | 569496 | Computer Organization and Architecture / Computer Science |
| Olavo Dadario Vianna Barreto | 569272 | Pensamento Computacional e Automação com Python / Soluções em Energias Renováveis e Sustentáveis |
| Jhon | Não informado | Modelagem Linear para Aprendizado de Máquina |

## 7. Conclusão

A nova arquitetura tornou o chatbot mais robusto. O uso de LangChain permitiu organizar melhor o prompt, o histórico e a chamada ao modelo. A separação entre agente principal e agente guardião tornou o comportamento mais controlável. Além disso, os testes documentados demonstram evolução em memória, segurança, clareza de resposta e execução no Google Colab.
