from copy import deepcopy
from graphviz import Digraph

NODE_COUNTER = 0

class Node:
    def __init__(self, state, action=None, parent=None):
        global NODE_COUNTER
        NODE_COUNTER += 1
        self.state = [row[:] for row in state]
        self.action = action
        self.parent = parent
        self.id = f"node_{NODE_COUNTER}"
        self.label = self._make_label()

    def _make_label(self):
        return "\n".join(
            "".join(str(x) if x != 0 else "_" for x in row)
            for row in self.state
        )

    def __str__(self):
        return self.label

    def get_successors(self):
        successors = []
        directions = [(0,1), (1,0), (-1,0), (0,-1)]

        # Luật 1: swap ô có tổng = 9
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    continue
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 3 and 0 <= nj < 3:
                        if self.state[ni][nj] != 0 and self.state[i][j] + self.state[ni][nj] == 9:
                            new_state = deepcopy(self.state)
                            new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                            successors.append(Node(new_state, parent=self, action=f"swap({self.state[i][j]},{self.state[ni][nj]})"))

        # Luật 2: swap góc chéo
        corner_pairs = [((0,0),(2,2)), ((0,2),(2,0))]
        for (i1,j1),(i2,j2) in corner_pairs:
            if self.state[i1][j1] != 0 and self.state[i2][j2] != 0:
                new_state = deepcopy(self.state)
                new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
                successors.append(Node(new_state, parent=self, action=f"corner({self.state[i1][j1]},{self.state[i2][j2]})"))
        return successors

    def draw(self, dot: Digraph):
        dot.node(self.id, self.label)
        if self.parent:
            dot.edge(self.parent.id, self.id, label=self.action)
