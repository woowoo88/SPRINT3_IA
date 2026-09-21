PROJECT_CONTEXT = """
ChargeGrid Intelligence é uma plataforma acadêmica para orquestrar recarga
comercial de veículos elétricos no contexto do EV Challenge GoodWe/FIAP.

Escopo da solução:
- gerenciamento automatizado de infraestrutura comercial de recarga;
- controle de demanda e balanceamento de potência entre pontos de recarga;
- registro do ciclo da sessão: início, fim, energia consumida, status e custo;
- integração conceitual com EV Charger instalado na FIAP e ecossistema digital GoodWe;
- comunicação prevista por OCPP para eletropostos e MODBUS para medidores/controladores;
- aplicação de regras de cobrança dinâmica conforme horário, demanda e tipo de usuário.

Dados de demonstração:
- site padrão: Campus FIAP - unidade demonstrativa;
- conectores simulados: CG-01, CG-02, CG-03 e CG-04;
- limite operacional demonstrativo: 22 kW por carregador AC;
- janela de menor demanda simulada: 22h às 6h;
- a plataforma deve recomendar verificação com profissional habilitado para qualquer
  alteração elétrica, manutenção, instalação ou situação de risco.

Restrições:
- não inventar especificações técnicas reais da GoodWe;
- diferenciar dados simulados de dados reais;
- não oferecer aconselhamento jurídico ou financeiro profissional;
- não orientar bypass de proteções elétricas, abertura de equipamentos ou manutenção perigosa.
"""


def build_context(facts: dict[str, str]) -> str:
    memory_lines = []
    if facts:
        memory_lines.append("Memória da sessão:")
        for key, value in sorted(facts.items()):
            memory_lines.append(f"- {key}: {value}")

    return PROJECT_CONTEXT + "\n" + "\n".join(memory_lines)
