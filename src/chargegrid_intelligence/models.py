from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass
class ModelResponse:
    content: str
    model_name: str
    estimated_tokens: int


class RuleBasedChargeGridModel:
    """Offline model used for reproducible academic tests."""

    name = "chargegrid-rule-v1"

    def generate(self, user_text: str, context: str, facts: dict[str, str]) -> ModelResponse:
        lower = user_text.lower()
        mentioned_site = facts.get("local_mencionado") or _extract_site(user_text)

        if _is_user_registering_site(lower, mentioned_site):
            content = (
                f"Entendido. Vou considerar {mentioned_site} como o local desta "
                "sessão para as próximas respostas."
            )
        elif _is_user_registering_amount(lower, facts):
            content = (
                f"Perfeito. Registrei que esse local possui {facts['quantidade_pontos']} "
                "pontos/vagas de recarga."
            )
        elif "quantas" in lower and ("vagas" in lower or "conectores" in lower or "pontos" in lower):
            amount = facts.get("quantidade_pontos")
            if amount:
                content = f"Você informou anteriormente que existem {amount} pontos/vagas de recarga."
            else:
                content = "Ainda não tenho uma quantidade de vagas registrada nesta sessão."
        elif _has_any(lower, ["local", "condominio", "condomínio", "onde"]):
            site = facts.get("local_mencionado")
            if site:
                content = f"O local mencionado na sessão foi {site}."
            else:
                content = "Ainda não tenho um local específico salvo na memória da sessão."
        elif _has_any(lower, ["ocpp", "modbus", "protocolo", "comunicação", "comunicacao"]):
            content = (
                "Na arquitetura proposta, OCPP conversa com os eletropostos para eventos de "
                "sessão, status e comandos operacionais. MODBUS fica no nível de medidores e "
                "controladores, apoiando leitura de grandezas elétricas e controle de demanda."
            )
        elif _has_any(lower, ["cobranca", "cobrança", "tarifa", "pagamento", "preço", "preco", "valor", "custo"]):
            tariff = facts.get("tarifa_informada", "uma tarifa configurada pelo operador")
            content = (
                f"A cobrança dinâmica pode usar {tariff}, horário, energia consumida e perfil "
                "do usuário. O agente registra início, fim, kWh estimado e regra aplicada, "
                "sempre deixando claro que os valores do protótipo são simulados."
            )
        elif _has_any(lower, ["demanda", "potencia", "potência", "balanceamento", "sobrecarga", "limite"]):
            amount = facts.get("quantidade_pontos", "os pontos ativos")
            content = (
                "O controle de demanda distribui a potência disponível entre "
                f"{amount} e prioriza a estabilidade da instalação. Se a carga total passar do "
                "limite configurado, o sistema reduz a potência por conector ou agenda sessões."
            )
        elif _has_any(lower, ["sessao", "sessão", "ciclo", "histórico", "historico"]):
            content = (
                "Cada sessão deve registrar usuário, conector, horário de início e fim, energia "
                "consumida, status do carregador, regra de tarifa e valor calculado."
            )
        elif _has_any(lower, ["status", "ativo", "ocupado", "disponível", "disponivel", "fila"]):
            content = _status_answer(facts)
        elif _has_any(lower, ["falha", "erro", "alerta", "indisponível", "indisponivel", "conector 2", "conector 3"]):
            content = (
                "Para tratar uma falha, o ChargeGrid deve registrar o evento, identificar o "
                "conector afetado, verificar se houve erro de comunicação OCPP ou leitura "
                "anormal via MODBUS e marcar o ponto como indisponível até a validação técnica."
            )
        elif _has_any(lower, ["relatório", "relatorio", "resumo", "dashboard", "indicador", "métrica", "metrica"]):
            content = _report_answer(facts)
        elif _has_any(lower, ["arquitetura", "agente", "langgraph", "memória", "memoria", "guardrails"]):
            content = (
                "A arquitetura usa um agente em LangGraph com etapas separadas: primeiro aplica "
                "guardrails, depois atualiza a memória da sessão, monta o contexto do ChargeGrid "
                "e só então gera a resposta. Isso facilita testes, segurança e evolução do projeto."
            )
        elif _has_any(lower, ["solar", "fotovoltaica", "fotovoltaico", "goodwe"]):
            content = (
                "No contexto do projeto, a integração com o ecossistema GoodWe pode ser tratada "
                "como apoio ao monitoramento energético e ao uso mais eficiente da recarga. Como "
                "não há especificação oficial anexada, a resposta deve permanecer conceitual e "
                "não inventar dados técnicos de produto."
            )
        else:
            content = _general_chargegrid_answer(user_text, facts)

        return ModelResponse(content=content, model_name=self.name, estimated_tokens=_estimate_tokens(content))


