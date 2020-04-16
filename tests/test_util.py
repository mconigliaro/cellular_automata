import cellular_automata.exceptions as exc
import cellular_automata.util as util
import pytest as pt


def test_list_visualizations():
    assert util.list_visualizations() == ['curses', 'none']


@pt.mark.parametrize(
    "rulestring, rules",
    [
        # B/S
        ["b01/s23", util.Rules(birth=(0, 1), survival=(2, 3))],
        ["b01/s", util.Rules(birth=(0, 1))],
        ["b/s01", util.Rules(survival=(0, 1))],
        ["b/s", util.Rules()],

        # S/B
        ["23/01", util.Rules(survival=(2, 3), birth=(0, 1))],
        ["01/", util.Rules(survival=(0, 1))],
        ["/01", util.Rules(birth=(0, 1))],
        ["/", util.Rules()],
    ]
)
def test_parse_rulestring(rulestring, rules):
    assert util.parse_rulestring(rulestring) == rules


@pt.mark.parametrize(
    "rulestring",
    [
        "invalid",
        ""
    ]
)
def test_parse_invalid_rulestring(rulestring):
    with pt.raises(exc.RulestringParseError):
        util.parse_rulestring(rulestring)
