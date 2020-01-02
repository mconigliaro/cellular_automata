import cellular_automata as ca
import collections.abc as abc
import curses as cs
import itertools as it
import random as rn
import signal as sig
import time as t


THEMES = {
    'atari': {
        'fg_color': cs.COLOR_WHITE,
        'bg_color': cs.COLOR_BLACK,
        'live_cell': '█',
        'dead_cell': ' '
    },
    'binary': {
        'fg_color': cs.COLOR_WHITE,
        'bg_color': cs.COLOR_BLACK,
        'live_cell': '1',
        'dead_cell': '0'
    },
    'default': {
        'fg_color': cs.COLOR_GREEN,
        'bg_color': cs.COLOR_BLACK,
        'live_cell': '❚',
        'dead_cell': ' '
    },
    'msdos': {
        'fg_color': cs.COLOR_WHITE,
        'bg_color': cs.COLOR_BLUE,
        'live_cell': '❚',
        'dead_cell': ' '
    },
    'matrix': {
        'fg_color': cs.COLOR_GREEN,
        'bg_color': cs.COLOR_BLACK,
        'live_cell': tuple(chr(x) for x in range(33, 127)),
        'dead_cell': ' '
    }
}


def run(height, width, population, rulestring, delay, theme):
    sig.signal(sig.SIGWINCH, _resize_handler)
    while True:
        try:
            cs.wrapper(_main,
                       height=height,
                       width=width,
                       population=population,
                       rulestring=rulestring,
                       delay=delay,
                       theme=theme)
        except WindowResizeException:
            continue


def _main(stdscr, height, width, population, rulestring, delay, theme):
    max_height, max_width = stdscr.getmaxyx()
    win_height = max_height - 1
    win_width = max_width - 1
    height = height or win_height
    width = width or win_width
    visible_x = min(height, win_height)
    visible_y = min(width, win_width)
    cells = height * width
    cell_chars = (THEMES[theme]['dead_cell'], THEMES[theme]['live_cell'])
    gens = ca.generations(height, width, population, rulestring)

    stdscr.clear()

    cs.start_color()
    cs.init_pair(1, THEMES[theme]['fg_color'], THEMES[theme]['bg_color'])
    cs.init_pair(2, cs.COLOR_BLACK, cs.COLOR_WHITE)
    cs.curs_set(0)

    for i, gen in enumerate(gens):
        for x, y in it.product(range(visible_x), range(visible_y)):
            cell = gen.grid[x, y]
            char = cell_chars[cell]
            if isinstance(char, abc.Iterable):
                char = rn.choice(char)
            stdscr.addch(x, y, char, cs.color_pair(1))

        gen_per_sec = f'{1 / gen.time :.1f}'
        pop_pct = f'{gen.population / cells * 100 :.1f}'

        status_bar = f'Ctrl+C to quit | '
        status_bar += f'RS: {rulestring} | '
        status_bar += f'Gen: {i} ({gen_per_sec}/s) | '
        status_bar += f'Pop: {gen.population}/{cells} ({pop_pct}%) | '
        status_bar += f'Delay: {delay}s'
        status_bar = status_bar.ljust(win_width, ' ')[:win_width]
        stdscr.addstr(win_height, 0, status_bar, cs.color_pair(2))

        stdscr.refresh()
        t.sleep(delay)


class WindowResizeException(Exception):
    pass


def _resize_handler(signum, frame):
    raise WindowResizeException()
