import matplotlib.pyplot as plt
import numpy as np
from collections import deque

def invert_maze(maze):
    return [[1 if cell == 0 else 0 for cell in row] for row in maze]

def solve_maze(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    queue = deque([start])
    visited = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return path[::-1]
        
        for dr, dc in directions:
            r, c = current[0] + dr, current[1] + dc
            if 0 <= r < rows and 0 <= c < cols and maze[r][c] == 1 and (r, c) not in visited:
                queue.append((r, c))
                visited[(r, c)] = current
    
    return None

def plot_maze(maze, path, title, start, goal):
    maze_array = np.array(maze)
    plt.figure(figsize=(12, 6))
    plt.imshow(maze_array, cmap='binary', interpolation='nearest')
    
    if path:
        path_y, path_x = zip(*path)
        plt.plot(path_x, path_y, 'r-', linewidth=2)
        plt.plot(path_x, path_y, 'ro', markersize=4)
    
    plt.plot(start[1], start[0], 'o', markersize=10, color='red', label='Inicio')
    plt.plot(goal[1], goal[0], 'X', markersize=10, color='green', label='Meta')
    
    plt.title(title)
    plt.legend()
    plt.grid(False)
    plt.show()

start = (12, 0)
goal = (0, 29)
maze = [
 [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0,0,0],
 [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0],
 [0,0,0,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0],
 [0,0,0,0,0,0,1,1,0,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0],
 [0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0],
 [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,0,0,0,0],
 [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0],
 [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1],
 [0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1],
 [0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

inverted_maze = invert_maze(maze)

path = solve_maze(inverted_maze, start, goal)

print("Laberinto Original (0=camino, 1=obstáculo)")
plot_maze(maze, None, "Laberinto Original", start, goal)

print("Laberinto Invertido (1=camino, 0=obstáculo)")
plot_maze(inverted_maze, None, "Laberinto Invertido", start, goal)

if path:
    print(f"Se encontró un camino de {len(path)} pasos")
    print("Camino encontrado:", path[:5], "...", path[-5:])
    print("\nLaberinto Invertido con Camino")
    plot_maze(inverted_maze, path, "Laberinto Invertido con Camino", start, goal)
else:
    print("No se encontró un camino válido")