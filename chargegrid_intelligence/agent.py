from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

from .guardrails import evaluate_guardrails
from .knowledge import build_context
from .memory import update_facts
from .models import estimate_tokens, system_prompt


class ChargeGridAgent:
    """Agente conversacional do ChargeGrid Intelligence usando LangChain e Gemini."""

    def __init__(self, model_name: str | None = None, temperature: float = 0.2):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY não foi configurada. No Colab, configure a chave antes de criar o agente."
            )

        os.environ["GOOGLE_API_KEY"] = api_key
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self._facts_by_session: dict[str, dict[str, str]] = {}
        self._history_by_session: dict[str, InMemoryChatMessageHistory] = {}

        llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=temperature,
            google_api_key=api_key,
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_prompt}"),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )
        chain = prompt | llm
        self._chain = RunnableWithMessageHistory(
            chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def ask(self, message: str, session_id: str = "default") -> dict[str, object]:
        guardrail = evaluate_guardrails(message)
        facts = self._facts_by_session.get(session_id, {})

        if not guardrail.allowed:
            return {
                "answer": guardrail.message,
                "facts": facts,
                "guardrail_category": guardrail.category,
                "model": "guardrail",
                "estimated_tokens": estimate_tokens(guardrail.message),
            }

        facts = update_facts(message, facts)
        self._facts_by_session[session_id] = facts
        context = build_context(facts)

        response = self._chain.invoke(
            {
                "input": message,
                "system_prompt": system_prompt(context=context, facts=facts),
            },
            config={"configurable": {"session_id": session_id}},
        )
        answer = str(getattr(response, "content", response)).strip()

        if guardrail.message:
            answer = f"{guardrail.message}\n\n{answer}"

        return {
            "answer": answer,
            "facts": facts,
            "guardrail_category": guardrail.category,
            "model": self.model_name,
            "estimated_tokens": estimate_tokens(answer),
        }

    def _get_history(self, session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in self._history_by_session:
            self._history_by_session[session_id] = InMemoryChatMessageHistory()
        return self._history_by_session[session_id]
