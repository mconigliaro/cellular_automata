import cellular_automata as ca
import pytest as pt


@pt.fixture
def grid():
    return [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15]
    ]


@pt.fixture
def neighborhood():
    return [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]


@pt.mark.parametrize(
    "x, y, count",
    [
        [0, 0, 1 + 4 + 5],
        [0, 3, 2 + 6 + 7],
        [1, 1, (0 + 1 + 2) + (4 + 6) + (8 + 9 + 10)],
        [1, 2, (1 + 2 + 3) + (5 + 7) + (9 + 10 + 11)],
        [2, 1, (4 + 5 + 6) + (8 + 10) + (12 + 13 + 14)],
        [2, 2, (5 + 6 + 7) + (9 + 11) + (13 + 14 + 15)],
        [3, 0, 8 + 9 + 13],
        [3, 3, 10 + 11 + 14]
    ]
)
def test_neighbors(grid, neighborhood, x, y, count):
    assert ca._neighbors(grid, neighborhood)[x][y] == count
