from collections.abc import Iterable
import curses
from game_of_life import generations
from itertools import product
from random import choice
from signal import signal, SIGWINCH
from time import sleep


THEMES = {
    'atari': {
        'fg_color': curses.COLOR_WHITE,
        'bg_color': curses.COLOR_BLACK,
        'live_cell': '█',
        'dead_cell': ' '
    },
    'binary': {
        'fg_color': curses.COLOR_WHITE,
        'bg_color': curses.COLOR_BLACK,
        'live_cell': '1',
        'dead_cell': '0'
    },
    'default': {
        'fg_color': curses.COLOR_GREEN,
        'bg_color': curses.COLOR_BLACK,
        'live_cell': '❚',
        'dead_cell': ' '
    },
    'msdos': {
        'fg_color': curses.COLOR_WHITE,
        'bg_color': curses.COLOR_BLUE,
        'live_cell': '❚',
        'dead_cell': ' '
    },
    'matrix': {
        'fg_color': curses.COLOR_GREEN,
        'bg_color': curses.COLOR_BLACK,
        'live_cell': tuple(chr(x) for x in range(33, 127)),
        'dead_cell': ' '
    }
}


def run(population, rulestring, delay, theme):
    signal(SIGWINCH, _resize_handler)
    while True:
        try:
            curses.wrapper(_main,
                           population=population,
                           rulestring=rulestring,
                           delay=delay,
                           theme=theme)
        except WindowResizeException:
            continue
        except KeyboardInterrupt:
            break


def _main(stdscr, population, rulestring, delay, theme):
    stdscr.clear()

    curses.start_color()
    curses.init_pair(1, THEMES[theme]['fg_color'], THEMES[theme]['bg_color'])
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    max_height, max_width = stdscr.getmaxyx()
    height = max_height - 1
    width = max_width - 1
    cells = height * width
    cell_chars = (THEMES[theme]['dead_cell'], THEMES[theme]['live_cell'])

    gs = generations(height, width, population, rulestring)
    for i, gen in enumerate(gs):
        for x, y in product(range(height), range(width)):
            char = cell_chars[gen.grid[x][y]]
            if isinstance(char, Iterable):
                char = choice(char)
            stdscr.addch(x, y, char, curses.color_pair(1))

        population = gen.born + gen.survived
        pop_pct = f'{population / cells * 100 :.1f}'

        status_bar = f'Ctrl+C to quit | '
        status_bar += f'Rulestring: {rulestring} | '
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
