from chargegrid_intelligence import ChargeGridAgent


def main() -> None:
    agent = ChargeGridAgent()
    print("ChargeGrid pronto. Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("Usuário: ").strip()
        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("ChargeGrid: sessão encerrada.")
            break

        resposta = agent.ask(pergunta, session_id="demo")
        print(f"ChargeGrid: {resposta['answer']}\n")


if __name__ == "__main__":
    main()
