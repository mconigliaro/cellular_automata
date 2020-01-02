import cellular_automata as ca


def run(height, width, population, rulestring):
    height = height or 24
    width = width or 79
    cells = height * width
    print(f'Ctrl+C to quit')
    print(f'Rulestring: {rulestring}')

    gens = ca.generations(height, width, population, rulestring)
    for i, g in enumerate(gens):
        gen_per_sec = f'{1 / g.time :.1f}'
        pop_pct = f'{g.population / cells * 100 :.1f}'
        if i % 1000 == 0:  # FIXME
            status = f'Generation: {i} ({gen_per_sec}/s) | '
            status += f'Population: {g.population}/{cells} ({pop_pct}%)'
            print(status)
