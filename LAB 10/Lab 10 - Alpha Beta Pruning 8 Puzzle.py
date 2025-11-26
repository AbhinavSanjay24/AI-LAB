import math

GOAL = (1,2,3,4,5,6,7,8,0)

# Manhattan distance heuristic
def manhattan(state):
    dist = 0
    for i,val in enumerate(state):
        if val == 0: continue
        goal = GOAL.index(val)
        r1,c1 = divmod(i,3)
        r2,c2 = divmod(goal,3)
        dist += abs(r1-r2) + abs(c1-c2)
    return dist

# Generate legal moves
def get_neighbors(state):
    moves = []
    zero = state.index(0)
    r,c = divmod(zero,3)
    dirs = []
    if r>0: dirs.append(-3)
    if r<2: dirs.append(3)
    if c>0: dirs.append(-1)
    if c<2: dirs.append(1)
    for d in dirs:
        new = list(state)
        new[zero], new[zero+d] = new[zero+d], new[zero]
        moves.append(tuple(new))
    return moves

# Pretty print puzzle board
def print_puzzle(state):
    for i in range(0,9,3):
        row = state[i:i+3]
        print(" ".join(str(x) if x!=0 else " " for x in row))
    print()

# Alpha Beta Minimax Search
def alphabeta(state, depth, alpha, beta, maximizing):
    print("State:")
    print_puzzle(state)
    print(f"Depth={depth}, α={alpha}, β={beta}")

    if depth == 0 or state == GOAL:
        score = -manhattan(state)
        print(f"Evaluation score: {score}\n")
        return score

    if maximizing:
        value = -math.inf
        for child in get_neighbors(state):
            value = max(value, alphabeta(child, depth-1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                print("Pruned (MAX branch)\n")
                break
        return value
    else:
        value = math.inf
        for child in get_neighbors(state):
            value = min(value, alphabeta(child, depth-1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                print("Pruned (MIN branch)\n")
                break
        return value


# -------- MAIN TEST ---------

initial = (1,2,3,
           4,5,6,
           7,0,8)

print("\nStarting Alpha Beta Search on 8-Puzzle...\n")

best_value = alphabeta(initial, depth=3,
                       alpha=-math.inf,
                       beta=math.inf,
                       maximizing=True)

print("Final best evaluation:", best_value)
