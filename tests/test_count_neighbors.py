import pytest

import cellular_automata as ca


@pytest.fixture
def universe():
    return [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]


@pytest.mark.parametrize(
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
def test_count_neighbors(universe, x, y, count):
    assert ca.count_neighbors(universe, 'closed')[x][y] == count
