# Relatório de Evolução - ChargeGrid Intelligence

## 1. Resumo da Evolução

Nas Sprints 1 e 2, o projeto ChargeWise AI funcionava como um chatbot simples em Python, integrado ao Ollama, com `system prompt`, exemplos few-shot, histórico manual e filtro por palavras-chave. Essa versão foi importante para validar a ideia de um assistente voltado a carregadores veiculares, mas ainda apresentava pouca separação de responsabilidades e controle limitado sobre memória, segurança e avaliação.

Na Sprint 03, o projeto evoluiu para o ChargeGrid Intelligence, com foco no gerenciamento automatizado de recarga comercial. A proposta passou a considerar controle de demanda, integração conceitual com eletropostos, registro do ciclo de sessão, protocolos OCPP/MODBUS e regras de cobrança dinâmica. A principal mudança técnica foi a refatoração do núcleo conversacional para uma arquitetura baseada em agentes usando LangGraph.

## 2. Refatoração e Decisões Técnicas

O framework escolhido foi o LangGraph, pois ele permite representar o fluxo do agente como um grafo de estados. Isso deixou a arquitetura mais clara do que uma sequência manual de chamadas ao modelo. O agente foi dividido nos seguintes nós:

| Nó | Responsabilidade |
|---|---|
| guardrails | validar prompt injection, risco elétrico, escopo, temas jurídicos e financeiros |
| memory | extrair fatos da conversa e atualizar memória por sessão |
| context | montar o contexto do ChargeGrid com dados simulados e memória |
| respond | gerar a resposta final usando o modelo configurado |

A memória por sessão é gerenciada pelo checkpointer em memória do LangGraph, usando `thread_id` como identificador da conversa. Assim, duas sessões diferentes não misturam informações. Para os testes, foram criados um modelo determinístico offline, um modelo conservador e um adaptador opcional para Ollama.

O principal trade-off foi aceitar uma arquitetura um pouco mais complexa em troca de mais controle. O chatbot antigo era mais simples de explicar, mas o novo fluxo facilita testes, manutenção e extensão futura para LLMs reais, ferramentas externas e integração com APIs.

## 3. Comparativo Antes x Depois

| Critério | Sprints 1 e 2 | Sprint 03 |
|---|---|---|
| Arquitetura | Script Python monolítico com prompt e histórico manual | Grafo de agente com nós separados no LangGraph |
| Memória | Lista de mensagens enviada ao modelo | Memória por sessão via `thread_id` e checkpointer |
| Escopo | Filtro simples por palavras-chave | Guardrails por categoria: escopo, injection, risco elétrico, jurídico e financeiro |
| Modelo | Llama 3.2 1B via Ollama | Modelos comparados: rule-v1, conservative-v1 e Ollama opcional |
| Testes | Casos manuais documentados | Testes automatizados com `pytest` |
| Segurança | Recusa básica para fora de contexto | Bloqueio de prompt injection e orientações elétricas perigosas |
| Métricas | Pouco estruturadas | Latência local inferior a 1s nos testes automatizados e tokens estimados por resposta |

Resultado geral: a nova arquitetura tornou o chatbot melhor para demonstração acadêmica, porque a memória ficou verificável, os guardrails ficaram separados do modelo e a comparação entre modelos passou a ser documentada.

## 4. Problemas Encontrados e Soluções

O primeiro problema foi a baixa separação de responsabilidades. Na versão anterior, prompt, contexto, filtro, memória e chamada ao modelo ficavam no mesmo arquivo. A alternativa seria apenas melhorar o script antigo, mas a solução adotada foi criar um pacote em `src/chargegrid_intelligence`, separando agente, memória, guardrails, conhecimento e modelos.

O segundo problema foi a dependência de um único modelo local. Se o Ollama não estivesse instalado, a demonstração poderia falhar. A solução foi criar modelos determinísticos offline para testes e manter o Ollama como opcional. Essa decisão aumenta a confiabilidade da entrega sem impedir uma evolução futura.

O terceiro problema foi a segurança. Prompt injection e pedidos perigosos poderiam induzir o chatbot a sair do escopo. A solução foi colocar guardrails antes da geração da resposta, bloqueando tentativas de revelar prompt interno, comandos fora do domínio e instruções elétricas inseguras.

## 5. Conclusão

A Sprint 03 transformou o chatbot em uma solução mais organizada e controlável. O ChargeGrid Intelligence ainda é um protótipo acadêmico, mas agora possui uma base mais próxima de uma aplicação real: fluxo de agente, memória por sessão, testes de segurança, comparação de modelos e documentação de evolução. O ganho principal não foi apenas trocar biblioteca, mas tornar o comportamento do chatbot mais previsível, verificável e seguro.
