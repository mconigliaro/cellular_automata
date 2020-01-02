import collections.abc as abc
import curses as cs
import itertools as it
import random as rand
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


def run(generations, args):
    while True:
        try:
            cs.wrapper(_main, generations, args)
        except cs.error as e:
            if e != 'add_wch() returned ERR':
                continue


def _main(stdscr, generations, args):
    rulestring = args.rulestring
    theme = args.theme
    delay = args.delay

    cs.curs_set(0)
    stdscr.timeout(0)

    stdscr.clear()

    cs.start_color()
    cs.init_pair(1, THEMES[theme]['fg_color'], THEMES[theme]['bg_color'])
    cs.init_pair(2, cs.COLOR_BLACK, cs.COLOR_WHITE)
    cell_chars = (THEMES[theme]['dead_cell'], THEMES[theme]['live_cell'])

    x_pos = 0
    y_pos = 0
    for i, gen in enumerate(generations):
        height, width = gen.grid.shape
        win_height = cs.LINES - 1
        win_width = cs.COLS - 1
        visible_x = min(height, win_height)
        visible_y = min(width, win_width)

        ch = stdscr.getch()
        if ch == cs.KEY_RESIZE:
            cs.resizeterm(*stdscr.getmaxyx())
            stdscr.clear()
        elif ch in (cs.KEY_DOWN, 115):
            if x_pos + visible_x < height:
                x_pos += 1
        elif ch in (cs.KEY_UP, 119):
            if x_pos > 0:
                x_pos -= 1
        elif ch in (cs.KEY_LEFT, 97):
            if y_pos > 0:
                y_pos -= 1
        elif ch in (cs.KEY_RIGHT, 100):
            if y_pos + visible_y < width:
                y_pos += 1
        elif ch == cs.KEY_HOME:
            x_pos = 0
            y_pos = 0

        for x, y in it.product(range(visible_x), range(visible_y)):
            cell = gen.grid[x + x_pos, y + y_pos]
            char = cell_chars[cell]
            if isinstance(char, abc.Iterable):
                char = rand.choice(char)
            stdscr.addch(x, y, char, cs.color_pair(1))

        pop_pct = f'{gen.population / gen.grid.size * 100 :.1f}'

        status_bar = f'Grid: {height}x{width} ({gen.grid.size}) | '
        status_bar += f'Rules: {rulestring} | '
        status_bar += f'Gen: {i} ({1 / gen.time :.1f}/s) | '
        status_bar += f'Pop: {gen.population} ({pop_pct}%)'
        status_bar = status_bar.ljust(win_width, ' ')[:win_width]
        stdscr.addstr(win_height, 0, status_bar, cs.color_pair(2))

        stdscr.refresh()
        t.sleep(delay)
