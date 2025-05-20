from random import randint
from itertools import permutations


matrix = [[""] * 4 for _ in range(4)]


def generate_population(
    size: int,
    letters: list[str],
    initial_grid: list[list[str]]
):
    population = [] # is the outter matrix
    for idx_row in range(size):
        individual = []  # is the inner matrix
        for idx_col in range(len(idx_row)):
            row = initial_grid[idx_row]
            # this is not actually needed
            empty_positions = [idx for idx, val in enumerate(row) if not val]
            fixed_letters = [idx for idx, val in enumerate(row) if val]
            # remaining_letters = letters - fixed_letters ?> Needs verification with Badr
            # shuffled = permutations(remaining_letters)
            for emptypos in empty_positions:
                # row[emptypos] = shuffled.pop(0)
                ...
            individual.append(row)
        population.append(individual)
    return population


def fitness(individual, initial_grid):
    score = 0
    # column violations
    for idxrow, _ in enumerate(individual):
        column_letters = [individual[idxrow][col] for col in range(4)]
        duplicates = 4 - len(set(column_letters))
        score += duplicates

    # subgrid violations (2x2)
    for subrow in [0, 2]:
        for subCol in [0, 2]:
            block = []
            for i in [0, 1]:
                for j in [0, 1]:
                    block.append(individual[subrow + i][subCol + j])
            duplicates = 4 - len(set(block))
            score += duplicates

    # check violations of fixed letters
    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2, 3]:
            if initial_grid[i][j] != "":
                if individual[i][j] != initial_grid[i][j]:
                    score += 1000   # heavy penalty
    return score


def tournament_selection(population, fitnesses, k):
    randrow = randint(0, 3)
    randcol = randint(0, 3)

    selected = population[randrow][randcol]
    best = min(selected, key=lambda x: fitnesses[population.index(x)])

    return best


# pending 5, 6, 7 and 8
# some questions were raised to Badr, I'm waiting his feedback.

