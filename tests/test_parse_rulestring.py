import pytest

import cellular_automata as ca


@pytest.mark.parametrize(
    "rulestring, rules",
    [
        ["b01/s23", ca.Rules(birth=(0, 1), survival=(2, 3))],
        ["23/01", ca.Rules(survival=(2, 3), birth=(0, 1))]
    ]
)
def test_parse_rulestring(rulestring, rules):
    assert ca.parse_rulestring(rulestring) == rules


@pytest.mark.parametrize(
    "rulestring",
    [
        "b/s",
        "b9/",
        "/s9",
        "/",
        ""
    ]
)
def test_parse_invalid_rulestring(rulestring):
    with pytest.raises(ValueError):
        ca.parse_rulestring(rulestring)
