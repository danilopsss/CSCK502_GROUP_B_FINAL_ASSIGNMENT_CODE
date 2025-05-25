# CSCK502_GROUP_B_FINAL_ASSIGNMENT_CODE

# Genetic Algorithm 4x4 Puzzle Solver

## Requirements

### 1️⃣ Packages

| Package       | Description                              |
|-------------- |------------------------------------------|
| Python ≥ 3.12 | Runtime                                  |
| `wordfreq`    | Supplies a list of English words         |
| `tabulate`    | Pretty-print tabular data in Python      |
| `tqdm`        | Fast, Extensible Progress Meter          |

### 2️⃣  (Recommended) create a virtual environment

```console
python -m venv venv
source venv/bin/activate
```

### 3️⃣  Install dependencies

```console
pip install --upgrade pip
pip install wordfreq
pip install tabulate
pip install tqdm
```

or if you use uv:

```console
uv run ga.py
```

## Running the files

```console
python ga.py
```

or

```console
uv run ga.py
```

## Log files

The log files (.log) contain each the results of 10 executions of the ga.py program.
The following table explains the differences between the files:

| Log file                      | Description                                         |
|-------------------------------|-----------------------------------------------------|
| ga_run_RISK.log               | 10 runs of word 'RISK' and as a target word.        |
| ga_run_WORD.log               | 10 runs of word 'WORD' and as a target word.        |
| ga_run_notarget.log           | 10 runs of random words with no target word.        |
| ga_run_target.log             | 10 runs of random words with each its target word.  |
| ga_run_successes_random.log   | 10 runs of random words success runs <br>with the word as the target.                 |

## Project Overview

The objective is to design and implement a genetic algorithm that solves a 4x4 puzzle similar to Sudoku. Each row, column, and 2x2 subgrid must contain all four unique letters exactly once.

Example of a solved grid using the letters `W`, `O`, `R`, and `D`:

```
W D R O
O R W D
R O D W
D W O R
```

## Constraints

- A 4x4 grid must be filled with 4 distinct letters.
- No letter can repeat in the same row, column, or 2x2 subgrid.
- The initial grid configuration may have pre-filled cells.
- The puzzle may have zero, one, or multiple valid solutions depending on the initial grid.

## Requirements

- Demonstrate the algorithm on multiple initial configurations.
- Display the solution to the puzzle given the initial configuration
- Show all populations created to get to that solution (if a solution is possible, given the initial configuration)
- [optional] display only the solutions that contain a specific word along the edges of the grid (e.g. if you use the four letters ‘W’,’O’,’R’,D’ you may want to show only the solutions that contain the word “WORD” along one or more edges)

## Deliverables

- Submit the solution logic as **pseudocode** and optionally in **Python**.
- A final report (2000–2500 words) detailing:
  - Chromosome representation
  - Fitness function design
  - Genetic operators (selection, crossover, mutation)
  - Experimental results and analysis
  - Justification for algorithmic decisions
