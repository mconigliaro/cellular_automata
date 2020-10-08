import cellular_automata.options as options


def test_list_visualizations():
    assert options.list_visualizations() == ['curses', 'none']
