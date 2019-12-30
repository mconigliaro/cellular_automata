from collections import namedtuple
from itertools import product
from random import sample


Generation = namedtuple('Generation', ['grid', 'born', 'died_under',
                        'died_over', 'survived'], defaults=[0, 0, 0, 0])


def first_generation(height, width, population):
    grid = [[0 for x in range(width)] for y in range(height)]
    born = int(height * width * (population / 100))
    for x, y in sample(tuple(product(range(height), range(width))), born):
        grid[x][y] = 1
    return Generation(grid=grid, born=born)


def generations(height, width, population):
    gen = first_generation(height, width, population)
    while True:
        yield gen
        gen = next_generation(gen)


def neighbors(grid, x, y):
    n = 0
    x_range = range(max(0, x - 1), min(len(grid), x + 2))
    y_range = range(max(0, y - 1), min(len(grid[0]), y + 2))
    for i, j in product(x_range, y_range):
        if (i, j) != (x, y):
            n += grid[i][j]
    return n


def next_generation(gen1):
    gen2 = []
    born = 0
    died_under = 0
    died_over = 0
    survived = 0
    for x in range(len(gen1.grid)):
        gen2.insert(x, [])
        for y in range(len(gen1.grid[0])):
            n = neighbors(gen1.grid, x, y)
            cell = gen1.grid[x][y]
            if cell == 0 and n == 3:
                gen2[x].append(1)
                born += 1
            elif cell == 1 and n < 2:
                gen2[x].append(0)
                died_under += 1
            elif cell == 1 and n > 3:
                gen2[x].append(0)
                died_over += 1
            else:
                gen2[x].append(cell)
                survived += cell

    return Generation(
        grid=gen2,
        born=born,
        died_under=died_under,
        died_over=died_over,
        survived=survived
    )
