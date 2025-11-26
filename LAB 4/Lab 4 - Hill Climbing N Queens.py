import random

# Generate a random board (one queen per row)
def random_board(n):
    return [random.randint(0, n-1) for _ in range(n)]

# Count number of attacking queen pairs
def heuristic(board):
    h = 0
    n = len(board)
    for i in range(n):
        for j in range(i+1, n):
            if board[i] == board[j] or abs(board[i]-board[j]) == abs(i-j):
                h += 1
    return h

# Get best neighbor state
def best_neighbor(board):
    n = len(board)
    best = board[:]
    best_h = heuristic(board)

    for row in range(n):
        for col in range(n):
            if board[row] != col:
                new_board = board[:]
                new_board[row] = col
                h = heuristic(new_board)
                if h < best_h:
                    best = new_board
                    best_h = h
    return best, best_h

# Hill climbing with random restarts
def hill_climbing(n):
    current = random_board(n)
    current_h = heuristic(current)

    while current_h != 0:
        neighbor, neighbor_h = best_neighbor(current)

        if neighbor_h >= current_h:  # local maxima / plateau
            current = random_board(n)   # restart
            current_h = heuristic(current)
        else:
            current = neighbor
            current_h = neighbor_h

    return current

# Print board nicely
def print_board(board):
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[row] == col:
                line += " Q "
            else:
                line += " . "
        print(line)
    print()

# -------- MAIN ----------
if __name__ == "__main__":
    N = 8   # change this for any N
    solution = hill_climbing(N)

    print(f"Solved {N}-Queens using Hill Climbing:\n")
    print_board(solution)
