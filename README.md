# Sudoku Solver using CSP and Simulated Annealing

## Overview
This project is part of an **Artificial Intelligence** course and focuses on solving Sudoku puzzles using two different AI approaches:
- **Constraint Satisfaction Problems (CSP)**
- **Simulated Annealing (SA)**

The goal is to compare exact search methods with local search techniques in terms of performance, scalability, and solution quality.

## Approaches Implemented

### Constraint Satisfaction Problem (CSP)
Sudoku is modeled as a CSP where:
- Each cell is a variable
- Possible digits form the domain
- Sudoku rules act as constraints

The following CSP techniques were implemented and tested:
- Basic Backtracking
- Minimum Remaining Values (MRV)
- Least Constraining Value (LCV)
- Forward Checking
- Combinations of the above heuristics

CSP guarantees a valid solution when one exists, but performance depends heavily on the heuristics used.

### Simulated Annealing (SA)
Simulated Annealing is implemented as a **local search** approach:
- Starts with a complete but invalid grid
- Iteratively swaps values to reduce constraint violations
- Uses a temperature-based acceptance probability to escape local minima

SA is faster and more scalable for large puzzles, but it does not guarantee a perfect solution.

## Experiments
- Tested on **easy, medium, and hard 9×9 Sudoku puzzles**
- Tested on a **16×16 Sudoku** to evaluate scalability
- Comparison metrics:
  - Runtime
  - Number of iterations / backtracks
  - Solution quality (constraint violations)

Results show that:
- Plain backtracking works well for small puzzles but does not scale
- CSP heuristics significantly improve performance on harder and larger puzzles
- SA quickly finds near-solutions, especially for large puzzles, but rarely reaches a valid solution

## Project Structure
- CSP solver implementations (backtracking, MRV, LCV, Forward Checking)
- Simulated Annealing solver
- Sample Sudoku puzzle files (9×9 and 16×16)
- Full project report with analysis and results

## Technologies Used
- Python
- Artificial Intelligence search techniques
- Constraint Satisfaction Problems
- Simulated Annealing

## Notes
This project was developed for academic purposes to demonstrate and compare different AI problem-solving strategies rather than to optimize for production use.

## Authors
- Omar Shoubaki  
- Omar Takhman
