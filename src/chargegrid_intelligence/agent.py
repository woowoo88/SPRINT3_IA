from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from .guardrails import evaluate_guardrails
from .knowledge import build_context
from .memory import update_facts
from .models import RuleBasedChargeGridModel


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    facts: dict[str, str]
    guardrail_category: str
    context: str
    model_name: str
    estimated_tokens: int


class ChargeGridAgent:
    """LangGraph agent for ChargeGrid Intelligence."""

    def __init__(self, model=None):
        self.model = model or RuleBasedChargeGridModel()
        self.graph = self._build_graph()

    def ask(self, message: str, session_id: str = "default") -> dict[str, object]:
        result = self.graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config={"configurable": {"thread_id": session_id}},
        )
        answer = result["messages"][-1].content
        return {
            "answer": answer,
            "facts": result.get("facts", {}),
            "guardrail_category": result.get("guardrail_category", "ok"),
            "model": result.get("model_name", getattr(self.model, "name", "unknown")),
            "estimated_tokens": result.get("estimated_tokens", 0),
        }

    def _build_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("guardrails", self._guardrails_node)
        workflow.add_node("memory", self._memory_node)
        workflow.add_node("context", self._context_node)
        workflow.add_node("respond", self._respond_node)

        workflow.add_edge(START, "guardrails")
        workflow.add_conditional_edges(
            "guardrails",
            self._route_guardrails,
            {"blocked": END, "allowed": "memory"},
        )
        workflow.add_edge("memory", "context")
        workflow.add_edge("context", "respond")
        workflow.add_edge("respond", END)

        return workflow.compile(checkpointer=MemorySaver())

    def _guardrails_node(self, state: AgentState) -> dict[str, object]:
        text = _last_user_message(state["messages"])
        result = evaluate_guardrails(text)
        updates: dict[str, object] = {"guardrail_category": result.category}
        if not result.allowed:
            updates["messages"] = [AIMessage(content=result.message)]
            updates["estimated_tokens"] = max(1, round(len(result.message.split()) * 1.35))
            updates["model_name"] = "guardrail"
        elif result.message:
            updates["messages"] = [AIMessage(content=result.message)]
        return updates

    def _route_guardrails(self, state: AgentState) -> str:
        return "blocked" if state.get("model_name") == "guardrail" else "allowed"

    def _memory_node(self, state: AgentState) -> dict[str, object]:
        facts = state.get("facts") or {}
        return {"facts": update_facts(_last_user_message(state["messages"]), facts)}

    def _context_node(self, state: AgentState) -> dict[str, object]:
        return {"context": build_context(state.get("facts") or {})}

    def _respond_node(self, state: AgentState) -> dict[str, object]:
        text = _last_user_message(state["messages"])
        response = self.model.generate(text, state.get("context", ""), state.get("facts") or {})
        prefix = ""
        if state.get("guardrail_category") in {"legal_caution", "financial_caution"}:
            prefix = state["messages"][-1].content + "\n\n"
        return {
            "messages": [AIMessage(content=prefix + response.content)],
            "model_name": response.model_name,
            "estimated_tokens": response.estimated_tokens,
        }


def _last_user_message(messages: list[BaseMessage]) -> str:
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return str(message.content)
    return ""
