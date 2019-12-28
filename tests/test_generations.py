from game_of_life import Generation, first_generation, generations
import pytest
from random import randint


@pytest.fixture
def height():
    return randint(1, 100)


@pytest.fixture
def width():
    return randint(1, 100)


@pytest.fixture
def gen(height, width):
    return next(generations(first_generation(height, width)))


def test_generations(height, width, gen):
    assert isinstance(gen, Generation)
    assert len(gen.grid) == height
    for x in gen.grid:
        assert len(x) == width
        for y in x:
            assert y in (0, 1)
