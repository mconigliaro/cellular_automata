import cellular_automata as ca
import pytest as pt
import random as rand


@pt.fixture
def height():
    return rand.randint(3, 15)


@pt.fixture
def width():
    return rand.randint(3, 15)


@pt.fixture
def neighborhood():
    return [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]


@pt.fixture
def gen(height, width, neighborhood):
    return next(ca.generations(height, width, 10, 'b3/s23', neighborhood))


def test_generations(height, width, gen):
    assert isinstance(gen, ca.Generation)
    assert len(gen.grid) == height
    for x in gen.grid:
        assert len(x) == width
        for y in x:
            assert y in (0, 1)
