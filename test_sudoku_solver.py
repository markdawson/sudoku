from sudoku_solver import solve
import unittest


class TestSudokuSolver(unittest.TestCase):
    cases = [
        ("sudoku_puzzle1.txt", "sudoku_puzzle1_solution.txt"),
        ("sudoku_puzzle2.txt", "sudoku_puzzle2_solution.txt"),
        ("sudoku_puzzle3.txt", "sudoku_puzzle3_solution.txt"),
    ]

    def test_sudoku_solver_with_cs(self):
        """
        Tests with constraint satisfaction heuristics.
        """
        for case in self.cases:
            with self.subTest(case=case):
                puzzle, solution = case
                with open(puzzle) as f:
                    sample_input = f.read().strip()
                    actual_output = solve(sample_input, print_results=False)

                with open(solution) as f:
                    expected_output = f.read().strip()

                assert actual_output == expected_output

    def test_sudoku_solver_without_cs(self):
        """
        Tests without constraint satisfaction heuristics.
        Instead this just uses brute force search.
        """
        for case in self.cases:
            with self.subTest(case=case):
                puzzle, solution = case
                with open(puzzle) as f:
                    sample_input = f.read().strip()
                    actual_output = solve(sample_input, print_results=False, use_constraint_satisfaction_heuristics=False)

                with open(solution) as f:
                    expected_output = f.read().strip()

                assert actual_output == expected_output
