from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "relatorio_evolucao_chargegrid.pdf"


def paragraph(text: str, style):
    return Paragraph(text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), style)


def build_pdf() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.8, leading=11))
    styles.add(ParagraphStyle(name="Tiny", parent=styles["BodyText"], fontSize=7.6, leading=9))

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=1.4 * cm,
        leftMargin=1.4 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
        title="Relatório de Evolução - ChargeGrid Intelligence",
    )

    story = []
    story.append(paragraph("Relatório de Evolução - ChargeGrid Intelligence", styles["Title"]))
    story.append(paragraph("EV Challenge GoodWe - Sprint 03 - Agentes de IA e Evolução Conversacional", styles["Small"]))
    story.append(Spacer(1, 0.25 * cm))

    sections = [
        (
            "1. Resumo da evolução",
            "Nas Sprints 1 e 2, o ChargeWise AI era um chatbot em Python com Ollama, system prompt, few-shot, histórico manual e filtro por palavras-chave. Na Sprint 03, o projeto evoluiu para o ChargeGrid Intelligence, focado em recarga comercial, controle de demanda, registro de sessões, OCPP/MODBUS e cobrança dinâmica. A principal mudança foi refatorar o núcleo conversacional para um agente em LangGraph.",
        ),
        (
            "2. Refatoração",
            "O LangGraph foi escolhido por permitir organizar a conversa como grafo de estados. O fluxo possui nós de guardrails, memória, contexto e resposta. A memória por sessão usa thread_id e checkpointer em memória, permitindo recuperar dados informados pelo usuário sem misturar sessões diferentes. O projeto também separa conhecimento, modelos e validações em módulos próprios.",
        ),
    ]
    for title, body in sections:
        story.append(paragraph(title, styles["Heading2"]))
        story.append(paragraph(body, styles["Small"]))

    story.append(paragraph("3. Comparativo antes x depois", styles["Heading2"]))
    table_data = [
        ["Critério", "Sprints 1 e 2", "Sprint 03"],
        ["Arquitetura", "Script monolítico", "Agente LangGraph com nós"],
        ["Memória", "Histórico manual", "Memória por sessão"],
        ["Segurança", "Filtro simples", "Guardrails por categoria"],
        ["Modelos", "Llama 3.2 1B", "rule-v1, conservative-v1, Ollama opcional"],
        ["Testes", "Manuais", "Pytest + casos documentados"],
    ]
    table = Table(table_data, colWidths=[3.1 * cm, 6.1 * cm, 7.0 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("LEADING", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(table)

    story.append(paragraph("4. Problemas encontrados e soluções", styles["Heading2"]))
    problems = [
        "Baixa separação de responsabilidades: a solução foi modularizar o pacote em agente, memória, guardrails, conhecimento e modelos.",
        "Dependência de um único modelo local: a solução foi criar modelos offline para testes e deixar Ollama como adaptador opcional.",
        "Risco de prompt injection e respostas perigosas: a solução foi executar guardrails antes da etapa de resposta.",
    ]
    for item in problems:
        story.append(paragraph("- " + item, styles["Small"]))

    story.append(paragraph("5. Conclusão", styles["Heading2"]))
    story.append(
        paragraph(
            "A nova arquitetura tornou o chatbot mais robusto porque separou fluxo, memória, segurança e modelo. O resultado é uma entrega acadêmica funcional, testável e mais próxima de uma aplicação real para orquestração de recarga comercial.",
            styles["Small"],
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT)
