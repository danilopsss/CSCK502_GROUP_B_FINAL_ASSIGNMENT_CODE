import random
import time
import datetime
from utils import (
    empty_grid,
    generate_starting_grid,
    choose_letters,
    log,
    flush_log,
    print_grid,
)

# Constants & Variables
POPULATION_SIZE = 1000
MAX_GENERATIONS = 500
TOURNAMENT_K = 3
MUTATION_RATE = 0.15


def is_valid_solution(grid):
    # Check all rows for uniqueness
    for row in grid:
        if len(set(row)) != 4:  # Check if all letters are unique
            return False

    # Check all columns for uniqueness
    for col in range(4):
        column = [grid[row][col] for row in range(4)]
        if len(set(column)) != 4:  # Check if all letters are unique
            return False

    # Check all 2x2 subgrids for uniqueness
    for box_row in range(2):
        for box_col in range(2):
            box = []
            for i in range(2):
                for j in range(2):
                    box.append(grid[box_row * 2 + i][box_col * 2 + j])
            if len(set(box)) != 4:  # Check if all letters are unique
                return False

    return True


def check_for_edge_word(grid, word):
    # Construct strings for top, bottom, left, right edges
    top = "".join(grid[0])
    bottom = "".join(grid[3])
    left = "".join(grid[i][0] for i in range(4))
    right = "".join(grid[i][3] for i in range(4))

    # Return true if any edge forms the target word
    if top == word or bottom == word or left == word or right == word:
        return True
    else:
        return False


def mutation(individual, initial_grid):
    # Randomly choose a row
    row = random.randint(0, 3)

    # Find mutable positions in the selected row
    mutable_positions = [col for col in range(4) if initial_grid[row][col] == "_"]

    if len(mutable_positions) < 2:
        return individual  # No mutation if there are less than 2 mutable positions

    # Pick two mutable positions in the row to swap
    col1, col2 = random.sample(mutable_positions, 2)

    # Swap the two positions
    individual[row][col1], individual[row][col2] = (
        individual[row][col2],
        individual[row][col1],
    )

    return individual


def crossover(parent1, parent2, initial_grid):
    child = []

    # Mix rows from parents to create a child
    for row_index in range(4):  # Assuming a 4x4 grid
        if random.random() < 0.5:  # Randomly choose which parent to take the row from
            child_row = parent1[row_index][:]
        else:
            child_row = parent2[row_index][:]

        child.append(child_row)

    # Reinforce initial values so they're never changed
    for i in range(4):
        for j in range(4):
            if initial_grid[i][j] != "_":
                child[i][j] = initial_grid[i][j]

    return child


def selection(population, fitness_scores):
    tournament_size = 3  # Size of the tournament
    best = None
    best_score = float("inf")  # Start with a very high score

    # Randomly choose individuals and pick the fittest among them
    for _ in range(tournament_size):
        idx = random.randint(0, len(population) - 1)  # Random index
        candidate = population[idx]
        candidate_score = fitness_scores[idx]

        if candidate_score < best_score:  # Check if this candidate is better
            best = candidate
            best_score = candidate_score

    return best


def fitness(grid, initial_grid):
    score = 0

    # Penalize duplicate letters in columns
    for col in range(4):  # Assuming a 4x4 grid
        column_letters = [grid[row][col] for row in range(4)]
        if len(set(column_letters)) != 4:  # Check for unique letters
            score += 1

    # Penalize duplicate letters in 2x2 boxes
    for box_row in range(2):  # 2x2 boxes
        for box_col in range(2):
            box_letters = []
            for i in range(2):
                for j in range(2):
                    row = box_row * 2 + i
                    col = box_col * 2 + j
                    box_letters.append(grid[row][col])
            if len(set(box_letters)) != 4:  # Check for unique letters
                score += 1

    # Large penalty if initial user-provided values are overwritten
    for i in range(4):
        for j in range(4):
            if initial_grid[i][j] != "_" and grid[i][j] != initial_grid[i][j]:
                score += 10000  # Large penalty

    return score


