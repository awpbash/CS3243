from typing import List, Tuple
from collections import deque
import numpy as np

def bfs_search(dct) -> List[Tuple[int, int]]:
    cols = dct['cols']
    rows = dct['rows']
    start = tuple(dct['start'])
    goals = set(tuple(goal) for goal in dct['goals'])
    obstacles = set(tuple(obstacle) for obstacle in dct['obstacles'])

    if start in obstacles:
        return []
    if start in goals:
        return [start]

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)] 
    visited = np.zeros((rows, cols), dtype=bool)
    for obstacle in obstacles:
        visited[obstacle] = True

    queue = deque([start])
    parent_map = {start: None}
    visited[start] = True

    while queue:
        current_position = queue.popleft()

        if current_position in goals:
            path = []
            while current_position is not None:
                path.append(current_position)
                current_position = parent_map[current_position]
            return path[::-1]

        for direction in directions:
            next_position = (current_position[0] + direction[0], current_position[1] + direction[1])

            if (0 <= next_position[0] < rows and 
                0 <= next_position[1] < cols and 
                not visited[next_position]):

                visited[next_position] = True
                parent_map[next_position] = current_position
                queue.append(next_position)

    return []
