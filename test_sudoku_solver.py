import unittest
from sudoku_solver import SudokuSolver


VALID_PUZZLE = """
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

SOLVED_BOARD = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


class TestSudokuSolver(unittest.TestCase):

    def test_solves_valid_puzzle(self):
        solver = SudokuSolver(VALID_PUZZLE)
        solution = solver.solve()
        self.assertEqual(solution, SOLVED_BOARD)

    def test_invalid_row_duplicate(self):
        puzzle = """
        550070000
        600195000
        098000060
        800060003
        400803001
        700020006
        060000280
        000419005
        000080079
        """

        with self.assertRaises(ValueError):
            SudokuSolver(puzzle)

    def test_invalid_board_length(self):
        with self.assertRaises(ValueError):
            SudokuSolver("123")

    def test_already_solved_board(self):
        puzzle = """
        534678912
        672195348
        198342567
        859761423
        426853791
        713924856
        961537284
        287419635
        345286179
        """

        solver = SudokuSolver(puzzle)
        solution = solver.solve()
        self.assertEqual(solution, SOLVED_BOARD)


if __name__ == "__main__":
    unittest.main()
