import heapq

GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)   # Goal state (0 = blank)

# Manhattan Distance Heuristic
def manhattan(state):
    dist = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        goal_idx = val - 1
        r, c = divmod(i, 3)
        gr, gc = divmod(goal_idx, 3)
        dist += abs(r - gr) + abs(c - gc)
    return dist

# Generate neighbors
def neighbors(state):
    res = []
    i = state.index(0)
    r, c = divmod(i, 3)
    moves = []
    if r > 0: moves.append((-3, "Up"))
    if r < 2: moves.append((3, "Down"))
    if c > 0: moves.append((-1, "Left"))
    if c < 2: moves.append((1, "Right"))
    for d, move in moves:
        new = list(state)
        new[i], new[i+d] = new[i+d], new[i]
        res.append((tuple(new), move))
    return res

# A* Search Algorithm
def astar(start):
    open_list = []
    heapq.heappush(open_list, (manhattan(start), 0, start, []))
    visited = set()
   
    while open_list:
        f, g, state, path = heapq.heappop(open_list)
        if state in visited:
            continue
        visited.add(state)

        if state == GOAL:
            return path

        for neigh, move in neighbors(state):
            if neigh not in visited:
                heapq.heappush(open_list,
                               (g+1+manhattan(neigh), g+1, neigh, path+[move]))
    return None

# Pretty print the board
def print_state(state):
    for i in range(0, 9, 3):
        row = state[i:i+3]
        print(" ".join(str(x) if x != 0 else " " for x in row))
    print()

# -------- MAIN --------
if __name__ == "__main__":
    # Example input
    initial = (1, 2, 3,
               4, 0, 6,
               7, 5, 8)   # Change this as required

    print("Initial State:")
    print_state(initial)

    solution = astar(initial)

    if solution:
        print("Solution found in", len(solution), "moves.")
        print("Moves:", " -> ".join(solution))
    else:
        print("No solution exists.")
