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


def neighbors(universe, topology):
    neighborhood = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    boundary = {
        "closed": "fill",
        "wrapped": "wrap"
    }[topology]
    return sp.convolve2d(universe, neighborhood, mode='same',
                         boundary=boundary, fillvalue=DEAD_CELL)


def next_generation(universe, topology, rules):
    start_time = t.time()
    neighbor_universe = neighbors(universe, topology)
    next_universe = np.full(universe.shape, DEAD_CELL, CELL_TYPE)
    population = 0

    for n in rules.birth:
        w = np.where((universe == DEAD_CELL) & (neighbor_universe == n))
        next_universe[w] = LIVE_CELL
        population += len(w[0])

    for n in rules.survival:
        w = np.where((universe == LIVE_CELL) & (neighbor_universe == n))
        next_universe[w] = LIVE_CELL
        population += len(w[0])

    return Generation(universe=next_universe, population=population,
                      time=t.time()-start_time)
