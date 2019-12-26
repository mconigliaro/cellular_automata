from game_of_life import next_generation
import pytest


@pytest.fixture
def generations():
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


def test_next_generation(generations):
    for g1, g2 in generations:
        assert next_generation(g1) == g2
