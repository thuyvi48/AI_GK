from puzzle_node import Node
from heuristic import Heuristic
from search import AStarSearch
from graphviz import Digraph
from collections import deque
import random, time

def bfs(start_node, goal_state):
    """Thuật toán BFS để so sánh"""
    visited = set()
    queue = deque([start_node])
    expanded = 0
    while queue:
        node = queue.popleft()
        expanded += 1
        if node.state == goal_state:
            return expanded
        visited.add(str(node.state))
        for child in node.get_successors():
            if str(child.state) not in visited:
                queue.append(child)
    return expanded

def main():
    # Một đối tượng Graphviz duy nhất
    dot = Digraph(comment="Final A* Search Tree")
    dot.attr(rankdir='TB', fontsize='10', size='10,8')

    start_states = {
        "Case1": [[1,3,4],[8,6,2],[7,0,5]]
    }

    goals = {
        "G1": [[1,2,3],[4,5,6],[7,8,0]],
        "G2": [[8,7,6],[5,4,3],[2,1,0]],
        "G3": [[1,2,0],[3,4,5],[6,7,8]],
        "G4": [[8,7,0],[6,5,4],[3,2,1]],
    }

    heuristics = ["misplaced", "manhattan"]

    for cname, start_state in start_states.items():
        start_node = Node(start_state)
        print(f"\n=== {cname} ===")
        for gname, goal_state in goals.items():
            print(f"\nGoal {gname}:")
            for h in heuristics:
                h_obj = Heuristic(h)
                astar = AStarSearch(h_obj, goal_state)
                print(f"→ A* ({h})")
                astar.search(start_node, record_tree=True, dot=dot)
            bfs_count = bfs(start_node, goal_state)
            print(f"BFS expanded: {bfs_count}")

    dot.render("Final_Search_Tree", format='png', view=False)

if __name__ == "__main__":
    main()
