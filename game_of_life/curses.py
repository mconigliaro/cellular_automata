import curses
from game_of_life import generations
from signal import signal, SIGWINCH
from time import sleep


def run(population, delay):
    signal(SIGWINCH, _resize_handler)
    while True:
        try:
            curses.wrapper(_main, population=population, delay=delay)
        except WindowResizeException:
            continue
        except KeyboardInterrupt:
            break


def _main(stdscr, population, delay):
    stdscr.clear()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    max_height, max_width = stdscr.getmaxyx()
    height = max_height - 1
    width = max_width - 1
    cells = height * width

    for i, gen in enumerate(generations(height, width, population)):
        for x in range(height):
            for y in range(width):
                char = '❚' if gen.grid[x][y] == 1 else ' '
                stdscr.addch(x, y, char, curses.color_pair(1))

        population = gen.born + gen.survived
        pop_pct = f'{population / cells * 100 :.1f}'

        status_bar = f'Ctrl+C to quit | '
        status_bar += f'Generation: {i} | '
        status_bar += f'Population: {population}/{cells} ({pop_pct}%) | '
        status_bar += f'Delay: {delay}s'
        status_bar = status_bar.ljust(width, ' ')[:width]
        stdscr.addstr(height, 0, status_bar, curses.color_pair(2))

        stdscr.refresh()
        sleep(delay)


class WindowResizeException(Exception):
    pass


def _resize_handler(signum, frame):
    raise WindowResizeException()