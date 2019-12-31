from collections import namedtuple
from itertools import product
from random import sample
import re
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
        gen = _next_generation(gen, rules)


def _first_generation(height, width, population):
    start_time = time.time()
    grid = [[DEAD_CELL for x in range(width)] for y in range(height)]
    born = int(height * width * (population / 100))
    for x, y in sample(tuple(product(range(height), range(width))), born):
        grid[x][y] = LIVE_CELL
    return Generation(grid=grid, born=born, time=time.time()-start_time)


def _neighbors(grid, x, y):
    x_range = range(max(0, x - 1), min(len(grid), x + 2))
    y_range = range(max(0, y - 1), min(len(grid[0]), y + 2))
    return sum(grid[i][j] for i, j in product(x_range, y_range)
               if (i, j) != (x, y))


def _next_generation(curr_gen, rules):
    start_time = time.time()
    next_gen = []
    born = 0
    died = 0
    survived = 0
    for x in range(len(curr_gen.grid)):
        next_gen.insert(x, [])
        for y in range(len(curr_gen.grid[x])):
            cell = curr_gen.grid[x][y]
            n = _neighbors(curr_gen.grid, x, y)
            if cell == DEAD_CELL:
                if n in rules.birth:
                    next_gen[x].append(LIVE_CELL)
                    born += 1
                else:
                    next_gen[x].append(DEAD_CELL)
            elif cell == LIVE_CELL:
                if n in rules.survival:
                    next_gen[x].append(LIVE_CELL)
                    survived += 1
                else:
                    next_gen[x].append(DEAD_CELL)
                    died += 1

    return Generation(grid=next_gen, born=born, died=died, survived=survived,
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
