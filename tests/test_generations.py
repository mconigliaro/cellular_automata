from game_of_life import Generation, generations
import pytest
from random import randint


@pytest.fixture
def height():
    return randint(3, 15)


@pytest.fixture
def width():
    return randint(3, 15)


@pytest.fixture
def gen(height, width):
    return next(generations(height, width, 10))


def test_generations(height, width, gen):
    assert isinstance(gen, Generation)
    assert len(gen.grid) == height
    for x in gen.grid:
        assert len(x) == width
        for y in x:
            assert y in (0, 1)
