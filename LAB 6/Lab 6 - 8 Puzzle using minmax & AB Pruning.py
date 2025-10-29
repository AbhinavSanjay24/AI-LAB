import copy
import time

# --- Goal State ---
GOAL = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# --- Utility Functions ---
def find_blank(puzzle):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == 0:
                return i, j

def is_goal(puzzle):
    return puzzle == GOAL

def manhattan_distance(puzzle):
    """Sum of Manhattan distances of tiles from their goal positions."""
    dist = 0
    for i in range(3):
        for j in range(3):
            val = puzzle[i][j]
            if val != 0:
                goal_i, goal_j = divmod(val - 1, 3)
                dist += abs(goal_i - i) + abs(goal_j - j)
    return dist

def generate_moves(puzzle):
    """Generate all possible moves by sliding the blank."""
    i, j = find_blank(puzzle)
    moves = []
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right
    for dx, dy in directions:
        x, y = i + dx, j + dy
        if 0 <= x < 3 and 0 <= y < 3:
            new_puzzle = copy.deepcopy(puzzle)
            new_puzzle[i][j], new_puzzle[x][y] = new_puzzle[x][y], new_puzzle[i][j]
            moves.append(new_puzzle)
    return moves

# --- Minimax with Alpha-Beta Pruning ---
def minimax(puzzle, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_goal(puzzle):
        # Closer to goal = better (negative Manhattan distance)
        return -manhattan_distance(puzzle)

    if maximizing_player:
        max_eval = float('-inf')
        for move in generate_moves(puzzle):
            eval = minimax(move, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for move in generate_moves(puzzle):
            eval = minimax(move, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval

def best_move(puzzle, depth=3):
    """Find the best move for MAX player."""
    best_val = float('-inf')
    best_state = None
    for move in generate_moves(puzzle):
        val = minimax(move, depth - 1, float('-inf'), float('inf'), False)
        if val > best_val:
            best_val = val
            best_state = move
    return best_state

def print_puzzle(puzzle):
    for row in puzzle:
        print(row)
    print()

# --- Main Solver Loop ---
def solve_8_puzzle(initial_state, depth_limit=3, max_steps=20):
    current = initial_state
    step = 0
    print("Initial State:")
    print_puzzle(current)

    while not is_goal(current) and step < max_steps:
        next_state = best_move(current, depth=depth_limit)
        if next_state is None or next_state == current:
            print("No better moves found. Stopping.")
            break

        step += 1
        print(f"Step {step}:")
        print_puzzle(next_state)
        current = next_state
        time.sleep(0.5)

    if is_goal(current):
        print("✅ Goal Reached!")
    else:
        print("⚠️ Stopped before reaching goal (depth or step limit).")

# --- Example Run ---
initial_state = [
    [1, 2, 3],
    [4, 6, 0],
    [7, 5, 8]
]

solve_8_puzzle(initial_state, depth_limit=3, max_steps=15)