class ConservativeChargeGridModel(RuleBasedChargeGridModel):
    name = "chargegrid-conservative-v1"

    def generate(self, user_text: str, context: str, facts: dict[str, str]) -> ModelResponse:
        response = super().generate(user_text, context, facts)
        if not _needs_professional_warning(user_text):
            return ModelResponse(
                content=response.content,
                model_name=self.name,
                estimated_tokens=response.estimated_tokens,
            )

        content = (
            response.content
            + " Como envolve instalação, capacidade elétrica ou manutenção, valide a decisão "
            "com um profissional habilitado e com a documentação oficial."
        )
        return ModelResponse(content=content, model_name=self.name, estimated_tokens=_estimate_tokens(content))


class OllamaChargeGridModel:
    def __init__(self, model_name: str = "llama3.2:1b", temperature: float = 0.1):
        self.name = model_name
        self.temperature = temperature

    def generate(self, user_text: str, context: str, facts: dict[str, str]) -> ModelResponse:
        import ollama

        prompt = f"""
Voce e o ChargeGrid Intelligence, agente do EV Challenge GoodWe/FIAP.
Use somente o contexto abaixo e nao invente especificacoes reais.

{context}

Pergunta do usuario:
{user_text}
"""
        result = ollama.chat(
            model=self.name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": self.temperature, "num_predict": 220},
        )
        content = result["message"]["content"]
        return ModelResponse(content=content, model_name=self.name, estimated_tokens=_estimate_tokens(content))


def _estimate_tokens(text: str) -> int:
    return max(1, round(len(text.split()) * 1.35))


def _has_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def _extract_site(text: str) -> str | None:
    site_match = re.search(
        r"(?:condominio|condomínio|eletroposto|campus|unidade)\s+([A-Za-zÀ-ÿ0-9 ._-]{2,40})",
        text,
        re.IGNORECASE,
    )
    if not site_match:
        return None
    return site_match.group(1).strip(" .")


def _is_user_registering_site(lower: str, site: str | None) -> bool:
    return bool(site) and any(term in lower for term in ["estou usando", "estou analisando", "meu local", "eletroposto"])


def _is_user_registering_amount(lower: str, facts: dict[str, str]) -> bool:
    if "quantas" in lower or "quantos" in lower:
        return False
    return bool(facts.get("quantidade_pontos")) and any(
        term in lower for term in ["existem", "temos", "tenho", "possui", "são", "sao"]
    ) and any(term in lower for term in ["vagas", "conectores", "carregadores", "pontos"])


def _needs_professional_warning(user_text: str) -> bool:
    lower = user_text.lower()
    risk_terms = [
        "instalação",
        "instalacao",
        "manutenção",
        "manutencao",
        "capacidade elétrica",
        "capacidade eletrica",
        "aterramento",
        "disjuntor",
        "risco",
        "abrir",
        "ligar direto",
    ]
    return any(term in lower for term in risk_terms)


def _status_answer(facts: dict[str, str]) -> str:
    amount = facts.get("quantidade_pontos")
    site = facts.get("local_mencionado")
    if amount:
        site_text = site or "o local informado"
        return (
            f"Para {site_text}, eu consideraria os {amount} pontos de recarga como a base do painel "
            "operacional. O status ideal deve mostrar quais conectores estão livres, ocupados, "
            "em falha ou aguardando liberação de pagamento."
        )
    if site:
        return (
            f"Para {site}, o status operacional deve mostrar conectores disponíveis, ocupados, "
            "em falha e em fila. Se você informar a quantidade de pontos, eu também consigo "
            "usar esse número no resumo."
        )
    return (
        "O status operacional deve mostrar conectores disponíveis, ocupados, em falha e em fila. "
        "Se você informar o local e a quantidade de pontos, eu consigo usar esses dados na resposta."
    )


def _report_answer(facts: dict[str, str]) -> str:
    site = facts.get("local_mencionado", "unidade analisada")
    amount = facts.get("quantidade_pontos", "pontos cadastrados")
    return (
        f"Um relatório do ChargeGrid para {site} pode trazer: quantidade de pontos ({amount}), "
        "sessões concluídas, energia consumida em kWh, tempo médio de uso, alertas por conector, "
        "receita estimada e recomendações de balanceamento de demanda."
    )


def _general_chargegrid_answer(user_text: str, facts: dict[str, str]) -> str:
    site = facts.get("local_mencionado")
    amount = facts.get("quantidade_pontos")
    memory = []
    if site:
        memory.append(f"local: {site}")
    if amount:
        memory.append(f"pontos de recarga: {amount}")

    memory_text = ""
    if memory:
        memory_text = " Considerando a memória da sessão (" + "; ".join(memory) + "),"
    else:
        memory_text = " Dentro do escopo do ChargeGrid,"

    return (
        f"{memory_text} a resposta deve priorizar operação de recarga comercial: registrar a "
        "sessão, acompanhar status dos conectores, controlar demanda, aplicar regra de cobrança "
        "e sinalizar riscos ou falhas para análise técnica. Se você quiser, posso detalhar essa "
        "pergunta por status, cobrança, OCPP, MODBUS, demanda ou relatório operacional."
    )
