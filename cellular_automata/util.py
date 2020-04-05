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
    match = re.match(r'b(\d*)\/s(\d*)', rulestring, re.IGNORECASE)
    if match:
        birth = tuple(int(x) for x in match[1])
        survival = tuple(int(x) for x in match[2])
    else:
        birth = tuple()
        survival = tuple()
    return Rules(birth=birth, survival=survival)
