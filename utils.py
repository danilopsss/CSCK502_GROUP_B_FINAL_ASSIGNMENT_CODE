"""
4×4 Genetic-Algorithm 'Sudoku' Solver Utility Functions
This module provides utility functions for generating and manipulating a 4x4 grid
"""

import random
from wordfreq import top_n_list
from typing import List

# Constants & Variables
PRINT_CONSOLE = True  # False to suppress console spam
WRITE_FILE = True  # False to avoid touching ga_run.log
LOG_SUCCESS_ONLY = False  # True to log only successful runs
LOGFILE = "ga_run.log"
_run_buffer: list[str] = []
Grid = List[List[str]]


# Functions
def log(msg: str, end: str = "\n"):
    """
    Print to console or append to the log file based on parameters.
    """
    if PRINT_CONSOLE:
        print(msg, end=end)
    _run_buffer.append(msg + end)


def flush_log(success: bool):
    """
    Write the buffered lines to file if WRITE_FILE is True
    and (success or not LOG_SUCCESS_ONLY).
    Then clear the buffer for the next run.
    """
    global _run_buffer
    if WRITE_FILE and (success or not LOG_SUCCESS_ONLY):
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.writelines(_run_buffer)
    _run_buffer = []  # reset for next run


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


def empty_grid(size: int) -> Grid:
    """
    4×4 grid filled with '_' placeholders.
    """
    return [["_" for _ in range(size)] for _ in range(size)]


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


def generate_starting_grid(
    grid: list[list], letters: List[str], fixed: int = 5
) -> Grid:
    """
    Place fixed letters randomly and preserve the constraint rules.
    The rest of the cells remain '_' (blank).
    """
    placed = 0
    attempts = 0
    # avoid infinite loops, arbitrary number (200).
    # A 4 × 4 board has only 16 cells. Even trying to place 5 fixed letters, there are at most 16 × 4 = 64 cell/letter combinations.
    # A limit of 200 should be sufficient to find a valid placement.
    while placed < fixed and attempts < 200:
        r, c = random.randint(0, 3), random.randint(0, 3)
        if grid[r][c] != "_":  # already filled
            attempts += 1
            continue
        letter = random.choice(letters)
        if is_safe(grid, r, c, letter):
            grid[r][c] = letter
            placed += 1
        attempts += 1
    if placed < fixed:
        raise RuntimeError("Could not generate a consistent starting grid.")
    return grid


def print_grid(grid):
    """
    Formatted grid for console view.
    """
    for row in grid:
        log(" ".join(row))
    log("")
