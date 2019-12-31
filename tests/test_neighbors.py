from cellular_automata import _neighbors
import pytest


@pytest.fixture
def grid():
    return [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15]
    ]


def test_neighbors(grid):
    assert _neighbors(grid, 0, 0) == 1 + 4 + 5
    assert _neighbors(grid, 0, 3) == 2 + 6 + 7
    assert _neighbors(grid, 1, 1) == (0 + 1 + 2) + (4 + 6) + (8 + 9 + 10)
    assert _neighbors(grid, 1, 2) == (1 + 2 + 3) + (5 + 7) + (9 + 10 + 11)
    assert _neighbors(grid, 2, 1) == (4 + 5 + 6) + (8 + 10) + (12 + 13 + 14)
    assert _neighbors(grid, 2, 2) == (5 + 6 + 7) + (9 + 11) + (13 + 14 + 15)
    assert _neighbors(grid, 3, 0) == 8 + 9 + 13
    assert _neighbors(grid, 3, 3) == 10 + 11 + 14
