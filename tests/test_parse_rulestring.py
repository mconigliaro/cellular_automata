import cellular_automata as ca
import pytest as pt


@pt.mark.parametrize(
    "rulestring, rules",
    [
        ["b01/s23", ca.Rules(birth=(0, 1), survival=(2, 3))],
        ["b01/s", ca.Rules(birth=(0, 1))],
        ["b/s01", ca.Rules(survival=(0, 1))],
        ["b/s", ca.Rules()],
        ["", ca.Rules()],
    ]
)
def test_parse_rulestring(rulestring, rules):
    assert ca._parse_rulestring(rulestring) == rules
