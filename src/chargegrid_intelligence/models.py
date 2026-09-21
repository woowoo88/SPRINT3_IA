from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass
class ModelResponse:
    content: str
    model_name: str
    estimated_tokens: int


class OpenAIChargeGridModel:
    """Real OpenAI-backed model used by ChargeGrid Intelligence."""

    def __init__(self, model_name: str | None = None, temperature: float = 0.2):
        self.name = model_name or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = temperature

    def generate(self, user_text: str, context: str, facts: dict[str, str]) -> ModelResponse:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY não foi configurada. No Colab, configure a chave antes de criar o agente."
            )

        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=self.name,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": _system_prompt(context, facts)},
                {"role": "user", "content": user_text},
            ],
        )
        content = response.choices[0].message.content or ""
        return ModelResponse(content=content.strip(), model_name=self.name, estimated_tokens=_estimate_tokens(content))


class OllamaChargeGridModel:
    """Real local LLM model through Ollama."""

    def __init__(self, model_name: str = "llama3.2:1b", temperature: float = 0.2):
        self.name = model_name
        self.temperature = temperature

    def generate(self, user_text: str, context: str, facts: dict[str, str]) -> ModelResponse:
        import ollama

        prompt = f"""
{_system_prompt(context, facts)}

Pergunta do usuário:
{user_text}
""".strip()
        result = ollama.chat(
            model=self.name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": self.temperature, "num_predict": 350},
        )
        content = result["message"]["content"]
        return ModelResponse(content=content.strip(), model_name=self.name, estimated_tokens=_estimate_tokens(content))


def _system_prompt(context: str, facts: dict[str, str]) -> str:
    return f"""
Você é o ChargeGrid Intelligence, um agente de IA conversacional do EV Challenge GoodWe/FIAP.

Responda sempre em português do Brasil, com acentuação correta, tom natural e em primeira pessoa.
Não fale de si mesmo em terceira pessoa. Não diga "o agente deve", "o sistema deve" ou frases de relatório.
Responda como um assistente real: "eu recomendo", "eu registro", "eu verificaria" ou responda diretamente.
Não use respostas prontas nem repita uma estrutura fixa. Adapte a resposta à pergunta específica do usuário.

Seu escopo é gerenciamento comercial de recarga veicular: eletropostos, sessões de recarga,
controle de demanda, OCPP, MODBUS, pagamento, tarifa dinâmica, status de conectores, vagas,
ocupação de vagas, estacionamento vinculado à recarga, falhas,
relatórios operacionais e integração conceitual com GoodWe.

Use a memória da sessão quando ela existir.
Se algum dado real não foi fornecido, explique que trabalha com dados simulados do protótipo.
Não invente especificações oficiais de produtos GoodWe.
Para riscos elétricos, instalação ou manutenção, recomende profissional habilitado.

Se a pergunta for sobre uma vaga específica, como "posso estacionar na vaga 12?" ou
"tem alguém estacionado?", responda como operador do ChargeGrid:
- se houver dado na memória, use esse dado;
- se não houver status real da vaga, diga claramente que não consigo confirmar ocupação em tempo real;
- explique como eu verificaria no painel: status da vaga/conector, sessão ativa, pagamento, reserva e alerta;
- nunca finja que viu uma vaga ocupada ou livre sem essa informação.

Contexto do projeto:
{context}

Memória estruturada:
{_format_memory(facts)}
""".strip()


def _format_memory(facts: dict[str, str]) -> str:
    if not facts:
        return "Nenhuma informação específica foi registrada ainda."
    return "\n".join(f"- {key}: {value}" for key, value in sorted(facts.items()))


def _estimate_tokens(text: str) -> int:
    return max(1, round(len(text.split()) * 1.35))
