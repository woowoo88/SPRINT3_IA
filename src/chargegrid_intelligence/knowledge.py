PROJECT_CONTEXT = """
ChargeGrid Intelligence e uma plataforma academica para orquestrar recarga
comercial de veiculos eletricos no contexto do EV Challenge GoodWe/FIAP.

Escopo da solucao:
- gerenciamento automatizado de infraestrutura comercial de recarga;
- controle de demanda e balanceamento de potencia entre pontos de recarga;
- registro do ciclo da sessao: inicio, fim, energia consumida, status e custo;
- integracao conceitual com EV Charger instalado na FIAP e ecossistema digital GoodWe;
- comunicacao prevista por OCPP para eletropostos e MODBUS para medidores/controladores;
- aplicacao de regras de cobranca dinamica conforme horario, demanda e tipo de usuario.

Dados de demonstracao:
- site padrao: Campus FIAP - unidade demonstrativa;
- conectores simulados: CG-01, CG-02, CG-03 e CG-04;
- limite operacional demonstrativo: 22 kW por carregador AC;
- janela de menor demanda simulada: 22h as 6h;
- a plataforma deve recomendar verificacao com profissional habilitado para qualquer
  alteracao eletrica, manutencao, instalacao ou situacao de risco.

Restricoes:
- nao inventar especificacoes tecnicas reais da GoodWe;
- diferenciar dados simulados de dados reais;
- nao oferecer aconselhamento juridico ou financeiro profissional;
- nao orientar bypass de protecoes eletricas, abertura de equipamentos ou manutencao perigosa.
"""


def build_context(facts: dict[str, str]) -> str:
    memory_lines = []
    if facts:
        memory_lines.append("Memoria da sessao:")
        for key, value in sorted(facts.items()):
            memory_lines.append(f"- {key}: {value}")

    return PROJECT_CONTEXT + "\n" + "\n".join(memory_lines)
