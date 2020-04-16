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
    grid: list
    population: float = 0
    time: float = 0


def generations(height, width, population, rulestring, random_seed=None):
    gen = first_generation(height, width, population, random_seed)
    rules = util.parse_rulestring(rulestring)
    while True:
        yield gen
        gen = next_generation(gen.grid, rules)


def first_generation(height, width, population, random_seed=None):
    start_time = t.time()
    grid = np.full((height, width), DEAD_CELL, CELL_TYPE)
    pop = int(height * width * (population / 100))
    cells = tuple(it.product(range(height), range(width)))
    rand.seed(random_seed)
    for x, y in rand.sample(cells, pop):
        grid[x, y] = LIVE_CELL
    return Generation(grid=grid, population=pop, time=t.time()-start_time)


def neighbors(grid):
    neighborhood = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    return sp.convolve2d(grid, np.array(neighborhood), mode='same',
                         boundary='wrap', fillvalue=DEAD_CELL).round()


def next_generation(grid, rules):
    start_time = t.time()
    neighbor_grid = neighbors(grid)
    next_grid = np.full(grid.shape, DEAD_CELL, CELL_TYPE)
    population = 0

    for n in rules.birth:
        w = np.where((grid == DEAD_CELL) & (neighbor_grid == n))
        next_grid[w] = LIVE_CELL
        population += len(w[0])

    for n in rules.survival:
        w = np.where((grid == LIVE_CELL) & (neighbor_grid == n))
        next_grid[w] = LIVE_CELL
        population += len(w[0])

    return Generation(grid=next_grid, population=population,
                      time=t.time()-start_time)
