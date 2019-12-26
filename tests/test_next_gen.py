from game_of_life import next_gen


def test_next_gen1():
    a = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    b = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert next_gen(a) == b


def test_next_gen2():
    a = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    b = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert next_gen(a) == b


def test_next_gen3():
    a = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    b = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    assert next_gen(a) == b


def test_next_gen4():
    a = [
        [1, 0, 1],
        [0, 1, 0],
        [0, 0, 1]
    ]
    b = [
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]
    assert next_gen(a) == b
