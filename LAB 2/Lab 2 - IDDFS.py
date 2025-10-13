import time
from collections import deque
import heapq


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def manhattan_distance(state):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            goal_x, goal_y = (state[i] - 1) // 3, (state[i] - 1) % 3
            current_x, current_y = i // 3, i % 3
            distance += abs(goal_x - current_x) + abs(goal_y - current_y)
    return distance

def is_goal(state):
    return state == GOAL_STATE


def get_neighbors(state):
    neighbors = []
    zero_pos = state.index(0)
    x, y = zero_pos // 3, zero_pos % 3
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_pos = new_x * 3 + new_y
            new_state = list(state)
            new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
            neighbors.append(tuple(new_state))
    
    return neighbors



def dfs(start_state):
    stack = [(start_state, [])]
    visited = set()
    visited.add(start_state)

    while stack:
        current_state, path = stack.pop()

        if is_goal(current_state):
            return path + [current_state]

        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [current_state]))
    
    return None



def best_first_search(start_state):
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(start_state), start_state, []))
    visited = set()
    visited.add(start_state)

    while open_list:
        _, current_state, path = heapq.heappop(open_list)

        if is_goal(current_state):
            return path + [current_state]

        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                heapq.heappush(open_list, (manhattan_distance(neighbor), neighbor, path + [current_state]))
    
    return None



def iddfs(start_state):
    def dfs_with_depth_limit(state, depth, path):
        if depth == 0:
            return None
        if is_goal(state):
            return path + [state]
        
        for neighbor in get_neighbors(state):
            result = dfs_with_depth_limit(neighbor, depth - 1, path + [state])
            if result:
                return result
        return None

    depth = 0
    while True:
        result = dfs_with_depth_limit(start_state, depth, [])
        if result:
            return result
        depth += 1


start_state = (5, 6, 3, 1, 2, 0, 4, 7, 8)


print("DFS Solution:")
start_time = time.time()
dfs_solution = dfs(start_state)
end_time = time.time()

if dfs_solution:
    for step in dfs_solution:
        print(step)
else:
    print("No solution found using DFS.")
print(f"Time taken for DFS: {end_time - start_time:.6f} seconds")


print("\nBest-First Search Solution:")
start_time = time.time()
best_first_solution = best_first_search(start_state)
end_time = time.time()
if best_first_solution:
    for step in best_first_solution:
        print(step)
else:
    print("No solution found using Best-First Search.")
print(f"Time taken for Best-First Search: {end_time - start_time:.6f} seconds")


print("\nIDDFS Solution:")
start_time = time.time()
iddfs_solution = iddfs(start_state)
end_time = time.time()
if iddfs_solution:
    for step in iddfs_solution:
        print(step)
else:
    print("No solution found using IDDFS.")
print(f"Time taken for IDDFS: {end_time - start_time:.6f} seconds")