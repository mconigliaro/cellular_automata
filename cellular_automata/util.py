import cellular_automata.exceptions as exc
import os
import pathlib as pl
import pkgutil as pu
import re
import typing as ty


class Rules(ty.NamedTuple):
    birth: tuple = ()
    survival: tuple = ()


def list_visualizations():
    path = os.path.join(pl.Path(__file__).parent, "visualizations")
    return [m.name for m in pu.iter_modules([path])]


def parse_rulestring(rulestring):
    bs_match = re.match(r'b(\d*)\/s(\d*)', rulestring, re.IGNORECASE)
    if bs_match:
        return Rules(birth=tuple(int(x) for x in bs_match[1]),
                     survival=tuple(int(x) for x in bs_match[2]))

    sb_match = re.match(r'(\d*)\/(\d*)', rulestring, re.IGNORECASE)
    if sb_match:
        return Rules(survival=tuple(int(x) for x in sb_match[1]),
                     birth=tuple(int(x) for x in sb_match[2]))

    raise exc.RulestringParseError(f"Unable to parse rulestring: {rulestring}")
