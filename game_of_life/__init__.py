from collections import namedtuple
from random import randint


Generation = namedtuple('Generation', ['grid', 'born', 'died_under',
                        'died_over', 'survived'], defaults=[0, 0, 0, 0])


def generations(height, width):
    gen = Generation(
        grid=tuple(tuple(randint(0, 1) for x in range(width))
                   for y in range(height))
    )
    while True:
        yield gen
        gen = next_generation(gen)


def neighbors(grid, x, y):
    s = 0
    for i in range(max(0, x - 1), min(len(grid), x + 2)):
        for j in range(max(0, y - 1), min(len(grid[0]), y + 2)):
            if (i, j) != (x, y):
                s += grid[i][j]
    return s


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
            if gen1.grid[x][y] == 0 and n == 3:
                gen2[x].append(1)
                born += 1
            elif gen1.grid[x][y] == 1 and n < 2:
                gen2[x].append(0)
                died_under += 1
            elif gen1.grid[x][y] == 1 and n > 3:
                gen2[x].append(0)
                died_over += 1
            else:
                gen2[x].append(gen1.grid[x][y])
                survived += gen1.grid[x][y]

    return Generation(
        grid=gen2,
        born=born,
        died_under=died_under,
        died_over=died_over,
        survived=survived
    )
