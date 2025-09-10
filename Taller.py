import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import heapq
import random

tree_with_costs = {
    'S': [('A', 3), ('B', 2), ('D', 4), ('E', 1)],
    'A': [('F', 5), ('G', 2)],
    'B': [('H', 3), ('R', 1)],
    'D': [('J', 2)],
    'E': [('K', 4), ('L', 3)],
    'F': [('M', 1)],
    'G': [],
    'H': [('O', 2), ('Q', 3)],
    'R': [('X', 4), ('T', 2)],
    'J': [('Y', 1)],
    'K': [('I', 5)],
    'L': [('CC', 2)],
    'M': [('N', 3)],
    'O': [('P', 1)],
    'Q': [('U', 2)],
    'X': [],
    'T': [('GG', 4)],
    'Y': [('Z', 3)],
    'I': [],
    'CC': [('DD', 1), ('EE', 2)],
    'EE': [('FF', 3)],
    'N': [],
    'P': [],
    'U': [('V', 2), ('W', 1)],  
    'GG': [],
    'Z': [('AA', 2), ('BB', 3)],
    'DD': [],
    'FF': [],
    'V': [],
    'W': [],  # Objetivo
    'AA': [],
    'BB': []
}

tree = {}
for node, children in tree_with_costs.items():
    tree[node] = [child[0] for child in children]

def create_graph():
    """Crear grafo para visualización"""
    G = nx.DiGraph()
    for parent, children in tree_with_costs.items():
        for child, cost in children:
            G.add_edge(parent, child, weight=cost)
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

def ucs_with_goal(tree_with_costs, start, goal):
    """UCS con objetivo y visualización"""
    visited = set()
    priority_queue = [(0, start, [start])]  
    parent = {start: None}
    step = 0
    
    G = create_graph()
    pos = hierarchy_pos(G, start)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(20, 14))
    
    while priority_queue:
        current_cost, current_node, current_path = heapq.heappop(priority_queue)
        
        if current_node not in visited:
            visited.add(current_node)
            
            if current_node == goal:
                plt.clf()
                nx.draw(G, pos, with_labels=True, node_color="lightblue", 
                       node_size=1000, font_size=7, font_weight="bold")
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
                nx.draw_networkx_nodes(G, pos, nodelist=current_path, node_color="green", node_size=1000)
                nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color="purple", node_size=1200)
                
                plt.title(f"UCS - ¡OBJETIVO 'W' ENCONTRADO!\n"
                         f"Camino: {' → '.join(current_path)}\n"
                         f"Costo total: {current_cost}\nLongitud: {len(current_path)-1} pasos\n"
                         f"Nodos visitados: {len(visited)}", fontsize=13, pad=20)
                plt.tight_layout()
                plt.pause(4)
                plt.ioff()
                
                return current_path, list(visited), current_cost
            
            for child, cost in tree_with_costs.get(current_node, []):
                if child not in visited:
                    new_cost = current_cost + cost
                    new_path = current_path + [child]
                    heapq.heappush(priority_queue, (new_cost, child, new_path))
                    parent[child] = current_node
            
            plt.clf()
            nx.draw(G, pos, with_labels=True, node_color="lightblue", 
                   node_size=1000, font_size=7, font_weight="bold")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
            nx.draw_networkx_nodes(G, pos, nodelist=list(visited), node_color="red", node_size=1000)
            nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color="orange", node_size=1000)
            
            next_nodes = [node for _, node, _ in priority_queue[:5]]
            if next_nodes:
                nx.draw_networkx_nodes(G, pos, nodelist=next_nodes, node_color="yellow", node_size=1000)
            
            nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color="purple", node_size=1200)
            
            queue_info = []
            for cost, node, path in priority_queue[:3]:
                queue_info.append(f"{node}({cost})")
            
            plt.title(f"UCS - Paso {step}\nVisitando: '{current_node}' (Costo: {current_cost})\n"
                     f"Visitados: {len(visited)}, En cola prioridad: {len(priority_queue)}\n"
                     f"Próximos: {', '.join(queue_info)}", fontsize=11, pad=20)
            plt.tight_layout()
            plt.pause(1.0)
            step += 1
    
    plt.ioff()
    return None, list(visited), float('inf')

