# sudoku_csp.py
from itertools import product

class SudokuCSP:
    def __init__(self):
        self.N = 9
        self.variables = [(r, c, v) for r in range(1, 10)
                          for c in range(1, 10)
                          for v in range(1, 10)]

    def varnum(self, r, c, v):
        """Mã hóa (r, c, v) thành biến duy nhất (1..729)."""
        return 81 * (r - 1) + 9 * (c - 1) + v

    def generate_clauses(self, puzzle):
        """Sinh tất cả các mệnh đề CNF cho Sudoku."""
        clauses = []

        # Mỗi ô phải có đúng 1 giá trị
        for r, c in product(range(1, 10), repeat=2):
            clauses.append([self.varnum(r, c, v) for v in range(1, 10)])  # at least one
            for v1 in range(1, 10):
                for v2 in range(v1 + 1, 10):
                    clauses.append([-self.varnum(r, c, v1), -self.varnum(r, c, v2)])  # at most one

        # Mỗi hàng chứa mỗi số đúng 1 lần
        for r, v in product(range(1, 10), range(1, 10)):
            clauses.append([self.varnum(r, c, v) for c in range(1, 10)])  # at least one
            for c1 in range(1, 10):
                for c2 in range(c1 + 1, 10):
                    clauses.append([-self.varnum(r, c1, v), -self.varnum(r, c2, v)])  # at most one

        # Mỗi cột chứa mỗi số đúng 1 lần
        for c, v in product(range(1, 10), range(1, 10)):
            clauses.append([self.varnum(r, c, v) for r in range(1, 10)])  # at least one
            for r1 in range(1, 10):
                for r2 in range(r1 + 1, 10):
                    clauses.append([-self.varnum(r1, c, v), -self.varnum(r2, c, v)])  # at most one

        # Mỗi block 3x3 chứa mỗi số đúng 1 lần
        for br in range(0, 3):
            for bc in range(0, 3):
                for v in range(1, 10):
                    cells = [(r, c) for r in range(1 + br * 3, 4 + br * 3)
                             for c in range(1 + bc * 3, 4 + bc * 3)]
                    clauses.append([self.varnum(r, c, v) for (r, c) in cells])  # at least one
                    for i in range(len(cells)):
                        for j in range(i + 1, len(cells)):
                            r1, c1 = cells[i]
                            r2, c2 = cells[j]
                            clauses.append([-self.varnum(r1, c1, v), -self.varnum(r2, c2, v)])  # at most one

        # Các gợi ý ban đầu (cố định giá trị)
        for r in range(1, 10):
            for c in range(1, 10):
                if puzzle[r - 1][c - 1] != 0:
                    v = puzzle[r - 1][c - 1]
                    clauses.append([self.varnum(r, c, v)])

        return clauses
