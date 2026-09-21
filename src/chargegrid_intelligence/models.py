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
        elif "local" in lower or "condominio" in lower or "condomínio" in lower:
            site = facts.get("local_mencionado")
            if site:
                content = f"O local mencionado na sessão foi {site}."
            else:
                content = "Ainda não tenho um local específico salvo na memória da sessão."
        elif "ocpp" in lower or "modbus" in lower:
            content = (
                "Na arquitetura proposta, OCPP conversa com os eletropostos para eventos de "
                "sessão, status e comandos operacionais. MODBUS fica no nível de medidores e "
                "controladores, apoiando leitura de grandezas elétricas e controle de demanda."
            )
        elif "cobranca" in lower or "cobrança" in lower or "tarifa" in lower or "pagamento" in lower:
            tariff = facts.get("tarifa_informada", "uma tarifa configurada pelo operador")
            content = (
                f"A cobrança dinâmica pode usar {tariff}, horário, energia consumida e perfil "
                "do usuário. O agente registra início, fim, kWh estimado e regra aplicada, "
                "sempre deixando claro que os valores do protótipo são simulados."
            )
        elif "demanda" in lower or "potencia" in lower or "potência" in lower or "balanceamento" in lower:
            amount = facts.get("quantidade_pontos", "os pontos ativos")
            content = (
                "O controle de demanda distribui a potência disponível entre "
                f"{amount} e prioriza a estabilidade da instalação. Se a carga total passar do "
                "limite configurado, o sistema reduz a potência por conector ou agenda sessões."
            )
        elif "sessao" in lower or "sessão" in lower:
            content = (
                "Cada sessão deve registrar usuário, conector, horário de início e fim, energia "
                "consumida, status do carregador, regra de tarifa e valor calculado."
            )
        else:
            content = (
                "Para o ChargeGrid Intelligence, a recomendação é tratar a recarga como uma "
                "operação comercial monitorada: registrar a sessão, acompanhar demanda, aplicar "
                "guardrails de segurança e acionar regras de cobrança dinâmica."
            )

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
