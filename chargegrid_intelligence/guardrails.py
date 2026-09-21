from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata


@dataclass(frozen=True)
class GuardrailResult:
    allowed: bool
    category: str
    message: str


class ScopeGuardAgent:
    """Agente responsável por bloquear perguntas fora do contexto ChargeGrid."""

    def evaluate(self, text: str, has_context: bool = False) -> GuardrailResult:
        return evaluate_guardrails(text, has_context=has_context)


PROMPT_INJECTION_TERMS = [
    "ignore todas as instrucoes",
    "ignore todas as instruções",
    "revele seu system prompt",
    "mostre seu system prompt",
    "voce nao trabalha mais",
    "você não trabalha mais",
    "desconsidere o contexto",
]

ELECTRICAL_RISK_TERMS = [
    "abrir o carregador",
    "burlar disjuntor",
    "desativar disjuntor",
    "sem aterramento",
    "remover protecao",
    "remover proteção",
    "ligar direto",
]

LEGAL_TERMS = ["processar", "contrato", "indenizacao", "indenização", "juridico", "jurídico"]
FINANCIAL_TERMS = ["investimento garantido", "lucro garantido", "rentabilidade", "acao", "ação"]

DOMAIN_TERMS = [
    "chargegrid",
    "goodwe",
    "fiap",
    "carregador",
    "recarga",
    "eletroposto",
    "veiculo eletrico",
    "veículo elétrico",
    "ocpp",
    "modbus",
    "demanda",
    "potencia",
    "potência",
    "tarifa",
    "sessao",
    "sessão",
    "cobranca",
    "cobrança",
    "energia",
    "vagas",
    "conectores",
    "status",
    "pagamento",
    "pagar",
    "cobrar",
    "custo",
    "preco",
    "preço",
    "pix",
    "cartao",
    "cartão",
    "relatorio",
    "relatório",
    "resumo",
    "dashboard",
    "falha",
    "erro",
    "alerta",
    "kwh",
    "ocupacao",
    "ocupação",
    "fila",
    "protocolo",
    "comunicacao",
    "comunicação",
    "arquitetura",
    "agente",
    "langchain",
    "memoria",
    "memória",
    "guardrails",
    "solar",
    "fotovoltaico",
    "ve",
    "ev",
    "carro eletrico",
    "carro elétrico",
    "estacao",
    "estação",
    "tomada",
    "plug",
    "ocupado",
    "livre",
    "disponivel",
    "disponível",
    "disponiveis",
    "disponíveis",
    "quanto",
    "quantos",
    "quantas",
    "sessao",
    "sessões",
    "carregar",
    "carregamento",
]


FOLLOW_UP_TERMS = [
    "e",
    "isso",
    "esse",
    "essa",
    "esses",
    "essas",
    "como",
    "quanto",
    "quantos",
    "quantas",
    "qual",
    "quais",
    "por que",
    "porque",
    "sim",
    "nao",
    "não",
    "me explica",
    "detalhe",
    "resuma",
]

GREETINGS = ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"]

OFF_TOPIC_TERMS = [
    "receita",
    "bolo",
    "futebol",
    "filme",
    "musica",
    "música",
    "namoro",
    "fofoca",
    "jogo do bicho",
    "loteria",
    "historia do brasil",
    "história do brasil",
]


def evaluate_guardrails(text: str, has_context: bool = False) -> GuardrailResult:
    lower = text.lower()
    normalized = _normalize(text)

    if any(_normalize(term) in normalized for term in PROMPT_INJECTION_TERMS):
        return GuardrailResult(
            allowed=False,
            category="prompt_injection",
            message=(
                "Não posso ignorar minhas instruções, revelar prompts internos ou sair do "
                "escopo do ChargeGrid Intelligence. Posso ajudar com operação segura de "
                "recarga, sessões, demanda, OCPP/MODBUS e cobrança dinâmica."
            ),
        )

    if any(_normalize(term) in normalized for term in ELECTRICAL_RISK_TERMS):
        return GuardrailResult(
            allowed=False,
            category="electrical_safety",
            message=(
                "Não posso orientar procedimentos elétricos perigosos. Para instalação, "
                "manutenção, aterramento, proteções ou abertura de equipamentos, procure "
                "um profissional habilitado e siga as normas aplicáveis."
            ),
        )

    if any(_normalize(term) in normalized for term in LEGAL_TERMS):
        return GuardrailResult(
            allowed=True,
            category="legal_caution",
            message=(
                "Posso explicar impactos operacionais em linguagem geral, mas não substituo "
                "orientação jurídica profissional."
            ),
        )

    if any(_normalize(term) in normalized for term in FINANCIAL_TERMS):
        return GuardrailResult(
            allowed=True,
            category="financial_caution",
            message=(
                "Posso ajudar com estimativas operacionais, mas não forneço aconselhamento "
                "financeiro profissional ou promessa de retorno."
            ),
        )

    if any(_normalize(term) in normalized for term in GREETINGS):
        return GuardrailResult(allowed=True, category="greeting", message="")

    has_domain_term = any(_normalize(term) in normalized for term in DOMAIN_TERMS)
    is_follow_up = has_context and (
        len(normalized.split()) <= 8
        or any(_normalize(term) in normalized for term in FOLLOW_UP_TERMS)
    )
    has_explicit_off_topic = any(_normalize(term) in normalized for term in OFF_TOPIC_TERMS)

    if not has_domain_term and not is_follow_up:
        return GuardrailResult(
            allowed=False,
            category="out_of_scope",
            message=(
                "Eu sou focado no ChargeGrid Intelligence e posso ajudar com recarga veicular, "
                "eletropostos, vagas, conectores, sessões, demanda, OCPP, MODBUS, pagamento, "
                "tarifa dinâmica e relatórios operacionais. Reformule sua pergunta dentro desse contexto."
            ),
        )

    if has_explicit_off_topic and not has_domain_term:
        return GuardrailResult(
            allowed=False,
            category="out_of_scope",
            message=(
                "Essa pergunta não faz parte do contexto do ChargeGrid Intelligence. "
                "Posso ajudar com recarga veicular, vagas, conectores, sessões, demanda, "
                "pagamento, tarifa dinâmica, OCPP, MODBUS e relatórios operacionais."
            ),
        )

    return GuardrailResult(allowed=True, category="ok", message="")


def _normalize(text: str) -> str:
    without_accents = unicodedata.normalize("NFKD", text)
    without_accents = "".join(char for char in without_accents if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", without_accents.lower()).strip()
