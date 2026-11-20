# Sudoku Solver

A Python Sudoku solver using Algorithm X and exact-cover constraint modeling.

## Overview

This project models a standard 9x9 Sudoku puzzle as an exact-cover problem. Each possible placement of a number must satisfy four constraints:

- Each cell contains one number
- Each row contains each number once
- Each column contains each number once
- Each 3x3 box contains each number once

The solver uses Algorithm X to search for a set of placements that satisfies every constraint.

## Features

- Solves standard 9x9 Sudoku puzzles
- Uses Algorithm X
- Models Sudoku as an exact-cover problem
- Validates rows, columns, and 3x3 boxes
- Accepts `0` or `.` for empty cells
- Includes automated tests

## Technologies

- Python
- Algorithm X
- Exact Cover
- Constraint Solving
- Recursion

## Run

```bash
python3 sudoku_solver.py