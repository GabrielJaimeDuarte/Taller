import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

tree = {
    'S': ['A', 'B', 'D', 'E'],
    'A': ['F', 'G'],
    'B': ['H', 'R'],
    'D': ['J'],
    'E': ['K', 'L'],
    'F': ['M'],
    'G': [],
    'H': ['O', 'Q'],
    'R': ['X', 'T'],
    'J': ['Y'],
    'K': ['I'],
    'L': ['CC'],
    'M': ['N'],
    'O': ['P'],
    'Q': ['U'],
    'X': [],
    'T': ['GG'],
    'Y': ['Z'],
    'I': [],
    'CC': ['DD', 'EE'],
    'EE': ['FF'],
    'N': [],
    'P': [],
    'U': ['V', 'W'],
    'GG': [],
    'Z': ['AA', 'BB'],
    'DD': [],
    'FF': [],
    'V': [],
    'W': [],  # Objetivo
    'AA': [],
    'BB': []
}

def create_graph():
    """Crear grafo para visualización"""
    G = nx.DiGraph()
    for parent, children in tree.items():
        for child in children:
            G.add_edge(parent, child)
    return G

def hierarchy_pos(G, root, width=8.0, vert_gap=0.3):
    """Función para posición jerárquica"""
    def _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter, pos=None, parent=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, 
                                    vert_loc=vert_loc-vert_gap, xcenter=nextx, 
                                    pos=pos, parent=root)
        return pos
    
    return _hierarchy_pos(G, root, width, vert_gap, 0, 0.5)

def bfs_with_goal(tree, start, goal):
    """BFS con objetivo y visualización"""
    visited = []
    queue = deque([start])
    parent = {start: None}
    step = 0
    
    G = create_graph()
    pos = hierarchy_pos(G, start)
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(20, 14))
    
    while queue:
        current_node = queue.popleft()
        
        if current_node not in visited:
            visited.append(current_node)
            
            if current_node == goal:
                path = []
                node = current_node
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                
                plt.clf()
                nx.draw(G, pos, with_labels=True, node_color="lightblue", 
                       node_size=1000, font_size=7, font_weight="bold")
                nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="green", node_size=1000)
                nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color="purple", node_size=1200)
                
                plt.title(f"BFS - ¡OBJETIVO 'W' ENCONTRADO!\n"
                         f"Camino: {' → '.join(path)}\nLongitud: {len(path)-1} pasos\n"
                         f"Nodos visitados: {len(visited)}", fontsize=13, pad=20)
                plt.tight_layout()
                plt.pause(3)
                plt.ioff()
                
                return path, visited
            
            for child in tree[current_node]:
                if child not in visited and child not in queue:
                    queue.append(child)
                    parent[child] = current_node
            
            plt.clf()
            nx.draw(G, pos, with_labels=True, node_color="lightblue", 
                   node_size=1000, font_size=7, font_weight="bold")
            nx.draw_networkx_nodes(G, pos, nodelist=visited, node_color="red", node_size=1000)
            nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color="orange", node_size=1000)
            if queue:
                nx.draw_networkx_nodes(G, pos, nodelist=list(queue), node_color="yellow", node_size=1000)
            nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color="purple", node_size=1200)
            
            plt.title(f"BFS - Paso {step}\nVisitando: '{current_node}'\n"
                     f"Visitados: {len(visited)}, En cola: {len(queue)}", fontsize=11, pad=20)
            plt.tight_layout()
            plt.pause(0.8)
            step += 1
    
    plt.ioff()
    return None, visited

