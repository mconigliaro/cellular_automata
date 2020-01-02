import cellular_automata as ca
import pytest as pt
import random as rn


@pt.fixture
def height():
    return rn.randint(3, 15)


@pt.fixture
def width():
    return rn.randint(3, 15)


@pt.fixture
def gen(height, width):
    return next(ca.generations(height, width, 10, 'b3/s23'))


def test_generations(height, width, gen):
    assert isinstance(gen, ca.Generation)
    assert len(gen.grid) == height
    for x in gen.grid:
        assert len(x) == width
        for y in x:
            assert y in (0, 1)
