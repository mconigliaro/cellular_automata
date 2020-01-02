import collections as col
import itertools as it
import numpy as np
import random as rn
import re
import scipy.signal as sp
import time as t


CELL_TYPE = int
DEAD_CELL = 0
LIVE_CELL = 1

Generation = col.namedtuple('Generation',
                            ['grid', 'population', 'time'],
                            defaults=[0, 0])

Rules = col.namedtuple('Rules', ['birth', 'survival'], defaults=[(), ()])


def generations(height, width, population, rulestring):
    gen = _first_generation(height, width, population)
    rules = _parse_rulestring(rulestring)
    while True:
        yield gen
        gen = _next_generation(gen.grid, rules)


def _first_generation(height, width, population):
    start_time = t.time()
    grid = np.full((height, width), DEAD_CELL, CELL_TYPE)
    pop = int(height * width * (population / 100))
    cells = tuple(it.product(range(height), range(width)))
    for x, y in rn.sample(cells, pop):
        grid[x, y] = LIVE_CELL
    return Generation(grid=grid, population=pop, time=t.time()-start_time)


def _neighbors(grid):
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    return sp.fftconvolve(grid, kernel, 'same').round()


def _next_generation(grid, rules):
    start_time = t.time()
    neighbors = _neighbors(grid)
    next_grid = np.full(grid.shape, DEAD_CELL, CELL_TYPE)
    population = 0

    for n in rules.birth:
        w = np.where((grid == DEAD_CELL) & (neighbors == n))
        next_grid[w] = LIVE_CELL
        population += len(w[0])

    for n in rules.survival:
        w = np.where((grid == LIVE_CELL) & (neighbors == n))
        next_grid[w] = LIVE_CELL
        population += len(w[0])

    return Generation(grid=next_grid, population=population,
                      time=t.time()-start_time)


def _parse_rulestring(rulestring):
    match = re.match(r'b(\d*)\/s(\d*)', rulestring, re.IGNORECASE)
    if match:
        birth = tuple(int(x) for x in match[1])
        survival = tuple(int(x) for x in match[2])
    else:
        birth = tuple()
        survival = tuple()
    return Rules(birth=birth, survival=survival)
