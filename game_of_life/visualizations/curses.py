from curses import curs_set, wrapper
from game_of_life import grid, generations
from time import sleep


def main(stdscr, height, width, delay):
    max_height, max_width = stdscr.getmaxyx()
    if not height:
        height = max_height - 1
    if not width:
        width = max_width - 1

    for i, g in enumerate(generations(grid(height, width))):
        population = 0
        for x in range(height):
            for y in range(width):
                if g[x][y] == 1:
                    population += 1
                stdscr.addch(x, y, str(g[x][y]))

        stdscr.addstr(max_height - 1, 0,
                      f'Generation: {i}  Population: {population}')
        curs_set(0)
        stdscr.refresh()
        sleep(delay)


def run(height=None, width=None, delay=0):
    wrapper(main, height=height, width=width, delay=delay)
