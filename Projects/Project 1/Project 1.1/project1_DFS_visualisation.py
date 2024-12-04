from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import os
import json
import time
from collections import deque

start_time = time.time()

def dfs_search(dct) -> List[Tuple[int, int]]:
    '''
    parameters in dct:
    -'cols': int
    -'rows': int
    -'start': Tuple[int, int]
    -'goals': List(Tuple[int, int])
    -'obstacles': List(Tuple[int, int])
    ''' 
    cols = dct['cols']
    rows = dct['rows']
    start = tuple(dct['start'])
    goals = set(tuple(goal) for goal in dct['goals'])
    obstacles = set(tuple(obstacle) for obstacle in dct['obstacles'])

    if start in goals:
        return [start], {start}

    # Direction vectors for right, up, left, down
    directions = [ (0,1), (-1,0), (0,-1),(1,0)]

    # Stack for DFS with path
    stack = [(start, [start])]
    visited = set()

    while stack:
        current_position, path = stack.pop()

        # If the current position is a goal, return the path
        if current_position in goals:
            print("solvable")
            return path, visited

        # Mark the current position as visited
        visited.add(current_position)

        # Explore neighbors in all directions
        for direction in directions:
            next_position = (current_position[0] + direction[0], current_position[1] + direction[1])

            # Check if the next position is within bounds, not visited, and not an obstacle
            if (0 <= next_position[0] < rows and 
                0 <= next_position[1] < cols and 
                next_position not in visited and 
                next_position not in obstacles):

                # Continue DFS with the next position and updated path
                stack.append((next_position, path + [next_position]))

    # If no path is found, return an empty list and the visited cells
    print("not solvable")
    return [], visited

def bfs_search(dct) -> List[Tuple[int, int]]:
    '''
    parameters in dct:
    -'cols': int
    -'rows': int
    -'start': Tuple[int, int]
    -'goals': List(Tuple[int, int])
    -'obstacles': List(Tuple[int, int])
    '''
    cols = dct['cols']
    rows = dct['rows']
    start = tuple(dct['start'])
    goals = set(tuple(goal) for goal in dct['goals'])
    obstacles = set(tuple(obstacle) for obstacle in dct['obstacles'])

    if start in goals:
        return [start], {start}

    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]  # Right, Up, Left, Down

    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)

    while queue:
        current_position, path = queue.popleft()

        if current_position in goals:
            print("solvable")
            return path, visited

        for direction in directions:
            next_position = (current_position[0] + direction[0], current_position[1] + direction[1])

            if (0 <= next_position[0] < rows and 
                0 <= next_position[1] < cols and 
                next_position not in visited and 
                next_position not in obstacles):

                visited.add(next_position)
                queue.append((next_position, path + [next_position]))

    print("not solvable")
    return [], visited

# Define the visualization function using matplotlib
def visualize_maze_plot(maze, path, output_file, visited):
    """
    Visualizes the maze and the path using Matplotlib and saves it as an image.

    Parameters:
    - maze: Dictionary containing maze details (rows, cols, obstacles, start, goals).
    - path: List of tuples representing the path from start to goal.
    - output_file: String representing the file path to save the plot image.
    - visited: Set of tuples representing the visited cells.
    """
    rows = maze['rows']
    cols = maze['cols']
    obstacles = set(tuple(obstacle) for obstacle in maze['obstacles'])
    start = tuple(maze['start'])
    goals = set(tuple(goal) for goal in maze['goals'])

    # Create a grid representation
    grid = np.zeros((rows, cols))
    
    # Mark obstacles in the grid
    for (r, c) in obstacles:
        grid[r][c] = 1  # 1 represents an obstacle
    
    # Initialize the plot
    fig, ax = plt.subplots(figsize=(cols / 2, rows / 2))
    
    # Display the grid
    ax.imshow(grid, cmap='Greys', origin='upper')

    # Plot the visited cells if no path is found
    if not path:
        for r, c in visited:
            ax.scatter(c, r, color='black', s=100, marker='x', label='Visited' if (r, c) == list(visited)[0] else "")

    # If a path exists, plot it
    if path:
        plt.title('Solvable Maze')
        # Extract x and y coordinates from the path
        x_coords = [c for r, c in path]
        y_coords = [r for r, c in path]
        
        # Plot the path as a blue line with markers
        ax.plot(x_coords, y_coords, color='blue', linewidth=2, label='Path')
        ax.scatter(x_coords, y_coords, color='blue', s=20)  # Optional: small dots on path
    else:
        plt.title('Not Solvable Maze')

    # Plot the start position
    ax.scatter(start[1], start[0], marker='o', color='green', s=200, label='Start')

    # Plot the goal positions
    for goal in goals:
        ax.scatter(goal[1], goal[0], marker='*', color='red', s=200, label='Goal')

    # Add grid lines for better readability
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)

    # Invert y-axis to have row 0 at the top
    ax.invert_yaxis()

    # Remove axis labels for a cleaner look
    ax.set_xticks([])
    ax.set_yticks([])

    # Handle legend to avoid duplicate labels
    handles, labels = ax.get_legend_handles_labels()
    by_label = {}
    for h, l in zip(handles, labels):
        if l not in by_label:
            by_label[l] = h
    ax.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(1.15, 1))

    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()


# Folder containing the JSON files
folder_path = r"C:\Users\ngjun\Desktop\Mods\Y3S1\CS3243\Project 1.1\upload_testcases\correctness"

# Iterate over all JSON files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json") and "_ab_" in filename:
        print(filename)
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r') as f:
            maze = json.load(f)
        
        # Run DFS search on the maze
        path, visited = bfs_search(maze)
        
        # Create an output filename
        output_filename = os.path.join(folder_path, filename.replace(".json", ".png"))
        # Visualize the maze and save to an image file
        visualize_maze_plot(maze, path, output_filename, visited)

print("--- %s seconds ---" % (time.time() - start_time))
