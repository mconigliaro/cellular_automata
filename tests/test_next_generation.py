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


@pt.fixture
def neighborhood():
    return [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]


def test_next_generation(grids, neighborhood):
    for grid1, grid2 in grids:
        rules = ca._parse_rulestring('b3/s23')
        grid1 = np.array(grid1)
        next_gen = ca._next_generation(grid1, rules, neighborhood).grid.tolist()
        assert next_gen == grid2
