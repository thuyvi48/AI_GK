# sudoku_visualizer.py
import matplotlib.pyplot as plt
import numpy as np

def visualize_sudoku(puzzle, solution):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks(np.arange(0, 10, 1))
    ax.set_yticks(np.arange(0, 10, 1))

    # Ẩn số trên trục X, Y
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Lưới
    ax.grid(True, which='both', color='black', linewidth=1)
    ax.set_aspect('equal')
    ax.invert_yaxis()

    # Đường viền đậm cho block 3x3
    for i in range(0, 10, 3):
        ax.axhline(i, color='black', linewidth=2)
        ax.axvline(i, color='black', linewidth=2)

    # Hiển thị số trong từng ô
    for r in range(9):
        for c in range(9):
            num = solution[r][c]
            if puzzle[r][c] != 0:
                # Số ban đầu (đậm, màu xanh)
                ax.text(c + 0.5, r + 0.5, str(num),
                        va='center', ha='center',
                        fontsize=16, fontweight='bold', color='royalblue')
            else:
                # Số được solver điền
                ax.text(c + 0.5, r + 0.5, str(num),
                        va='center', ha='center',
                        fontsize=16, color='black')

    plt.title("Sudoku", fontsize=18, pad=15)
    plt.show()
