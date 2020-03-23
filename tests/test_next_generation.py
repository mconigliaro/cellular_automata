import cellular_automata as ca
import numpy as np
import pytest as pt


@pt.fixture
def rules():
    return ca._parse_rulestring('b3/s23')


@pt.fixture
def neighborhood():
    return [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]


@pt.mark.parametrize(
    "grid1, grid2",
    [
        [np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]), [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]],

        [np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]), [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]],

        [np.array([
            [1, 0, 1],
            [0, 1, 0],
            [0, 0, 1]
        ]), [
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ]]
    ]
)
def test_next_generation(rules, neighborhood, grid1, grid2):
    next_gen = ca._next_generation(grid1, rules, neighborhood).grid.tolist()
    assert next_gen == grid2
