import time
import math

#Loads an easy/medium/hard or a 16x16 puzzle from the selected textfile
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
                    # support G = 16 while keeping everything else the same
                    if ch.upper() == 'G':
                        row.append(16)
                    else:
                        # this is used for the 16x16 puzzle but works for both
                        row.append(int(ch, 16))

            puzzle.append(row)

    return puzzle

# constraints checking
def isValid(grid, row, col, value):
    size = len(grid)

    # row check
    if value in grid[row]:
        return False

    # column check
    for r in range(size):
        if grid[r][col] == value:
            return False

    # box check (works for 9x9 and 16x16)
    box_size = int(math.sqrt(size))
    #box rows and columns are 0,3,6 for 9x9 and 0,4,8,12 for 16x16
    box_row = int(math.floor(row / box_size) * box_size)
    box_column = int(math.floor(col / box_size) * box_size)

    for r in range(box_row, box_row + box_size):
        for c in range(box_column, box_column + box_size):
            if grid[r][c] == value:
                return False

    return True

# getting domain (list of all legal values)
def getDomain(grid, row, col):
    domain = []
    size = len(grid)

    for v in range(1, size + 1):
        if isValid(grid, row, col, v):
            domain.append(v)

    return domain

"""
 this functiions selects the unassigned variable
 if we dont use mrv we just use the first unassigned variable
    if we use mrv we select the cell with the smallest domain
 """
def getUnassignedVariable(grid, heuristics):
    size = len(grid)
    if not heuristics["mrv"]:

        for r in range(size):
            for c in range(size):
                if grid[r][c] == 0:
                    return (r, c)
        return None
    else:
        #if we are using mrv (minimum remaining values) we need to find the cell with the smallest domain
        selected_cell = None
        min_domain_size = 200
        for r in range(size):
            for c in range(size):
                if grid[r][c] == 0:
                    domain_size = len(getDomain(grid, r, c))
                    if domain_size < min_domain_size:
                        min_domain_size = domain_size
                        selected_cell = (r, c)
        return selected_cell

"""
helps in lcv by selecting the value
that has the least constraining effects on its neighboring
rows, columns, and boxes
"""
def constraintsCount(grid, row, col, value):
    size = len(grid)
    count = 0

    # row neighbors
    for column in range(size):
        #the if statement makes sure we skip the cell we're on
        if grid[row][column] == 0 and column != col:
            if isValid(grid, row, column, value):
                count += 1

    # column neighbors
    for r in range(size):
        if grid[r][col] == 0 and r != row:
            if isValid(grid, r, col, value):
                count += 1

    # box neighbors
    box_size = int(math.sqrt(size))
    box_row = int(math.floor(row / box_size) * box_size)
    box_column = int(math.floor(col / box_size) * box_size)
    for r in range(box_row, box_row + box_size):
        for c in range(box_column, box_column + box_size):
            if grid[r][c] == 0 and (r != row and c != col):
                if isValid(grid, r, c, value):
                    count += 1

    return count

def orderDomainValues(grid, row, col, heuristics):
    domain = getDomain(grid, row, col)
    if not heuristics["lcv"]:
        return domain

    #list of tuples first element is constraint count second is the value which generated it
    scored = []
    for value in domain:
        score = constraintsCount(grid, row, col, value)
        scored.append((score, value))

    #sort by first element of tuple (constraint count)
    scored.sort()

    ordered_scores = []
    for pair in scored:
        ordered_scores.append(pair[1])
    return ordered_scores

#  forward checking
def hasEmptyDomain(grid):
    size = len(grid)
    for r in range(size):
        for c in range(size):
            if grid[r][c] == 0:
                if len(getDomain(grid, r, c)) == 0:
                    return True
    return False

def backtrack(grid, heuristics):
    global iterations
    iterations += 1

    unassigned = getUnassignedVariable(grid, heuristics)
    if unassigned is None:
        return True

    row, col = unassigned

    for value in orderDomainValues(grid, row, col, heuristics):
        if isValid(grid, row, col, value):
            grid[row][col] = value

            # forward checking step
            if heuristics["fc"]:
                if hasEmptyDomain(grid):
                    grid[row][col] = 0
                    continue

            if not backtrack(grid, heuristics):
                grid[row][col] = 0
            else:
                return True

            grid[row][col] = 0

    return False

def csp(grid, heuristics):
    print("Solving with CSP:")
    global iterations
    iterations = 0
    start_time = time.time()
    result = backtrack(grid, heuristics)
    end_time = time.time()
    total_time = (end_time - start_time) * 1000
    print("Time taken: {:.4f} ms".format(total_time))
    print("Iterations:", iterations)
    print()
    return result

def print_grid(grid):
    for row in grid:
        line = ""

        for x in row:
            if x == 0:
                line += "0 "          # empty cell
            elif x <= 9:
                line += str(x) + " "
            else:
                # convert 10-16 to A-G
                line += chr(ord('A') + (x - 10)) + " "

        print(line)
    print()

# Menu
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

heuristics = {"mrv": False, "lcv": False, "fc": False}

print("\nChoose heuristics:")
print("1. Plain Backtracking")
print("2. Backtracking with MRV")
print("3. Backtracking with LCV")
print("4. Backtracking with Forward Checking")
print("5. Backtracking with both MRV and LCV")
print("6. Backtracking with MRV, LCV, and Forward Checking")
choice = input("Enter choice (1-6): ")

if choice == "2":
    heuristics["mrv"] = True
elif choice == "3":
    heuristics["lcv"] = True
elif choice == "4":
    heuristics["fc"] = True
elif choice == "5":
    heuristics["mrv"] = True
    heuristics["lcv"] = True
elif choice == "6":
    heuristics["mrv"] = True
    heuristics["lcv"] = True
    heuristics["fc"] = True
elif choice != "1":
    print("Invalid choice")
    exit()

print("\nSettings selected")
print(f"Puzzle size: {len(puzzle)}x{len(puzzle)}")
print(f"Heuristics: MRV = {heuristics['mrv']}, LCV = {heuristics['lcv']}, Forward Checking = {heuristics['fc']}\n")

if csp(puzzle, heuristics):
    print("Solution found:")
    print_grid(puzzle)
else:
    print("No solution exists")
