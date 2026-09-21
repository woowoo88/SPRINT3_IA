from chargegrid_intelligence import ScopeGuardAgent


def test_blocks_out_of_scope_question():
    guard = ScopeGuardAgent()
    result = guard.evaluate("qual a receita de bolo?")

    assert result.allowed is False
    assert result.category == "out_of_scope"


def test_allows_chargegrid_question_without_context():
    guard = ScopeGuardAgent()
    result = guard.evaluate("quantas vagas de recarga temos disponíveis?")

    assert result.allowed is True


def test_allows_short_follow_up_with_context():
    guard = ScopeGuardAgent()
    result = guard.evaluate("e quais estão livres?", has_context=True)

    assert result.allowed is True
