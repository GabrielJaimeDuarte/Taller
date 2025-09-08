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

def bfs_with_goal(tree, start, goal):
    visited = []
    queue = deque([start])
    parent = {}  
    parent[start] = None
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(20, 14))
    
    G = nx.DiGraph()
    for parent_node, children in tree.items():
        for child in children:
            G.add_edge(parent_node, child)
    
    def hierarchy_pos(G, root, width=1.0, vert_gap=0.25, vert_loc=0, xcenter=0.5):
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
        
        return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    
    pos = hierarchy_pos(G, start, width=8.0, vert_gap=0.3)
    step = 0
    
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
                       node_size=1000, font_size=7, font_weight="bold", 
                       arrows=True, arrowstyle='->', arrowsize=10)
                
                nx.draw_networkx_nodes(G, pos, nodelist=path, 
                                      node_color="green", node_size=1000)
                nx.draw_networkx_nodes(G, pos, nodelist=[goal], 
                                      node_color="purple", node_size=1200)
                
                plt.title(f"¡OBJETIVO 'W' ENCONTRADO!\n"
                         f"Camino: {' → '.join(path)}\n"
                         f"Longitud del camino: {len(path)-1} pasos\n"
                         f"Nodos visitados: {len(visited)}", 
                         fontsize=13, pad=20, color='green')
                plt.tight_layout()
                plt.pause(5)
                plt.ioff()
                plt.show()
                
                return path, visited
            
            for child in tree[current_node]:
                if child not in visited and child not in queue:
                    queue.append(child)
                    parent[child] = current_node  # Registrar el padre
            
            plt.clf()
            nx.draw(G, pos, with_labels=True, node_color="lightblue", 
                   node_size=1000, font_size=7, font_weight="bold", 
                   arrows=True, arrowstyle='->', arrowsize=10)
            
            nx.draw_networkx_nodes(G, pos, nodelist=visited, 
                                  node_color="red", node_size=1000)
            
            nx.draw_networkx_nodes(G, pos, nodelist=[current_node], 
                                  node_color="orange", node_size=1000)
            
            if queue:
                nx.draw_networkx_nodes(G, pos, nodelist=list(queue), 
                                      node_color="yellow", node_size=1000)
            
            nx.draw_networkx_nodes(G, pos, nodelist=[goal], 
                                  node_color="purple", node_size=1200)
            
            plt.title(f"BFS - Buscando 'W' - Paso {step}\n"
                     f"Visitando: '{current_node}'\n"
                     f"Visitados: {len(visited)}, En cola: {len(queue)}\n"
                     f"Cola actual: {list(queue)}", 
                     fontsize=11, pad=20)
            plt.tight_layout()
            plt.pause(1.0)
            step += 1
    
    plt.ioff()
    plt.show()
    return None, visited

print("Iniciando BFS desde 'S' buscando el objetivo 'W'...")
path, visited_nodes = bfs_with_goal(tree, 'S', 'W')

if path:
    print(f"\n¡OBJETIVO ENCONTRADO!")
    print(f"Camino a 'W': {' → '.join(path)}")
    print(f"Longitud del camino: {len(path)-1} pasos")
    print(f"Nodos visitados: {len(visited_nodes)}")
    print(f"Todos los nodos visitados: {visited_nodes}")
else:
    print("\nObjetivo 'W' no encontrado")