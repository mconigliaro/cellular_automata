from collections import namedtuple
from itertools import product
from random import sample
import re
from numpy import array, full, ndenumerate
from scipy.signal import fftconvolve
import time


DEAD_CELL = 0
LIVE_CELL = 1

Generation = namedtuple('Generation',
                        ['grid', 'born', 'died', 'survived', 'time'],
                        defaults=[0, 0, 0, 0])

Rules = namedtuple('Rules', ['birth', 'survival'])


def generations(height, width, population, rulestring):
    gen = _first_generation(height, width, population)
    rules = _parse_rulestring(rulestring)
    while True:
        yield gen
        gen = _next_generation(gen.grid, rules)


def _first_generation(height, width, population):
    start_time = time.time()
    grid = full((height, width), DEAD_CELL, int)
    born = int(height * width * (population / 100))
    for x, y in sample(tuple(product(range(height), range(width))), born):
        grid[x][y] = LIVE_CELL
    return Generation(grid=grid, born=born, time=time.time()-start_time)


def _neighbors(grid):
    kernel = array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    return fftconvolve(grid, kernel, 'same').round()


def _next_generation(grid, rules):
    start_time = time.time()
    neighbors = _neighbors(grid)
    next_grid = full(grid.shape, DEAD_CELL, int)
    born = 0
    died = 0
    survived = 0
    for (x, y), cell in ndenumerate(grid):
        if cell == DEAD_CELL and neighbors[x][y] in rules.birth:
            next_grid[x][y] = LIVE_CELL
            born += 1
        elif cell == LIVE_CELL:
            if neighbors[x][y] in rules.survival:
                next_grid[x][y] = LIVE_CELL
                survived += 1
            else:
                died += 1

    return Generation(grid=next_grid, born=born, died=died, survived=survived,
                      time=time.time()-start_time)


def _parse_rulestring(rulestring):
    match = re.match(r'b(\d*)\/s(\d*)', rulestring, re.IGNORECASE)
    if match:
        birth = tuple(int(x) for x in match[1])
        survival = tuple(int(x) for x in match[2])
    else:
        birth = tuple()
        survival = tuple()

    return Rules(birth=birth, survival=survival)
