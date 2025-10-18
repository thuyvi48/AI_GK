from node import Node
from heuristic import Heuristic
from graphviz import Digraph
from search_astar import AStar
from search_bfs import BFS
from collections import deque
import time
import random

# ==============================
def print_state(state):
    for row in state:
        print(" ".join(str(x) if x != 0 else "_" for x in row))

def highlight_path(goal_node, dot, limit=300):
    current = goal_node
    drawn = 0
    while current.parent and drawn < limit:
        parent_id = str(current.parent.state)
        child_id = str(current.state)
        dot.edge(parent_id, child_id, color="red", penwidth="3")
        current = current.parent
        drawn += 1
    if drawn >= limit:
        print(f"Only drew first {limit} steps of path to goal.")

def is_solvable(state):
    flat = [x for r in state for x in r if x != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0

def random_state(goal):
    nums = [x for row in goal for x in row]
    while True:
        random.shuffle(nums)
        new_state = [nums[i:i+3] for i in range(0, 9, 3)]
        if is_solvable(new_state):
            return new_state

def bfs(start_node, goal_state, max_nodes=200):
    visited = set()
    queue = deque([start_node])
    expanded = 0
    start_time = time.time()

    while queue:
        node = queue.popleft()
        expanded += 1
        if expanded >= max_nodes:
            break
        if node.state == goal_state:
            return {"expanded": expanded, "time": time.time() - start_time}
        visited.add(str(node.state))
        for child in node.get_successors():
            if str(child.state) not in visited:
                queue.append(child)
    return {"expanded": expanded, "time": time.time() - start_time}

def add_nodes_limited_iterative(root_node, dot, max_nodes=2000):
    """
    Thêm node và edge vào dot, giới hạn số node bằng BFS (không đệ quy)
    """
    drawn = 0
    queue = deque([root_node])

    while queue and drawn < max_nodes:
        node = queue.popleft()
        for child in node.get_successors():
            parent_id = str(node.state)
            child_id = str(child.state)
            dot.edge(parent_id, child_id)
            drawn += 1
            if drawn >= max_nodes:
                break
            queue.append(child)


# ==============================
def main():
    dot = Digraph(comment="Final A* Search Tree")
    dot.attr(rankdir='TB', fontsize='10', size='10,8')

    start_states = {
        "Case1": [[1, 3, 4],
                  [8, 6, 2],
                  [7, 0, 5]]
    }

    goals = {
        "G1": [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 0]],
        "G2": [[8, 7, 6],
               [5, 4, 3],
               [2, 1, 0]],
        "G3": [[1, 2, 0],
               [3, 4, 5],
               [6, 7, 8]],
        "G4": [[8, 7, 0],
               [6, 5, 4],
               [3, 2, 1]],
    }

    heuristics = ["misplaced", "manhattan"]

    for cname, start_state in start_states.items():
        print(f"\n=== {cname} ===\nInitial state:")
        print_state(start_state)

        for gname, goal_state in goals.items():
            print(f"\nGoal {gname}:")
            print_state(goal_state)
            print()

            for h in heuristics:
                h_obj = Heuristic(h)
                astar = AStar(h_obj, goal_state)
                print(f"→ A* ({h})")
                # record_tree=True để tạo cây, nhưng Graphviz sẽ không treo vì highlight limit
                # A* search
                result = astar.search(Node(start_state), record_tree=False)  # KHÔNG record toàn tree trực tiếp
                goal_node = result.get("goal")
                elapsed = result["time"]

                if goal_node:
                    print(f"Goal found in {elapsed:.3f}s | Expanded: {result['expanded']}")
                    # vẽ toàn bộ cây nhưng giới hạn số node
                    add_nodes_limited_iterative(goal_node, dot, max_nodes=10)
                    # highlight đường đi đỏ
                    highlight_path(goal_node, dot, limit=300)
                else:
                    print(f"Goal not found. Expanded: {result['expanded']}")

            # BFS so sánh
            bfs_res = bfs(Node(start_state), goal_state, max_nodes=200)
            print(f"→ BFS (limited) | Expanded: {bfs_res['expanded']} | Time: {bfs_res['time']:.3f}s")

    dot.render("Final_Search_Tree", format='png', view=False)
    print("\nFinal search tree saved as 'Final_Search_Tree.png'")

if __name__ == "__main__":
    main()
