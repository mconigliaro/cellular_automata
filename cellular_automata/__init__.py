import cellular_automata.util as util
import itertools as it
import numpy as np
import random as rand
import scipy.signal as sp
import time as t
import typing as ty


CELL_TYPE = int
DEAD_CELL = 0
LIVE_CELL = 1


class Generation(ty.NamedTuple):
    universe: list
    population: float = 0
    time: float = 0


def generations(height, width, population, topology, rulestring,
                random_seed=None):
    gen = first_generation(height, width, population, random_seed)
    rules = util.parse_rulestring(rulestring)
    while True:
        yield gen
        gen = next_generation(gen.universe, topology, rules)


def first_generation(height, width, population, random_seed=None):
    start_time = t.time()
    universe = np.full((height, width), DEAD_CELL, CELL_TYPE)
    pop = int(height * width * (population / 100))
    cells = tuple(it.product(range(height), range(width)))
    rand.seed(random_seed)
    for x, y in rand.sample(cells, pop):
        universe[x, y] = LIVE_CELL

    return Generation(universe=universe, population=pop,
                      time=t.time()-start_time)


def count_neighbors(universe, topology):
    neighborhood = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    boundary = {
        "closed": "fill",
        "wrapped": "wrap"
    }[topology]

    return sp.convolve2d(universe, neighborhood, mode='same',
                         boundary=boundary, fillvalue=DEAD_CELL)


def next_generation(universe, topology, rules):
    start_time = t.time()
    neighbors = count_neighbors(universe, topology)
    next_universe = np.full(universe.shape, DEAD_CELL, CELL_TYPE)
    next_universe[np.where(
        np.isin(neighbors, rules.birth)
        | (universe == LIVE_CELL) & np.isin(neighbors, rules.survival)
    )] = LIVE_CELL

    return Generation(universe=next_universe,
                      population=np.count_nonzero(next_universe),
                      time=t.time()-start_time)
