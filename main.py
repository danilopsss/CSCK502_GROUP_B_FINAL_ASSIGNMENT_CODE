"""
4×4 Genetic-Algorithm 'Sudoku' Solver
"""

import random
from wordfreq import top_n_list
from typing import List

# Constants & Variables
POPULATION_SIZE = 40
MAX_GENERATIONS = 500
TOURNAMENT_K = 3
MUTATION_RATE = 0.15
Grid = List[List[str]]


# Functions
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


def empty_grid() -> Grid:
    """
    4×4 grid filled with '.' placeholders.
    """
    return [["." for _ in range(4)] for _ in range(4)]


def is_safe(grid: Grid, row: int, col: int, letter: str) -> bool:
    """
    Return True if `letter` can be placed at (row, col) without conflicts.
    """
    # Row
    if letter in grid[row]:
        return False
    # Column
    if letter in (grid[r][col] for r in range(4)):
        return False
    # 2×2 block
    br, bc = (row // 2) * 2, (col // 2) * 2  # block’s top-left cell
    for r in range(br, br + 2):
        for c in range(bc, bc + 2):
            if grid[r][c] == letter:
                return False
    return True


def generate_starting_grid(letters: List[str], fixed: int = 5) -> Grid:
    """
    Place fixed letters randomly and preserve the constraint rules.
    The rest of the cells remain '.' (blank).
    """
    generated_grid = empty_grid()
    placed = 0
    attempts = 0
    # avoid infinite loops, arbitrary number (200).
    # A 4 × 4 board has only 16 cells. Even trying to place 5 fixed letters, there are at most 16 × 4 = 64 cell/letter combinations.
    # A limit of 200 should be sufficient to find a valid placement.
    while placed < fixed and attempts < 200:
        r, c = random.randint(0, 3), random.randint(0, 3)
        if generated_grid[r][c] != ".":  # already filled
            attempts += 1
            continue
        letter = random.choice(letters)
        if is_safe(generated_grid, r, c, letter):
            generated_grid[r][c] = letter
            placed += 1
        attempts += 1
    if placed < fixed:
        raise RuntimeError("Could not generate a consistent starting grid.")
    return generated_grid


def print_grid(grid: Grid) -> None:
    """
    Formatted grid for console view.
    """
    for row in grid:
        print(" ".join(row))
    print()


# Config
LETTERS = choose_letters()

# Main code
# The partially completed grid is provided by the User.
# In this case, for easier testing, the User is the machine itself that generates a random grid.
print("Using letters:", LETTERS)
starting_grid = generate_starting_grid(LETTERS, fixed=5)
print("Initial (valid, incomplete) grid:")
print_grid(starting_grid)
