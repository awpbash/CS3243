from typing import List, Tuple
from collections import deque
import numpy as np

def dfs_search(dct) -> List[Tuple[int, int]]:
    cols = dct['cols']
    rows = dct['rows']
    start = tuple(dct['start'])
    goals = set(tuple(goal) for goal in dct['goals'])
    obstacles = set(tuple(obstacle) for obstacle in dct['obstacles'])

    if start in obstacles:
        return []
    if start in goals:
        return [start]
    #Heuristic is that we should prioritise directions that gets use closer to the goal. This is only a 1 time computation and is kinda like greedy search but still dfs
    nearest_goal = min(goals, key=lambda g: abs(g[0] - start[0]) + abs(g[1] - start[1]))

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    directions.sort(key=lambda d: abs((start[0] + d[0]) - nearest_goal[0]) + abs((start[1] + d[1]) - nearest_goal[1]))

    visited = np.zeros((rows, cols), dtype=bool) #use numpy boolean array to mark visited compared to set cos FAST
    for obstacle in obstacles:
        visited[obstacle] = True

    stack = deque([start]) #double ended queue so much faster than list
    parent_map = {} #instead of keeping path in stack which may explode memory, use hashmap for backtracking and fast retrieval
    visited[start] = True

    while stack:
        current_position = stack.pop()

        if current_position in goals:
            path = []
            while current_position is not None:
                path.append(current_position)
                current_position = parent_map.get(current_position)
            return path[::-1]

        for direction in directions:
            next_position = (current_position[0] + direction[0], current_position[1] + direction[1])

            if (0 <= next_position[0] < rows and 
                0 <= next_position[1] < cols and 
                not visited[next_position]):

                visited[next_position] = True
                parent_map[next_position] = current_position
                stack.append(next_position)

    return []
