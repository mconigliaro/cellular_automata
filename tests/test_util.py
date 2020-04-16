import cellular_automata.exceptions as exc
import cellular_automata.util as util
import pytest as pt


def test_list_visualizations():
    assert util.list_visualizations() == ['curses', 'none']


@pt.mark.parametrize(
    "rulestring, rules",
    [
        ["b01/s23", util.Rules(birth=(0, 1), survival=(2, 3))],
        ["23/01", util.Rules(survival=(2, 3), birth=(0, 1))]
    ]
)
def test_parse_rulestring(rulestring, rules):
    assert util.parse_rulestring(rulestring) == rules


@pt.mark.parametrize(
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
    with pt.raises(exc.RulestringParseError):
        print(util.parse_rulestring(rulestring))
