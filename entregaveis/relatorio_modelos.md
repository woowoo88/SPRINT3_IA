# Relatório de Modelos - ChargeGrid Intelligence

## Objetivo

Este relatório registra a comparação entre modelos e configurações avaliadas durante a Sprint 03 do ChargeGrid Intelligence. O objetivo foi escolher uma configuração adequada para um agente conversacional acadêmico voltado ao gerenciamento comercial de recarga veicular.

## Framework utilizado

O framework escolhido foi o LangChain, utilizado para organizar o fluxo conversacional, montar o prompt com contexto, manter histórico de mensagens e integrar o modelo de linguagem ao agente principal.

Principais componentes utilizados:

- `ChatGoogleGenerativeAI`: integração com o modelo Gemini.
- `ChatPromptTemplate`: composição do prompt de sistema e da pergunta do usuário.
- `MessagesPlaceholder`: inclusão do histórico da sessão no prompt.
- `InMemoryChatMessageHistory`: memória conversacional por sessão.

## Modelos e configurações avaliadas

| Modelo ou configuração | Situação | Resultado observado |
|---|---|---|
| Gemini 2.5 Flash | Testado inicialmente | A API retornou erro de indisponibilidade para novos usuários. O modelo não foi mantido na versão final. |
| Gemini 3.6 Flash | Testado e adotado | Executou as chamadas do agente com boa qualidade, respostas naturais em português e compatibilidade com o Colab. |
| Gemini 3.6 Flash com parâmetro `temperature` | Testado durante ajustes | A biblioteca informou que o modelo usa padrões fixos de amostragem e ignora `temperature`. O parâmetro foi removido da configuração padrão. |

## Conjunto de testes utilizado

Os testes foram organizados em quatro grupos:

1. Perguntas funcionais sobre vagas, conectores, pagamento, OCPP e MODBUS.
2. Perguntas de memória, com pelo menos três turnos de conversa.
3. Perguntas fora do escopo do ChargeGrid.
4. Tentativas de prompt injection e riscos de segurança elétrica.

## Resultados obtidos

| Critério | Gemini 2.5 Flash | Gemini 3.6 Flash |
|---|---:|---:|
| Disponibilidade para execução | Não disponível | Disponível |
| Qualidade das respostas em português | Não avaliada por bloqueio de API | Boa |
| Compatibilidade com Colab | Não validada | Boa após ajuste de dependências |
| Resposta com contexto automático | Não validada | Adequada |
| Memória por sessão | Não validada | Adequada |
| Segurança e guardrails | Não validada | Adequada com `ScopeGuardAgent` |
| Modelo escolhido | Não | Sim |

## Diferenças percebidas

O Gemini 2.5 Flash não foi mantido porque a API retornou erro informando que o modelo não estava mais disponível para novos usuários. O Gemini 3.6 Flash foi adotado por estar disponível, funcionar no Colab e responder de forma mais natural depois dos ajustes de prompt e limpeza de saída.

Durante os testes, a resposta do Gemini 3.6 Flash chegou inicialmente em formato de blocos com metadados. Esse problema foi corrigido com uma função de extração de texto, para que o usuário receba apenas a resposta final da IA.

## Vantagens do modelo escolhido

- Disponível para execução no ambiente do projeto.
- Boa qualidade de resposta em português.
- Integração direta com LangChain.
- Compatível com o modo de conversa contínua.
- Funcionou com memória por sessão e contexto interno.

## Limitações e trade-offs

- O agente depende de chave válida do Gemini.
- Os dados operacionais são simulados, pois o protótipo não está conectado a sensores reais.
- Alguns parâmetros de geração, como `temperature`, podem ser ignorados pelo modelo escolhido.
- A comparação com modelos indisponíveis ficou limitada pela disponibilidade da API.

## Modelo escolhido para a versão final

O modelo escolhido para a versão final foi o Gemini 3.6 Flash.

## Justificativa da escolha

A escolha foi baseada na disponibilidade real para execução, na integração com LangChain, na qualidade das respostas em português e na compatibilidade com o Google Colab. O modelo atendeu melhor ao objetivo da Sprint 03: transformar o chatbot em uma aplicação de agentes mais robusta, com memória, contexto automático e guardrails.
