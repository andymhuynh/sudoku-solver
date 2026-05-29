"""
Sudoku Solver using Algorithm X / Exact Cover.

Run:
    python sudoku_solver.py

Input format:
    Use 0 or . for empty cells.
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple, Optional


Cell = Tuple[int, int]
Constraint = Tuple[str, int, int]
Option = Tuple[int, int, int]


class SudokuSolver:
    SIZE = 9
    BOX = 3

    def __init__(self, board: str) -> None:
        self.board = self._parse_board(board)
        self.constraints: Dict[Constraint, Set[Option]] = {}
        self.options: Dict[Option, List[Constraint]] = {}
        self.solution: List[Option] = []

        self._build_exact_cover()

    def _parse_board(self, board: str) -> List[List[int]]:
        chars = [char for char in board if char.isdigit() or char == "."]

        if len(chars) != 81:
            raise ValueError("Board must contain exactly 81 cells.")

        parsed_board = []

        for row in range(self.SIZE):
            current_row = []

            for col in range(self.SIZE):
                char = chars[row * self.SIZE + col]

                if char == "." or char == "0":
                    current_row.append(0)
                elif "1" <= char <= "9":
                    current_row.append(int(char))
                else:
                    raise ValueError("Board may only contain digits, 0, or dots.")

            parsed_board.append(current_row)

        self._validate_board(parsed_board)
        return parsed_board

    def _validate_board(self, board: List[List[int]]) -> None:
        for row in range(self.SIZE):
            values = [board[row][col] for col in range(self.SIZE) if board[row][col] != 0]

            if len(values) != len(set(values)):
                raise ValueError(f"Duplicate value found in row {row + 1}.")

        for col in range(self.SIZE):
            values = [board[row][col] for row in range(self.SIZE) if board[row][col] != 0]

            if len(values) != len(set(values)):
                raise ValueError(f"Duplicate value found in column {col + 1}.")

        for box_row in range(0, self.SIZE, self.BOX):
            for box_col in range(0, self.SIZE, self.BOX):
                values = []

                for row in range(box_row, box_row + self.BOX):
                    for col in range(box_col, box_col + self.BOX):
                        if board[row][col] != 0:
                            values.append(board[row][col])

                if len(values) != len(set(values)):
                    raise ValueError("Duplicate value found in a 3x3 box.")

    def _box_index(self, row: int, col: int) -> int:
        return (row // self.BOX) * self.BOX + (col // self.BOX)

    def _get_constraints(self, row: int, col: int, value: int) -> List[Constraint]:
        return [
            ("cell", row, col),
            ("row", row, value),
            ("col", col, value),
            ("box", self._box_index(row, col), value),
        ]

    def _build_exact_cover(self) -> None:
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                possible_values = (
                    [self.board[row][col]]
                    if self.board[row][col] != 0
                    else range(1, 10)
                )

                for value in possible_values:
                    option = (row, col, value)
                    constraints = self._get_constraints(row, col, value)

                    self.options[option] = constraints

                    for constraint in constraints:
                        if constraint not in self.constraints:
                            self.constraints[constraint] = set()

                        self.constraints[constraint].add(option)

    def solve(self) -> Optional[List[List[int]]]:
        if self._search():
            solved_board = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]

            for row, col, value in self.solution:
                solved_board[row][col] = value

            return solved_board

        return None

    def _search(self) -> bool:
        if not self.constraints:
            return True

        constraint = min(self.constraints, key=lambda key: len(self.constraints[key]))

        if len(self.constraints[constraint]) == 0:
            return False

        for option in list(self.constraints[constraint]):
            removed = self._select(option)
            self.solution.append(option)

            if self._search():
                return True

            self.solution.pop()
            self._deselect(option, removed)

        return False

    def _select(self, option: Option) -> List[Tuple[Constraint, Set[Option]]]:
        removed = []

        for constraint in self.options[option]:
            if constraint not in self.constraints:
                continue

            related_options = self.constraints.pop(constraint)
            removed.append((constraint, related_options))

            for related_option in related_options:
                if related_option == option:
                    continue

                for related_constraint in self.options[related_option]:
                    if related_constraint in self.constraints:
                        self.constraints[related_constraint].discard(related_option)

        return removed

    def _deselect(
        self,
        option: Option,
        removed: List[Tuple[Constraint, Set[Option]]],
    ) -> None:
        for constraint, related_options in reversed(removed):
            self.constraints[constraint] = related_options

            for related_option in related_options:
                if related_option == option:
                    continue

                for related_constraint in self.options[related_option]:
                    if related_constraint in self.constraints:
                        self.constraints[related_constraint].add(related_option)


def print_board(board: List[List[int]]) -> None:
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("------+-------+------")

        row_values = []

        for col in range(9):
            if col % 3 == 0 and col != 0:
                row_values.append("|")

            row_values.append(str(board[row][col]))

        print(" ".join(row_values))


def main() -> None:
    puzzle = """
    530070000
    600195000
    098000060
    800060003
    400803001
    700020006
    060000280
    000419005
    000080079
    """

    solver = SudokuSolver(puzzle)
    solution = solver.solve()

    if solution is None:
        print("No solution found.")
    else:
        print_board(solution)


if __name__ == "__main__":
    main()