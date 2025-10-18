import copy
from graphviz import Digraph

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move

    def get_successors(self):
        successors = []
        x, y = next((i, j) for i in range(3) for j in range(3) if self.state[i][j] == 0)
        moves = [(-1,0),(1,0),(0,-1),(0,1)]

        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in self.state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]

                # Luật 1: Tổng = 9 → cho phép thêm hoán vị đặc biệt
                if (self.state[x][y] + self.state[nx][ny]) == 9:
                    successors.append(Node(new_state, self, move=f"swap9 ({self.state[x][y]}↔{self.state[nx][ny]})"))

                # Luật chuẩn (di chuyển ô trống)
                successors.append(Node(new_state, self, move=f"move {self.state[nx][ny]}"))

        # Luật 2: hoán vị hai góc chéo
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        diagonal_pairs = [((0, 0), (2, 2)), ((0, 2), (2, 0))]

        for (x1, y1), (x2, y2) in diagonal_pairs:
            new_state = [row[:] for row in self.state]
            new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
            successors.append(Node(new_state, self, move=f"swap_diag ({self.state[x1][y1]}↔{self.state[x2][y2]})"))

        return successors


    def draw(self, dot):
        dot.node(str(self.state), label=self.format_state(), shape='box')

        if self.parent:
            dot.edge(str(self.parent.state), str(self.state))

    def format_state(self):
        flat = [str(x) if x != 0 else "_" for r in self.state for x in r]
        return f"{flat[0]} {flat[1]} {flat[2]}\n{flat[3]} {flat[4]} {flat[5]}\n{flat[6]} {flat[7]} {flat[8]}"
