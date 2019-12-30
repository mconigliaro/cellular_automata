from collections import namedtuple
from itertools import product
from random import sample
import re


DEAD_CELL = 0
LIVE_CELL = 1

Generation = namedtuple('Generation', ['grid', 'born', 'died', 'survived'],
                        defaults=[0, 0, 0])

Rules = namedtuple('Rules', ['birth', 'survival'])


def generations(height, width, population, rulestring):
    gen = _first_generation(height, width, population)
    rules = _parse_rulestring(rulestring)
    while True:
        yield gen
        gen = _next_generation(gen, rules)


def _first_generation(height, width, population):
    grid = [[DEAD_CELL for x in range(width)] for y in range(height)]
    born = int(height * width * (population / 100))
    for x, y in sample(tuple(product(range(height), range(width))), born):
        grid[x][y] = LIVE_CELL
    return Generation(grid=grid, born=born)


def _neighbors(grid, x, y):
    x_range = range(max(0, x - 1), min(len(grid), x + 2))
    y_range = range(max(0, y - 1), min(len(grid[0]), y + 2))
    return sum(grid[i][j] for i, j in product(x_range, y_range)
               if (i, j) != (x, y))


def _next_generation(gen1, rules):
    gen2 = []
    born = 0
    died = 0
    survived = 0
    for x in range(len(gen1.grid)):
        gen2.insert(x, [])
        for y in range(len(gen1.grid[0])):
            n = _neighbors(gen1.grid, x, y)
            cell = gen1.grid[x][y]
            if cell == DEAD_CELL:
                if n in rules.birth:
                    gen2[x].append(LIVE_CELL)
                    born += 1
                else:
                    gen2[x].append(DEAD_CELL)
            elif cell == LIVE_CELL:
                if n in rules.survival:
                    gen2[x].append(LIVE_CELL)
                    survived += 1
                else:
                    gen2[x].append(DEAD_CELL)
                    died += 1

    return Generation(
        grid=gen2,
        born=born,
        died=died,
        survived=survived
    )


def _parse_rulestring(rulestring):
    match = re.match(r'b(\d*)\/s(\d*)', rulestring, re.IGNORECASE)
    if match is None:
        birth = tuple()
        survival = tuple()
    else:
        birth = tuple(int(x) for x in match[1])
        survival = tuple(int(x) for x in match[2])
    return Rules(birth=birth, survival=survival)
