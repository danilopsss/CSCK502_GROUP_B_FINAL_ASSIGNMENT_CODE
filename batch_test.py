from ga import run_ga
from tabulate import tabulate
from utils import choose_letters
from tqdm import tqdm, trange
import itertools

TRIALS = 1000

POP_GRID = [20, 40, 60, 80, 120]
MUT_GRID = [0.05, 0.08, 0.10, 0.15]

results = []
# letters = ["W", "O", "R", "D"]
# letters = ["R", "I", "S", "K"]
letters = choose_letters()

# Get all combinations so can track progress
param_combinations = list(itertools.product(POP_GRID, MUT_GRID))
# for pop, mut in itertools.product(POP_GRID, MUT_GRID):
for pop, mut in tqdm(param_combinations, desc="Grid Configs", position=0):
    succ = gens_sum = time_sum = 0
    # for t in trange(TRIALS, desc="Trials", leave=False):
    for t in trange(
        TRIALS, desc=f"Trials (Pop={pop}, Mut={mut:.2f})", position=1, leave=False
    ):
        ok, gens, secs = run_ga(
            pop_size=pop,
            mut_rate=mut,
            max_gens=500,
            fixed_clues=2,
            use_edge_word=True,
            letters=letters,
            seed=t,
        )
        time_sum += secs
        if ok:
            succ += 1
            gens_sum += gens
    rate = succ / TRIALS
    avg_gens = gens_sum / succ if succ else None
    avg_secs = time_sum / TRIALS
    results.append((pop, mut, rate, avg_gens, avg_secs))

# sort: highest success → lowest avg gens
results.sort(key=lambda x: (-x[2], x[3] or 1e9))

table = [
    {
        "population": pop,
        "mutation rate": mut,
        "success": f"{rate:6.2%}",
        "average generation": f"{avg_gens:.1f}" if avg_gens else "-",
        "average seconds": f"{avg_secs:.2f}",
    }
    for pop, mut, rate, avg_gens, avg_secs in results
]
print(tabulate(table, headers="keys", tablefmt="github"))
