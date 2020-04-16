import cellular_automata as ca
import pytest as pt


@pt.fixture
def grid():
    return [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]


@pt.mark.parametrize(
    "x, y, count",
    [
        [0, 0, 2 + 4 + 5],
        [0, 1, (1 + 3) + (4 + 5 + 6)],
        [0, 2, 2 + 5 + 6],
        [1, 0, (1 + 2) + 5 + (7 + 8)],
        [1, 1, (1 + 2 + 3) + (4 + 6) + (7 + 8 + 9)],
        [1, 2, (2 + 3) + 5 + (8 + 9)],
        [2, 0, (4 + 5) + 8],
        [2, 1, (4 + 5 + 6) + (7 + 9)],
        [2, 2, (5 + 6) + 8]
    ]
)
def test_neighbors(grid, x, y, count):
    assert ca.neighbors(grid, 'closed')[x][y] == count
