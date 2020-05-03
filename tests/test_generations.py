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
def gen(height, width):
    return next(ca.generations(height, width, 10, 'wrapped', 'b3/s23'))


def test_generations(height, width, gen):
    assert isinstance(gen, ca.Generation)
    assert len(gen.universe) == height
    for x in gen.universe:
        assert len(x) == width
        for y in x:
            assert y in (ca.DEAD_CELL, ca.LIVE_CELL)
