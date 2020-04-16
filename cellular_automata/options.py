import argparse as ap
import cellular_automata.util as util
import cellular_automata.visualizations.curses as cur
import shutil as sh


def parse(args=None):
    columns, lines = sh.get_terminal_size(fallback=(256, 256))

    parser = ap.ArgumentParser(
        description="Simple 2D cellular automata implementation",
        formatter_class=ap.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-s',
        '--seed',
        help='Random seed'
    )
    parser.add_argument(
        '-x',
        '--height',
        type=int,
        default=lines-1,
        help='Universe height'
    )
    parser.add_argument(
        '-y',
        '--width',
        type=int,
        default=columns-1,
        help='Universe width'
    )
    parser.add_argument(
        '-p',
        '--population',
        type=float,
        default=33.3,
        help='Initial population as a percentage of the universe'
    )
    parser.add_argument(
        '-t',
        '--topology',
        choices=('closed', 'wrapped'),
        default='wrapped',
        help='Universe topology'
    )
    parser.add_argument(
        '-r',
        '--rulestring',
        default='b3/s23',
        help='Rulestring in B/S or S/B notation'
    )
    parser.add_argument(
        '-v',
        '--visualization',
        choices=util.list_visualizations(),
        default='curses',
        help='Visualization type'
    )
    parser.add_argument(
        '--theme',
        choices=cur.THEMES.keys(),
        default='default',
        help='Curses theme'
    )
    parser.add_argument(
        '-d',
        '--delay',
        type=float,
        default=0,
        help='Refresh delay in seconds'
    )

    return parser.parse_args(args)
