import random
from utils import empty_grid, generate_starting_grid, choose_letters


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


def print_grid(grid):
    for row in grid:
        print(" ".join(row))
    print()  # Print a newline for better readability


def check_for_edge_word(grid, word=None):
    # If no word is provided, return True (no edge word check)
    if not word:
        return True
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
    """
    Hybrid mutation function that randomly does row swaps or column swaps.
    50% Chance to swap two mutable cells in a random row
    50% Chance to swap two mutable cells in a random column.
    """

    def row_swap():
        # Randomly choose a row
        row = random.randint(0, 3)
        # Find mutable positions in the selected row
        mutable_positions = [col for col in range(4) if initial_grid[row][col] == "_"]
        if len(mutable_positions) >= 2:
            col1, col2 = random.sample(mutable_positions, 2)
            individual[row][col1], individual[row][col2] = (
                individual[row][col2],
                individual[row][col1],
            )

    def column_swap():
        # Randomly choose a column
        col = random.randint(0, 3)
        # find mutable positions in the selected column
        mutable_positions = [row for row in range(4) if initial_grid[row][col] == "_"]
        if len(mutable_positions) >= 2:
            row1, row2 = random.sample(mutable_positions, 2)
            individual[row1][col], individual[row2][col] = (
                individual[row2][col],
                individual[row1][col],
            )

    # decide randomly whether to swap rows or columns
    if random.random() < 0.5:
        row_swap()
    else:
        column_swap()

    return individual


def crossover(parent1, parent2, initial_grid):
    """
    Hybrid crossover function
    50% row-based one-point crossover
    50% column-based one-point crossover.
    """

    # Decide which crossover method to use
    if random.random() < 0.5:
        # row-based crossover
        cut = random.randint(1, 3)  # position 1..3
        child = parent1[:cut] + parent2[cut:]
    else:
        # column-based crossover
        cut = random.randint(1, 3)
        child = []
        for row_index in range(4):
            child.append(parent1[row_index][:cut] + parent2[row_index][cut:])

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


def edge_penalty(grid, word):
    """
    Return 0 if the target word appears on any edge, else return
    the *minimum* Hamming distance between the word and each edge.
    """
    top = "".join(grid[0])
    bottom = "".join(grid[3])
    left = "".join(r[0] for r in grid)
    right = "".join(r[3] for r in grid)

    # Word already present → no penalty
    if word in (top, bottom, left, right):
        return 0

    # Compute how many letters differ for each edge
    def hamming(a, b):
        return sum(x != y for x, y in zip(a, b))

    return min(
        hamming(top, word),
        hamming(bottom, word),
        hamming(left, word),
        hamming(right, word),
    )


def fitness(grid, initial_grid, target_word=None):
    """
    Calculate fitness score of the grid.
    Each rule violation adds the exact count of duplicates
        (4 - unique).
        This give the genetic algorithm a smoother gradient.
    Lower score = better solution.
    """
    score = 0

    # Penalize duplicate letters in rows
    for row in grid:
        score += 4 - len(set(row))

    # Penalize duplicate letters in columns
    for col in range(4):  # Assuming a 4x4 grid
        column_letters = [grid[row][col] for row in range(4)]
        score += 4 - len(set(column_letters))
        # if len(set(column_letters)) != 4:  # Check for unique letters
        #    score += 1

    # Penalize duplicate letters in 2x2 boxes
    for box_row in range(2):  # 2x2 boxes
        for box_col in range(2):
            box_letters = []
            for i in range(2):
                for j in range(2):
                    row = box_row * 2 + i
                    col = box_col * 2 + j
                    box_letters.append(grid[row][col])
            score += 4 - len(set(box_letters))
            # if len(set(box_letters)) != 4:  # Check for unique letters
            #    score += 1

    # Large penalty if initial user-provided values are overwritten
    for i in range(4):
        for j in range(4):
            if initial_grid[i][j] != "_" and grid[i][j] != initial_grid[i][j]:
                score += 10000  # Large penalty

    if target_word:
        score += edge_penalty(grid, target_word)

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


def main():
    # Define the distinct letters to use
    letters = ["W", "O", "R", "D"]
    # random.seed(42)
    # letters = choose_letters()
    print("Using letters:", letters)
    initial_grid = empty_grid(size=4)
    initial_grid = generate_starting_grid(grid=initial_grid, letters=letters, fixed=5)
    # Patch the initial grid to guarantee that the target word is always placeable
    for row, col in [(0, 0), (0, 3), (3, 0), (3, 3)]:
        if initial_grid[row][col] != "_":
            initial_grid[row][col] = "_"
    print("Initial (valid, incomplete) grid:")
    print_grid(initial_grid)

    # GA parameters
    population_size = 40
    max_generations = 500
    mutation_rate = 0.15
    target_word = "".join(letters)  # Optional goal for word on edge
    # target_word = None
    print("Target word:", target_word)

    # Generate initial population
    population = initialize_population(population_size, letters, initial_grid)

    for generation in range(1, max_generations + 1):
        fitness_scores = []
        print(f"\nGeneration {generation}")
        # Evaluate fitness of each individual
        for individual in population:
            score = fitness(individual, initial_grid, target_word)
            fitness_scores.append(score)

            flat = " ".join("".join(row) for row in individual)
            print(f"{flat} fit={score}")

            # If a perfect solution is found
            if score == 0:
                if check_for_edge_word(individual, target_word):
                    print_grid(individual)
                    print(f"Solution found in generation {generation}")
                    return

        new_population = []

        # Create next generation using selection, crossover, mutation
        while len(new_population) < population_size:
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)

            child = crossover(parent1, parent2, initial_grid)

            if random.random() < mutation_rate:
                child = mutation(child, initial_grid)

            new_population.append(child)

        population = new_population

    print(f"No solution found within {max_generations} generations.")


# Call the main function to start the algorithm
if __name__ == "__main__":
    main()
