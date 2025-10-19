from puzzle_node import Node
from heuristic import Heuristic
from search import AStarSearch
from graphviz import Digraph
from collections import deque
import time

# BFS
def bfs(start_node, goal_state):
    visited = set()
    queue = deque([(start_node, 0)])  
    expanded, generated = 0, 0
    start_time = time.time()

    while queue:
        node, cost = queue.popleft()
        expanded += 1
        if node.state == goal_state:
            end_time = time.time()
            return {
                "expanded": expanded,
                "generated": generated,
                "cost": cost,
                "time": end_time - start_time,
                "path_len": cost
            }

        visited.add(str(node.state))
        for child in node.get_successors():
            generated += 1
            if str(child.state) not in visited:
                queue.append((child, cost + 1))

    end_time = time.time()
    return {"expanded": expanded, "generated": generated, "cost": None, "time": end_time - start_time}


def main():
    dot = Digraph(comment="A* Search Tree (All Heuristics)")
    dot.attr(rankdir='TB', fontsize='10', size='10,8')

    start_states = {
        "Case 1": [[1, 3, 4],
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
               [3, 2, 1]]
    }

    heuristics = ["misplaced", "manhattan"]

    summary = {"BFS": [], "misplaced": [], "manhattan": []}

    for cname, start_state in start_states.items():
        print(f"\n==== {cname} ====")
        start_node = Node(start_state)

        for gname, goal_state in goals.items():
            print(f"\n--- Goal {gname} ---")
            print("Start state:")
            for r in start_state: print(r)
            print("Goal state:")
            for r in goal_state: print(r)

            # --- BFS ---
            bfs_result = bfs(start_node, goal_state)
            print(f"\n[BFS] Expanded: {bfs_result['expanded']} | "
                  f"Generated: {bfs_result['generated']} | "
                  f"Cost: {bfs_result['cost']} | "
                  f"Time: {bfs_result['time']:.4f}s")
            summary["BFS"].append(bfs_result)

            # --- A* với 2 heuristic ---
            for h in heuristics:
                h_obj = Heuristic(h)
                astar = AStarSearch(h_obj, goal_state)
                print(f"\n[A* - {h}]")
                start_time = time.time()
                result = astar.search(start_node, record_tree=True, dot=dot)
                end_time = time.time()
                duration = end_time - start_time

                print(f"Expanded: {result['expanded']} | Generated: {result['generated']} | "
                      f"Time: {duration:.4f}s")

                if "path" in result and result["path"]:
                    cost = len(result["path"]) - 1
                    print(f"Path cost: {cost}")
                    print("Path (from start → goal):")
                    for step, n in enumerate(result["path"]):
                        print(f"Step {step}:")
                        for row in n.state:
                            print(row)
                        print("-----------")
                else:
                    cost = None
                    print("No path found.")

                summary[h].append({
                    "expanded": result["expanded"],
                    "generated": result["generated"],
                    "time": duration,
                    "cost": cost
                })

    dot.render("Final_Search_Tree", format='pdf', view=False)

    # --- In bảng trung bình ---
    print("\n---BẢNG SO SÁNH TRUNG BÌNH---")
    for algo in ["BFS", "misplaced", "manhattan"]:
        if not summary[algo]:
            continue
        avg_exp = sum(r["expanded"] for r in summary[algo]) / len(summary[algo])
        avg_time = sum(r["time"] for r in summary[algo]) / len(summary[algo])
        avg_cost = sum(r["cost"] for r in summary[algo] if r["cost"] is not None) / len(summary[algo])
        print(f"{algo.upper():10s} | Avg Expanded: {avg_exp:8.2f} | Avg Time: {avg_time:8.4f}s | Avg Cost: {avg_cost:5.2f}")


if __name__ == "__main__":
    main()
