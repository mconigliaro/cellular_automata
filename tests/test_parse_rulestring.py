import cellular_automata as ca


def test_parse_rulestring():
    assert ca._parse_rulestring('b01/s23') == ca.Rules(birth=(0, 1),
                                                       survival=(2, 3))
    assert ca._parse_rulestring('b01/s') == ca.Rules(birth=(0, 1))
    assert ca._parse_rulestring('b/s01') == ca.Rules(survival=(0, 1))
    assert ca._parse_rulestring('b/s') == ca.Rules()
    assert ca._parse_rulestring('') == ca.Rules()