print("=" * 60)
print("BÚSQUEDA POR AMPLITUD (BFS)")
print("=" * 60)
bfs_path, bfs_visited = bfs_with_goal(tree, 'S', 'W')

print("\n" + "=" * 60)
print("BÚSQUEDA POR PROFUNDIDAD (DFS)")
print("=" * 60)
dfs_path, dfs_visited = dfs_with_goal(tree, 'S', 'W')

print("\n" + "=" * 60)
print("BÚSQUEDA DE COSTO UNIFORME (UCS)")
print("=" * 60)
ucs_path, ucs_visited, ucs_cost = ucs_with_goal(tree_with_costs, 'S', 'W')

print("\n" + "=" * 80)
print("RESULTADOS COMPARATIVOS - BFS vs DFS vs UCS")
print("=" * 80)

if bfs_path:
    print(f"BFS  - Camino: {' → '.join(bfs_path)}")
    print(f"     - Longitud: {len(bfs_path)-1} pasos, Nodos visitados: {len(bfs_visited)}")
else:
    print("BFS - No se encontró el camino")

if dfs_path:
    print(f"DFS  - Camino: {' → '.join(dfs_path)}")
    print(f"     - Longitud: {len(dfs_path)-1} pasos, Nodos visitados: {len(dfs_visited)}")
else:
    print("DFS - No se encontró el camino")

if ucs_path:
    print(f"UCS  - Camino: {' → '.join(ucs_path)}")
    print(f"     - Costo total: {ucs_cost}, Longitud: {len(ucs_path)-1} pasos")
    print(f"     - Nodos visitados: {len(ucs_visited)}")
else:
    print("UCS - No se encontró el camino")

# COMPARACIÓN DETALLADA
print("\n" + "=" * 80)
print("ANÁLISIS COMPARATIVO")
print("=" * 80)

if bfs_path and dfs_path and ucs_path:
    print("✓ Los tres algoritmos encontraron el objetivo 'W'")
    print(f"\n📊 COMPARACIÓN DE CAMINOS:")
    print(f"   BFS:  {len(bfs_path)-1} pasos - {' → '.join(bfs_path)}")
    print(f"   DFS:  {len(dfs_path)-1} pasos - {' → '.join(dfs_path)}")
    print(f"   UCS:  {ucs_cost} unidades de costo - {' → '.join(ucs_path)}")
    
    print(f"\n📊 EFICIENCIA EN NODOS VISITADOS:")
    print(f"   BFS visitó: {len(bfs_visited)} nodos")
    print(f"   DFS visitó: {len(dfs_visited)} nodos")
    print(f"   UCS visitó: {len(ucs_visited)} nodos")
    
    if ucs_cost < len(bfs_path) - 1:  # Comparar costo UCS vs pasos BFS
        print(f"\n🎯 UCS encontró un camino MÁS ECONÓMICO que BFS")
        print(f"   (Costo UCS: {ucs_cost} vs Pasos BFS: {len(bfs_path)-1})")
    elif ucs_cost == len(bfs_path) - 1:
        print(f"\n🎯 UCS y BFS encontraron caminos igual de eficientes")
    else:
        print(f"\n🎯 BFS encontró un camino más corto en pasos")
        print(f"   (Pasos BFS: {len(bfs_path)-1} vs Costo UCS: {ucs_cost})")
    
    print(f"\n💡 OBSERVACIONES:")
    print("- BFS garantiza el camino más corto en número de pasos")
    print("- UCS garantiza el camino de menor costo acumulado")
    print("- DFS puede encontrar caminos más largos pero a veces más rápido")
    print("- UCS considera los costos de las aristas en la búsqueda")

print("\n" + "=" * 80)
print("COSTOS DEL ÁRBOL")
print("=" * 80)
for node, children in tree_with_costs.items():
    if children:
        costs_str = ", ".join([f"{child}({cost})" for child, cost in children])
        print(f"{node} → [{costs_str}]")