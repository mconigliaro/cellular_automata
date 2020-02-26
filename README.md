# cellular_automata

Simple 2D [cellular automata](https://www.conwaylife.com/wiki/Cellular_automaton) implementation with fun visualizations for your terminal.

The default automaton is [Conway's Game of Life](https://www.conwaylife.com/wiki/Conway%27s_Game_of_Life), but [many other automata](https://www.conwaylife.com/wiki/List_of_Life-like_cellular_automata) with different [rules](https://www.conwaylife.com/wiki/Rulestring) and [neighborhoods](https://www.conwaylife.com/wiki/Neighbourhood) are supported.

By default, the grid will be set to the dimensions of the terminal window. When the grid is bigger than the terminal window, the arrow/WASD keys can be used to adjust the viewport.

![](screenshots/1.png)

## Getting Started

    pip install pipenv
    pipenv install --dev
    pipenv shell
    ...

## Run Tests

    pytest

## Run Simulation

Use `--help` to see available options:

    ca
