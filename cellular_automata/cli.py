import argparse
import importlib
import shutil
import os
import pathlib
import pkgutil

import cellular_automata
import cellular_automata.visualizations.curses


def list_visualizations() -> list:
    path = os.path.join(pathlib.Path(__file__).parent, "visualizations")
    return [m.name for m in pkgutil.iter_modules([path])]


def parse(args=None) -> argparse.Namespace:
    columns, lines = shutil.get_terminal_size(fallback=(256, 256))

    parser = argparse.ArgumentParser(
        description="Simple 2D cellular automata implementation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-s", "--seed", help="Random seed")
    parser.add_argument(
        "-x", "--height", type=int, default=lines - 1, help="Universe height"
    )
    parser.add_argument(
        "-y", "--width", type=int, default=columns - 1, help="Universe width"
    )
    parser.add_argument(
        "-p",
        "--population",
        type=float,
        default=33.3,
        help="Initial population as a percentage of the universe",
    )
    parser.add_argument(
        "-t",
        "--topology",
        choices=("closed", "wrapped"),
        default="wrapped",
        help="Universe topology",
    )
    parser.add_argument(
        "-r", "--rulestring", default="b3/s23", help="Rulestring in B/S or S/B notation"
    )
    parser.add_argument(
        "-v",
        "--visualization",
        choices=list_visualizations(),
        default="curses",
        help="Visualization type",
    )
    parser.add_argument(
        "--theme",
        choices=cellular_automata.visualizations.curses.THEMES.keys(),
        default="default",
        help="Curses theme",
    )
    parser.add_argument(
        "-d", "--delay", type=float, default=0, help="Refresh delay in seconds"
    )

    return parser.parse_args(args)


def main() -> None:
    opts = parse()

    gens = cellular_automata.generations(
        opts.height,
        opts.width,
        opts.population,
        opts.topology,
        opts.rulestring,
        opts.seed,
    )

    module_base = "cellular_automata.visualizations"
    vis = importlib.import_module(f"{module_base}.{opts.visualization}")
    try:
        vis.run(gens, opts)
    except KeyboardInterrupt:
        pass
