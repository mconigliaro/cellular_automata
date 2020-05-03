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

KEYS_DOWN = (cs.KEY_DOWN, ord('s'))
KEYS_SDOWN = (336, ord('S'))
KEYS_UP = (cs.KEY_UP, ord('w'))
KEYS_SUP = (337, ord('W'))
KEYS_LEFT = (cs.KEY_LEFT, ord('a'))
KEYS_SLEFT = (cs.KEY_SLEFT, ord('A'))
KEYS_RIGHT = (cs.KEY_RIGHT, ord('d'))
KEYS_SRIGHT = (cs.KEY_SRIGHT, ord('D'))


def run(generations, args):
    while True:
        try:
            cs.wrapper(_main, generations, args)
        except cs.error as e:
            if e != 'add_wch() returned ERR':
                continue


def _main(stdscr, generations, args):
    cs.curs_set(0)
    stdscr.timeout(0)

    stdscr.clear()

    theme = args.theme
    cs.start_color()
    cs.init_pair(1, THEMES[theme]['fg_color'], THEMES[theme]['bg_color'])
    cs.init_pair(2, cs.COLOR_BLACK, cs.COLOR_WHITE)
    cell_chars = (THEMES[theme]['dead_cell'], THEMES[theme]['live_cell'])

    x_pos = 0
    y_pos = 0
    for i, gen in enumerate(generations):
        height, width = gen.universe.shape
        win_height = cs.LINES - 1
        win_width = cs.COLS - 1
        visible_x = min(height, win_height)
        visible_y = min(width, win_width)

        ch = stdscr.getch()
        if ch == cs.KEY_RESIZE:
            x_pos = 0
            y_pos = 0
            cs.resizeterm(*stdscr.getmaxyx())
            stdscr.clear()
            stdscr.refresh()
        elif ch in KEYS_DOWN:
            if x_pos + visible_x < height:
                x_pos += 1
        elif ch in KEYS_SDOWN:
            if x_pos + visible_x * 2 < height:
                x_pos += visible_x
            else:
                x_pos = height - visible_x
        elif ch in KEYS_UP:
            if x_pos > 0:
                x_pos -= 1
        elif ch in KEYS_SUP:
            if x_pos - visible_x > 0:
                x_pos -= visible_x
            else:
                x_pos = 0
        elif ch in KEYS_LEFT:
            if y_pos > 0:
                y_pos -= 1
        elif ch in KEYS_SLEFT:
            if y_pos - visible_y > 0:
                y_pos -= visible_y
            else:
                y_pos = 0
        elif ch in KEYS_RIGHT:
            if y_pos + visible_y < width:
                y_pos += 1
        elif ch in KEYS_SRIGHT:
            if y_pos + visible_y * 2 < width:
                y_pos += visible_y
            else:
                y_pos = width - visible_y
        elif ch == cs.KEY_HOME:
            x_pos = 0
            y_pos = 0

        for x, y in it.product(range(visible_x), range(visible_y)):
            cell = gen.universe[x + x_pos, y + y_pos]
            char = cell_chars[cell]
            if isinstance(char, abc.Iterable):
                char = rand.choice(char)
            stdscr.addch(x, y, char, cs.color_pair(1))

        pop_pct = f'{gen.population / gen.universe.size * 100 :.1f}'

        status_bar = f'Ctrl+C to quit | '
        status_bar += f'Size: {height}x{width} | '
        status_bar += f'Position: {x_pos},{y_pos} | '
        status_bar += f'Topology: {args.topology.capitalize()} | '
        status_bar += f'Rules: {args.rulestring} | '
        status_bar += f'Generation: {i} ({1 / gen.time :.1f}/s) | '
        status_bar += f'Population: {gen.population} ({pop_pct}%)'
        status_bar = status_bar.ljust(win_width, ' ')[:win_width]
        stdscr.addstr(win_height, 0, status_bar, cs.color_pair(2))

        stdscr.refresh()
        t.sleep(args.delay)