def initialize_population(size, letters, initial_grid):
    population = []

    for _ in range(size):
        individual = []

        for row_index in range(4):  # Assuming a 4x4 grid
            row = initial_grid[row_index][:]  # Copy the initial row
            empty_positions = []

            # Collect positions that are still empty
            for col in range(4):
                if row[col] == "_":
                    empty_positions.append(col)

            # Track which letters are already placed
            fixed_letters = [row[col] for col in range(4) if row[col] != "_"]

            # Fill remaining positions with a random permutation of unused letters
            remaining_letters = list(set(letters) - set(fixed_letters))
            random.shuffle(remaining_letters)

            for pos in empty_positions:
                row[pos] = remaining_letters.pop(0)  # Fill with remaining letters

            individual.append(row)

        population.append(individual)

    return population


def run_ga(
    pop_size: int,
    mut_rate: float,
    max_gens: int = 300,
    fixed_clues: int = 5,
    use_edge_word: bool = True,
    letters: list[str] | None = None,
    seed: int | None = None,
) -> tuple[bool, int, float]:
    """
    Run GA once with the given parameters.
    Returns (success, generations_used, elapsed_seconds).
    """
    if seed is not None:
        random.seed(seed)

    edge_word = "".join(letters) if use_edge_word else None
    init_grid = empty_grid(4)
    init_grid = generate_starting_grid(init_grid, letters, fixed_clues)
    for r, c in [(0, 0), (0, 3), (3, 0), (3, 3)]:
        init_grid[r][c] = "_"  # keep corners free

    population = initialize_population(pop_size, letters, init_grid)
    start_clock = time.perf_counter()

    for gen in range(1, max_gens + 1):
        fits = [fitness(ind, init_grid) for ind in population]
        best_idx = min(range(pop_size), key=fits.__getitem__)
        best_fit = fits[best_idx]
        elite = population[best_idx]

        if best_fit == 0 and check_for_edge_word(elite, edge_word):
            return True, gen, time.perf_counter() - start_clock

        new_pop = []
        while len(new_pop) < pop_size:
            p1 = selection(population, fits)
            p2 = selection(population, fits)
            child = crossover(p1, p2, init_grid)
            if random.random() < mut_rate:
                child = mutation(child, init_grid)
            new_pop.append(child)
        new_pop.append(elite)
        if len(new_pop) > pop_size:
            new_pop.pop(random.randrange(len(new_pop)))
        population = new_pop

    return False, max_gens, time.perf_counter() - start_clock


def main():
    log(f"\n=== New run {datetime.datetime.now():%Y-%m-%d %H:%M:%S} ===")
    # Define the distinct letters to use
    letters = ["W", "O", "R", "D"]
    # letters = ["R", "I", "S", "K"]
    # letters = choose_letters()
    initial_grid = empty_grid(size=4)
    initial_grid = generate_starting_grid(grid=initial_grid, letters=letters, fixed=2)
    log("Initial (valid, incomplete) grid:")
    print_grid(initial_grid)

    # GA parameters
    target_word = "".join(letters)  # Optional goal for word on edge
    log(f"Target word: {target_word}")

    # Generate initial population
    population = initialize_population(POPULATION_SIZE, letters, initial_grid)

    for generation in range(1, MAX_GENERATIONS + 1):
        fitness_scores = []
        log(f"\nGeneration {generation}")

        # Evaluate fitness of each individual
        for individual in population:
            score = fitness(individual, initial_grid)
            fitness_scores.append(score)

            flat = " ".join("".join(row) for row in individual)
            log(f"{flat} fit={score}")

            # If a perfect solution is found
            if score == 0:
                if check_for_edge_word(individual, target_word):
                    print_grid(individual)
                    log(
                        f"Solution found in generation {generation}, for letters {letters}."
                    )
                    return

        new_population = []

        # Create next generation using selection, crossover, mutation
        while len(new_population) < POPULATION_SIZE:
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)

            child = crossover(parent1, parent2, initial_grid)

            if random.random() < MUTATION_RATE:
                child = mutation(child, initial_grid)

            new_population.append(child)

        population = new_population

    log(
        f"No solution found within {MAX_GENERATIONS} generations, for letters {letters}."
    )


# Call the main function to start the algorithm
if __name__ == "__main__":
    main()
