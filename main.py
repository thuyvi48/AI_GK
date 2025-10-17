from node import Node
from heuristic import Heuristic
from graphviz import Digraph
from collections import deque
from search_astar import AStar
from search_bfs import BFS

import time
import random
import copy

# ==============================
# BFS cơ bản (so sánh)
# ==============================
def bfs(start_node, goal_state, max_nodes=None):
    visited = set()
    queue = deque([start_node])
    expanded = 0
    start_time = time.time()

    while queue:
        node = queue.popleft()
        expanded += 1

        if max_nodes is not None and expanded >= max_nodes:
            break

        if node.state == goal_state:
            elapsed = time.time() - start_time
            return {"expanded": expanded, "time": elapsed}

        visited.add(str(node.state))
        for child in node.get_successors():
            if str(child.state) not in visited:
                queue.append(child)

    elapsed = time.time() - start_time
    return {"expanded": expanded, "time": elapsed}


# ==============================
# In ma trận trạng thái
# ==============================
def print_state(state):
    for row in state:
        print(" ".join(str(x) if x != 0 else "_" for x in row))


# ==============================
# Vẽ đường đi đỏ từ goal về start
# ==============================
def highlight_path(goal_node, dot):
    current = goal_node
    while current.parent:
        parent_id = str(current.parent.state)
        child_id = str(current.state)
        dot.edge(parent_id, child_id, color="red", penwidth="3")
        current = current.parent


# ==============================
# Kiểm tra trạng thái có thể giải được
# ==============================
def is_solvable(state):
    flat = [x for r in state for x in r if x != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0


# ==============================
# Sinh trạng thái ngẫu nhiên có thể giải được
# ==============================
def random_state(goal):
    """Sinh trạng thái ngẫu nhiên hợp lệ (có thể giải được)."""
    nums = [x for row in goal for x in row]
    while True:
        random.shuffle(nums)
        new_state = [nums[i:i+3] for i in range(0, 9, 3)]
        if is_solvable(new_state):
            return new_state


# ==============================
# Thí nghiệm ngẫu nhiên và đo time / space complexity
# ==============================
def experiment(goal_state, trials=5):
    heuristics = ["misplaced", "manhattan"]
    results = []

    for i in range(trials):
        start = random_state(goal_state)
        print(f"\n🧩 Trial {i+1} | Start:")
        print_state(start)

        # Chạy A* cho từng heuristic
        for h in heuristics:
            h_obj = Heuristic(h)
            astar = AStar(h_obj, goal_state)
            res = astar.search(Node(start))
            results.append({
                "method": f"A* ({h})",
                "time": res["time"],
                "expanded": res["expanded"]
            })

        # Chạy BFS (có giới hạn để tránh treo)
        bfs_search = BFS(goal_state)
        res = bfs_search.search(Node(start), record_tree=False)
        results.append({
            "method": "BFS",
            "time": res["time"],
            "expanded": res["expanded"]
        })

    # Tổng hợp kết quả trung bình
    summary = {}
    for r in results:
        m = r["method"]
        if m not in summary:
            summary[m] = {"time": 0, "expanded": 0, "count": 0}
        summary[m]["time"] += r["time"]
        summary[m]["expanded"] += r["expanded"]
        summary[m]["count"] += 1

    print("\n📊 Average Results:")
    for m, v in summary.items():
        avg_time = v["time"] / v["count"]
        avg_expanded = v["expanded"] / v["count"]
        print(f"{m:<15} | Avg Time: {avg_time:.4f}s | Avg Expanded: {avg_expanded:.1f}")


# ==============================
# Chương trình chính
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
        start_node = Node(start_state)
        print(f"\n=== {cname} ===")
        print("\nInitial state:")
        print_state(start_state)

        for gname, goal_state in goals.items():
            print(f"\nGoal {gname}:")
            print_state(goal_state)
            print()

            # A* Search
            # ==============================
            for h in heuristics:
                h_obj = Heuristic(h)
                astar = AStar(h_obj, goal_state)
                print(f"→ A* ({h})")
                start_time = time.time()

                # ⚙️ Tìm đến goal, KHÔNG dừng sớm
                result = astar.search(Node(start_state), record_tree=True, dot=dot, max_nodes=None)
                goal_node = result.get("goal")
                elapsed = result["time"]

                if goal_node:
                    print(f"✅ Goal found in {elapsed:.3f}s | Expanded: {result['expanded']}")
                    # 🧩 Giới hạn số node được vẽ
                    highlight_limit = 300
                    current = goal_node
                    drawn = 0
                    while current.parent and drawn < highlight_limit:
                        parent_id = str(current.parent.state)
                        child_id = str(current.state)
                        dot.edge(parent_id, child_id, color="red", penwidth="3")
                        current = current.parent
                        drawn += 1
                    if drawn >= highlight_limit:
                        print(f"⚠️ Only drew first {highlight_limit} steps of path to goal.")
                else:
                    print(f"❌ Goal not found. Expanded: {result['expanded']}")


            # BFS (so sánh, có giới hạn)
            bfs_result = bfs(Node(start_state), goal_state, max_nodes=2000)
            print(f"→ BFS (for comparison)")
            print(f"BFS expanded: {bfs_result['expanded']} | Time: {bfs_result['time']:.3f}s")

    dot.render("Final_Search_Tree", format='png', view=False)
    print("\n✅ Search tree has been saved as 'Final_Search_Tree.png'")

    print("\n=== RANDOMIZED EXPERIMENTS ===")
    experiment(goals["G1"], trials=3)

if __name__ == "__main__":
    main()
