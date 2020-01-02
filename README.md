# cellular_automata

Simple [cellular automata](https://www.conwaylife.com/wiki/Cellular_automaton)
implementation with fun visualizations for your terminal

![](https://gitlab.com/mconigliaro/cellular_automata/raw/master/screenshots/1.png)

## Getting Started

    pip install pipenv
    pipenv install --dev
    pipenv shell
    ...

## Run Tests

    pytest

## Run Simulation

By default, the game grid will be set to the dimensions of the terminal window.
When the game grid is bigger than the terminal window, the arrow/WASD keys can
be used to adjust the viewport.

    ca [--help]
