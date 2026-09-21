from __future__ import annotations

import argparse

from .agent import ChargeGridAgent
from .models import ConservativeChargeGridModel, OllamaChargeGridModel, RuleBasedChargeGridModel


def build_model(name: str):
    if name == "conservative":
        return ConservativeChargeGridModel()
    if name.startswith("ollama:"):
        return OllamaChargeGridModel(model_name=name.removeprefix("ollama:"))
    return RuleBasedChargeGridModel()


def main() -> None:
    parser = argparse.ArgumentParser(description="ChargeGrid Intelligence CLI")
    parser.add_argument("--session", default="demo", help="Identificador da sessao conversacional")
    parser.add_argument("--model", default="rule", help="rule, conservative ou ollama:<modelo>")
    args = parser.parse_args()

    agent = ChargeGridAgent(model=build_model(args.model))
    print("ChargeGrid Intelligence - digite 'sair' para encerrar.")
    while True:
        question = input("Voce: ").strip()
        if question.lower() in {"sair", "exit", "quit"}:
            break
        result = agent.ask(question, session_id=args.session)
        print(f"ChargeGrid: {result['answer']}\n")


if __name__ == "__main__":
    main()
