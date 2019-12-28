from game_of_life import Generation, next_generation
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
        assert next_generation(Generation(grid=grid1)).grid == grid2
