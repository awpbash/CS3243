from typing import List, Tuple
import heapq
from enum import Enum

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    FLASH = 4
    NUKE = 5

directions = {
    Action.UP: (-1, 0),
    Action.DOWN: (1, 0),
    Action.LEFT: (0, -1),
    Action.RIGHT: (0, 1)
}

def manhat_dist(p1, p2) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def search(dct) -> Tuple[List[int], int]:
    cols = dct['cols']
    rows = dct['rows']
    obstacles = set(tuple(obstacle) for obstacle in dct['obstacles'])
    creeps = {(creep[0], creep[1]): creep[2] for creep in dct['creeps']}
    start = tuple(dct['start'])
    goals = set(tuple(goal) for goal in dct['goals'])
    num_flash_left = dct['num_flash_left']
    num_nuke_left = dct['num_nuke_left']

    if start in obstacles or start in goals:
        return [], 0
    
    MP_cost = {Action.UP: 4, Action.DOWN: 4, Action.LEFT: 4, Action.RIGHT: 4, Action.FLASH: 10, Action.NUKE: 50}

    def is_valid(pos):
        x, y = pos
        return 0 <= x < rows and 0 <= y < cols and pos not in obstacles

    def use_flash(current_pos, direction, flashes_left):
        if flashes_left <= 0:
            return None
        x, y = current_pos
        while is_valid((x + direction[0], y + direction[1])):
            x += direction[0]
            y += direction[1]
        return (x, y) if (x, y) != current_pos else None

    open_set = []
    heapq.heappush(open_set, (0, start, [], 0, num_flash_left, num_nuke_left))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhat_dist(start, min(goals, key=lambda g: manhat_dist(start, g)))}

    while open_set:
        _, current_pos, actions, consecutive_actions, flashes_left, nukes_left = heapq.heappop(open_set)

        if current_pos in goals:
            return [action.value for action in actions], g_score[current_pos]

        for action in [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]:
            direction = directions[action]
            neighbor = (current_pos[0] + direction[0], current_pos[1] + direction[1])

            if not is_valid(neighbor):
                continue

            # Calculate the additional MP cost from creeps
            creep_cost = creeps.get(neighbor, 0) * 2
            tentative_g_score = g_score[current_pos] + MP_cost[action] + creep_cost

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhat_dist(neighbor, min(goals, key=lambda g: manhat_dist(neighbor, g)))
                heapq.heappush(open_set, (f_score[neighbor], neighbor, actions + [action], consecutive_actions + 1, flashes_left, nukes_left))

            # Check for flash usage if the same action has been used consecutively
            if consecutive_actions >= 5 and flashes_left > 0:
                flashed_pos = use_flash(current_pos, direction, flashes_left)
                if flashed_pos:
                    flash_creep_cost = creeps.get(flashed_pos, 0) * 2
                    flashed_g_score = g_score[current_pos] + MP_cost[Action.FLASH] + flash_creep_cost + \
                                      (abs(flashed_pos[0] - current_pos[0]) + abs(flashed_pos[1] - current_pos[1])) * 2
                    if flashed_pos not in g_score or flashed_g_score < g_score[flashed_pos]:
                        g_score[flashed_pos] = flashed_g_score
                        f_score[flashed_pos] = flashed_g_score + manhat_dist(flashed_pos, min(goals, key=lambda g: manhat_dist(flashed_pos, g)))
                        heapq.heappush(open_set, (f_score[flashed_pos], flashed_pos, actions + [Action.FLASH], 0, flashes_left - 1, nukes_left))
    
    return [], 0  # No valid path found

def create_grid_visualization(dct, path, total_cost):
    rows, cols = dct['rows'], dct['cols']
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    obstacles = set(tuple(obstacle) for obstacle in dct['obstacles'])
    creeps = {(creep[0], creep[1]): creep[2] for creep in dct['creeps']}
    start = tuple(dct['start'])
    goals = set(tuple(goal) for goal in dct['goals'])

    # Mark obstacles
    for obstacle in obstacles:
        grid[obstacle[0]][obstacle[1]] = '#'

    # Mark creeps
    for creep, num in creeps.items():
        grid[creep[0]][creep[1]] = str(num)

    # Mark the path
    x, y = start
    grid[x][y] = 'S'  # Start position
    for action_value in path:
        action = Action(action_value)
        if action in directions:  # Standard movement
            direction = directions[action]
            x += direction[0]
            y += direction[1]
            if (x, y) in goals:
                grid[x][y] = 'G'  # Goal position
            else:
                grid[x][y] = '*'
        elif action == Action.FLASH:  # Handle FLASH action
            while True:
                next_x = x + directions[Action.UP][0]
                next_y = y + directions[Action.UP][1]
                if 0 <= next_x < rows and 0 <= next_y < cols and grid[next_x][next_y] == '.':
                    x, y = next_x, next_y
                    grid[x][y] = '*'  # Mark the path while flashing
                    if (x, y) in goals:
                        grid[x][y] = 'G'
                        break
                else:
                    break

    # Output the grid and total cost
    with open("grid_visualization_20x20.txt", "w") as file:
        file.write("Grid visualization:\n\n")
        for row in grid:
            file.write(" ".join(row) + "\n")
        file.write(f"\nTotal MP cost: {total_cost}\n")


# Example usage
dct = {
    'cols': 20,
    'rows': 20,
    'obstacles': [
        [1, 1], [2, 2], [3, 3], [4, 4], [5, 5],
        [6, 6], [7, 7], [8, 8], [9, 9], [10, 10],
        [11, 11], [12, 12], [13, 13], [14, 14], [15, 15], [0, 19],
        [19, 0], [10, 5], [5, 10]
    ],
    'creeps': [
        [2, 3, 2], [4, 5, 3], [6, 7, 1], [8, 9, 4],
        [10, 11, 2], [12, 13, 3], [14, 15, 5], [16, 17, 1],
        [18, 19, 2], [3, 17, 3], [7, 12, 4], [15, 3, 2]
    ],
    'start': [0, 0],
    'goals': [[19, 19]],
    'num_flash_left': 2,
    'num_nuke_left': 1
}

path, total_cost = search(dct)
create_grid_visualization(dct, path, total_cost)
print("gay")
