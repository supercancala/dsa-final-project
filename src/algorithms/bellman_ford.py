import sys
from time import time
from graph_generator import createGraph 

def bellmanFord(V, edges, src):
    inf = float('inf')

    # Normalize edge types to python ints and compute the true maximum node index.
    normalized_edges = []
    max_node = -1
    for item in edges:
        u, v, w = item
        ui, vi, wi = int(u), int(v), int(w)
        normalized_edges.append((ui, vi, wi))
        if ui > max_node:
            max_node = ui
        if vi > max_node:
            max_node = vi

    # If edges contain nodes outside the declared V, expand V to accommodate them.
    V = max(V, max_node + 1)

    dist = [inf] * V
    dist[int(src)] = 0

    # Optimization: Early Termination
    for i in range(V - 1):
        changes = False
        for u, v, w in normalized_edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changes = True

        # If no changes in a full pass, stop.
        if not changes:
            return dist

    # Negative cycle check
    for u, v, w in normalized_edges:
        if dist[u] != inf and dist[u] + w < dist[v]:
            return [-1]

    return dist

if __name__ == '__main__':
    src = 0
    
    # 1. USE A SMALLER NUMBER FOR THE REAL TEST
    # Bellman-Ford is slow. 2,000 is a good stress test. 
    # 500,000 will hang your machine forever.
    try:
        val = input("Enter nodes (Recommended: 2000): ")
        v = int(val)
    except ValueError:
        v = 2000

    print(f"Generating raw graph for {v} nodes...")
    raw_edges = createGraph(v)

    # 2. CRITICAL FIX: MAKE IT UNDIRECTED
    # We must double the edges (u->v AND v->u) to match Dijkstra's environment
    # and ensure we can actually leave node 0. Normalize to ints while doing so.
    print("Converting to Undirected graph...")
    undirected_edges = []
    for item in raw_edges:
        u, w_v, w = item
        u, w_v, w = int(u), int(w_v), int(w)
        undirected_edges.append([u, w_v, w])
        undirected_edges.append([w_v, u, w]) # Add the reverse path
    
    print(f"Total Edges to process: {len(undirected_edges)}")

    print(f"Running Bellman-Ford...")
    start = time()  
    ans = bellmanFord(v, undirected_edges, src)
    end = time()

    print("-" * 30)
    print(f"Algorithm Finished.")
    print(f"Time Taken: {end-start:.4f} seconds")
    print("-" * 30)
    print(f"Sample output: {ans[:5]}")