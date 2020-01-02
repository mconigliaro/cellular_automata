import cellular_automata as ca
import numpy as np
import pytest as pt


@pt.fixture
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
        rules = ca._parse_rulestring('b3/s23')
        grid1 = np.array(grid1)
        assert ca._next_generation(grid1, rules).grid.tolist() == grid2