def dfs_with_goal(tree, start, goal):
    """DFS con objetivo y visualización"""
    visited = []
    stack = [start]
    parent = {start: None}
    step = 0
    
    G = create_graph()
    pos = hierarchy_pos(G, start)
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(20, 14))
    
    while stack:
        current_node = stack.pop()
        
        if current_node not in visited:
            visited.append(current_node)
            
            if current_node == goal:
                path = []
                node = current_node
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                
                plt.clf()
                nx.draw(G, pos, with_labels=True, node_color="lightblue", 
                       node_size=1000, font_size=7, font_weight="bold")
                nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="green", node_size=1000)
                nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color="purple", node_size=1200)
                
                plt.title(f"DFS - ¡OBJETIVO 'W' ENCONTRADO!\n"
                         f"Camino: {' → '.join(path)}\nLongitud: {len(path)-1} pasos\n"
                         f"Nodos visitados: {len(visited)}", fontsize=13, pad=20)
                plt.tight_layout()
                plt.pause(3)
                plt.ioff()
                
                return path, visited
            
            for child in reversed(tree[current_node]):
                if child not in visited and child not in stack:
                    stack.append(child)
                    parent[child] = current_node
            
            plt.clf()
            nx.draw(G, pos, with_labels=True, node_color="lightblue", 
                   node_size=1000, font_size=7, font_weight="bold")
            nx.draw_networkx_nodes(G, pos, nodelist=visited, node_color="red", node_size=1000)
            nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color="orange", node_size=1000)
            if stack:
                nx.draw_networkx_nodes(G, pos, nodelist=stack, node_color="yellow", node_size=1000)
            nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color="purple", node_size=1200)
            
            plt.title(f"DFS - Paso {step}\nVisitando: '{current_node}'\n"
                     f"Visitados: {len(visited)}, En pila: {len(stack)}", fontsize=11, pad=20)
            plt.tight_layout()
            plt.pause(0.8)
            step += 1
    
    plt.ioff()
    return None, visited

print("=" * 60)
print("BÚSQUEDA POR AMPLITUD (BFS)")
print("=" * 60)
bfs_path, bfs_visited = bfs_with_goal(tree, 'S', 'W')

print("\n" + "=" * 60)
print("BÚSQUEDA POR PROFUNDIDAD (DFS)")
print("=" * 60)
dfs_path, dfs_visited = dfs_with_goal(tree, 'S', 'W')

print("\n" + "=" * 60)
print("RESULTADOS COMPARATIVOS")
print("=" * 60)

if bfs_path:
    print(f"BFS - Camino encontrado: {' → '.join(bfs_path)}")
    print(f"BFS - Longitud del camino: {len(bfs_path)-1} pasos")
    print(f"BFS - Nodos visitados: {len(bfs_visited)}")
    print(f"BFS - Todos los visitados: {bfs_visited}")
else:
    print("BFS - No se encontró el camino")

print()

if dfs_path:
    print(f"DFS - Camino encontrado: {' → '.join(dfs_path)}")
    print(f"DFS - Longitud del camino: {len(dfs_path)-1} pasos")
    print(f"DFS - Nodos visitados: {len(dfs_visited)}")
    print(f"DFS - Todos los visitados: {dfs_visited}")
else:
    print("DFS - No se encontró el camino")

print("\n" + "=" * 60)
print("COMPARACIÓN BFS vs DFS")
print("=" * 60)
if bfs_path and dfs_path:
    print(f"✓ Ambos algoritmos encontraron el objetivo 'W'")
    print(f"✓ BFS encontró un camino de: {len(bfs_path)-1} pasos")
    print(f"✓ DFS encontró un camino de: {len(dfs_path)-1} pasos")
    print(f"✓ BFS visitó {len(bfs_visited)} nodos")
    print(f"✓ DFS visitó {len(dfs_visited)} nodos")
    
    if len(bfs_path) < len(dfs_path):
        print("✓ BFS es mejor para encontrar el camino más corto")
    elif len(dfs_path) < len(bfs_path):
        print("✓ DFS encontró un camino más corto (inusual)")
    else:
        print("✓ Ambos encontraron caminos de la misma longitud")
        
    if len(bfs_visited) < len(dfs_visited):
        print("✓ BFS fue más eficiente en número de nodos visitados")
    else:
        print("✓ DFS fue más eficiente en número de nodos visitados")