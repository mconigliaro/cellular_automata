from game_of_life import grid
import pytest


@pytest.fixture
def h():
    return 99


@pytest.fixture
def w():
    return 100


@pytest.fixture
def g(h, w):
    return grid(h, w)


def test_grid(h, w, g):
    assert len(g) == h
    for x in g:
        assert len(x) == w
        for y in x:
            assert y in (0, 1)
