from collections import deque
from graphviz import Digraph
import time

class BFS:
    def __init__(self, goal_state):
        self.goal_state = goal_state

    def search(self, start_node, record_tree=False, dot=None):
        start_time = time.time()
        queue = deque([start_node])
        visited = set()
        expanded, generated = 0, 0

        if record_tree and dot:
            start_node.draw(dot)

        while queue:
            current = queue.popleft()
            expanded += 1
            if current.state == self.goal_state:
                return {
                    "method": "BFS",
                    "expanded": expanded,
                    "generated": generated,
                    "time": time.time() - start_time,
                    "goal": current
                }

            s_key = str(current.state)
            visited.add(s_key)
            for child in current.get_successors():
                c_key = str(child.state)
                if c_key not in visited:
                    queue.append(child)
                    generated += 1
                    if record_tree and dot:
                        child.draw(dot)

        return {"method": "BFS", "expanded": expanded, "generated": generated, "time": time.time() - start_time}
