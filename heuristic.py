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

    def _misplaced(self, node, goal):
        flat = [x for r in node.state for x in r]
        goal_flat = [x for r in goal for x in r]
        return sum(1 for i in range(9) if flat[i] != 0 and flat[i] != goal_flat[i])

    def _manhattan(self, node, goal):
        goal_pos = {v:(i,j) for i,r in enumerate(goal) for j,v in enumerate(r)}
        total = 0
        for i in range(3):
            for j in range(3):
                v = node.state[i][j]
                if v != 0:
                    gi, gj = goal_pos[v]
                    total += abs(i-gi)+abs(j-gj)
        return total
