# sudoku_solver.py
from pysat.solvers import Glucose3
from sudoku_csp import SudokuCSP

class SudokuSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.csp = SudokuCSP()
        self.solver = Glucose3()

    def solve(self):
        clauses = self.csp.generate_clauses(self.puzzle)
        for clause in clauses:
            self.solver.add_clause(clause)

        if not self.solver.solve():
            print("Không tìm thấy nghiệm hợp lệ.")
            return None

        model = self.solver.get_model()
        grid = [[0 for _ in range(9)] for _ in range(9)]

        for val in model:
            if val > 0:
                r = (val - 1) // 81 + 1
                c = ((val - 1) % 81) // 9 + 1
                v = ((val - 1) % 9) + 1
                if 1 <= r <= 9 and 1 <= c <= 9:
                    grid[r - 1][c - 1] = v

        self.solver.delete()  # giải phóng tài nguyên
        return grid
