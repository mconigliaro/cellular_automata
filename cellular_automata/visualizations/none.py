import time as t


def run(generations, args):
    last_status = 0
    for i, gen in enumerate(generations):
        if t.time() - last_status > 1:
            g = f'{i} ({1 / gen.time :.1f}/s)'
            p_pct = f'{gen.population / gen.grid.size * 100 :.1f}'
            p = f'{gen.population} ({p_pct}%)'
            print(f'Generation: {g} | Population: {p}')
            last_status = t.time()
