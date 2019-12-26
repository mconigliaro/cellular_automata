from random import randint


def grid(height, width):
    return [[randint(0, 1) for x in range(width)] for y in range(height)]


def neighbors(g, x, y):
    s = 0
    for i in range(max(0, x - 1), min(len(g), x + 2)):
        for j in range(max(0, y - 1), min(len(g[0]), y + 2)):
            if (i, j) != (x, y):
                s += g[i][j]
    return s


def next_gen(g1):
    g2 = []
    for x in range(len(g1)):
        g2.insert(x, [])
        for y in range(len(g1[0])):
            n = neighbors(g1, x, y)
            if g1[x][y] == 1 and (n < 2 or n > 3):
                g2[x].append(0)
            elif g1[x][y] == 0 and n == 3:
                g2[x].append(1)
            else:
                g2[x].append(g1[x][y])
    return g2
