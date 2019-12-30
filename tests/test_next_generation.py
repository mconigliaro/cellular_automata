from game_of_life import Generation, _next_generation, _parse_rulestring
import pytest


@pytest.fixture
def grids():
    return [
        ([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ], [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),

        ([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ], [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]),

        ([
            [1, 0, 1],
            [0, 1, 0],
            [0, 0, 1]
        ], [
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ])
    ]


def test_next_generation(grids):
    for grid1, grid2 in grids:
        g = Generation(grid=grid1)
        rules = _parse_rulestring('b3/s23')
        assert _next_generation(g, rules).grid == grid2
