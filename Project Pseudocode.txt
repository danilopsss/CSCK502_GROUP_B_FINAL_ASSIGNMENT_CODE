# 1 - Main Control Loop
PROCEDURE Main()
    # Define the distinct letters to use
    letters ← ["W", "O", "R", "D"]

    # Example user-provided grid (partially filled)
    initialGrid ← [
        ["W", "_", "_", "O"],
        ["_", "_", "_", "_"],
        ["_", "_", "_", "_"],
        ["_", "_", "_", "_"]
    ]

    # GA parameters
    populationSize ← 20
    maxGenerations ← 100
    mutationRate ← 0.03
    crossoverRate ← 0.8
    targetWord ← "WORD"  # Optional goal for word on edge

    # Generate initial population
    population ← InitializePopulation(populationSize, letters, initialGrid)

    FOR generation ← 1 TO maxGenerations DO
        fitnessScores ← []

        # Evaluate fitness of each individual
        FOR EACH individual IN population DO
            score ← Fitness(individual, initialGrid)
            fitnessScores.APPEND(score)

            # If a perfect solution is found
            IF score = 0 THEN
                IF CheckForEdgeWord(individual, targetWord) THEN
                    PrintGrid(individual)
                    PRINT "Solution found in generation", generation
                    RETURN
                END IF
            END IF
        END FOR

        newPopulation ← []

        # Create next generation using selection, crossover, mutation
        WHILE newPopulation.LENGTH < populationSize DO
            parent1 ← Selection(population, fitnessScores)
            parent2 ← Selection(population, fitnessScores)

            child ← Crossover(parent1, parent2, initialGrid)

            IF Random() < mutationRate THEN
                child ← Mutation(child, initialGrid)
            END IF

            newPopulation.APPEND(child)
        END WHILE

        population ← newPopulation
    END FOR

    PRINT "No solution found within", maxGenerations, "generations."
END PROCEDURE


# 2 - Initial Population Generation
PROCEDURE InitializePopulation(size, letters, initialGrid)
    population ← []

    FOR i ← 1 TO size DO
        individual ← []

        FOR rowIndex ← 0 TO 3 DO
            row ← COPY(initialGrid[rowIndex])
            emptyPositions ← []

            # Collect positions that are still empty
            FOR col ← 0 TO 3 DO
                IF row[col] = "_" THEN
                    emptyPositions.APPEND(col)
                END IF
            END FOR

            # Track which letters are already placed
            fixedLetters ← []
            FOR col ← 0 TO 3 DO
                IF row[col] ≠ "_" THEN
                    fixedLetters.APPEND(row[col])
                END IF
            END FOR

            # Fill remaining positions with a random permutation of unused letters
            remainingLetters ← DIFFERENCE(letters, fixedLetters)
            shuffled ← SHUFFLE(remainingLetters)

            FOR EACH pos IN emptyPositions DO
                row[pos] ← shuffled[0]
                shuffled.REMOVE_AT(0)
            END FOR

            individual.APPEND(row)
        END FOR

        population.APPEND(individual)
    END FOR

    RETURN population
END PROCEDURE


# 3 - Fitness Evaluation
PROCEDURE Fitness(grid, initialGrid)
    score ← 0

    # Penalize duplicate letters in columns
    FOR col ← 0 TO 3 DO
        columnLetters ← []
        FOR row ← 0 TO 3 DO
            columnLetters.APPEND(grid[row][col])
        END FOR
        IF COUNT_UNIQUE(columnLetters) ≠ 4 THEN
            score ← score + 1
        END IF
    END FOR

    # Penalize duplicate letters in 2x2 boxes
    FOR boxRow ← 0 TO 1 DO
        FOR boxCol ← 0 TO 1 DO
            boxLetters ← []
            FOR i ← 0 TO 1 DO
                FOR j ← 0 TO 1 DO
                    row ← boxRow * 2 + i
                    col ← boxCol * 2 + j
                    boxLetters.APPEND(grid[row][col])
                END FOR
            END FOR
            IF COUNT_UNIQUE(boxLetters) ≠ 4 THEN
                score ← score + 1
            END IF
        END FOR
    END FOR

    # Large penalty if initial user-provided values are overwritten
    FOR i ← 0 TO 3 DO
        FOR j ← 0 TO 3 DO
            IF initialGrid[i][j] ≠ "_" AND grid[i][j] ≠ initialGrid[i][j] THEN
                score ← score + 10000
            END IF
        END FOR
    END FOR

    RETURN score
