from __future__ import annotations

import re


def update_facts(text: str, facts: dict[str, str]) -> dict[str, str]:
    """Extract simple session facts from the user's message."""
    updated = dict(facts)
    normalized = text.strip()

    site_match = re.search(
        r"(?:condominio|condomínio|eletroposto|campus|unidade)\s+([A-Za-zÀ-ÿ0-9 ._-]{2,40})",
        normalized,
        re.IGNORECASE,
    )
    if site_match:
        updated["local_mencionado"] = site_match.group(1).strip(" .")

    vagas_match = re.search(
        r"(?:existem|temos|tenho|ha|há|sao|são|possui)\s+(\d+)\s+(?:vagas|conectores|carregadores|pontos)",
        normalized,
        re.IGNORECASE,
    )
    if vagas_match:
        updated["quantidade_pontos"] = vagas_match.group(1)

    tarifa_match = re.search(
        r"(?:tarifa|preco|preço|valor)\s+(?:de\s+)?R?\$?\s*([0-9]+(?:[,.][0-9]{1,2})?)",
        normalized,
        re.IGNORECASE,
    )
    if tarifa_match:
        updated["tarifa_informada"] = "R$ " + tarifa_match.group(1).replace(".", ",")

    perfil_match = re.search(
        r"\b(?:sou|perfil de)\s+(sindico|síndico|operador|gestor|motorista|tecnico|técnico)\b",
        normalized,
        re.IGNORECASE,
    )
    if perfil_match:
        updated["perfil_usuario"] = perfil_match.group(1).lower()

    return updated
