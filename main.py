# main.py
from puzzle_node import Node
from heuristic import Heuristic
from search import AStarSearch
from graphviz import Digraph
from collections import deque
import random

# BFS để so sánh (sử dụng các luật successor giống Node.get_successors)
def bfs(start_node, goal_state):
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

# Kiểm tra solvable (8-puzzle parity) - dùng cho experiment
def is_solvable_flat(tup9):
    arr = [x for x in tup9 if x != 0]
    inversions = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions % 2 == 0

def random_solvable_flat():
    while True:
        tup = tuple(random.sample(range(9), 9))
        if is_solvable_flat(tup):
            return tup

def randomized_experiment(num_trials=5):
    print(f"\n=== Randomized experiment: {num_trials} trials ===")
    goals = [
        [[1,2,3],[4,5,6],[7,8,0]]
    ]
    heuristics = ["misplaced", "manhattan"]
    results = {}
    for h in heuristics:
        results[h] = {"expanded":0, "path":0, "time":0, "fail":0}
    for t in range(num_trials):
        flat = random_solvable_flat()
        start_node = Node.from_flat_tuple(flat)
        for h in heuristics:
            hobj = Heuristic(h)
            solver = AStarSearch(hobj, goals[0])
            res = solver.search(start_node, record_tree=False, dot=None)
            if res["path_length"] >= 0:
                results[h]["expanded"] += res["expanded"]
                results[h]["path"] += res["path_length"]
                results[h]["time"] += res["time"]
            else:
                results[h]["fail"] += 1
    # print averages
    for h in heuristics:
        denom = num_trials - results[h]["fail"]
        if denom > 0:
            print(f"\nHeuristic {h}: avg expanded={results[h]['expanded']/denom:.1f}, avg path={results[h]['path']/denom:.1f}, avg time={results[h]['time']/denom:.4f}s, fails={results[h]['fail']}")
        else:
            print(f"\nHeuristic {h}: all trials failed ({results[h]['fail']})")

def main():
    # final single Digraph
    dot = Digraph(comment="Final A* Search Tree")
    dot.attr(rankdir='TB', fontsize='10', size='10,8')
    dot.attr('node', shape='box', fontsize='9')

    # one or many start cases (you can expand)
    cases = {
        "Case1": [[1,3,4],[8,6,2],[7,0,5]]
    }

    goals = {
        "G1": [[1,2,3],[4,5,6],[7,8,0]],
        "G2": [[8,7,6],[5,4,3],[2,1,0]],
        "G3": [[1,2,0],[3,4,5],[6,7,8]],
        "G4": [[8,7,0],[6,5,4],[3,2,1]],
    }

    heuristics = ["misplaced", "manhattan"]

    for case_name, start_state in cases.items():
        print(f"\n=== {case_name} ===")
        for gname, goal_state in goals.items():
            print(f"\nGoal {gname}:")
            for h in heuristics:
                # create fresh start_node each search to avoid reusing node objects and duplicate parents
                start_node = Node(start_state)
                h_obj = Heuristic(h)
                astar = AStarSearch(h_obj, goal_state)
                print(f"-> Running A* ({h}) ...", end=" ")
                res = astar.search(start_node, record_tree=True, dot=dot)
                if res["path_length"] >= 0:
                    print(f"done. path_len={res['path_length']}, expanded={res['expanded']}, time={res['time']:.4f}s")
                else:
                    print(f"no solution. expanded={res['expanded']}")
            # BFS compare (single start_node)
            s_for_bfs = Node(start_state)
            bfs_exp = bfs(s_for_bfs, goal_state)
            print(f"BFS expanded: {bfs_exp}")

    # render final single image
    dot.render("Final_Search_Tree", format='png', view=False, quiet=True)
    print("\nFinal image saved: Final_Search_Tree.png")

    # run randomized experiment (prints averages)
    randomized_experiment(num_trials=5)

if __name__ == "__main__":
    main()
