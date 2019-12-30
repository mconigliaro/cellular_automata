from game_of_life import _parse_rulestring, Rules


def test_parse_rulestring():
    assert _parse_rulestring('b0/s12') == Rules(birth=(0,), survival=(1, 2))
    assert _parse_rulestring('b/s01') == Rules(birth=(), survival=(0, 1))
    assert _parse_rulestring('b/s') == Rules(birth=(), survival=())
    assert _parse_rulestring('') == Rules(birth=(), survival=())