END PROCEDURE


# 4 - Tournament Selection
PROCEDURE Selection(population, fitnessScores)
    tournamentSize ← 3
    best ← NULL
    bestScore ← ∞

    # Randomly choose individuals and pick the fittest among them
    FOR i ← 1 TO tournamentSize DO
        idx ← RANDOM_INT(0, population.LENGTH - 1)
        candidate ← population[idx]
        candidateScore ← fitnessScores[idx]

        IF candidateScore < bestScore THEN
            best ← candidate
            bestScore ← candidateScore
        END IF
    END FOR

    RETURN best
END PROCEDURE


# 5 - Crossover Operator
PROCEDURE Crossover(parent1, parent2, initialGrid)
    child ← []

    # Mix rows from parents to create a child
    FOR row ← 0 TO 3 DO
        IF Random() < 0.5 THEN
            childRow ← COPY(parent1[row])
        ELSE
            childRow ← COPY(parent2[row])
        END IF
        child.APPEND(childRow)
    END FOR

    # Reinforce initial values so they're never changed
    FOR i ← 0 TO 3 DO
        FOR j ← 0 TO 3 DO
            IF initialGrid[i][j] ≠ "_" THEN
                child[i][j] ← initialGrid[i][j]
            END IF
        END FOR
    END FOR

    RETURN child
END PROCEDURE


# 6 - Mutation Operator
PROCEDURE Mutation(individual, initialGrid)
    # Randomly choose a row
    row ← RANDOM_INT(0, 3)

    # Pick two mutable positions in the row to swap
    col1 ← RANDOM_INT(0, 3)
    col2 ← RANDOM_INT(0, 3)

    WHILE initialGrid[row][col1] ≠ "_" DO
        col1 ← RANDOM_INT(0, 3)
    END WHILE

    WHILE initialGrid[row][col2] ≠ "_" OR col2 = col1 DO
        col2 ← RANDOM_INT(0, 3)
    END WHILE

    # Swap the two positions
    temp ← individual[row][col1]
    individual[row][col1] ← individual[row][col2]
    individual[row][col2] ← temp

    RETURN individual
END PROCEDURE


# 7 - Validate Final Solution
PROCEDURE IsValidSolution(grid)
    # Check all rows
    FOR i ← 0 TO 3 DO
        row ← grid[i]
        IF COUNT_UNIQUE(row) ≠ 4 THEN
            RETURN FALSE
        END IF
    END FOR

    # Check all columns
    FOR j ← 0 TO 3 DO
        column ← []
        FOR i ← 0 TO 3 DO
            column.APPEND(grid[i][j])
        END FOR
        IF COUNT_UNIQUE(column) ≠ 4 THEN
            RETURN FALSE
        END IF
    END FOR

    # Check all 2x2 subgrids
    FOR boxRow ← 0 TO 1 DO
        FOR boxCol ← 0 TO 1 DO
            box ← []
            FOR i ← 0 TO 1 DO
                FOR j ← 0 TO 1 DO
                    box.APPEND(grid[boxRow*2 + i][boxCol*2 + j])
                END FOR
            END FOR
            IF COUNT_UNIQUE(box) ≠ 4 THEN
                RETURN FALSE
            END IF
        END FOR
    END FOR

    RETURN TRUE
END PROCEDURE


# 8 - Optional: Check for Target Word on Grid Edges
PROCEDURE CheckForEdgeWord(grid, word)
    # Construct strings for top, bottom, left, right edges
    top ← JOIN(grid[0])
    bottom ← JOIN(grid[3])
    left ← grid[0][0] & grid[1][0] & grid[2][0] & grid[3][0]
    right ← grid[0][3] & grid[1][3] & grid[2][3] & grid[3][3]

    # Return true if any edge forms the target word
    IF top = word OR bottom = word OR left = word OR right = word THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    END IF
END PROCEDURE
