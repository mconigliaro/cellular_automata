import cellular_automata.cli


def test_list_visualizations():
    assert cellular_automata.cli.list_visualizations() == ["curses", "none"]
