import time
import math
import random

# loading puzzle
def loadPuzzle(file_path):
    puzzle = []
    
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            row = []

            for ch in line:
                if ch == '0':
                    row.append(0)

                else:
                    if ch.upper() in 'ABCDEFG':
                        row.append(10 + ord(ch.upper()) - ord('A'))
                    else:
                        row.append(int(ch))

            puzzle.append(row)

    return puzzle

# copy grid without using copy module
def copy_grid(grid):
    return [row[:] for row in grid]

# generate initial solution: fill empty cells with random valid numbers
def generateInitialSolution(puzzle):
    solution = copy_grid(puzzle)
    size = len(puzzle)
    
    # fill each 3x3 box with random of 1-9 (no duplicates in box)
    box_size = int(math.sqrt(size))
    
    for box_r in range(0, size, box_size):
        for box_c in range(0, size, box_size):
            # collect fixed numbers in this box
            fixed_in_box = set()
            for r in range(box_r, box_r + box_size):
                for c in range(box_c, box_c + box_size):
                    if solution[r][c] != 0:
                        fixed_in_box.add(solution[r][c])
            
            # fill empty cells in box with random numbers not already in box
            available = [num for num in range(1, size+1) if num not in fixed_in_box]
            random.shuffle(available)
            
            idx = 0
            for r in range(box_r, box_r + box_size):
                for c in range(box_c, box_c + box_size):
                    if solution[r][c] == 0:
                        solution[r][c] = available[idx]
                        idx += 1
    
    return solution

# calculate total violations
def calculateViolations(grid):
    size = len(grid)
    violations = 0
    
    # 1. row violations (count duplicates in each row)
    for r in range(size):
        row = grid[r]
        # count how many times each number appears
        counts = [0] * (size + 1)
        for num in row:
            if num != 0:
                counts[num] += 1
        # add violations: for each number, if appears > 1, add (count-1)
        for count in counts:
            if count > 1:
                violations += (count - 1)
    
    # 2. column violations
    for c in range(size):
        counts = [0] * (size + 1)
        for r in range(size):
            num = grid[r][c]
            if num != 0:
                counts[num] += 1
        for count in counts:
            if count > 1:
                violations += (count - 1)
    
    # 3. box violations
    box_size = int(math.sqrt(size))
    for box_r in range(0, size, box_size):
        for box_c in range(0, size, box_size):
            counts = [0] * (size + 1)
            for r in range(box_r, box_r + box_size):
                for c in range(box_c, box_c + box_size):
                    num = grid[r][c]
                    if num != 0:
                        counts[num] += 1
            for count in counts:
                if count > 1:
                    violations += (count - 1)
    
    return violations

