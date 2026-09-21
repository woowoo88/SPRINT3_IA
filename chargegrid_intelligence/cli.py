from __future__ import annotations

import argparse

from .agent import ChargeGridAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="ChargeGrid Intelligence CLI")
    parser.add_argument("--session", default="demo", help="Identificador da sessão conversacional")
    args = parser.parse_args()

    agent = ChargeGridAgent()
    print("ChargeGrid Intelligence - digite 'sair' para encerrar.")
    while True:
        question = input("Você: ").strip()
        if question.lower() in {"sair", "exit", "quit"}:
            break
        result = agent.ask(question, session_id=args.session)
        print(f"ChargeGrid: {result['answer']}\n")


if __name__ == "__main__":
    main()
