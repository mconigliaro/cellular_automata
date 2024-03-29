from argparse import Namespace
from typing import Iterable
import curses
import itertools
import random
import time

from numpy import ndarray


THEMES = {
    "atari": {
        "fg_color": curses.COLOR_WHITE,
        "bg_color": curses.COLOR_BLACK,
        "live_cell": "█",
        "dead_cell": " ",
    },
    "binary": {
        "fg_color": curses.COLOR_WHITE,
        "bg_color": curses.COLOR_BLACK,
        "live_cell": "1",
        "dead_cell": "0",
    },
    "default": {
        "fg_color": curses.COLOR_GREEN,
        "bg_color": curses.COLOR_BLACK,
        "live_cell": "❚",
        "dead_cell": " ",
    },
    "msdos": {
        "fg_color": curses.COLOR_WHITE,
        "bg_color": curses.COLOR_BLUE,
        "live_cell": "❚",
        "dead_cell": " ",
    },
    "matrix": {
        "fg_color": curses.COLOR_GREEN,
        "bg_color": curses.COLOR_BLACK,
        "live_cell": tuple(chr(x) for x in range(33, 127)),
        "dead_cell": " ",
    },
}

KEYS_DOWN = (curses.KEY_DOWN, ord("s"))
KEYS_UP = (curses.KEY_UP, ord("w"))
KEYS_LEFT = (curses.KEY_LEFT, ord("a"))
KEYS_RIGHT = (curses.KEY_RIGHT, ord("d"))
KEYS_PAGE_DOWN = (336, ord("S"))
KEYS_PAGE_UP = (337, ord("W"))
KEYS_PAGE_LEFT = (curses.KEY_SLEFT, ord("A"))
KEYS_PAGE_RIGHT = (curses.KEY_SRIGHT, ord("D"))
KEYS_SPEED_DOWN = ord("-")
KEYS_SPEED_UP = ord("+")

SPEED_INCREMENT = 0.01


def run(generations: ndarray, args: Namespace) -> None:
    while True:
        try:
            curses.wrapper(_main, generations, args)
        except curses.error as e:
            if e != "add_wch() returned ERR":
                continue


def _main(stdscr, generations: ndarray, args: Namespace):
    curses.curs_set(0)
    stdscr.timeout(0)

    stdscr.clear()

    theme = args.theme
    curses.start_color()
    curses.init_pair(1, THEMES[theme]["fg_color"], THEMES[theme]["bg_color"])
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    cell_chars = (THEMES[theme]["dead_cell"], THEMES[theme]["live_cell"])
    delay = args.delay

    x_pos = 0
    y_pos = 0
    for i, gen in enumerate(generations):
        height, width = gen.universe.shape
        win_height = curses.LINES - 1
        win_width = curses.COLS - 1
        visible_x = min(height, win_height)
        visible_y = min(width, win_width)

        ch = stdscr.getch()
        if ch == curses.KEY_RESIZE:
            x_pos = 0
            y_pos = 0
            curses.resizeterm(*stdscr.getmaxyx())
            stdscr.clear()
            stdscr.refresh()
        elif ch in KEYS_DOWN:
            if x_pos + visible_x < height:
                x_pos += 1
        elif ch in KEYS_PAGE_DOWN:
            if x_pos + visible_x * 2 < height:
                x_pos += visible_x
            else:
                x_pos = height - visible_x
        elif ch in KEYS_UP:
            if x_pos > 0:
                x_pos -= 1
        elif ch in KEYS_PAGE_UP:
            if x_pos - visible_x > 0:
                x_pos -= visible_x
            else:
                x_pos = 0
        elif ch in KEYS_LEFT:
            if y_pos > 0:
                y_pos -= 1
        elif ch in KEYS_PAGE_LEFT:
            if y_pos - visible_y > 0:
                y_pos -= visible_y
            else:
                y_pos = 0
        elif ch in KEYS_RIGHT:
            if y_pos + visible_y < width:
                y_pos += 1
        elif ch in KEYS_PAGE_RIGHT:
            if y_pos + visible_y * 2 < width:
                y_pos += visible_y
            else:
                y_pos = width - visible_y
        elif ch == curses.KEY_HOME:
            x_pos = 0
            y_pos = 0
        elif ch == KEYS_SPEED_DOWN:
            delay = delay + SPEED_INCREMENT if delay == 0 else delay * 2
        elif ch == KEYS_SPEED_UP:
            tmp_delay = delay / 2
            delay = tmp_delay if tmp_delay > SPEED_INCREMENT else 0

        for x, y in itertools.product(range(visible_x), range(visible_y)):
            cell = gen.universe[x + x_pos, y + y_pos]
            char = cell_chars[cell]
            if isinstance(char, Iterable):
                char = random.choice(char)
            stdscr.addch(x, y, char, curses.color_pair(1))

        pop_pct = f"{gen.population / gen.universe.size * 100 :.1f}"

        status_bar = "Ctrl+C to quit | "
        status_bar += f"Size: {height}x{width} | "
        status_bar += f"Pos: {x_pos},{y_pos} | "
        status_bar += f"Top: {args.topology.capitalize()} | "
        status_bar += f"Rules: {args.rulestring} | "
        status_bar += f"Gen: {i} ({1 / gen.time :.1f}/s) | "
        status_bar += f"Pop: {gen.population} ({pop_pct}%) | "
        status_bar += f"Delay: {delay :.2f}s"
        status_bar = status_bar.ljust(win_width, " ")[:win_width]
        stdscr.addstr(win_height, 0, status_bar, curses.color_pair(2))

        stdscr.refresh()
        time.sleep(delay)
