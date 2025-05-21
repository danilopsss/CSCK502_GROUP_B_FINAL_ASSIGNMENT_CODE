"""
4×4 Genetic-Algorithm 'Sudoku' Solver
"""

import random
from wordfreq import top_n_list
from typing import List


def choose_letters() -> List[str]:
    """
    Return a list of four distinct uppercase letters.
    """
    # Pull 50 000 common English words, filter for len==4 & distinct letters
    candidates = [
        w.upper() for w in top_n_list("en", 50_000) if len(w) == 4 and len(set(w)) == 4
    ]
    if not candidates:
        raise ValueError("No 4-letter candidate words found.")
    return list(random.choice(candidates))


# Config
LETTERS = choose_letters()
POPULATION_SIZE = 40
MAX_GENERATIONS = 500
TOURNAMENT_K = 3
MUTATION_RATE = 0.15

# Main code
print("Using letters:", LETTERS)
