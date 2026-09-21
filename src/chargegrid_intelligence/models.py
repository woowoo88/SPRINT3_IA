from __future__ import annotations

from dataclasses import dataclass


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

        if "quantas" in lower and ("vagas" in lower or "conectores" in lower or "pontos" in lower):
            amount = facts.get("quantidade_pontos")
            if amount:
                content = f"Voce informou anteriormente que existem {amount} pontos/vagas de recarga."
            else:
                content = "Ainda nao tenho uma quantidade de vagas registrada nesta sessao."
        elif "local" in lower or "condominio" in lower or "condomínio" in lower:
            site = facts.get("local_mencionado")
            if site:
                content = f"O local mencionado na sessao foi {site}."
            else:
                content = "Ainda nao tenho um local especifico salvo na memoria da sessao."
        elif "ocpp" in lower or "modbus" in lower:
            content = (
                "Na arquitetura proposta, OCPP conversa com os eletropostos para eventos de "
                "sessao, status e comandos operacionais. MODBUS fica no nivel de medidores e "
                "controladores, apoiando leitura de grandezas eletricas e controle de demanda."
            )
        elif "cobranca" in lower or "cobrança" in lower or "tarifa" in lower or "pagamento" in lower:
            tariff = facts.get("tarifa_informada", "uma tarifa configurada pelo operador")
            content = (
                f"A cobranca dinamica pode usar {tariff}, horario, energia consumida e perfil "
                "do usuario. O agente registra inicio, fim, kWh estimado e regra aplicada, "
                "sempre deixando claro que os valores do prototipo sao simulados."
            )
        elif "demanda" in lower or "potencia" in lower or "potência" in lower or "balanceamento" in lower:
            amount = facts.get("quantidade_pontos", "os pontos ativos")
            content = (
                "O controle de demanda distribui a potencia disponivel entre "
                f"{amount} e prioriza estabilidade da instalacao. Se a carga total passar do "
                "limite configurado, o sistema reduz a potencia por conector ou agenda sessoes."
            )
        elif "sessao" in lower or "sessão" in lower:
            content = (
                "Cada sessao deve registrar usuario, conector, horario de inicio e fim, energia "
                "consumida, status do carregador, regra de tarifa e valor calculado."
            )
        else:
            content = (
                "Para o ChargeGrid Intelligence, a recomendacao e tratar a recarga como uma "
                "operacao comercial monitorada: registrar a sessao, acompanhar demanda, aplicar "
                "guardrails de seguranca e acionar regras de cobranca dinamica."
            )

        return ModelResponse(content=content, model_name=self.name, estimated_tokens=_estimate_tokens(content))


class ConservativeChargeGridModel(RuleBasedChargeGridModel):
    name = "chargegrid-conservative-v1"

    def generate(self, user_text: str, context: str, facts: dict[str, str]) -> ModelResponse:
        response = super().generate(user_text, context, facts)
        content = (
            response.content
            + " Para decisao real de instalacao, capacidade eletrica ou manutencao, valide com "
            "um profissional habilitado e documentacao oficial."
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
