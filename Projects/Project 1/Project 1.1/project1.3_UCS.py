from typing import List, Tuple
import heapq
import numpy as np
#using heap instead of deque
def ucs_search(dct) -> List[Tuple[int, int]]:
    cols = dct['cols']
    rows = dct['rows']
    start = tuple(dct['start'])
    goals = set(tuple(goal) for goal in dct['goals'])
    obstacles = set(tuple(obstacle) for obstacle in dct['obstacles'])

    if start in obstacles:
        return []
    if start in goals:
        return [start]

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  #Right, Down, Left, Up
    
    visited = np.zeros((rows, cols), dtype=bool)
    for obstacle in obstacles:
        visited[obstacle] = True

    pq = []
    heapq.heappush(pq, (0, start))
    parent_map = {start: None}
    cost_map = {start: 0}
    visited[start] = True

    while pq:
        current_cost, current_position = heapq.heappop(pq)

        if current_position in goals:
            path = []
            while current_position is not None:
                path.append(current_position)
                current_position = parent_map[current_position]
            return path[::-1]

        for direction in directions:
            next_position = (current_position[0] + direction[0], current_position[1] + direction[1])
            next_cost = current_cost + 1  # All moves cost 1

            if (0 <= next_position[0] < rows and 
                0 <= next_position[1] < cols and 
                not visited[next_position]):

                if next_position not in cost_map or next_cost < cost_map[next_position]:
                    cost_map[next_position] = next_cost
                    parent_map[next_position] = current_position
                    heapq.heappush(pq, (next_cost, next_position))
                    visited[next_position] = True

    return []
