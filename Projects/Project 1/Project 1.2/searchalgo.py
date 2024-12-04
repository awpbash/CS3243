import heapq
from enum import Enum

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    FLASH = 4
    NUKE = 5

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def apply_nuke(nuke_pos, rows, cols, creeps, obstacles):
    """Apply nuke and return all the positions affected within a Manhattan distance of 10."""
    nuked_positions = set()
    nuke_x, nuke_y = nuke_pos

    for x in range(max(0, nuke_x - 10), min(rows, nuke_x + 10 + 1)):
        for y in range(max(0, nuke_y - 10), min(cols, nuke_y + 10 + 1)):
            if manhattan_distance((nuke_x, nuke_y), (x, y)) <= 10 and (x, y) not in obstacles:
                nuked_positions.add((x, y))
    return nuked_positions

def search(dct) -> list[int]:
    # Build grid
    rows, cols = dct['rows'], dct['cols']
    start = tuple(dct['start'])
    goals = [tuple(goal) for goal in dct['goals']]
    obstacles = set(tuple(obstacle) for obstacle in dct['obstacles'])
    creeps = {(x, y): num_creeps for x, y, num_creeps in dct['creeps']}
    num_flash_left = dct['num_flash_left']
    num_nuke_left = dct['num_nuke_left']
    nuked = set()
    #pq for A*Star where f_cost = total, h_cost = heuristic, g_cost = actual path cost
    pq = []
    heapq.heappush(pq, (0, 0, start, [], num_flash_left, (set(), num_nuke_left)))  # (f_cost, g_cost, position, actions, flash_left, (nuked_positions, nuke_left))
    visited = set()

    #directions for UP, DOWN, LEFT, RIGHT
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while pq:
        f_cost, g_cost, current_pos, actions, flash_left, (nuked, nukes_left) = heapq.heappop(pq)

        # Goal test
        if current_pos in goals:
            print(f_cost)
            return actions

        #visited check
        if (current_pos, flash_left, tuple(nuked)) in visited:
            continue
        visited.add((current_pos, flash_left, tuple(nuked)))

        #normal movement
        for i, (dx, dy) in enumerate(directions):
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            #check if new_pos is valid
            if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and new_pos not in obstacles:
                new_cost = 4
                if new_pos in creeps and new_pos not in nuked:
                    new_cost += creeps[new_pos]
                
                #calculate heuristic
                h_cost = min(manhattan_distance(new_pos, goal) for goal in goals)
                total_cost = g_cost + new_cost + h_cost

                heapq.heappush(pq, (total_cost, g_cost + new_cost, new_pos, actions + [i], flash_left, (nuked, nukes_left)))

        if flash_left > 0:
            for i, (dx, dy) in enumerate(directions):
                new_pos = current_pos  # Start flashing from the current position
                flash_cost = 10
                while True:

                    next_pos = (new_pos[0] + dx, new_pos[1] + dy)
                    

                    if not (0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols):
                        break 

                    if next_pos in obstacles:
                        break 
                    new_pos = next_pos
                    flash_cost += 2

                    if new_pos in creeps and new_pos not in nuked:
                        flash_cost += creeps.get(new_pos, 0) 
                move_pos = new_pos
                move_cost = 0 
                num_grids_traveled = 0

                while True:

                    next_pos = (move_pos[0] + dx, move_pos[1] + dy)
                    
                    #check if next_pos is within bounds
                    if not (0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols):
                        break  # Stop at boundary
                    
                    #check if next_pos is an obstacle
                    if next_pos in obstacles:
                        break  # Stop at obstacle
                    
                    #if valid, update move_pos to next_pos
                    move_pos = next_pos
                    num_grids_traveled += 1

                    #add creep cost for moving through the grid
                    move_cost += creeps.get(move_pos, 0)  # Add creep cost if present

                #calculate the total cost based on flash and grid traversal after flash
                final_cost = 2 * num_grids_traveled + move_cost  # Post-flash movement cost (2 per grid + creeps)

                #heuristic to calculate estimated distance to the nearest goal
                h_cost = min(manhattan_distance(move_pos, goal) for goal in goals)
                total_cost = g_cost + flash_cost + final_cost + h_cost

                #push new state with updated costs and position into the priority queue
                #append `Action.FLASH.value` once, and then `i` (direction) once
                if move_pos != current_pos:  # Only push if we actually moved
                    heapq.heappush(pq, (total_cost, g_cost + flash_cost + final_cost, move_pos, actions + [Action.FLASH.value, i], flash_left - 1, (nuked, nukes_left)))

        #Nuke spell
        if nukes_left > 0:
            nuked_positions = apply_nuke(current_pos, rows, cols, creeps, obstacles)
            #combine nuke set if got more than 1 nuke available
            updated_nuked = nuked.union(nuked_positions)

            #calculate heuristic
            h_cost = min(manhattan_distance(current_pos, goal) for goal in goals)
            nuke_cost = 50
            total_cost = g_cost + nuke_cost + h_cost
            
            #push into pq
            heapq.heappush(pq, (total_cost, g_cost + nuke_cost, current_pos, actions + [Action.NUKE.value], flash_left, (updated_nuked, nukes_left - 1)))

    #return empty list if no valid path is found
    return []

'''
Big Idea
create a set called nuked to store all the positions that have been nuked
everytime we move, we check if the box is in nuked set, if yes then no creep cost
if no then add the creep cost to the total cost

For flash, we create a while loop to keep going in the direction until we hit an obstacle
then we calculate the cost of the flash and creeps encountered and add it to the total cost

For nuke, we use the apply_nuke function to get all the positions that will be affected by the nuke
We can union the nuked set with the nuked_positions to get the updated nuked set
'''

