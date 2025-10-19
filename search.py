from heapq import heappush, heappop
from graphviz import Digraph
import itertools

class AStarSearch:
    def __init__(self, heuristic, goal_state):
        self.heuristic = heuristic
        self.goal_state = goal_state

    def is_goal(self, node):
        return node.state == self.goal_state

    def _reconstruct_path(self, node):
        path = []
        cur = node
        while cur is not None:
            path.append(cur)
            cur = cur.parent
        return list(reversed(path))

    def search(self, start_node, record_tree=False, dot=None):
        """Tìm kiếm A* và ghi vào Graphviz nếu có"""
        open_list = []
        counter = itertools.count()  # Bộ đếm duy nhất để tránh lỗi so sánh Node
        g_cost = {str(start_node.state): 0}
        f_cost = {str(start_node.state): self.heuristic.evaluate(start_node, self.goal_state)}

        heappush(open_list, (f_cost[str(start_node.state)], next(counter), start_node))
        visited = set()

        if record_tree and dot is not None:
            start_node.draw(dot)

        expanded, generated = 0, 0

        while open_list:
            f, _, current = heappop(open_list)
            s_key = str(current.state)
            if s_key in visited:
                continue
            visited.add(s_key)
            expanded += 1

            if self.is_goal(current):
                print("Goal reached!")
                
                # --- Gọi hàm tái tạo đường đi ---
                path = self._reconstruct_path(current)
                print("Path length (steps):", len(path) - 1)
                print("==== PATH FROM START TO GOAL ====")
                for n in path:
                    print(n)
                    print("-------------------------")
                
                return {"expanded": expanded, "generated": generated}


            for child in current.get_successors():
                generated += 1
                c_key = str(child.state)
                g_new = g_cost[s_key] + 1
                if c_key not in g_cost or g_new < g_cost[c_key]:
                    g_cost[c_key] = g_new
                    f_cost[c_key] = g_new + self.heuristic.evaluate(child, self.goal_state)
                    heappush(open_list, (f_cost[c_key], next(counter), child))  # thêm counter
                    if record_tree and dot is not None:
                        child.draw(dot)
        return {"expanded": expanded, "generated": generated}
