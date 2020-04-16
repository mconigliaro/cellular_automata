import cellular_automata as ca
import pytest as pt


@pt.fixture
def grid():
    return [
        [0, 0, 0, 0, 0],
        [0, 1, 2, 3, 0],
        [0, 4, 5, 6, 0],
        [0, 7, 8, 9, 0],
        [0, 0, 0, 0, 0]
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
        [1, 1, 2 + 4 + 5],
        [1, 2, (1 + 3) + (4 + 5 + 6)],
        [1, 3, 2 + 5 + 6],
        [2, 1, (1 + 2) + 5 + (7 + 8)],
        [2, 2, (1 + 2 + 3) + (4 + 6) + (7 + 8 + 9)],
        [2, 3, (2 + 3) + 5 + (8 + 9)],
        [3, 1, (4 + 5) + 8],
        [3, 2, (4 + 5 + 6) + (7 + 9)],
        [3, 3, (5 + 6) + 8]
    ]
)
def test_neighbors(grid, neighborhood, x, y, count):
    assert ca.neighbors(grid, neighborhood)[x][y] == count