# generate neighbor: swap two cells in the same row 
def generateNeighbor(grid, fixed_cells):
    size = len(grid)
    neighbor = copy_grid(grid)
    
    # try swapping two not fixed cells in a random 3x3 box
    box_size = int(math.sqrt(size))
    
    for _ in range(100):
        # pick random box
        box_r = random.randint(0, size//box_size - 1) * box_size
        box_c = random.randint(0, size//box_size - 1) * box_size
        
        # find all not fixed cells in this box
        non_fixed_cells = []
        for r in range(box_r, box_r + box_size):
            for c in range(box_c, box_c + box_size):
                if (r, c) not in fixed_cells:
                    non_fixed_cells.append((r, c))
        
        if len(non_fixed_cells) >= 2:
            cell1, cell2 = random.sample(non_fixed_cells, 2)
            r1, c1 = cell1
            r2, c2 = cell2
            
            # swap values
            neighbor[r1][c1], neighbor[r2][c2] = neighbor[r2][c2], neighbor[r1][c1]
            return neighbor
    
    return grid

# simulated annealing algorithm
def simulatedAnnealing(puzzle, initial_temp=1000.0, cooling_rate=0.99, min_temp=0.1, max_iterations=100000):
    print("Solving with Simulated Annealing:")
    
    # track fixed cells (original puzzle numbers that cant change)
    fixed_cells = set()
    for r in range(len(puzzle)):
        for c in range(len(puzzle)):
            if puzzle[r][c] != 0:
                fixed_cells.add((r, c))
    
    # generate initial solution
    current_solution = generateInitialSolution(puzzle)
    current_violations = calculateViolations(current_solution)
    
    best_solution = copy_grid(current_solution)
    best_violations = current_violations
    
    temperature = initial_temp
    iteration = 0
    start_time = time.time()
    
    print(f"Initial violations: {current_violations}")
    print(f"Temperature schedule: {initial_temp} -> {min_temp} (rate: {cooling_rate})")
    
    while temperature > min_temp and iteration < max_iterations and best_violations > 0:
        # generate neighbor
        neighbor = generateNeighbor(current_solution, fixed_cells)
        neighbor_violations = calculateViolations(neighbor)
        
        # calculate energy difference (we want to MINIMIZE violations)
        delta = neighbor_violations - current_violations
        
        # acceptance criteria
        if delta < 0:
            # Better solution always accept
            current_solution = neighbor
            current_violations = neighbor_violations
        else:
            # worse solution accept with probability
            acceptance_prob = math.exp(-delta / temperature)
            if random.random() < acceptance_prob:
                current_solution = neighbor
                current_violations = neighbor_violations
        
        # update best solution
        if current_violations < best_violations:
            best_solution = copy_grid(current_solution)
            best_violations = current_violations
        
        # cool down
        temperature *= cooling_rate
        iteration += 1
        
        # progress report every 10000 iterations
        
        if iteration % 10000 == 0:
            print(f"Iteration {iteration}: Temp={temperature:.2f}, Best violations={best_violations}")
    
    end_time = time.time()
    total_time = (end_time - start_time) * 1000  # convert to ms
    
    return best_solution, best_violations, total_time, iteration

def print_grid(grid):
    size = len(grid)
    for r in range(size):
        line = ""
        for c in range(size):
            val = grid[r][c]
            if size == 16:
                if val == 0:
                    line += "0 "
                elif val == 16:
                    line += "G "
                elif val >= 10:
                    # Convert 10-15 to A-F
                    line += f"{chr(ord('A') + (val - 10))} "
                else:
                    line += f"{val} "
            else:
                line += f"{val} "
        print(line)
    print()

# main menu
def main():
    print("Choose puzzle difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. 16x16 Puzzle")
    choice = input("Enter choice (1-4): ")
    
    if choice == '1':
        puzzle = loadPuzzle("easy.txt")
    elif choice == '2':
        puzzle = loadPuzzle("medium.txt")
    elif choice == '3':
        puzzle = loadPuzzle("hard.txt")
    elif choice == '4':
        puzzle = loadPuzzle("16x16.txt")
    else:
        print("Invalid entry")
        exit()
    
    print("\nLoaded puzzle:")
    print_grid(puzzle)
    
    # get SA parameters from user (or use defaults)
    print("\nSimulated Annealing Parameters (press Enter for defaults):\n")
    initial_temp = input(f"Initial temperature (default 1000.0): ")
    cooling_rate = input(f"Cooling rate (default 0.99): ")
    min_temp = input(f"Minimum temperature (default 0.1): ")
    max_iter = input(f"Maximum iterations (default 100000): ")
    
    # use defaults if empty
    if initial_temp == "":
        initial_temp = 1000.0
    else:
        initial_temp = float(initial_temp)
    
    if cooling_rate == "":
        cooling_rate = 0.99
    else:
        cooling_rate = float(cooling_rate)
    
    if min_temp == "":
        min_temp = 0.1
    else:
        min_temp = float(min_temp)
    
    if max_iter == "":
        max_iter = 100000
    else:
        max_iter = int(max_iter)
    
    # run SA
    solution, violations, time_ms, iterations = simulatedAnnealing(
        puzzle, initial_temp, cooling_rate, min_temp, max_iter
    )
    
    print("\nFinal solution:")
    print_grid(solution)
    
    print("\nSA Results Summary:")
    print(f"Violations: {violations}")
    print(f"Time: {time_ms:.4f} ms")
    print(f"Iterations: {iterations}")
    print(f"Valid solution: {'yes' if violations == 0 else 'no'}")

if __name__ == "__main__":
    main()