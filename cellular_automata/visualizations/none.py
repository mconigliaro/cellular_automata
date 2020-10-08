import time


def run(generations, args):
    last_status = 0
    for i, gen in enumerate(generations):
        if time.time() - last_status > 1:
            g = f'{i} ({1 / gen.time :.1f}/s)'
            p_pct = f'{gen.population / gen.universe.size * 100 :.1f}'
            p = f'{gen.population} ({p_pct}%)'
            print(f'Generation: {g} | Population: {p}')
            last_status = time.time()
