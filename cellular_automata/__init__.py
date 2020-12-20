import itertools
import numpy
import random
import re
import scipy.signal as signal
import time as t
import typing


CELL_TYPE = int
DEAD_CELL = 0
LIVE_CELL = 1


class Rules(typing.NamedTuple):
    birth: tuple = ()
    survival: tuple = ()


class Generation(typing.NamedTuple):
    universe: list
    population: float = 0
    time: float = 0


def parse_rulestring(rulestring):
    bs_match = re.match(r'b([0-8]+)\/s([0-8]+)', rulestring, re.IGNORECASE)
    if bs_match:
        return Rules(birth=tuple(int(x) for x in bs_match[1]),
                     survival=tuple(int(x) for x in bs_match[2]))

    sb_match = re.match(r'([0-8]+)\/([0-8]+)', rulestring, re.IGNORECASE)
    if sb_match:
        return Rules(survival=tuple(int(x) for x in sb_match[1]),
                     birth=tuple(int(x) for x in sb_match[2]))

    raise ValueError(f"Unable to parse rulestring: {rulestring}")


def generations(height, width, population, topology, rulestring,
                random_seed=None):
    gen = first_generation(height, width, population, random_seed)
    rules = parse_rulestring(rulestring)
    while True:
        yield gen
        gen = next_generation(gen.universe, topology, rules)


def first_generation(height, width, population, random_seed=None):
    start_time = t.time()
    universe = numpy.full((height, width), DEAD_CELL, CELL_TYPE)
    pop = int(height * width * (population / 100))
    cells = tuple(itertools.product(range(height), range(width)))
    random.seed(random_seed)
    for x, y in random.sample(cells, pop):
        universe[x, y] = LIVE_CELL

    return Generation(universe=universe, population=pop,
                      time=t.time()-start_time)


def count_neighbors(universe, topology):
    neighborhood = numpy.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    boundary = {
        "closed": "fill",
        "wrapped": "wrap"
    }[topology]

    return signal.convolve2d(universe, neighborhood, mode='same',
                             boundary=boundary, fillvalue=DEAD_CELL)


def next_generation(universe, topology, rules):
    start_time = t.time()
    neighbors = count_neighbors(universe, topology)
    next_universe = numpy.full(universe.shape, DEAD_CELL, CELL_TYPE)
    next_universe[numpy.where(
        numpy.isin(neighbors, rules.birth)
        | (universe == LIVE_CELL) & numpy.isin(neighbors, rules.survival)
    )] = LIVE_CELL

    return Generation(universe=next_universe,
                      population=numpy.count_nonzero(next_universe),
                      time=t.time()-start_time)
