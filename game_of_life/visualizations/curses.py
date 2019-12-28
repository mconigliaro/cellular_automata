import curses
from game_of_life import generations
from time import sleep


def run(height=None, width=None, delay=0):
    curses.wrapper(main, height=height, width=width, delay=delay)


def main(stdscr, height, width, delay):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    if not height:
        height = curses.LINES - 2
    if not width:
        width = curses.COLS - 1
    cells = height * width

    for i, gen in enumerate(generations(height, width)):
        for x in range(height):
            for y in range(width):
                if gen.grid[x][y] == 1:
                    stdscr.addch(x, y, '█')
                else:
                    stdscr.addch(x, y, ' ')

        status_bar = f'Ctrl+C to quit | '
        status_bar += f'Generation: {i} | '
        population = gen.born + gen.survived
        pop_pct = f'{population / cells * 100 :.1f}'
        status_bar += f'Population: {population}/{cells} ({pop_pct}%) | '
        status_bar += f'Delay: {delay}s'
        status_bar = status_bar.ljust(width, ' ')[:width]
        stdscr.addstr(height + 1, 0, status_bar, curses.color_pair(1))

        stdscr.refresh()
        sleep(delay)
