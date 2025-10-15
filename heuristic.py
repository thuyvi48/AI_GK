# heuristic.py
class Heuristic:
    def __init__(self, mode="misplaced"):
        self.mode = mode

    def evaluate(self, node, goal_state=None):
        """Tính heuristic dựa theo mode, có thể truyền goal_state tùy chọn"""
        if goal_state is None:
            goal_state = [[1,2,3],[4,5,6],[7,8,0]]  # goal mặc định

        if self.mode == "misplaced":
            return self._misplaced_tiles(node, goal_state)
        elif self.mode == "manhattan":
            return self._manhattan_distance(node, goal_state)
        else:
            raise ValueError("Heuristic mode không hợp lệ")

    def _misplaced_tiles(self, node, goal_state):
        flat = [x for row in node.state for x in row]
        goal_flat = [x for row in goal_state for x in row]
        return sum(1 for i in range(9) if flat[i] != 0 and flat[i] != goal_flat[i])

    def _manhattan_distance(self, node, goal_state):
        goal_pos = {val: (i, j)
                    for i, row in enumerate(goal_state)
                    for j, val in enumerate(row)}
        total = 0
        for i in range(3):
            for j in range(3):
                val = node.state[i][j]
                if val != 0:
                    gi, gj = goal_pos[val]
                    total += abs(i - gi) + abs(j - gj)
        return total
