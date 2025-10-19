class Heuristic:
    def __init__(self, mode="misplaced"):
        self.mode = mode

    def evaluate(self, node, goal_state=None):
        goal_state = goal_state or [[1,2,3],[4,5,6],[7,8,0]]

        if self.mode == "misplaced":
            return self._misplaced(node, goal_state)

        elif self.mode == "manhattan":
            return self._manhattan(node, goal_state)

        else:
            raise ValueError("Heuristic mode không hợp lệ")

    # Misplaced 
    def _misplaced(self, node, goal):
        misplaced = 0
        for i in range(3):
            for j in range(3):
                v = node.state[i][j]
                if v != 0 and v != goal[i][j]:
                    misplaced += 1
        return misplaced

    # Manhattan 
    def _manhattan(self, node, goal):
        goal_pos = {v: (i, j) for i, row in enumerate(goal) for j, v in enumerate(row)}
        total = 0
        for i in range(3):
            for j in range(3):
                v = node.state[i][j]
                if v == 0:
                    continue
                gi, gj = goal_pos[v]
                total += abs(i - gi) + abs(j - gj)
        return total // 2 
