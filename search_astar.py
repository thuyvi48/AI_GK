from heapq import heappush, heappop
import itertools
import time

class AStar:
    def __init__(self, heuristic, goal_state):
        self.heuristic = heuristic
        self.goal_state = goal_state

    def search(self, start_node, record_tree=False, dot=None, max_nodes=None):
        start_time = time.time()
        open_list = []
        counter = itertools.count()

        g_cost = {str(start_node.state): 0}
        f_cost = {str(start_node.state): self.heuristic.evaluate(start_node, self.goal_state)}
        heappush(open_list, (f_cost[str(start_node.state)], next(counter), start_node))
        visited = set()
        expanded, generated = 0, 0

        if record_tree and dot:
            start_node.draw(dot)

        while open_list:
            f, _, current = heappop(open_list)
            s_key = str(current.state)
            if s_key in visited:
                continue
            visited.add(s_key)
            expanded += 1

            # Dừng khi đạt giới hạn n nút
            if max_nodes is not None and expanded >= max_nodes:
                return {
                    "method": "A*",
                    "expanded": expanded,
                    "generated": generated,
                    "time": time.time() - start_time,
                    "goal": None
                }

            if current.state == self.goal_state:
                return {
                    "method": "A*",
                    "expanded": expanded,
                    "generated": generated,
                    "time": time.time() - start_time,
                    "goal": current
                }

            for child in current.get_successors():
                generated += 1
                c_key = str(child.state)
                g_new = g_cost[s_key] + 1
                if c_key not in g_cost or g_new < g_cost[c_key]:
                    g_cost[c_key] = g_new
                    f_cost[c_key] = g_new + self.heuristic.evaluate(child, self.goal_state)
                    heappush(open_list, (f_cost[c_key], next(counter), child))
                    if record_tree and dot:
                        child.draw(dot)

        return {"method": "A*", "expanded": expanded, "generated": generated, "time": time.time() - start_time}

