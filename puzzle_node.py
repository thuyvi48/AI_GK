# puzzle_node.py
from copy import deepcopy
from graphviz import Digraph

NODE_COUNTER = 0

class Node:
    def __init__(self, state, action=None, parent=None):
        """
        state: list of lists 3x3, e.g. [[1,2,3],[4,5,6],[7,8,0]]
        """
        global NODE_COUNTER
        NODE_COUNTER += 1
        self.state = [row[:] for row in state]
        self.action = action
        self.parent = parent
        self.id = f"node_{NODE_COUNTER}"
        self.label = self._make_label()

    @staticmethod
    def from_flat_tuple(tup9):
        """Tạo Node từ tuple 9 phần tử (dùng cho experiment)"""
        lst = list(tup9)
        return Node([lst[0:3], lst[3:6], lst[6:9]])

    def _make_label(self):
        return "\n".join(
            "".join(str(x) if x != 0 else "_" for x in row)
            for row in self.state
        )

    def __str__(self):
        return self.label

    # ===== Successors =====
    def get_blank_pos(self):
        for i, row in enumerate(self.state):
            for j, v in enumerate(row):
                if v == 0:
                    return i, j
        raise ValueError("Không tìm thấy ô trống")

    def get_successors(self):
        """
        Sinh successors theo đề:
         - swap hai ô kề nhau nếu cả hai khác 0 và sum == 9
         - swap hai góc chéo (0,0)<->(2,2) và (0,2)<->(2,0) nếu cả hai khác 0
        Trả về danh sách Node (mỗi node có parent = self và action mô tả)
        """
        successors = []
        directions = [(0,1), (1,0), (-1,0), (0,-1)]

        # Luật 1: swap ô kề nhau có tổng = 9 (cả hai khác 0)
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
        """Add this node and edge from parent (if exists) into dot"""
        dot.node(self.id, self.label)
        if self.parent is not None:
            dot.edge(self.parent.id, self.id, label=self.action)
