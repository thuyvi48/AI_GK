# search.py
from heapq import heappush, heappop
from graphviz import Digraph
import itertools
import time

class AStarSearch:
    def __init__(self, heuristic_obj, goal_state=None):
        self.heuristic = heuristic_obj
        self.goal_state = goal_state or [[1,2,3],[4,5,6],[7,8,0]]

    def is_goal(self, node):
        return node.state == self.goal_state

    def reconstruct_path(self, node):
        path = []
        cur = node
        while cur is not None:
            path.append(cur)
            cur = cur.parent
        path.reverse()
        return path

    def search(self, start_node, record_tree=False, dot: Digraph = None):
        """
        Trả về dict:
          { "path_nodes": [...], "path_length": int,
            "expanded": int, "generated": int, "time": float }
        Nếu record_tree và dot được truyền, node/edge sẽ được thêm vào dot (KHÔNG render ở đây).
        """
        t0 = time.time()
        open_list = []
        counter = itertools.count()
        g_cost = {str(start_node.state): 0}
        f_cost = {str(start_node.state): self.heuristic.evaluate(start_node, self.goal_state)}
        heappush(open_list, (f_cost[str(start_node.state)], next(counter), start_node))
        visited = set()

        if record_tree and dot is not None:
            start_node.draw(dot)

        expanded = 0
        generated = 0

        while open_list:
            f, _, current = heappop(open_list)
            s_key = str(current.state)
            if s_key in visited:
                continue
            visited.add(s_key)
            expanded += 1

            if self.is_goal(current):
                path = self.reconstruct_path(current)
                t1 = time.time()

                if record_tree and dot is not None:
                    for node in path:
                        dot.node(node.id, node.label, fillcolor="lightcoral", style="filled", color="red", penwidth="2")
                    for i in range(len(path) - 1):
                        dot.edge(path[i].id, path[i+1].id, color="red", penwidth="2", label=path[i+1].action or "")

                return {
                    "path_nodes": path,
                    "path_length": len(path) - 1,
                    "expanded": expanded,
                    "generated": generated,
                    "time": t1 - t0
                }

            for child in current.get_successors():
                generated += 1
                c_key = str(child.state)
                g_new = g_cost[s_key] + 1
                if c_key not in g_cost or g_new < g_cost[c_key]:
                    g_cost[c_key] = g_new
                    f_cost[c_key] = g_new + self.heuristic.evaluate(child, self.goal_state)
                    heappush(open_list, (f_cost[c_key], next(counter), child))
                    if record_tree and dot is not None:
                        child.draw(dot)

        t1 = time.time()
        return {
            "path_nodes": [],
            "path_length": -1,
            "expanded": expanded,
            "generated": generated,
            "time": t1 - t0
        }
